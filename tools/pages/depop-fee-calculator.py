PAGE = dict(
    slug="depop-fee-calculator",
    cat="Platform fees",
    gig="profit",
    nav_name="Depop fee calculator",
    title="Depop Fee Calculator 2026: US and UK Fees, Boosts and Profit",
    desc="Free Depop fee calculator for US, UK and AU sellers. See the 3.3% + $0.45 processing fee on item, shipping and tax, the 12% boost fee, your payout and profit.",
    h1="Depop fee calculator",
    lead="Depop charges no selling fee to sellers based in the US, UK or Australia. You still pay payment processing (3.3% + $0.45 in the US) on the item, shipping and any sales tax, plus a boosting fee (12% in the US and UK, 8% in Australia) on sales from boosted listings. Enter a sale to see each fee, what lands in your Depop Balance, your profit, and the price you need to list at for the profit you want.",
    form="""      <label for="region">Where you sell from</label>
      <select id="region" class="full"><option value="us">United States ($)</option><option value="uk">United Kingdom (&pound;)</option><option value="au">Australia (A$)</option></select>
      <label for="price">Item sale price</label>
      <div class="in"><span class="cur">$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="40"></div>
      <label for="ship">Shipping the buyer pays</label>
      <div class="in"><span class="cur">$</span><input id="ship" type="number" inputmode="decimal" min="0" step="0.01" value="6"></div>
      <label for="method">How you ship</label>
      <select id="method" class="full"><option value="label">Depop Shipping label</option><option value="own">I arrange my own shipping</option></select>
      <label for="label">Your shipping cost <small>(the Depop label cost, or the postage you pay)</small></label>
      <div class="in"><span class="cur">$</span><input id="label" type="number" inputmode="decimal" min="0" step="0.01" value="6"></div>
      <label for="tax">Sales tax on the item <small>(US sales tax Depop adds at checkout for the buyer's location; leave at 0 if your receipt shows none)</small></label>
      <div class="in"><input id="tax" type="number" inputmode="decimal" min="0" step="0.1" value="0"><span>%</span></div>
      <label for="cost">What you paid for the item</label>
      <div class="in"><span class="cur">$</span><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="10"></div>
      <label for="want">Profit you want <small>(for the target price)</small></label>
      <div class="in"><span class="cur">$</span><input id="want" type="number" inputmode="decimal" min="0" step="0.01" value="25"></div>
      <label class="check"><input id="boost" type="checkbox"> This sale came from a boosted listing</label>
      <details><summary class="note">Edit fee rates</summary>
      <label for="pp">Payment processing</label>
      <div class="in"><input id="pp" type="number" min="0" step="0.1" value="3.3"><span>%</span></div>
      <label for="pf">Processing fixed fee per order</label>
      <div class="in"><span class="cur">$</span><input id="pf" type="number" min="0" step="0.01" value="0.45"></div>
      <label for="bp">Boosting fee <small>(12% US and UK, 8% Australia)</small></label>
      <div class="in"><input id="bp" type="number" min="0" step="1" value="12"><span>%</span></div>
      <label for="sp">Depop selling fee <small>(0 in the US, UK and Australia; 10% for sellers elsewhere)</small></label>
      <div class="in"><input id="sp" type="number" min="0" step="1" value="0"><span>%</span></div>
      </details>""",
    out="""<div class="big"><span>Your profit</span><b id="profit"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>
      <h3>Price for a target profit</h3>
      <table><tbody id="rows2"></tbody></table>
      <p class="note">Buyers in the US, UK and Australia also pay Depop a Marketplace fee of up to 5% of the item price plus up to $1, &pound;1 or A$1. It does not come out of your payout, so enter the price you set, not the buyer's total. In Australia it is built into the price buyers see.</p>""",
    js="""var RATES={us:['$',3.3,0.45,12],uk:['£',2.9,0.30,12],au:['A$',2.6,0.30,8]};
var lastR=$('region').value,cur='$';
function mm(c){return (c<0?'-':'')+cur+(Math.abs(c)/100).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})}
function ct(id){return Math.round(n(id)*100)}
function rnd(x){return Math.round(x+1e-7)}
function calc(){
  var R=$('region').value;
  if(!RATES[R])R='us';
  if(R!==lastR){lastR=R;var q=RATES[R];$('pp').value=q[1];$('pf').value=q[2].toFixed(2);$('bp').value=q[3];if(R!=='us')$('tax').value=0}
  cur=RATES[R][0];
  document.querySelectorAll('.cur').forEach(function(s){s.textContent=cur});
  var S=ct('ship'),L=ct('label'),C=ct('cost'),t=n('tax')/100,pp=n('pp')/100,pf=ct('pf'),bp=n('bp')/100,sp=n('sp')/100;
  var own=$('method').value==='own',bo=$('boost').checked;
  function f(P){
    var tx=rnd(P*t),pb=P+S+tx,pr=pb>0?rnd(pb*pp+pf):0,bb=own?P+S:P,bf=bo?rnd(bb*bp):0,sf=rnd(bb*sp);
    var fees=pr+bf+sf,bal=P+S-fees-(own?0:L);
    return {tx:tx,pb:pb,pr:pr,bb:bb,bf:bf,sf:sf,fees:fees,bal:bal,profit:bal-(own?L:0)-C};
  }
  var wv=$('want').value.trim();
  if(wv==='')setRows([['Enter the profit you want to see the price to list at.','']],'rows2');
  else{
    var W=Math.round(Math.max(0,parseFloat(wv)||0)*100),k=1-pp*(1+t)-(bo?bp:0)-sp,best=-1;
    if(k>0){
      var c=Math.max(1,Math.floor((W-f(0).profit)/k-7/k));
      for(var i=0;i<2000000;i++,c++)if(f(c).profit>=W){best=c;break}
    }
    if(best===1)setRows([['Shipping minus your costs already makes that profit, at any price.','']],'rows2');
    else if(best>0){var h=f(best);
      setRows([[W?'To make '+mm(W)+' profit, list at':'To break even, list at',mm(best),'total'],['Depop fees at that price',mm(-h.fees)],['Profit at that price',mm(h.profit)]],'rows2')}
    else setRows([['No price reaches that profit with these rates.','']],'rows2');
  }
  var P=ct('price');
  if(!P){$('profit').textContent='-';setRows([['Enter the item sale price to see Depop fees.','']]);verdict(false,'Enter a sale price to see your fees and profit.');return}
  var g=f(P),pct=g.fees/P;
  var r=[['Item + shipping the buyer pays',mm(P+S)]];
  if(g.tx)r.push(['Sales tax ('+n('tax')+'%), collected and sent to the state by Depop',mm(g.tx)]);
  r.push(['Payment processing ('+n('pp')+'% + '+mm(pf)+' on '+mm(g.pb)+')',mm(-g.pr)]);
  r.push([bo?'Boosting fee ('+n('bp')+'% of '+mm(g.bb)+')':'Boosting fee',bo?mm(-g.bf):'not boosted']);
  r.push(['Depop selling fee'+(sp?' ('+n('sp')+'% of '+mm(g.bb)+')':''),mm(-g.sf)]);
  r.push(['Total Depop fees (share of item price)',mm(-g.fees)+' ('+pc(pct)+')']);
  if(!own)r.push(['Depop Shipping label, deducted',mm(-L)]);
  r.push(['Paid to your Depop Balance',mm(g.bal)]);
  if(own)r.push(['Postage you pay yourself',mm(-L)]);
  r.push(['What you paid for the item',mm(-C)],['Profit',mm(g.profit),'total']);
  setRows(r);$('profit').textContent=mm(g.profit);
  if(g.profit<0)verdict(false,'This sale loses '+mm(-g.profit)+'. Raise the price or the shipping charge, or skip the boost on cheap items.');
  else{var msg='You make '+mm(g.profit)+" profit. Depop's fees take "+pc(pct)+' of the item price.';
    if(pf&&pf/P>0.05)msg+=' The fixed '+mm(pf)+' processing fee alone is '+pc(pf/P)+' of this price. Processing is charged once per bundle, so selling cheap items together keeps more.';
    verdict(true,msg)}
}""",
    note="Depop fees checked on 20 October 2026 on Depop's own help centre: Seller fees and charges (updated 21 July 2026), Boosted Listings (updated 24 July 2026), the Boosted Listings Policy (effective 23 March 2026), State Sales Tax in the US and the Marketplace fee pages for the US, UK and Australia. Sellers based in the US, UK and Australia pay no selling fee on USD, GBP or AUD sales. Payment processing is 3.3% + $0.45 (US), 2.9% + &pound;0.30 (UK) or 2.6% + A$0.30 (Australia), charged on item + shipping + any sales tax. Boosting is 12% in the US and UK for listings from 23 March 2026 and 8% in Australia, charged on the item price plus shipping only if you arrange your own shipping. Depop's Boosted Listings Policy example uses 3.3% + &pound;0.45 for a UK sale, which conflicts with the fee page, so the UK default follows the fee page; check your receipt. Depop works out US sales tax at checkout from the buyer's location; this calculator applies your rate to the item price only, so if your receipt shows a different tax amount, change the rate to match. Sellers outside these three countries pay a 10% selling fee plus PayPal fees, which vary. Each fee is rounded to the cent, so a receipt can differ by a cent. All rates are editable.",
    body="""<h2>How Depop's fees work in 2026</h2>
<p>If you are based in the US, UK or Australia, Depop takes no selling fee. You still pay up to three things on each sale:</p>
<p><strong>Payment processing.</strong> 3.3% + $0.45 in the US, 2.9% + &pound;0.30 in the UK and 2.6% + A$0.30 in Australia. Depop's fee page says Depop Payments (via Stripe) charges it on the item sale price plus shipping costs and any applicable taxes. That is why the fee looks bigger than 3.3% of your price.</p>
<p><strong>Boosting fee.</strong> 12% in the US and UK for listings created from 23 March 2026, and 8% in Australia. You pay it only when a buyer viewed, clicked or liked the boosted listing and bought within 28 days. It is charged on the item price excluding tax, plus the shipping cost only if you arrange your own shipping. It is not charged on Depop Shipping labels.</p>
<p><strong>Shipping.</strong> With a Depop Shipping label you are paid the item price plus shipping, and the label cost is deducted along with the fees. If you arrange your own shipping, you keep the shipping money and pay the postage yourself.</p>
<p class="formula">Processing = (item + shipping + tax) x 3.3% + $0.45<br>Boost = item x 12%, or (item + shipping) x 12% if you ship yourself<br>Profit = item + shipping - processing - boost - label or postage - item cost</p>
<p>These rules come from Depop's <a href="https://depophelp.zendesk.com/hc/en-gb/articles/360001791127-Seller-fees-and-charges" rel="noopener">Seller fees and charges</a>, <a href="https://depophelp.zendesk.com/hc/en-gb/articles/10110299060753-Boosted-Listings" rel="noopener">Boosted Listings</a> and <a href="https://depophelp.zendesk.com/hc/en-gb/articles/360047922234-I-don-t-recognise-a-fee-or-charge" rel="noopener">I don't recognise a fee or charge</a> help pages. If a sale is refunded, Depop reverses all of its fees, boost included.</p>
<h2>What changed and when</h2>
<ul>
<li><strong>UK:</strong> the 10% selling fee was removed for listings created from 20 March 2024. Buyers started paying a Marketplace fee on 15 April 2024.</li>
<li><strong>US:</strong> the 10% selling fee was removed for new listings on 15 July 2024. The buyer Marketplace fee started on 18 July 2024.</li>
<li><strong>Boosting:</strong> the fee page lists 12% for new US and UK listings from 23 March 2026, and 8% in Australia. It does not give a rate for US or UK listings created before that date, and one Depop help page (I don't recognise a fee or charge) still says 8%. Your receipt shows the boosting fee charged, so if it differs, enter that rate under Edit fee rates.</li>
<li><strong>Australia:</strong> the selling fee was removed for sellers based in Australia from 22 July 2026, and buyers there started paying a Marketplace fee the same day.</li>
<li><strong>eBay:</strong> eBay completed its purchase of Depop on 30 July 2026. Depop's eBay FAQ (updated 30 July 2026) says there are no planned changes to fees or payments at this time.</li>
</ul>
<h2>Worked example</h2>
<p>A US seller sells a jacket for <strong>$40</strong>. The buyer pays <strong>$6</strong> shipping, the Depop Shipping label costs $6, there is no sales tax, the jacket cost $10, and the sale did not come from a boost.</p>
<ul>
<li>Processing: 3.3% x $46.00 = $1.518, plus $0.45 = <strong>$1.97</strong>.</li>
<li>Paid to your Depop Balance: $46.00 - $1.97 - $6.00 label = <strong>$38.03</strong>.</li>
<li>Profit after the $10 cost: <strong>$28.03</strong>. Depop's fees are 4.9% of the item price.</li>
</ul>
<p>Change one thing at a time and the numbers move like this:</p>
<ul>
<li>The sale came from a boost, Depop label: boost 12% x $40 = $4.80, profit <strong>$23.23</strong>.</li>
<li>Boosted, but you arrange your own shipping: boost 12% x $46 = $5.52, $38.51 paid to your balance, profit <strong>$22.51</strong> after $6 postage.</li>
<li>Same again with 8% sales tax ($3.20) in the buyer's state: processing is charged on $49.20, so it is $2.07, while the boost stays $5.52 because tax is excluded. Profit <strong>$22.41</strong>.</li>
<li>The first sale in the UK (&pound;40, &pound;6 shipping, &pound;6 label, &pound;10 cost): 2.9% x &pound;46 + &pound;0.30 = &pound;1.63, profit <strong>&pound;28.37</strong>.</li>
<li>To make $25 profit with the first setup, list at <strong>$36.86</strong>, or $42.09 if the sale comes from a boost.</li>
</ul>
<p>Depop's own Boosted Listings Policy gives this example: a boosted item that sells for &pound;50 including shipping pays &pound;6.00 boosting and &pound;2.10 processing, &pound;8.10 in total. Its processing figure uses 3.3% + &pound;0.45, the US rates, not the UK rate on the fee page. Enter a $50 price, $0 shipping and own shipping with the boost ticked and the calculator gives the same $8.10 at US rates.</p>
<h2>When boosting is worth it</h2>
<p>At 12%, a boost costs $4.80 on a $40 item, more than twice the processing fee, and $5.52 if you ship yourself, because then shipping is boosted too. You only pay when the buyer saw or interacted with the boosted listing and bought within 28 days. So the real question is whether the boost brings a sale you would not have made in that time. It tends to make sense for slow movers and items with margin to spare, and less sense for items that sell fast anyway or that you have already priced tight. If you boost, using a Depop Shipping label keeps shipping out of the boost fee.</p>
<h2>Cheap items and the fixed fee</h2>
<p>The fixed $0.45 is charged once per order, so it hits small sales hardest. A $2 item with free shipping pays $0.52 in processing, 26.0% of the price, leaving $1.48 before you pay for postage. Depop's fee page says processing applies once per bundle transaction, so bundling cheap pieces or setting a minimum price for small items keeps more of each sale.</p>""",
    faqs=[
        ("Does Depop still charge a 10% selling fee?", "Not for sellers based in the US, UK or Australia. The UK dropped it for listings created from 20 March 2024, the US for new listings from 15 July 2024, and Australia from 22 July 2026. Sellers elsewhere still pay 10% on the item price, plus shipping if they don't use a Depop label, and PayPal's processing fee on top."),
        ("Why is my Depop processing fee more than 3.3% + $0.45 of my price?", "Because it is charged on the item price plus shipping plus any sales tax, not on the price alone. A $40 item with $6 shipping pays 3.3% of $46.00 plus $0.45, which is $1.97. Add 8% sales tax and the base becomes $49.20, so the fee is $2.07. On a $2 item with free shipping, the $0.52 fee is 26% of the price."),
        ("How much is the Depop boosting fee and when do I pay it?", "12% in the US and UK for listings created from 23 March 2026, and 8% in Australia. You pay it only if the buyer viewed, clicked or liked the boosted listing and bought within 28 days. It is charged on the item price excluding tax, plus shipping only if you arrange your own shipping, and never on a Depop Shipping label. On a $40 item that is $4.80, and it is reversed if the sale is refunded."),
        ("Does the buyer's Marketplace fee come out of my payout?", "No. Buyers pay it on top of the price you set: up to 5% of the item price plus a fixed amount of up to $1, &pound;1 or A$1, not counting tax and shipping. In the US and UK the exact amount is shown at checkout; in Australia it is built into the price buyers see. Your payout is the item price plus shipping, minus processing, any boost fee and any Depop label cost."),
    ],
    related=["poshmark-fee-calculator", "ebay-fee-calculator", "etsy-vs-ebay", "stripe-fee-calculator", "profit-margin-calculator"],
    tests=[
        {"expect": {"rows": ["$46.00", "-$1.97", "not boosted", "-$6.00", "$38.03", "-$10.00", "4.9%"], "profit": "$28.03",
                    "rows2": "$36.86", "verdict": ["You make $28.03", "4.9%"]}},
        {"click": ["boost"], "expect": {"rows": ["-$4.80", "12% of $40.00"], "profit": "$23.23", "rows2": "$42.09"}},
        {"set": {"method": "own", "tax": "8"}, "click": ["boost"], "expect": {"rows": ["collected and sent to the state by Depop", "$3.20", "on $49.20", "-$2.07", "12% of $46.00", "-$5.52", "$38.41"], "profit": "$22.41"}},
        {"set": {"price": "50", "ship": "0", "label": "0", "cost": "0", "method": "own"}, "click": ["boost"], "expect": {"rows": ["-$2.10", "-$6.00", "-$8.10"], "profit": "$41.90"}},
        {"set": {"region": "uk"}, "expect": {"rows": ["2.9% + £0.30 on £46.00", "-£1.63", "£38.37"], "profit": "£28.37", "rows2": "£"}},
        {"set": {"region": "au", "price": "0"}, "expect": {"profit": "-", "rows": "Enter the item sale price", "verdict": "Enter a sale price", "rows2": ["A$25.00", "A$36.40"]}},
    ],
)
