"""Pins 11-20 (Day 5). Reuses the helpers and styles from make_pins.py. Numbers match site/index.html math:
Etsy fee = 9.5% of (price + shipping) + $0.45 (6.5% transaction, 3% + 25c processing, 20c listing); Shopify Basic = 2.9% + 30c."""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
_src = open("make_pins.py").read().split("# 1 free calculator")[0]
exec(_src)  # font helpers, colors, block/rows/footer/new, CALC/SHEET

# 11 small items
im, d = new()
y = block(d, 120, "Small Etsy sales pay the highest fee rate", 88, NAVY)
y = block(d, y + 30, "Etsy's fixed 45¢ per order hits small sales hardest:", 46, GREY, False)
y = rows(d, y + 60, [("$10 sale", "$1.40 = 14.0%"), ("$20 sale", "$2.35 = 11.8%"), ("$50 sale", "$5.20 = 10.4%")], hl={0})
y = block(d, y + 50, "Bundle small items, or raise the price, so the fixed fees don't eat the margin.", 44, NAVY)
footer(d, CALC); im.save(OUT.format(11))

# 12 price handmade worked example
im, d = new()
y = block(d, 120, "How to price a handmade item for a 30% profit", 84, NAVY)
y = rows(d, y + 50, [("Materials", "$6.00"), ("Shipping label (free shipping)", "$4.50"),
                     ("Etsy fees at $18.10", "$2.17"), ("You keep", "$5.43 = 30%")])
d.rounded_rectangle([80, y + 50, 920, y + 250], 24, fill=NAVY)
d.text((500, y + 110), "($6 + $4.50 + $0.45)", fill="white", font=font(46), anchor="mm")
d.text((500, y + 190), "÷ (1 − 9.5% − 30%) = $18.10", fill="white", font=font(46, True), anchor="mm")
block(d, y + 290, "The free calculator works out this price for you.", 44, NAVY)
footer(d, CALC); im.save(OUT.format(12))

# 13 when Shopify pays off
im, d = new()
y = block(d, 120, "Etsy or Shopify? The break-even on a $30 item", 84, NAVY)
y = rows(d, y + 50, [("Etsy fees per sale", "$3.30"), ("Shopify fees per sale", "$1.17"),
                     ("You save on Shopify", "$2.13"), ("Shopify Basic plan", "$39 / month")])
y = block(d, y + 50, "You need about 19 orders a month before Shopify is cheaper.", 50, RED)
block(d, y + 30, "But Etsy brings the buyers. Shopify traffic is on you.", 42, GREY, False)
footer(d, CALC); im.save(OUT.format(13))

# 14 margin vs markup
im, d = new()
y = block(d, 120, "\"I double my cost\" is not a 50% profit", 88, NAVY)
y = rows(d, y + 50, [("Sell price", "$20.00"), ("Materials", "-$10.00"), ("Etsy fees", "-$2.35"),
                     ("Shipping label", "-$4.00"), ("Real profit", "$3.65 = 18%")], hl={4})
block(d, y + 50, "Markup is on your cost. Margin is what's left of the sale. Check yours free.", 44, NAVY)
footer(d, CALC); im.save(OUT.format(14))

# 15 hourly rate
im, d = new()
y = block(d, 120, "What are you really paying yourself per hour?", 86, NAVY)
y = rows(d, y + 50, [("Candle sells for", "$24.00"), ("Materials", "-$6.00"), ("Shipping label", "-$5.00"),
                     ("Etsy fees", "-$2.73"), ("Left for you", "$10.27"), ("45 min of work", "$13.69 / hour")], hl={5})
block(d, y + 50, "Add labor minutes per product and see your real hourly rate in the profit sheet.", 42, NAVY)
footer(d, SHEET); im.save(OUT.format(15))

# 16 monthly bookkeeping
im, d = new("#FFFFFF")
y = block(d, 120, "Etsy bookkeeping in 2 minutes a month", 88, NAVY)
for i, t in enumerate(["Download your Etsy Order Items CSV", "Paste it into one tab",
                       "Read profit per product, after every fee"], 1):
    d.ellipse([80, y + 50, 160, y + 130], fill=ACC)
    d.text((120, y + 90), str(i), fill="white", font=font(48, True), anchor="mm")
    y = block(d, y + 60, t, 48, "#222", False, x=190, width=730) + 40
block(d, y + 40, "Excel + Google Sheets. One-time $14, no app reading your shop.", 44, NAVY)
footer(d, SHEET); im.save(OUT.format(16))

# 17 discounts
im, d = new()
y = block(d, 120, "A 20% off sale can cut your profit by 39%", 86, NAVY)
y = rows(d, y + 50, [("Full price $30: you keep", "$14.00"), ("20% off, $24: you keep", "$8.57")], hl={1})
y = block(d, y + 50, "Materials ($7.50) and the label ($5.20) don't go on sale. Only your profit does.", 46, GREY, False)
block(d, y + 40, "Check a sale price before you run it.", 48, RED)
footer(d, CALC); im.save(OUT.format(17))

# 18 phone calculator
im, d = new(NAVY)
y = block(d, 160, "Etsy profit calculator", 100, "white")
y = block(d, y + 30, "Type your price, materials and shipping label. See fees, profit and margin.", 48, "#C9D6E8", False)
y = rows(d, y + 60, [("Etsy", "Included"), ("Shopify", "Included"), ("Amazon", "Included"), ("eBay", "Included")])
block(d, y + 50, "Free. No signup. Works on your phone.", 46, "white")
footer(d, CALC); im.save(OUT.format(18))

# 19 ads paying off
im, d = new()
y = block(d, 120, "Are your Etsy Ads actually making money?", 86, NAVY)
y = rows(d, y + 50, [("Ad spend this month", "$30.00"), ("Sales from ads", "5"),
                     ("Profit per sale before ads", "$9.00"), ("Real profit from ads", "$15.00")], hl={3})
y = block(d, y + 50, "If profit per sale were $5, the same ads would lose you $5.", 46, RED)
block(d, y + 30, "The profit sheet spreads ad spend across products so you can see it.", 40, GREY, False)
footer(d, SHEET); im.save(OUT.format(19))

# 20 Shopify fees on $40
im, d = new()
y = block(d, 120, "Shopify fees on a $40 sale", 92, NAVY)
y = rows(d, y + 50, [("Card fee 2.9% + 30¢", "-$1.46"), ("Materials", "-$12.00"),
                     ("Shipping label", "-$6.00"), ("You keep", "$20.54")])
y = block(d, y + 50, "Plus your monthly plan. Basic: $39, spread across every order.", 44, GREY, False)
block(d, y + 30, "Compare Shopify, Etsy, Amazon and eBay free.", 46, NAVY)
footer(d, CALC); im.save(OUT.format(20))
print("ok")
