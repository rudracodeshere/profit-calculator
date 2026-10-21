PAGE = dict(
    slug="mercari-fee-calculator",
    cat="Platform fees",
    gig="profit",
    nav_name="Mercari fee calculator",
    title="Mercari Fee Calculator 2026: What You Earn After the 10% Fee and Shipping",
    desc="Free Mercari fee calculator for US sellers: the 10% fee on item price plus buyer-paid shipping, what you earn, your profit, and the price that earns a set amount.",
    h1="Mercari fee calculator",
    lead="Enter one Mercari sale. The calculator takes the 10% selling fee on the item price plus any shipping the buyer pays, subtracts the label if you offer free shipping, then shows your profit and the lowest price that earns a set amount.",
    form="""      <label for="price">Sold price of the item</label>
      <div class="in"><span>$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="40"></div>
      <label for="who">Who pays shipping</label>
      <select id="who" class="full">
        <option value="buyer" selected>Buyer pays shipping (Mercari label)</option>
        <option value="seller">I pay shipping (free shipping or ship on my own)</option>
      </select>
      <label for="label">Shipping label price <small>(Mercari's price for your weight and service, or your own postage)</small></label>
      <div class="in"><span>$</span><input id="label" type="number" inputmode="decimal" min="0" step="0.01" value="8"></div>
      <label for="cost">What the item cost you</label>
      <div class="in"><span>$</span><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="12"></div>
      <label for="want">Amount you want to earn <small>(after Mercari's fee and shipping)</small></label>
      <div class="in"><span>$</span><input id="want" type="number" inputmode="decimal" min="0" step="0.01" value="30"></div>
      <label class="check"><input id="ip" type="checkbox"> Cash out this sale with Instant Pay ($3 per cash-out)</label>
      <details><summary class="note">Edit fee rates</summary>
      <label for="pct">Mercari selling fee</label>
      <div class="in"><input id="pct" type="number" min="0" step="0.1" value="10"><span>%</span></div>
      <label for="ipf">Instant Pay fee per cash-out</label>
      <div class="in"><span>$</span><input id="ipf" type="number" min="0" step="0.01" value="3"></div>
      <label for="bp">Buyer Protection fee <small>(paid by the buyer)</small></label>
      <div class="in"><input id="bp" type="number" min="0" step="0.1" value="3.6"><span>%</span></div>
      </details>""",
    out="""<div class="big"><span>You earn</span><b id="earn"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>
      <h3>What the buyer pays</h3>
      <table><tbody id="buyer"></tbody></table>
      <h3>Price needed to earn a set amount</h3>
      <table><tbody id="rows2"></tbody></table>""",
    js="""function calc(){
  var r=n('pct')/100,bp=n('bp')/100,buy=$('who').value==='buyer';
  var Pc=Math.round(n('price')*100),Sc=Math.round(n('label')*100),Cc=Math.round(n('cost')*100),Wc=Math.round(n('want')*100);
  var ipc=$('ip').checked?Math.round(n('ipf')*100):0;
  function rnd(x){return Math.round(+x.toFixed(6))}
  function feeB(p){return rnd(r*(p+Sc))}
  function feeS(p){return rnd(r*p)}
  function earnB(p){return p-feeB(p)}
  function earnS(p){return p-feeS(p)-Sc}
  function lowest(f){
    if(r>=1)return -1;
    var lo=1,hi=Math.ceil((Wc+Sc+1)/(1-r))+2;
    if(hi>1e11)return -1;
    while(lo<hi){var mid=Math.floor((lo+hi)/2);if(f(mid)>=Wc)hi=mid;else lo=mid+1}
    return f(lo)>=Wc?lo:-1;
  }
  if(!Wc)setRows([['Enter the amount you want to earn.','']],'rows2');
  else{
    var qb=lowest(earnB),qs=lowest(earnS);
    if(qb<0||qs<0)setRows([['No price earns that with these rates.','']],'rows2');
    else setRows([['To earn '+m(Wc/100)+' with buyer-paid shipping, list at',m(qb/100),'total'],['With free shipping, list at',m(qs/100),'total'],
      ['Buyer pays either way, before sales tax',m((qs+rnd(qs*bp))/100)]],'rows2');
  }
  if(!Pc){$('earn').textContent='-';setRows([["Enter the sold price to see Mercari's fee.",'']]);setRows([['Enter the sold price.','']],'buyer');verdict(false,'No sale entered yet.');return}
  var fee=buy?feeB(Pc):feeS(Pc),earn=buy?earnB(Pc):earnS(Pc),pr=earn-Cc-ipc;
  var rows=[['Item price',m(Pc/100)]];
  if(buy)rows.push(['Shipping the buyer pays',m(Sc/100)],["Mercari label, paid from the buyer's shipping",m(-Sc/100)]);
  rows.push(['Mercari selling fee ('+n('pct')+'% of '+m((buy?Pc+Sc:Pc)/100)+')',m(-fee/100)]);
  if(!buy)rows.push(['Shipping label you pay',m(-Sc/100)]);
  rows.push(['You earn',m(earn/100)]);
  if(ipc)rows.push(['Instant Pay fee (per cash-out)',m(-ipc/100)]);
  rows.push(['What you paid for the item',m(-Cc/100)],['Profit',m(pr/100),'total']);
  setRows(rows);
  $('earn').textContent=m(earn/100);
  var base=buy?Pc+Sc:Pc,bpc=rnd(base*bp);
  setRows([[buy?'Item + shipping':'Item price (shipping included)',m(base/100)],['Buyer Protection fee ('+n('bp')+'%)',m(bpc/100)],['Buyer pays before sales tax',m((base+bpc)/100),'total']],'buyer');
  if(pr<0)verdict(false,'This sale loses '+m(-pr/100)+' after '+(buy?'the fee':'the fee, the label')+(ipc?', Instant Pay':'')+' and what you paid for the item. Raise the price'+(buy?'.':' or let the buyer pay shipping.'));
  else if(buy&&Sc)verdict(true,'You make '+m(pr/100)+' profit. With free shipping at this price you would earn '+m(earnS(Pc)/100)+'. Price it at '+m((Pc+Sc)/100)+' to earn the same '+m(earn/100)+'.');
  else if(!buy&&Sc)verdict(true,'You make '+m(pr/100)+' profit. If the buyer paid the '+m(Sc/100)+' shipping instead, this price would earn '+m(earnB(Pc)/100)+'.');
  else verdict(true,'You make '+m(pr/100)+' profit. Mercari keeps '+m(fee/100)+', '+pc(fee/Pc)+' of the price.');
}""",
    note="US Mercari fees, checked October 20, 2026 on Mercari's own Help Center: \"Fees on Mercari\" (updated May 7, 2026), \"FAQs about our new fee structure\" and the shipping guide for sellers. Mercari charges a 10% selling fee on the item price plus any shipping the buyer pays, with no separate payment processing fee on listings created or updated since January 6, 2025. With free shipping the label comes out of your earnings. Mercari's fee pages put only buyer-paid shipping in the fee and don't mention free shipping, so with free shipping the fee here is 10% of the item price. Your Mercari Gross Sales Report shows the fee actually charged on each order. The 3.6% Buyer Protection fee is paid by the buyer. Direct Deposit is free ($2 if a deposit fails) and Instant Pay is $3 per cash-out, up to $600 a month. Mercari's label prices changed on October 19, 2026, so enter the price Mercari shows you. Fees are rounded to the nearest cent here and Mercari's figures may differ by a cent or two. Every rate is editable under Edit fee rates.",
    body="""<h2>How Mercari fees work in 2026</h2>
<p><strong>Selling fee.</strong> Since January 6, 2025, Mercari charges sellers a flat 10% of the item price plus any shipping the buyer pays, on new and updated listings. The fee comes out of your sale, so you never pay it separately.</p>
<p><strong>No processing fee.</strong> Listings created or updated since that date carry no separate payment processing fee. The old 2.9% + $0.50 processing fee belongs to the previous fee structure, so it isn't in this calculator.</p>
<p><strong>Buyer Protection fee.</strong> The buyer pays 3.6% of the item price plus buyer-paid shipping at checkout. It doesn't come out of your earnings, but it does raise the total your buyer sees, which is why the calculator shows it.</p>
<p><strong>Cashing out.</strong> Direct Deposit to your bank is free. A deposit that fails costs $2. Instant Pay sends money to an eligible debit card in about 30 minutes for $3 per cash-out, up to $600 a month and once a day.</p>
<h2>Buyer-paid shipping vs free shipping</h2>
<p class="formula">Buyer pays shipping: you earn = price - 10% x (price + shipping)<br>Free shipping: you earn = price - 10% x price - label</p>
<p>Worked example: you sell a <strong>$40</strong> item that cost you <strong>$12</strong>, and Mercari's label is <strong>$8</strong>.</p>
<p><strong>Buyer pays shipping.</strong> The fee is 10% of $48, which is $4.80. You earn <strong>$35.20</strong> and your profit is <strong>$23.20</strong>. The buyer pays $48 plus a $1.73 Buyer Protection fee, $49.73 before sales tax.</p>
<p><strong>Free shipping at the same $40.</strong> The fee drops to $4.00, but the $8.00 label comes out of your sale. You earn $28.00 and your profit is $16.00. The buyer pays $40 plus $1.44, which is $41.44.</p>
<p><strong>Free shipping priced at $48.</strong> The fee is $4.80, the label is $8.00 and you earn $35.20, exactly the same as buyer-paid shipping. The buyer also pays the same $49.73. So free shipping doesn't cost you more in fees. It only costs you more if you don't add the label to your price.</p>
<p>If you cash out that buyer-paid sale on its own with Instant Pay, your profit drops by $3.00 to $20.20.</p>
<h2>Pricing backward from what you want to earn</h2>
<p class="formula">Buyer pays shipping: price = (target + 10% x shipping) / 0.9<br>Free shipping: price = (target + label) / 0.9</p>
<p>To earn $30 with an $8 label, list at <strong>$34.22</strong> with buyer-paid shipping: the fee is 10% of $42.22, which is $4.22, and $34.22 - $4.22 = $30.00. With free shipping, list at <strong>$42.22</strong>: the fee is $4.22, the label is $8.00 and you keep $30.00. The buyer pays $43.74 before sales tax either way. If you accept offers, list a little above this so an accepted offer still earns what you need.</p>
<h2>Other costs to know</h2>
<p><strong>Instant Pay is per cash-out, not per sale.</strong> $3 on a single sale that earns $35.20 is about 8.5% of it. Let a few sales build up, or use free Direct Deposit when you can wait.</p>
<p><strong>Cheap items with free shipping.</strong> A $10 item with an $8 free-shipping label earns $1.00 after the $1.00 fee and the label. If the item cost you $5, you lose $4.00. Let the buyer pay shipping on small items, or bundle them.</p>
<p><strong>Cancellations.</strong> If you cancel sales often, Mercari warns you first and then may charge a cancellation fee of 5% of the item price, up to $25.</p>
<p><strong>Label problems.</strong> If a package is heavier or bigger than the label you bought, Mercari takes the overweight or oversize charge from your sales. USPS charges $50 when a non-hazardous item ships in a box that still has a visible HAZMAT label. For packages postmarked on or after September 1, 2026, Mercari splits that fee with you, so $25 comes out of your earnings.</p>
<p><strong>Authentication.</strong> Mercari's fee page lists a $5 Mercari Authenticate fee, paid by the seller, for items over a set price that go through third-party authentication, and $10 for an Authenticate Certificate.</p>""",
    faqs=[
        ("How much does Mercari take from a $40 sale?", "10%, which is $4.00, if you offer free shipping. If the buyer pays $8 shipping, the fee is $4.80 because it also applies to that shipping, and you earn $35.20."),
        ("Does Mercari charge its 10% fee on shipping?", "Yes, on shipping the buyer pays. Mercari's fee page sets the fee at 10% of the item price plus buyer-paid shipping, so with free shipping the fee is on the item price only and the label is taken out of your earnings instead."),
        ("Is free shipping or buyer-paid shipping better on Mercari?", "They earn the same if you add the label to your price. A $48 item with free shipping and a $40 item with $8 buyer-paid shipping both earn $35.20, and the buyer pays $49.73 either way. Free shipping only earns less if you don't raise the price."),
        ("Does Mercari still charge a payment processing fee or a fee to cash out?", "There is no separate processing fee on listings created or updated since January 6, 2025. Direct Deposit is free, with a $2 fee only if a deposit fails. Instant Pay costs $3 per cash-out, up to $600 a month."),
    ],
    related=["poshmark-fee-calculator", "ebay-fee-calculator", "etsy-vs-ebay", "paypal-fee-calculator", "profit-margin-calculator", "markup-calculator"],
    tests=[
        {"expect": {"rows": ["$40.00", "$8.00", "-$4.80", "$35.20", "-$12.00", "$23.20"], "earn": "$35.20", "buyer": ["$1.73", "$49.73"],
                    "rows2": ["$34.22", "$42.22", "$43.74"], "verdict": ["$28.00", "$48.00"]}},
        {"set": {"who": "seller"}, "expect": {"rows": ["-$4.00", "-$8.00", "$28.00", "$16.00"], "earn": "$28.00", "buyer": ["$1.44", "$41.44"], "verdict": "$35.20"}},
        {"set": {"who": "seller", "price": "48"}, "expect": {"earn": "$35.20", "rows": "-$4.80", "buyer": "$49.73"}},
        {"set": {"ip": True}, "expect": {"rows": ["-$3.00", "$20.20"]}},
        {"set": {"price": "0", "want": ""}, "expect": {"earn": "-", "rows": "Enter the sold price", "verdict": "No sale", "rows2": "Enter the amount"}},
        {"set": {"who": "seller", "price": "10", "label": "8", "cost": "5"}, "expect": {"rows": "-$1.00", "earn": "$1.00", "verdict": "loses $4.00"}},
    ],
)
