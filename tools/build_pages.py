#!/usr/bin/env python3
"""Build calculator pages from tools/pages/*.py specs.

Each spec module defines PAGE = dict(
  slug, cat, title, desc, h1, lead, nav_name,   # nav_name: short link text
  form,        # HTML for the inputs column
  out,         # HTML for the results column (optional; default table+verdict)
  js,          # JS body; helpers $, n, m, pc, setRows, verdict are in scope; must define calc()
  note,        # small print under the tool (rates/date)
  body,        # HTML article: how it works, formula, worked example
  faqs,        # [(question, answer_html)]
  related,     # [slug, ...] 3-6 related pages
  result_url,  # optional: product in the one box under the result (default cta_url, then the Seller Profit Sheet); None = no box
  buy_lead,    # optional: first words of the box line
  starter_line, # optional: True adds the $3 Etsy Price Calculator Sheet line inside the box
  og_image,    # optional, pin path
  tests,       # [{set:{id:val}, click:[id], expect:{id: substring or [substrings]}}] checked in Chromium
)
Run: python3 tools/build_pages.py  (writes <slug>/index.html, sitemap.xml, tools/registry.json, homepage list)
Test: python3 tools/build_pages.py --tests [slug ...] > t.json && node tools/check_pages.js t.json
"""
import hashlib, html, importlib.util, json, pathlib, re, sys, datetime, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://rudracodeshere.github.io/profit-calculator/"
GUMROAD = "https://quietprofitsheets.gumroad.com/l/seller-profit-sheet"
KIT = "https://quietprofitsheets.gumroad.com/l/get-paid-kit"
TODAY = datetime.date.today().isoformat()
FIVERR = "https://www.fiverr.com/rudrasharma_in"
# Done-for-you offer under each tool: (link, line). A page spec can set gig: "seo" | "profit" | "sheet" | "pod", or None for no line.
GIGS = {
    "seo": (FIVERR + "/write-etsy-seo-titles-13-tags-and-descriptions-for-your-listings", "Rather have someone rewrite your Etsy titles, 13 tags and descriptions for you? I do it on Fiverr, from $5."),
    "profit": (FIVERR + "/write-etsy-seo-titles-13-tags-and-descriptions-for-your-listings", "Prices sorted? The next fix is getting found: I rewrite Etsy titles, 13 tags and descriptions on Fiverr, from $5."),
    "sheet": (FIVERR + "/build-a-custom-excel-or-google-sheets-tracker-with-formulas", "Need a custom Excel or Google Sheets tracker built around how you work? I build them on Fiverr, from $5."),
    "pod": (FIVERR + "/find-which-of-your-etsy-products-lose-money-and-fix-your-prices", "Selling print on demand shirts or mugs on Etsy? I write the titles and 13 tags that get POD listings found, on Fiverr."),
}
CAT_GIG = {"Invoices & getting paid": "sheet"}
BUDGET = "https://quietprofitsheets.gumroad.com/l/2027-budget-spreadsheet"
PLANNER = "https://quietprofitsheets.gumroad.com/l/christmas-budget-planner"
SIZEKIT = "https://quietprofitsheets.gumroad.com/l/printable-size-kit"
STARTER = "https://quietprofitsheets.gumroad.com/l/etsy-price-calculator-sheet"  # $3, no FIRST10
PETSIT = "https://quietprofitsheets.gumroad.com/l/pet-sitting-spreadsheet"  # $49, no FIRST10
# Launch code (Gumroad, 50% off, 10 uses). Valid only on these three; never add it to the $5 products.
LAUNCH = {GUMROAD: ("$7", "$14"), KIT: ("$4.50", "$9"), BUDGET: ("$4.50", "$9")}


def gum(url, medium, slug):
    """Gumroad link with FIRST10 (launch products only) and utm tags."""
    code = "code=FIRST10&amp;" if url in LAUNCH else ""
    return f"{url}?{code}utm_source=calculator&amp;utm_medium={medium}&amp;utm_content={slug}"


