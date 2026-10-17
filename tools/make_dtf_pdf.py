#!/usr/bin/env python3
"""One-page printable DTF / t-shirt design size chart linked from /dtf-transfer-size-chart/.
Same numbers as tools/pages/dtf-transfer-size-chart.py. Needs reportlab. Run: python3 tools/make_dtf_pdf.py"""
import pathlib
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

OUT = pathlib.Path(__file__).resolve().parent.parent / "dtf-transfer-size-chart" / "dtf-size-chart.pdf"
BY_SIZE = [("XS", '8.5" - 9.5"', "XS (4-5)", '8" - 9"'), ("S", '9.5" - 10.5"', "S (6-8)", '9" - 9.5"'),
           ("M", '10.5" - 11"', "M (10-12)", '9.5" - 10.5"'), ("L", '11"', "L (14-16)", '10.5" - 11"'),
           ("XL", '11" - 11.5"', "XL (18-20)", '11" - 11.5"'), ("2XL", '11.5" - 12"', "Toddler 2T-4T", '6" - 7"'),
           ("3XL", '12" - 12.5"', "Infant 0-24M", '4" - 5"'), ("4XL", '12.5" - 13"', "", ""), ("5XL", '13" - 13.5"', "", "")]
PLACES = [("T-shirt full front", '10" - 11.5"', '11" - 13"'), ("T-shirt full back", '11" - 12.5"', '14" - 16"'),
          ("Left chest (adult)", '3.5" - 4"', '3.5" - 4"'), ("Back collar (tag)", '2.5" - 3"', '2.5" - 3"'),
          ("Short sleeve", '3" - 4"', '2" - 3.5"'), ("Long sleeve, down the arm", '2"', '14" - 18"'),
          ("Oversized tee front", '12.5" - 14"', '14" - 16"'), ("Oversized tee back", '13" - 15"', '15" - 18"'),
          ("Hoodie front, above the pocket", '10" - 11.5"', '11" - 13"'), ("Hoodie back", '13" - 15"', '16" - 18"'),
          ("Tank top front", '9" - 10"', '12" - 14"'), ("Youth front", '8" - 9"', '9" - 11"'),
          ("Youth left chest", '2.5" - 3"', '2.5" - 3"'), ("Tote bag", '9"', '9"'), ("Cap front", '3" - 4"', '2" - 2.5"')]

c = canvas.Canvas(str(OUT), pagesize=letter)
c.setTitle("DTF transfer size chart")
pw, ph = letter
m = 0.6 * inch
y = ph - m
c.setFont("Helvetica-Bold", 20); c.drawString(m, y - 6, "DTF transfer and t-shirt design size chart"); y -= 28
c.setFont("Helvetica", 10); c.setFillGray(0.35)
c.drawString(m, y, "Starting sizes in inches. Lay the transfer on your actual blank before pressing. Artwork pixels = width x 300."); y -= 26
c.setFillGray(0)

def table(y, heads, rows, cols):
    c.setFont("Helvetica-Bold", 10.5)
    for x, h in zip(cols, heads): c.drawString(x, y, h)
    y -= 5; c.setLineWidth(0.6); c.line(m, y, pw - m, y); y -= 14
    c.setFont("Helvetica", 10.5)
    for i, r in enumerate(rows):
        if i % 2:
            c.setFillGray(0.95); c.rect(m, y - 4, pw - 2 * m, 15, stroke=0, fill=1); c.setFillGray(0)
        for x, v in zip(cols, r): c.drawString(x, y, v)
        y -= 15
    return y - 14

c.setFont("Helvetica-Bold", 13); c.drawString(m, y, "Full front or back width by shirt size"); y -= 18
y = table(y, ["Adult size", "Design width", "Youth / kids", "Design width"], BY_SIZE, [m, m + 1.3 * inch, m + 3.4 * inch, m + 5.1 * inch])
c.setFont("Helvetica-Bold", 13); c.drawString(m, y, "By garment and placement"); y -= 18
y = table(y, ["Garment and placement", "Width", "Height"], PLACES, [m, m + 3.4 * inch, m + 5.1 * inch])
c.setFont("Helvetica", 9.5); c.setFillGray(0.35)
c.drawString(m, m + 12, "Free calculator: rudracodeshere.github.io/profit-calculator/dtf-transfer-size-chart/")
c.drawString(m, m, "Sources: Kingdom DTF and xTool sizing guides, October 2026.")
c.save()
print(OUT)
