# Carrier dates verified Oct 18, 2026 against the official 2026 pages listed in SRC below. Re-check in late Nov.
USPS_PAGE = "https://www.usps.com/holiday/holiday-shipping-dates.htm"
USPS_NEWS = "https://about.usps.com/newsroom/national-releases/2026/0922-usps-recommends-2026-holiday-mailing-shipping-dates.htm"
UPS_PDF = "https://assets.ups.com/adobe/assets/urn:aaid:aem:e8548535-8096-4fa9-9cef-2b81aef7c26c/original/as/year-end-holiday-schedule-us-en.pdf"
UPS_PAGE = "https://www.ups.com/us/en/support/shipping-support/shipping-services/holiday-shipping-schedule"
FEDEX_PDF = "https://www.fedex.com/content/dam/fedex/us-united-states/services/2026_Peak_Last_Day_to_ship.pdf"
FEDEX_PAGE = "https://www.fedex.com/en-us/holiday/last-days-to-ship.html"
ETSY_CUTOFF = "https://help.etsy.com/hc/en-us/articles/35656110566167-Understanding-Shipping-Carrier-Surcharges-Cutoff-Dates-for-the-Holidays"
ETSY_SHIPBY = "https://help.etsy.com/hc/en-us/articles/115015588087-How-to-Set-Processing-Times-Processing-Profiles-and-Ship-By-Dates"
CHECKED = "checked Oct 18, 2026"

# id, carrier, service, ship-by date, routes (l48 = within the lower 48, off = to/from AK, HI, PR, territories, intl = US to other countries), target
SERVICES = [
    ("uga", "USPS", "Ground Advantage", "2026-12-17", "l48", "before Dec 25"),
    ("ufc", "USPS", "First-Class Mail (cards, flat envelopes)", "2026-12-17", "l48 off", "before Dec 25"),
    ("upm", "USPS", "Priority Mail", "2026-12-18", "l48 off", "before Dec 25"),
    ("upme", "USPS", "Priority Mail Express", "2026-12-19", "l48 off", "before Dec 25"),
    ("ufci", "USPS", "First-Class Package International", "2026-12-09", "intl", "before Dec 25"),
    ("upmi", "USPS", "Priority Mail International", "2026-12-09", "intl", "before Dec 25"),
    ("upmei", "USPS", "Priority Mail Express International", "2026-12-16", "intl", "before Dec 25"),
    ("x3ds", "UPS", "3 Day Select", "2026-12-21", "l48", "on Dec 24"),
    ("x2da", "UPS", "2nd Day Air", "2026-12-22", "l48", "on Dec 24"),
    ("xnda", "UPS", "Next Day Air", "2026-12-23", "l48", "on Dec 24"),
    ("fge", "FedEx", "Ground Economy", "2026-12-15", "l48", "on Dec 24"),
    ("fg5", "FedEx", "Ground / Home Delivery, 5-day transit", "2026-12-17", "l48", "on Dec 24"),
    ("fg4", "FedEx", "Ground / Home Delivery, 4-day transit", "2026-12-18", "l48", "on Dec 24"),
    ("fg3", "FedEx", "Ground / Home Delivery, 3-day transit", "2026-12-21", "l48", "on Dec 24"),
    ("fg2", "FedEx", "Ground / Home Delivery, 2-day transit", "2026-12-22", "l48", "on Dec 24"),
    ("fg1", "FedEx", "Ground / Home Delivery, 1-day transit", "2026-12-23", "l48", "on Dec 24"),
    ("fes", "FedEx", "Express Saver", "2026-12-21", "l48", "on Dec 24"),
    ("f2d", "FedEx", "2Day / 2Day AM", "2026-12-22", "l48", "on Dec 24"),
    ("fon", "FedEx", "Standard, Priority or First Overnight", "2026-12-23", "l48", "on Dec 24"),
]
SRC = {"USPS": USPS_PAGE, "UPS": UPS_PDF, "FedEx": FEDEX_PDF}


