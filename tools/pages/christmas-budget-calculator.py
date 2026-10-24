PLANNER = "https://quietprofitsheets.gumroad.com/l/christmas-budget-planner"

PAGE = dict(
    slug="christmas-budget-calculator",
    cat="Budgets & planning",
    nav_name="Christmas budget calculator",
    title="Christmas Budget Calculator: Gift Budget Per Person and How Much to Save Each Payday",
    desc="Free Christmas budget calculator. Set a gift budget per child and per adult, add food, decorations and travel, and see your total and how much to put aside each payday before you shop.",
    h1="Christmas budget calculator",
    lead="Put in who you buy for and what else Christmas costs you. You get your total budget, the split between gifts and everything else, and how much to set aside each payday so December is paid for before it starts.",
    form="""      <label for="kids">Kids you buy for</label>
      <div class="in"><input id="kids" type="number" inputmode="numeric" min="0" step="1" value="2"><span>kids</span></div>
      <label for="pkid">Gift budget per child</label>
      <div class="in"><span>$</span><input id="pkid" type="number" inputmode="decimal" min="0" step="5" value="150"></div>
      <label for="adults">Adults you buy for</label>
      <div class="in"><input id="adults" type="number" inputmode="numeric" min="0" step="1" value="4"><span>adults</span></div>
      <label for="padult">Gift budget per adult</label>
      <div class="in"><span>$</span><input id="padult" type="number" inputmode="decimal" min="0" step="5" value="50"></div>
      <label for="food">Food and hosting</label>
      <div class="in"><span>$</span><input id="food" type="number" inputmode="decimal" min="0" step="10" value="200"></div>
      <label for="deco">Tree and decorations</label>
      <div class="in"><span>$</span><input id="deco" type="number" inputmode="decimal" min="0" step="5" value="50"></div>
      <label for="wrap">Wrapping, cards and postage</label>
      <div class="in"><span>$</span><input id="wrap" type="number" inputmode="decimal" min="0" step="5" value="40"></div>
      <label for="travel">Travel and outings</label>
      <div class="in"><span>$</span><input id="travel" type="number" inputmode="decimal" min="0" step="10" value="0"></div>
      <label for="saved">Already saved for Christmas</label>
      <div class="in"><span>$</span><input id="saved" type="number" inputmode="decimal" min="0" step="10" value="0"></div>
      <label for="freq">How often you get paid</label>
      <select id="freq"><option value="7">Every week</option><option value="14" selected>Every 2 weeks</option><option value="m">Once a month</option></select>
      <label for="pay">Your next payday</label>
      <input id="pay" type="date">
      <label for="by">Finish shopping by</label>
      <input id="by" type="date">
      <label for="today">Today</label>
      <input id="today" type="date">""",
    out="""<div class="big"><span>Put aside each payday</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""var MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],DN=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
function dt(s){var p=s.split('-');return new Date(Date.UTC(+p[0],+p[1]-1,+p[2]))}
function iso(d){return d.toISOString().slice(0,10)}
function f(d){return DN[d.getUTCDay()]+', '+MON[d.getUTCMonth()]+' '+d.getUTCDate()}
function next(d,fq){var x=new Date(d.getTime());if(fq=='m'){var day=d.getUTCDate();x.setUTCDate(1);x.setUTCMonth(x.getUTCMonth()+1);var last=new Date(Date.UTC(x.getUTCFullYear(),x.getUTCMonth()+1,0)).getUTCDate();x.setUTCDate(Math.min(day,last))}else x.setUTCDate(x.getUTCDate()+(+fq));return x}
(function(){var t=new Date(),td=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate()));
  var y=td.getUTCMonth()==11&&td.getUTCDate()>25?td.getUTCFullYear()+1:td.getUTCFullYear();
  if(!$('today').value)$('today').value=iso(td);
  if(!$('pay').value){var p=new Date(td.getTime());p.setUTCDate(p.getUTCDate()+7);$('pay').value=iso(p)}
  if(!$('by').value)$('by').value=y+'-12-14';})();
function calc(){
  var k=Math.floor(n('kids')),a=Math.floor(n('adults')),gk=k*n('pkid'),ga=a*n('padult'),gifts=gk+ga,
      other=n('food')+n('deco')+n('wrap')+n('travel'),total=gifts+other,saved=n('saved'),need=Math.max(0,total-saved);
  if(!$('today').value||!$('pay').value||!$('by').value){$('big').textContent='-';setRows([]);verdict(false,'Pick your next payday and the date you want to finish shopping.');return}
  var today=dt($('today').value),by=dt($('by').value),fq=$('freq').value,d=dt($('pay').value),c=0,last=null;
  while(d<today)d=next(d,fq);
  while(d<=by&&c<200){c++;last=d;d=next(d,fq)}
  var xmas=new Date(Date.UTC(by.getUTCFullYear(),11,25)),left=Math.round((xmas-today)/864e5);
  var rows=[[k+(k==1?' child':' kids')+' x '+m(n('pkid')),m(gk)],[a+(a==1?' adult':' adults')+' x '+m(n('padult')),m(ga)],['Gifts',m(gifts)],
    ['Food, decorations, wrapping and travel',m(other)],['Total Christmas budget',m(total),'total']];
  if(saved)rows.push(['Already saved',m(saved)],['Still to save',m(need)]);
  rows.push(['Paydays left before '+f(by),c],['Days until Christmas',left<0?'passed':left]);
  setRows(rows);
  if(!total){$('big').textContent='-';verdict(false,'Add the people you buy for and your other Christmas costs to see your budget.');return}
  if(!need){$('big').textContent=m(0);verdict(true,'You have already saved '+m(saved)+', which covers the whole '+m(total)+' budget. Track what you spend so it stays that way.');return}
  if(!c){$('big').textContent=m(need);verdict(false,'There is no payday between today and '+f(by)+', so the full '+m(need)+' has to come from money you already have. Move your shopping date later or trim the list.');return}
  var per=Math.ceil(need/c*100)/100;
  $('big').textContent=m(per);
  verdict(per<=need/2||c>1,'Put aside '+m(per)+' on each of your next '+c+' paydays, the last one '+f(last)+', and your '+m(total)+' Christmas is paid for by '+f(by)+'. Gifts are '+Math.round(gifts/total*100)+'% of the budget.');
}""",
    note="Paydays are counted from your next payday up to and including your finish-shopping date. Monthly paydays keep the same day of the month, moved to the last day in shorter months. The amount per payday is rounded up to the cent so the total is always covered. Nothing you enter leaves your browser.",
    body="""<h2>How the Christmas budget is worked out</h2>
<p>A Christmas budget is two parts: what you spend on gifts, and everything else the season costs. People tend to plan the first and forget the second, then find the tree, the big dinner, the wrapping paper and the stamps on the credit card in January.</p>
<p class="formula">Total budget = (kids x budget per child) + (adults x budget per adult) + food + decorations + wrapping + travel</p>
<p class="formula">Put aside each payday = (total budget - already saved) / paydays left before you finish shopping</p>
<h2>Worked example</h2>
<p>You buy for <strong>2 kids at $150</strong> each and <strong>4 adults at $50</strong> each. That's $300 + $200 = <strong>$500</strong> on gifts. Add $200 for food and hosting, $50 for the tree and decorations and $40 for wrapping, cards and postage, and the other costs come to <strong>$290</strong>. The total Christmas budget is <strong>$790</strong>.</p>
<p>Counting from Wed, Oct 21, say you're paid every 2 weeks with the next payday on Fri, Oct 23, and you want to finish shopping by Mon, Dec 14. That leaves 4 paydays: Oct 23, Nov 6, Nov 20 and Dec 4. $790 / 4 = <strong>$197.50 each payday</strong>. Paid weekly, it's 8 paydays and <strong>$98.75</strong> each. Paid monthly on the 23rd, only Oct 23 and Nov 23 are left, so it's <strong>$395.00</strong> each.</p>
<p>If you've already put $190 aside, you only need to find $600 more: <strong>$150.00</strong> on each of the 4 paydays.</p>
<h2>How to set a gift budget per person</h2>
<p>Start from the total you can afford, not from a list of gift ideas. Take what you can set aside before your shopping date, subtract the other costs first (they're harder to cut), and split what's left between the people you buy for. Kids usually get a bigger share than adults. For coworkers, neighbors and teachers, one small flat amount each keeps it simple.</p>
<p>If the number per payday is more than you can spare, you have three levers: buy for fewer adults (a family gift swap or a Secret Santa cuts the list fast), lower the per-person amount, or pick a later shopping date. Change any field above and the payday amount updates as you type.</p>
<h2>Keep it on track in December</h2>
<p>A budget only works if you track what you actually spend. Write down each gift as you buy it, with the price and who it's for, and check it against that person's budget before you buy the next one. Keep receipts and return-by dates together, since a lot of December buys get swapped in January.</p>
<p>Once Christmas is paid for, the next job is January. If you want the whole of next year planned the same way, month by month, the <a href="https://quietprofitsheets.gumroad.com/l/2027-budget-spreadsheet?utm_source=calculator&amp;utm_medium=body&amp;utm_content=christmas-budget-calculator" rel="noopener">2027 budget spreadsheet</a> does that in Google Sheets or Excel.</p>""",
    faqs=[
        ("How much should I budget for Christmas?", "Work backward from what you can save before you shop. Add up the gifts per person, then add food, decorations, wrapping and travel, which often come to more than people expect. In the example above that's $500 on gifts plus $290 for everything else."),
        ("How much should I spend per child at Christmas?", "There's no right number. Pick one amount per child that fits your total, and use the same amount for each child so it feels fair. Put it in the budget per child field to see what it does to your total and payday savings."),
        ("How do I save for Christmas from each paycheck?", "Divide what you still need by the paydays left before your shopping date. With $790 to save and 4 paydays left, that's $197.50 each. Move the money to a separate savings account on payday so it isn't spent."),
        ("What costs do people forget in a Christmas budget?", "Food and hosting, the tree and decorations, wrapping paper and tape, cards and postage, travel to family, outings, and gifts for teachers, coworkers and neighbors."),
    ],
    related=["holiday-order-cutoff-calculator", "price-increase-calculator", "break-even-calculator", "profit-margin-calculator"],
    cta_head="Track every gift, not just the total",
    cta_text="The <strong>Christmas Budget Spreadsheet + Gift Tracker</strong> keeps a budget per person, a gift list with prices, status and return-by dates, a season budget for food, decorations, travel and postage, and a savings plan that works out how much to put aside each payday. It flags anyone over budget and moves to next Christmas on its own. Excel and Google Sheets, plus printable PDF worksheets. One-time $5.",
    cta_url=PLANNER,
    cta_btn="Get the Christmas Budget Spreadsheet",
    cta_extra=["budget"],
    gig=None,
    tests=[
        {"set": {"today": "2026-10-21", "pay": "2026-10-23", "by": "2026-12-14"},
         "expect": {"big": "$197.50", "rows": ["$300.00", "$200.00", "$500.00", "$290.00", "$790.00", "65"], "verdict": ["4 paydays", "Fri, Dec 4", "63%"]}},
        {"set": {"today": "2026-10-21", "pay": "2026-10-23", "by": "2026-12-14", "freq": "7"}, "expect": {"big": "$98.75", "verdict": ["8 paydays", "Fri, Dec 11"]}},
        {"set": {"today": "2026-10-21", "pay": "2026-10-23", "by": "2026-12-14", "freq": "m"}, "expect": {"big": "$395.00", "verdict": ["2 paydays", "Mon, Nov 23"]}},
        {"set": {"today": "2026-10-21", "pay": "2026-10-23", "by": "2026-12-14", "saved": "190"}, "expect": {"big": "$150.00", "rows": ["$190.00", "$600.00"]}},
        {"set": {"today": "2026-10-21", "pay": "2026-10-23", "by": "2026-12-14", "saved": "1000"}, "expect": {"big": "$0.00", "verdict": "covers the whole"}},
        {"set": {"today": "2026-10-21", "pay": "2026-10-23", "by": "2026-10-22"}, "expect": {"big": "$790.00", "verdict": "no payday"}},
        {"set": {"today": "2026-10-21", "pay": "2026-10-23", "by": "2026-12-14", "kids": "0", "adults": "0", "food": "0", "deco": "0", "wrap": "0"}, "expect": {"big": "-", "verdict": "Add the people"}},
        {"set": {"today": "2026-11-10", "pay": "2026-10-23", "by": "2026-12-14", "kids": "3", "pkid": "200"}, "expect": {"big": "$545.00", "rows": ["$600.00", "$1,090.00"], "verdict": "Fri, Dec 4"}},
    ],
)
