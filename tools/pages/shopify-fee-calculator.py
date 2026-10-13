PAGE = dict(
    slug="shopify-fee-calculator",
    cat="Platform fees",
    nav_name="Shopify fee calculator",
    title="Shopify Fee Calculator 2026: Card Fees, Plans and Break-Even",
    desc="Free Shopify fee calculator. See card fees per order, your monthly cost as a % of sales, and the sales level where Grow or Advanced becomes cheaper.",
    h1="Shopify fee calculator",
    lead="Pick your plan and payment setup, then enter a typical order and how many orders you get a month. You get the fee on each order, what Shopify costs you per month as a share of sales, and the exact monthly sales where a bigger plan starts saving money.",
    form="""      <label for="plan">Your Shopify plan</label>
      <select id="plan" class="full"><option value="0">Basic</option><option value="1">Grow</option><option value="2">Advanced</option></select>
      <label for="bill">Billing</label>
      <select id="bill" class="full"><option value="m">Monthly</option><option value="y">Yearly (lower monthly price)</option></select>
      <label for="ch">Sales channel</label>
      <select id="ch" class="full"><option value="on">Online store</option><option value="in">In person (Shopify POS)</option></select>
      <label for="gw">Payment gateway <small>(online only)</small></label>
      <select id="gw" class="full"><option value="sp">Shopify Payments</option><option value="tp">Third-party gateway (PayPal, Stripe, etc.)</option></select>
      <label for="avg">Average order value</label>
      <div class="in"><span>$</span><input id="avg" type="number" inputmode="decimal" min="0" step="0.01" value="50"></div>
      <label for="orders">Orders per month</label>
      <div class="in"><input id="orders" type="number" inputmode="numeric" min="0" step="1" value="300"></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="mo0">Plan price, monthly billing <small>(Basic / Grow / Advanced)</small></label>
      <div class="in"><span>$</span><input id="mo0" type="number" min="0" step="1" value="39"><span>$</span><input id="mo1" type="number" min="0" step="1" value="105"><span>$</span><input id="mo2" type="number" min="0" step="1" value="399"></div>
      <label for="yr0">Plan price per month, yearly billing</label>
      <div class="in"><span>$</span><input id="yr0" type="number" min="0" step="1" value="29"><span>$</span><input id="yr1" type="number" min="0" step="1" value="79"><span>$</span><input id="yr2" type="number" min="0" step="1" value="299"></div>
      <label for="on0">Online card rate, Shopify Payments <small>(%)</small></label>
      <div class="in"><input id="on0" type="number" min="0" step="0.1" value="2.9"><span>%</span><input id="on1" type="number" min="0" step="0.1" value="2.7"><span>%</span><input id="on2" type="number" min="0" step="0.1" value="2.5"><span>%</span></div>
      <label for="onf">Online fixed fee per order</label>
      <div class="in"><span>$</span><input id="onf" type="number" min="0" step="0.01" value="0.30"></div>
      <label for="in0">In-person card rate <small>(%)</small></label>
      <div class="in"><input id="in0" type="number" min="0" step="0.1" value="2.6"><span>%</span><input id="in1" type="number" min="0" step="0.1" value="2.5"><span>%</span><input id="in2" type="number" min="0" step="0.1" value="2.4"><span>%</span></div>
      <label for="inf">In-person fixed fee per order</label>
      <div class="in"><span>$</span><input id="inf" type="number" min="0" step="0.01" value="0.10"></div>
      <label for="tp0">Shopify's third-party gateway fee <small>(%)</small></label>
      <div class="in"><input id="tp0" type="number" min="0" step="0.1" value="2"><span>%</span><input id="tp1" type="number" min="0" step="0.1" value="1"><span>%</span><input id="tp2" type="number" min="0" step="0.1" value="0.6"><span>%</span></div>
      <label for="gwp">Your third-party gateway's own rate</label>
      <div class="in"><input id="gwp" type="number" min="0" step="0.1" value="2.9"><span>% +</span><span>$</span><input id="gwf" type="number" min="0" step="0.01" value="0.30"></div>
      </details>""",
    out="""<div class="big"><span>Shopify's cut of your monthly sales</span><b id="eff"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <h3>Per month</h3>
      <table><tbody id="rows2"></tbody></table>
      <h3>All three plans at this volume</h3>
      <table class="wide"><thead><tr><th>Plan</th><th>Cost / month</th><th>% of sales</th></tr></thead><tbody id="plans"></tbody></table>
      <p id="be" class="note"></p>
      <div id="verdict" class="verdict"></div>""",
    js="""var PL=['Basic','Grow','Advanced'];
function calc(){
  var i=+$('plan').value,yr=$('bill').value==='y',inp=$('ch').value==='in',tp=!inp&&$('gw').value==='tp';
  var A=n('avg'),N=Math.round(n('orders')),R=A*N;
  function rate(j){
    if(inp)return [n('in'+j)/100,n('inf'),0];
    if(tp)return [n('gwp')/100,n('gwf'),n('tp'+j)/100];
    return [n('on'+j)/100,n('onf'),0];
  }
  function fee(j){return n((yr?'yr':'mo')+j)}
  function per(j){var r=rate(j);return A*(r[0]+r[2])+r[1]}
  function month(j){return fee(j)+N*per(j)}
  var r=rate(i),card=A*r[0]+r[1],extra=A*r[2],po=card+extra;
  var lab=inp?'In-person card fee':(tp?'Gateway processing':'Card processing');
  var rows=[['Order value',m(A)],[lab+' ('+(r[0]*100).toFixed(2).replace(/\\.?0+$/,'')+'% + '+m(r[1])+')',m(-card)]];
  if(tp)rows.push(['Shopify third-party fee ('+(r[2]*100).toFixed(2).replace(/\\.?0+$/,'')+'%)',m(-extra)]);
  rows.push(['You receive per order',m(A-po),'total']);
  setRows(rows);
  if(!A||!N){
    $('eff').textContent='-';
    setRows([['Enter an average order value and orders per month to see your monthly cost.','']],'rows2');
    $('plans').innerHTML='';$('be').textContent='';
    verdict(false,'Add your order value and monthly orders to compare plans.');
    return;
  }
  var tot=month(i);
  $('eff').textContent=pc(tot/R,2);
  setRows([['Monthly sales ('+N+' x '+m(A)+')',m(R)],['Card fees',m(-N*po)],[PL[i]+' plan fee',m(-fee(i))],['Total Shopify cost',m(-tot),'total']],'rows2');
  var h='',best=0;
  for(var j=0;j<3;j++){var c=month(j);if(c<month(best))best=j;h+='<tr><td>'+PL[j]+(j===i?' (yours)':'')+'</td><td>'+m(c)+'</td><td>'+pc(c/R,2)+'</td></tr>'}
  $('plans').innerHTML=h;
  var be=[];
  function bk(a,b){var d=per(a)-per(b);if(d<=0)return PL[b]+' never beats '+PL[a]+' on fees with these rates.';
    return PL[b]+' beats '+PL[a]+' above $'+Math.round((fee(b)-fee(a))/d*A).toLocaleString('en-US')+' a month in sales.'}
  be.push(bk(0,1));be.push(bk(1,2));
  $('be').textContent='Break-even ('+(yr?'yearly':'monthly')+' billing, '+m(A)+' orders): '+be.join(' ');
  if(best===i)verdict(true,PL[i]+' is the cheapest plan at '+m(R)+' a month in sales. '+(i<2?bk(i,i+1):'You are on the top plan.'));
  else verdict(false,'At '+m(R)+' a month, '+PL[best]+' would cost '+m(tot-month(best))+' less per month than '+PL[i]+'.');
}""",
    note="US Shopify rates as of October 2026: Basic $39/mo ($29 billed yearly) with 2.9% + $0.30 online; Grow $105/mo ($79 yearly) with 2.7% + $0.30; Advanced $399/mo ($299 yearly) with 2.5% + $0.30. Third-party gateway fee 2% / 1% / 0.6% on top of your gateway's own rate. In-person rates shown are defaults; check your admin, as rates differ by country and change over time. Apps, themes and currency conversion are not included.",
    body="""<h2>What Shopify actually charges</h2>
<p><strong>The plan fee.</strong> A flat monthly subscription: Basic, Grow or Advanced. Paying yearly lowers the monthly price by roughly a quarter.</p>
<p><strong>Card processing.</strong> With Shopify Payments you pay a percentage plus $0.30 on every online order. The percentage drops as the plan gets more expensive: 2.9% on Basic, 2.7% on Grow, 2.5% on Advanced.</p>
<p><strong>The third-party gateway fee.</strong> If you take payments through another processor instead of Shopify Payments, Shopify adds its own 2% (Basic), 1% (Grow) or 0.6% (Advanced) on top of what that processor charges you. On a $50 Basic order that is an extra $1.00.</p>
<h2>The formula</h2>
<p class="formula">Monthly Shopify cost = plan fee + orders x (order value x card % + $0.30)</p>
<p>Example: 300 orders a month at $50 on Basic, monthly billing. Each order costs $1.75 in card fees, so card fees come to $525.00 a month. Add the $39 plan fee and Shopify costs you $564.00, or 3.76% of your $15,000 in sales. At the same volume Grow would cost $600.00 and Advanced $864.00, so Basic is still the right plan.</p>
<h2>When upgrading pays for itself</h2>
<p>A bigger plan costs more per month but takes a smaller percentage of every order. The upgrade pays off once the percentage you save covers the extra subscription. On monthly billing, Grow costs $66 more than Basic and saves 0.2% of sales, so it breaks even at <strong>$33,000</strong> a month in online sales. Advanced beats Grow above <strong>$147,000</strong> a month.</p>
<p>Two things move those numbers a lot. Yearly billing narrows the price gap, bringing the Grow break-even down to $25,000. A third-party gateway widens the percentage gap: the gateway fee drops from 2% to 1%, so Grow pays off at just $6,600 a month. If you use a third-party gateway on Basic and sell more than that, either switch to Shopify Payments or upgrade.</p>
<p>The plan comparison here only counts payment fees. Grow and Advanced also include more staff accounts and reporting, which may matter more than a few dollars of fees.</p>""",
    faqs=[
        ("How much does Shopify take per sale?", "On Basic with Shopify Payments, 2.9% + $0.30 per online order. A $50 order costs $1.75 and you receive $48.25. The monthly plan fee comes on top of that."),
        ("When is Shopify Grow worth it over Basic?", "On card fees alone, once you sell more than $33,000 a month online with monthly billing, or $25,000 a month with yearly billing. Below that, Basic is cheaper."),
        ("What is Shopify's third-party transaction fee?", "If you don't use Shopify Payments, Shopify charges 2% of each order on Basic, 1% on Grow and 0.6% on Advanced, on top of your payment provider's own fee. That is $1.00 on a $50 order on Basic."),
        ("Does Shopify charge fees on in-person sales?", "Yes, through Shopify POS with Shopify Payments, at a lower card rate than online. The defaults here are editable because in-person rates depend on your plan and country."),
    ],
    related=["etsy-vs-shopify", "stripe-fee-calculator", "paypal-fee-calculator", "profit-margin-calculator", "break-even-calculator"],
    og_image="pins/pin-02.png",
    tests=[
        {"expect": {"rows": ["$50.00", "-$1.75", "$48.25"], "rows2": ["$15,000.00", "-$525.00", "-$39.00", "-$564.00"], "eff": "3.76%",
                    "plans": ["$564.00", "$600.00", "$864.00"], "be": ["$33,000", "$147,000"], "verdict": "Basic is the cheapest"}},
        {"set": {"gw": "tp"}, "expect": {"rows": ["-$1.00", "-$1.75"], "be": "$6,600"}},
        {"set": {"bill": "y"}, "expect": {"be": ["$25,000", "$110,000"]}},
        {"set": {"orders": "1000"}, "expect": {"verdict": "Grow would cost $34.00 less"}},
        {"set": {"orders": "0"}, "expect": {"eff": "-", "verdict": "Add your order value"}},
    ],
)
