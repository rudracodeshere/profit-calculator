PAGE = dict(
    slug="invoice-late-fee-calculator",
    cat="Invoices & getting paid",
    nav_name="Invoice late fee calculator",
    title="Invoice Late Fee Calculator: Monthly % Plus Flat Fee, by Days Late",
    desc="Free invoice late fee calculator. Enter the invoice amount, days overdue, monthly late fee % and any flat fee to see the fee, the new balance and the wording for your invoice.",
    h1="Invoice late fee calculator",
    lead="Enter an unpaid invoice, how many days late it is, and the late fee in your terms. You get the fee to add, the new balance, what each extra day costs the client, and a line of wording to put on your invoices.",
    form="""      <label for="amt">Invoice amount</label>
      <div class="in"><span>$</span><input id="amt" type="number" inputmode="decimal" min="0" step="0.01" value="2400"></div>
      <label for="days">Days past the due date</label>
      <div class="in"><input id="days" type="number" inputmode="numeric" min="0" step="1" value="45"><span>days</span></div>
      <label for="rate">Late fee per month <small>(% of the unpaid balance)</small></label>
      <div class="in"><input id="rate" type="number" inputmode="decimal" min="0" step="0.1" value="1.5"><span>%</span></div>
      <label for="flat">Flat late fee <small>(one-time, 0 for none)</small></label>
      <div class="in"><span>$</span><input id="flat" type="number" inputmode="decimal" min="0" step="1" value="25"></div>
      <label for="grace">Grace period <small>(days before the % fee starts)</small></label>
      <div class="in"><input id="grace" type="number" inputmode="numeric" min="0" step="1" value="0"><span>days</span></div>""",
    out="""<div class="big"><span>Late fee to add</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>
      <h3>Wording for your invoices</h3>
      <p id="clause" class="formula" style="font-weight:400"></p>""",
    js="""function calc(){
  var A=n('amt'),d=Math.floor(n('days')),r=n('rate')/100,F=n('flat'),g=Math.floor(n('grace'));
  if(!A){$('big').textContent='-';setRows([]);verdict(false,'Enter the invoice amount to see the late fee.');$('clause').textContent='';return}
  var cd=Math.max(0,d-g),pct=Math.round(A*r*cd/30*100)/100,flat=d>0?F:0,fee=pct+flat,daily=A*r/30;
  $('big').textContent=m(fee);
  setRows([['Invoice amount',m(A)],['Days late',d],['Days the % fee applies',cd],[pc(r,2)+' a month, pro-rated daily',m(pct)],['Flat late fee',m(flat)],
    ['Total late fee',m(fee)],['Balance now owed',m(A+fee),'total'],['Each extra day adds',m(daily)],['Equal to a yearly rate of',pc(r*12)]]);
  if(!d)verdict(true,'This invoice is not overdue yet, so no late fee applies. A short reminder 3 days before the due date gets many invoices paid on time.');
  else verdict(fee<=A*0.1,'At '+d+' days late, the client owes '+m(A+fee)+': '+m(A)+' plus a '+m(fee)+' late fee. Every further day adds '+m(daily)+'.'+(fee>A*0.1?' The fee is now over 10% of the invoice, which a court or the client may see as a penalty; check your local limit.':''));
  $('clause').textContent='Payment is due within 14 days of the invoice date. Late payments incur '+(r?(+(r*100).toFixed(2))+'% per month on the unpaid balance, calculated daily from '+(g?g+' days after ':'')+'the due date':'no interest')+(F?', plus a one-time late fee of '+m(F):'')+', per our agreed terms.';
}""",
    note="The % fee is simple interest, pro-rated daily on a 30-day month: amount x monthly rate x days / 30. The flat fee is added once the invoice is a day late. A late fee is only enforceable if the client agreed to it before the work started, and many US states cap the rate; in the UK, business invoices can carry statutory interest of 8% a year above the Bank of England base rate instead. This is math, not legal advice.",
    body="""<h2>How the late fee is worked out</h2>
<p>Most freelancers and small businesses charge a late fee as a monthly percentage of the unpaid balance, often <strong>1.5% a month</strong> (18% a year), sometimes with a small flat fee on top. Charging it daily from the due date means the client pays for exactly how late they are, and it gives them a reason to pay today instead of next week.</p>
<p class="formula">Late fee = invoice amount x monthly rate x days late / 30 + flat fee</p>
<h2>Worked example</h2>
<p>A <strong>$2,400</strong> invoice is <strong>45 days</strong> late. Your terms say 1.5% a month plus a $25 late fee. The percentage part is 2,400 x 0.015 x 45 / 30 = <strong>$54.00</strong>. Add the $25 flat fee and the late fee is <strong>$79.00</strong>, so the client now owes <strong>$2,479.00</strong>. Each extra day adds 2,400 x 0.015 / 30 = <strong>$1.20</strong>.</p>
<p>With a 15-day grace period the percentage only runs for 30 days: 2,400 x 0.015 x 30 / 30 = $36.00, or $61.00 with the flat fee.</p>
<h2>Making a late fee stick</h2>
<p>The fee has to be agreed before the work starts. Put it in your contract or proposal, print the wording above on every invoice, and mention it in your reminders from the first overdue email. A fee you add without warning is easy for a client to refuse, and it sours the relationship.</p>
<p>Keep the rate reasonable. In the US the legal maximum depends on your state; some cap late fees or interest well below 18% a year. In the UK, business-to-business invoices carry statutory interest of 8% a year over the Bank of England base rate, plus fixed compensation of &pound;40, &pound;70 or &pound;100 depending on the debt, even if your contract says nothing. In the EU, the Late Payment Directive sets interest at least 8 points over the ECB reference rate plus &euro;40.</p>
<p>The fee is a nudge, not the plan. What gets most invoices paid is a steady sequence of short, polite emails that ask for a specific payment date. The <a href="../payment-reminder-email-generator/">payment reminder email generator</a> writes the right one for how late the invoice is.</p>""",
    faqs=[
        ("What is a normal late fee on an invoice?", "1% to 1.5% a month on the unpaid balance is common, often with a flat fee of $25 to $50. On a $2,400 invoice 45 days late, 1.5% a month comes to $54.00."),
        ("Can I charge a late fee if it wasn't in my contract?", "Usually not in the US, unless the client agrees to it. In the UK, business invoices carry statutory interest and fixed compensation even without a clause. Add the fee to your terms before the next project."),
        ("Is 1.5% a month the same as 18% a year?", "Yes, as simple interest: 1.5% x 12 = 18%. This calculator charges it daily, so 45 days at 1.5% a month is 2.25% of the invoice."),
        ("When should the late fee start?", "The day after the due date, unless your terms give a grace period. A short grace period of 5 to 7 days avoids charging clients whose payment is already in transit."),
    ],
    related=["payment-reminder-email-generator", "paypal-fee-calculator", "stripe-fee-calculator", "break-even-calculator", "profit-margin-calculator"],
    cta_head="Stop writing awkward payment chasers",
    cta_text="The <strong>Get Paid Kit</strong> has 10 ready-to-send emails from the friendly reminder to the letter before action, payment terms and a late fee policy to add before the work starts, and the <strong>Invoice Chaser</strong> spreadsheet: it tracks every invoice, works out late fees, tells you who to chase today and writes the email with the client's name, amounts and dates filled in. Word, Google Docs, Excel and Google Sheets. One-time $9.",
    cta_url="https://quietprofitsheets.gumroad.com/l/get-paid-kit",
    cta_btn="Get the Get Paid Kit",
    tests=[
        {"expect": {"big": "$79.00", "rows": ["$54.00", "$25.00", "$2,479.00", "$1.20", "18.0%"], "verdict": ["45 days late", "$2,479.00"],
                    "clause": ["1.5% per month", "$25.00"]}},
        {"set": {"grace": "15"}, "expect": {"big": "$61.00", "rows": ["$36.00", "30"], "clause": "15 days after"}},
        {"set": {"days": "0"}, "expect": {"big": "$0.00", "verdict": "not overdue"}},
        {"set": {"amt": "0"}, "expect": {"big": "-", "verdict": "Enter the invoice amount"}},
        {"set": {"amt": "300", "days": "90"}, "expect": {"big": "$38.50", "verdict": "over 10%"}},
        {"set": {"rate": "0", "flat": "40"}, "expect": {"big": "$40.00", "clause": "no interest"}},
    ],
)
