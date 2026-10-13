PAGE = dict(
    slug="etsy-ads-calculator",
    cat="Etsy tools",
    nav_name="Etsy Ads ROAS calculator",
    title="Etsy Ads Calculator: Break-Even ROAS and Cost Per Click",
    desc="Is your Etsy Ads budget making money? Enter budget, cost per click and conversion rate for orders, cost per order, ROAS, break-even ROAS and profit.",
    h1="Etsy Ads calculator: are your ads paying for themselves?",
    lead="Etsy Ads (the promoted listings inside Etsy search) charge you per click. Enter your daily budget, what a click costs and how often clicks turn into orders. You get orders per month, the ad cost of each order, your ROAS against the break-even ROAS, and whether the ads add or take away profit.",
    form="""      <label for="budget">Daily budget</label>
      <div class="in"><span>$</span><input id="budget" type="number" inputmode="decimal" min="0" step="0.5" value="5"><span>/day</span></div>
      <label for="cpc">Average cost per click</label>
      <div class="in"><span>$</span><input id="cpc" type="number" inputmode="decimal" min="0" step="0.01" value="0.35"></div>
      <label for="cr">Conversion rate <small>(orders &divide; clicks)</small></label>
      <div class="in"><input id="cr" type="number" inputmode="decimal" min="0" max="100" step="0.1" value="2.5"><span>%</span></div>
      <label for="aov">Average order value <small>(item + shipping the buyer pays)</small></label>
      <div class="in"><span>$</span><input id="aov" type="number" inputmode="decimal" min="0" step="0.01" value="40"></div>
      <label for="pmode">Profit per order before ads</label>
      <select id="pmode" class="full"><option value="calc">Work it out from my costs</option><option value="enter">I know it, let me enter it</option></select>
      <div id="wcalc"><label for="costs">Materials + packaging + label per order</label>
      <div class="in"><span>$</span><input id="costs" type="number" inputmode="decimal" min="0" step="0.01" value="14"></div></div>
      <div id="wenter" style="display:none"><label for="profit">Profit per order before ads</label>
      <div class="in"><span>$</span><input id="profit" type="number" inputmode="decimal" min="0" step="0.01" value="12"></div></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="tx">Transaction fee</label>
      <div class="in"><input id="tx" type="number" min="0" step="0.1" value="6.5"><span>%</span></div>
      <label for="pp">Payment processing</label>
      <div class="in"><input id="pp" type="number" min="0" step="0.1" value="3"><span>% +</span><span>$</span><input id="pf" type="number" min="0" step="0.01" value="0.25"></div>
      <label for="lfee">Listing fee per item sold</label>
      <div class="in"><span>$</span><input id="lfee" type="number" min="0" step="0.01" value="0.20"></div>
      <label for="days">Days per month</label>
      <div class="in"><input id="days" type="number" min="1" step="1" value="30"></div>
      </details>""",
    out="""<div class="big"><span>Profit added by Etsy Ads per month</span><b id="net"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var enter=$('pmode').value=='enter';
  $('wcalc').style.display=enter?'none':'';$('wenter').style.display=enter?'':'none';
  var b=n('budget'),cpc=n('cpc'),cr=Math.min(n('cr'),100)/100,aov=n('aov'),days=n('days')||30;
  var pr=enter?n('profit'):aov-aov*(n('tx')+n('pp'))/100-n('pf')-n('lfee')-n('costs');
  if(!b||!cpc||!cr||!aov){$('net').textContent='-';setRows([]);verdict(false,'Enter a daily budget, cost per click, conversion rate and order value. Etsy Ads shows the last three in Shop Manager > Marketing > Etsy Ads.');return}
  var sp=b*days,cl=sp/cpc,o=cl*cr,cpo=cpc/cr,rev=o*aov,roas=rev/sp,net=o*pr-sp;
  var r=[['Ad spend per month',m(sp)],['Clicks per day',(b/cpc).toFixed(1)],['Orders from ads per month',o.toFixed(1)],['Ad cost per order',m(cpo)],['Revenue from ads',m(rev)],['Profit per order before ads',m(pr)],['Your ROAS',roas.toFixed(2)]];
  if(pr>0)r.push(['Break-even ROAS',(aov/pr).toFixed(2)],['Break-even cost per click',m(pr*cr)]);
  else r.push(['Break-even ROAS','none (no profit to spend)']);
  r.push(['Profit added by ads',m(net),'total']);
  setRows(r);$('net').textContent=m(net);
  if(pr<=0)verdict(false,'Each order already loses '+m(-pr)+' before ads. Advertising only makes the loss bigger. Fix the price first.');
  else if(net<0)verdict(false,'Each ad order costs '+m(cpo)+' in clicks but only makes '+m(pr)+'. You need a ROAS of '+(aov/pr).toFixed(2)+' or a cost per click under '+m(pr*cr)+'. Pause the listings with the worst ROAS first.');
  else verdict(true,'Ads cost '+m(cpo)+' per order against '+m(pr)+' of profit. Your ROAS of '+roas.toFixed(2)+' clears the break-even of '+(aov/pr).toFixed(2)+'.');
}""",
    note="Etsy Ads as of October 2026: pay per click, minimum budget $1/day, a daily budget is a maximum and may not all be spent. Fee rates are US: 6.5% transaction, 3% + $0.25 processing, $0.20 listing fee, assuming one item per order. Offsite Ads are a separate fee charged per sale; see the Offsite Ads calculator.",
    body="""<h2>How Etsy Ads cost works</h2>
<p>You set a daily budget. Etsy shows your listings in search and on other Etsy pages, and charges you each time a shopper clicks one. Clicks are priced by auction, so your cost per click moves with competition for your search terms. Only some clicks turn into orders, and that conversion rate decides how much each ad order really costs.</p>
<p class="formula">Ad cost per order = cost per click &divide; conversion rate</p>
<p class="formula">Break-even ROAS = average order value &divide; profit per order before ads</p>
<h2>Worked example</h2>
<p>A $5 daily budget is <strong>$150.00</strong> a month. At $0.35 a click that buys 14.3 clicks a day. With a 2.5% conversion rate, 10.7 orders a month come from ads, so each costs <strong>$14.00</strong> in clicks.</p>
<p>Orders average $40, and after Etsy's fees and $14 of costs each makes <strong>$21.75</strong> before ads. Revenue from ads is $428.57, a ROAS of <strong>2.86</strong>. The break-even ROAS is $40 &divide; $21.75 = <strong>1.84</strong>, and the highest cost per click you can afford is <strong>$0.54</strong>. The ads add <strong>$83.04</strong> of profit a month.</p>
<p>If clicks cost $0.60 instead, ROAS drops to 1.67, under break-even, and the same budget loses $14.06 a month.</p>
<h2>How to compare with the ROAS Etsy shows you</h2>
<p>In Shop Manager &gt; Marketing &gt; Etsy Ads, Etsy reports revenue, spend and ROAS (revenue &divide; spend) for the shop and for each listing. Put that ROAS next to the break-even ROAS above:</p>
<p><strong>Etsy ROAS above break-even:</strong> the ads earn more profit than they cost.</p>
<p><strong>Etsy ROAS below break-even:</strong> every dollar of ads returns less than a dollar of profit, even if the ROAS looks high. A ROAS of 2 sounds good, but if your break-even is 3.33 (a $40 order that only makes $12), you are paying to sell.</p>
<p>Two cautions. Etsy credits an order to the ads if the buyer clicked an ad within its attribution window, so some of those buyers would have found you anyway, and your true ROAS is likely lower than the dashboard says. And a listing-level ROAS on three orders is noise; judge listings on at least a month of data.</p>
<h2>Getting more from the same budget</h2>
<p>Turn off ads on listings with a ROAS under your break-even, so the budget goes to the ones that work. Put ads on listings with higher order values: a $60 order has far more room to pay for clicks than a $12 one. And check this calculator again after any price change, because a price rise lifts your break-even cost per click.</p>""",
    faqs=[
        ("What is a good ROAS for Etsy Ads?", "Any ROAS above your break-even, which is your order value divided by your profit per order before ads. For a $40 order that makes $21.75, break-even is 1.84. For a $40 order that makes $12, it is 3.33."),
        ("How much should I spend on Etsy Ads per day?", "The minimum is $1 a day. Start small, run it for a month, then compare Etsy's ROAS for each listing with your break-even ROAS. Raise the budget only on listings that clear it."),
        ("What is a good cost per click on Etsy?", "One below your break-even cost per click: profit per order times conversion rate. With $21.75 of profit and a 2.5% conversion rate, that is $0.54. Above that, each ad order loses money."),
        ("Are Etsy Ads and Offsite Ads the same thing?", "No. Etsy Ads are optional, run inside Etsy and charge per click from a budget you set. Offsite Ads run on other websites and charge a percentage of the order only when an ad leads to a sale."),
    ],
    related=["roas-calculator", "etsy-offsite-ads-calculator", "etsy-profit-calculator", "etsy-fee-calculator", "break-even-calculator"],
    og_image="pins/pin-05.png",
    tests=[
        {"expect": {"net": ["$83.04"], "rows": ["$150.00", "14.3", "10.7", "$14.00", "$428.57", "$21.75", "2.86", "1.84", "$0.54"]}},
        {"set": {"cpc": "0.60"}, "expect": {"net": ["-$14.06"], "rows": ["1.67"], "verdict": ["ROAS of 1.84"]}},
        {"set": {"pmode": "enter"}, "expect": {"rows": ["3.33", "$0.30"], "net": ["-$21.43"]}},
        {"set": {"cpc": "0"}, "expect": {"verdict": ["Enter a daily budget"]}},
    ],
)
