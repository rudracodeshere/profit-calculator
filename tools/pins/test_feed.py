#!/usr/bin/env python3
"""Check the generated Pinterest RSS feed.

Runs the same generator as the daily pin release (tools/pins/build_feed.py) and
checks that the XML it would write is well-formed and that every item guid is
unique. Read-only: a write to pins/feed.xml is intercepted, and the file is
restored if anything still changes it.
"""
import contextlib
import io
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_feed

FEED = os.path.join(build_feed.ROOT, "pins", "feed.xml")


def generated_xml():
    """Return the feed XML build() would write, without touching the file."""
    captured = []
    real_open = open

    def patched(file, mode="r", *args, **kwargs):
        path = os.fspath(file)
        if os.path.abspath(path) == os.path.abspath(FEED) and "w" in mode:
            buf = io.StringIO()
            captured.append(buf)
            return buf
        return real_open(file, mode, *args, **kwargs)

    build_feed.open = patched
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            build_feed.build()
    finally:
        del build_feed.open
    if captured:
        return captured[-1].getvalue()
    with real_open(FEED, encoding="utf-8") as f:
        return f.read()


def problems(xml):
    found = []
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as err:
        return [f"not well-formed XML: {err}"], 0
    if root.tag != "rss":
        found.append(f"root element is <{root.tag}>, expected <rss>")
    if root.get("version") != "2.0":
        found.append(f"rss version is {root.get('version')!r}, expected '2.0'")
    channel = root.find("channel")
    if channel is None:
        found.append("missing <channel>")
        return found, 0
    guids = []
    for i, item in enumerate(channel.findall("item"), start=1):
        guid = item.find("guid")
        text = "" if guid is None or guid.text is None else guid.text.strip()
        if not text:
            title = item.findtext("title") or "(no title)"
            found.append(f"item {i} ({title}) has no guid")
        else:
            guids.append(text)
    seen = {}
    for guid in guids:
        seen[guid] = seen.get(guid, 0) + 1
    for guid, count in seen.items():
        if count > 1:
            found.append(f"duplicate guid ({count} items): {guid}")
    return found, len(guids)


def main():
    before = open(FEED, "rb").read() if os.path.exists(FEED) else None
    try:
        xml = generated_xml()
    finally:
        if before is None:
            if os.path.exists(FEED):
                os.remove(FEED)
                print("removed pins/feed.xml created during the check", file=sys.stderr)
        else:
            after = open(FEED, "rb").read()
            if after != before:
                with open(FEED, "wb") as f:
                    f.write(before)
                print("restored pins/feed.xml", file=sys.stderr)
    found, count = problems(xml)
    if found:
        print("FAIL pin feed")
        for line in found:
            print(f"  {line}")
        return 1
    print(f"ok   pin feed: well-formed RSS 2.0, {count} items, {count} unique guids")
    return 0


if __name__ == "__main__":
    sys.exit(main())
