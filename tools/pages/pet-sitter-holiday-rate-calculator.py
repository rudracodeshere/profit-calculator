PAGE = dict(
    slug="pet-sitter-holiday-rate-calculator",
    cat="Pricing & margins",
    nav_name="Pet sitter holiday rate calculator",
    title="Pet Sitter Holiday Rate Calculator: Overnight and Drop-In Quotes",
    desc="Free holiday rate calculator for pet sitters. Add a holiday surcharge to your overnight or drop-in rate and get the holiday price and the full booking quote.",
    h1="Pet sitter holiday rate calculator for overnights and visits",
    lead="Enter your normal price per visit or night, your holiday surcharge, and how much of the booking falls on holiday dates. You get the holiday price, the booking total to quote, and how much extra the holiday dates earn you.",
    form="""      <label for="rate">Your normal price per visit or night</label>
      <div class="in"><span>$</span><input id="rate" type="number" inputmode="decimal" min="0" step="0.5" value="75"></div>
      <label for="pct">Holiday surcharge</label>
      <div class="in"><input id="pct" type="number" inputmode="decimal" min="0" step="1" value="15"><span>%</span></div>
      <label for="flat">Or a flat extra per holiday visit or night <small>(0 if you only use a percent)</small></label>
      <div class="in"><span>$</span><input id="flat" type="number" inputmode="decimal" min="0" step="1" value="0"></div>
      <label for="total">Visits or nights in the booking</label>
      <div class="in"><input id="total" type="number" inputmode="numeric" min="0" step="1" value="7"></div>
      <label for="hol">How many of them are on holiday dates</label>
      <div class="in"><input id="hol" type="number" inputmode="numeric" min="0" step="1" value="3"></div>""",
    out="""<div class="big"><span>Quote for this booking</span><b id="quote"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var r=n('rate'),p=n('pct'),f=n('flat'),t=Math.round(n('total')),h=Math.round(n('hol'));
  if(!r||!t){$('quote').textContent='-';setRows([]);verdict(false,'Enter your normal price and how many visits or nights the booking has.');return}
  if(h>t){$('quote').textContent='-';setRows([]);verdict(false,'Holiday visits or nights can\\'t be more than the '+t+' in the booking.');return}
  var hr=r*(1+p/100)+f,reg=t-h,q=reg*r+h*hr,extra=q-t*r;
  $('quote').textContent=m(q);
  setRows([['Holiday price per visit or night',m(hr)],['Regular: '+reg+' x '+m(r),m(reg*r)],['Holiday: '+h+' x '+m(hr),m(h*hr)],['Booking total',m(q),'total'],['Extra from the holiday dates',m(extra)],
    ['At 10% surcharge',m(reg*r+h*(r*1.1+f))],['At 20% surcharge',m(reg*r+h*(r*1.2+f))],['At 25% surcharge',m(reg*r+h*(r*1.25+f))]]);
  verdict(true,h?'Quote '+m(q)+'. The '+h+' holiday '+(h==1?'date adds ':'dates add ')+m(extra)+' to the normal '+m(t*r)+'.':'No holiday dates in this booking, so it\\'s your normal '+m(q)+'.');
}""",
    note="The holiday price is your normal price plus the percent, plus any flat extra. Visits or nights outside your holiday dates stay at your normal price. Pick your own holiday dates: sitters use anything from just the day itself to the whole stretch from Thanksgiving through New Year.",
    body="""<h2>How the holiday price is worked out</h2>
<p class="formula">Holiday price = normal price &times; (1 + surcharge %) + flat extra</p>
<p class="formula">Booking total = regular visits &times; normal price + holiday visits &times; holiday price</p>
<p>Only the visits or nights that fall on your holiday dates get the higher price. That keeps a long booking that just touches Christmas from jumping in price for every day.</p>
<h2>Worked example</h2>
<p>An overnight sitter charges <strong>$75 a night</strong> and adds <strong>15%</strong> on holiday dates. A client books 7 nights, and 3 of them fall on the holiday dates.</p>
<p>The holiday price is $75 &times; 1.15 = <strong>$86.25</strong>. The 4 regular nights come to $300 and the 3 holiday nights to $258.75, so the quote is <strong>$558.75</strong>. That's $33.75 more than 7 nights at the normal price.</p>
<p>With a flat $20 per holiday night instead of a percent, the holiday price is $95 and the quote is $585.</p>
<h2>Choosing your surcharge and dates</h2>
<p><strong>Percent or flat.</strong> A percent grows with your price, so it works across drop-ins, walks and overnights. A flat amount is easier to explain to clients. You can use both.</p>
<p><strong>Pick the dates once and write them down.</strong> Common windows are the holiday itself, the days around it, or a set stretch such as December 20 to January 1. Whatever you pick, tell clients when they book so the quote isn't a surprise.</p>
<p><strong>New and existing clients.</strong> Some sitters charge regulars a smaller surcharge than new clients. Run the calculator once for each.</p>""",
    faqs=[
        ("How much should pet sitters charge on holidays?", "Many sitters add a surcharge on holiday dates, either a percent of their normal price or a flat amount per visit or night. Use the numbers you would be happy working the holiday for; the calculator shows what each choice does to the quote."),
        ("Which days count as holiday dates?", "You decide. Some sitters charge holiday rates only on the day itself, others on the days around it, and others on a whole stretch such as December 20 to January 1. Tell clients your dates when they book."),
        ("Does the surcharge apply to the whole booking?", "Not in this calculator. Only the visits or nights on your holiday dates get the holiday price, and the rest stay at your normal price. In the example, 3 of 7 nights are on holiday dates, so the quote is $558.75 instead of $525."),
        ("Can I use a flat holiday fee instead of a percent?", "Yes. Set the percent to 0 and enter the flat extra. A $75 night with a $20 flat holiday extra becomes $95."),
    ],
    related=["price-increase-calculator", "invoice-late-fee-calculator", "markup-calculator", "profit-margin-calculator"],
    cta_head="Track every booking, client and holiday rate in one sheet",
    cta_text="The <strong>Pet Sitting Business Tracker</strong> fills in each booking's price for you, applies your holiday rate on your holiday dates, keeps pets, meds and vet details in one place, and shows what you earned and what you're still owed each month. Excel and Google Sheets, one-time $49.",
    cta_url="https://quietprofitsheets.gumroad.com/l/pet-sitting-spreadsheet", cta_btn="Get the Pet Sitting Business Tracker",
    cta_extra=[], gig=None,
    tests=[
        {"expect": {"quote": ["$558.75"], "rows": ["$86.25", "$300.00", "$258.75", "$33.75"], "verdict": ["Quote $558.75", "add $33.75"]}},
        {"set": {"pct": "0", "flat": "20"}, "expect": {"quote": ["$585.00"], "rows": ["$95.00"]}},
        {"set": {"hol": "0"}, "expect": {"quote": ["$525.00"], "verdict": ["No holiday dates"]}},
        {"set": {"hol": "9"}, "expect": {"verdict": ["can't be more than the 7"]}},
        {"set": {"rate": "0"}, "expect": {"verdict": ["Enter your normal price"]}},
    ],
)