# The one product box right under each result: url -> (lead-in, product name, price text). A spec can set result_url, or None for no box.
PRODUCTS = {
    GUMROAD: ("See this for every product at once, net profit after fees, shipping and ads: the", "Seller Profit Sheet", "<strong>50% off with code FIRST10</strong>: $7 (normally $14), first 10 buyers. Excel + Google Sheets, one-time."),
    KIT: ("Track every invoice and know who to chase today: the", "Invoice Tracker + 10 reminder emails", "<strong>50% off with code FIRST10</strong>: $4.50 (normally $9), first 10 buyers."),
    BUDGET: ("Plan all of 2027 in one sheet: the", "2027 Budget Planner Spreadsheet", "<strong>50% off with code FIRST10</strong>: $4.50 (normally $9), first 10 buyers."),
    PLANNER: ("Budget per person, gift list and how much to save each payday: the", "Christmas Budget Spreadsheet + Gift Tracker", "$5. Google Sheets, Excel and printable PDF."),
    PETSIT: ("Every booking priced for you, holiday rates included: the", "Pet Sitting Business Tracker", "$49. Excel + Google Sheets, one-time."),
    SIZEKIT: ("Ready-made \"sizes included\" images and a print guide for your buyers: the", "Etsy Print Size Guide Kit", "$5."),
}
# One line under the intro, visible above the fold on mobile (snippet B): url -> (question, link text)
TOPLINE = {
    GUMROAD: ("Want it for every product at once?", "Seller Profit Sheet, $7 with FIRST10"),
    KIT: ("Chasing more than one invoice?", "Invoice Tracker + 10 reminder emails, $4.50 with FIRST10"),
    PLANNER: ("Want the gift list and per-person budgets too?", "Christmas Budget Spreadsheet, $5"),
    PETSIT: ("Want every booking priced for you?", "Pet Sitting Business Tracker, $49"),
    SIZEKIT: ("Need the listing images too?", "Etsy Print Size Guide Kit, $5"),
}


def buy_box(url, slug, lead=None, starter=False):
    """The one product box under the result: a plain line, a button, and (Etsy pricing pages) the $3 starter line."""
    if url is None:
        return ""
    a, name, price = PRODUCTS[url]
    btn = f"Get the {name}" + (f": {LAUNCH[url][0]} with FIRST10" if url in LAUNCH else "")
    return (f'<div class="buybox">\n        <p class="buy">{lead or a} <strong>{name}</strong>{"." if url in LAUNCH else ","} {price}</p>\n'
            f'        <a class="btn" href="{gum(url, "result", slug)}" rel="noopener">{btn}</a>{starter_line(slug) if starter else ""}\n      </div>')


def top_line(url, slug):
    if url not in TOPLINE:
        return ""
    q, text = TOPLINE[url]
    return (f'<p class="topbuy" style="margin:6px 0 14px;font-size:.92rem">Free tool, no sign-up. {q} '
            f'<a href="{gum(url, "topline", slug)}" rel="noopener">{text}</a>.</p>\n')


def pin_save(url, og, title):
    q = urllib.parse.urlencode({"url": url, "media": og, "description": title})
    return f'\n      <p class="note"><a href="https://www.pinterest.com/pin/create/button/?{html.escape(q)}" target="_blank" rel="noopener">Save this calculator to Pinterest</a></p>'


def starter_line(slug):
    """One line under the buy button on Etsy pricing pages (spec: starter_line=True)."""
    return (f'\n        <p style="margin:10px 0 0;font-size:.9rem">Just want the price math? <a href="{gum(STARTER, "starter-line", slug)}" '
            f'rel="noopener" style="font-weight:700">Etsy Price Calculator Sheet, $3</a></p>')



# Hand-built pages that are not generated, so the registry and sitemap know them.
STATIC = [
    dict(slug="", cat="Platform fees", nav_name="Etsy, Shopify, Amazon & eBay fee calculator", lastmod="2026-10-23"),
    dict(slug="etsy-vs-shopify", cat="Compare platforms", nav_name="Etsy vs Shopify break-even", lastmod="2026-10-23"),
    dict(slug="etsy-pricing-calculator", cat="Etsy tools", nav_name="Etsy pricing calculator", lastmod="2026-10-23"),
    dict(slug="etsy-offsite-ads-calculator", cat="Etsy tools", nav_name="Etsy Offsite Ads calculator", lastmod="2026-10-23"),
    dict(slug="about", cat="About", nav_name="About these calculators", lastmod="2026-10-21"),  # built from tools/about.html
]
CATS = ["Platform fees", "Etsy tools", "Print & design sizes", "Pricing & margins", "Maker pricing", "Compare platforms", "Invoices & getting paid", "Budgets & planning"]

