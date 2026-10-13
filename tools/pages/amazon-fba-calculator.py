PAGE = dict(
    slug="amazon-fba-calculator",
    cat="Platform fees",
    nav_name="Amazon FBA calculator",
    title="Amazon FBA Calculator 2026: Profit, Margin, ROI per Unit",
    desc="Free Amazon FBA profit calculator: referral fee, FBA fee, storage, inbound shipping and seller plan per unit, with margin, ROI and break-even price.",
    h1="Amazon FBA profit calculator",
    lead="Enter your selling price, the fees Amazon quotes for your item and what the unit costs you to make or buy. You get profit per unit, margin, return on your product cost and the lowest price that still breaks even.",
    form="""      <label for="price">Selling price</label>
      <div class="in"><span>$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="25"></div>
      <label for="fba">FBA fulfillment fee per unit <small>(depends on size and weight)</small></label>
      <div class="in"><span>$</span><input id="fba" type="number" inputmode="decimal" min="0" step="0.01" value="4.50"></div>
      <label for="stor">Monthly storage per unit <small>(average while it sits in the warehouse)</small></label>
      <div class="in"><span>$</span><input id="stor" type="number" inputmode="decimal" min="0" step="0.01" value="0.15"></div>
      <label for="inb">Inbound shipping to Amazon per unit</label>
      <div class="in"><span>$</span><input id="inb" type="number" inputmode="decimal" min="0" step="0.01" value="0.50"></div>
      <label for="cost">Product cost per unit</label>
      <div class="in"><span>$</span><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="6"></div>
      <label for="plan">Seller plan</label>
      <select id="plan" class="full"><option value="pro">Professional ($39.99/month)</option><option value="ind">Individual ($0.99 per item sold)</option></select>
      <label for="units">Units you sell per month <small>(spreads the Professional fee)</small></label>
      <div class="in"><input id="units" type="number" inputmode="numeric" min="1" step="1" value="100"></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="ref">Referral fee for your category <small>(8-17% typical, most are 15%)</small></label>
      <div class="in"><input id="ref" type="number" min="0" step="0.1" value="15"><span>%</span></div>
      <label for="refmin">Minimum referral fee per item</label>
      <div class="in"><span>$</span><input id="refmin" type="number" min="0" step="0.01" value="0.30"></div>
      <label for="pro">Professional plan per month</label>
      <div class="in"><span>$</span><input id="pro" type="number" min="0" step="0.01" value="39.99"></div>
      <label for="ind">Individual plan per item sold</label>
      <div class="in"><span>$</span><input id="ind" type="number" min="0" step="0.01" value="0.99"></div>
      </details>""",
    out="""<div class="big"><span>Profit per unit</span><b id="profit"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var P=n('price'),r=n('ref')/100,mn=n('refmin'),pro=$('plan').value==='pro',u=Math.max(1,Math.round(n('units')));
  var pl=pro?n('pro')/u:n('ind'),amz=n('fba')+n('stor')+pl,own=n('inb')+n('cost');
  var fixed=amz+own,be=r<1?fixed/(1-r):0;
  if(be*r<mn)be=fixed+mn;
  var beTxt=r<1?m(be):'not possible at this referral rate';
  if(!P){$('profit').textContent='-';setRows([['Enter a selling price to see your profit.',''],['Break-even price',beTxt]]);verdict(false,'No price entered yet. You need at least '+beTxt+' to cover these costs.');return}
  var ref=Math.max(P*r,mn),fees=ref+amz,profit=P-fees-own;
  setRows([['Selling price',m(P)],['Referral fee ('+n('ref')+'%, min '+m(mn)+')',m(-ref)],['FBA fulfillment',m(-n('fba'))],['Storage',m(-n('stor'))],
    [pro?'Professional plan ('+m(n('pro'))+' / '+u+' units)':'Individual plan per item',m(-pl)],['Total Amazon fees',m(-fees)+' ('+pc(fees/P)+')'],
    ['Inbound shipping',m(-n('inb'))],['Product cost',m(-n('cost'))],['Profit per unit',m(profit),'total'],['Margin',pc(profit/P)],
    ['ROI on product cost',n('cost')?pc(profit/n('cost')):'n/a'],['Break-even price',beTxt]]);
  if(n('ind'))$('rows').innerHTML+='<tr><td>Professional is cheaper above</td><td>'+Math.floor(n('pro')/n('ind'))+' units/month</td></tr>';
  $('profit').textContent=m(profit);
  if(profit<0)verdict(false,'Each sale loses '+m(-profit)+'. You need at least '+beTxt+' just to break even.');
  else verdict(profit/P>=0.2,'You make '+m(profit)+' a unit, a '+pc(profit/P)+' margin. '+(profit/P<0.2?'That is thin for FBA: returns, ads and long-term storage can wipe it out.':'There is room for returns and some ad spend.'));
}""",
    note="US Amazon rates as of October 2026: referral fee varies by category, 8-17% typical, most are 15%, with a $0.30 minimum per item. Professional plan $39.99/month, Individual $0.99 per item sold. FBA fulfillment and storage fees depend on your item's size, weight and the season, so copy them from Amazon's revenue calculator or your fee preview. Returns, ads, prep and long-term storage fees are not included.",
    body="""<h2>The fees on an FBA sale</h2>
<p><strong>Referral fee.</strong> Amazon's commission, a percentage of the selling price that depends on the category. Most categories are 15%, with a $0.30 minimum per item, which only bites on items under $2.</p>
<p><strong>FBA fulfillment fee.</strong> A fixed fee per unit for picking, packing and shipping, set by the item's size tier and shipping weight. It does not change with price, so it takes a much bigger share of cheap items.</p>
<p><strong>Storage.</strong> Charged monthly per cubic foot. Turn it into a per-unit figure by dividing your monthly storage bill by the units you sell that month. Slow sellers pay storage for many months.</p>
<p><strong>Your seller plan.</strong> Professional is $39.99 a month however much you sell. Individual has no monthly fee but charges $0.99 on every item. Professional is cheaper once you sell more than about 40 units a month.</p>
<h2>The formula</h2>
<p class="formula">Profit = price - referral fee - FBA fee - storage - plan share - inbound shipping - product cost</p>
<p>Example: a $25 item with a 15% referral fee ($3.75), a $4.50 FBA fee, $0.15 storage and the Professional plan spread over 100 units ($0.40). Amazon takes $8.80, or 35.2% of the price. Add $0.50 inbound shipping and a $6 product cost and you make <strong>$9.70</strong> a unit: a 38.8% margin and 161.7% ROI on product cost. The break-even price is $13.59.</p>
<p>On the Individual plan the same unit pays $0.99 instead of $0.40 and profit drops to $9.11.</p>
<h2>Margin vs ROI</h2>
<p>Margin tells you how much of each sale you keep. ROI tells you how hard your inventory money works: $6 spent on stock that returns $9.70 of profit is a 161.7% return per cycle. Wholesale and arbitrage sellers often screen products by ROI; private label sellers tend to watch margin because ad spend comes out of it.</p>""",
    faqs=[
        ("How much does Amazon take from a $25 sale with FBA?", "With a 15% referral fee, a $4.50 FBA fee, $0.15 storage and the Professional plan spread over 100 units, $8.80, or 35.2% of the price. Your FBA fee depends on size and weight."),
        ("What is the Amazon referral fee minimum?", "$0.30 per item in most categories. On a $1.50 item, 15% comes to less than that, so Amazon charges $0.30 instead."),
        ("How do I find my break-even price on Amazon?", "Add up every fixed cost per unit (FBA fee, storage, plan share, inbound shipping and product cost) and divide by 1 minus the referral rate. For the example on this page that is $13.59."),
        ("Should I use the Individual or Professional plan?", "Individual costs $0.99 per item; Professional costs $39.99 a month. At 100 units a month Professional works out to $0.40 a unit, so it is cheaper above about 40 sales a month."),
    ],
    related=["ebay-fee-calculator", "etsy-vs-amazon-handmade", "profit-margin-calculator", "break-even-calculator", "cogs-calculator", "roas-calculator"],
    og_image="pins/pin-04.png",
    tests=[
        {"expect": {"rows": ["$25.00", "-$3.75", "-$4.50", "-$0.15", "-$0.40", "-$8.80", "35.2%", "-$0.50", "-$6.00", "38.8%", "161.7%", "$13.59", "40 units/month"], "profit": "$9.70"}},
        {"set": {"plan": "ind"}, "expect": {"rows": "-$0.99", "profit": "$9.11"}},
        {"set": {"price": "1.5"}, "expect": {"rows": ["-$0.30", "-$10.35"], "verdict": "loses"}},
        {"set": {"price": ""}, "expect": {"profit": "-", "verdict": "$13.59"}},
        {"set": {"units": "0", "cost": "0"}, "expect": {"rows": "n/a"}},
    ],
)
