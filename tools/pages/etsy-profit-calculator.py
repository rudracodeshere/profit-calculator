PAGE = dict(
    cta_extra=["budget"],
    slug="etsy-profit-calculator",
    cat="Etsy tools",
    nav_name="Etsy monthly profit calculator",
    title="Etsy Profit Calculator: Your Shop's Real Monthly Profit (2026)",
    desc="Work out your Etsy shop's monthly net profit: revenue, every Etsy fee, Etsy Ads, refunds, materials and labels, plus margin, profit per order and hourly pay.",
    h1="Etsy profit calculator: what does your shop make in a month?",
    lead="A single sale can look fine while the month loses money. Enter a typical month for your whole shop: orders, average order, materials, labels, ad spend and refunds. You get net profit, margin, profit per order and, if you add your hours, what you actually earn per hour. Nothing leaves your browser.",
    form="""      <label for="orders">Orders per month</label>
      <div class="in"><input id="orders" type="number" inputmode="decimal" min="0" step="1" value="100"></div>
      <label for="aov">Average item total per order <small>(before shipping)</small></label>
      <div class="in"><span>$</span><input id="aov" type="number" inputmode="decimal" min="0" step="0.01" value="30"></div>
      <label for="ipo">Average items per order</label>
      <div class="in"><input id="ipo" type="number" inputmode="decimal" min="1" step="0.1" value="1.2"></div>
      <label for="ship">Shipping charged per order <small>(0 if free)</small></label>
      <div class="in"><span>$</span><input id="ship" type="number" inputmode="decimal" min="0" step="0.01" value="4"></div>
      <label for="mat">Materials + packaging per item</label>
      <div class="in"><span>$</span><input id="mat" type="number" inputmode="decimal" min="0" step="0.01" value="7"></div>
      <label for="label">Shipping label per order</label>
      <div class="in"><span>$</span><input id="label" type="number" inputmode="decimal" min="0" step="0.01" value="4.50"></div>
      <label for="share">Orders from Offsite Ads</label>
      <div class="in"><input id="share" type="number" inputmode="decimal" min="0" max="100" step="1" value="10"><span>%</span></div>
      <label for="ads">Etsy Ads spend per month</label>
      <div class="in"><span>$</span><input id="ads" type="number" inputmode="decimal" min="0" step="1" value="60"></div>
      <label for="refund">Orders refunded</label>
      <div class="in"><input id="refund" type="number" inputmode="decimal" min="0" max="100" step="0.5" value="2"><span>%</span></div>
      <label for="other">Other monthly costs <small>(software, supplies, packaging stock)</small></label>
      <div class="in"><span>$</span><input id="other" type="number" inputmode="decimal" min="0" step="1" value="25"></div>
      <label class="check"><input id="plus" type="checkbox"> I pay for Etsy Plus ($10/month)</label>
      <label for="hours">Hours you work on the shop per month <small>(optional)</small></label>
      <div class="in"><input id="hours" type="number" inputmode="decimal" min="0" step="1" value="0"><span>hrs</span></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="tx">Transaction fee</label>
      <div class="in"><input id="tx" type="number" min="0" step="0.1" value="6.5"><span>%</span></div>
      <label for="pp">Payment processing</label>
      <div class="in"><input id="pp" type="number" min="0" step="0.1" value="3"><span>% +</span><span>$</span><input id="pf" type="number" min="0" step="0.01" value="0.25"></div>
      <label for="oa">Offsite Ads rate <small>(12% if your shop made over $10k last year)</small></label>
      <div class="in"><input id="oa" type="number" min="0" step="1" value="15"><span>%</span></div>
      <label for="lfee">Listing fee per item sold</label>
      <div class="in"><span>$</span><input id="lfee" type="number" min="0" step="0.01" value="0.20"></div>
      </details>""",
    out="""<div class="big"><span>Net profit this month</span><b id="net"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var o=n('orders'),ot=n('aov')+n('ship'),rev=o*ot,items=o*Math.max(1,n('ipo'));
  if(!o||!ot){$('net').textContent='-';setRows([]);verdict(false,'Enter your orders per month and an average order value to see the month.');return}
  var tx=rev*n('tx')/100,pp=o*(ot*n('pp')/100+n('pf')),lf=items*n('lfee');
  var oaOrders=o*Math.min(n('share'),100)/100,oa=oaOrders*Math.min(ot*n('oa')/100,100);
  var fees=tx+pp+lf+oa,ads=n('ads'),plus=$('plus').checked?10:0;
  var rf=o*Math.min(n('refund'),100)/100*ot*(1-n('tx')/100);
  var mat=items*n('mat'),lab=o*n('label'),oth=n('other');
  var etsy=fees+ads+plus,net=rev-etsy-rf-mat-lab-oth,hrs=n('hours');
  $('net').textContent=m(net);
  var r=[['Revenue ('+Math.round(o)+' orders x '+m(ot)+')',m(rev)],['Transaction fees',m(-tx)],['Payment processing',m(-pp)],['Listing fees ('+(Math.round(items*10)/10)+' items)',m(-lf)]];
  if(oa)r.push(['Offsite Ads ('+(Math.round(oaOrders*10)/10)+' orders)',m(-oa)]);
  if(ads)r.push(['Etsy Ads',m(-ads)]);
  if(plus)r.push(['Etsy Plus',m(-plus)]);
  r.push(['Total paid to Etsy',m(-etsy)+' ('+pc(etsy/rev)+')']);
  if(rf)r.push(['Refunds (after fee credit)',m(-rf)]);
  r.push(['Materials + packaging',m(-mat)],['Shipping labels',m(-lab)]);
  if(oth)r.push(['Other costs',m(-oth)]);
  r.push(['Net profit',m(net),'total'],['Profit margin',pc(net/rev)],['Profit per order',m(net/o)]);
  if(hrs)r.push(['Your effective hourly pay',m(net/hrs)+'/hr']);
  setRows(r);
  if(net<0)verdict(false,'This month loses '+m(-net)+'. Each order costs you '+m(-net/o)+'. Check ad spend and your lowest-priced items first.');
  else if(hrs&&net/hrs<15)verdict(false,'You make '+m(net)+' but only '+m(net/hrs)+' for each hour you put in. A price rise of a few dollars per order changes that more than more orders do.');
  else verdict(true,'You keep '+pc(net/rev,0)+' of what buyers pay, '+m(net/o)+' per order. Etsy takes '+pc(etsy/rev,0)+' including ads.');
}""",
    note="US Etsy rates as of October 2026: 6.5% transaction fee and 3% + $0.25 processing on each order total (items + shipping), $0.20 listing fee per item sold, Offsite Ads 15% (12% over $10k/yr, max $100 per order), Etsy Plus $10/month. Refunds assume the item is not resold; Etsy credits the transaction fee back on a refund but keeps the processing fee. Sales tax and income tax are left out. Processing rates differ outside the US, so edit them above.",
    body="""<h2>Why monthly profit is different from per-sale profit</h2>
<p>Per-sale calculators answer "is this price right?". This one answers "did the shop make money?". The gap between the two is everything that doesn't belong to a single sale: Etsy Ads billed daily, Etsy Plus, the refund you issued for a broken mug, the roll of mailers you bought this month. A shop can price every item correctly and still end the month behind if those costs aren't counted.</p>
<h2>The formula</h2>
<p class="formula">Net profit = revenue &minus; Etsy fees &minus; Etsy Ads &minus; Etsy Plus &minus; refunds &minus; materials &minus; labels &minus; other costs</p>
<p>Revenue is orders times the average order total (items plus the shipping you charge). Etsy fees are the 6.5% transaction fee and 3% processing on that revenue, $0.25 per order, $0.20 per item sold, and 15% on the share of orders that came through Offsite Ads.</p>
<h2>Worked example</h2>
<p>A shop with 100 orders a month, $30 of items per order (1.2 items on average) and $4 shipping charged takes in <strong>$3,400.00</strong>. Etsy's fees come to $221.00 in transaction fees, $127.00 processing, $24.00 in listing fees for 120 items and $51.00 of Offsite Ads on 10 orders. Add $60 of Etsy Ads and the shop pays Etsy <strong>$483.00</strong>, 14.2% of revenue.</p>
<p>Two refunds cost $63.58 after Etsy credits back the transaction fee. Materials at $7 per item are $840.00, labels at $4.50 are $450.00, and $25 goes on other costs. Net profit: <strong>$1,538.42</strong>, a 45.2% margin, or $15.38 per order. If the shop takes 40 hours a month and pays for Etsy Plus, that is $1,528.42, or <strong>$38.21 an hour</strong>.</p>
<h2>Where monthly profit usually leaks</h2>
<p><strong>Etsy Ads.</strong> It is the one cost that grows without a sale attached. Compare the monthly spend line to profit per order: the ads have to bring in enough extra orders to cover their own cost before they add anything. The <a href="../etsy-ads-calculator/">Etsy Ads calculator</a> works out whether yours do.</p>
<p><strong>Small orders.</strong> The $0.45 of fixed fees per order and the label cost don't shrink with the order. If your average order is under $20, your margin is fragile.</p>
<p><strong>Refunds.</strong> A refunded handmade item is usually gone for good, so you lose the materials and label as well as the revenue. Even a 2% refund rate is worth tracking.</p>
<p>This page uses averages. To see which listings carry the month and which drag it down, you need your full sales export broken out per product.</p>""",
    faqs=[
        ("How do I calculate my Etsy shop's profit for the month?", "Take total revenue (items plus shipping charged), then subtract every Etsy fee, Etsy Ads, Etsy Plus, refunds, materials, shipping labels and other costs. Your monthly CSV from Shop Manager &gt; Settings &gt; Options &gt; Download Data has the sales and fees; materials and labels you add yourself."),
        ("What is a good profit margin for an Etsy shop?", "It depends on how much of your time is in the product. In the example above the shop keeps 45.2%, but that is before paying for 40 hours of work. A margin that still looks healthy after you count your hours is the one to aim for."),
        ("Do Etsy Ads count as an Etsy fee?", "They are billed by Etsy on your payment account, so they come out of the same deposit. This calculator puts them in the total paid to Etsy ($483.00 in the example) but lists them separately, because you control them."),
        ("Does Etsy refund fees when I refund an order?", "Etsy credits back the transaction fee on the refunded amount. The payment processing fee is not returned, and neither is the listing fee. The refund line here reflects that."),
        ("Is my Etsy profit the same as my taxable income?", "Close, but not exactly. Income tax is left out here, and your tax return may treat some costs (equipment, home office) differently. Use this for running the shop and ask a tax professional for the return."),
    ],
    related=["etsy-fee-calculator", "etsy-ads-calculator", "etsy-hourly-wage-calculator", "etsy-offsite-ads-calculator", "profit-margin-calculator", "break-even-calculator"],
    og_image="pins/pin-02.png",
    tests=[
        {"expect": {"net": ["$1,538.42"], "rows": ["$3,400.00", "-$221.00", "-$127.00", "-$24.00", "-$51.00", "-$60.00", "-$483.00", "14.2%", "-$63.58", "-$840.00", "-$450.00", "-$25.00", "45.2%", "$15.38"]}},
        {"set": {"hours": "40"}, "click": ["plus"], "expect": {"net": ["$1,528.42"], "rows": ["-$10.00", "-$493.00", "$38.21/hr"]}},
        {"set": {"orders": "50", "aov": "12", "ipo": "1", "ship": "0", "mat": "6", "label": "4", "share": "0", "ads": "150", "refund": "0", "other": "40"}, "expect": {"net": ["-$169.50"], "rows": ["$600.00", "-$229.50", "-$3.39"], "verdict": ["loses $169.50"]}},
        {"set": {"orders": "0"}, "expect": {"verdict": ["Enter your orders"]}},
    ],
)
