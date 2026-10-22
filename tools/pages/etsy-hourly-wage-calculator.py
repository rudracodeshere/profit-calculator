PAGE = dict(
    slug="etsy-hourly-wage-calculator",
    cat="Etsy tools", starter_line=True, pin_save=True,
    nav_name="Etsy hourly wage calculator",
    title="Etsy Hourly Wage Calculator: Are You Paying Yourself?",
    desc="Find your real hourly pay on Etsy after fees, materials and labels, counting time to make, pack and list. Then see the price that pays your target wage.",
    h1="Etsy hourly wage calculator: are you paying yourself?",
    lead="Take your current price, subtract Etsy's fees, materials and the label, and divide what's left by all the time one sale takes: making it, packing it, and your share of photographing and listing. That's your real hourly wage. Then see what price would pay the wage you want.",
    form="""      <label for="price">Item price</label>
      <div class="in"><span>$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="36"></div>
      <label for="ship">Shipping you charge <small>(0 for free shipping)</small></label>
      <div class="in"><span>$</span><input id="ship" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
      <label for="mat">Materials + packaging</label>
      <div class="in"><span>$</span><input id="mat" type="number" inputmode="decimal" min="0" step="0.01" value="9"></div>
      <label for="label">Shipping label you pay</label>
      <div class="in"><span>$</span><input id="label" type="number" inputmode="decimal" min="0" step="0.01" value="5"></div>
      <label for="tmake">Minutes to make one</label>
      <div class="in"><input id="tmake" type="number" inputmode="decimal" min="0" step="5" value="60"><span>min</span></div>
      <label for="tpack">Minutes to pack and ship it</label>
      <div class="in"><input id="tpack" type="number" inputmode="decimal" min="0" step="1" value="10"><span>min</span></div>
      <label for="tlist">Minutes of photos, listing and messages per sale <small>(total time &divide; items sold)</small></label>
      <div class="in"><input id="tlist" type="number" inputmode="decimal" min="0" step="1" value="10"><span>min</span></div>
      <label for="target">Hourly wage you want</label>
      <div class="in"><span>$</span><input id="target" type="number" inputmode="decimal" min="0" step="0.5" value="20"><span>/hr</span></div>
      <label for="minw">Minimum wage where you live</label>
      <div class="in"><span>$</span><input id="minw" type="number" inputmode="decimal" min="0" step="0.25" value="15"><span>/hr</span></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="tx">Transaction fee</label>
      <div class="in"><input id="tx" type="number" min="0" step="0.1" value="6.5"><span>%</span></div>
      <label for="pp">Payment processing</label>
      <div class="in"><input id="pp" type="number" min="0" step="0.1" value="3"><span>% +</span><span>$</span><input id="pf" type="number" min="0" step="0.01" value="0.25"></div>
      <label for="lfee">Listing fee per item sold</label>
      <div class="in"><span>$</span><input id="lfee" type="number" min="0" step="0.01" value="0.20"></div>
      </details>""",
    out="""<div class="big"><span>Your real hourly wage</span><b id="wage"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var p=n('price'),s=n('ship'),c=n('mat')+n('label'),mk=n('tmake'),mins=mk+n('tpack')+n('tlist'),h=mins/60;
  var rate=(n('tx')+n('pp'))/100,fix=n('pf')+n('lfee'),t=p+s,fees=t*rate+fix,k=t-fees-c;
  function priceFor(w){return Math.max(0,(w*h+c+fix)/(1-rate)-s)}
  if(!mins){$('wage').textContent='-';setRows([]);verdict(false,'Enter how many minutes one sale takes you to see your hourly wage.');return}
  if(!p){$('wage').textContent='-';setRows([]);verdict(false,'Enter your item price.');return}
  var w=k/h,tw=n('target'),mw=n('minw');
  $('wage').textContent=m(w)+'/hr';
  var r=[['Buyer pays',m(t)],['Etsy fees',m(-fees)],['Materials + packaging',m(-n('mat'))],['Shipping label',m(-n('label'))],['Left to pay you',m(k),'total'],['Time per sale',Math.round(mins)+' min ('+h.toFixed(2)+' hrs)']];
  if(mk&&mk<mins)r.push(['Wage counting making time only',m(k/(mk/60))+'/hr']);
  if(tw)r.push(['Price for '+m(tw)+'/hr',m(priceFor(tw))]);
  if(mw)r.push(['Price for minimum wage ('+m(mw)+'/hr)',m(priceFor(mw))]);
  setRows(r);
  if(k<0)verdict(false,'You pay '+m(-k)+' to sell each one, before counting your time. Charge at least '+m(priceFor(0))+' just to cover costs.');
  else if(mw&&w<mw)verdict(false,'You earn '+m(w)+' an hour, under the '+m(mw)+' minimum wage. Charge '+m(priceFor(tw||mw))+' to pay yourself '+m(tw||mw)+'/hr.');
  else if(tw&&w<tw)verdict(false,'You earn '+m(w)+' an hour, above minimum wage but short of your '+m(tw)+' target. '+m(priceFor(tw))+' gets you there.');
  else verdict(true,'You pay yourself '+m(w)+' an hour for every minute of the sale, not just the making.');
}""",
    note="US Etsy rates as of October 2026: 6.5% transaction fee and 3% + $0.25 processing on the order total (item + shipping), $0.20 listing fee per item sold. One item per order, no Offsite Ads, no sales tax. The wage is before income tax and self-employment tax. Minimum wages vary by state and city, so enter yours.",
    body="""<h2>How your real hourly wage is worked out</h2>
<p>Everything left after Etsy's fees, materials and the label is what pays you. Divide it by all the time a sale takes, not only the making. Packing, printing the label, the post office run, photographing and writing the listing, and answering buyer messages are all part of the job. For listing time, take the hours you spent on photos and listings this month and divide by the items you sold.</p>
<p class="formula">Hourly wage = (price + shipping &minus; Etsy fees &minus; materials &minus; label) &divide; hours per sale</p>
<p>To find the price that pays a target wage, the fees have to be solved for, because they grow with the price:</p>
<p class="formula">Price = (wage &times; hours + materials + label + $0.45) &divide; (1 &minus; 9.5%) &minus; shipping charged</p>
<h2>Worked example</h2>
<p>A $36 item with free shipping, $9 in materials and packaging, and a $5 label. Etsy takes $3.87, which leaves <strong>$18.13</strong>. It takes 60 minutes to make, 10 to pack and 10 of listing and admin, 80 minutes in total. That is <strong>$13.60 an hour</strong>, under a $15 minimum wage.</p>
<p>Counting only the hour of making, it looks like $18.13 an hour. The 20 minutes of packing and admin are what pull it under minimum wage.</p>
<p>To earn $20 an hour the price has to be <strong>$45.43</strong>. To match a $15 minimum wage it needs <strong>$38.07</strong>. At $50 the wage would be $23.10.</p>
<h2>What to do if the number is low</h2>
<p><strong>Raise the price first.</strong> In the example, going from $36 to $45.43 takes the wage from $13.60 to $20. Testing a higher price on a few listings costs you nothing but a few weeks.</p>
<p><strong>Cut time that isn't making.</strong> Batch your photography, reuse listing templates, buy labels online in one session. Time you save on admin raises your hourly wage without touching the price.</p>
<p><strong>Make in batches.</strong> Twenty of an item rarely take twenty times as long as one. Time a batch and divide by the count for a truer minutes-to-make.</p>
<p>The minutes per item vary across a catalog, and so does the wage. Matching your sales export to time per product shows which listings are paying you and which are a hobby.</p>""",
    faqs=[
        ("How do I calculate my hourly wage selling on Etsy?", "Subtract Etsy's fees, materials and the shipping label from what the buyer pays, then divide by the hours one sale takes, including packing and listing time. The $36 example leaves $18.13 for 80 minutes, which is $13.60 an hour."),
        ("Should I include listing and photography time?", "Yes. It is real work the sale depends on. Spread it across your sales: if you spend 5 hours a month on photos and listings and sell 30 items, that is 10 minutes per sale."),
        ("What should I charge to pay myself $20 an hour on Etsy?", "Add your wage for the time, materials, label and $0.45 of fixed fees, then divide by 0.905 to cover the 9.5% Etsy takes. For 80 minutes of work with $14 of costs, that is $45.43."),
        ("Is it normal to earn less than minimum wage on Etsy?", "Many makers do, often because they count only making time. If your number is under minimum wage, the calculator shows the price that fixes it: $38.07 for the example to reach $15 an hour."),
    ],
    related=["etsy-pricing-calculator", "handmade-pricing-calculator", "etsy-profit-calculator", "etsy-fee-calculator", "price-increase-calculator"],
    og_image="pins/pin-07.png",
    tests=[
        {"expect": {"wage": ["$13.60/hr"], "rows": ["$36.00", "-$3.87", "$18.13", "80 min", "$18.13/hr", "$45.43", "$38.07"], "verdict": ["under the $15.00 minimum"]}},
        {"set": {"price": "50"}, "expect": {"wage": ["$23.10/hr"], "verdict": ["You pay yourself $23.10"]}},
        {"set": {"price": "25", "tmake": "45", "tpack": "5", "tlist": "10", "target": "18", "minw": "12"}, "expect": {"rows": ["$10.90/hr", "$35.86", "$29.23"], "verdict": ["under the $12.00 minimum"]}},
        {"set": {"price": "36", "minw": "0", "target": "16"}, "expect": {"verdict": ["short of your $16.00 target"]}},
        {"set": {"tmake": "0", "tpack": "0", "tlist": "0"}, "expect": {"verdict": ["Enter how many minutes"]}},
    ],
)