CSS = """:root{--ink:#1d2430;--muted:#5b6575;--line:#dde3ea;--bg:#f6f8fb;--card:#fff;--navy:#1F3A5F;--red:#B00020;--redbg:#fbe9eb;--green:#1b7a3a;--greenbg:#e7f4ea;--accent:#e8613a}
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);background:var(--bg)}
main{max-width:860px;margin:0 auto;padding:24px 16px 60px}
h1{font-size:clamp(1.6rem,4vw,2.2rem);line-height:1.2;margin:.2em 0 .3em;color:var(--navy)}
h2{font-size:1.3rem;margin:2em 0 .5em;color:var(--navy)}
h3{font-size:1.05rem;margin:1.4em 0 .3em}
p.lead{color:var(--muted);margin-top:0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:700px){.grid{grid-template-columns:1fr}}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:16px}
.tabs button{flex:1;min-width:80px;padding:10px;border:1px solid var(--line);background:#fff;border-radius:8px;font:inherit;font-weight:600;cursor:pointer;color:var(--muted)}
.tabs button[aria-pressed=true]{background:var(--navy);color:#fff;border-color:var(--navy)}
label{display:block;font-size:.9rem;font-weight:600;margin:12px 0 4px}
label small{font-weight:400;color:var(--muted)}
.in{display:flex;align-items:center;border:1px solid var(--line);border-radius:8px;background:#fff}
.in span{padding:0 10px;color:var(--muted)}
.in input,.in select{flex:1;border:0;padding:10px 10px 10px 0;font:inherit;background:transparent;min-width:0}
.in input:first-child{padding-left:10px}
select.full{width:100%;padding:10px;border:1px solid var(--line);border-radius:8px;font:inherit;background:#fff}
.check{display:flex;gap:8px;align-items:center;font-weight:400;margin-top:14px}
table{width:100%;border-collapse:collapse;font-size:.95rem}
td{padding:7px 0;border-bottom:1px solid var(--line)}
td:last-child{text-align:right;font-variant-numeric:tabular-nums;padding-left:8px}
tr.total td{font-weight:700;border-bottom:0;font-size:1.1rem;padding-top:12px}
.big{border:1px solid var(--line);border-radius:10px;padding:14px;text-align:center;margin-bottom:10px}
.big b{display:block;font-size:1.7rem;font-variant-numeric:tabular-nums;color:var(--navy)}
.verdict{margin-top:14px;padding:12px 14px;border-radius:8px;font-weight:600}
.verdict:empty{display:none}
.verdict.bad{background:var(--redbg);color:var(--red)}
.verdict.ok{background:var(--greenbg);color:var(--green)}
.buybox{margin-top:14px;padding:14px 16px;border:2px solid var(--accent);border-radius:10px;background:#fff8f5}
.buybox p.buy{margin:0 0 8px;font-size:.95rem}
.buybox .btn{margin-top:0}
.btn{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;font-weight:700;padding:12px 20px;border-radius:8px;margin-top:6px}
.btn:hover{filter:brightness(1.05)}
.note{font-size:.85rem;color:var(--muted)}
.formula{background:#fff;border-left:4px solid var(--navy);padding:10px 14px;border-radius:4px;font-weight:600}
.related{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:8px;padding:0;list-style:none}
.related a{display:block;background:#fff;border:1px solid var(--line);border-radius:8px;padding:10px 12px;text-decoration:none;color:var(--navy);font-weight:600}
.related a:hover{border-color:var(--navy)}
nav{font-size:.9rem;margin-bottom:8px}
.dfy{margin:14px 0 0;padding:12px 16px;border:1px dashed var(--line);border-radius:10px;background:#fff;font-size:.95rem}
footer{margin-top:40px;font-size:.8rem;color:var(--muted)}
th{text-align:left;font-size:.85rem;color:var(--muted);padding:6px 0;border-bottom:1px solid var(--line)}
.wide td,.wide th{text-align:right;padding:6px 4px}
.wide td:first-child,.wide th:first-child{text-align:left}"""

HELPERS = """var $=function(id){return document.getElementById(id)};
var n=function(id){var v=parseFloat($(id).value);return isFinite(v)&&v>0?v:0};
var m=function(x){return (x<0?'-$':'$')+Math.abs(x).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})};
var pc=function(x,d){return (x*100).toFixed(d===undefined?1:d)+'%'};
function setRows(rows,id){var h='';rows.forEach(function(r){h+='<tr'+(r[2]?' class="'+r[2]+'"':'')+'><td>'+r[0]+'</td><td>'+r[1]+'</td></tr>'});$(id||'rows').innerHTML=h}
function verdict(ok,text,id){var v=$(id||'verdict');v.className='verdict '+(ok?'ok':'bad');v.textContent=text}"""

