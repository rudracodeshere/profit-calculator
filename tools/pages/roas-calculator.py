PAGE = dict(
    slug="roas-calculator",
    cat="Pricing & margins",
    nav_name="ROAS calculator",
    title="ROAS Calculator: Break-Even ROAS, Target ROAS and CPA",
    desc="Free ROAS calculator for online sellers. See your return on ad spend, the break-even ROAS for your margin, the ROAS you need for a profit target, and max CPA.",
    h1="ROAS calculator: is your ad spend making money?",
    lead="Enter what you spent on ads and the sales they brought in. You get your ROAS, the ROAS where ads stop losing money for your margin, the ROAS you need for a profit target, and the most you can pay to get one order.",
    form="""      <label for="spend">Ad spend</label>
      <div class="in"><span>$</span><input id="spend" type="number" inputmode="decimal" min="0" step="1" value="500"></div>
      <label for="rev">Revenue from those ads</label>
      <div class="in"><span>$</span><input id="rev" type="number" inputmode="decimal" min="0" step="1" value="2000"></div>
      <label for="orders">Orders from those ads</label>
      <div class="in"><input id="orders" type="number" inputmode="numeric" min="0" step="1" value="40"></div>
      <label for="mg">Margin before ads <small>(after product cost, fees and shipping)</small></label>
      <div class="in"><input id="mg" type="number" inputmode="decimal" min="0" max="100" step="1" value="40"><span>%</span></div>
      <label for="tp">Profit you want to keep after ads <small>(% of revenue)</small></label>
      <div class="in"><input id="tp" type="number" inputmode="decimal" min="0" max="100" step="1" value="10"><span>%</span></div>""",
    out="""<div class="big"><span>Your ROAS</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function x(v){return v.toFixed(2)+'x'}
function calc(){
  var s=n('spend'),r=n('rev'),o=Math.round(n('orders')),g=n('mg')/100,t=n('tp')/100;
  var be=g>0?x(1/g):'none (no margin)',tr=g>t?x(1/(g-t)):'not reachable';
  var aov=o?r/o:0,rows=[];
  if(!s){$('big').textContent='-';setRows([['Break-even ROAS',be],['Target ROAS for '+pc(t,0)+' profit',tr]]);verdict(false,'Enter your ad spend to see your ROAS. The break-even ROAS above already applies to any campaign at this margin.');return}
  var roas=r/s,profit=r*g-s;
  $('big').textContent=x(roas);
  rows.push(['ROAS (revenue / spend)',x(roas)+' ('+pc(roas,0)+')'],['ACoS (spend / revenue)',r?pc(s/r):'n/a'],['Break-even ROAS',be],['Target ROAS for '+pc(t,0)+' profit',tr],['Margin kept before ads',m(r*g)],['Profit after ads',m(profit),'total']);
  if(r)rows.push(['Profit after ads as % of revenue',pc(profit/r)]);
  if(o){rows.push(['Cost per order (CPA)',m(s/o)],['Average order value',m(aov)],['Break-even CPA',m(aov*g)]);if(g>t)rows.push(['Target CPA',m(aov*(g-t))])}
  setRows(rows);
  if(!g)verdict(false,'With no margin before ads, any ad spend is a loss. Fix the price or costs first.');
  else if(profit<0)verdict(false,'These ads lose '+m(-profit)+'. At a '+pc(g,0)+' margin you need at least '+be+' ROAS; you are at '+x(roas)+'.');
  else if(g>t&&roas<1/(g-t))verdict(false,'Profitable by '+m(profit)+', but below your '+tr+' target. Cut the weakest ads or raise prices before scaling.');
  else verdict(true,'These ads make '+m(profit)+' after spend. ROAS '+x(roas)+' is above your '+be+' break-even, so there is room to scale carefully.');
}""",
    note="ROAS here uses the revenue the ad platform attributes to the ads. Meta, Google, Pinterest and Etsy each use their own attribution window, so check against your own sales data. Margin before ads should already include marketplace fees (Etsy US 9.5% + $0.25 as of October 2026, Shopify Payments 2.9% + $0.30 on Basic) and any free-shipping cost.",
    body="""<h2>What ROAS tells you, and what it doesn't</h2>
<p>ROAS (return on ad spend) is the revenue an ad brought in divided by what the ad cost. $2,000 of sales from $500 of ads is a 4.00x ROAS, sometimes written as 400%. It measures revenue, not profit. Whether 4.00x is good depends entirely on how much of that revenue you keep before ads.</p>
<h2>Break-even ROAS</h2>
<p>Your margin before ads is what's left of each sale after the product cost, marketplace and payment fees, and any shipping you cover. Ads have to be paid out of that. If you keep 40% of revenue, each $1 of ad spend needs $2.50 of sales just to pay for itself.</p>
<p class="formula">Break-even ROAS = 1 / margin before ads &nbsp;|&nbsp; Target ROAS = 1 / (margin - target profit %)</p>
<p>At a 40% margin, break-even ROAS is <strong>2.50x</strong>. If you also want to keep 10% of revenue as profit, you need 1 / 0.30 = <strong>3.33x</strong>. A product with a 25% margin needs 4.00x just to break even, which is why low-margin products are hard to advertise.</p>
<h2>Worked example</h2>
<p>A shop spends $500 on Meta ads and Ads Manager reports 40 purchases worth $2,000. ROAS is 4.00x and the cost per order is <strong>$12.50</strong>. With a 40% margin, the shop keeps $800.00 before ads and <strong>$300.00</strong> after, 15.0% of the ad revenue. The average order is $50.00, so the break-even CPA is $20.00 and the CPA that leaves 10% profit is $15.00.</p>
<h2>Where to find the numbers on each platform</h2>
<p><strong>Meta Ads:</strong> the "Purchase ROAS" and "Cost per purchase" columns in Ads Manager, once your pixel or Shopify connection reports purchases. <strong>Google Ads:</strong> "Conv. value / cost" is ROAS, and "Cost / conv." is CPA. <strong>Pinterest Ads:</strong> conversion reporting shows ROAS and cost per action when the Pinterest tag tracks checkouts. <strong>Etsy Ads:</strong> the Etsy Ads dashboard shows spend, revenue and ROAS for ads shown on Etsy. Etsy Offsite Ads are different: you pay a 15% or 12% fee only when a sale happens, so there is no spend to enter here.</p>
<p>Amazon Sponsored Products reports ACoS instead, which is spend divided by sales: the inverse of ROAS. A 25.0% ACoS equals a 4.00x ROAS.</p>""",
    faqs=[
        ("What is a good ROAS for an online store?", "Any ROAS above your break-even, which is 1 divided by your margin before ads. At a 40% margin that is 2.50x; at a 25% margin it is 4.00x. A ROAS that is great for one shop can lose money for another."),
        ("Is a 2x ROAS profitable?", "Only if you keep more than 50% of revenue before ads. At a 40% margin, $500 of ads that bring in $1,000 lose $100.00."),
        ("How do I calculate break-even CPA?", "Multiply your average order value by your margin before ads. A $50.00 average order at a 40% margin gives a break-even CPA of $20.00."),
        ("What's the difference between ROAS and ACoS?", "ROAS is revenue divided by ad spend; ACoS, used by Amazon, is ad spend divided by revenue. They are inverses: 4.00x ROAS is 25.0% ACoS."),
    ],
    related=["etsy-ads-calculator", "etsy-offsite-ads-calculator", "profit-margin-calculator", "break-even-calculator", "price-increase-calculator"],
    og_image="pins/pin-08.png",
    tests=[
        {"expect": {"big": "4.00x", "rows": ["400%", "25.0%", "$800.00", "2.50x", "3.33x", "$300.00", "15.0%", "$12.50", "$50.00", "$20.00", "$15.00"], "verdict": "make $300.00"}},
        {"set": {"rev": "1000"}, "expect": {"big": "2.00x", "rows": "-$100.00", "verdict": "lose $100.00"}},
        {"set": {"mg": "25"}, "expect": {"rows": "4.00x"}},
        {"set": {"rev": "1500"}, "expect": {"big": "3.00x", "verdict": "below your 3.33x target"}},
        {"set": {"spend": "0"}, "expect": {"big": "-", "verdict": "Enter your ad spend", "rows": "2.50x"}},
        {"set": {"mg": "0", "orders": "0"}, "expect": {"rows": ["none", "not reachable"], "verdict": "no margin"}},
    ],
)
