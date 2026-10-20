"""Pinterest pin images (1000x1500), one per page in pins.json, saved to pins/feed/<name>.png.
build_feed.py turns them into the RSS feed Pinterest auto-publishes from. Rerun after editing pins.json."""
import json, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "pins", "feed")
FONTS = "/usr/share/fonts/opentype/inter/"
font = lambda s, w="Bold": ImageFont.truetype(FONTS + f"Inter-{w}.otf", s)  # noqa: E731

# (background, ink, accent, card) per theme; pins rotate through them
THEMES = [("#FBF7F0", "#1F3A5F", "#E8613A", "#FFFFFF"),
          ("#EEF4F1", "#173F35", "#2E8B6A", "#FFFFFF"),
          ("#F5F0FA", "#3A2A5C", "#8A5CD0", "#FFFFFF"),
          ("#1F3A5F", "#FFFFFF", "#F2B544", "#2A4A73")]


def cta(slug):
    if "generator" in slug:
        return "Free email generator  ·  no signup"
    if "checker" in slug:
        return "Free tag checker  ·  no signup"
    return "Free calculator  ·  no signup"


def name(slug, img=None):
    return img or slug or "fee-calculator"


def wrap(d, text, f, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur]


def draw(pin, theme, size=96):
    bg, ink, acc, card = theme
    dark = bg == "#1F3A5F"
    im = Image.new("RGB", (1000, 1500), bg)
    d = ImageDraw.Draw(im)
    # kicker pill
    f = font(34, "SemiBold")
    k = pin["kicker"].upper()
    w = d.textlength(k, font=f)
    d.rounded_rectangle([80, 96, 80 + w + 56, 156], 30, fill=acc)
    d.text((108, 126), k, fill="#FFFFFF" if not dark else "#1F3A5F", font=f, anchor="lm")
    # headline, shrink until it fits in 4 lines
    hf = font(size, "ExtraBold")
    lines = wrap(d, pin["head"], hf, 840)
    y = 200
    for line in lines:
        d.text((80, y), line, fill=ink, font=hf); y += int(size * 1.12)
    if pin.get("art"):  # product art on a card instead of bullets (path relative to this folder)
        art = Image.open(os.path.join(HERE, pin["art"])).convert("RGB")
        art = art.resize((840, round(840 * art.height / art.width)), Image.LANCZOS)
        top = max(y + 50, (y + 1150 - art.height - 40) // 2)
        d.rounded_rectangle([60, top, 940, top + art.height + 40], 36, fill=card)
        im.paste(art, (80, top + 20))
        rows, h = [], art.height + 40
    else:
        rows, h = None, 0
    # bullets on a card
    bf = font(46, "Medium")
    if rows is None:
        rows = [wrap(d, b, bf, 680) for b in pin["bullets"]]
        h = sum(len(r) * 58 + 64 for r in rows) + 40
        top = max(y + 50, (y + 1150 - h) // 2)  # centre the card between headline and button
        d.rounded_rectangle([60, top, 940, top + h], 36, fill=card)
    y = top + 48
    for r in rows:
        d.ellipse([110, y, 170, y + 60], fill=acc)
        d.line([(125, y + 31), (137, y + 43), (156, y + 19)], fill="#FFFFFF", width=7, joint="curve")
        for line in r:
            d.text((200, y + 4), line, fill="#FFFFFF" if dark else "#222222", font=bf); y += 58
        y += 64
    # call to action
    cy = max(top + h + 60, 1150)
    d.rounded_rectangle([80, cy, 920, cy + 120], 60, fill=acc)
    d.text((500, cy + 60), pin.get("cta") or cta(pin["slug"]), fill="#FFFFFF" if not dark else "#1F3A5F", font=font(46, "Bold"), anchor="mm")
    if cy + 120 > 1370 and size > 64:  # too tall: retry with a smaller headline
        return draw(pin, theme, size - 8)
    d.text((500, 1420), pin.get("foot", "Quiet Profit Sheets  ·  rudracodeshere.github.io/profit-calculator"), fill=ink, font=font(26, "Medium"), anchor="mm")
    return im


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pins = json.load(open(os.path.join(HERE, "pins.json")))
    k = 0  # pins with a fixed "theme" don't move the rotation, so inserting one keeps everyone else's colours
    for p in pins:
        t = p["theme"] if "theme" in p else k % len(THEMES)
        k += "theme" not in p
        draw(p, THEMES[t]).save(os.path.join(OUT, name(p["slug"], p.get("img")) + ".png"), optimize=True)
    print(len(pins), "pins ->", OUT)
