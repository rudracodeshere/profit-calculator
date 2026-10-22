# Free seller calculators

Free, no-signup calculators for Etsy, Shopify, eBay, Amazon, Poshmark and freelance sellers. Live site: https://rudracodeshere.github.io/profit-calculator/

Every calculator runs in the browser, uses editable US fee rates, and has its worked example checked by an automated browser test.

## Platform fees

- [Amazon FBA calculator](https://rudracodeshere.github.io/profit-calculator/amazon-fba-calculator/)
- [eBay fee calculator](https://rudracodeshere.github.io/profit-calculator/ebay-fee-calculator/)
- [Etsy fee calculator](https://rudracodeshere.github.io/profit-calculator/etsy-fee-calculator/)
- [Gumroad fee calculator](https://rudracodeshere.github.io/profit-calculator/gumroad-fee-calculator/)
- [PayPal fee calculator](https://rudracodeshere.github.io/profit-calculator/paypal-fee-calculator/)
- [Poshmark fee calculator](https://rudracodeshere.github.io/profit-calculator/poshmark-fee-calculator/)
- [Shopify fee calculator](https://rudracodeshere.github.io/profit-calculator/shopify-fee-calculator/)
- [Stripe fee calculator](https://rudracodeshere.github.io/profit-calculator/stripe-fee-calculator/)

## Etsy tools

- [Etsy pricing calculator](https://rudracodeshere.github.io/profit-calculator/etsy-pricing-calculator/)
- [Etsy Offsite Ads calculator](https://rudracodeshere.github.io/profit-calculator/etsy-offsite-ads-calculator/)
- [Etsy Ads ROAS calculator](https://rudracodeshere.github.io/profit-calculator/etsy-ads-calculator/)
- [Etsy digital download calculator](https://rudracodeshere.github.io/profit-calculator/etsy-digital-download-calculator/)
- [Etsy free shipping calculator](https://rudracodeshere.github.io/profit-calculator/etsy-free-shipping-calculator/)
- [Etsy hourly wage calculator](https://rudracodeshere.github.io/profit-calculator/etsy-hourly-wage-calculator/)
- [Etsy monthly profit calculator](https://rudracodeshere.github.io/profit-calculator/etsy-profit-calculator/)
- [Etsy sale & coupon calculator](https://rudracodeshere.github.io/profit-calculator/etsy-sale-calculator/)
- [Etsy title and tag checker](https://rudracodeshere.github.io/profit-calculator/etsy-title-tag-checker/)
- [Holiday order cutoff calculator](https://rudracodeshere.github.io/profit-calculator/holiday-order-cutoff-calculator/)

## Print & design sizes

- [DTF transfer size chart and t-shirt design size calculator](https://rudracodeshere.github.io/profit-calculator/dtf-transfer-size-chart/)
- [KDP cover size and spine width calculator](https://rudracodeshere.github.io/profit-calculator/kdp-cover-size-calculator/)
- [Printable wall art size and DPI calculator](https://rudracodeshere.github.io/profit-calculator/printable-wall-art-size-calculator/)

## Pricing & margins

- [Break-even calculator](https://rudracodeshere.github.io/profit-calculator/break-even-calculator/)
- [COGS calculator](https://rudracodeshere.github.io/profit-calculator/cogs-calculator/)
- [Markup calculator](https://rudracodeshere.github.io/profit-calculator/markup-calculator/)
- [Pet sitter holiday rate calculator](https://rudracodeshere.github.io/profit-calculator/pet-sitter-holiday-rate-calculator/)
- [Pet sitting rate calculator](https://rudracodeshere.github.io/profit-calculator/pet-sitting-rate-calculator/)
- [Price increase calculator](https://rudracodeshere.github.io/profit-calculator/price-increase-calculator/)
- [Profit margin calculator](https://rudracodeshere.github.io/profit-calculator/profit-margin-calculator/)
- [ROAS calculator](https://rudracodeshere.github.io/profit-calculator/roas-calculator/)

## Maker pricing

- [Candle pricing calculator](https://rudracodeshere.github.io/profit-calculator/candle-pricing-calculator/)
- [Handmade pricing calculator](https://rudracodeshere.github.io/profit-calculator/handmade-pricing-calculator/)
- [Jewelry pricing calculator](https://rudracodeshere.github.io/profit-calculator/jewelry-pricing-calculator/)
- [Print on demand profit calculator](https://rudracodeshere.github.io/profit-calculator/print-on-demand-profit-calculator/)
- [Wholesale price calculator](https://rudracodeshere.github.io/profit-calculator/wholesale-price-calculator/)

## Compare platforms

- [Etsy vs Shopify break-even](https://rudracodeshere.github.io/profit-calculator/etsy-vs-shopify/)
- [Etsy vs Amazon Handmade](https://rudracodeshere.github.io/profit-calculator/etsy-vs-amazon-handmade/)
- [Etsy vs eBay fees](https://rudracodeshere.github.io/profit-calculator/etsy-vs-ebay/)

## Invoices & getting paid

- [Invoice due date (Net 30) calculator](https://rudracodeshere.github.io/profit-calculator/invoice-due-date-calculator/)
- [Invoice late fee calculator](https://rudracodeshere.github.io/profit-calculator/invoice-late-fee-calculator/)
- [Payment reminder email generator](https://rudracodeshere.github.io/profit-calculator/payment-reminder-email-generator/)

## Budgets & planning

- [Christmas budget calculator](https://rudracodeshere.github.io/profit-calculator/christmas-budget-calculator/)

[About and fee sources](https://rudracodeshere.github.io/profit-calculator/about/)

Pages are generated from `tools/pages/*.py` by `tools/build_pages.py`; test with `tools/check_pages.js`.
The pin feed is checked with `python3 tools/pins/test_feed.py` (valid XML, unique item guids).

## Live smoke test

Read-only check of the published site. It loads every page in the live sitemap and fails on any JavaScript console error or page error. Gumroad buy links are checked offline: every product slug must be one this site sells, and the FIRST10 discount may appear only on the Seller Profit Sheet, the Get Paid Kit, and the 2027 Budget Planner, with `?code=FIRST10` kept on the link. That mode does not request gumroad.com.

```bash
npm install --no-save playwright
npx playwright install chromium
node tools/smoke_live.js
```

Set `SMOKE_FETCH_GUMROAD=1` to also fetch each Gumroad product URL and require HTTP 200. GitHub Actions sets that only for a manual run. After a Pages deploy the check stays offline, so those runs do not count as Gumroad views.

Pass a base URL to target a different host: `node tools/smoke_live.js https://rudracodeshere.github.io/profit-calculator/`. The script does not modify the repo or the site.
