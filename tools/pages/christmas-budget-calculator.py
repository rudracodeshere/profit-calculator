PAGE = dict(
    slug="christmas-budget-calculator",
    cat="Holiday season",
    gig="sheet",
    nav_name="Christmas budget calculator",
    title="Christmas Budget Calculator: Gift Budget per Person + How Much to Save Each Payday",
    desc="Free Christmas budget calculator. Set a gift budget per kid, adult and friend, add food, travel and decorations, and see your total and how much to set aside each payday until you shop. Free printable worksheet.",
    h1="Christmas budget calculator",
    lead="Add up the whole season, not just the gifts: a budget per person, plus food, travel, decorations and wrapping. Then see how much to set aside each payday so it's paid for before you shop.",
    form="""      <label for="kids">Kids you buy for <small>(count x budget each)</small></label>
      <div class="grid" style="gap:8px">
        <div class="in"><input id="kids" type="number" inputmode="numeric" min="0" step="1" value="2"><span>kids</span></div>
        <div class="in"><span>$</span><input id="perKid" type="number" inputmode="decimal" min="0" step="5" value="150"></div>
      </div>
      <label for="adults">Adults in the family</label>
      <div class="grid" style="gap:8px">
        <div class="in"><input id="adults" type="number" inputmode="numeric" min="0" step="1" value="4"><span>people</span></div>
        <div class="in"><span>$</span><input id="perAdult" type="number" inputmode="decimal" min="0" step="5" value="75"></div>
      </div>
      <label for="others">Friends, coworkers, teachers, neighbors</label>
      <div class="grid" style="gap:8px">
        <div class="in"><input id="others" type="number" inputmode="numeric" min="0" step="1" value="5"><span>people</span></div>
        <div class="in"><span>$</span><input id="perOther" type="number" inputmode="decimal" min="0" step="5" value="25"></div>
      </div>
      <label for="food">Food and hosting</label>
      <div class="in"><span>$</span><input id="food" type="number" inputmode="decimal" min="0" step="10" value="250"></div>
      <label for="travel">Holiday travel</label>
      <div class="in"><span>$</span><input id="travel" type="number" inputmode="decimal" min="0" step="10" value="150"></div>
      <label for="decor">Tree and decorations</label>
      <div class="in"><span>$</span><input id="decor" type="number" inputmode="decimal" min="0" step="5" value="75"></div>
      <label for="wrap">Wrapping, cards and postage</label>
      <div class="in"><span>$</span><input id="wrap" type="number" inputmode="decimal" min="0" step="5" value="50"></div>
      <label for="extra">Anything else <small>(outings, outfits, giving)</small></label>
      <div class="in"><span>$</span><input id="extra" type="number" inputmode="decimal" min="0" step="5" value="0"></div>
      <label for="saved">Already set aside</label>
      <div class="in"><span>$</span><input id="saved" type="number" inputmode="decimal" min="0" step="10" value="300"></div>
      <label for="weeks">Weeks until you shop <small>(filled in to Dec 15)</small></label>
      <div class="in"><input id="weeks" type="number" inputmode="numeric" min="0" step="1" value=""><span>weeks</span></div>
      <label for="freq">How often you get paid</label>
      <select id="freq" class="full"><option value="1">Weekly</option><option value="2" selected>Every 2 weeks</option><option value="2.1667">Twice a month</option><option value="4.333">Monthly</option></select>
      <label for="pay">Take-home pay per paycheck <small>(optional)</small></label>
      <div class="in"><span>$</span><input id="pay" type="number" inputmode="decimal" min="0" step="50" value="1800"></div>""",
    out="""<div class="big"><span>Set aside each payday</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>
      <p class="note" style="margin-top:14px"><a href="christmas-budget-printable-letter.pdf">Free printable Christmas budget worksheet (PDF, US Letter)</a> &middot; <a href="christmas-budget-printable-a4.pdf">A4</a></p>""",
    js="""if(!$('weeks').value){var t=new Date(),y=t.getFullYear(),d=new Date(y,11,15);if(t>d)d=new Date(y+1,11,15);$('weeks').value=Math.max(0,Math.floor((d-t)/604800000))}
function calc(){
  var gifts=n('kids')*n('perKid')+n('adults')*n('perAdult')+n('others')*n('perOther');
  var other=n('food')+n('travel')+n('decor')+n('wrap')+n('extra'),total=gifts+other,saved=n('saved'),need=Math.max(0,total-saved);
  var w=Math.floor(n('weeks')),step=parseFloat($('freq').value)||2,pays=Math.max(1,Math.floor(w/step)),per=need/pays,pay=n('pay');
  if(!total){$('big').textContent='-';setRows([]);verdict(false,'Add the people you buy for, or any holiday cost, to see your budget.');return}
  $('big').textContent=m(per);
  setRows([['Gifts',m(gifts)],['Food, travel, decorations and the rest',m(other)],['Christmas total',m(total),'total'],['Already set aside',m(saved)],
    ['Still to set aside',m(need)],['Paydays left',w?pays:'1 (shopping now)'],['Each payday',m(per)],['Per week',m(w?need/w:need)],
    ['Start in January next year',m(total/12)+' a month']]);
  if(!need){verdict(true,'You have already set aside the full '+m(total)+'. Anything left over can start next year\\'s fund.');return}
  var line='Set aside '+m(per)+' each payday for '+(w?pays+' paydays':'this payday')+' to have '+m(total)+' ready by the time you shop.';
  if(pay){var s=per/pay;verdict(s<=0.15,line+' That is '+pc(s)+' of each paycheck'+(s>0.15?', which is a lot. Trim the per-person amounts or the list, or swap some gifts for experiences.':'.'))}
  else verdict(true,line);
}""",
    note="Paydays are counted from the weeks you enter: every 2 weeks = weeks / 2, twice a month = weeks / 2.17, monthly = weeks / 4.33, rounded down. Amounts stay in your browser; nothing is saved or sent.",
    body="""<h2>How to set a Christmas budget</h2>
<p>Most Christmas overspending isn't the big gifts. It's the costs nobody wrote down: the second trip to the store, the stocking stuffers, the extra groceries for hosting, the postage. So budget the <strong>whole season</strong>, in two parts:</p>
<ul>
<li><strong>Gifts, per person.</strong> Decide an amount for each person before you shop. Grouping helps: kids, close family, then a smaller amount for friends, coworkers, teachers and neighbors.</li>
<li><strong>Everything else.</strong> Food and hosting, travel, the tree and decorations, wrapping, cards and postage, outings, outfits and giving.</li>
</ul>
<p class="formula">Christmas total = (people x budget each, per group) + food + travel + decorations + wrapping + other</p>
<p>Then work backwards from the day you want to shop. Divide what's still to save by the paydays left, and set that aside every payday. Next year, divide the total by 12 and start in January.</p>
<h2>Worked example</h2>
<p>Two kids at <strong>$150</strong> each, four adults at <strong>$75</strong> and five friends and coworkers at <strong>$25</strong> come to $300 + $300 + $125 = <strong>$725</strong> in gifts. Add $250 for food, $150 for travel, $75 for the tree and decorations and $50 for wrapping and postage: <strong>$525</strong>. The season costs <strong>$1,250</strong>.</p>
<p>With $300 already set aside and 8 weeks to go, $950 is left to save. Paid every 2 weeks, that is 4 paydays, so <strong>$237.50 a payday</strong> (about $118.75 a week). On an $1,800 paycheck that is 13.2%. Saving the same $1,250 from January would take <strong>$104.17 a month</strong>.</p>
<h2>What do people actually spend?</h2>
<p>In the National Retail Federation's 2025 holiday survey, US shoppers planned to spend <strong>$890.49</strong> on average: $627.93 on gifts and $262.56 on food, candy, decorations and cards. Gallup's October 2025 poll put planned gift spending at <strong>$1,007</strong>, and $651 for households earning under $50,000. Use these as a sanity check, not a target: the right budget is the one you can pay for in cash by December.</p>
<h2>Keeping to it</h2>
<p>Write every gift down as you buy it, with what you paid, and check it against that person's budget. When someone goes over, take it from another line on purpose instead of letting the total drift. Keep receipts and return-by dates for anything that might go back. A <a href="christmas-budget-printable-letter.pdf">printable worksheet</a> works; a spreadsheet does the adding up for you.</p>""",
    faqs=[
        ("How much should I spend on Christmas?", "Whatever you can pay in cash by the time you shop. Add up gifts per person plus food, travel, decorations and wrapping, then divide what's left to save by your paydays. If that is more than about 15% of each paycheck, trim the list or the per-person amounts."),
        ("How much should I spend per child at Christmas?", "There is no standard amount. Pick one figure per child that fits your total, keep it equal between siblings, and count stocking stuffers inside it, not on top."),
        ("How much should I save each month for Christmas?", "Divide your Christmas total by the months left before you shop. Starting in January, a $1,250 Christmas is $104.17 a month."),
        ("What costs do people forget in a Christmas budget?", "Food and hosting, travel, wrapping paper, cards and postage, stocking stuffers, outfits for parties, and gifts for teachers, coworkers and neighbors. Give each one its own line."),
    ],
    related=["break-even-calculator", "invoice-late-fee-calculator", "profit-margin-calculator"],
    cta_head="Track every gift and every payday",
    cta_text="The <strong>Christmas Budget Planner &amp; Gift Tracker</strong> keeps a budget per person, a gift list with status from idea to wrapped, every other holiday cost, and works out how much to set aside each payday. Google Sheets and Excel, with a filled-in demo and printable worksheets. One-time $5.",
    cta_url="https://quietprofitsheets.gumroad.com/l/christmas-budget-planner",
    cta_btn="Get the Christmas Budget Planner",
    og_image="pins/feed/christmas-budget-calculator.png",
    tests=[
        {"set": {"weeks": "8"}, "expect": {"big": "$237.50", "rows": ["$725.00", "$525.00", "$1,250.00", "$950.00", "$118.75", "$104.17"], "verdict": ["13.2%", "4 paydays"]}},
        {"set": {"weeks": "8", "freq": "1"}, "expect": {"big": "$118.75", "rows": "8"}},
        {"set": {"weeks": "8", "freq": "4.333"}, "expect": {"big": "$950.00"}},
        {"set": {"weeks": "8", "saved": "1300"}, "expect": {"big": "$0.00", "verdict": "already set aside"}},
        {"set": {"weeks": "8", "pay": "800"}, "expect": {"verdict": ["29.7%", "a lot"]}},
        {"set": {"weeks": "8", "kids": "0", "adults": "0", "others": "0", "food": "0", "travel": "0", "decor": "0", "wrap": "0"}, "expect": {"big": "-", "verdict": "Add the people"}},
    ],
)
