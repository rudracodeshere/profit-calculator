#!/usr/bin/env python3
"""Tell Bing, Yandex, Seznam and Naver (IndexNow) about every URL in sitemap.xml.
Run after a deploy is live: python3 tools/indexnow.py [url ...]  (no args = whole sitemap)
The key file <KEY>.txt sits at the site root; its folder scopes the URLs we may submit."""
import json, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://rudracodeshere.github.io/profit-calculator/"
KEY = next(p.stem for p in ROOT.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem))
urls = sys.argv[1:] or re.findall(r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text())
body = json.dumps({"host": "rudracodeshere.github.io", "key": KEY, "keyLocation": f"{BASE}{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print(r.status, f"submitted {len(urls)} urls")
except urllib.error.HTTPError as e:
    print(e.code, e.read()[:300])
    sys.exit(1)
