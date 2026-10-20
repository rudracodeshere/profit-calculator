PAGE = dict(
    slug="payment-reminder-email-generator",
    cat="Invoices & getting paid",
    nav_name="Payment reminder email generator",
    title="Payment Reminder Email Generator: Overdue Invoice Templates by Days Late",
    desc="Free payment reminder email generator. Enter the client, invoice and due date and get the right reminder for how late it is, from a friendly nudge to a final notice, ready to copy.",
    h1="Payment reminder email generator",
    lead="Fill in the invoice and its due date. The generator picks the right email for how late the payment is, from a polite heads-up before the due date to a final notice, fills in the amounts and dates, and lets you copy it in one click.",
    form="""      <label for="client">Client name</label>
      <div class="in"><input id="client" type="text" value="Northfield Dental"></div>
      <label for="inv">Invoice number</label>
      <div class="in"><input id="inv" type="text" value="1042"></div>
      <label for="amt">Invoice amount</label>
      <div class="in"><span>$</span><input id="amt" type="number" inputmode="decimal" min="0" step="0.01" value="2400"></div>
      <label for="due">Due date</label>
      <div class="in"><input id="due" type="date"></div>
      <label for="stage">Email</label>
      <select id="stage" class="full"><option value="auto">Pick for me by days late</option><option value="0">1. Before due (3 days before the due date)</option><option value="1">2. Due today (On the due date)</option><option value="2">3. Friendly overdue (1 to 6 days late)</option><option value="3">4. Firm overdue (7 to 13 days late)</option><option value="4">5. Fee added (14 to 29 days late)</option><option value="5">6. Final notice (30 to 44 days late)</option><option value="6">7. Letter before action (45+ days late)</option></select>
      <label for="me">Your name</label>
      <div class="in"><input id="me" type="text" placeholder="Your name"></div>
      <label for="pay">Payment link or bank details</label>
      <div class="in"><input id="pay" type="text" placeholder="https://..."></div>
      <details><summary class="note">Late fee and final step</summary>
      <label for="rate">Late fee per month <small>(% of the balance, 0 for none)</small></label>
      <div class="in"><input id="rate" type="number" min="0" step="0.1" value="1.5"><span>%</span></div>
      <label for="flat">Flat late fee <small>(added from 14 days late)</small></label>
      <div class="in"><span>$</span><input id="flat" type="number" min="0" step="1" value="25"></div>
      <label for="pd">Days to pay in the email</label>
      <div class="in"><input id="pd" type="number" min="1" step="1" value="7"><span>days</span></div>
      <label for="act">Your final step <small>(only what you will really do)</small></label>
      <div class="in"><input id="act" type="text" value="pass the debt to a collection agency"></div>
      </details>""",
    out="""<div class="big"><span>Email to send</span><b id="big" style="font-size:1.3rem"></b></div>
      <p class="note" id="when"></p>
      <label>Subject</label>
      <p id="subj" style="background:#fff;border:1px solid var(--line);border-radius:8px;padding:10px;margin:0"></p>
      <label>Email</label>
      <pre id="body" style="white-space:pre-wrap;font:inherit;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px;margin:0"></pre>
      <p><button id="copy" type="button" class="btn" style="border:0;cursor:pointer;font:inherit;font-weight:700">Copy subject and email</button></p>""",
    js="""var T=[{"n": "Before due", "w": "3 days before the due date", "s": "Invoice {invoice} due {due}", "b": "Hi {client},\\n\\nA quick heads-up that invoice {invoice} for {amount} is due on {due}. You can pay here: {paylink}\\n\\nIf anything on the invoice needs changing, tell me now and I'll fix it before the due date.\\n\\nThanks,\\n{me}"}, {"n": "Due today", "w": "On the due date", "s": "Invoice {invoice} is due today", "b": "Hi {client},\\n\\nInvoice {invoice} for {amount} is due today. Payment link: {paylink}\\n\\nIf it's already on its way, thank you, and please ignore this email.\\n\\n{me}"}, {"n": "Friendly overdue", "w": "1 to 6 days late", "s": "Invoice {invoice} is now overdue", "b": "Hi {client},\\n\\nI haven't seen payment for invoice {invoice} ({amount}), which was due on {due}. It's easy to miss, so here's the link again: {paylink}\\n\\nCould you let me know the date it will be paid?\\n\\nThanks,\\n{me}"}, {"n": "Firm overdue", "w": "7 to 13 days late", "s": "Overdue: invoice {invoice}, {days} days past due", "b": "Hi {client},\\n\\nInvoice {invoice} for {amount} is now {days} days past its due date of {due}.\\n\\nUnder our payment terms a late fee applies to overdue balances, and it grows each day the invoice stays unpaid. Please pay by {deadline} to keep it small: {paylink}\\n\\nIf there's a problem with the invoice or the work, reply and tell me what it is so we can sort it out.\\n\\n{me}"}, {"n": "Fee added", "w": "14 to 29 days late", "s": "Second notice: invoice {invoice} is now {total}", "b": "Hi {client},\\n\\nInvoice {invoice} is {days} days overdue. Under our agreed terms a late fee of {fee} has been added, so the balance is now {total}.\\n\\nPlease reply with the date you will pay. If I don't hear back by {deadline}, I'll pause further work on your account until the balance is cleared.\\n\\nPay here: {paylink}\\n\\n{me}"}, {"n": "Final notice", "w": "30 to 44 days late", "s": "Final notice: invoice {invoice} ({total})", "b": "Hi {client},\\n\\nThis is a final notice for invoice {invoice}. It was due on {due} and is now {days} days overdue. The balance including late fees is {total}.\\n\\nPayment in full is needed by {deadline}. If it hasn't arrived by then, I will {action} to recover the balance.\\n\\nI would much rather settle this directly. If you can't pay in full, reply before {deadline} with a payment plan and I'll consider it.\\n\\nPay here: {paylink}\\n\\n{me}\\n{business}"}, {"n": "Letter before action", "w": "45+ days late", "s": "Letter before action: unpaid invoice {invoice}", "b": "Dear {client},\\n\\nRe: unpaid invoice {invoice}, balance {total}\\n\\nDespite earlier reminders, invoice {invoice}, due on {due}, is still unpaid {days} days after the due date. The amount now owed, including late fees under our agreed terms, is {total}.\\n\\nUnless payment in full is received by {deadline}, I intend to {action} without further notice. This may add costs to the amount you owe where the law allows.\\n\\nIf you dispute any part of this invoice, please set out your reasons in writing before {deadline}.\\n\\nPayment details: {paylink}\\n\\nYours sincerely,\\n{me}\\n{business}"}];
var STG=[[-3,0],[0,1],[1,2],[7,3],[14,4],[30,5],[45,6]];
var fmtD=function(d){return d.toLocaleDateString('en-US',{day:'numeric',month:'short',year:'numeric'})};
var today=new Date();today.setHours(0,0,0,0);
if(!$('due').value){var dd=new Date(today.getTime()-10*864e5);$('due').value=dd.getFullYear()+'-'+('0'+(dd.getMonth()+1)).slice(-2)+'-'+('0'+dd.getDate()).slice(-2)}
var txt=function(id,ph){var v=$(id).value.trim();return v||'['+ph+']'};
function calc(){
  var due=$('due').value?new Date($('due').value+'T00:00:00'):today,d=Math.round((today-due)/864e5);
  var A=n('amt'),r=n('rate')/100,F=n('flat');
  var fee=Math.round(A*r*Math.max(0,d)/30*100)/100+(d>=14?F:0);
  var i=0;STG.forEach(function(s){if(d>=s[0])i=s[1]});
  if($('stage').value!=='auto')i=+$('stage').value;
  var t=T[i],v={client:txt('client','Client name'),invoice:txt('inv','Invoice #'),amount:m(A),due:fmtD(due),days:String(Math.max(0,d)),
    fee:m(fee),total:m(A+fee),deadline:fmtD(new Date(today.getTime()+Math.max(1,Math.floor(n('pd')||7))*864e5)),
    paylink:txt('pay','Payment link'),action:txt('act','your next step'),me:txt('me','Your name'),business:''};
  var fill=function(s){return s.replace(/\\{(\\w+)\\}/g,function(_,k){return v[k]}).replace(/\\n\\n\\n+/g,'\\n\\n').replace(/\\n+$/,'')};
  $('big').textContent=(i+1)+'. '+t.n;
  $('when').textContent='Send: '+t.w+'. '+(d>0?'This invoice is '+d+' day'+(d==1?'':'s')+' late':d==0?'This invoice is due today':'This invoice is due in '+(-d)+' day'+(d==-1?'':'s'))+(fee>0&&i>=3?'; late fee so far '+m(fee)+'.':'.');
  $('subj').textContent=fill(t.s);
  $('body').textContent=fill(t.b);
}
$('copy').addEventListener('click',function(){var s='Subject: '+$('subj').textContent+'\\n\\n'+$('body').textContent;
  (navigator.clipboard?navigator.clipboard.writeText(s):Promise.reject()).then(function(){$('copy').textContent='Copied'},function(){window.prompt('Copy this email:',s)});
  setTimeout(function(){$('copy').textContent='Copy subject and email'},2000)});""",
    note="The email is suggested by days past the due date: 3 days before, on the day, 1 to 6, 7 to 13, 14 to 29, 30 to 44 and 45+ days late. Late fees are simple interest pro-rated daily, plus the flat fee from 14 days late; only charge them if your client agreed to them in advance. Nothing you type leaves your browser. Templates, not legal advice.",
    body="""<h2>The reminder sequence that gets invoices paid</h2>
<p>Most late invoices aren't refused, they're forgotten. A short, regular sequence of emails that gets a little firmer each time, and always asks for a specific payment date, gets most of them paid without a single awkward call.</p>
<table class="wide"><thead><tr><th>When</th><th>Email</th><th>What it does</th></tr></thead><tbody>
<tr><td>3 days before due</td><td>Before due</td><td>Heads-up with the payment link; catches invoice problems early</td></tr>
<tr><td>Due date</td><td>Due today</td><td>Neutral reminder</td></tr>
<tr><td>1 to 6 days late</td><td>Friendly overdue</td><td>Assumes it was missed; asks for a date</td></tr>
<tr><td>7 to 13 days late</td><td>Firm overdue</td><td>Mentions the late fee in your terms</td></tr>
<tr><td>14 to 29 days late</td><td>Fee added</td><td>States the new balance; work pauses if no reply</td></tr>
<tr><td>30 to 44 days late</td><td>Final notice</td><td>Names a deadline and your next step</td></tr>
<tr><td>45+ days late</td><td>Letter before action</td><td>Formal last warning before collection or court</td></tr>
</tbody></table>
<h2>Rules for chasing a late payment</h2>
<p><strong>Ask for a date.</strong> "When will this be paid?" gets a commitment. "Just checking in" gets ignored.</p>
<p><strong>Reply in the same thread</strong> so the client sees every earlier reminder.</p>
<p><strong>Find the person who pays.</strong> From the third email, ask who handles invoices and copy them in.</p>
<p><strong>Only name a consequence you will carry out.</strong> If you say work pauses at 14 days, pause it. Empty threats teach clients to wait.</p>
<p><strong>Stay polite, even in the final notice.</strong> If the debt ever goes to an agency or small claims court, these emails are your evidence.</p>
<p>To see what the late fee comes to, use the <a href="../invoice-late-fee-calculator/">invoice late fee calculator</a>.</p>""",
    faqs=[
        ("How do I politely remind a client to pay an invoice?", "Keep it short: the invoice number, amount, due date and payment link, then ask the date it will be paid. For the first overdue reminder, assume it was missed rather than ignored."),
        ("How many reminders should I send for an unpaid invoice?", "Usually five to seven: before the due date, on it, then at about 3, 7, 14, 30 and 45 days late. Each one gets firmer and the last two name a deadline and what you will do next."),
        ("What should a final notice for an unpaid invoice say?", "The invoice number, the original due date, the balance including any agreed late fees, a final date to pay, and the step you will take if it isn't paid, such as passing it to a collection agency."),
        ("Can I add a late fee to a reminder email?", "Only if the client agreed to it before the work started, usually in your contract or on the invoice. If they did, state the fee and the new balance from about 14 days late."),
    ],
    related=["invoice-late-fee-calculator", "paypal-fee-calculator", "stripe-fee-calculator", "profit-margin-calculator", "break-even-calculator"],
    cta_head="Never write a chaser from scratch again",
    cta_text="The <strong>Invoice Tracker Template Google Sheets + Excel, Payment Reminder Email Templates (Word + PDF)</strong> has all 10 emails (these 7 plus replies for &ldquo;we'll pay next week&rdquo;, a payment plan offer and a thank-you), payment terms and a late fee policy to add before the next project, and the <strong>Invoice Chaser</strong> spreadsheet that tracks every invoice, works out late fees, flags who to chase today and writes each email for you. Word, Google Docs, Excel and Google Sheets. One-time $9.",
    cta_url="https://quietprofitsheets.gumroad.com/l/get-paid-kit",
    cta_btn="Get the Invoice Tracker Template",
    tests=[
        {"expect": {"big": "4. Firm overdue", "subj": "Overdue: invoice 1042, 10 days past due", "body": ["Hi Northfield Dental", "$2,400.00", "late fee"], "when": "10 days late"}},
        {"set": {"due": "2020-01-01"}, "expect": {"big": "7. Letter before action", "body": ["Dear Northfield Dental", "collection agency", "[Your name]"]}},
        {"set": {"stage": "1"}, "expect": {"subj": "is due today"}},
        {"set": {"client": "", "me": "Sam Lee"}, "expect": {"body": ["[Client name]", "Sam Lee"]}},
        {"set": {"due": "2099-01-01"}, "expect": {"big": "1. Before due", "when": "due in"}},
        {"set": {"stage": "4"}, "expect": {"subj": "is now $2,412.00", "big": "5. Fee added"}},
    ],
)