def _options():
    out = []
    for c in ("USPS", "UPS", "FedEx"):
        out.append(f'<optgroup label="{c}">')
        for i, cc, s, d, r, t in SERVICES:
            if cc == c:
                out.append(f'<option value="{i}"{" selected" if i == "uga" else ""}>{c} {s}</option>')
        out.append("</optgroup>")
    return "".join(out)


def _js_data():
    rows = ",".join('{id:"%s",c:"%s",s:"%s",d:"%s",r:"%s",t:"%s"}' % x for x in SERVICES)
    return "var S=[" + rows + "];var SRC={USPS:'" + USPS_PAGE + "',UPS:'" + UPS_PDF + "',FedEx:'" + FEDEX_PDF + "'};"


def _fmt(d):
    import datetime
    x = datetime.date.fromisoformat(d)
    return x.strftime("%a, %b ") + str(x.day)


def _table():
    h = ['<table class="wide"><thead><tr><th>Carrier and service</th><th>Ship by (2026)</th><th>Delivery</th></tr></thead><tbody>']
    for i, c, s, d, r, t in SERVICES:
        where = {"l48": "lower 48", "l48 off": "US incl. AK, HI, PR", "intl": "US to all listed regions"}[r]
        h.append(f'<tr><td><a href="{SRC[c]}" rel="noopener">{c}</a> {s} <small>({where})</small></td><td>{_fmt(d)}</td><td>{t}</td></tr>')
    h.append("</tbody></table>")
    return "".join(h)


