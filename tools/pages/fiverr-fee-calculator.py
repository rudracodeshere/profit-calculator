PAGE = dict(
    slug="fiverr-fee-calculator",
    cat="Platform fees",
    nav_name="Fiverr fee calculator",
    gig="sheet",
    title="Fiverr Fee Calculator 2026: Seller Earnings, Buyer Service Fee and Withdrawals",
    desc="Free Fiverr fee calculator for sellers and buyers: Fiverr's 20% cut, the 5.5% + $3.50 buyer service fee, tips, early payout and withdrawal fees, and what you take home.",
    h1="Fiverr fee calculator",
    lead="Enter a gig price. See what Fiverr keeps, what lands in your account and what the buyer is charged at checkout. Add a tip, an extra bought later or your payout method to see the full picture.",
    form="""      <label for="gig">Gig price <small>(package plus any extras bought at checkout)</small></label>
      <div class="in"><span>$</span><input id="gig" type="number" inputmode="decimal" min="0" step="0.01" value="50"></div>
      <label for="later">Extras added after the order started <small>(a separate payment)</small></label>
      <div class="in"><span>$</span><input id="later" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
      <label for="tip">Tip from the buyer <small>(a separate payment, minimum $5)</small></label>
      <div class="in"><span>$</span><input id="tip" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
      <label for="wd">Withdrawal fee <small>(PayPal $0, Payoneer USD wire $1, local bank transfer or Payoneer account $3; charged per withdrawal)</small></label>
      <div class="in"><span>$</span><input id="wd" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
      <label class="check"><input id="early" type="checkbox"> I use early payout (Top Rated or Seller Plus Premium, 1% of earnings)</label>
      <label for="want">Take-home you want from one order <small>(optional, to find the price)</small></label>
      <div class="in"><span>$</span><input id="want" type="number" inputmode="decimal" min="0" step="0.01" value="" placeholder="e.g. 100"></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="com">Fiverr commission on gigs, extras and tips</label>
      <div class="in"><input id="com" type="number" min="0" step="0.1" value="20"><span>%</span></div>
      <label for="sf">Buyer service fee</label>
      <div class="in"><input id="sf" type="number" min="0" step="0.1" value="5.5"><span>%</span></div>
      <label for="flat">Small order fee, per payment</label>
      <div class="in"><span>$</span><input id="flat" type="number" min="0" step="0.01" value="3.50"></div>
      <label for="thr">Small order fee applies to payments under</label>
      <div class="in"><span>$</span><input id="thr" type="number" min="0" step="1" value="200"></div>
      <label for="ep">Early payout fee <small>(% of earnings)</small></label>
      <div class="in"><input id="ep" type="number" min="0" step="0.1" value="1"><span>%</span></div>
      </details>""",
    out="""<div class="big"><span>You receive</span><b id="keep"></b></div>
      <div class="big"><span>Buyer pays at checkout</span><b id="buyer"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>
      <p id="need" class="formula" style="font-weight:400;margin:12px 0 0;display:none"></p>""",
    js="""function calc(){
  var g=n('gig'),x=n('later'),t=n('tip'),wd=n('wd'),c=n('com')/100,ep=$('early').checked?n('ep')/100:0;
  var pct=function(p){return p>0?Math.round(p*n('sf'))/100:0};
  var sm=function(p){return p>0&&p<n('thr')?n('flat'):0};
  var fee=function(p){return pct(p)+sm(p)};
  var want=n('want'),d=(1-c)*(1-ep),need=$('need');
  if(want&&d>0){need.style.display='';need.innerHTML='To take home <b>'+m(want)+'</b> from one order'+(wd?' after a '+m(wd)+' withdrawal fee':'')+', price the gig at <b>'+m(Math.ceil((want+wd)/d*100-1e-6)/100)+'</b>.'}
  else need.style.display='none';
  var sale=g+x+t;
  if(!sale){$('keep').textContent=m(0);$('buyer').textContent=m(0);setRows([["Enter a gig price to see Fiverr's fees.",'']]);verdict(false,'No order entered yet.');return}
  var bf=fee(g)+fee(x)+fee(t),buy=sale+bf,com=sale*c,earn=sale-com,ef=earn*ep,rec=earn-ef-wd,fk=com+bf+ef;
  var r=[['Gig price',m(g)]];
  if(x)r.push(['Extras added later',m(x)]);
  if(t)r.push(['Tip',m(t)]);
  if(g){r.push(['Buyer service fee ('+n('sf')+'% of '+m(g)+')',m(pct(g))]);if(sm(g))r.push(['Small order fee (payment under '+m(n('thr'))+')',m(sm(g))])}
  if(x)r.push(['Service fee on the later extras',m(fee(x))]);
  if(t)r.push(['Service fee on the tip',m(fee(t))]);
  r.push(['Buyer pays, before sales tax or VAT',m(buy)]);
  r.push(["Fiverr's "+n('com')+'% commission',m(-com)],['Your earnings ('+(+(100-n('com')).toFixed(2))+'%)',m(earn)]);
  if(ef)r.push(['Early payout fee ('+n('ep')+'% of earnings)',m(-ef)]);
  if(wd)r.push(['Withdrawal fee',m(-wd)]);
  r.push(['Fiverr keeps in total, '+pc(fk/buy)+' of what the buyer pays',m(fk)],['You receive',m(rec),'total']);
  setRows(r);$('keep').textContent=m(rec);$('buyer').textContent=m(buy);
  if(rec<=0)verdict(false,'You receive nothing from this order after fees.'+(wd?' Let your balance build up and withdraw several orders at once, so the '+m(wd)+' withdrawal fee is paid once.':''));
  else verdict(true,'Fiverr keeps '+m(fk)+' of the '+m(buy)+' the buyer pays ('+pc(fk/buy)+'). You get '+m(rec)+'.'+(bf?" The buyer's service fees add "+pc(bf/sale)+' on top of your price.':''));
}""",
    note="""Rates from Fiverr's <a href="https://www.fiverr.com/legal-portal/legal-terms/payment-terms-of-service" rel="noopener">Payment Terms</a> (last updated September 2026: sellers earn 80% of the purchase amount; buyers pay 5.5% plus a $3.50 small order fee on purchases under $200) and the Fiverr Help Center, all checked October 20, 2026: <a href="https://help.fiverr.com/hc/en-us/articles/9234443621137-Your-earnings-page" rel="noopener">Your earnings page</a> (sellers earn 80% of every order, Gig Extras and tips included), <a href="https://help.fiverr.com/hc/en-us/articles/360050216133-Paying-for-orders-extras-or-custom-offers" rel="noopener">Paying for orders, extras, or custom offers</a> (buyer service fee 5.5% plus $3.50 on orders under $200, charged on each payment), <a href="https://help.fiverr.com/hc/en-us/articles/360049982453-Tipping-your-freelancer" rel="noopener">Tipping your freelancer</a>, <a href="https://help.fiverr.com/hc/en-us/articles/360010530058-Withdrawing-your-earnings-managing-payout-methods" rel="noopener">Withdrawing your earnings</a>, <a href="https://help.fiverr.com/hc/en-us/articles/14257019400465-Setting-up-Payoneer-as-a-payout-method" rel="noopener">Setting up Payoneer</a> and <a href="https://help.fiverr.com/hc/en-us/articles/4402267122449-Early-Payout" rel="noopener">Early Payout</a> (1% of earnings). Fiverr's own pages disagree in two places: the help article "How Fiverr works for clients" still says $3.00 on orders under $100, and the withdrawal article lists $1 for a bank transfer via Payoneer where the Payoneer article and the Payment Terms list $3 for a local bank transfer. Check your checkout or payout screen and edit the rates if yours differ. Hourly contracts are billed differently (5.5% of the hourly rate plus a $5 order initiation fee), so this calculator is for Gig orders. Buyer totals leave out sales tax, VAT and currency conversion. In some regions buyers see an all-in price that already includes the service fee; that changes the display, not what you earn.""",
    body="""<h2>How Fiverr fees work</h2>
<p><strong>The seller's 20%.</strong> Fiverr keeps 20% of everything a buyer pays you: the gig package, Gig Extras and tips. You earn the other 80%. If you give a buyer a Seller Plus coupon or promotion, you earn 80% of the discounted price, so a 10% discount cuts your earnings by 10% too.</p>
<p><strong>The buyer's service fee.</strong> On top of your price, the buyer pays a service fee of 5.5%, plus $3.50 when the payment is under $200. Each payment is charged on its own: the order, an extra added after the order started, and a tip each get their own 5.5% fee, and their own $3.50 if that payment is under $200. That is why a $10 tip costs the buyer $14.05.</p>
<p><strong>Withdrawal and early payout.</strong> Fiverr charges nothing to withdraw to PayPal (minimum $1). Through Payoneer, a USD wire to your bank costs $1, a local-currency bank transfer $3 (minimum $20 for either), and a transfer to a Payoneer account $3 (minimum $10). The fee is per withdrawal, not per order, and you can withdraw up to $5,000 at a time. Top Rated sellers and Seller Plus Premium members who meet Fiverr's eligibility criteria can use early payout to clear earnings sooner, for 1% of the earnings cleared.</p>
<p><strong>Clearing.</strong> Earnings from a completed order clear over 14 days before you can withdraw them, and a tip clears on its own 14-day clock. Top Rated sellers wait 7 days, and Fiverr Pro sellers also get a shorter clearing period.</p>
<h2>The formula</h2>
<p class="formula">Buyer service fee = payment x 5.5% + $3.50 if that payment is under $200</p>
<p class="formula">You receive = (gig + extras + tip) x 80% - early payout fee - withdrawal fee</p>
<p class="formula">Gig price for a take-home target = (target + withdrawal fee) / 0.8 (or / 0.792 with early payout)</p>
<h2>Worked example</h2>
<p>A <strong>$50</strong> gig, no tip, withdrawn to PayPal. The buyer's service fee is $2.75 (5.5% of $50) plus the $3.50 small order fee, $6.25 in all, so the buyer pays <strong>$56.25</strong>. Fiverr's 20% commission is $10.00 and you receive <strong>$40.00</strong>. Fiverr keeps $16.25 altogether, 28.9% of what the buyer paid, and the buyer's fee alone adds 12.5% to your price.</p>
<p>The buyer then tips <strong>$10</strong>. The tip is a separate payment with its own fee: $0.55 plus $3.50, so $4.05. The buyer has now paid $70.30, you receive $48.00 and Fiverr keeps $22.30 (31.7%).</p>
<p>If instead the buyer adds a <strong>$20 extra</strong> after the order started, that is its own payment too, with a $4.60 fee ($1.10 + $3.50), and the buyer pays $80.85 in all. Had the extra been picked at checkout as part of one $70 order, the buyer's fees would have been $7.35 instead of $10.85.</p>
<p>A <strong>$250</strong> gig withdrawn to a Payoneer account ($3) with early payout: the buyer fee is $13.75 with no small order fee, so the buyer pays $263.75. Your 80% is $200.00, early payout takes $2.00 and the withdrawal $3.00, leaving <strong>$195.00</strong>.</p>
<p>Working backwards: to take home $100 from one order via PayPal without early payout, price the gig at $100 / 0.8 = <strong>$125.00</strong>.</p>
<h2>Pricing tips</h2>
<p>Start from what you want to keep and divide by 0.8. Then look at the buyer's side. Under $200 the $3.50 small order fee makes cheap gigs look expensive at checkout: a $10 gig costs the buyer $14.05, 40.5% more than your price, while a $200 gig costs $211.00, just 5.5% more. Packages that bundle the extras buyers usually want keep everything in one payment with one fee.</p>
<p>Coupons and promotions come out of your 80%, so a 10% coupon on a $50 gig cuts your earnings from $40.00 to $36.00. If your payout method charges a fee, let your balance build up and withdraw several orders at once.</p>""",
    faqs=[
        ("How much does Fiverr take from sellers?", "20% of every order, including Gig Extras and tips, so you earn 80%. A $50 gig pays you $40.00. Withdrawing to PayPal is free, while Payoneer charges $1 to $3 per withdrawal."),
        ("What service fee does the buyer pay on Fiverr?", "5.5% of each payment, plus $3.50 on payments under $200. A $50 order costs the buyer $56.25 and a $200 order $211.00. Fiverr's Payment Terms (updated September 2026) confirm these rates, but one help article still says $3.00 on orders under $100, so check the fee shown at checkout and edit the rates above if it differs."),
        ("Does Fiverr take a cut of tips?", "Yes. You earn 80% of a tip, and the buyer pays the standard service fee on it as a separate payment. A $10 tip costs the buyer $14.05 and pays you $8.00. The minimum tip is $5."),
        ("How much does it cost to withdraw money from Fiverr?", "PayPal is free (minimum $1). Bank transfer via Payoneer is $1 for a USD wire or $3 in local currency (minimum $20), and a Payoneer account is $3 (minimum $10). You can withdraw up to $5,000 at a time once earnings clear, after 14 days (7 for Top Rated sellers). Early payout, for Top Rated and Seller Plus Premium sellers, costs 1% of the earnings."),
    ],
    related=["paypal-fee-calculator", "stripe-fee-calculator", "invoice-late-fee-calculator", "payment-reminder-email-generator", "gumroad-fee-calculator", "profit-margin-calculator"],
    cta_head="Invoicing clients outside Fiverr too?",
    cta_text="Fiverr charges the buyer when the order is placed. Clients you invoice yourself pay when they get round to it. The <strong>Invoice Tracker Template Google Sheets + Excel, Payment Reminder Email Templates (Word + PDF)</strong> gives you the <strong>Invoice Chaser</strong> spreadsheet, which tracks every invoice, works out late fees, flags who to chase today and writes the email for you, plus 10 ready-to-send reminder emails and payment terms with a late fee policy to add before the work starts. Word, Google Docs, Excel and Google Sheets. One-time $9.",
    cta_url="https://quietprofitsheets.gumroad.com/l/get-paid-kit",
    cta_btn="Get the Invoice Tracker Template",
    tests=[
        {"expect": {"rows": ["$2.75", "$3.50", "$56.25", "-$10.00", "$40.00", "$16.25", "28.9%"], "keep": "$40.00", "buyer": "$56.25",
                    "verdict": ["28.9%", "12.5%"]}},
        {"set": {"tip": "10"}, "expect": {"rows": ["$4.05", "-$12.00", "$22.30", "31.7%"], "keep": "$48.00", "buyer": "$70.30"}},
        {"set": {"gig": "250", "wd": "3"}, "click": ["early"], "expect": {"rows": ["$13.75", "-$50.00", "$200.00", "-$2.00", "-$3.00"], "keep": "$195.00", "buyer": "$263.75"}},
        {"set": {"gig": "200"}, "expect": {"rows": "$11.00", "buyer": "$211.00", "keep": "$160.00"}},
        {"set": {"later": "20", "want": "100"}, "expect": {"rows": ["$4.60", "$24.85"], "buyer": "$80.85", "keep": "$56.00", "need": "$125.00"}},
        {"set": {"gig": "", "tip": ""}, "expect": {"verdict": "No order entered", "keep": "$0.00", "buyer": "$0.00", "rows": "Enter a gig price"}},
    ],
)
