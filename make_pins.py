"""10 Pinterest pins (1000x1500) for the calculator page and the Gumroad listing. Numbers match site/index.html math."""
from PIL import Image, ImageDraw, ImageFont

import glob, os
def _find(name):
    hits = glob.glob(f"/usr/share/fonts/**/{name}", recursive=True) + glob.glob(os.path.expanduser(f"~/.local/share/fonts/**/{name}"), recursive=True)
    return hits[0] if hits else None
REG = _find("LiberationSans-Regular.ttf") or _find("DejaVuSans.ttf") or _find("Arial.ttf")
BOLD = _find("LiberationSans-Bold.ttf") or _find("DejaVuSans-Bold.ttf") or REG
font = lambda s, b=False: ImageFont.truetype(BOLD if b else REG, s)  # noqa: E731
NAVY, RED, REDBG, GREEN, GREENBG, GREY, CREAM, ACC = "#1F3A5F", "#B00020", "#F4CCCC", "#1b7a3a", "#D9EAD3", "#555555", "#FBF7F0", "#E8613A"
os.makedirs("pins", exist_ok=True)
OUT = "pins/pin-{:02d}.png"


def wrap(d, text, f, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur]


def block(d, y, text, size, color, bold=True, x=80, width=840, gap=1.18):
    f = font(size, bold)
    for line in wrap(d, text, f, width):
        d.text((x, y), line, fill=color, font=f); y += int(size * gap)
    return y


def rows(d, y, data, hl=None, x=80, w=840, rh=78, size=36):
    for i, (a, b) in enumerate(data):
        bg = REDBG if hl and i in hl else ("#FFFFFF" if i % 2 == 0 else "#F1F4F8")
        d.rectangle([x, y, x + w, y + rh], fill=bg)
        bold = hl and i in hl
        d.text((x + 24, y + rh / 2), a, fill="#222", font=font(size, bold), anchor="lm")
        d.text((x + w - 24, y + rh / 2), b, fill=RED if bold else "#222", font=font(size, True), anchor="rm")
        y += rh
    return y


def footer(d, cta):
    d.rectangle([0, 1330, 1000, 1500], fill=NAVY)
    d.text((500, 1390), cta, fill="white", font=font(44, True), anchor="mm")
    d.text((500, 1450), "Quiet Profit Sheets", fill="#C9D6E8", font=font(30), anchor="mm")


def new(bg=CREAM):
    im = Image.new("RGB", (1000, 1500), bg)
    return im, ImageDraw.Draw(im)


CALC, SHEET = "Free calculator: link below", "Profit sheet: link below"

# 1 free calculator
im, d = new()
y = block(d, 120, "Free Etsy fee calculator", 92, NAVY)
y = block(d, y + 30, "See what Etsy, Shopify, Amazon or eBay takes from a sale, and what you actually keep.", 44, GREY, False)
y = rows(d, y + 60, [("Buyer pays", "$28.00"), ("Etsy fees", "-$3.11"), ("Your materials", "-$7.50"),
                     ("Shipping label", "-$5.20"), ("You keep", "$12.19")])
block(d, y + 50, "No signup. Works on your phone.", 40, NAVY)
footer(d, CALC); im.save(OUT.format(1))

# 2 what Etsy takes from $25
im, d = new()
y = block(d, 120, "What Etsy really takes from a $25 sale", 84, NAVY)
y = rows(d, y + 60, [("Transaction fee 6.5%", "$1.63"), ("Payment processing 3% + 25¢", "$1.00"),
                     ("Listing renewal", "$0.20"), ("Total Etsy fees", "$2.83")], hl={3})
y = block(d, y + 50, "That's 11.3% before materials, packaging or the shipping label.", 46, GREY, False)
block(d, y + 30, "From Offsite Ads? Add another $3.75.", 46, RED)
footer(d, CALC); im.save(OUT.format(2))

# 3 free shipping myth
im, d = new()
y = block(d, 120, "\"Free shipping\" doesn't avoid Etsy's 6.5% fee", 80, NAVY)
y = block(d, y + 40, "Charge $20 + $5 shipping, or $25 with free shipping: Etsy's fees are $2.83 either way.", 48, GREY, False)
y = block(d, y + 40, "The fee follows the money the buyer pays, wherever you put it.", 48, GREY, False)
block(d, y + 60, "Price the label into your item, and check what you keep.", 50, RED)
footer(d, CALC); im.save(OUT.format(3))