DEFAULT_OUT = '<table aria-live="polite"><tbody id="rows"></tbody></table>\n      <div id="verdict" class="verdict"></div>'



def load_specs(only=None):
    specs = []
    for f in sorted((ROOT / "tools" / "pages").glob("*.py")):
        if only and f.stem not in only:
            continue
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        p = dict(mod.PAGE)
        p["_file"] = f.name
        specs.append(p)
    return specs


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def render(p, names):
    slug = p["slug"]
    url = BASE + slug + "/"
    e = html.escape
    og = BASE + p.get("og_image", "pins/pin-01.png")
    faq_html = "".join(f"<h3>{q}</h3>\n<p>{a}</p>\n" for q, a in p["faqs"])
    ld = [
        {"@context": "https://schema.org", "@type": "WebApplication", "name": strip_tags(p["h1"]), "url": url,
         "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": p["desc"]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in p["faqs"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Seller calculators", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": p["nav_name"], "item": url}]},
    ]
    rel = "".join(f'<li><a href="../{s}/">{e(names[s])}</a></li>' for s in p["related"])
    result_url = p.get('result_url', p.get('cta_url', GUMROAD))
    gig = p.get("gig", CAT_GIG.get(p["cat"], "profit"))
    dfy_html = "" if gig is None else '<p class="dfy">%s <a href="%s" rel="noopener">See the offer on Fiverr</a></p>\n' % (GIGS[gig][1], GIGS[gig][0])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['desc'])}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(strip_tags(p['h1']))}">
<meta property="og:description" content="{e(p['desc'])}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<link rel="icon" href="../logo.png">
<style>
{CSS}
</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<main>
<nav><a href="../">&larr; All seller calculators</a></nav>
<h1>{p['h1']}</h1>
<p class="lead">{p['lead']}</p>
{top_line(p.get('top_url', result_url), slug)}
<div class="card">
  <div class="grid">
    <div>
{p['form']}
    </div>
    <div>
      {p.get('out', DEFAULT_OUT)}
      {buy_box(result_url, slug, p.get('buy_lead'), p.get('starter_line'))}{pin_save(url, og, p['title']) if p.get('pin_save') else ''}
    </div>
  </div>
  <p class="note">{p['note']}</p>
</div>

{dfy_html}
{p['body']}

<h2>Questions</h2>
{faq_html}
<h2>Related calculators</h2>
<ul class="related">{rel}</ul>

<footer>Independent tool, not affiliated with any marketplace or payment company. Fee rates are US defaults and change over time; every rate above is editable. Made by <a href="{p.get('store_url', 'https://quietprofitsheets.gumroad.com/?utm_source=calculator')}">Quiet Profit Sheets</a>. <a href="../#all">All calculators</a> &middot; <a href="../about/">About &amp; sources</a>.</footer>
</main>
<script>
(function(){{
{HELPERS}
{p['js']}
document.querySelectorAll('input,select').forEach(function(el){{el.addEventListener('input',calc);el.addEventListener('change',calc)}});
calc();
}})();
</script>
</body>
</html>
"""


def render_about():
    body = (ROOT / "tools" / "about.html").read_text()
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>About: Free Seller Calculators by Quiet Profit Sheets</title>
<meta name="description" content="Who makes these free seller calculators, how the math is checked, and where every fee rate comes from, with links to each platform's official fee page.">
<link rel="canonical" href="{BASE}about/">
<link rel="icon" href="../logo.png">
<style>
{CSS}
</style>
</head>
<body>
<main>
<nav><a href="../">&larr; All seller calculators</a></nav>
{body}
<footer>Made by <a href="https://quietprofitsheets.gumroad.com/?utm_source=calculator&amp;utm_content=about">Quiet Profit Sheets</a>.</footer>
</main>
</body>
</html>
"""


