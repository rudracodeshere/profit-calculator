PAGE = dict(
    slug="stripe-fee-calculator",
    cat="Platform fees",
    nav_name="Stripe fee calculator",
    title="Stripe Fee Calculator 2026: Net Payout, Reverse and Monthly",
    desc="Free Stripe fee calculator: payout after 2.9% + 30 cents, what to charge to receive an exact amount, international and conversion fees, monthly cost.",
    h1="Stripe fee calculator",
    lead="Enter a card payment to see Stripe's fee and your payout. Enter the amount you need to end up with to get the price to charge. Add your monthly volume to see what Stripe costs you as a share of revenue.",
    form="""      <label for="amt">Payment amount</label>
      <div class="in"><span>$</span><input id="amt" type="number" inputmode="decimal" min="0" step="0.01" value="100"></div>
      <label for="want">Amount you want to receive</label>
      <div class="in"><span>$</span><input id="want" type="number" inputmode="decimal" min="0" step="0.01" value="100"></div>
      <label class="check"><input id="intl" type="checkbox"> International card</label>
      <label class="check"><input id="fx" type="checkbox"> Currency conversion needed</label>
      <label for="cnt">Payments per month</label>
      <div class="in"><input id="cnt" type="number" inputmode="numeric" min="0" step="1" value="500"></div>
      <label for="avg">Average payment</label>
      <div class="in"><span>$</span><input id="avg" type="number" inputmode="decimal" min="0" step="0.01" value="40"></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="sp">Domestic card rate</label>
      <div class="in"><input id="sp" type="number" min="0" step="0.1" value="2.9"><span>% +</span><span>$</span><input id="sf" type="number" min="0" step="0.01" value="0.30"></div>
      <label for="ip">International card surcharge</label>
      <div class="in"><input id="ip" type="number" min="0" step="0.1" value="1.5"><span>%</span></div>
      <label for="fp">Currency conversion surcharge</label>
      <div class="in"><input id="fp" type="number" min="0" step="0.1" value="1"><span>%</span></div>
      </details>""",
    out="""<div class="big"><span>You receive</span><b id="recv"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <h3>Work backward</h3>
      <table><tbody id="rows2"></tbody></table>
      <h3>Per month</h3>
      <table><tbody id="rows3"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var pct=n('sp'),fix=n('sf');
  if($('intl').checked)pct+=n('ip');
  if($('fx').checked)pct+=n('fp');
  var r=pct/100,lab='Stripe fee ('+(+pct.toFixed(2))+'% + '+m(fix)+')';
  var A=n('amt'),fee=A?A*r+fix:0,got=A-fee;
  setRows([['Customer pays',m(A)],[lab,m(-fee)],['You receive',m(got),'total']]);
  $('recv').textContent=m(got);
  if(r>=1){setRows([['The rate takes the whole payment.','']],'rows2');setRows([],'rows3');verdict(false,'Check the rates: they add up to 100% or more.');return}
  var W=n('want');
  if(W){var ask=Math.ceil((W+fix)/(1-r)*100-1e-6)/100,f2=ask*r+fix;
    setRows([['To receive '+m(W)+', charge',m(ask),'total'],[lab,m(-f2)],['You receive',m(ask-f2)]],'rows2');}
  else setRows([['Enter the amount you want to receive.','']],'rows2');
  var N=Math.round(n('cnt')),V=n('avg'),R=N*V,mf=N&&V?R*r+N*fix:0;
  if(R)setRows([['Volume ('+N+' x '+m(V)+')',m(R)],['Stripe fees',m(-mf)],['Effective rate',pc(mf/R,2),'total']],'rows3');
  else setRows([['Enter payments per month and an average payment.','']],'rows3');
  if(A&&got<=0)verdict(false,'The '+m(fix)+' fixed fee is larger than this payment would leave. Avoid card payments this small.');
  else if(R)verdict(true,'Stripe costs you '+m(mf)+' a month, '+pc(mf/R,2)+' of revenue. The fixed fee is '+m(N*fix)+' of that.');
  else verdict(A>0,A?'Stripe keeps '+m(fee)+' of this payment.':'Enter a payment amount to see the fee.');
}""",
    note="US Stripe standard pricing as of October 2026: 2.9% + $0.30 per successful domestic card charge, +1.5% for international cards and +1% when currency conversion is required. ACH, wallets, Stripe Tax, Billing and disputes ($15 each) have separate pricing. Negotiated or non-US accounts differ, so the rates are editable.",
    body="""<h2>Stripe's standard card fee</h2>
<p>On standard US pricing, Stripe charges 2.9% + $0.30 on each successful card payment. Two surcharges stack on top: 1.5% when the card was issued outside the US, and 1% when the payment has to be converted into your payout currency. An international card in a foreign currency costs 5.4% + $0.30.</p>
<p class="formula">Payout = amount - (amount x rate + $0.30)</p>
<p>Example: a $100 domestic payment costs $3.20 and you receive $96.80. If the card is international, the fee is $4.70 and you get $95.30. Add currency conversion and it is $5.70, leaving $94.30.</p>
<h2>Charging enough to cover the fee</h2>
<p>Passing the fee on means solving for the price, not adding 2.9%. Divide what you want to keep, plus $0.30, by 1 minus the rate:</p>
<p class="formula">Charge = (amount you want + $0.30) / (1 - rate)</p>
<p>To receive $100 from a domestic card, charge $103.30. For an international card, charge $104.92. Check your local rules before adding a surcharge to card payments; some US states restrict it.</p>
<h2>Your monthly Stripe cost</h2>
<p>Stripe has no monthly fee on standard pricing, so your cost scales with volume. 500 payments of $40 is $20,000 a month, and Stripe takes $730.00 of it, an effective 3.65%. The $0.30 fixed part is $150 of that, which is why low-priced products or many small payments push your effective rate up. If 100% of those payments were on international cards, the bill would be $1,030.00.</p>""",
    faqs=[
        ("How much does Stripe charge on $100?", "$3.20 for a domestic card at 2.9% + $0.30, so you receive $96.80. An international card costs $4.70."),
        ("How much should I charge to get $100 after Stripe fees?", "$103.30 with a US card. With an international card, $104.92."),
        ("What is the Stripe fee on $50?", "$1.75 at 2.9% + $0.30, so you receive $48.25."),
        ("Does Stripe charge a monthly fee?", "Not on standard pricing. You pay per successful payment only. Extra products such as Billing, Tax or Radar for Fraud Teams are priced separately."),
    ],
    related=["paypal-fee-calculator", "shopify-fee-calculator", "gumroad-fee-calculator", "profit-margin-calculator", "price-increase-calculator"],
    og_image="pins/pin-06.png",
    tests=[
        {"expect": {"rows": ["-$3.20", "$96.80"], "rows2": ["$103.30"], "rows3": ["$20,000.00", "-$730.00", "3.65%"], "verdict": "$150.00"}},
        {"click": ["intl"], "expect": {"rows": ["-$4.70", "$95.30"], "rows2": "$104.92", "rows3": "-$1,030.00"}},
        {"click": ["intl", "fx"], "expect": {"rows": ["5.4%", "-$5.70", "$94.30"]}},
        {"set": {"amt": "50"}, "expect": {"rows": ["-$1.75", "$48.25"]}},
        {"set": {"amt": "", "want": "", "cnt": "0"}, "expect": {"rows2": "Enter the amount", "rows3": "Enter payments", "verdict": "Enter a payment"}},
    ],
)
