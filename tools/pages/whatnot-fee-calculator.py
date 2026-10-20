PAGE = dict(
    slug="whatnot-fee-calculator",
    cat="Platform fees",
    gig="profit",
    nav_name="Whatnot fee calculator",
    title="Whatnot Fee Calculator 2026: Commission Tiers, Processing and Profit",
    desc="Free Whatnot fee calculator with the September 2026 commission tiers: commission by category on the item price, 2.9% + $0.30 processing on the full order, your payout, profit and break-even bid.",
    h1="Whatnot fee calculator",
    lead="Enter one Whatnot sale. The calculator applies your category's commission at your sales tier to the item price only (8% at the Standard tier, 4% for coins), charges 2.9% + $0.30 processing on everything the buyer pays (item, shipping and sales tax), then takes off your item cost to show your payout, profit and the lowest winning bid that breaks even.",
    form="""      <label for="item">Sale price or winning bid <small>(after any coupon you give)</small></label>
      <div class="in"><span>$</span><input id="item" type="number" inputmode="decimal" min="0" step="0.01" value="25"></div>
      <label for="ship">Shipping the buyer pays <small>(it pays for the label, but processing is charged on it)</small></label>
      <div class="in"><span>$</span><input id="ship" type="number" inputmode="decimal" min="0" step="0.01" value="6"></div>
      <label for="tax">Buyer's sales tax rate <small>(Whatnot collects and remits it; the rate varies by place and item)</small></label>
      <div class="in"><input id="tax" type="number" inputmode="decimal" min="0" step="0.1" value="8"><span>%</span></div>
      <label class="check"><input id="ts" type="checkbox" checked> The buyer's state also taxes shipping (29 states and DC generally do)</label>
      <label for="cat">Category <small>(the show's category for live sales)</small></label>
      <select id="cat" class="full"><option value="sports">Sports</option><option value="tcg" selected>Trading card games (TCG)</option><option value="fashion">Fashion</option><option value="oc">Other collectibles</option><option value="coins">Coins &amp; money</option><option value="other">Other</option></select>
      <label for="tier">Your tier <small>(set by last 4-week period's sales)</small></label>
      <select id="tier" class="full"><option value="0" selected>Standard (under $15,000 in 4-week sales)</option><option value="1">Tier 1 ($15,000 to $34,999)</option><option value="2">Tier 2 ($35,000 to $49,999)</option><option value="3">Tier 3 ($50,000 to $99,999)</option><option value="4">Tier 4 ($100,000 to $249,999)</option><option value="5">Tier 5 ($250,000 to $499,999)</option><option value="6">Tier 6 ($500,000 and up)</option></select>
      <p id="rnow" class="note" style="margin:6px 0 0"></p>
      <label for="cost">What the item cost you</label>
      <div class="in"><span>$</span><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="10"></div>
      <label for="sship">Shipping you cover <small>(free or capped shipping, 0 if the buyer pays it all)</small></label>
      <div class="in"><span>$</span><input id="sship" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
      <label class="check"><input id="hv" type="checkbox"> High-value promo: the item is in an eligible category (0% commission on the part above $1,500)</label>
      <details><summary class="note">Edit fee rates</summary>
      <label for="ovr">Your commission rate <small>(blank uses the rate card; type your Seller Hub rate, or 0 during a 0% promo)</small></label>
      <div class="in"><input id="ovr" type="number" inputmode="decimal" min="0" step="0.01" value="" placeholder="from rate card"><span>%</span></div>
      <label for="pp">Payment processing rate</label>
      <div class="in"><input id="pp" type="number" min="0" step="0.1" value="2.9"><span>%</span></div>
      <label for="pf">Processing fee per order</label>
      <div class="in"><span>$</span><input id="pf" type="number" min="0" step="0.01" value="0.30"></div>
      <label for="thr">High-value threshold <small>(no commission above this)</small></label>
      <div class="in"><span>$</span><input id="thr" type="number" min="0" step="1" value="1500"></div>
      <label for="tc">Sales tax on commission <small>(only DC, HI, NM, WV sellers)</small></label>
      <div class="in"><input id="tc" type="number" min="0" step="0.01" value="0"><span>%</span></div>
      <label for="tpx">Sales tax on processing <small>(only CT, HI, NM, OH, SD, TX, WV sellers)</small></label>
      <div class="in"><input id="tpx" type="number" min="0" step="0.01" value="0"><span>%</span></div>
      </details>""",
    out="""<div class="big"><span>Your profit</span><b id="keep"></b></div>
      <p id="be" style="margin:0 0 8px;text-align:center"></p>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""var R={sports:[8,7.75,7.5,7.25,7,6.75,6.5],tcg:[8,7.75,7.5,7.25,7,6.75,6.5],fashion:[8,7,6.5,5.5,5,4.5,4.5],oc:[8,7.25,6.5,6,5,5,5],coins:[4,3.9,3.8,3.7,3.6,3.55,3.5],other:[8,7,6.5,5.5,4,4,4]};
var TN=['Standard','Tier 1','Tier 2','Tier 3','Tier 4','Tier 5','Tier 6'];
var r2=function(x){return Math.round(x*100+1e-7)/100};
var tp=function(x){return (+x.toFixed(2))+'%'};
function calc(){
  var own=$('ovr').value.trim()!=='',ti=parseInt($('tier').value,10)||0,ct=$('cat'),cr=own?n('ovr'):(R[ct.value]||R.tcg)[ti],c=cr/100;
  $('rnow').textContent='Commission rate used: '+tp(cr)+(own?', your own rate':' for '+ct.options[ct.selectedIndex].text+' at '+TN[ti]);
  var item=n('item'),ship=n('ship'),tr=n('tax')/100,ts=$('ts').checked,cost=n('cost'),ss=n('sship'),pp=n('pp')/100,pf=n('pf'),thr=n('thr'),tc=n('tc')/100,tx=n('tpx')/100,hv=$('hv').checked&&thr>0;
  function F(x){var t=r2((x+(ts?ship:0))*tr),b=r2(x+ship+t),bs=hv?Math.min(x,thr):x,cm=r2(c*bs),cx=r2(cm*tc),pr=r2(pp*b+pf),pt=r2(pr*tx),fe=r2(cm+cx+pr+pt),pa=r2(x-fe-ss);return {tax:t,buyer:b,base:bs,comm:cm,ctax:cx,proc:pr,ptax:pt,fees:fe,pay:pa,profit:r2(pa-cost)}}
  if(!item){$('keep').textContent=m(0);$('be').innerHTML='Break-even winning bid: <b>-</b>';setRows([['Enter the sale price or winning bid to see Whatnot fees.','']]);verdict(false,'No sale entered yet.');return}
  var f=F(item),tax=f.tax,buyer=f.buyer,base=f.base,comm=f.comm,ctax=f.ctax,proc=f.proc,ptax=f.ptax,fees=f.fees,pay=f.pay,profit=f.profit;
  var k=c*(1+tc),q=pp*(1+tr)*(1+tx),num=cost+ss+(pp*ship*(ts?1+tr:1)+pf)*(1+tx),sl=1-k-q,den=sl,be=den>0?num/den:-1;
  if(hv&&be>thr){den=1-q;be=(num+k*thr)/den}
  var beT='-';
  // cent rounding makes profit wobble near zero, so scan up from safely below the exact answer to find the lowest bid with profit >= 0
  if(be>=0){var bc=Math.max(1,Math.floor((be-0.1/sl)*100)),i=0;while(i++<20000&&F(bc/100).profit<0)bc++;if(i<=20000)beT=m(bc/100)}
  var r=[['Buyer pays ('+m(item)+' item + '+m(ship)+' shipping + '+m(tax)+' tax)',m(buyer)],
    ['Commission ('+tp(cr)+' of '+(base<item?'the first '+m(base):m(item))+')',m(-comm)]];
  if(ctax)r.push(['Sales tax on commission ('+tp(n('tc'))+')',m(-ctax)]);
  r.push(['Payment processing ('+tp(n('pp'))+' of '+m(buyer)+' + '+m(pf)+')',m(-proc)]);
  if(ptax)r.push(['Sales tax on processing ('+tp(n('tpx'))+')',m(-ptax)]);
  r.push(['Total Whatnot fees ('+pc(fees/item)+' of the sale price)',m(-fees)]);
  if(ss)r.push(['Shipping you cover',m(-ss)]);
  r.push(['Whatnot pays you',m(pay),'total'],['What the item cost you',m(-cost)],['Your profit',m(profit),'total']);
  setRows(r);$('keep').textContent=m(profit);$('be').innerHTML='Break-even winning bid: <b>'+beT+'</b>';
  if(profit<0)verdict(false,'This sale loses '+m(-profit)+'. Your break-even winning bid is '+beT+'.');
  else verdict(true,'Whatnot takes '+pc(fees/item)+' of your '+m(item)+' sale. You keep '+m(profit)+' profit, a profit margin of '+pc(profit/item)+'.');
}""",
    note="""US Whatnot rates checked October 20, 2026 in Whatnot's Help Center: <a href="https://help.whatnot.com/hc/en-us/articles/4847069165965-Whatnot-seller-fees" rel="noopener">Whatnot seller fees</a>, <a href="https://help.whatnot.com/hc/en-us/articles/27912945518733-Reduced-Commission-on-High-Value-Orders" rel="noopener">Reduced Commission on High-Value Orders</a>, <a href="https://help.whatnot.com/hc/en-us/articles/14477076380941-Reduced-commission-on-Coins-Money" rel="noopener">Reduced commission on Coins &amp; Money</a>, <a href="https://help.whatnot.com/hc/en-us/articles/32083195713421-Taxes-on-Whatnot-commissions-and-fees" rel="noopener">Taxes on Whatnot commissions and fees</a>, <a href="https://help.whatnot.com/hc/en-us/articles/360061196012-U-S-Sales-Tax-Collection-on-Whatnot" rel="noopener">U.S. Sales Tax Collection on Whatnot</a>, <a href="https://help.whatnot.com/hc/en-us/articles/4412099990157-Taxes-on-shipping" rel="noopener">Taxes on shipping</a> and <a href="https://help.whatnot.com/hc/en-us/articles/36772664621837-Seller-Weekly-Orders-Report" rel="noopener">Seller Weekly Orders Report</a>. The tiered commission started September 21, 2026 for existing sellers. Your total sales in a 4-week period set your tier for the next period, and each sale is charged the rate for the show's category (live) or the product's category (marketplace). Commission is charged on the item price only. Processing is 2.9% + $0.30 per order on the total the buyer pays, including shipping and sales tax. Through October 31, 2026, Premier Shop sellers get 10% off their commission (8% becomes 7.2%); type that rate under Edit fee rates. Promotional rates, such as 0% for new sellers, replace your tier rate while they run, and the $1,500 high-value break is a limited-time promotion. Whatnot lists 29 states and DC that generally charge sales tax on buyer-paid shipping for a taxable item, so the calculator taxes shipping by default; untick that box for a buyer in a state that does not, such as California. Canada, the UK, the EU, Australia and Japan use different thresholds or rates. Your exact rate is in Seller Hub.""",
    body="""<h2>How Whatnot fees work</h2>
<p><strong>Commission.</strong> Whatnot takes a percentage of the item's sale price, after any coupon you gave. Shipping and sales tax are not included. Since September 21, 2026 the rate depends on two things: your tier, set by your total sales in all categories over the last 4-week period, and the category of the sale. For a live sale that is the show's category; for a marketplace sale it is the product's category. The Standard rate is 8% (4% for coins), and it drops as your 4-week sales grow.</p>
<p><strong>Payment processing.</strong> 2.9% + $0.30 per order in the US, charged on everything the buyer pays: the item, the shipping and the sales tax. Tiers do not lower it. On cheap items this is the fee that hurts, because the $0.30 and the 2.9% on shipping stay the same however low the bid goes.</p>
<p><strong>Shipping.</strong> Buyers pay shipping by default, and that money buys the label, so it is not income. When the item is taxable, 29 states and DC generally charge the buyer sales tax on that shipping too, and processing is charged on that tax as well. Some sellers can offer free shipping in their shows, or cap what buyers pay and cover the rest; the part you cover comes out of your payout. <a href="https://help.whatnot.com/hc/en-us/articles/15788140338957-Offer-free-or-discounted-shipping" rel="noopener">Whatnot's own example</a>: with a $7.75 cap and a $20 shipping cost, the buyer pays $7.75 and you pay $12.25.</p>
<p><strong>Sales tax on fees.</strong> <a href="https://help.whatnot.com/hc/en-us/articles/32083195713421-Taxes-on-Whatnot-commissions-and-fees" rel="noopener">Whatnot says</a> a few states make it charge sales tax on its fees, which it takes from your earnings. Commission is taxed for sellers in DC, Hawaii, New Mexico and West Virginia. Processing is taxed in Connecticut (at a special 1%), Hawaii, New Mexico, Ohio, South Dakota, Texas (your full sales tax rate cut by 20%, so Houston's 8.25% becomes 6.6%) and West Virginia. Resale certificates don't exempt you. Enter your rate under Edit fee rates.</p>
<p><strong>Cancellation fee.</strong> If you cancel an order for a reason in your control, <a href="https://help.whatnot.com/hc/en-us/articles/360061603971-Cancel-an-order-before-you-ship" rel="noopener">Whatnot may charge</a> $3 or 3% of the order total, whichever is higher. You see whether a fee applies before you confirm. Your first one is waived, and accepting a buyer's cancellation request made through Whatnot carries no fee.</p>
<h2>US commission rates by tier</h2>
<p>Effective September 21, 2026. Tier thresholds are your total sales across all categories in one 4-week period.</p>
<div style="overflow-x:auto">
<table class="wide"><thead><tr><th>Tier (4-week sales)</th><th>Sports, TCG</th><th>Fashion</th><th>Other collect.</th><th>Coins</th><th>Other</th></tr></thead><tbody>
<tr><td>Standard (up to $14,999)</td><td>8.00%</td><td>8.00%</td><td>8.00%</td><td>4.00%</td><td>8.00%</td></tr>
<tr><td>Tier 1 ($15,000+)</td><td>7.75%</td><td>7.00%</td><td>7.25%</td><td>3.90%</td><td>7.00%</td></tr>
<tr><td>Tier 2 ($35,000+)</td><td>7.50%</td><td>6.50%</td><td>6.50%</td><td>3.80%</td><td>6.50%</td></tr>
<tr><td>Tier 3 ($50,000+)</td><td>7.25%</td><td>5.50%</td><td>6.00%</td><td>3.70%</td><td>5.50%</td></tr>
<tr><td>Tier 4 ($100,000+)</td><td>7.00%</td><td>5.00%</td><td>5.00%</td><td>3.60%</td><td>4.00%</td></tr>
<tr><td>Tier 5 ($250,000+)</td><td>6.75%</td><td>4.50%</td><td>5.00%</td><td>3.55%</td><td>4.00%</td></tr>
<tr><td>Tier 6 ($500,000+)</td><td>6.50%</td><td>4.50%</td><td>5.00%</td><td>3.50%</td><td>4.00%</td></tr>
</tbody></table>
</div>
<p>Whatnot's fee page does not list which of its categories fall in each column, so check the rate card in Seller Hub for your category. Your rate is locked for the whole period: cross a threshold mid-period and the lower rate starts next period. Cancelled orders come off your total.</p>
<h2>The formula</h2>
<p class="formula">Whatnot pays you = item price - commission rate x item price - (2.9% x (item + shipping + tax) + $0.30) - any state tax on those fees - shipping you cover</p>
<p>Profit is that payout minus what the item cost you. The break-even winning bid is the lowest price where profit reaches zero, after the commission and processing that price itself adds.</p>
<h2>Worked example</h2>
<p>You sell a trading card for <strong>$25</strong> at the Standard tier (8%). The buyer pays $6 shipping plus 8% sales tax on the item and the shipping ($2.48), so the buyer pays <strong>$33.48</strong>. Commission is 8% of $25 = <strong>$2.00</strong>. Processing is 2.9% of $33.48 + $0.30 = <strong>$1.27</strong>. Total fees are <strong>$3.27</strong>, 13.1% of the sale price, and Whatnot pays you <strong>$21.73</strong>. After a $10 item cost your profit is <strong>$11.73</strong>, a 46.9% margin. The break-even winning bid is <strong>$11.80</strong>: at that price the fees come to $1.80 and your profit is exactly $0.00.</p>
<p>At Tier 3 (7.25%) the same card pays $1.81 commission, so fees are $3.08, you get $21.92 and keep $11.92. The break-even bid drops to $11.70.</p>
<p>A $1 start that sells for $1, with the same $6 shipping: the buyer pays $7.56, commission is $0.08 and processing $0.52, so fees are $0.60, 60.0% of the sale. If the item cost you $0.50, you lose $0.10. That item needs a $1.11 bid just to break even.</p>
<p>A $2,000 card with the high-value promo: the buyer pays $2,166.48 with tax. Commission is 8% of the first $1,500 = <strong>$120.00</strong>, the same figure as Whatnot's own example, and processing on the full $2,166.48 is $63.13. Whatnot pays you $1,816.87, a $616.87 profit after a $1,200 cost. Without the promo the commission would be $160.00.</p>
<p>The same $25 sale as a coin (4%) by a seller in Houston, Texas who also covers $2 of shipping: commission $1.00, processing $1.27 plus $0.08 sales tax on it at 6.6% (Houston's 8.25% cut by 20%, the rate in Whatnot's own example), so Whatnot pays $20.65 and the profit is $10.65.</p>
<h2>Tips for Whatnot sellers</h2>
<p>On $1 starts, the real cost is not the commission. It is the $0.30 plus 2.9% of the shipping and tax, which you pay even when the bid stays at $1. Know your break-even bid before you run an item at $1.</p>
<p>A tier you reach this period only pays off next period, and every period starts again from zero. If you are close to a threshold near the end of a period, the extra sales can lower your rates for the whole next 4 weeks.</p>
<p>The headline 3% rate is a custom deal for the very largest sellers who work with an account manager. It is not on the public rate card. And don't list in a cheaper category than what you sell: Whatnot treats that as fee avoidance.</p>""",
    faqs=[
        ("How much does Whatnot take from a $25 sale?", "$3.27 if the buyer pays $6 shipping and 8% sales tax on the item and shipping, at the Standard 8% rate: $2.00 commission on the item plus $1.27 processing (2.9% of the $33.48 the buyer pays, plus $0.30). That is 13.1% of the sale price. For a trading card or sports item at Tier 3 (7.25%) it drops to $3.08."),
        ("Does Whatnot charge fees on shipping and sales tax?", "Commission, no: it is charged on the item price only, after any seller coupon. Processing, yes: 2.9% + $0.30 is charged on the full amount the buyer pays, including shipping and sales tax. On a $25 card with $6 shipping and $2.48 tax, processing is charged on $33.48."),
        ("How do Whatnot's commission tiers work?", "Your total sales across all categories in a 4-week (28-day) period set your tier for the next period. The US thresholds are $15,000 for Tier 1, $35,000 for Tier 2, $50,000 for Tier 3, $100,000 for Tier 4, $250,000 for Tier 5 and $500,000 for Tier 6. Your rate is locked for the whole period, and each sale is charged its category's rate at your tier. Cancelled orders, private shows and local pickup orders come off the total. Rates as low as 3% are custom deals for the largest sellers."),
        ("What is the $1,500 high-value commission break?", "Since January 14, 2026, Whatnot charges 0% commission on the part of an item's sale price above $1,500 in Comics &amp; Anime, Toys &amp; Hobbies, Coins &amp; Money, Trading Card Games, Entertainment Cards, the Sports Singles subcategories, Bags &amp; Accessories and Jewelry &amp; Watches (the last two were added June 4, 2026). Sports breaks and Surprise Products are excluded, and processing is still charged on the full order. A $2,000 sale at 8% pays $120 commission instead of $160. Whatnot's example uses 8% on the first $1,500; the calculator applies your selected rate there, and Seller Hub shows the exact charge. It is a limited-time promotion."),
    ],
    related=["ebay-fee-calculator", "poshmark-fee-calculator", "paypal-fee-calculator", "stripe-fee-calculator", "profit-margin-calculator", "break-even-calculator"],
    tests=[
        {"expect": {"rows": ["$33.48", "$2.48 tax", "-$2.00", "-$1.27", "-$3.27", "13.1%", "$21.73", "-$10.00"], "keep": "$11.73", "be": "$11.80", "verdict": ["13.1%", "46.9%"]}},
        {"set": {"tier": "3"}, "expect": {"rows": ["7.25%", "-$1.81", "-$3.08", "$21.92"], "keep": "$11.92", "be": "$11.70", "rnow": "7.25%"}},
        {"set": {"item": "2000", "cost": "1200"}, "click": ["hv"], "expect": {"rows": ["$2,166.48", "first $1,500.00", "-$120.00", "-$63.13", "-$183.13", "$1,816.87"], "keep": "$616.87"}},
        {"set": {"item": "1", "cost": "0.5"}, "expect": {"rows": ["$7.56", "-$0.08", "-$0.52", "-$0.60", "60.0%"], "keep": "-$0.10", "be": "$1.11", "verdict": ["loses $0.10", "$1.11"]}},
        {"set": {"cat": "coins", "sship": "2", "tpx": "6.6"}, "expect": {"rows": ["-$1.00", "-$1.27", "-$0.08", "-$2.00", "$20.65"], "keep": "$10.65"}},
        {"set": {"tax": "10.25", "cat": "sports", "cost": "30.11", "sship": "5"}, "click": ["ts"], "expect": {"rows": ["$33.56", "$2.56 tax", "-$3.27", "$16.73"], "keep": "-$13.38", "be": "$40.06", "verdict": "$40.06"}},
    ],
)
