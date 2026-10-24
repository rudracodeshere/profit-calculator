#!/usr/bin/env python3
"""Make og.png, the 1200x630 link-preview image used by every page."""
import pathlib, re
from PIL import Image, ImageDraw, ImageFont
ROOT = pathlib.Path(__file__).resolve().parent.parent
import subprocess
def _find(name):
    out = subprocess.run(["fc-list", "--format", "%{file}\n"], capture_output=True, text=True).stdout.split()
    return next((f for f in out if f.endswith("/" + name)), None)
REG = _find("LiberationSans-Regular.ttf") or _find("DejaVuSans.ttf")
BOLD = _find("LiberationSans-Bold.ttf") or _find("DejaVuSans-Bold.ttf") or REG
W, H = 1200, 630
img = Image.new("RGB", (W, H), "#1F3A5F")
d = ImageDraw.Draw(img)
def center(y, text, size, fill, bold=True):
    f = ImageFont.truetype(BOLD if bold else REG, size)
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)
center(120, "What does the platform take?", 72, "#ffffff")
center(240, "Etsy · Shopify · Amazon · eBay", 52, "#e8613a")
center(340, "Fee and profit calculator", 56, "#ffffff")
d.rounded_rectangle((300, 450, 900, 520), 14, outline="#ffffff", width=3)
center(463, "See what you keep", 38, "#ffffff")
center(565, "rudracodeshere.github.io/profit-calculator", 28, "#c9d4e3", bold=False)
img.save(ROOT / "og.png", optimize=True)
print("og.png", img.size)
