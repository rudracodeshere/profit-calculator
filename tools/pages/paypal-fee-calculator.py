PAGE = dict(
    slug="paypal-fee-calculator",
    cat="Platform fees",
    cta_head="Sending invoices? Know who owes you, and what to send them.",
    cta_text="The <strong>Invoice Tracker Template Google Sheets + Excel, Payment Reminder Email Templates (Word + PDF)</strong> includes the <strong>Invoice Chaser</strong> spreadsheet: it tracks every invoice and its due date, works out late fees, tells you who to chase today and writes the email with the client's name, amounts and dates filled in. Plus 10 ready-to-send payment reminder emails. Word, Google Docs, Excel and Google Sheets.",
    cta_url="https://quietprofitsheets.gumroad.com/l/get-paid-kit",
    cta_btn="Get the Invoice Tracker Template",
    cta_extra=["seller"],
    nav_name="PayPal fee calculator",
    title="PayPal Fee Calculator 2026: What You Receive and What to Charge",
    desc="Free PayPal fee calculator: what you receive after fees, or what to ask for to receive an exact amount. Goods & Services, Checkout, invoices, international.",
    h1="PayPal fee calculator",
    lead="Pick the kind of PayPal payment, then enter what the buyer pays to see what lands in your account. Or work backward: enter the amount you need to receive and get the exact amount to invoice.",
    form="""      <label for="preset">Payment type</label>
      <select id="preset" class="full"><option value="gs">Goods &amp; Services (2.99%, no fixed fee)</option><option value="cd">Card payment (2.99% + $0.49)</option><option value="co">PayPal Checkout / invoice (3.49% + $0.49)</option><option value="cu">Custom rate (set under Edit fee rates)</option></select>
      <label class="check"><input id="intl" type="checkbox"> Buyer is outside the US (international fee)</label>
      <label for="amt">Amount the buyer pays</label>
      <div class="in"><span>$</span><input id="amt" type="number" inputmode="decimal" min="0" step="0.01" value="100"></div>
      <label for="want">Amount you want to receive</label>
      <div class="in"><span>$</span><input id="want" type="number" inputmode="decimal" min="0" step="0.01" value="100"></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="cp">Custom rate</label>
      <div class="in"><input id="cp" type="number" min="0" step="0.01" value="2.99"><span>% +</span><span>$</span><input id="cf" type="number" min="0" step="0.01" value="0.49"></div>
      <label for="ip">International fee added</label>
      <div class="in"><input id="ip" type="number" min="0" step="0.1" value="1.5"><span>%</span></div>
      </details>""",
    out="""<div class="big"><span>You receive</span><b id="recv"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <h3>Work backward</h3>
      <table><tbody id="rows2"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var p=$('preset').value,pct,fix;
  if(p==='gs'){pct=2.99;fix=0}else if(p==='cd'){pct=2.99;fix=0.49}else if(p==='co'){pct=3.49;fix=0.49}else{pct=n('cp');fix=n('cf')}
  if($('intl').checked)pct+=n('ip');
  var r=pct/100,lab='PayPal fee ('+(+pct.toFixed(2))+'%'+(fix?' + '+m(fix):'')+')';
  var A=n('amt'),fee=A?A*r+fix:0,got=A-fee;
  setRows([['Buyer pays',m(A)],[lab,m(-fee)],['You receive',m(got),'total'],['Fee as share of payment',A?pc(fee/A,2):'-']]);
  $('recv').textContent=m(got);
  var W=n('want');
  if(r>=1){setRows([['This rate takes the whole payment.','']],'rows2');verdict(false,'Check the custom rate: it is 100% or more.');return}
  if(W){
    var ask=Math.ceil((W+fix)/(1-r)*100-1e-6)/100,f2=ask*r+fix;
    setRows([['To receive '+m(W)+', ask for',m(ask),'total'],[lab,m(-f2)],['You receive',m(ask-f2)]],'rows2');
  }else setRows([['Enter the amount you want to receive.','']],'rows2');
  if(A&&got<=0)verdict(false,'The fixed '+m(fix)+' fee eats this whole payment. Bundle small payments into one.');
  else if(!A)verdict(false,'Enter a payment amount to see the fee.');
  else verdict(true,'PayPal keeps '+m(fee)+'. '+(W?'To net '+m(W)+' after fees, invoice '+m(Math.ceil((W+fix)/(1-r)*100-1e-6)/100)+'.':''));
}""",
    note="US PayPal rates as of October 2026: Goods &amp; Services payments 2.99% with no fixed fee; standard card payments 2.99% + $0.49; PayPal Checkout and invoicing 3.49% + $0.49; international payments add 1.5%. The fixed fee differs when you're paid in another currency, and PayPal adjusts rates over time, so use the custom option to match your account's fee page. The backward calculation rounds up to the next cent so you never end up short.",
    body="""<h2>How PayPal fees are worked out</h2>
<p>A commercial PayPal payment costs a percentage of the amount, and most payment types add a fixed fee too. PayPal's US fee table lists Goods &amp; Services payments at 2.99% with no fixed fee. Standard card payments are 2.99% + $0.49. If the buyer pays through a PayPal Checkout button on your site or through a PayPal invoice, the rate is 3.49% + $0.49. Payments from buyers outside the US add another 1.5%.</p>
<p class="formula">You receive = amount - (amount x rate + fixed fee)</p>
<p>Example: a $100 Goods &amp; Services payment costs $2.99 in fees, so you receive $97.01. The same payment by card costs $3.48 ($96.52 left), and through an invoice it costs $3.98 ($96.02 left). As Goods &amp; Services from an international buyer it costs $4.49, leaving $95.51.</p>
<h2>How much to charge so you receive a set amount</h2>
<p>You can't just add 2.99% to your price, because the fee is also charged on the part you added. Divide instead:</p>
<p class="formula">Amount to ask for = (amount you want + fixed fee) / (1 - rate)</p>
<p>To receive $100 from a Goods &amp; Services payment, ask for $103.09. The fee on $103.09 is $3.08, which leaves $100.01, because the amount is rounded up to the next cent so you never end up short. For an international buyer you would ask for $104.71. For a card payment, which adds the $0.49 fixed fee, ask for $103.59.</p>
<h2>Small payments</h2>
<p>The $0.49 fixed fee on card, Checkout and invoice payments matters more the smaller the payment. On $100 it is under half a percent, but on a $20 card payment the total fee is $1.09, more than 5% of the payment. The same $20 as Goods &amp; Services costs $0.60. If customers pay you small amounts often, collect them in one invoice.</p>""",
    faqs=[
        ("What is the PayPal fee for $100?", "For a US Goods &amp; Services payment, $2.99 (2.99%, no fixed fee), so you receive $97.01. A card payment costs $3.48 (2.99% + $0.49). Through PayPal Checkout or an invoice it is $3.98."),
        ("How much should I charge to receive $100 after PayPal fees?", "$103.09 for a US Goods &amp; Services payment: divide $100 by 1 minus 2.99% and round up to the cent. For a card payment, add the $0.49 fixed fee to $100 first, which gives $103.59."),
        ("What is the PayPal fee on $20?", "$0.60 as a Goods &amp; Services payment (2.99%), so you receive $19.40. As a card payment it is $1.09 at 2.99% + $0.49, leaving $18.91."),
        ("Does PayPal charge more for international payments?", "Yes. A payment from a buyer outside the US adds 1.5%, so Goods &amp; Services becomes 4.49%, or $4.49 on $100."),
        ("Are Friends &amp; Family payments free?", "Sending money to friends and family from a bank or PayPal balance in the US has no fee, but those payments have no purchase protection and shouldn't be used for sales. Use Goods &amp; Services for anything you sell."),
    ],
    related=["stripe-fee-calculator", "shopify-fee-calculator", "gumroad-fee-calculator", "ebay-fee-calculator", "markup-calculator"],
    og_image="pins/pin-05.png",
    tests=[
        {"expect": {"rows": ["$100.00", "PayPal fee (2.99%)", "-$2.99", "$97.01"], "recv": "$97.01", "rows2": ["$103.09", "-$3.08", "$100.01"]}},
        {"set": {"preset": "cd"}, "expect": {"rows": ["2.99% + $0.49", "-$3.48", "$96.52"], "rows2": ["$103.59", "-$3.59", "$100.00"]}},
        {"set": {"preset": "co"}, "expect": {"rows": ["-$3.98", "$96.02"]}},
        {"click": ["intl"], "expect": {"rows": ["4.49%", "-$4.49", "$95.51"], "rows2": "$104.71"}},
        {"set": {"amt": "20"}, "expect": {"rows": ["-$0.60", "$19.40", "2.99%"]}},
        {"set": {"preset": "cd", "amt": "20"}, "expect": {"rows": ["-$1.09", "$18.91", "5.44%"]}},
        {"set": {"preset": "cd", "amt": "0.30", "want": ""}, "expect": {"verdict": "eats this whole payment", "rows2": "Enter the amount"}},
        {"set": {"preset": "cu", "cp": "4", "cf": "0"}, "expect": {"rows": "-$4.00"}},
    ],
)
