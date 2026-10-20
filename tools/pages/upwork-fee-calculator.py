PAGE = dict(
    slug="upwork-fee-calculator",
    cat="Platform fees",
    nav_name="Upwork fee calculator",
    title="Upwork Fee Calculator 2026: Freelancer Fee, Client Fee and Take-Home Pay",
    desc="Free Upwork fee calculator: the 0% to 15% freelancer service fee, the client's marketplace and contract initiation fees, withdrawal fees and what to bill to take home a set amount.",
    h1="Upwork fee calculator",
    lead="Enter one contract. The calculator takes your freelancer service fee off the amount you bill and shows what reaches your bank after Connects and the withdrawal fee. It also shows what the client really pays once Upwork adds its marketplace fee and contract initiation fee.",
    gig="sheet",
    form="""      <label for="amt">Contract amount you bill the client <small>(fixed price, milestone, or hours x rate)</small></label>
      <div class="in"><span>$</span><input id="amt" type="number" inputmode="decimal" min="0" step="0.01" value="1000"></div>
      <label for="fee">Your freelancer service fee <small>(0% to 15%, shown on the offer or proposal)</small></label>
      <div class="in"><input id="fee" type="number" inputmode="decimal" min="0" max="100" step="0.1" value="10"><span>%</span></div>
      <label for="conn">Connects spent on the proposal <small>(shown on the job post, 0 if none)</small></label>
      <div class="in"><input id="conn" type="number" inputmode="numeric" min="0" step="1" value="0"></div>
      <label for="wsel">How you withdraw</label>
      <select id="wsel" class="full" style="width:0;min-width:100%">
        <option value="0">U.S. bank, U.S. tax address: free</option>
        <option value="2.99">U.S. bank, intl. tax address: $2.99</option>
        <option value="2">Instant Pay to a U.S. debit card: $2</option>
        <option value="0.99">Direct to Local Bank: $0.99</option>
        <option value="50">U.S. dollar wire: $50</option>
        <option value="other">PayPal, Payoneer or other</option>
      </select>
      <label for="wd">Withdrawal fee per transfer <small>(fills in from the method above; for PayPal or Payoneer, copy it from your Upwork withdrawal settings)</small></label>
      <div class="in"><span>$</span><input id="wd" type="number" inputmode="decimal" min="0" step="0.01" value="0" placeholder="from your withdrawal settings"></div>
      <label for="csel">Client's marketplace fee <small>(Basic plan, paid by the client on top of your rate; 3% only for qualifying U.S. clients)</small></label>
      <select id="csel" class="full" style="width:0;min-width:100%">
        <option value="7.99">7.99%: flat rate, the maximum</option>
        <option value="5">5%: tiered rate, card or PayPal</option>
        <option value="3">3%: tiered rate, U.S. bank account</option>
      </select>
      <details><summary class="note">Edit fee rates</summary>
      <label for="cmf">Client Marketplace Fee <small>(fills in from the choice above; Business Plus is 10%, or 8% for some U.S. clients paying by checking)</small></label>
      <div class="in"><input id="cmf" type="number" min="0" step="0.01" value="7.99"><span>%</span></div>
      <label for="cif">Contract initiation fee <small>(Basic plan: $0.99 to $14.99 per new contract, set to the maximum here. Business Plus: none on hourly contracts, up to $4.99 on small fixed-price ones)</small></label>
      <div class="in"><span>$</span><input id="cif" type="number" min="0" step="0.01" value="14.99"></div>
      <label for="cp">Price per Connect</label>
      <div class="in"><span>$</span><input id="cp" type="number" min="0" step="0.01" value="0.15"></div>
      </details>""",
    out="""<div class="big"><span>Reaches your bank</span><b id="keep"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function r2(x){return (x<0?-1:1)*Math.round(Math.abs(x)*100+1e-6)/100}
function setW(){var v=$('wsel').value;$('wd').value=v==='other'?'':v}
function setC(){$('cmf').value=$('csel').value}
$('wsel').addEventListener('input',setW);$('wsel').addEventListener('change',setW);
$('csel').addEventListener('input',setC);$('csel').addEventListener('change',setC);
function billFor(T,f){
  var net=function(b){return r2(b-r2(b*f/100))},B=r2(T/(1-f/100)),i=0;
  while(net(B)<T-0.001&&i++<100000)B=r2(B+0.01);
  while(B>=0.01&&net(r2(B-0.01))>=T-0.001&&i++<100000)B=r2(B-0.01);
  return B}
function calc(){
  var A=r2(n('amt')),f=n('fee');
  if(!A){$('keep').textContent=m(0);setRows([]);verdict(false,'Enter the contract amount to see Upwork fees.');return}
  var ff=r2(A*f/100),rec=r2(A-ff),cn=r2(n('conn')*n('cp')),wd=r2(n('wd')),bank=r2(rec-cn-wd);
  var cr=n('cmf'),cf=r2(A*cr/100),ci=r2(n('cif')),cp=r2(A+cf+ci),up=r2(ff+cf+ci);
  var r=[['Contract amount',m(A)],['Freelancer service fee ('+f+'%)',m(-ff)],['You receive on Upwork',m(rec)]];
  if(cn)r.push(['Connects ('+n('conn')+' x '+m(n('cp'))+')',m(-cn)]);
  if(wd)r.push(['Withdrawal fee (per withdrawal, not per contract)',m(-wd)]);
  else if($('wsel').value==='other')r.push(['Withdrawal fee: type it in from your Upwork withdrawal settings',m(0)]);
  r.push(['Reaches your bank',m(bank),'total'],['<strong>What the client pays</strong>',''],['Contract amount',m(A)],
    ['Client marketplace fee ('+cr+'%)',m(cf)],['Contract initiation fee',m(ci)],['Client pays, before any tax',m(cp),'total'],
    ['Upwork fees on this contract (both sides)',m(up)+' ('+pc(up/cp)+')'],
    ['Lowest bill that takes home '+m(A)+' after the service fee',f<100?m(billFor(A,f)):'n/a']);
  setRows(r);$('keep').textContent=m(bank);
  if(rec<=0)verdict(false,'At a '+f+'% service fee nothing from this contract reaches you. Check the fee on your offer; Upwork charges 0% to 15%.');
  else if(bank<=0)verdict(false,'After Connects and the withdrawal fee, nothing from this contract reaches your bank. Withdraw several payments together so you pay the withdrawal fee once.');
  else verdict(true,'Upwork keeps '+pc((cp-bank)/cp)+' of the '+m(cp)+' the client pays; '+pc(bank/cp)+' reaches your bank.');
}""",
    note="""Upwork rates checked October 20, 2026 in the Upwork Help Center articles <a href="https://support.upwork.com/hc/en-us/articles/211062538-Learn-about-the-Freelancer-Service-Fee" rel="noopener">Freelancer Service Fee</a>, <a href="https://support.upwork.com/hc/en-us/articles/40445575013395-When-do-I-pay-a-Freelancer-Service-Fee" rel="noopener">When do I pay a Freelancer Service Fee</a>, <a href="https://support.upwork.com/hc/en-us/articles/4660220468499-What-is-the-Client-Marketplace-Fee" rel="noopener">Client Marketplace Fee</a>, <a href="https://support.upwork.com/hc/en-us/articles/211068088-How-to-pay-by-bank-account-as-a-client" rel="noopener">paying by bank account</a>, <a href="https://support.upwork.com/hc/en-us/articles/50793925943699-Try-Upwork-s-Business-Plus-plan-Promo-terms-and-conditions" rel="noopener">Business Plus promo terms</a>, <a href="https://support.upwork.com/hc/en-us/articles/26106318334611-What-is-the-Contract-Initiation-Fee-on-Upwork" rel="noopener">Contract Initiation Fee</a>, <a href="https://support.upwork.com/hc/en-us/articles/30915724346387-How-Business-Plus-plan-fees-work-on-Upwork" rel="noopener">Business Plus fees</a>, <a href="https://support.upwork.com/hc/en-us/articles/360051594473-How-U-S-sales-tax-works-for-Upwork-clients" rel="noopener">U.S. sales tax for clients</a>, <a href="https://support.upwork.com/hc/en-us/articles/360025040794-Direct-Contracts-bring-a-client-to-Upwork" rel="noopener">Direct Contracts</a>, <a href="https://support.upwork.com/hc/en-us/articles/211062898-Understanding-and-using-Connects" rel="noopener">Connects</a>, <a href="https://support.upwork.com/hc/en-us/articles/211060918-How-to-get-paid-on-Upwork" rel="noopener">How to get paid</a> and the withdrawal articles for <a href="https://support.upwork.com/hc/en-us/articles/227022468-Direct-to-U-S-Bank-timing-and-fees-explained" rel="noopener">U.S. bank</a>, <a href="https://support.upwork.com/hc/en-us/articles/211060578-What-are-the-fees-limits-and-timing-of-Direct-to-Local-Bank-payments" rel="noopener">local bank</a>, <a href="https://support.upwork.com/hc/en-us/articles/211063898-How-do-wire-transfers-work-on-Upwork" rel="noopener">wire</a>, <a href="https://support.upwork.com/hc/en-us/articles/211063978-What-are-the-PayPal-fees-and-timing-for-withdrawals" rel="noopener">PayPal</a> and <a href="https://support.upwork.com/hc/en-us/articles/211064008-How-quickly-Payoneer-pays-and-what-fees-apply" rel="noopener">Payoneer</a>, plus Upwork's <a href="https://www.sec.gov/Archives/edgar/data/1627475/000162747526000047/upwk-20260630.htm" rel="noopener">10-Q for the quarter ended June 30, 2026</a>. Your service fee is 0% to 15% per contract, set by Upwork, shown on the offer or proposal and then locked for that contract. It has been variable for new contracts since May 2025; contracts formed before then keep a flat 10%, which is this page's default. Direct Contracts are 5% (0% with Freelancer Plus), and Enterprise contracts are typically 10%. Upwork's sources differ on the client's Basic plan fee: the Client Marketplace Fee article says up to 7.99%, or 3% for qualifying U.S. clients paying by bank account, while the 10-Q gives 5% (3% by bank account) and the bank account article calls 5% the usual rate. Upwork's Business Plus promo terms explain both: clients on a flat structure pay 7.99% whatever the payment method, and clients on a tiered structure pay 5%, or 3% by U.S. bank account. This page defaults to 7.99%, the most a Basic client pays, plus the maximum $14.99 of the $0.99 to $14.99 initiation fee. Business Plus clients pay 10% (8% for some U.S. clients paying by checking) and an initiation fee of up to $4.99 only on small fixed-price contracts (Upwork's two articles put the cutoff at under $100 and at $100 or less), so change those under Edit fee rates. Sales tax or VAT that Upwork adds for clients in some places is not included. Withdrawal: Direct to U.S. Bank is free with a U.S. tax address and $2.99 with a non-U.S. tax address since September 1, 2026; Instant Pay to a U.S. debit card $2; Direct to Local Bank $0.99 plus incoming fees at some banks; U.S. dollar wire $50 plus bank and intermediary fees. Upwork does not publish its PayPal or Payoneer fee in the Help Center; it shows in your withdrawal settings, and those services may add their own. Connects cost $0.15 each. This page rounds each fee to the nearest cent, as Upwork's own service fee examples do.""",
    body="""<h2>How Upwork fees work</h2>
<p><strong>Freelancer service fee.</strong> Upwork takes 0% to 15% of what you earn on a contract, bonuses included. Upwork sets the rate for each contract, and you see it on the offer or while you write the proposal, so you know it before you agree. Once the proposal, offer or contract is sent, the rate is locked for that contract, but your next contract can carry a different one. This variable fee started in May 2025; contracts formed before then keep the old flat 10%. On Direct Contracts, with a client you brought to Upwork yourself, the fee is 5%, or 0% with an active Freelancer Plus membership. If a client gets a refund, Upwork returns the service fee you paid on that amount.</p>
<p><strong>Client fees.</strong> The client pays these on top of your rate, so they don't come out of your pay, but they do raise the client's total. On the free Basic plan the Client Marketplace Fee is up to 7.99% of every payment to you. Upwork's own pages describe two setups: a flat 7.99% whatever the payment method, or a tiered 5%, cut to 3% for qualifying U.S. clients who pay from a bank account. There is also a one-time Contract Initiation Fee of $0.99 to $14.99 on each new contract, even with a freelancer the client has hired before. Business Plus clients pay 10% (8% for some U.S. clients paying by checking) and an initiation fee only on small fixed-price contracts. The marketplace fee is not refunded, even if the payment is. Depending on where the client is, Upwork may also add sales tax or VAT.</p>
<p><strong>Getting the money out.</strong> Direct to U.S. Bank is free if your tax address is in the U.S. Since September 1, 2026 it costs $2.99 per withdrawal if your tax address is outside the U.S. Instant Pay to a U.S. debit card is $2 per transfer. Direct to Local Bank is $0.99 per withdrawal, plus incoming fees at some banks. A U.S. dollar wire is $50, plus whatever your bank and any intermediary bank charge. Upwork's fee for PayPal and Payoneer is not listed in its Help Center; you see it in your withdrawal settings when you add the method, and PayPal or Payoneer may charge their own fees too. Each of these is charged per withdrawal, so taking out several payments at once means paying it once.</p>
<p><strong>Connects.</strong> Submitting a proposal costs Connects, at $0.15 each. The number needed varies by job and is shown on the job post. They are part of what it costs to win the work, so the calculator takes them off what reaches your bank.</p>
<h2>The formula</h2>
<p class="formula">You receive = amount billed x (1 - service fee %)<br>Client pays = amount billed x (1 + marketplace fee %) + initiation fee<br>To take home T, bill T / (1 - service fee %)</p>
<p>Upwork rounds the service fee to the nearest cent: its own examples turn $26.664 into $26.66 and $33.336 into $33.34. This page rounds every fee the same way, so a result can be a cent or two away from the simple math. The bill amount it shows is the lowest, to the cent, that still leaves you the target after that rounding. To take home $500 at 15%, for example, $588.23 is enough, one cent less than the simple math rounded.</p>
<h2>Worked example</h2>
<p>A <strong>$1,000</strong> fixed-price contract with a <strong>10%</strong> freelancer service fee. The client is on the Basic plan at the 7.99% flat rate, and the initiation fee is the maximum $14.99. You withdraw to a U.S. bank with a U.S. tax address, so the withdrawal is free.</p>
<p>The service fee is $100.00, so you receive <strong>$900.00</strong> on Upwork and the same $900.00 reaches your bank. The client pays the $1,000 plus a $79.90 marketplace fee plus the $14.99 initiation fee, <strong>$1,094.89</strong> in all before any tax. Upwork's fees on both sides come to $194.89, which is 17.8% of what the client pays; the other 82.2% reaches you. To take home the full $1,000 after the service fee, you would bill <strong>$1,111.11</strong>.</p>
<p>If the client is on the tiered rate instead, the marketplace fee is $50.00 by card or PayPal (the client pays $1,064.99) or $30.00 by U.S. bank account ($1,044.99). If the contract carries a 15% service fee, you receive $850.00, and you would need to bill $1,176.47 to clear $1,000. Upwork's own example shows the rounding: to net $20 an hour at a 10% fee you bill $22.22, and 12 hours comes to $266.64. The fee is $26.664, rounded to $26.66, so you net $239.98 instead of $240.</p>
<h2>Pricing tip: divide, don't add</h2>
<p>To cover a fee, divide your target by (1 - fee) instead of adding the fee percentage on top. Adding 10% to $1,000 gives $1,100, and 10% of $1,100 is $110, which leaves you $990. Dividing gives $1,111.11, and 10% of that is $111.11, which leaves exactly $1,000. At 15% the gap is bigger: billing $1,150 nets $977.50, while $1,176.47 nets $1,000.00. Since the rate can change from one contract to the next, check the fee on each offer before you quote.</p>
<h2>Upwork fees and your taxes</h2>
<p>Upwork says the total billed to your clients counts as your income, and the service fee you paid may be deductible as a business expense. In the example above, that means $1,000 of income and a $100 fee, not $900 of income. The fee shows as its own line in your Transactions report and your Billings and earnings report. Check with a tax professional for your own situation.</p>""",
    faqs=[
        ("How much does Upwork take from freelancers in 2026?", "Between 0% and 15% of what you earn on each contract, set by Upwork and shown on the offer or proposal before you agree. At 10%, a $1,000 contract leaves you $900.00; at 15%, $850.00. Contracts formed before May 2025 keep a flat 10%, and Direct Contracts with clients you bring yourself are 5% (0% with Freelancer Plus)."),
        ("What does the client pay on top of my rate?", "On the Basic plan, a Client Marketplace Fee of up to 7.99% of each payment plus a one-time Contract Initiation Fee of $0.99 to $14.99 per new contract. Some clients pay a flat 7.99%; others are on a tiered 5%, or 3% when a qualifying U.S. client pays by bank account. So a $1,000 contract costs a Basic client at most $1,094.89 before any sales tax or VAT. Business Plus clients pay 10%, or 8% for some U.S. clients paying by checking."),
        ("How do I set my rate so I take home a set amount?", "Divide the amount you want by (1 - your fee). To take home $1,000 at 10%, bill $1,111.11; at 15%, bill $1,176.47. Upwork rounds the fee to the cent, so the result can shift by a cent: in Upwork's own example, netting $20 an hour at 10% means charging $22.22, and 12 hours nets $239.98."),
        ("What are Upwork's withdrawal fees?", "Direct to U.S. Bank is free with a U.S. tax address and $2.99 per withdrawal with a non-U.S. tax address since September 1, 2026. Instant Pay to a U.S. debit card is $2, Direct to Local Bank is $0.99, and a U.S. dollar wire is $50. Upwork's PayPal and Payoneer fees are shown in your withdrawal settings, and those services may add their own."),
    ],
    related=["paypal-fee-calculator", "stripe-fee-calculator", "gumroad-fee-calculator", "price-increase-calculator", "invoice-late-fee-calculator", "markup-calculator"],
    cta_head="Billing clients outside Upwork too?",
    cta_text="On Upwork contracts, Upwork collects for you. For the clients you find and invoice yourself, the <strong>Invoice Tracker Template Google Sheets + Excel, Payment Reminder Email Templates (Word + PDF)</strong> keeps you paid: the <strong>Invoice Chaser</strong> spreadsheet tracks every invoice, works out late fees, tells you who to chase today and writes the email with the client's name, amounts and dates filled in. It also has 10 ready-to-send emails from the friendly reminder to the letter before action, plus payment terms and a late fee policy to add before the work starts. Word, Google Docs, Excel and Google Sheets. One-time $9.",
    cta_url="https://quietprofitsheets.gumroad.com/l/get-paid-kit",
    cta_btn="Get the Invoice Tracker Template",
    tests=[
        {"expect": {"rows": ["-$100.00", "$900.00", "$79.90", "$14.99", "$1,094.89", "$194.89", "17.8%", "$1,111.11"], "keep": "$900.00",
                    "verdict": ["17.8%", "82.2%"]}},
        {"set": {"fee": "15", "csel": "3"}, "expect": {"rows": ["-$150.00", "$850.00", "Client marketplace fee (3%)", "$30.00", "$1,044.99", "$194.99", "18.7%", "$1,176.47"], "keep": "$850.00"}},
        {"set": {"amt": "266.64"}, "expect": {"rows": ["-$26.66", "$296.27"], "keep": "$239.98"}},
        {"set": {"amt": "500", "fee": "15"}, "expect": {"rows": ["-$75.00", "$588.23"], "keep": "$425.00"}},
        {"set": {"conn": "20", "wsel": "50", "csel": "5"}, "expect": {"rows": ["-$3.00", "-$50.00", "Client marketplace fee (5%)", "$1,064.99"], "keep": "$847.00", "verdict": ["20.5%", "79.5%"]}},
        {"set": {"amt": "", "fee": ""}, "expect": {"verdict": "Enter the contract amount", "keep": "$0.00"}},
    ],
)
