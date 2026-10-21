PAGE = dict(
    slug="etsy-digital-download-calculator",
    cat="Etsy tools",
    cta_extra=["sizekit"],
    nav_name="Etsy digital download calculator",
    title="Etsy Digital Download Calculator: Fees, Profit and Sales Goal",
    desc="Selling printables, patterns or SVGs on Etsy? See the fees on each digital sale, what you keep, and how many sales a month it takes to reach your income goal.",
    h1="Etsy digital download calculator",
    lead="Digital products have no materials and no shipping, so Etsy's fees are nearly your only cost. On a cheap file they take a bigger bite than most sellers expect. Enter your price to see the fees, what you keep, and how many sales a month your income goal needs.",
    form="""      <label for="price">Price of the download</label>
      <div class="in"><span>$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="8"></div>
      <label for="share">Sales from Offsite Ads</label>
      <div class="in"><input id="share" type="number" inputmode="decimal" min="0" max="100" step="1" value="0"><span>%</span></div>
      <label class="check"><input id="fx" type="checkbox"> My listing currency differs from my bank currency (2.5% conversion)</label>
      <label for="goal">Monthly income goal <small>(take-home)</small></label>
      <div class="in"><span>$</span><input id="goal" type="number" inputmode="decimal" min="0" step="10" value="500"></div>
      <label for="mcost">Monthly costs <small>(design software, font and graphics licenses, Etsy Plus)</small></label>
      <div class="in"><span>$</span><input id="mcost" type="number" inputmode="decimal" min="0" step="1" value="10"></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="tx">Transaction fee</label>
      <div class="in"><input id="tx" type="number" min="0" step="0.1" value="6.5"><span>%</span></div>
      <label for="pp">Payment processing</label>
      <div class="in"><input id="pp" type="number" min="0" step="0.1" value="3"><span>% +</span><span>$</span><input id="pf" type="number" min="0" step="0.01" value="0.25"></div>
      <label for="lfee">Listing fee per sale</label>
      <div class="in"><span>$</span><input id="lfee" type="number" min="0" step="0.01" value="0.20"></div>
      <label for="oa">Offsite Ads rate <small>(12% if your shop made over $10k last year)</small></label>
      <div class="in"><input id="oa" type="number" min="0" step="1" value="15"><span>%</span></div>
      </details>""",
    out="""<div class="big"><span>Sales per month for your goal</span><b id="need"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>
      <h3>Fees by price point</h3>
      <table class="wide"><thead><tr><th>Price</th><th>Fees</th><th>Fee %</th><th>You keep</th></tr></thead><tbody id="tbl"></tbody></table>""",
    js="""function parts(p){
  var sh=Math.min(n('share'),100)/100;
  return {tx:p*n('tx')/100,pp:p*n('pp')/100+n('pf'),lf:n('lfee'),oa:sh*Math.min(p*n('oa')/100,100),fx:$('fx').checked?p*0.025:0};
}
function tot(f){return f.tx+f.pp+f.lf+f.oa+f.fx}
function calc(){
  var h='';[2,5,10,20].forEach(function(q){var f=tot(parts(q));h+='<tr><td>'+m(q)+'</td><td>'+m(f)+'</td><td>'+pc(f/q)+'</td><td>'+m(q-f)+'</td></tr>'});
  $('tbl').innerHTML=h;
  var p=n('price');
  if(!p){$('need').textContent='-';setRows([]);verdict(false,'Enter a price to see the fees on one sale.');return}
  var f=parts(p),fees=tot(f),k=p-fees,goal=n('goal')+n('mcost');
  var r=[['Buyer pays',m(p)],['Transaction fee',m(-f.tx)],['Payment processing',m(-f.pp)],['Listing fee',m(-f.lf)]];
  if(f.oa)r.push(['Offsite Ads (average per sale)',m(-f.oa)]);
  if(f.fx)r.push(['Currency conversion',m(-f.fx)]);
  r.push(['Total fees',m(-fees)+' ('+pc(fees/p)+')'],['You keep per sale',m(k),'total']);
  setRows(r);
  if(k<=0){$('need').textContent='-';verdict(false,'Fees take the whole price. Raise it or sell it in a bundle.');return}
  var need=Math.ceil(goal/k-1e-9);$('need').textContent=goal?need+' sales':'-';
  if(fees/p>0.2)verdict(false,'Etsy takes '+pc(fees/p,0)+' of every sale at this price. A bundle at a higher price keeps more of each dollar.'+(goal?' You need '+need+' sales a month for '+m(n('goal'))+'.':''));
  else verdict(true,'You keep '+m(k)+' of every '+m(p)+' sale.'+(goal?' That is '+need+' sales a month, about '+Math.ceil(need/30)+' a day, for '+m(n('goal'))+' after '+m(n('mcost'))+' of monthly costs.':''));
}""",
    note="US Etsy rates as of October 2026: 6.5% transaction fee, 3% + $0.25 payment processing, $0.20 listing fee charged again each time a digital listing sells, Offsite Ads 15% (12% over $10k/yr) on ad-driven sales, 2.5% currency conversion when your listing and bank currencies differ. One item per order. Sales tax and VAT that Etsy collects from buyers are left out, as is income tax.",
    body="""<h2>What Etsy charges on a digital download</h2>
<p>A digital listing pays the same fees as a physical one: the <strong>6.5% transaction fee</strong>, <strong>3% + $0.25 processing</strong> and the <strong>$0.20 listing fee</strong>, which Etsy charges again every time the listing sells and renews. There is no shipping and no label, so the fees are usually your only cost per sale.</p>
<p class="formula">You keep per sale = price &times; (1 &minus; 9.5%) &minus; $0.45</p>
<p class="formula">Sales per month = (income goal + monthly costs) &divide; what you keep per sale</p>
<h2>Worked example</h2>
<p>An $8 printable. Etsy takes $0.52 in transaction fees, $0.49 processing and $0.20 for the listing: <strong>$1.21</strong>, or 15.1%. You keep <strong>$6.79</strong>. To take home $500 a month after $10 of software costs, you need <strong>76 sales</strong> a month.</p>
<p>If 20% of your sales come from Offsite Ads and you're paid in a different currency, fees rise to $1.65 a sale (20.6%), you keep $6.35, and the same goal takes 81 sales.</p>
<h2>Why cheap downloads lose so much to fees</h2>
<p>The $0.45 of fixed fees per order is the same on a $2 file and a $20 one. The table under the calculator shows the effect: at $2 Etsy takes 32.0% of the sale, at $5 it takes 18.5%, at $10 it's 14.0%. At $3, the 133 sales you'd need for a $300 month means fees eat almost a quarter of everything buyers pay.</p>
<p>Three ways around it:</p>
<p><strong>Bundle.</strong> Ten $2 coloring pages sold separately pay the fixed fees ten times. As one $12 bundle they pay it once.</p>
<p><strong>Encourage multi-item orders.</strong> The $0.25 processing fee is per order, so a buyer who adds three files to one cart pays it once. A shop coupon for 3+ items can pay for itself.</p>
<p><strong>Price on value, not effort.</strong> A file costs nothing to copy, so the price should reflect what it saves or gives the buyer, not how long it took you this one time.</p>
<p>With a large catalog of low-priced files, the per-listing view in your sales export shows which designs actually carry the shop.</p>""",
    faqs=[
        ("How much does Etsy take from a digital download sale?", "In the US, 6.5% transaction fee, 3% + $0.25 processing and $0.20 listing fee. On an $8 download that is $1.21, leaving you $6.79."),
        ("Do I pay the listing fee every time a digital item sells?", "Yes. Each sale renews the listing for another $0.20, even though the file never runs out. That is why the fixed fees matter so much on low prices."),
        ("What's the cheapest price that makes sense for an Etsy digital download?", "There is no hard floor, but at $2 Etsy takes 32.0% of each sale and at $5 it takes 18.5%. Many sellers bundle small files to get the price up and the fee share down."),
        ("Do Offsite Ads apply to digital products?", "Yes. If a buyer comes through an Etsy ad on another site and buys within 30 days, the 15% fee (or 12%) applies to digital items too. Enter your share of ad sales to include it."),
    ],
    related=["etsy-fee-calculator", "etsy-offsite-ads-calculator", "gumroad-fee-calculator", "etsy-profit-calculator", "etsy-sale-calculator"],
    og_image="pins/pin-06.png",
    tests=[
        {"expect": {"need": ["76 sales"], "rows": ["$8.00", "-$0.52", "-$0.49", "-$0.20", "-$1.21", "15.1%", "$6.79"], "tbl": ["32.0%", "18.5%", "14.0%"]}},
        {"set": {"share": "20"}, "click": ["fx"], "expect": {"need": ["81 sales"], "rows": ["-$1.65", "20.6%", "$6.35"]}},
        {"set": {"price": "3", "goal": "300", "mcost": "0"}, "expect": {"need": ["133 sales"], "rows": ["24.5%"]}},
        {"set": {"price": "0"}, "expect": {"verdict": ["Enter a price"], "tbl": ["32.0%"]}},
        {"set": {"price": "0.40"}, "expect": {"verdict": ["Fees take the whole price"]}},
    ],
)
