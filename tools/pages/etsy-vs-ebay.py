PAGE = dict(
    slug="etsy-vs-ebay",
    cat="Compare platforms",
    nav_name="Etsy vs eBay fees",
    title="Etsy vs eBay Fees 2026: Same Item, Side by Side",
    desc="Compare Etsy and eBay fees on the same sale: what each takes per order and per month, what you keep after costs, and how sales tax and ads change it.",
    h1="Etsy vs eBay: which takes less of your sale?",
    lead="Enter one item as you would list it on both sites. You get each platform's fees line by line, what you keep after your costs, and the difference over a month of orders. Every rate is editable.",
    form="""      <label for="pr">Item price</label>
      <div class="in"><span>$</span><input id="pr" type="number" inputmode="decimal" min="0" step="0.01" value="30"></div>
      <label for="sh">Shipping you charge the buyer</label>
      <div class="in"><span>$</span><input id="sh" type="number" inputmode="decimal" min="0" step="0.01" value="6"></div>
      <label for="tx">Buyer's sales tax rate <small>(eBay's fee includes tax)</small></label>
      <div class="in"><input id="tx" type="number" inputmode="decimal" min="0" step="0.1" value="0"><span>%</span></div>
      <label for="co">Item cost <small>(materials or what you paid)</small></label>
      <div class="in"><span>$</span><input id="co" type="number" inputmode="decimal" min="0" step="0.01" value="10"></div>
      <label for="lb">Shipping label + packaging</label>
      <div class="in"><span>$</span><input id="lb" type="number" inputmode="decimal" min="0" step="0.01" value="6"></div>
      <label for="od">Orders per month</label>
      <div class="in"><input id="od" type="number" inputmode="decimal" min="0" step="1" value="20"></div>
      <label for="os">Etsy orders from Offsite Ads</label>
      <div class="in"><input id="os" type="number" inputmode="decimal" min="0" max="100" step="1" value="0"><span>%</span></div>
      <label for="pl">eBay promoted listings ad rate <small>(0 if you don't promote)</small></label>
      <div class="in"><input id="pl" type="number" inputmode="decimal" min="0" step="0.5" value="0"><span>%</span></div>
      <label for="st">eBay Store subscription <small>(optional, per month)</small></label>
      <div class="in"><span>$</span><input id="st" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
      <label class="check"><input id="trs" type="checkbox"> eBay Top Rated Plus listing (10% off the final value fee)</label>
      <details><summary class="note">Edit fee rates</summary>
      <label for="etx">Etsy transaction fee</label>
      <div class="in"><input id="etx" type="number" min="0" step="0.1" value="6.5"><span>%</span></div>
      <label for="epp">Etsy payment processing</label>
      <div class="in"><input id="epp" type="number" min="0" step="0.1" value="3"><span>% +</span><span>$</span><input id="epf" type="number" min="0" step="0.01" value="0.25"></div>
      <label for="elf">Etsy listing fee per item sold</label>
      <div class="in"><span>$</span><input id="elf" type="number" min="0" step="0.01" value="0.20"></div>
      <label for="eoa">Etsy Offsite Ads rate <small>(12% over $10k/yr sales)</small></label>
      <div class="in"><input id="eoa" type="number" min="0" step="1" value="15"><span>%</span></div>
      <label for="bfv">eBay final value fee <small>(13.6% most categories; varies)</small></label>
      <div class="in"><input id="bfv" type="number" min="0" step="0.1" value="13.6"><span>%</span></div>
      <label for="bpo">eBay per-order fee <small>(over $10 / $10 or less)</small></label>
      <div class="in"><span>$</span><input id="bpo" type="number" min="0" step="0.01" value="0.40"><span>/</span><span>$</span><input id="bps" type="number" min="0" step="0.01" value="0.30"></div>
      </details>""",
    out="""<div class="big"><span id="winl">Cheaper for this order</span><b id="big"></b></div>
      <table class="wide" aria-live="polite"><thead><tr><th>Per order</th><th>Etsy</th><th>eBay</th></tr></thead><tbody id="cmp"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var t=n('pr')+n('sh'),tax=t*n('tx')/100,g=t+tax,q=n('od'),own=n('co')+n('lb');
  var e1=t*n('etx')/100,e2=t?g*n('epp')/100+n('epf'):0,e3=t?n('elf'):0,e4=n('os')/100*Math.min(t*n('eoa')/100,100),ef=e1+e2+e3+e4;
  var b1=g*n('bfv')/100*($('trs').checked?0.9:1),b2=t?(g>10?n('bpo'):n('bps')):0,b3=g*n('pl')/100,bf=b1+b2+b3;
  var ek=t-ef-own,bk=t-bf-own,st=n('st');
  function row(l,a,b,c){return '<tr'+(c?' class="total"':'')+'><td>'+l+'</td><td>'+a+'</td><td>'+b+'</td></tr>'}
  $('cmp').innerHTML=row('Buyer pays (before tax)',m(t),m(t))+row('Transaction / final value fee',m(-e1),m(-b1))+
    row('Processing / per order',m(-e2),m(-b2))+row('Listing fee',m(-e3),'$0.00')+row('Ads',m(-e4),m(-b3))+
    row('Total fees',m(-ef),m(-bf))+row('Share of order',t?pc(ef/t):'0%',t?pc(bf/t):'0%')+row('You keep after costs',m(ek),m(bk),1)+
    row('Fees per month ('+q+' orders)',m(ef*q),m(bf*q+st))+row('Kept per month',m(ek*q),m(bk*q-st));
  if(!t){$('big').textContent='-';verdict(false,'Enter an item price to compare the two platforms.');return}
  var d=bf-ef,dm=(bf*q+st)-ef*q;
  $('big').textContent=(d>=0?'Etsy':'eBay')+', by '+m(Math.abs(d));
  if(d>=0){var fv=g?(ef-b2-b3)/g/($('trs').checked?0.9:1):0;verdict(true,'Etsy leaves you '+m(d)+' more per order, '+m(dm)+' a month at '+q+' orders. eBay would only match Etsy if its final value fee in your category were '+(fv>0?pc(fv):'0%')+' or less.')}
  else verdict(true,'eBay leaves you '+m(-d)+' more per order'+(dm<0?', '+m(-dm)+' a month at '+q+' orders':', but the store subscription cancels it out over a month')+'. Most of the gap is Etsy Offsite Ads; check those orders still pay.');
}""",
    note="US rates as of October 2026. Etsy: 6.5% transaction fee on item + shipping, 3% + $0.25 processing on the total including tax, $0.20 listing fee per item sold. eBay: 13.6% final value fee for most categories (some categories are higher or lower) on the total the buyer pays including shipping and sales tax, plus $0.40 per order ($0.30 on orders of $10 or less). Offsite Ads are averaged over the share of orders entered. Sales tax is collected and paid by both marketplaces, so it is not counted as income.",
    body="""<h2>How the two fee models differ</h2>
<p><strong>Etsy</strong> splits its cut into small pieces: a 6.5% transaction fee on the item and shipping, 3% + $0.25 for payment processing and $0.20 every time an item sells (the listing renews). Together that is about 9.5% plus $0.45 on a typical one-item order. Offsite Ads add 15% (or 12%) on orders that come through Etsy's ads on other sites.</p>
<p><strong>eBay</strong> charges one larger final value fee, 13.6% in most categories, plus $0.40 per order. The difference that catches sellers out: eBay calculates it on the whole amount the buyer pays, <em>including sales tax</em>. Etsy's 6.5% transaction fee leaves tax out (only its 3% processing fee includes it).</p>
<p class="formula">Etsy = 6.5% x (item + shipping) + 3% x (item + shipping + tax) + $0.25 + $0.20<br>eBay = 13.6% x (item + shipping + tax) + $0.40</p>
<h2>A worked example</h2>
<p>A $30 item with $6 shipping, no tax. Etsy takes <strong>$3.87</strong> and eBay takes <strong>$5.30</strong>, so Etsy leaves you $1.43 more. After a $10 item cost and a $6 label you keep $16.13 on Etsy and $14.70 on eBay. Over 20 orders a month that is $77.40 in Etsy fees against $105.92 on eBay, a $28.52 gap.</p>
<p>Add a 7% sales tax and eBay's fee rises to $5.64 while Etsy's only goes to $3.95. A Top Rated Plus discount brings eBay down to $4.81 on the untaxed order, still above Etsy. Etsy only loses on fees when a large share of your orders come through Offsite Ads: at half your orders, Etsy's average fee is $6.57 and eBay is $1.27 cheaper.</p>
<h2>What the fees don't tell you</h2>
<p><strong>Who is shopping.</strong> Etsy buyers are looking for handmade, vintage and craft supplies, and often search by style or occasion. eBay buyers often search for a specific thing: a part, a model number, a collectible, a used item at a good price. Auctions and Best Offer let the market set the price, which suits resale and rare items more than made-to-order work.</p>
<p><strong>Listing costs.</strong> Every Etsy listing costs $0.20 up front and lasts four months. eBay gives a monthly allowance of free listings and charges an insertion fee beyond it, so a large catalog of slow-moving items can cost less to keep listed on eBay.</p>
<p><strong>Subscriptions are optional on both.</strong> An eBay Store adds a monthly fee and more free listings; Etsy Plus is $10 a month. Neither is needed to sell. If you add one, put it in the store box above (or count Etsy Plus as overhead) and check it is paid back.</p>
<p>Many sellers list on both. Fees are only half of it: compare the price each audience will actually pay for the same item.</p>""",
    faqs=[
        ("Is eBay or Etsy cheaper to sell on?", "On fees, Etsy is usually cheaper. On a $30 item with $6 shipping Etsy takes $3.87 and eBay takes $5.30. eBay only comes out ahead when many of your Etsy orders come through Offsite Ads."),
        ("Does eBay charge fees on sales tax?", "Yes. eBay's final value fee is a percentage of the total the buyer pays, including shipping and sales tax. With 7% tax on a $36 order, eBay's fee goes from $5.30 to $5.64."),
        ("Does Top Rated Plus make eBay cheaper than Etsy?", "It helps but usually not enough. The 10% discount on the final value fee cuts eBay's fee on a $36 order to $4.81, still above Etsy's $3.87."),
        ("Do I need an eBay Store to sell on eBay?", "No. A store subscription is optional. It mainly pays off if you list more items than the free monthly allowance covers, since stores come with more free listings. Enter its monthly price above to see what it does to your monthly total."),
    ],
    related=["ebay-fee-calculator", "etsy-fee-calculator", "etsy-vs-amazon-handmade", "etsy-vs-shopify", "etsy-offsite-ads-calculator", "poshmark-fee-calculator"],
    og_image="pins/pin-13.png",
    tests=[
        {"expect": {"big": "Etsy, by $1.43", "cmp": ["$36.00", "-$3.87", "-$5.30", "$16.13", "$14.70", "$77.40", "$105.92", "$322.60", "$294.08", "14.7%"], "verdict": ["$1.43", "$28.52", "9.6%"]}},
        {"set": {"tx": "7"}, "expect": {"cmp": ["-$3.95", "-$5.64"], "big": "Etsy, by $1.69"}},
        {"click": ["trs"], "expect": {"cmp": "-$4.81", "big": "Etsy, by $0.94"}},
        {"set": {"os": "50"}, "expect": {"cmp": ["-$2.70", "-$6.57"], "big": "eBay, by $1.27", "verdict": "Offsite Ads"}},
        {"set": {"pr": "6", "sh": "0"}, "expect": {"cmp": ["-$1.02", "-$1.12", "-$0.30"]}},
        {"set": {"st": "20"}, "expect": {"cmp": "$125.92"}},
        {"set": {"pr": "0", "sh": "0"}, "expect": {"big": "-", "verdict": "Enter an item price"}},
    ],
)
