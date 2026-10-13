PAGE = dict(
    slug="ebay-fee-calculator",
    cat="Platform fees",
    nav_name="eBay fee calculator",
    title="eBay Fee Calculator 2026: Final Value Fee, Ads and What You Keep",
    desc="Free eBay fee calculator: final value fee on item, shipping and tax, per-order fee, promoted listing ad rate and Top Rated Plus discount, plus your profit.",
    h1="eBay fee calculator",
    lead="Enter one eBay sale. The calculator applies the final value fee to the full amount the buyer pays, sales tax included, adds the per-order fee and any promoted listing fee, then takes off your item cost and shipping label to show what you keep.",
    form="""      <label for="item">Sold price of the item</label>
      <div class="in"><span>$</span><input id="item" type="number" inputmode="decimal" min="0" step="0.01" value="40"></div>
      <label for="ship">Shipping you charge the buyer</label>
      <div class="in"><span>$</span><input id="ship" type="number" inputmode="decimal" min="0" step="0.01" value="8"></div>
      <label for="tax">Buyer's sales tax rate <small>(eBay collects and remits it)</small></label>
      <div class="in"><input id="tax" type="number" inputmode="decimal" min="0" step="0.1" value="8"><span>%</span></div>
      <label for="ad">Promoted listing ad rate <small>(0 if not promoted, or the sale didn't come from the ad)</small></label>
      <div class="in"><input id="ad" type="number" inputmode="decimal" min="0" step="0.1" value="0"><span>%</span></div>
      <label for="cost">What the item cost you</label>
      <div class="in"><span>$</span><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="12"></div>
      <label for="label">Shipping label you pay</label>
      <div class="in"><span>$</span><input id="label" type="number" inputmode="decimal" min="0" step="0.01" value="6"></div>
      <label class="check"><input id="trs" type="checkbox"> I'm Top Rated with a Top Rated Plus listing (10% off the final value fee)</label>
      <details><summary class="note">Edit fee rates</summary>
      <label for="fvf">Final value fee for your category</label>
      <div class="in"><input id="fvf" type="number" min="0" step="0.1" value="13.6"><span>%</span></div>
      <label for="po">Per-order fee</label>
      <div class="in"><span>$</span><input id="po" type="number" min="0" step="0.01" value="0.40"></div>
      <label for="pos">Per-order fee on small orders</label>
      <div class="in"><span>$</span><input id="pos" type="number" min="0" step="0.01" value="0.30"></div>
      <label for="thr">Small order means a total of up to</label>
      <div class="in"><span>$</span><input id="thr" type="number" min="0" step="0.01" value="10"></div>
      </details>""",
    out="""<div class="big"><span>You keep</span><b id="keep"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var base=n('item')+n('ship'),tax=base*n('tax')/100,tot=base+tax;
  if(!base){$('keep').textContent=m(0);setRows([['Enter the sold price to see eBay fees.','']]);verdict(false,'No sale entered yet.');return}
  var fv=tot*n('fvf')/100,disc=$('trs').checked?fv*0.1:0,po=tot>n('thr')?n('po'):n('pos'),ad=tot*n('ad')/100;
  var fees=fv-disc+po+ad,costs=n('cost')+n('label'),keep=base-fees-costs;
  var r=[['Buyer pays (item + shipping + tax)',m(tot)],['Sales tax, passed to the state',m(-tax)],['Final value fee ('+n('fvf')+'% of '+m(tot)+')',m(-fv)]];
  if(disc)r.push(['Top Rated Plus discount (10%)',m(disc)]);
  r.push(['Per-order fee',m(-po)]);
  if(ad)r.push(['Promoted listing ('+n('ad')+'%)',m(-ad)]);
  r.push(['Total eBay fees',m(-fees)+' ('+pc(fees/base)+')'],['Item cost + label',m(-costs)],['You keep',m(keep),'total']);
  setRows(r);$('keep').textContent=m(keep);
  if(keep<0)verdict(false,'This sale loses '+m(-keep)+'. Raise the price or the shipping charge, or drop the ad rate.');
  else verdict(true,'eBay takes '+pc(fees/base)+' of the '+m(base)+' you charged. Your profit is '+pc(keep/base,0)+' of it.');
}""",
    note="US eBay rates as of October 2026: final value fee 13.6% for most categories, charged on the total the buyer pays including shipping and sales tax, plus $0.40 per order ($0.30 if the order total is $10 or less). Some categories charge more or less, and higher rates can apply above a price cap, so set your category's rate under Edit fee rates. The Top Rated Plus discount is applied to the percentage part of the final value fee only.",
    body="""<h2>How eBay fees work</h2>
<p><strong>Final value fee.</strong> eBay takes a percentage of the whole order: the item price, the shipping you charge and the sales tax the buyer pays. For most categories that is 13.6%. You don't keep the tax, but you still pay the fee on it.</p>
<p><strong>Per-order fee.</strong> A fixed $0.40 on every order, or $0.30 if the order total is $10 or less.</p>
<p><strong>Promoted listings.</strong> If you promote a listing at a chosen ad rate and the sale comes through the ad, eBay charges that rate on the same order total. A 5% ad rate costs you more than a third of the final value fee again.</p>
<p><strong>Top Rated Plus.</strong> Top Rated sellers get 10% off the final value fee on listings that qualify (fast handling and free 30-day returns). It is a discount on the fee, not 10% of the sale.</p>
<h2>The formula</h2>
<p class="formula">eBay fees = (item + shipping + tax) x (FVF % + ad %) + per-order fee</p>
<p>Example: a $40 item with $8 shipping to a buyer who pays 8% sales tax. The buyer pays $51.84, of which $3.84 is tax. The final value fee is $7.05 and the per-order fee $0.40, so eBay keeps $7.45, which is 15.5% of the $48 you charged. After a $12 item cost and a $6 label you keep <strong>$22.55</strong>.</p>
<p>Promote the same listing at 5% and the ad adds $2.59, leaving $19.96. Without the ad but with Top Rated Plus, the final value fee drops by $0.71 and you keep $23.25.</p>
<h2>Pricing tips</h2>
<p>Because the fee is charged on shipping too, moving cost from the item price into the shipping charge does not save fees. Price your item so it still makes money after roughly 15% to 16% of the total goes to eBay, more if you promote. On small sales the fixed fee hurts most: an $8 item with free shipping pays $1.39 in fees, over 17% of the sale.</p>""",
    faqs=[
        ("Does eBay charge fees on sales tax?", "Yes. The final value fee is calculated on the total amount of the sale, which includes sales tax. On a $48 order with 8% tax, you pay the fee on $51.84."),
        ("How much does eBay take from a $40 sale?", "With $8 shipping and 8% tax, $7.45 in total: $7.05 final value fee plus the $0.40 per-order fee, at the 13.6% rate. Your category rate may differ."),
        ("How is the promoted listing fee calculated?", "It is your ad rate times the same total the final value fee uses, item plus shipping plus tax. A 5% ad rate on a $51.84 order costs $2.59, charged only when the sale is attributed to the ad."),
        ("What is the eBay per-order fee?", "$0.40 per order, or $0.30 when the order total is $10 or less. On an $8 order with free shipping and no tax, fees come to $1.39 including the $0.30."),
    ],
    related=["etsy-vs-ebay", "amazon-fba-calculator", "poshmark-fee-calculator", "profit-margin-calculator", "markup-calculator"],
    og_image="pins/pin-03.png",
    tests=[
        {"expect": {"rows": ["$51.84", "-$3.84", "-$7.05", "-$0.40", "-$7.45", "15.5%", "-$18.00"], "keep": "$22.55"}},
        {"set": {"ad": "5"}, "expect": {"rows": "-$2.59", "keep": "$19.96"}},
        {"click": ["trs"], "expect": {"rows": "$0.71", "keep": "$23.25"}},
        {"set": {"item": "8", "ship": "0", "tax": "0", "cost": "0", "label": "0"}, "expect": {"rows": ["-$0.30", "-$1.09", "-$1.39", "17.4%"]}},
        {"set": {"item": "", "ship": ""}, "expect": {"verdict": "No sale entered"}},
    ],
)
