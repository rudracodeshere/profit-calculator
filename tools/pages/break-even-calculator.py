PAGE = dict(
    slug="break-even-calculator",
    cat="Pricing & margins",
    nav_name="Break-even calculator",
    title="Break-Even Calculator for Online Sellers: Units and Revenue",
    desc="Free break-even calculator for online shops. Enter monthly fixed costs, price, unit cost and fees to see sales needed to break even or hit a profit goal.",
    h1="Break-even calculator for online sellers",
    lead="Enter what your shop costs to run each month and what one sale earns after product costs and fees. You get the number of sales you need to cover your costs, the sales needed for a profit goal, and what a 10% price rise would change.",
    form="""      <label for="fixed">Monthly fixed costs <small>(subscriptions, software, rent, tools)</small></label>
      <div class="in"><span>$</span><input id="fixed" type="number" inputmode="decimal" min="0" step="1" value="300"></div>
      <label for="price">Price per unit <small>(what the buyer pays)</small></label>
      <div class="in"><span>$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="24"></div>
      <label for="vc">Variable cost per unit <small>(materials, packaging, label you pay)</small></label>
      <div class="in"><span>$</span><input id="vc" type="number" inputmode="decimal" min="0" step="0.01" value="8"></div>
      <label for="goal">Monthly profit goal</label>
      <div class="in"><span>$</span><input id="goal" type="number" inputmode="decimal" min="0" step="10" value="1000"></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="feep">Fees as % of price <small>(Etsy US: 6.5% + 3% = 9.5%)</small></label>
      <div class="in"><input id="feep" type="number" min="0" step="0.1" value="9.5"><span>%</span></div>
      <label for="feef">Fixed fee per sale <small>(Etsy US: $0.25 + $0.20 listing)</small></label>
      <div class="in"><span>$</span><input id="feef" type="number" min="0" step="0.01" value="0.45"></div>
      </details>""",
    out="""<div class="big"><span>Sales to break even each month</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function units(x){return Math.ceil(x-1e-9)}
function calc(){
  var F=n('fixed'),p=n('price'),v=n('vc'),G=n('goal'),fp=n('feep')/100,ff=n('feef');
  var fee=p*fp+ff,cm=p-v-fee;
  if(!p){$('big').textContent='-';setRows([]);verdict(false,'Enter a price per unit to see your break-even point.');return}
  if(cm<=0){$('big').textContent='Never';setRows([['Price',m(p)],['Variable cost + fees',m(-(v+fee))],['Left per sale',m(cm),'total']]);verdict(false,'Each sale loses '+m(-cm)+' before fixed costs, so no number of sales breaks even. Raise the price or cut the unit cost first.');return}
  var be=units(F/cm),tg=units((F+G)/cm);
  var p2=p*1.1,cm2=p2-v-(p2*fp+ff),be2=units(F/cm2),tg2=units((F+G)/cm2);
  $('big').textContent=be+' units';
  setRows([['Price',m(p)],['Variable cost',m(-v)],['Fees per unit',m(-fee)],['Contribution per unit',m(cm),'total'],['Contribution margin',pc(cm/p)],
    ['Break-even units / month',be],['Break-even revenue / month',m(be*p)],
    ['Units for '+m(G)+' profit',tg],['Revenue for '+m(G)+' profit',m(tg*p)],
    ['At '+m(p2)+' (+10%): contribution',m(cm2)],['At +10%: break-even units',be2],['At +10%: units for '+m(G)+' profit',tg2]]);
  verdict(true,'You need '+be+' sales a month to cover '+m(F)+' of fixed costs, and '+tg+' to make '+m(G)+'. A 10% price rise cuts that to '+tg2+', so you could lose '+(tg-tg2)+' sales and still hit the goal.');
}""",
    note="Fee defaults are Etsy US as of October 2026 (6.5% transaction + 3% processing on the price, $0.25 processing + $0.20 listing per sale). For Shopify Basic use 2.9% and $0.30; for eBay about 13.6% and $0.40. Shipping you charge separately is left out; if you offer free shipping, put the label in variable cost. Units are rounded up to whole sales.",
    body="""<h2>How break-even works</h2>
<p>Every sale leaves some money after paying for the product itself and the fees on that sale. That leftover is the <strong>contribution per unit</strong>. Your fixed costs, the ones you pay whether you sell anything or not, have to be covered by those contributions. Break-even is the point where they are.</p>
<p class="formula">Break-even units = fixed costs / (price - variable cost - fees per unit)</p>
<p>Fixed costs for an online seller are things like a Shopify plan, Etsy Plus, email software, design apps, a workspace or a monthly ad budget you have committed to. Variable costs rise with each sale: materials, packaging, the shipping label if you offer free shipping, and marketplace fees.</p>
<h2>Worked example</h2>
<p>You sell a $24 item that costs $8 to make and ship. Etsy's US fees on it are 9.5% of $24 ($2.28) plus $0.45, so <strong>$2.73</strong>. Each sale contributes $24 - $8 - $2.73 = <strong>$13.27</strong> toward fixed costs.</p>
<p>With $300 a month of fixed costs, you need 300 / 13.27 = 22.6 sales, so <strong>23 sales</strong> and <strong>$552.00</strong> of revenue to break even. To make $1,000 on top, you need (300 + 1,000) / 13.27 = 97.97, so <strong>98 sales</strong>, or $2,352.00 of revenue.</p>
<h2>What a 10% price rise does</h2>
<p>Raise the price to $26.40 and the contribution goes to <strong>$15.44</strong>, because nearly all of the extra $2.40 is profit (only the 9.5% fee comes out of it). Break-even falls to 20 sales and the $1,000 goal falls to 85 sales. That is 13 fewer sales for the same profit, which is why a small price change often matters more than a big push for volume. The <a href="../price-increase-calculator/">price increase calculator</a> shows how many sales you could lose before a rise stops paying off.</p>
<p>A whole-shop break-even hides which products carry the rest. For a per-product view you need your full sales export with each item's own cost and fees.</p>""",
    faqs=[
        ("How do I calculate break-even for a small business?", "Add up your monthly fixed costs and divide by what each sale leaves after its own costs and fees. $300 of fixed costs and $13.27 per sale gives 22.6, so 23 sales a month."),
        ("Should I include marketplace fees in break-even?", "Yes, as a variable cost per unit. Percentage fees grow with the price, so a $24 Etsy sale at 9.5% plus $0.45 carries $2.73 of fees. Monthly plan fees like Shopify or Etsy Plus go in fixed costs instead."),
        ("Should I pay myself before break-even?", "If you want the business to pay you, put your target pay in the profit goal, or add a salary to fixed costs. Break-even with no pay only means the shop isn't losing cash."),
        ("Does raising prices lower break-even?", "Yes, often a lot. In the example a 10% rise from $24 to $26.40 lifts contribution from $13.27 to $15.44 and cuts break-even from 23 sales to 20."),
    ],
    related=["price-increase-calculator", "profit-margin-calculator", "cogs-calculator", "roas-calculator", "etsy-vs-shopify", "handmade-pricing-calculator"],
    og_image="pins/pin-07.png",
    tests=[
        {"expect": {"big": "23 units", "rows": ["-$2.73", "$13.27", "55.3%", "$552.00", "98", "$2,352.00", "$26.40", "$15.44", "20", "85"], "verdict": ["23 sales", "98", "lose 13 sales"]}},
        {"set": {"price": "0"}, "expect": {"big": "-", "verdict": "Enter a price"}},
        {"set": {"price": "8"}, "expect": {"big": "Never", "verdict": "no number of sales"}},
        {"set": {"fixed": "0", "goal": "0"}, "expect": {"big": "0 units"}},
        {"set": {"feep": "2.9", "feef": "0.30"}, "expect": {"rows": ["-$1.00", "$15.00"], "big": "20 units"}},
    ],
)
