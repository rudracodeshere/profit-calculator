PAGE = dict(
    slug="profit-margin-calculator",
    cat="Pricing & margins",
    nav_name="Profit margin calculator",
    title="Profit Margin Calculator: Margin, Markup and Price From Cost",
    desc="Free profit margin calculator for online sellers. Get gross profit, margin and markup from cost and price, the price for a target margin, or your max cost.",
    h1="Profit margin calculator",
    lead="Pick what you know. Enter cost and price to get your margin and markup, enter a cost and a target margin to get the price to charge, or enter a price and a margin to find the most you can pay for the product.",
    form="""      <label for="mode">What do you want to find?</label>
      <select id="mode" class="full">
        <option value="a">Margin and markup (I know cost and price)</option>
        <option value="b">Price to charge (I know cost and target margin)</option>
        <option value="c">Maximum cost (I know price and target margin)</option>
      </select>
      <div id="fCost">
      <label for="cost">Cost per unit <small>(product, materials, packaging)</small></label>
      <div class="in"><span>$</span><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="12"></div>
      </div>
      <div id="fPrice">
      <label for="price">Selling price</label>
      <div class="in"><span>$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="30"></div>
      </div>
      <div id="fMargin">
      <label for="margin">Target gross margin</label>
      <div class="in"><input id="margin" type="number" inputmode="decimal" min="0" max="99" step="1" value="40"><span>%</span></div>
      </div>
      <div id="fFees">
      <label for="fees">Platform fees per sale <small>(optional, for net margin)</small></label>
      <div class="in"><span>$</span><input id="fees" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
      </div>""",
    out="""<div class="big"><span id="bigLabel">Gross margin</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function show(id,on){$(id).style.display=on?'':'none'}
function calc(){
  var mode=$('mode').value,c=n('cost'),p=n('price'),g=n('margin')/100,f=n('fees');
  show('fCost',mode!=='c');show('fPrice',mode!=='b');show('fMargin',mode!=='a');show('fFees',mode==='a');
  if(mode==='a'){
    $('bigLabel').textContent='Gross margin';
    if(!p){$('big').textContent='-';setRows([]);verdict(false,'Enter a selling price to see your margin.');return}
    var gp=p-c,net=p-c-f;
    $('big').textContent=pc(gp/p);
    var r=[['Selling price',m(p)],['Cost per unit',m(-c)],['Gross profit',m(gp),'total'],['Gross margin',pc(gp/p)],['Markup on cost',c?pc(gp/c):'n/a (cost is $0)']];
    if(f)r.push(['Platform fees',m(-f)],['Net profit after fees',m(net),'total'],['Net margin',pc(net/p)]);
    setRows(r);
    if(net<0)verdict(false,'You lose '+m(-net)+' on every sale. Raise the price or cut the cost.');
    else if(!f)verdict(gp/p>=0.4,'Gross margin is '+pc(gp/p)+'. Fees, shipping and ads still come out of the '+m(gp)+'; enter your fees to see net margin.');
    else verdict(net/p>=0.2,'After fees you keep '+m(net)+' per sale, a '+pc(net/p)+' net margin.'+(net/p<0.2?' That leaves little room for ads or discounts.':''));
  }else if(mode==='b'){
    $('bigLabel').textContent='Price to charge';
    if(g>=1){$('big').textContent='-';setRows([]);verdict(false,'A margin must be under 100%. A 100% margin would mean the product cost nothing.');return}
    if(!c){$('big').textContent='-';setRows([]);verdict(false,'Enter your cost per unit to get a price.');return}
    var pr=c/(1-g);
    $('big').textContent=m(pr);
    setRows([['Cost per unit',m(c)],['Target gross margin',pc(g)],['Price to charge',m(pr),'total'],['Gross profit per unit',m(pr-c)],['Markup on cost',pc((pr-c)/c)]]);
    verdict(true,'Charge '+m(pr)+' to keep '+pc(g)+' of the price. Adding '+pc(g,0)+' to the cost would only give '+m(c*(1+g))+', a '+pc(g/(1+g))+' margin.');
  }else{
    $('bigLabel').textContent='Maximum cost per unit';
    if(g>=1){$('big').textContent='-';setRows([]);verdict(false,'A margin must be under 100%.');return}
    if(!p){$('big').textContent='-';setRows([]);verdict(false,'Enter your selling price to get a maximum cost.');return}
    var mc=p*(1-g);
    $('big').textContent=m(mc);
    setRows([['Selling price',m(p)],['Target gross margin',pc(g)],['Maximum cost per unit',m(mc),'total'],['Gross profit per unit',m(p-mc)]]);
    verdict(true,'Keep your landed cost at or below '+m(mc)+' per unit. Every dollar above that comes straight out of your '+pc(g,0)+' margin.');
  }
}""",
    note="Gross margin = (price - cost) / price. Markup = (price - cost) / cost. Enter Etsy, Shopify, Amazon or eBay fees in dollars to see net margin; the fee calculators linked below give you that number. The Etsy example uses US rates as of October 2026 (6.5% transaction, 3% + $0.25 processing, $0.20 listing). Nothing leaves your browser.",
    body="""<h2>Margin vs markup</h2>
<p>Both compare the same profit to a different base. <strong>Margin</strong> divides profit by the selling price. <strong>Markup</strong> divides profit by the cost. A product that costs $12 and sells for $30 makes $18 of gross profit. That is a 60% margin ($18 / $30) and a 150% markup ($18 / $12).</p>
<p>Margin can never reach 100%, because that would mean the item cost nothing. Markup has no ceiling. If a supplier or a pricing guide gives you a percentage, check which one it means before you use it.</p>
<h2>The formulas</h2>
<p class="formula">Margin = (price - cost) / price &nbsp;|&nbsp; Price for a target margin = cost / (1 - margin) &nbsp;|&nbsp; Max cost = price x (1 - margin)</p>
<p>Example: your cost is $12 and you want a 40% margin. The price is $12 / 0.60 = <strong>$20.00</strong>. Turned around, if the market price for a similar item is $30 and you need 40%, the most you can pay to make or buy it is $30 x 0.60 = <strong>$18.00</strong>.</p>
<p>A common mistake is to add the margin to the cost. $12 plus 40% is $16.80, which is only a 28.6% margin.</p>
<h2>Gross margin vs net margin for sellers</h2>
<p><strong>Gross margin</strong> only subtracts what the product costs you: materials, the wholesale price, packaging, inbound freight. <strong>Net margin</strong> also subtracts the costs of selling it. For an online seller the biggest of those is usually the marketplace or payment fee.</p>
<p>Take the $30 item that costs $12 again, sold on Etsy with free shipping. Etsy's US fees on $30 are $1.95 (6.5% transaction), $1.15 (3% + $0.25 processing) and $0.20 (listing), so $3.30 in total. Gross margin is 60%, but after fees you keep $14.70, a <strong>49.0%</strong> net margin. Shipping labels you pay, ads and returns pull it lower still.</p>
<p>Use gross margin to compare products and suppliers. Use net margin to decide whether a product is worth selling at all. A per-product net margin needs your full sales export, because fees, discounts and ad costs differ from order to order.</p>""",
    faqs=[
        ("How do I calculate a 40% profit margin?", "Divide the cost by 0.60 (that is, 1 minus 0.40). A $12 cost needs a $20.00 price. Check: $8 profit / $20 = 40%."),
        ("Is a 50% margin the same as a 100% markup?", "Yes. An item that costs $10 and sells for $20 has a 100% markup and a 50% margin. Both describe the same $10 of profit."),
        ("What is the difference between gross and net profit margin?", "Gross margin subtracts only the product cost. Net margin also subtracts fees and other selling costs. A $30 Etsy sale with a $12 cost has a 60% gross margin but a 49.0% net margin after $3.30 of Etsy fees."),
        ("Why can't my margin be over 100%?", "Margin is profit as a share of the price, and profit can't be larger than the price unless the cost is negative. If you see a number over 100%, it is a markup, not a margin."),
    ],
    related=["markup-calculator", "break-even-calculator", "cogs-calculator", "price-increase-calculator", "etsy-fee-calculator", "etsy-profit-calculator"],
    og_image="pins/pin-05.png",
    tests=[
        {"expect": {"big": "60.0%", "rows": ["$18.00", "60.0%", "150.0%"]}},
        {"set": {"fees": "3.30"}, "expect": {"rows": ["-$3.30", "$14.70", "49.0%"]}},
        {"set": {"mode": "b"}, "expect": {"big": "$20.00", "rows": ["$8.00", "66.7%"], "verdict": ["$16.80", "28.6%"]}},
        {"set": {"mode": "c"}, "expect": {"big": "$18.00", "rows": ["$12.00"]}},
        {"set": {"cost": "10", "price": "20"}, "expect": {"big": "50.0%", "rows": ["100.0%"]}},
        {"set": {"price": "0"}, "expect": {"big": "-", "verdict": "Enter a selling price"}},
        {"set": {"mode": "b", "margin": "100"}, "expect": {"verdict": "under 100%"}},
    ],
)
