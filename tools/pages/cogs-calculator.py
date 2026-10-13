PAGE = dict(
    slug="cogs-calculator",
    cat="Pricing & margins",
    nav_name="COGS calculator",
    title="COGS Calculator: Cost of Goods Sold per Unit and per Period",
    desc="Free COGS calculator for online sellers. Work out cost per unit from a production batch, or cost of goods sold for a period from inventory and purchases.",
    h1="COGS calculator (cost of goods sold)",
    lead="Two ways to get your cost of goods sold. Per unit: enter what one batch cost to make or buy and how many units it produced. Per period: enter your inventory at the start and end and what you bought in between.",
    form="""      <label for="mode">What do you want to calculate?</label>
      <select id="mode" class="full">
        <option value="batch">Cost per unit from a batch</option>
        <option value="period">COGS for a period (month, quarter, year)</option>
      </select>
      <div id="fBatch">
      <label for="mat">Materials or product cost for the batch</label>
      <div class="in"><span>$</span><input id="mat" type="number" inputmode="decimal" min="0" step="0.01" value="180"></div>
      <label for="pack">Packaging for the batch</label>
      <div class="in"><span>$</span><input id="pack" type="number" inputmode="decimal" min="0" step="0.01" value="24"></div>
      <label for="frt">Inbound shipping and duties <small>(getting supplies to you)</small></label>
      <div class="in"><span>$</span><input id="frt" type="number" inputmode="decimal" min="0" step="0.01" value="36"></div>
      <label for="lab">Labor <small>(optional: paid help, or your own time at an hourly rate)</small></label>
      <div class="in"><span>$</span><input id="lab" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
      <label for="units">Units the batch produced</label>
      <div class="in"><input id="units" type="number" inputmode="numeric" min="0" step="1" value="60"></div>
      <label for="price">Selling price per unit <small>(optional)</small></label>
      <div class="in"><span>$</span><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="18"></div>
      </div>
      <div id="fPeriod" style="display:none">
      <label for="beg">Beginning inventory <small>(at cost)</small></label>
      <div class="in"><span>$</span><input id="beg" type="number" inputmode="decimal" min="0" step="0.01" value="2000"></div>
      <label for="buy">Purchases during the period <small>(stock, materials, inbound freight)</small></label>
      <div class="in"><span>$</span><input id="buy" type="number" inputmode="decimal" min="0" step="0.01" value="3500"></div>
      <label for="end">Ending inventory <small>(at cost)</small></label>
      <div class="in"><span>$</span><input id="end" type="number" inputmode="decimal" min="0" step="0.01" value="1800"></div>
      <label for="rev">Net sales for the period <small>(optional)</small></label>
      <div class="in"><span>$</span><input id="rev" type="number" inputmode="decimal" min="0" step="0.01" value="9000"></div>
      </div>""",
    out="""<div class="big"><span id="bigLabel">COGS per unit</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var per=$('mode').value==='period';
  $('fBatch').style.display=per?'none':'';$('fPeriod').style.display=per?'':'none';
  if(!per){
    $('bigLabel').textContent='COGS per unit';
    var tot=n('mat')+n('pack')+n('frt')+n('lab'),u=Math.round(n('units')),p=n('price');
    if(!u){$('big').textContent='-';setRows([['Batch cost',m(tot)]]);verdict(false,'Enter how many units the batch produced.');return}
    var c=tot/u,r=[['Materials',m(n('mat'))],['Packaging',m(n('pack'))],['Inbound shipping',m(n('frt'))]];
    if(n('lab'))r.push(['Labor',m(n('lab'))]);
    r.push(['Total batch cost',m(tot)],['Units',u],['COGS per unit',m(c),'total']);
    $('big').textContent=m(c);
    if(p){r.push(['Gross profit per unit',m(p-c)],['Gross margin',pc((p-c)/p)])}
    setRows(r);
    if(!p)verdict(true,'Each unit costs '+m(c)+'. Enter a selling price to see the gross margin.');
    else verdict(p-c>0,p-c>0?'Each unit costs '+m(c)+' and sells for '+m(p)+', leaving '+m(p-c)+' before fees and shipping.':'Each unit costs more than it sells for. Raise the price or lower the batch cost.');
  }else{
    $('bigLabel').textContent='Cost of goods sold';
    var b=n('beg'),pu=n('buy'),e=n('end'),s=n('rev'),cg=b+pu-e;
    if(cg<0){$('big').textContent='-';setRows([['Available for sale',m(b+pu)],['Ending inventory',m(e)]]);verdict(false,'Ending inventory is larger than what you started with plus what you bought. Check the counts or missing purchases.');return}
    $('big').textContent=m(cg);
    var rr=[['Beginning inventory',m(b)],['+ Purchases',m(pu)],['= Available for sale',m(b+pu)],['- Ending inventory',m(-e)],['Cost of goods sold',m(cg),'total']];
    if(s)rr.push(['Net sales',m(s)],['Gross profit',m(s-cg)],['Gross margin',pc((s-cg)/s)]);
    setRows(rr);
    if(!s)verdict(true,'You sold '+m(cg)+' worth of inventory at cost. Enter net sales to see gross profit.');
    else verdict(s>cg,s>cg?'Gross profit is '+m(s-cg)+' on '+m(s)+' of sales. Fees, ads and overhead still come out of that.':'Your goods cost more than you sold them for this period.');
  }
}""",
    note="For planning, not tax advice. Value inventory at what you paid, not retail price. Inventory rules differ by country and business type; ask a tax professional how they apply to you. Guidance as of October 2026.",
    body="""<h2>What goes into COGS</h2>
<p>Cost of goods sold is what the items you sold cost you to make or buy. For an online seller that usually means materials or wholesale stock, packaging that ships with the product, and inbound shipping or import duties to get supplies to you. Direct labor counts if you pay someone to make the product.</p>
<p>It does not include selling costs: marketplace fees, payment processing, outbound shipping labels, ads or software. Those are expenses, but they belong lower down your profit and loss, and mixing them into COGS makes your gross margin look worse than it is.</p>
<h2>COGS per unit from a batch</h2>
<p class="formula">COGS per unit = (materials + packaging + inbound freight + labor) / units produced</p>
<p>Example: a batch of 60 candles takes $180 of wax, wicks, fragrance and jars, $24 of boxes and labels, and $36 of freight on the supplies. That is $240, or <strong>$4.00</strong> per candle. At an $18 price the gross profit is $14.00 per candle, a 77.8% gross margin. If you count 5 hours of your own time at $20, the batch costs $340 and each candle $5.67.</p>
<p>Whether to include your own time is a choice. Leaving it out tells you cash cost. Putting it in tells you whether the price pays you a wage.</p>
<h2>COGS for a month, quarter or year</h2>
<p class="formula">COGS = beginning inventory + purchases - ending inventory</p>
<p>Example: you started the quarter with $2,000 of stock at cost, bought $3,500 more and counted $1,800 left at the end. You sold <strong>$3,700</strong> of inventory. On $9,000 of net sales that is $5,300 of gross profit, a 58.9% gross margin.</p>
<p>This method needs an actual count at the end of the period. If you skip it, your COGS will be off by however much stock went missing, broke or was used for samples.</p>
<p>US sole proprietors filing Schedule C will see cost of goods sold on line 4, worked out in Part III. That is only a pointer to where the number goes; the IRS instructions and a tax professional decide what you include.</p>""",
    faqs=[
        ("Is shipping included in COGS?", "Inbound shipping to get stock or materials to you usually is. Outbound shipping labels to customers are a selling cost, not COGS, even though you pay them per order."),
        ("Are Etsy or Shopify fees part of cost of goods sold?", "No. Marketplace and payment fees are selling expenses. Keep them out of COGS so your gross margin compares products fairly, then subtract fees separately to get net profit."),
        ("How do I calculate COGS if I make products myself?", "Add up a batch's materials, packaging and inbound freight, then divide by the units it made. $240 for 60 units is $4.00 each. Add labor if you pay a maker or want to price in your own time."),
        ("What if I don't track inventory?", "Count what you have on hand once at the start and end of the period, valued at what you paid. Then COGS is beginning inventory plus purchases minus ending inventory: $2,000 + $3,500 - $1,800 = $3,700."),
    ],
    related=["profit-margin-calculator", "handmade-pricing-calculator", "candle-pricing-calculator", "break-even-calculator", "markup-calculator"],
    og_image="pins/pin-09.png",
    tests=[
        {"expect": {"big": "$4.00", "rows": ["$240.00", "$14.00", "77.8%"]}},
        {"set": {"lab": "100"}, "expect": {"big": "$5.67", "rows": ["$340.00"]}},
        {"set": {"mode": "period"}, "expect": {"big": "$3,700.00", "rows": ["$5,500.00", "$5,300.00", "58.9%"]}},
        {"set": {"units": "0"}, "expect": {"big": "-", "verdict": "Enter how many units"}},
        {"set": {"mode": "period", "end": "9000"}, "expect": {"big": "-", "verdict": "Check the counts"}},
        {"set": {"mode": "period", "rev": "0"}, "expect": {"verdict": "Enter net sales"}},
    ],
)
