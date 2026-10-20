PAGE = dict(
    slug="invoice-due-date-calculator",
    cat="Invoices & getting paid",
    nav_name="Invoice due date (Net 30) calculator",
    title="Invoice Due Date Calculator: Net 30, Net 60 and 2/10 Net 30 With Dates",
    desc="Free invoice due date calculator. Enter the invoice date and terms like Net 30, Net 60 or 2/10 Net 30 to get the exact due date, the early payment discount date and how many days are left or overdue.",
    h1="Invoice due date calculator (Net 30)",
    lead="Enter the invoice date and your payment terms. You get the exact due date, how many days are left or how late it is, and, for terms like 2/10 Net 30, the last day for the early payment discount and what it's worth.",
    form="""      <label for="inv">Invoice date</label>
      <input id="inv" type="date">
      <label for="net">Payment terms <small>(Net days, 0 for due on receipt)</small></label>
      <div class="in"><span>Net</span><input id="net" type="number" inputmode="numeric" min="0" step="1" value="30"><span>days</span></div>
      <label for="from">Count the days from</label>
      <select id="from"><option value="inv" selected>The invoice date</option><option value="eom">The end of the invoice month (EOM)</option></select>
      <label for="wknd">If the due date lands on a weekend</label>
      <select id="wknd"><option value="keep" selected>Keep that date</option><option value="mon">Move it to Monday</option></select>
      <label for="amt">Invoice amount</label>
      <div class="in"><span>$</span><input id="amt" type="number" inputmode="decimal" min="0" step="0.01" value="2400"></div>
      <label for="disc">Early payment discount <small>(the 2 in 2/10 Net 30, 0 for none)</small></label>
      <div class="in"><input id="disc" type="number" inputmode="decimal" min="0" step="0.5" value="0"><span>%</span></div>
      <label for="ddays">Discount period <small>(the 10 in 2/10 Net 30)</small></label>
      <div class="in"><input id="ddays" type="number" inputmode="numeric" min="0" step="1" value="10"><span>days</span></div>
      <label for="today">Today</label>
      <input id="today" type="date">""",
    out="""<div class="big"><span>Payment is due</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""var MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],DN=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
function dt(s){var p=s.split('-');return new Date(Date.UTC(+p[0],+p[1]-1,+p[2]))}
function iso(d){return d.toISOString().slice(0,10)}
function f(d){return DN[d.getUTCDay()]+', '+MON[d.getUTCMonth()]+' '+d.getUTCDate()}
function add(d,k){var x=new Date(d.getTime());x.setUTCDate(x.getUTCDate()+k);return x}
(function(){var t=new Date(),td=iso(new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate())));
  if(!$('today').value)$('today').value=td;if(!$('inv').value)$('inv').value=td;})();
function calc(){
  if(!$('inv').value){$('big').textContent='-';setRows([]);verdict(false,'Pick the invoice date to see when it is due.');return}
  var inv=dt($('inv').value),N=Math.floor(n('net')),eom=$('from').value=='eom',
      start=eom?new Date(Date.UTC(inv.getUTCFullYear(),inv.getUTCMonth()+1,0)):inv,due=add(start,N),moved=false;
  if($('wknd').value=='mon'&&(due.getUTCDay()==6||due.getUTCDay()==0)){due=add(due,due.getUTCDay()==6?2:1);moved=true}
  var A=n('amt'),r=n('disc')/100,dd=Math.floor(n('ddays'));
  $('big').textContent=f(due)+', '+due.getUTCFullYear();
  var terms=(r&&dd?(+(r*100).toFixed(2))+'/'+dd+' ':'')+(N?'Net '+N:'Due on receipt')+(eom?' EOM':'');
  var rows=[['Invoice date',f(inv)],['Terms',terms],['Due date',f(due)+(moved?' (moved off the weekend)':''),'total']];
  var dl=null;
  if(r&&dd&&dd<N){dl=add(start,dd);rows.push(['Last day for the '+pc(r,r*100%1?1:0)+' discount',f(dl)]);
    if(A)rows.push(['Discount if paid by then',m(A*r)],['Pay early and send',m(A*(1-r))]);
    rows.push(['Discount as a yearly rate',pc(r/(1-r)*365/(N-dd))])}
  var today=$('today').value?dt($('today').value):null,diff=today?Math.round((due-today)/864e5):null;
  if(today)rows.push([diff<0?'Days overdue':'Days until due',Math.abs(diff)]);
  setRows(rows);
  if(diff===null)verdict(true,'Payment on this invoice is due '+f(due)+', '+due.getUTCFullYear()+'.');
  else if(diff<0)verdict(false,'This invoice is '+(-diff)+(diff==-1?' day':' days')+' overdue. It was due '+f(due)+'. Send a short reminder that asks for a payment date, and add a late fee only if your terms include one.');
  else if(diff==0)verdict(true,'This invoice is due today, '+f(due)+'.');
  else verdict(true,'Due '+f(due)+', in '+diff+(diff==1?' day':' days')+'.'+(dl&&today<=dl?' Paid by '+f(dl)+', the client keeps '+m(A*r)+'.':''));
}""",
    note="Net terms count calendar days, weekends and holidays included: Net 30 on Oct 21 is due Nov 20. EOM counts from the last day of the invoice month. The yearly rate of a discount is discount / (1 - discount) x 365 / (net days - discount days). What counts as the due date is whatever your contract says; this is a date calculator, not legal advice.",
    body="""<h2>How Net 30 is worked out</h2>
<p><strong>Net 30</strong> means the full amount is due 30 calendar days after the invoice date. Count every day, weekends and holidays included, and start counting the day after the invoice date. Net 15, Net 45, Net 60 and Net 90 work the same way with a different number.</p>
<p class="formula">Due date = invoice date + net days</p>
<p><strong>EOM</strong> (end of month) terms start the count from the last day of the month the invoice was sent. <strong>Net 30 EOM</strong> on an invoice dated Oct 21 is due 30 days after Oct 31: Mon, Nov 30.</p>
<p><strong>Due on receipt</strong> means pay now. In practice most clients treat it as within a few days, so if you want it paid fast, say a date.</p>
<h2>Worked examples</h2>
<p><strong>Net 30.</strong> An invoice dated Wed, Oct 21, 2026 is due <strong>Fri, Nov 20, 2026</strong>. On Dec 5 it's 15 days overdue.</p>
<p><strong>Net 60.</strong> The same invoice is due Sun, Dec 20. If your terms move weekend dates to the next business day, it's due <strong>Mon, Dec 21</strong>.</p>
<p><strong>2/10 Net 30.</strong> A $2,400 invoice dated Oct 21: the client can take 2% off if they pay by <strong>Sat, Oct 31</strong>, sending $2,352 instead of $2,400 and keeping $48. Otherwise the full $2,400 is due Fri, Nov 20.</p>
<h2>Is a 2/10 Net 30 discount worth offering?</h2>
<p>The discount looks small, but the client is being paid 2% to pay 20 days sooner. As a yearly rate that's 0.02 / 0.98 x 365 / 20 = <strong>37.2%</strong>. That's why big companies take it whenever they can, and why it's an expensive way for a small business to get paid. Offer it only if waiting the extra 20 days costs you more, say because you're paying interest on a credit line to cover the gap.</p>
<p class="formula">Yearly rate = discount / (1 - discount) x 365 / (net days - discount days)</p>
<h2>When the due date passes</h2>
<p>Most late payments are forgotten, not refused. Put the due date on the invoice itself ("Due Fri, Nov 20, 2026", not just "Net 30"), send a friendly reminder a few days before it, and follow up the day after it passes with a request for a specific payment date. The <a href="../payment-reminder-email-generator/">payment reminder email generator</a> writes each of those emails, and the <a href="../invoice-late-fee-calculator/">invoice late fee calculator</a> works out the fee if your terms include one.</p>""",
    faqs=[
        ("How do you calculate Net 30?", "Add 30 calendar days to the invoice date. Weekends and holidays count. An invoice dated Oct 21, 2026 is due Nov 20, 2026."),
        ("Does Net 30 include weekends?", "Yes. Net terms count calendar days, not business days. Some contracts move a weekend due date to the next business day; pick that option above if yours does."),
        ("What does 2/10 Net 30 mean?", "The client can take 2% off if they pay within 10 days. Otherwise the full amount is due in 30 days. On a $2,400 invoice that's $2,352 by day 10 or $2,400 by day 30."),
        ("What does Net 30 EOM mean?", "The 30 days start at the end of the month the invoice was sent. An invoice dated Oct 21 with Net 30 EOM is due Nov 30."),
        ("Is Net 30 from the invoice date or the date it was received?", "From the invoice date, unless your contract says otherwise. Send invoices the day the work is done so the clock starts right away."),
    ],
    related=["invoice-late-fee-calculator", "payment-reminder-email-generator", "stripe-fee-calculator", "paypal-fee-calculator", "break-even-calculator"],
    cta_head="Know which invoices are due without counting days",
    cta_text="The <strong>Invoice Tracker Template Google Sheets + Excel, Payment Reminder Email Templates (Word + PDF)</strong> includes the <strong>Invoice Chaser</strong> spreadsheet: it tracks every invoice and its due date, works out late fees, tells you who to chase today and writes the email with the client's name, amounts and dates filled in. It also has 10 ready-to-send reminder emails and payment terms to add before the work starts. Word, Google Docs, Excel and Google Sheets. One-time $9.",
    cta_url="https://quietprofitsheets.gumroad.com/l/get-paid-kit",
    cta_btn="Get the Invoice Tracker Template",
    tests=[
        {"set": {"inv": "2026-10-21", "today": "2026-10-21"}, "expect": {"big": "Fri, Nov 20, 2026", "rows": ["Wed, Oct 21", "Net 30", "30"], "verdict": "in 30 days"}},
        {"set": {"inv": "2026-10-21", "today": "2026-12-05"}, "expect": {"rows": "Days overdue", "verdict": "15 days overdue"}},
        {"set": {"inv": "2026-10-21", "today": "2026-10-21", "from": "eom"}, "expect": {"big": "Mon, Nov 30, 2026", "rows": "Net 30 EOM"}},
        {"set": {"inv": "2026-10-21", "today": "2026-10-21", "net": "60"}, "expect": {"big": "Sun, Dec 20, 2026"}},
        {"set": {"inv": "2026-10-21", "today": "2026-10-21", "net": "60", "wknd": "mon"}, "expect": {"big": "Mon, Dec 21, 2026", "rows": "moved off the weekend"}},
        {"set": {"inv": "2026-10-21", "today": "2026-10-21", "disc": "2"}, "expect": {"big": "Fri, Nov 20, 2026", "rows": ["2/10 Net 30", "Sat, Oct 31", "$48.00", "$2,352.00", "37.2%"], "verdict": "keeps $48.00"}},
        {"set": {"inv": "2026-10-21", "today": "2026-10-21", "net": "0"}, "expect": {"big": "Wed, Oct 21, 2026", "rows": "Due on receipt", "verdict": "due today"}},
        {"set": {"inv": "2026-01-15", "today": "2026-01-15", "net": "45"}, "expect": {"big": "Sun, Mar 1, 2026"}},
    ],
)
