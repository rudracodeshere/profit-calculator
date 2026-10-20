"""Writes pins/feed.xml, the RSS feed Pinterest auto-publishes from (Settings > Bulk create Pins > Auto-publish).
Pins in pins.json are released in order, PER_DAY a day from START, so the board gets a steady trickle
instead of 35 pins at once. A daily GitHub Action (.github/workflows/pin-feed.yml) reruns this and commits.
Standard library only, so it runs on a bare Actions runner. Images come from make_pins.py."""
import datetime as dt, json, os
from email.utils import format_datetime
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = "https://rudracodeshere.github.io/profit-calculator/"
START = dt.datetime(2026, 10, 17, 12, 0, tzinfo=dt.timezone.utc)
PER_DAY = 2


def released(now):
    pins = json.load(open(os.path.join(HERE, "pins.json")))
    out = []
    i = 0  # queue slot; a pin with its own "at" (ISO UTC time) goes out then and doesn't take a slot
    for p in pins:
        if "at" in p:
            at = dt.datetime.fromisoformat(p["at"].replace("Z", "+00:00"))
        else:
            at = START + dt.timedelta(days=i // PER_DAY, hours=8 * (i % PER_DAY)); i += 1
        if at <= now:
            out.append((at, p))
    return out


def item(at, p):
    # optional "img" (image name) + "link" (absolute URL) let a pin point off-site, e.g. at a Gumroad product
    img_name = (p.get("img") or p["slug"] or "fee-calculator") + ".png"
    img = BASE + "pins/feed/" + img_name
    page = BASE + (p["slug"] + "/" if p["slug"] else "")
    link = p.get("link") or page  # guid below stays page-based, so changing a pin's link never re-posts it
    size = os.path.getsize(os.path.join(ROOT, "pins", "feed", img_name))
    return f"""  <item>
    <title>{escape(p["title"])}</title>
    <link>{escape(link)}</link>
    <guid isPermaLink="false">{escape(link) + "#" + p["img"] if p.get("img") else page + "#pin-1"}</guid>
    <pubDate>{format_datetime(at)}</pubDate>
    <description><![CDATA[<p><img src="{img}" alt="{escape(p["head"])}"></p><p>{p["desc"]}</p>]]></description>
    <enclosure url="{img}" length="{size}" type="image/png"/>
    <media:content url="{img}" medium="image" type="image/png" width="1000" height="1500"/>
  </item>"""


def build(now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    items = released(now)
    items.sort(key=lambda x: x[0], reverse=True)  # newest first, like a blog feed
    last = items[0][0] if items else START
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Quiet Profit Sheets: free calculators for Etsy and small online sellers</title>
  <link>{BASE}</link>
  <atom:link href="{BASE}pins/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Free fee, pricing and profit calculators for Etsy, Shopify, print on demand and handmade sellers.</description>
  <language>en</language>
  <lastBuildDate>{format_datetime(last)}</lastBuildDate>
{chr(10).join(item(at, p) for at, p in items)}
</channel>
</rss>
"""
    path = os.path.join(ROOT, "pins", "feed.xml")
    old = open(path).read() if os.path.exists(path) else ""
    if xml != old:
        open(path, "w").write(xml)
    print(f"{len(items)} pins released; feed {'updated' if xml != old else 'unchanged'}")


if __name__ == "__main__":
    build()
