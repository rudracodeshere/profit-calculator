PAGE = dict(
    slug="pet-sitting-rate-calculator",
    cat="Pricing & margins",
    nav_name="Pet sitting rate calculator",
    title="Pet Sitting Rate Calculator: Overnight, Drop-In and Extra Pet Quote",
    desc="Free pet sitting rate calculator. Enter your overnight and drop-in prices, how many of each, and any extra pets, and get the full quote for the stay.",
    h1="Pet sitting rate calculator for overnights and drop-ins",
    lead="Enter your own prices and the booking. You get the quote for the whole stay, split into overnights, drop-in visits and extra pets, so you can send one number to the client.",
    form="""      <label for="night">Your price per overnight</label>
      <div class="in"><span>$</span><input id="night" type="number" inputmode="decimal" min="0" step="0.5" value="75"></div>
      <label for="nights">Overnights in the booking</label>
      <div class="in"><input id="nights" type="number" inputmode="numeric" min="0" step="1" value="7"></div>
      <label for="drop">Your price per drop-in visit</label>
      <div class="in"><span>$</span><input id="drop" type="number" inputmode="decimal" min="0" step="0.5" value="25"></div>
      <label for="drops">Drop-in visits in the booking</label>
      <div class="in"><input id="drops" type="number" inputmode="numeric" min="0" step="1" value="4"></div>
      <label for="pets">Extra pets <small>(beyond the first)</small></label>
      <div class="in"><input id="pets" type="number" inputmode="numeric" min="0" step="1" value="1"></div>
      <label for="fee">Extra pet fee per overnight or visit</label>
      <div class="in"><span>$</span><input id="fee" type="number" inputmode="decimal" min="0" step="0.5" value="5"></div>""",
    out="""<div class="big"><span>Quote for this booking</span><b id="quote"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var nr=n('night'),nn=Math.round(n('nights')),dr=n('drop'),dn=Math.round(n('drops')),ep=Math.round(n('pets')),f=n('fee');
  var units=nn+dn;
  if(!units){$('quote').textContent='-';setRows([]);verdict(false,'Enter how many overnights or drop-in visits the booking has.');return}
  var on=nn*nr,dv=dn*dr,pe=ep*f*units,q=on+dv+pe;
  $('quote').textContent=m(q);
  setRows([['Overnights: '+nn+' x '+m(nr),m(on)],['Drop-ins: '+dn+' x '+m(dr),m(dv)],['Extra pets: '+ep+' x '+m(f)+' x '+units,m(pe)],['Booking total',m(q),'total'],['Average per day of care',m(q/Math.max(nn,1))]]);
  verdict(true,'Quote '+m(q)+' for '+nn+' overnight'+(nn==1?'':'s')+' and '+dn+' drop-in'+(dn==1?'':'s')+'.');
}""",
    note="Every price here is yours to set; the defaults are only an example. The extra pet fee is charged once per overnight or visit for each pet beyond the first.",
    body="""<h2>How the quote is worked out</h2>
<p class="formula">Quote = overnights &times; overnight price + drop-ins &times; drop-in price + extra pets &times; extra pet fee &times; (overnights + drop-ins)</p>
<h2>Worked example</h2>
<p>A sitter charges <strong>$75 an overnight</strong> and <strong>$25 a drop-in</strong>, plus <strong>$5 per extra pet</strong> per overnight or visit. The client books 7 overnights and 4 drop-ins for 2 dogs.</p>
<p>Overnights come to 7 &times; $75 = $525 and drop-ins to 4 &times; $25 = $100. The second dog adds 1 &times; $5 &times; 11 = $55. The quote is <strong>$680</strong>.</p>
<p>If some of those dates are holidays, the <a href="../pet-sitter-holiday-rate-calculator/">holiday rate calculator</a> adds your surcharge to just those dates.</p>
<h2>Setting your prices</h2>
<p><strong>Overnights.</strong> An overnight usually covers the evening, the night and the morning, so it is priced well above a single visit.</p>
<p><strong>Drop-ins.</strong> Price each visit by how long you stay and how far you drive.</p>
<p><strong>Extra pets.</strong> A small fee per extra pet covers the added feeding, walking and cleanup without changing your base price.</p>""",
    faqs=[
        ("How much should I charge for pet sitting overnight?", "Set an overnight price that pays for the evening, night and morning you spend there. Enter it here with the number of nights to see the full quote."),
        ("How do I price pet sitting for a week?", "Count the overnights and any extra drop-in visits, add an extra pet fee if there's more than one pet, and quote the total. In the example, 7 overnights and 4 drop-ins for 2 dogs come to $680."),
        ("Should I charge more for extra pets?", "Many sitters add a fee for each pet beyond the first. Here it is charged once per overnight or visit, so 1 extra pet at $5 over 11 overnights and visits adds $55."),
        ("What about holidays?", "Use the holiday rate calculator to add a surcharge to only the holiday dates in the booking."),
    ],
    related=["pet-sitter-holiday-rate-calculator", "price-increase-calculator", "invoice-late-fee-calculator", "markup-calculator"],
    cta_head="Track every booking, client and holiday rate in one sheet",
    cta_text="The <strong>Pet Sitting Business Tracker</strong> fills in each booking's price for you, adds extra pet fees, applies your holiday rate on your holiday dates, keeps pets, meds and vet details in one place, and shows what you earned and what you're still owed each month. Excel and Google Sheets, one-time $49.",
    cta_url="https://quietprofitsheets.gumroad.com/l/pet-sitting-spreadsheet", cta_btn="Get the Pet Sitting Business Tracker",
    cta_extra=[], gig=None,
    tests=[
        {"expect": {"quote": ["$680.00"], "rows": ["$525.00", "$100.00", "$55.00"], "verdict": ["Quote $680.00"]}},
        {"set": {"pets": "0"}, "expect": {"quote": ["$625.00"]}},
        {"set": {"drops": "0"}, "expect": {"quote": ["$560.00"]}},
        {"set": {"nights": "0", "drops": "0"}, "expect": {"verdict": ["Enter how many"]}},
    ],
)
