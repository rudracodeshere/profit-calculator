PAGE = dict(
    slug="pet-sitting-rate-calculator",
    cat="Pricing & margins",
    nav_name="Pet sitting rate calculator",
    title="Pet Sitter Rates Calculator: Quote a Week of Overnights, Drop-Ins and Holidays",
    desc="Free pet sitter rates calculator. Enter your overnight and drop-in prices, extra pets and any holiday surcharge, and get the full quote for a week's stay.",
    h1="Pet sitting rate calculator for a week of overnights",
    lead="Enter your own prices and the booking. You get one number to send the client, split into overnights, drop-in visits, extra pets and the holiday surcharge on just the holiday dates.",
    form="""      <label for="night">Your price per overnight</label>
      <div class="in"><span>$</span><input id="night" type="number" inputmode="decimal" min="0" step="0.5" value="75"></div>
      <label for="nights">Overnights in the booking</label>
      <div class="in"><input id="nights" type="number" inputmode="numeric" min="0" step="1" value="7"></div>
      <label for="drop">Your price per drop-in visit</label>
      <div class="in"><span>$</span><input id="drop" type="number" inputmode="decimal" min="0" step="0.5" value="25"></div>
      <label for="drops">Drop-in visits in the booking</label>
      <div class="in"><input id="drops" type="number" inputmode="numeric" min="0" step="1" value="0"></div>
      <label for="pets">Extra pets <small>(beyond the first)</small></label>
      <div class="in"><input id="pets" type="number" inputmode="numeric" min="0" step="1" value="0"></div>
      <label for="fee">Extra pet fee per overnight or visit</label>
      <div class="in"><span>$</span><input id="fee" type="number" inputmode="decimal" min="0" step="0.5" value="5"></div>
      <label for="pct">Holiday surcharge <small>(0 if none)</small></label>
      <div class="in"><input id="pct" type="number" inputmode="decimal" min="0" step="1" value="15"><span>%</span></div>
      <label for="hn">Overnights on holiday dates</label>
      <div class="in"><input id="hn" type="number" inputmode="numeric" min="0" step="1" value="3"></div>
      <label for="hd">Drop-ins on holiday dates</label>
      <div class="in"><input id="hd" type="number" inputmode="numeric" min="0" step="1" value="0"></div>""",
    out="""<div class="big"><span>Quote for this booking</span><b id="quote"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var nr=n('night'),nn=Math.round(n('nights')),dr=n('drop'),dn=Math.round(n('drops')),ep=Math.round(n('pets')),f=n('fee'),p=n('pct'),hn=Math.round(n('hn')),hd=Math.round(n('hd'));
  var units=nn+dn;
  function no(t){$('quote').textContent='-';setRows([]);verdict(false,t)}
  if(!units)return no('Enter how many overnights or drop-in visits the booking has.');
  if(hn>nn)return no('Holiday overnights can\\'t be more than the '+nn+' overnights in the booking.');
  if(hd>dn)return no('Holiday drop-ins can\\'t be more than the '+dn+' drop-ins in the booking.');
  var on=nn*nr,dv=dn*dr,pe=ep*f*units,hx=(hn*nr+hd*dr)*p/100,q=on+dv+pe+hx;
  $('quote').textContent=m(q);
  setRows([['Overnights: '+nn+' x '+m(nr),m(on)],['Drop-ins: '+dn+' x '+m(dr),m(dv)],['Extra pets: '+ep+' x '+m(f)+' x '+units,m(pe)],['Holiday surcharge: '+p+'% on '+(hn+hd)+' holiday date'+(hn+hd==1?'':'s'),m(hx)],['Booking total',m(q),'total'],['Holiday overnight price',m(nr*(1+p/100))]]);
  verdict(true,'Quote '+m(q)+' for '+nn+' overnight'+(nn==1?'':'s')+(dn?' and '+dn+' drop-in'+(dn==1?'':'s'):'')+'.'+(hx?' The holiday dates add '+m(hx)+'.':''));
}""",
    note="Every price here is yours to set; the defaults are only an example. The extra pet fee is charged once per overnight or visit for each pet beyond the first. The holiday surcharge applies only to the overnights and visits on your holiday dates.",
    body="""<h2>How the quote is worked out</h2>
<p class="formula">Quote = overnights &times; overnight price + drop-ins &times; drop-in price + extra pets &times; extra pet fee &times; (overnights + drop-ins) + surcharge % &times; (holiday overnights &times; overnight price + holiday drop-ins &times; drop-in price)</p>
<h2>Worked example: a week of overnights</h2>
<p>A sitter charges <strong>$75 an overnight</strong> and adds <strong>15%</strong> on holiday dates. A client books 7 nights, and 3 of them fall on holiday dates.</p>
<p>The 7 nights come to 7 &times; $75 = $525. The holiday price is $75 &times; 1.15 = $86.25, so the 3 holiday nights add 3 &times; $11.25 = $33.75. The quote is <strong>$558.75</strong>.</p>
<p>Add 4 drop-ins at $25 and a second dog at $5 per overnight or visit, and the quote becomes $525 + $100 + $55 + $33.75 = <strong>$713.75</strong>.</p>
<h2>Setting your prices</h2>
<p><strong>Overnights.</strong> An overnight usually covers the evening, the night and the morning, so it is priced well above a single visit.</p>
<p><strong>Drop-ins.</strong> Price each visit by how long you stay and how far you drive.</p>
<p><strong>Extra pets.</strong> A small fee per extra pet covers the added feeding, walking and cleanup without changing your base price.</p>
<p><strong>Holidays.</strong> Pick your holiday dates once and tell clients when they book. Only those dates get the surcharge, so a long stay that just touches Christmas doesn't jump in price for every day.</p>""",
    faqs=[
        ("How much should I charge for pet sitting for a week?", "Count the overnights and any drop-in visits, add an extra pet fee if there's more than one pet, and add your holiday surcharge on any holiday dates. In the example, 7 overnights at $75 with 3 holiday nights at 15% come to $558.75."),
        ("How much should I charge for pet sitting overnight?", "Set an overnight price that pays for the evening, night and morning you spend there. Enter it here with the number of nights to see the full quote."),
        ("Should I charge more for extra pets?", "Many sitters add a fee for each pet beyond the first. Here it is charged once per overnight or visit, so 1 extra pet at $5 over 11 overnights and visits adds $55."),
        ("How much should pet sitters charge on holidays?", "Many sitters add a percent on holiday dates. Enter yours and how many overnights and visits fall on those dates; the rest of the booking stays at your normal price."),
    ],
    related=["price-increase-calculator", "invoice-late-fee-calculator", "markup-calculator", "profit-margin-calculator"],
    cta_head="Track every booking, client and holiday rate in one sheet",
    cta_text="The <strong>Pet Sitting Business Tracker</strong> fills in each booking's price for you, adds extra pet fees, applies your holiday rate on your holiday dates, keeps pets, meds and vet details in one place, and shows what you earned and what you're still owed each month. Excel and Google Sheets, one-time $49.",
    cta_url="https://quietprofitsheets.gumroad.com/l/pet-sitting-spreadsheet", cta_btn="Get the Pet Sitting Business Tracker",
    cta_extra=[], gig=None,
    tests=[
        {"expect": {"quote": ["$558.75"], "rows": ["$525.00", "$33.75", "$86.25"], "verdict": ["Quote $558.75", "add $33.75"]}},
        {"set": {"pct": "0"}, "expect": {"quote": ["$525.00"]}},
        {"set": {"drops": "4", "pets": "1"}, "expect": {"quote": ["$713.75"], "rows": ["$100.00", "$55.00"]}},
        {"set": {"drops": "4", "hd": "2"}, "expect": {"quote": ["$666.25"]}},
        {"set": {"hn": "9"}, "expect": {"verdict": ["can't be more than the 7"]}},
        {"set": {"hd": "1"}, "expect": {"verdict": ["can't be more than the 0"]}},
        {"set": {"nights": "0", "drops": "0", "hn": "0"}, "expect": {"verdict": ["Enter how many"]}},
    ],
)
