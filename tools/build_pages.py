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
  cta_head, cta_text,   # optional overrides for the Seller Profit Sheet box
  cta_url, cta_btn,     # optional: point the box at another product (e.g. KIT)
  cta_extra,   # optional: [key in EXTRAS] second product link(s) in the box; default by cat (CAT_EXTRA)
  og_image,    # optional, pin path
  tests,       # [{set:{id:val}, click:[id], expect:{id: substring or [substrings]}}] checked in Chromium
)
Run: python3 tools/build_pages.py  (writes <slug>/index.html, sitemap.xml, tools/registry.json, homepage list)
Test: python3 tools/build_pages.py --tests [slug ...] > t.json && node tools/check_pages.js t.json
"""
import hashlib, html, importlib.util, json, pathlib, re, sys, datetime

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
# Second "get the sheet" link inside the product box: key -> (url, link text, price line)
EXTRAS = {
    "budget": ("https://quietprofitsheets.gumroad.com/l/2027-budget-spreadsheet", "2027 Budget Planner Spreadsheet", "Planning next year's money too? The %s plans income, bills and savings month by month, $9. Launch price: 50%% off with FIRST10, first 10 buyers."),
    "planner": ("https://quietprofitsheets.gumroad.com/l/christmas-budget-planner", "Christmas Budget Planner &amp; Gift Tracker", "Budgeting your own holidays? The %s keeps every gift and dollar in one sheet, $5."),
}
CAT_EXTRA = {"Platform fees": ["budget"]}
# One-line product link right under each result: url -> (name, price). A spec can set result_url, or result_url=None for none.
PRODUCTS = {
    GUMROAD: ("Seller Profit Sheet", 14),
    KIT: ("Invoice Tracker Template Google Sheets + Excel, Payment Reminder Email Templates (Word + PDF)", 9),
    "https://quietprofitsheets.gumroad.com/l/printable-size-kit": ("Etsy Print Size Guide Kit", 5),
    EXTRAS["planner"][0]: ("Christmas Budget Planner &amp; Gift Tracker", 5),
}
BUY_LINE = '<p class="buy" style="margin:12px 0 0;font-size:.95rem">Get the <a href="%s?utm_source=calculator&amp;utm_medium=result&amp;utm_content=%s" rel="noopener" style="font-weight:700">%s</a>, $%d one-time.</p>'


# Launch code (Gumroad, 50% off, 10 uses): link applies it, line says so. Only products the code is confirmed on.
LAUNCH = {GUMROAD, KIT}
LAUNCH_LINE = ' <strong>Launch price: 50% off with FIRST10, first 10 buyers.</strong></p>'


def buy_line(url, slug):
    if url is None:
        return ""
    line = BUY_LINE % (url, slug, PRODUCTS[url][0], PRODUCTS[url][1])
    if url in LAUNCH:
        line = line.replace("?utm_source", "?code=FIRST10&amp;utm_source", 1).replace("</p>", LAUNCH_LINE)
    return line

# Hand-built pages that are not generated, so the registry and sitemap know them.
STATIC = [
    dict(slug="", cat="Platform fees", nav_name="Etsy, Shopify, Amazon & eBay fee calculator", lastmod="2026-10-19"),
    dict(slug="etsy-vs-shopify", cat="Compare platforms", nav_name="Etsy vs Shopify break-even", lastmod="2026-10-19"),
    dict(slug="etsy-pricing-calculator", cat="Etsy tools", nav_name="Etsy pricing calculator", lastmod="2026-10-19"),
    dict(slug="etsy-offsite-ads-calculator", cat="Etsy tools", nav_name="Etsy Offsite Ads calculator", lastmod="2026-10-19"),
    dict(slug="about", cat="About", nav_name="About these calculators", lastmod="2026-10-15"),  # built from tools/about.html
]
CATS = ["Platform fees", "Etsy tools", "Print & design sizes", "Pricing & margins", "Maker pricing", "Compare platforms", "Invoices & getting paid"]

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
.cta{margin-top:28px;background:var(--navy);color:#fff;border-radius:12px;padding:22px}
.cta h2{color:#fff;margin-top:0}
.cta p{color:#d6e0ee}
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

DEFAULT_CTA_HEAD = "That's one product. Which of yours lose money?"
DEFAULT_CTA_TEXT = ("The <strong>Seller Profit Sheet</strong> does this math for every product at once. Paste your Etsy or Shopify "
    "sales export (or type in Amazon and eBay sales) and it shows net profit per product after fees, labels, discounts, returns "
    "and ad spend, with a red LOSING MONEY flag on anything underwater. Excel and Google Sheets, one-time $14, no subscription.")


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
    cta_link = f"{p.get('cta_url', GUMROAD)}?utm_source=calculator&amp;utm_content={slug}"
    extra = "".join('\n  <p style="margin:14px 0 0;font-size:.95rem">%s</p>' % (EXTRAS[k][2] % f'<a href="{EXTRAS[k][0]}?{"code=FIRST10&amp;" if k == "budget" else ""}utm_source=calculator&amp;utm_content={slug}" rel="noopener" style="color:#fff;font-weight:700">{EXTRAS[k][1]}</a>')
                    for k in p.get("cta_extra", CAT_EXTRA.get(p["cat"], [])))
    gig = p.get("gig", CAT_GIG.get(p["cat"], "profit"))
    cta_html = "" if p.get("cta_head", "") is None else f"""<div class="cta">
  <h2>{p.get('cta_head', DEFAULT_CTA_HEAD)}</h2>
  <p>{p.get('cta_text', DEFAULT_CTA_TEXT)}</p>
  <a class="btn" href="{cta_link}" rel="noopener">{p.get('cta_btn', 'Get the Seller Profit Sheet')}</a>{extra}
</div>
"""
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

<div class="card">
  <div class="grid">
    <div>
{p['form']}
    </div>
    <div>
      {p.get('out', DEFAULT_OUT)}
      {buy_line(p.get('result_url', p.get('cta_url', GUMROAD)), slug)}
    </div>
  </div>
  <p class="note">{p['note']}</p>
</div>

{cta_html}{dfy_html}
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
<footer>Made by <a href="https://quietprofitsheets.gumroad.com/l/seller-profit-sheet?utm_source=about">Quiet Profit Sheets</a>.</footer>
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
              "Read-only check of the published site. It loads every page in the live sitemap, fails on any JavaScript console error or page error, checks that every Gumroad buy link returns HTTP 200, and checks that links carrying the FIRST10 discount keep `?code=FIRST10` and point only at the Seller Profit Sheet, the Get Paid Kit, and the 2027 Budget Planner.",
              "",
              "```bash",
              "npm install --no-save playwright",
              "npx playwright install chromium",
              "node tools/smoke_live.js",
              "```",
              "",
              "Pass a base URL to target a different host: `node tools/smoke_live.js https://rudracodeshere.github.io/profit-calculator/`. The script only sends GET requests and does not modify the repo or the site. GitHub Actions runs it after a successful GitHub Pages deploy.",
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