# 4 which product is losing money (sheet)
im, d = new("#FFFFFF")
y = block(d, 120, "Which of your products is losing money?", 88, NAVY)
y = block(d, y + 20, "Real numbers from our demo shop, after fees, labels, returns and ads:", 42, GREY, False)
y += 50
for name, profit, bad in [("Lavender Soy Candle", "+$30.50", 0), ("Handmade Ceramic Mug", "-$22.97", 1),
                          ("Frog Sticker Pack", "+$11.37", 0), ("Linen Tote Bag", "+$12.91", 0)]:
    d.rectangle([80, y, 920, y + 120], fill=REDBG if bad else GREENBG)
    d.text((110, y + 40), name, fill="#222", font=font(40, bool(bad)), anchor="lm")
    d.text((110, y + 88), "LOSING MONEY" if bad else "Healthy", fill=RED if bad else GREEN, font=font(32, True), anchor="lm")
    d.text((890, y + 60), profit, fill=RED if bad else "#222", font=font(48, True), anchor="rm")
    y += 136
block(d, y + 40, "A best-selling item can still lose money on every order.", 46, RED)
footer(d, SHEET); im.save(OUT.format(4))

# 5 cost x 2
im, d = new()
y = block(d, 120, "Stop pricing at \"cost x 2\"", 92, NAVY)
y = block(d, y + 30, "Fees are a % of your price, not your cost. Use this instead:", 46, GREY, False)
d.rounded_rectangle([80, y + 40, 920, y + 300], 24, fill=NAVY)
d.text((500, y + 120), "Price =", fill="white", font=font(54, True), anchor="mm")
d.text((500, y + 200), "(cost + label + fixed fees)", fill="white", font=font(44), anchor="mm")
d.text((500, y + 260), "÷ (1 − fee % − target margin)", fill="white", font=font(44), anchor="mm")
block(d, y + 360, "The free calculator does this math for Etsy, Shopify, Amazon and eBay.", 46, NAVY)
footer(d, CALC); im.save(OUT.format(5))

# 6 platform comparison on $30
im, d = new()
y = block(d, 120, "Fees on a $30 sale: Etsy vs Shopify vs Amazon vs eBay", 76, NAVY)
y = rows(d, y + 60, [("Shopify (Basic)", "$1.17"), ("Etsy", "$3.30"), ("eBay", "$4.48"),
                     ("Amazon (15% referral)", "$4.50"), ("Etsy + Offsite Ads", "$7.80")], hl={4})
block(d, y + 50, "US rates, Oct 2026, $30 item with free shipping. Shopify's monthly plan fee not included.", 34, GREY, False)
footer(d, CALC); im.save(OUT.format(6))

# 7 offsite ads
im, d = new()
y = block(d, 120, "What Etsy Offsite Ads do to a $30 sale", 84, NAVY)
y = rows(d, y + 60, [("Normal Etsy fees", "$3.30"), ("Offsite Ads 15%", "$4.50"), ("Total fees", "$7.80")], hl={2})
y = block(d, y + 50, "That's 26% of the sale gone before materials and shipping.", 48, RED)
block(d, y + 30, "Check if your margins survive it.", 46, GREY, False)
footer(d, CALC); im.save(OUT.format(7))

# 8 the sheet
im, d = new("#FFFFFF")
y = block(d, 120, "True profit per product, in one spreadsheet", 84, NAVY)
for t in ["Paste your Etsy or Shopify sales export", "Type in Amazon, eBay and market sales",
          "Fees, labels, returns and ads come out", "See net profit and margin per product",
          "Red flag on anything losing money"]:
    d.ellipse([80, y + 62, 112, y + 94], fill=ACC)
    y = block(d, y + 50, t, 46, "#222", False, x=140, width=780) + 10
block(d, y + 50, "Excel + Google Sheets. One-time $14, no subscription.", 44, NAVY)
footer(d, SHEET); im.save(OUT.format(8))

# 9 forgotten costs
im, d = new()
y = block(d, 120, "5 costs that quietly eat your Etsy profit", 84, NAVY)
for i, t in enumerate(["Fees on the shipping you charge", "The label on \"free shipping\" orders",
                       "Coupons and sale discounts", "Returns and refunds", "Etsy Ads and Offsite Ads"], 1):
    d.text((80, y + 75), str(i), fill=ACC, font=font(64, True), anchor="lm")
    y = block(d, y + 50, t, 48, "#222", False, x=150, width=770) + 26
block(d, y + 30, "Track all five, per product, in one sheet.", 46, RED)
footer(d, SHEET); im.save(OUT.format(9))

# 10 paste export
im, d = new()
y = block(d, 120, "Paste your Etsy export. See which products make money.", 80, NAVY)
y = block(d, y + 30, "Once a month, about 2 minutes. No app connected to your shop.", 46, GREY, False)
y = rows(d, y + 60, [("Mug", "-21% margin"), ("Candle", "19% margin"), ("Stickers", "43% margin")], hl={0})
footer(d, SHEET); im.save(OUT.format(10))
print("ok")
