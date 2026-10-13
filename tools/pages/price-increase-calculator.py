PAGE = dict(
    slug="price-increase-calculator",
    cat="Pricing & margins",
    nav_name="Price increase calculator",
    title="Price Increase Calculator: How Many Sales Can You Lose?",
    desc="Free price increase calculator. See how many sales you can lose after raising prices and still earn the same, or how many more a discount needs.",
    h1="Price increase calculator: how many sales can you afford to lose?",
    lead="Thinking about raising your price, or cutting it? Enter your current price, costs and monthly sales, then the new price. You get the profit change at the same volume and the exact drop in sales that would wipe it out, or the extra sales a lower price has to bring in.",
    form="""      <label for="cur">Current price</label>
      <div class="in"><span>$</span><input id="cur" type="number" inputmode="decimal" min="0" step="0.01" value="20"></div>
      <label for="cost">Cost per unit <small>(product, packaging, label you pay)</small></label>
      <div class="in"><span>$</span><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="8"></div>
      <label for="units">Units sold per month at the current price</label>
      <div class="in"><input id="units" type="number" inputmode="numeric" min="0" step="1" value="100"></div>
      <label for="np">New price you're considering</label>
      <div class="in"><span>$</span><input id="np" type="number" inputmode="decimal" min="0" step="0.01" value="23"></div>
      <details><summary class="note">Edit fee rate</summary>
      <label for="fee">Marketplace + payment fees <small>(% of price)</small></label>
      <div class="in"><input id="fee" type="number" min="0" step="0.1" value="10"><span>%</span></div>
      </details>""",
    out="""<div class="big"><span id="bigLabel">Sales you can lose and still earn the same</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var p0=n('cur'),c=n('cost'),f=n('fee')/100,u=Math.round(n('units')),p1=n('np');
  var c0=p0-c-p0*f,c1=p1-c-p1*f,up=p1>=p0;
  $('bigLabel').textContent=up?'Sales you can lose and still earn the same':'Extra sales you need to earn the same';
  if(!p0||!p1){$('big').textContent='-';setRows([]);verdict(false,'Enter both the current price and the new price.');return}
  var r=[['Profit per sale now',m(c0)],['Profit per sale at '+m(p1),m(c1)]];
  if(c1<=0){$('big').textContent='-';setRows(r);verdict(false,'At '+m(p1)+' every sale loses '+m(-c1)+' after cost and fees. No amount of volume makes that up.');return}
  if(c0<=0){$('big').textContent='-';setRows(r);verdict(true,'At '+m(p0)+' you lose '+m(-c0)+' per sale, so any volume at '+m(p1)+' beats it. Raise the price.');return}
  if(p1===p0){$('big').textContent='0';setRows(r);verdict(true,'Same price, same profit. Enter a different new price.');return}
  var need=c0/c1,pct=up?1-need:need-1;
  if(u){
    var nu=Math.ceil(u*need-1e-9),d=up?u-nu:nu-u,P0=u*c0,P1=u*c1;
    $('big').textContent=d+' a month ('+pc(pct)+')';
    r.push(['Monthly profit now ('+u+' sales)',m(P0)],['Monthly profit at '+m(p1)+', same '+u+' sales',m(P1)],['Change at same volume',(P1>=P0?'+':'')+m(P1-P0),'total'],['Sales needed for the same profit',nu+' a month']);
    setRows(r);
    if(up)verdict(true,'Raising to '+m(p1)+' adds '+m(P1-P0)+' a month if sales hold. It only stops paying if you lose more than '+d+' of your '+u+' monthly sales.');
    else verdict(false,'Dropping to '+m(p1)+' costs '+m(P0-P1)+' a month unless it brings at least '+d+' extra sales ('+pc(pct)+' more) every month.');
  }else{
    $('big').textContent=pc(pct);
    setRows(r);
    verdict(up,up?'You can lose up to '+pc(pct)+' of your sales at '+m(p1)+' and still earn the same. Enter monthly units for counts.':'You need '+pc(pct)+' more sales at '+m(p1)+' to earn the same. Enter monthly units for counts.');
  }
}""",
    note="Fees default to 10% of the price as a round figure; Etsy US is 9.5% plus $0.45 per order, Shopify Basic 2.9% + $0.30 and eBay 13.6% + $0.40 for most categories, as of October 2026. Edit the rate to match your platform. Sales needed are rounded up to whole sales.",
    body="""<h2>Why a price rise can survive lost sales</h2>
<p>When you raise a price, your costs stay the same, so almost all of the increase is extra profit. A product that sells for $20, costs $8 and pays 10% in fees leaves you <strong>$10.00</strong> per sale. At $23 it leaves <strong>$12.70</strong>. The price went up 15%, but the profit per sale went up 27%.</p>
<p>That gap is your cushion. You can sell fewer units and still take home the same amount.</p>
<p class="formula">Sales you can lose = 1 - (profit per sale now / profit per sale at new price)</p>
<h2>Worked example: raising $20 to $23</h2>
<p>You sell 100 a month and make <strong>$1,000.00</strong>. If sales hold at $23, you make <strong>$1,270.00</strong>, $270.00 more. To make the same $1,000 at $23 you only need 1,000 / 12.70 = 78.7 sales, so 79. You could lose <strong>21 of your 100 sales</strong>, or 21.3%, before the increase costs you anything.</p>
<h2>Worked example: cutting $20 to $18</h2>
<p>Discounts work the other way. At $18 you keep $8.20 per sale. At 100 sales that is $820.00, $180.00 less than now. To get back to $1,000 you need 1,000 / 8.20 = 122 sales, <strong>22 extra a month</strong> or 22.0% more, for a 10% price cut. Check the <a href="../etsy-sale-calculator/">Etsy sale calculator</a> before you run a discount.</p>
<h2>How to test a price change</h2>
<p>Change the price on one or two of your steady sellers rather than the whole shop, and leave it for at least a few weeks so normal ups and downs even out. Compare profit, not revenue or order count. A rise that loses fewer sales than this calculator allows has paid off, even if your order count looks worse.</p>
<p>The cushion is biggest on low-margin products, because a few dollars more is a large share of a small profit. Those are also the products where a per-product view from your full sales export is most useful.</p>""",
    faqs=[
        ("How many customers can I lose if I raise prices?", "Divide your profit per sale now by your profit per sale at the new price, and subtract from 1. Going from $10.00 to $12.70 per sale means you can lose 21.3% of sales, about 21 of 100, and earn the same."),
        ("How much more do I need to sell after a price cut?", "Divide current profit per sale by the new profit per sale. Cutting a $20 price to $18 drops profit from $10.00 to $8.20 per sale, so you need 22.0% more sales just to stand still."),
        ("Should I raise prices on Etsy?", "Run the numbers for your listing first. Because Etsy's fees are mostly a percentage of the price, a rise keeps about 90% of the extra money. If you would lose fewer sales than the calculator allows, the rise pays."),
        ("Does a price increase change my fees?", "Yes, percentage fees rise with the price. This calculator includes that: at 10% fees, a $3 rise adds $2.70 of profit per sale, not $3."),
    ],
    related=["break-even-calculator", "profit-margin-calculator", "etsy-sale-calculator", "etsy-pricing-calculator", "roas-calculator", "markup-calculator"],
    og_image="pins/pin-10.png",
    tests=[
        {"expect": {"big": ["21 a month", "21.3%"], "rows": ["$10.00", "$12.70", "$1,000.00", "$1,270.00", "+$270.00", "79 a month"], "verdict": "21 of your 100"}},
        {"set": {"np": "18"}, "expect": {"big": ["22 a month", "22.0%"], "rows": ["$8.20", "$820.00", "-$180.00", "122 a month"]}},
        {"set": {"units": "0"}, "expect": {"big": "21.3%"}},
        {"set": {"np": "8"}, "expect": {"big": "-", "verdict": "No amount of volume"}},
        {"set": {"np": "0"}, "expect": {"big": "-", "verdict": "Enter both"}},
        {"set": {"cur": "8.50"}, "expect": {"verdict": "any volume"}},
    ],
)