PAGE = dict(
    result_url="https://quietprofitsheets.gumroad.com/l/christmas-budget-planner",
    cta_extra=["planner"],
    slug="holiday-order-cutoff-calculator",
    cat="Etsy tools",
    nav_name="Holiday order cutoff calculator",
    title="Holiday Order Cutoff Calculator 2026: Last Day to Promise Christmas Delivery",
    desc="Free 2026 holiday order cutoff calculator for Etsy and online sellers. Enter your processing days and USPS, UPS or FedEx service to get the last order date you can promise for Christmas, from official 2026 carrier deadlines.",
    h1="Holiday order cutoff calculator 2026: last day to promise Christmas delivery",
    lead="Enter how many processing days you need and the shipping service you use. The calculator takes the carrier's official 2026 ship-by date for Christmas, steps back through your processing days, and gives you the last day a buyer can order and still get it in time. Put that date in your shop banner and listings.",
    form=f"""      <label for="proc">Processing time <small>(days you need before shipping)</small></label>
      <div class="in"><input id="proc" type="number" inputmode="numeric" min="1" max="60" step="1" value="3"><span>days</span></div>
      <label for="sched">Days you prepare and ship orders</label>
      <select id="sched" class="full"><option value="5" selected>Monday to Friday</option><option value="6">Monday to Saturday</option><option value="7">Every day</option></select>
      <label for="route">Where the package goes</label>
      <select id="route" class="full"><option value="l48" selected>Within the lower 48 states</option><option value="off">To or from Alaska, Hawaii, Puerto Rico or a US territory</option><option value="intl">From the US to another country (USPS)</option></select>
      <label for="svc">Carrier and service</label>
      <select id="svc" class="full">{_options()}</select>
      <label for="today">Today's date <small>(for the countdown)</small></label>
      <div class="in"><input id="today" type="date" value=""></div>""",
    out="""<div class="big"><span>Last day to take orders for Christmas</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>
      <h3>Every service at this processing time</h3>
      <table class="wide"><tbody id="all"></tbody></table>""",
    js=_js_data() + """
var DN=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function dt(s){var p=s.split('-');return new Date(Date.UTC(+p[0],p[1]-1,+p[2]))}
function add(d,k){return new Date(d.getTime()+k*864e5)}
function f(d){return DN[d.getUTCDay()]+', '+MN[d.getUTCMonth()]+' '+d.getUTCDate()}
function work(d,w){var x=d.getUTCDay();return w==7||(x>=1&&x<=w)}
function cut(c,p,w){
  while(!work(c,w))c=add(c,-1);              /* last day you actually ship */
  var x=c,k=0;while(k<p){x=add(x,-1);if(work(x,w))k++}  /* step back p processing days */
  var y=add(x,1);while(!work(y,w))y=add(y,1);  /* orders until the next processing day starts the same clock */
  return {ship:c,last:add(y,-1)};
}
if(!$('today').value){var t=new Date();$('today').value=t.getFullYear()+'-'+('0'+(t.getMonth()+1)).slice(-2)+'-'+('0'+t.getDate()).slice(-2)}
function calc(){
  var p=Math.min(60,Math.max(1,Math.round(n('proc'))||1)),w=+$('sched').value,r=$('route').value,el=$('svc');
  [].forEach.call(el.options,function(o){var s=S.filter(function(z){return z.id==o.value})[0];o.disabled=s.r.split(' ').indexOf(r)<0});
  if(el.options[el.selectedIndex].disabled){for(var i=0;i<el.options.length;i++)if(!el.options[i].disabled){el.selectedIndex=i;break}}
  var s=S.filter(function(z){return z.id==el.value})[0],c=dt(s.d),o=cut(c,p,w),today=$('today').value?dt($('today').value):null;
  $('big').textContent=f(o.last)+', 2026';
  var rows=[[s.c+' '+s.s+' ship-by date','<a href="'+SRC[s.c]+'" rel="noopener">'+f(c)+'</a>'],['Your last shipping day',f(o.ship)],['Processing time',p+(p==1?' day':' days')],['Last order date',f(o.last),'total']];
  if(today){var left=Math.round((o.last-today)/864e5);rows.push(['Days left from '+f(today),left<0?'passed':left])}
  setRows(rows);
  var msg='Promise Christmas delivery ('+s.t+') on orders placed by '+f(o.last)+'. Ship them '+s.c+' '+s.s+' by '+f(o.ship)+'.';
  if(today&&o.last<today)verdict(false,'That cutoff has passed for '+s.c+' '+s.s+'. Pick a faster service below or offer gift cards and digital items instead.');
  else verdict(true,msg+(o.ship<c?' The carrier date is a '+DN[c.getUTCDay()]+', a day you do not ship, so it moves back to '+f(o.ship)+'.':''));
  var h='';S.forEach(function(z){if(z.r.split(' ').indexOf(r)<0)return;var q=cut(dt(z.d),p,w);h+='<tr><td>'+z.c+' '+z.s+'</td><td style="white-space:nowrap">'+(today&&q.last<today?'passed':f(q.last))+'</td></tr>'});
  $('all').innerHTML=h;
}""",
    note=f"""2026 carrier ship-by dates from the official <a href="{USPS_PAGE}" rel="noopener">USPS</a>, <a href="{UPS_PDF}" rel="noopener">UPS</a> and <a href="{FEDEX_PDF}" rel="noopener">FedEx</a> holiday pages, {CHECKED}. USPS dates are for delivery before Dec 25; UPS and FedEx dates are for delivery on Thu, Dec 24. Not offered because the carrier publishes no fixed 2026 date: UPS Ground (UPS says check ups.com/ctc for your ZIP codes), USPS Ground Advantage to or from Alaska, Hawaii and territories (10+ days, check USPS service commitments). Carrier dates are recommendations, not guarantees. No holidays are counted as days off; add any you take to your processing time.""",
    body=f"""<h2>How the cutoff is worked out</h2>
<p>Etsy counts processing time from the day after an order is placed, using only the days in your order processing schedule. The end of that count is the order's "ship by" date (<a href="{ETSY_SHIPBY}" rel="noopener">Etsy Help</a>, {CHECKED}). So the latest order you can accept is the one whose ship-by date still lands on or before the carrier's last day to ship.</p>
<p class="formula">Last order date = carrier ship-by date, moved back to a day you ship, minus your processing days (counting only days you work)</p>
<p>Three rules handle the weekends:</p>
<p><strong>1. The carrier date falls on a day off.</strong> USPS Priority Mail Express is Saturday, Dec 19. If you ship Monday to Friday, your real last day is Friday, Dec 18.</p>
<p><strong>2. Weekends don't count as processing days</strong> unless you work them, the same as Etsy's Monday to Friday schedule.</p>
<p><strong>3. Weekend orders join Monday's clock.</strong> An order placed on Saturday or Sunday starts processing on Monday, exactly like Friday's order. So when the count lands on a Friday, the cutoff runs through Sunday.</p>
<h2>Worked examples (Monday to Friday schedule)</h2>
<p><strong>3 days, USPS Ground Advantage.</strong> Ship by Thu, Dec 17. Count back Wed 16, Tue 15, Mon 14. Last order date: <strong>Mon, Dec 14</strong>. An order on Monday is processed Tue, Wed, Thu and ships Thursday.</p>
<p><strong>2 days, FedEx 2Day.</strong> Ship by Tue, Dec 22. Count back Mon 21, Fri 18. Orders from Friday through Sunday all start processing Monday, so the last order date is <strong>Sun, Dec 20</strong>.</p>
<p><strong>1 day, USPS Priority Mail Express.</strong> The Saturday Dec 19 date moves to Fri, Dec 18, then back one day: <strong>Thu, Dec 17</strong>. Ship Saturdays and it becomes Fri, Dec 18.</p>
<h2>Official 2026 holiday shipping deadlines</h2>
<p>Every date below was read from the carrier's own 2026 page or PDF, {CHECKED}. We only list services with a published date.</p>
{_table()}
<h3>Sources</h3>
<ul>
<li><a href="{USPS_PAGE}" rel="noopener">USPS: 2026 Holiday Shipping Deadlines</a> (usps.com), {CHECKED}. Lower 48, Alaska/Hawaii/territories and international tables.</li>
<li><a href="{USPS_NEWS}" rel="noopener">USPS Newsroom: Postal Service Recommends 2026 Holiday Mailing and Shipping Dates</a>, Sept 22, 2026, {CHECKED}.</li>
<li><a href="{UPS_PDF}" rel="noopener">UPS: 2026 Year-End Holiday Schedule (PDF)</a>, linked from the <a href="{UPS_PAGE}" rel="noopener">UPS Holiday Schedule page</a>, {CHECKED}. Recommended last days to ship for Dec 24 delivery. UPS Ground: no fixed date, check ups.com/ctc.</li>
<li><a href="{FEDEX_PDF}" rel="noopener">FedEx: 2026 Shipping deadlines for holiday packages (PDF)</a>, linked from <a href="{FEDEX_PAGE}" rel="noopener">FedEx Holiday Schedule &amp; Last Days to Ship</a>, {CHECKED}. Last ship dates for Dec 24 delivery; Ground and Home Delivery depend on transit days.</li>
<li><a href="{ETSY_SHIPBY}" rel="noopener">Etsy Help: How to Set Processing Times, Processing Profiles and "Ship By" Dates</a>, {CHECKED}. How ship-by dates are counted.</li>
<li><a href="{ETSY_CUTOFF}" rel="noopener">Etsy Help: Understanding Shipping Carrier Surcharges &amp; Cutoff Dates for the Holidays</a>, {CHECKED}. Its table had not been updated for 2026 yet (it still showed last season's dates, e.g. Priority Mail Express Dec 20), so we use the carriers' 2026 pages instead.</li>
</ul>
<h2>Set it up in your Etsy shop</h2>
<p>Put the date in your shop announcement and the first line of your listings ("Order by Mon, Dec 14 for Christmas delivery in the US"). Check that each listing's processing profile matches the processing time you entered here, and mark any days off in your order processing schedule so Etsy's ship-by dates agree with yours. If you sell a mix of quick and made-to-order items, run the calculator once per processing time.</p>""",
    faqs=[
        ("What is the last day to ship USPS for Christmas 2026?", "USPS recommends Thu, Dec 17 for Ground Advantage and First-Class Mail, Fri, Dec 18 for Priority Mail and Sat, Dec 19 for Priority Mail Express, within the lower 48 states, for delivery before Dec 25."),
        ("What are the UPS and FedEx holiday deadlines for 2026?", "For delivery on Dec 24, UPS lists Mon, Dec 21 for 3 Day Select, Tue, Dec 22 for 2nd Day Air and Wed, Dec 23 for Next Day Air. FedEx lists Mon, Dec 21 for Express Saver, Tue, Dec 22 for 2Day, Wed, Dec 23 for overnight services, Tue, Dec 15 for Ground Economy, and Dec 17 to Dec 23 for Ground and Home Delivery depending on 1 to 5 transit days."),
        ("Does UPS Ground have a Christmas deadline?", "UPS did not publish a fixed 2026 date for UPS Ground. It depends on your origin and destination ZIP codes, so check UPS Calculate Time and Cost. The calculator leaves it out rather than guess."),
        ("Do weekends count as Etsy processing days?", "Only if your order processing schedule includes them. With a Monday to Friday schedule, a 3 day processing time on an order placed Friday ends on Wednesday."),
        ("What should I tell buyers after the cutoff?", "Say plainly that new orders will arrive after Christmas, switch to a faster service if your margins allow it, or point gift buyers to digital downloads and gift cards that need no shipping."),
    ],
    related=["etsy-free-shipping-calculator", "etsy-sale-calculator", "etsy-profit-calculator", "etsy-fee-calculator", "etsy-pricing-calculator"],
    og_image="pins/feed/holiday-order-cutoff-calculator.png",
    cta_head="Holiday orders are coming. Which ones make you money?",
    cta_text="December's rush hides thin margins: free shipping, coupons and surcharge-season labels. The <strong>Seller Profit Sheet</strong> shows net profit per product after Etsy fees, labels, discounts, refunds and ad spend, with a red LOSING MONEY flag on anything underwater. Paste your Etsy or Shopify sales export. Excel and Google Sheets, one-time $14, no subscription.",
    gig="seo",
    tests=[
        {"set": {"today": "2026-10-18"}, "expect": {"big": "Mon, Dec 14, 2026", "rows": ["Thu, Dec 17", "3 days", "Mon, Dec 14", "57"], "verdict": "orders placed by Mon, Dec 14", "all": ["Ground Advantage", "Sun, Dec 20"]}},
        {"set": {"today": "2026-10-18", "proc": "2", "svc": "f2d"}, "expect": {"big": "Sun, Dec 20, 2026", "rows": ["Tue, Dec 22"]}},
        {"set": {"today": "2026-10-18", "proc": "1", "svc": "upme"}, "expect": {"big": "Thu, Dec 17, 2026", "rows": ["Sat, Dec 19", "Fri, Dec 18"], "verdict": "moves back to Fri, Dec 18"}},
        {"set": {"today": "2026-10-18", "proc": "1", "svc": "upme", "sched": "6"}, "expect": {"big": "Fri, Dec 18, 2026"}},
        {"set": {"today": "2026-10-18", "proc": "5", "svc": "x3ds"}, "expect": {"big": "Mon, Dec 14, 2026"}},
        {"set": {"today": "2026-10-18", "proc": "1", "svc": "xnda", "sched": "7"}, "expect": {"big": "Tue, Dec 22, 2026"}},
        {"set": {"today": "2026-10-18", "route": "intl"}, "expect": {"rows": "Wed, Dec 9", "big": "Sun, Dec 6, 2026", "all": "Priority Mail Express International"}},
        {"set": {"today": "2026-10-18", "route": "off", "svc": "uga"}, "expect": {"rows": "First-Class Mail"}},
        {"set": {"today": "2026-12-16", "proc": "3"}, "expect": {"verdict": "has passed", "rows": "passed"}},
        {"set": {"today": "2026-10-18", "proc": "10", "svc": "fg3"}, "expect": {"big": "Mon, Dec 7, 2026"}},
    ],
)