def write_readme(reg):
    lines = ["# Free seller calculators", "",
             f"Free, no-signup calculators for Etsy, Shopify, eBay, Amazon, Poshmark and freelance sellers. Live site: {BASE}", "",
             "Every calculator runs in the browser, uses editable US fee rates, and has its worked example checked by an automated browser test.", ""]
    for c in CATS:
        items = [r for r in reg if r["cat"] == c and r["slug"]]
        if items:
            lines += [f"## {c}", ""] + [f"- [{r['nav_name']}]({BASE}{r['slug']}/)" for r in items] + [""]
    lines += [f"[About and fee sources]({BASE}about/)", "",
              "Pages are generated from `tools/pages/*.py` by `tools/build_pages.py`; test with `tools/check_pages.js`.",
              "The pin feed is checked with `python3 tools/pins/test_feed.py` (valid XML, unique item guids).",
              "",
              "## Live smoke test",
              "",
              "Read-only check of the published site. It loads every page in the live sitemap and fails on any JavaScript console error or page error. Gumroad buy links are checked offline: every product slug must be one this site sells, and the FIRST10 discount may appear only on the Seller Profit Sheet, the Get Paid Kit, and the 2027 Budget Planner, with `?code=FIRST10` kept on the link. That mode does not request gumroad.com.",
              "",
              "```bash",
              "npm install --no-save playwright",
              "npx playwright install chromium",
              "node tools/smoke_live.js",
              "```",
              "",
              "Set `SMOKE_FETCH_GUMROAD=1` to also fetch each Gumroad product URL and require HTTP 200. GitHub Actions sets that only for a manual run. After a Pages deploy the check stays offline, so those runs do not count as Gumroad views.",
              "",
              "Pass a base URL to target a different host: `node tools/smoke_live.js https://rudracodeshere.github.io/profit-calculator/`. The script does not modify the repo or the site.",
              ""]
    (ROOT / "README.md").write_text("\n".join(lines))


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    specs = load_specs(only)
    if "--tests" in sys.argv:
        print(json.dumps([dict(slug=p["slug"], tests=p.get("tests", [])) for p in specs if not only or p["slug"] in only]))
        return
    names = {s["slug"]: s["nav_name"] for s in STATIC}
    names[""] = "Fee & profit calculator"
    for p in specs:
        if p["slug"] in names:
            sys.exit(f"duplicate slug {p['slug']}")
        names[p["slug"]] = p["nav_name"]
    for p in specs:
        for r in p["related"]:
            if r not in names:
                if not only:
                    sys.exit(f"{p['_file']}: unknown related slug {r}")
                names[r] = r.replace("-", " ").capitalize()
        if p["cat"] not in CATS:
            sys.exit(f"{p['_file']}: unknown cat {p['cat']}")
        out = ROOT / p["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(render(p, names))
    if only:  # partial build: pages only, leave sitemap/registry/homepage alone
        print(f"built {len(specs)} pages (partial)")
        return
    reg_path = ROOT / "tools" / "registry.json"
    prev = {r["slug"]: r for r in json.loads(reg_path.read_text())} if reg_path.exists() else {}
    reg = [dict(slug=s["slug"], cat=s["cat"], nav_name=s["nav_name"], lastmod=s["lastmod"]) for s in STATIC]
    for p in specs:
        h = hashlib.sha1(render(p, names).encode()).hexdigest()[:12]
        old = prev.get(p["slug"], {})
        lm = old["lastmod"] if old.get("hash") == h else TODAY
        reg.append(dict(slug=p["slug"], cat=p["cat"], nav_name=p["nav_name"], lastmod=lm, hash=h))
    reg_path.write_text(json.dumps(reg, indent=1))
    (ROOT / "about").mkdir(exist_ok=True)
    (ROOT / "about" / "index.html").write_text(render_about())
    write_readme(reg)
    urls = "\n".join(f"  <url><loc>{BASE}{r['slug'] + '/' if r['slug'] else ''}</loc><lastmod>{r['lastmod']}</lastmod></url>" for r in reg)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    # homepage directory block between markers
    idx = ROOT / "index.html"
    h = idx.read_text()
    groups = []
    for c in CATS:
        items = [r for r in reg if r["cat"] == c and r["slug"]]
        if items:
            lis = "".join(f'<li><a href="{r["slug"]}/">{html.escape(r["nav_name"])}</a></li>' for r in items)
            groups.append(f'<h3>{c}</h3>\n<ul class="related">{lis}</ul>')
    block = '<!--ALL-->\n<h2 id="all">All free seller calculators</h2>\n' + "\n".join(groups) + "\n<!--/ALL-->"
    if "<!--ALL-->" in h:
        h = re.sub(r"<!--ALL-->.*?<!--/ALL-->", lambda _: block, h, flags=re.S)
        idx.write_text(h)
    print(f"built {len(specs)} pages; {len(reg)} urls in sitemap")



if __name__ == "__main__":
    main()
