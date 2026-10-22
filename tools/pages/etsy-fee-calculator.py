PAGE = dict(
    slug="etsy-fee-calculator",
    cat="Platform fees", starter_line=True, pin_save=True, cta_extra=[],
    nav_name="Etsy fee calculator",
    title="Etsy Fee Calculator 2026: Every Fee on One Sale, and What You Keep",
    desc="Free Etsy fee calculator. Enter a sale and see the transaction fee, payment processing, listing fee, Offsite Ads and currency conversion, plus what you keep after costs.",
    h1="Etsy fee calculator",
    lead="Enter one Etsy order. You get every fee Etsy takes, line by line, and what is left after your materials and the shipping label. All rates are editable if Etsy changes them or you sell outside the US. Nothing leaves your browser.",
    form="""      <label for="price">Item price</label>
      <div class="in"><span>$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="25"></div>
      <label for="ship">Shipping you charge the buyer</label>
      <div class="in"><span>$</span><input id="ship" type="number" inputmode="decimal" min="0" step="0.01" value="5"></div>
      <label for="qty">Quantity in the order</label>
      <div class="in"><input id="qty" type="number" min="1" step="1" value="1"></div>
      <label for="cost">Materials + packaging per item</label>
      <div class="in"><span>$</span><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="8"></div>
      <label for="label">Shipping label you pay</label>
      <div class="in"><span>$</span><input id="label" type="number" inputmode="decimal" min="0" step="0.01" value="5"></div>
      <label class="check"><input id="offsite" type="checkbox"> Order came from Offsite Ads</label>
      <label class="check"><input id="fx" type="checkbox"> My listing currency differs from my bank currency (2.5% conversion)</label>
      <details><summary class="note">Edit fee rates</summary>
      <label for="tx">Transaction fee</label>
      <div class="in"><input id="tx" type="number" min="0" step="0.1" value="6.5"><span>%</span></div>
      <label for="pp">Payment processing</label>
      <div class="in"><input id="pp" type="number" min="0" step="0.1" value="3"><span>% +</span><span>$</span><input id="pf" type="number" min="0" step="0.01" value="0.25"></div>
      <label for="oa">Offsite Ads rate <small>(12% if your shop made over $10k last year)</small></label>
      <div class="in"><input id="oa" type="number" min="0" step="1" value="15"><span>%</span></div>
      </details>""",
    js="""function calc(){
  var q=Math.max(1,Math.round(n('qty'))),t=n('price')*q+n('ship');
  var tx=t*n('tx')/100,pp=t*n('pp')/100+n('pf'),lf=0.20*q;
  var oa=$('offsite').checked?Math.min(t*n('oa')/100,100):0,fx=$('fx').checked?t*0.025:0;
  var fees=tx+pp+lf+oa+fx,costs=n('cost')*q+n('label'),keep=t-fees-costs;
  var r=[['Buyer pays',m(t)],['Transaction fee ('+n('tx')+'%)',m(-tx)],['Payment processing',m(-pp)],['Listing fee ($0.20 x '+q+')',m(-lf)]];
  if(oa)r.push(['Offsite Ads ('+n('oa')+'%, max $100)',m(-oa)]);
  if(fx)r.push(['Currency conversion (2.5%)',m(-fx)]);
  r.push(['Total Etsy fees',m(-fees)+' ('+(t?pc(fees/t):'0%')+')'],['Materials + label',m(-costs)],['You keep',m(keep),'total']);
  setRows(r);
  verdict(keep>=0,keep<0?'This order loses '+m(-keep)+' after fees and costs.':'Etsy takes '+m(fees)+' of '+m(t)+'. You keep '+(t?pc(keep/t,0):'0%')+' of the order.');
}""",
    note="US Etsy rates as of October 2026: 6.5% transaction fee and 3% + $0.25 processing on the order total (items + shipping), $0.20 listing fee per item sold. Processing rates differ by country (for example 4% + £0.20 in the UK). Sales tax is left out; processing on the tax portion adds a few cents per order.",
    body="""<h2>Every Etsy fee, explained</h2>
<p><strong>Listing fee: $0.20.</strong> You pay it when you publish a listing and again each time an item sells and the listing auto-renews. A quantity-3 order costs $0.60 in listing fees.</p>
<p><strong>Transaction fee: 6.5%</strong> of the order total: item price, the shipping you charge, and gift wrap. Offering free shipping doesn't avoid it. It just means the fee is charged on a higher item price.</p>
<p><strong>Payment processing: 3% + $0.25</strong> per order in the US, also on the order total. Other countries have their own rate.</p>
<p><strong>Offsite Ads: 15% or 12%</strong>, only on orders that came from an Etsy ad on another site within 30 days of the click, capped at $100 per order. See the <a href="../etsy-offsite-ads-calculator/">Offsite Ads calculator</a> to check whether those sales still make money.</p>
<p><strong>Currency conversion: 2.5%</strong> when your listings are priced in a different currency from your payment account.</p>
<h2>The quick formula</h2>
<p class="formula">Etsy fees (US) = 9.5% of (items + shipping) + $0.25 + $0.20 per item</p>
<p>Example: a $25 item with $5 shipping. The order total is $30, so the fees are $1.95 (transaction) + $1.15 (processing) + $0.20 (listing) = <strong>$3.30</strong>, or 11% of the order. With $8 of materials and a $5 label, you keep <strong>$13.70</strong>. If the same order came from Offsite Ads, another $4.50 goes, leaving $9.20.</p>
<h2>Why the percentage is higher on cheap items</h2>
<p>The $0.45 of fixed fees per order ($0.25 processing plus the $0.20 listing fee) barely matters on a $60 order, but on a $5 sticker it adds 9 points to the share Etsy takes. Bundling low-priced items, or setting a minimum order, keeps fixed fees from eating small sales.</p>""",
    faqs=[
        ("How much does Etsy take from a $20 sale?", "With free shipping, $2.35: $1.30 transaction fee, $0.85 processing and the $0.20 listing fee. That is 11.75% of the sale, before any Offsite Ads fee."),
        ("Does Etsy charge fees on shipping?", "Yes. Both the 6.5% transaction fee and the 3% processing fee apply to the shipping you charge the buyer."),
        ("Does Etsy charge fees on sales tax?", "The 6.5% transaction fee is not charged on sales tax. In the US the 3% processing fee is calculated on the full amount the buyer pays, tax included, which adds a few cents per order. This calculator leaves tax out to keep the inputs simple."),
        ("Is Etsy Plus worth it?", "Etsy Plus costs $10 a month and gives listing and ad credits. It only pays off if you would spend that on listings and Etsy Ads anyway; treat it as monthly overhead, not a per-sale fee."),
    ],
    related=["etsy-pricing-calculator", "etsy-offsite-ads-calculator", "etsy-profit-calculator", "etsy-free-shipping-calculator", "etsy-vs-shopify"],
    og_image="pins/pin-01.png",
    tests=[
        {"expect": {"rows": ["$30.00", "-$1.95", "-$1.15", "-$0.20", "-$3.30", "$13.70"]}},
        {"click": ["offsite"], "expect": {"rows": ["-$4.50", "$9.20"]}},
        {"set": {"price": "20", "ship": "0", "cost": "0", "label": "0"}, "expect": {"rows": ["-$2.35", "11.8%"]}},
        {"set": {"qty": "3", "price": "10", "ship": "5", "cost": "1", "label": "4"}, "expect": {"rows": ["-$0.60", "$35.00"]}},
    ],
)
