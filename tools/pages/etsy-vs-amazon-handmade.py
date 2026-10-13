PAGE = dict(
    slug="etsy-vs-amazon-handmade",
    cat="Compare platforms",
    nav_name="Etsy vs Amazon Handmade",
    title="Etsy vs Amazon Handmade Fees (2026): Which Costs Less?",
    desc="Compare Etsy and Amazon Handmade fees on the same order, per sale and per month, and find the order total where one becomes cheaper than the other.",
    h1="Etsy vs Amazon Handmade: fees side by side",
    lead="Enter one order as it would sell on both. You get Etsy's fees against Amazon Handmade's 15% referral fee, what each costs to fulfill, the monthly difference, and the exact order totals where the cheaper platform switches.",
    form="""      <label for="pr">Item price</label>
      <div class="in"><span>$</span><input id="pr" type="number" inputmode="decimal" min="0" step="0.01" value="35"></div>
      <label for="sh">Shipping you charge the buyer</label>
      <div class="in"><span>$</span><input id="sh" type="number" inputmode="decimal" min="0" step="0.01" value="5"></div>
      <label for="lb">Your shipping label + packaging</label>
      <div class="in"><span>$</span><input id="lb" type="number" inputmode="decimal" min="0" step="0.01" value="6"></div>
      <label for="od">Orders per month</label>
      <div class="in"><input id="od" type="number" inputmode="decimal" min="0" step="1" value="20"></div>
      <label class="check"><input id="fba" type="checkbox"> Use FBA on Amazon (Amazon ships; replaces your label)</label>
      <label for="ff">FBA fulfillment fee per unit <small>(depends on size and weight)</small></label>
      <div class="in"><span>$</span><input id="ff" type="number" inputmode="decimal" min="0" step="0.01" value="5"></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="ar">Amazon Handmade referral fee</label>
      <div class="in"><input id="ar" type="number" min="0" step="0.5" value="15"><span>%</span></div>
      <label for="am">Minimum referral fee per item</label>
      <div class="in"><span>$</span><input id="am" type="number" min="0" step="0.01" value="1.00"></div>
      <label for="ap">Amazon monthly plan fee <small>(waived for approved Handmade artisans; $39.99 if not)</small></label>
      <div class="in"><span>$</span><input id="ap" type="number" min="0" step="0.01" value="0"></div>
      <label for="etx">Etsy transaction fee</label>
      <div class="in"><input id="etx" type="number" min="0" step="0.1" value="6.5"><span>%</span></div>
      <label for="epp">Etsy payment processing</label>
      <div class="in"><input id="epp" type="number" min="0" step="0.1" value="3"><span>% +</span><span>$</span><input id="epf" type="number" min="0" step="0.01" value="0.25"></div>
      <label for="elf">Etsy listing fee per item sold</label>
      <div class="in"><span>$</span><input id="elf" type="number" min="0" step="0.01" value="0.20"></div>
      </details>""",
    out="""<div class="big"><span>Cheaper for this order</span><b id="big"></b></div>
      <table class="wide" aria-live="polite"><thead><tr><th>Per order</th><th>Etsy</th><th>Amazon</th></tr></thead><tbody id="cmp"></tbody></table>
      <div id="verdict" class="verdict"></div>
      <h3>Where the cheaper platform switches</h3>
      <p id="cross"></p>""",
    js="""function calc(){
  var t=n('pr')+n('sh'),q=n('od'),fb=$('fba').checked;
  var er=(n('etx')+n('epp'))/100,eFix=n('epf')+n('elf'),ar=n('ar')/100,mn=n('am');
  var eFul=n('lb'),aFul=fb?n('ff'):n('lb'),plan=n('ap'),pp=q?plan/q:plan;
  var eFee=t?er*t+eFix:0,aRef=t?Math.max(ar*t,mn):0;
  var E=eFee+eFul,A=aRef+aFul+pp;
  function row(l,a,b,c){return '<tr'+(c?' class="total"':'')+'><td>'+l+'</td><td>'+a+'</td><td>'+b+'</td></tr>'}
  $('cmp').innerHTML=row('Buyer pays',m(t),m(t))+row('Etsy fees / referral fee',m(-eFee),m(-aRef))+row('Plan fee per order',m(0),m(-pp))+
    row(fb?'Label / FBA fee':'Shipping label',m(-eFul),m(-aFul))+row('Fees + fulfillment',m(-E),m(-A),1)+row('You keep (before item cost)',m(t-E),m(t-A))+
    row('Fees per month ('+q+' orders)',m(eFee*q),m(aRef*q+plan));
  // crossover: Etsy(T)=er*T+eF, Amazon(T)=max(ar*T,mn)+aF
  var eF=eFix+eFul,aF=aFul+pp,K=ar>0?mn/ar:Infinity,roots=[];
  if(er>0){var t1=(mn+aF-eF)/er;if(t1>0&&t1<K)roots.push(t1)}
  if(ar!==er){var t2=(eF-aF)/(ar-er);if(t2>0&&t2>=K)roots.push(t2)}
  roots.sort(function(a,b){return a-b});
  function who(T){var d=(Math.max(ar*T,mn)+aF)-(er*T+eF);return d>0?'Etsy':d<0?'Amazon Handmade':'Tie'}
  var b=[0].concat(roots),parts=[];
  for(var i=0;i<b.length;i++){var lo=b[i],hi=i+1<b.length?b[i+1]:null,w=who(hi===null?lo+1000:(lo+hi)/2);
    parts.push((hi===null?(i?'Over '+m(lo):'At every order total'):(i?m(lo)+' to '+m(hi):'Under '+m(hi)))+': '+w+' is cheaper.')}
  $('cross').textContent=parts.join(' ')+(roots.length?' (Order total, item + shipping, with the costs above.)':'');
  if(!t){$('big').textContent='-';verdict(false,'Enter an item price to compare Etsy and Amazon Handmade.');return}
  var d=A-E;
  $('big').textContent=(d>=0?'Etsy':'Amazon')+', by '+m(Math.abs(d));
  if(d>=0)verdict(true,'Etsy costs '+m(d)+' less per order, '+m(d*q)+' a month at '+q+' orders. Amazon\\'s '+pc(ar,1)+' referral rate is higher than Etsy\\'s '+pc(er,1)+', so the gap grows with the order size.');
  else verdict(true,'Amazon Handmade costs '+m(-d)+' less per order, '+m(-d*q)+' a month at '+q+' orders. Remember Etsy Offsite Ads would widen this gap; Amazon has no equivalent fee.');
}""",
    note="US rates as of October 2026. Amazon Handmade: 15% referral fee on the total sale price including shipping, with a $1.00 minimum per item under Amazon Handmade's rules (editable, as Amazon can change it); the Professional selling plan fee is waived for approved Handmade artisans. Etsy: 6.5% transaction + 3% + $0.25 processing + $0.20 listing per item sold. FBA fees depend on size, weight and season, so enter your own. One item per order; sales tax and Etsy Offsite Ads left out.",
    body="""<h2>Two different fee shapes</h2>
<p><strong>Etsy</strong> takes a smaller percentage plus fixed amounts: 6.5% + 3% of the order, plus $0.25 processing and $0.20 listing, about 9.5% + $0.45. <strong>Amazon Handmade</strong> takes one bigger percentage, a 15% referral fee on the item and shipping, with a $1.00 minimum per item, and nothing fixed on top. Approved Handmade artisans don't pay the $39.99 monthly Professional plan fee that other Amazon sellers pay.</p>
<p>Because one has the higher rate and the other the fixed fee, the lines cross. On small orders, Etsy's fixed $0.45 weighs more than Amazon's extra 5.5 points. On anything bigger, Amazon's 15% costs more. Amazon's $1.00 minimum adds a second crossing at the very bottom.</p>
<p class="formula">Etsy = 9.5% x order + $0.45 &nbsp;|&nbsp; Amazon Handmade = max(15% x order, $1.00)<br>Crossover: 15% x T = 9.5% x T + $0.45, so T = $0.45 / 5.5% = $8.18</p>
<h2>A worked example</h2>
<p>A $35 necklace with $5 shipping is a $40 order. Etsy takes <strong>$4.25</strong>; Amazon Handmade takes <strong>$6.00</strong>. With the same $6 label on both, Etsy saves you $1.75 an order, $35.00 a month at 20 orders.</p>
<p>The calculator solves the crossover with your numbers. With the defaults, Amazon is cheaper only between $5.79 and $8.18. A $6 order shows why: Etsy's fees are $1.02, Amazon's minimum is $1.00.</p>
<h2>Where FBA changes the answer</h2>
<p>If you send stock to Amazon's warehouses, the FBA fee replaces your own label and packing. When the FBA fee is lower than what you spend to ship an order yourself, Amazon can win on much larger orders. With a $5.00 FBA fee against your $6 label, Amazon is cheaper on every order under $26.36. Your FBA fee depends on the item's size and weight, so check it in Amazon's fee preview before you rely on this. FBA also adds storage and inbound shipping costs not shown here.</p>
<h2>Beyond fees</h2>
<p>Etsy shoppers come looking for handmade and personalized items; Amazon Handmade puts your work in front of people already shopping on Amazon, often with Prime delivery expectations. Amazon Handmade requires an application and approval as an artisan; Etsy lets anyone open a shop. Etsy also charges Offsite Ads on some orders, which this comparison leaves out; if many of your orders come from them, see the <a href="../etsy-offsite-ads-calculator/">Offsite Ads calculator</a>.</p>""",
    faqs=[
        ("What are Amazon Handmade's fees?", "A 15% referral fee on the item price plus shipping, with a minimum of $1.00 per item, and no monthly Professional plan fee for approved artisans. On a $40 order that is $6.00."),
        ("Is Amazon Handmade cheaper than Etsy?", "Usually not on fees. On a $40 order Etsy takes $4.25 and Amazon Handmade $6.00. Amazon only wins on very small orders, or when FBA costs you less than shipping the order yourself."),
        ("Does Amazon Handmade have a monthly fee?", "Not for approved Handmade artisans: the $39.99 Professional plan fee is waived. If it were charged, at 20 orders a month it would add about $2.00 per order, and Etsy would be cheaper at every order total."),
        ("Can I sell the same items on Etsy and Amazon Handmade?", "Yes, as long as each item meets Amazon Handmade's rules for handmade goods. Selling on both means tracking stock and profit in two places, since each reports fees in its own format."),
    ],
    related=["etsy-vs-ebay", "etsy-vs-shopify", "amazon-fba-calculator", "etsy-fee-calculator", "handmade-pricing-calculator"],
    og_image="pins/pin-14.png",
    tests=[
        {"expect": {"big": "Etsy, by $1.75", "cmp": ["$40.00", "-$4.25", "-$6.00", "$85.00", "$120.00"], "verdict": ["$1.75", "$35.00"], "cross": ["Under $5.79: Etsy", "$5.79 to $8.18: Amazon Handmade", "Over $8.18: Etsy"]}},
        {"set": {"pr": "6", "sh": "0"}, "expect": {"big": "Amazon, by $0.02", "cmp": ["-$1.02", "-$1.00"]}},
        {"click": ["fba"], "expect": {"big": "Etsy, by $0.75", "cmp": "-$5.00", "cross": ["Under $26.36: Amazon Handmade", "Over $26.36: Etsy"]}},
        {"set": {"ap": "39.99"}, "expect": {"cmp": ["-$2.00", "$159.99"], "cross": "At every order total: Etsy is cheaper."}},
        {"set": {"am": "0.30", "pr": "6", "sh": "0"}, "expect": {"cmp": "-$0.90", "big": "Amazon, by $0.12"}},
        {"set": {"pr": "0", "sh": "0"}, "expect": {"big": "-", "verdict": "Enter an item price"}},
    ],
)
