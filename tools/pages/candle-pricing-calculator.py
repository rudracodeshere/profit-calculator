PAGE = dict(
    slug="candle-pricing-calculator",
    cat="Maker pricing", starter_line=True,
    nav_name="Candle pricing calculator",
    title="Candle Pricing Calculator: Cost per Candle and Retail Price",
    desc="Cost one candle from wax, fragrance load (as % of wax), wick, vessel, label and labor. Get a retail price, a wholesale check and a batch shopping list.",
    h1="Candle pricing calculator",
    lead="Enter your wax and fragrance prices, how much goes in each candle and what the rest of the candle costs. You get the cost per candle, a suggested retail price, a wholesale check and how much wax and oil a batch needs.",
    form="""      <label for="wp">Wax price</label>
      <div class="in"><span>$</span><input id="wp" type="number" inputmode="decimal" min="0" step="0.01" value="3.50"><span>per lb</span></div>
      <label for="wo">Wax per candle</label>
      <div class="in"><input id="wo" type="number" inputmode="decimal" min="0" step="0.1" value="8"><span>oz (weight)</span></div>
      <label class="check"><input id="fill" type="checkbox"> That's the total fill weight (wax + oil), not wax alone</label>
      <label for="fl">Fragrance load <small>(% of wax weight)</small></label>
      <div class="in"><input id="fl" type="number" inputmode="decimal" min="0" step="0.5" value="8"><span>%</span></div>
      <label for="op">Fragrance oil price</label>
      <div class="in"><span>$</span><input id="op" type="number" inputmode="decimal" min="0" step="0.01" value="2.00"><span>per oz</span></div>
      <label for="wk">Wick (with sustainer / sticker)</label>
      <div class="in"><span>$</span><input id="wk" type="number" inputmode="decimal" min="0" step="0.01" value="0.15"></div>
      <label for="vs">Vessel (jar, tin)</label>
      <div class="in"><span>$</span><input id="vs" type="number" inputmode="decimal" min="0" step="0.01" value="2.50"></div>
      <label for="lb">Label and lid</label>
      <div class="in"><span>$</span><input id="lb" type="number" inputmode="decimal" min="0" step="0.01" value="0.60"></div>
      <label for="pk">Packaging <small>(box, warning sticker, filler)</small></label>
      <div class="in"><span>$</span><input id="pk" type="number" inputmode="decimal" min="0" step="0.01" value="0.72"></div>
      <label for="mn">Labor per candle <small>(pour, cure, wick trim, label)</small></label>
      <div class="in"><input id="mn" type="number" inputmode="decimal" min="0" step="1" value="15"><span>minutes</span></div>
      <label for="hr">Your hourly rate</label>
      <div class="in"><span>$</span><input id="hr" type="number" inputmode="decimal" min="0" step="0.5" value="20"><span>/ hour</span></div>
      <label for="mu">Retail price multiplier <small>(x cost per candle)</small></label>
      <div class="in"><input id="mu" type="number" inputmode="decimal" min="0" step="0.1" value="3"><span>x</span></div>
      <label for="bt">Batch size</label>
      <div class="in"><input id="bt" type="number" inputmode="decimal" min="0" step="1" value="24"><span>candles</span></div>""",
    out="""<div class="big"><span>Suggested retail price</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>
      <h3>Batch</h3>
      <table><tbody id="batch"></tbody></table>""",
    js="""function f2(x){return x.toFixed(2)}
function calc(){
  var w=n('wo'),L=n('fl')/100,wax=$('fill').checked?w/(1+L):w,oil=wax*L;
  var wc=wax/16*n('wp'),oc=oil*n('op');
  var mat=wc+oc+n('wk')+n('vs')+n('lb')+n('pk'),lab=n('mn')/60*n('hr'),cost=mat+lab;
  var rt=cost*n('mu'),ws=rt/2,wpro=ws-cost,wm=ws?wpro/ws:0,b=Math.round(n('bt'));
  $('big').textContent=m(rt);
  setRows([['Wax ('+f2(wax)+' oz at '+m(n('wp'))+'/lb)',m(wc)],['Fragrance oil ('+f2(oil)+' oz)',m(oc)],['Wick',m(n('wk'))],['Vessel',m(n('vs'))],['Label and lid',m(n('lb'))],['Packaging',m(n('pk'))],
    ['Materials',m(mat)],['Labor ('+n('mn')+' min)',m(lab)],['Cost per candle',m(cost),'total'],
    ['Total pour weight',f2(wax+oil)+' oz'],['Oil as a share of the whole candle',(wax+oil)?pc(oil/(wax+oil)):'0%'],
    ['Retail ('+n('mu')+'x cost)',m(rt)],['Wholesale at half of retail',m(ws)],['Wholesale profit',m(wpro)+' ('+pc(wm)+')']]);
  setRows([['Wax to melt',f2(wax*b/16)+' lb ('+f2(wax*b)+' oz)'],['Fragrance oil to weigh out',f2(oil*b)+' oz'],['Batch cost ('+b+' candles)',m(cost*b)],['Batch value at retail',m(rt*b),'total']],'batch');
  if(!cost){verdict(false,'Enter your wax, vessel and other costs to price a candle.');return}
  if(wm<0.3)verdict(false,'If a shop buys at half of retail ('+m(ws)+'), you make '+m(wpro)+' a candle. For a 50% wholesale margin, retail at 4x cost: '+m(cost*4)+'.');
  else verdict(true,'Each candle costs '+m(cost)+'. At '+m(rt)+' retail you can still wholesale at '+m(ws)+' and make '+m(wpro)+' a candle.');
}""",
    note="All prices are your own supplier prices; nothing here is a live or typical price. Fragrance load is calculated on wax weight, the way most wax suppliers state their maximum load. Weigh oil, don't measure it by volume. Fees for selling on Etsy or elsewhere are not included. As of October 2026.",
    body="""<h2>Fragrance load is a percentage of the wax</h2>
<p>This is the mistake that throws off candle costs and scent throw. An 8% fragrance load means the oil weighs 8% of the <strong>wax</strong>, not 8% of the finished candle. For 8 oz of wax that is 0.64 oz of oil, and the candle weighs 8.64 oz in total. Oil makes up only 7.4% of that total, but the load is still 8%, because load is measured against the wax.</p>
<p class="formula">Oil (oz) = wax (oz) x fragrance load &nbsp;|&nbsp; Wax cost = wax oz / 16 x price per lb</p>
<p>If you know your vessel's total fill weight instead (say 8 oz of wax and oil together), divide by 1 plus the load to get the wax: 8 / 1.08 = 7.41 oz of wax and 0.59 oz of oil. Tick the fill-weight box above and the calculator does this for you. Check your wax supplier's sheet for the maximum load it holds; going over it can make oil sweat out of the wax.</p>
<h2>A worked example</h2>
<p>A candle with 8 oz of soy wax at $3.50 a pound uses $1.75 of wax. At 8% load it needs 0.64 oz of fragrance oil, which at $2.00 an ounce is $1.28. Add a $0.15 wick, a $2.50 jar, $0.60 for the label and lid, and $0.72 of packaging, and the materials come to <strong>$7.00</strong>. Fifteen minutes of labor at $20 an hour is $5.00, so the candle costs <strong>$12.00</strong>.</p>
<p>At 3x cost the retail price is <strong>$36.00</strong>. A shop buying at half of retail pays $18.00, which still leaves you $6.00 a candle, a 33.3% margin. A batch of 24 needs 12.00 lb of wax and 15.36 oz of oil, costs $288.00 and is worth $864.00 at retail.</p>
<h2>Costs candle makers leave out</h2>
<p>Test burns, the jars that crack, warning labels, the dust cover and the box all belong in the cost per candle. So does your time for pouring, curing, trimming wicks and labeling, not just the minutes the wax is in the pot. If you sell online, marketplace fees and the shipping you absorb come out of the retail price too, so check it with the <a href="../etsy-fee-calculator/">Etsy fee calculator</a> once you have a price.</p>""",
    faqs=[
        ("How do I calculate how much fragrance oil to use?", "Multiply the wax weight by the fragrance load. 8 oz of wax at an 8% load takes 0.64 oz of oil. Weigh both on a scale; fluid ounces of oil are not the same as ounces by weight."),
        ("Is fragrance load based on wax weight or total weight?", "Wax weight, in the way most suppliers state it. If you only know the total fill weight, divide it by 1 plus the load to find the wax: an 8 oz fill at 8% is 7.41 oz of wax and 0.59 oz of oil."),
        ("How much should I charge for a candle?", "Start from your full cost per candle, labor included, and multiply. A candle that costs $12.00 to make sells for $36.00 at 3x, which leaves room for a shop to buy it at $18.00. If you plan to wholesale a lot, 4x cost gives you a 50% wholesale margin."),
        ("How much wax do I need for 24 candles?", "Multiply the wax per candle by 24 and divide by 16 for pounds. At 8 oz each, that is 12.00 lb of wax plus 15.36 oz of fragrance oil at an 8% load."),
    ],
    related=["handmade-pricing-calculator", "wholesale-price-calculator", "etsy-pricing-calculator", "cogs-calculator", "etsy-fee-calculator"],
    og_image="pins/pin-10.png",
    tests=[
        {"expect": {"big": "$36.00", "rows": ["$1.75", "0.64 oz", "$1.28", "$7.00", "$5.00", "$12.00", "8.64 oz", "7.4%", "$18.00", "$6.00 (33.3%)"], "batch": ["12.00 lb", "15.36 oz", "$288.00", "$864.00"], "verdict": "$6.00"}},
        {"click": ["fill"], "expect": {"rows": ["7.41 oz", "0.59 oz", "8.00 oz", "$11.78"], "big": "$35.33"}},
        {"set": {"mu": "2"}, "expect": {"big": "$24.00", "verdict": "$48.00"}},
        {"set": {"mu": "4"}, "expect": {"big": "$48.00", "rows": "50.0%"}},
        {"set": {"wo": "0", "wk": "0", "vs": "0", "lb": "0", "pk": "0", "mn": "0"}, "expect": {"big": "$0.00", "rows": "0%", "verdict": "Enter your wax"}},
    ],
)
