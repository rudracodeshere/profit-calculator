PAGE = dict(
    slug="tiktok-shop-fee-calculator",
    cat="Platform fees",
    nav_name="TikTok Shop fee calculator",
    title="TikTok Shop Fee Calculator (US, 2026): Referral Fee, Commission and Profit",
    desc="Free TikTok Shop fee calculator for US sellers: 6% referral fee on item plus shipping, creator affiliate commission, optional Smart Promotion fee, refund admin fee and what you keep.",
    h1="TikTok Shop fee calculator",
    lead="For most US categories TikTok Shop takes a 6% referral fee on the item price plus the shipping the buyer pays (5% for some fine jewelry and pre-owned items). If a creator made the sale, you also pay their commission on the item price only. Enter one order to see the referral fee, the creator commission, Smart Promotion if you are enrolled, and what you keep after your item cost and label.",
    form="""      <label for="item">Item price <small>(before any discount you fund)</small></label>
      <div class="in"><span>$</span><input id="item" type="number" inputmode="decimal" min="0" step="0.01" value="30"></div>
      <label for="ship">Shipping the buyer pays</label>
      <div class="in"><span>$</span><input id="ship" type="number" inputmode="decimal" min="0" step="0.01" value="4"></div>
      <label for="disc">Discount you fund <small>(your coupon, price cut or share of a co-funded deal; leave out discounts TikTok pays for)</small></label>
      <div class="in"><span>$</span><input id="disc" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
      <label for="aff">Creator affiliate commission <small>(0 if you sold it yourself)</small></label>
      <div class="in"><input id="aff" type="number" inputmode="decimal" min="0" step="0.1" value="15"><span>%</span></div>
      <label for="sp">Smart Promotion fee <small>(0 if not enrolled; 3.5% outside campaigns, 1 to 2 points more during campaigns)</small></label>
      <div class="in"><input id="sp" type="number" inputmode="decimal" min="0" step="0.1" value="0"><span>%</span></div>
      <label for="cost">What the item cost you</label>
      <div class="in"><span>$</span><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="8"></div>
      <label for="label">Shipping label or fulfillment fee you pay</label>
      <div class="in"><span>$</span><input id="label" type="number" inputmode="decimal" min="0" step="0.01" value="5"></div>
      <details><summary class="note">Edit fee rates</summary>
      <label for="ref">Referral fee for your category</label>
      <div class="in"><input id="ref" type="number" min="0" step="0.1" value="6"><span>%</span></div>
      <label for="adm">Refund admin fee <small>(% of the referral fee)</small></label>
      <div class="in"><input id="adm" type="number" min="0" step="1" value="20"><span>%</span></div>
      <label for="cap">Refund admin fee cap per SKU <small>(0 for no cap)</small></label>
      <div class="in"><span>$</span><input id="cap" type="number" min="0" step="0.01" value="5"></div>
      </details>""",
    out="""<div class="big"><span>You keep</span><b id="keep"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""function calc(){
  var item=n('item'),ship=n('ship'),disc=n('disc'),base=item+ship-disc;
  if(!item){$('keep').textContent=m(0);setRows([['Enter the item price to see TikTok Shop fees.','']]);verdict(false,'No sale entered yet.');return}
  if(base<=0){$('keep').textContent=m(0);setRows([['Your discount is as big as the whole order.','']]);verdict(false,'Lower the discount to see TikTok Shop fees.');return}
  var ref=n('ref'),aff=n('aff'),sp=n('sp'),cb=Math.max(0,item-disc);
  var c=function(b,r){return Math.round(b*r+1e-6)/100};
  var rf=c(base,ref),cm=c(cb,aff),spf=c(base,sp),fees=rf+cm+spf,costs=n('cost')+n('label'),keep=base-fees-costs;
  var ra=c(rf,n('adm')),cap=n('cap');if(cap&&ra>cap)ra=cap;
  var r=[['TikTok charges its fee on (item + shipping - your discount)',m(base)],['Referral fee ('+ref+'% of '+m(base)+')',m(-rf)],
    ['Creator commission ('+aff+'% of '+m(cb)+')',m(-cm)]];
  if(spf)r.push(['Smart Promotion ('+sp+'% of '+m(base)+')',m(-spf)]);
  r.push(['Total TikTok fees and commission',m(-fees)+' ('+pc(fees/base)+')'],['Item cost + label',m(-costs)],['You keep',m(keep),'total'],
    ['If fully refunded, TikTok keeps a refund admin fee of',m(ra)]);
  setRows(r);$('keep').textContent=m(keep);
  if(keep<0)verdict(false,'This sale loses '+m(-keep)+'. Lower the commission, raise the price or the shipping charge.');
  else verdict(true,(cm?'TikTok and the creator take ':'TikTok takes ')+pc(fees/base)+' of the '+m(base)+' order. Your profit is '+pc(keep/base,0)+' of it.');
}""",
    note="""US rates checked on October 20, 2026 on TikTok Shop Seller University: the <a href="https://seller-us.tiktok.com/university/essay?knowledge_id=5988482086864682&amp;lang=en" rel="noopener">category referral fee table</a> (dated October 8, 2026), the <a href="https://seller-us.tiktok.com/university/essay?knowledge_id=5982454398175018&amp;lang=en" rel="noopener">referral fee and refund admin fee policy</a>, the <a href="https://seller-us.tiktok.com/university/essay?knowledge_id=2336057241700098&amp;lang=en" rel="noopener">settlement report guide</a>, the <a href="https://seller-us.tiktok.com/university/essay?knowledge_id=4827354015483691&amp;lang=en" rel="noopener">Smart Promotion guide</a> and <a href="https://seller-us.tiktok.com/university/essay?knowledge_id=386652959082253&amp;lang=en" rel="noopener">cost guide</a>, and the <a href="https://seller-us.tiktok.com/university/essay?knowledge_id=3507056320268087&amp;lang=en" rel="noopener">FBT rate card</a>. The referral fee is 6% for most categories and 5% for diamond, gold, jade, platinum and ruby/sapphire/emerald jewelry and for pre-owned items; pre-owned and collectibles pay 3% on any part of a sale over $10,000, which this calculator does not split out. It is charged on what the buyer pays plus TikTok-funded discounts, minus tax, so shipping is included. This calculator rounds each fee to the nearest cent, so your statement can differ by a cent. Smart Promotion is charged on each order's GMV, and TikTok's Smart Promotion pages do not say whether that includes shipping, so this calculator applies it to the same order amount as the referral fee; your Smart Promotion dashboard shows your actual rate. Sellers whose business registration address is in Texas or West Virginia also pay <a href="https://seller-us.tiktok.com/university/essay?knowledge_id=1017269682849550&amp;lang=en" rel="noopener">sales tax on the referral fee</a> since November 1, 2025 (not included above). Some orders pay less: TikTok's <a href="https://seller-us.tiktok.com/university/essay?knowledge_id=6219480922474258&amp;lang=en" rel="noopener">Q4 2026 LIVE auction policy</a> charges 4% or 3% on qualifying LIVE auction orders with a $1 starting bid from October 1 to December 31, 2026, and invited sellers can get a lower rate on orders from qualifying <a href="https://seller-us.tiktok.com/university/essay?knowledge_id=1007832535975694&amp;lang=en" rel="noopener">GMV Max ad campaigns</a>. TikTok's <a href="https://seller-us.tiktok.com/university/essay?knowledge_id=3658966022407944&amp;lang=en" rel="noopener">August 2026 new seller promotion</a> pays ads credits, not a lower referral fee, so no new seller rate is assumed. If Seller Center shows a different rate, enter it under Edit fee rates.""",
    body="""<h2>How TikTok Shop fees work</h2>
<p><strong>Referral fee.</strong> For US sellers this is the fee TikTok Shop takes on every sale. TikTok's referral fee policy says it covers all TikTok Shop fees except shipping and tax; optional programs such as Smart Promotion are charged on top. It is 6% for most categories and 5% for some fine jewelry and pre-owned items. It is charged on what the buyer pays, including the shipping they pay, with any TikTok-funded discount added back and sales tax taken out. A discount you fund yourself, including your share of a co-funded promotion, lowers it.</p>
<p><strong>Creator commission.</strong> If a creator's video or LIVE made the sale, you pay them the affiliate commission rate you set for that product. TikTok works it out as (product price excluding tax - your discount) x rate, so the shipping charge is not included. If the order is refunded before the creator is paid, which is usually 15 days after delivery, the commission comes back to you.</p>
<p><strong>Smart Promotion.</strong> An optional program that TikTok now requires for its big platform campaigns and flash sales. It charges a fixed 3.5% of each order's GMV, shown as a Smart Promotion Fee on your settlement. During big platform campaigns a Smart Promotion Campaign Period Fee is added: TikTok's guides put it at 1% to 2% of GMV in one place and 1% in another, so check the Smart Promotion dashboard in Seller Center, which shows the rate you are actually paying. Leave it at 0 if you are not enrolled.</p>
<p><strong>No separate transaction fee.</strong> The old fee of $0.30 per order plus a percentage only applied to orders placed before April 3, 2023. TikTok's settlement report guide marks that fee "No longer applicable" and lists no other processing fee, and its referral fee policy says the referral fee covers all TikTok Shop fees except shipping and tax, so this calculator adds no separate 2% or 3% processing fee. If your settlement shows a charge that is not covered here, add it to the label box.</p>
<p><strong>TikTok-funded discounts.</strong> When TikTok pays for a discount, the buyer pays less but your gross sales on the settlement are counted before that discount, and the referral fee is charged as if the buyer paid full price. Neither your payout nor the fee changes, so leave those discounts out of the calculator.</p>
<p><strong>Fulfilled by TikTok.</strong> Since June 16, 2025 FBT orders ship free to the buyer by default, so enter 0 for shipping and put your FBT fulfillment fee in the label box. If you opted out, buyers pay a flat $5.99 on orders under $30, but TikTok keeps it: your settlement credits the $5.99 and takes it back as a Customer Shipping Fee Offset, and TikTok pays you $0.75 per unit on those orders. TikTok's referral fee formula includes shipping the buyer pays and lists no FBT exception, so in that case enter $5.99 as shipping and add $5.99 minus $0.75 per unit to your fulfillment fee in the label box.</p>
<h2>The formula</h2>
<p class="formula">Referral fee = 6% x (item + buyer shipping - your discount)<br>Creator commission = rate x (item - your discount)</p>
<h2>Worked example</h2>
<p>A <strong>$30</strong> item, the buyer pays <strong>$4</strong> shipping, there is no seller discount, and it sold through a creator's video at <strong>15%</strong> commission. The referral fee base is $30 + $4 = <strong>$34.00</strong>, so the 6% referral fee is <strong>$2.04</strong>. The creator gets 15% of the $30 item, not the shipping: <strong>$4.50</strong>. Together TikTok and the creator take <strong>$6.54</strong>, which is 19.2% of the order. After the $8 item cost and the $5 label you keep <strong>$14.46</strong>, 43% of the $34.00. Sales tax is left out of both fees.</p>
<p>If that order is fully refunded, TikTok gives back the $2.04 referral fee minus a refund admin fee of <strong>$0.41</strong>: 20% of the fee, capped at $5 per SKU.</p>
<ul>
<li>Enrolled in Smart Promotion at 3.5%: it adds $1.19, and you keep $13.27.</li>
<li>A $5 coupon you fund: the base drops to $29.00, the referral fee to $1.74 and the commission to 15% of $25, which is $3.75. You keep $10.51.</li>
<li>You sold it yourself, with no creator: fees are $2.04, 6.0% of the order, and you keep $18.96.</li>
</ul>
<h2>Getting paid</h2>
<p>TikTok Shop settles an order after it is delivered to the customer and has no open refund or return request. The minimum payout is $1. "You keep" in the calculator is what is left of that one order after TikTok's fees, the creator's commission, your item cost and your label.</p>
<h2>Pricing tips</h2>
<p>When a creator makes the sale, their commission can cost more than TikTok does: in the example the 15% commission is $4.50 against a $2.04 referral fee, and together they take about a fifth of the order before your own costs. Because shipping is in the referral base but not in the commission base, charging for shipping costs you 6% of it, while folding it into the item price costs 6% plus the commission rate (plus Smart Promotion if you are enrolled, which this calculator applies to both). Free samples you send to creators are a real cost too: divide the cost of samples by the sales they bring in and add that to the item cost above.</p>""",
    faqs=[
        ("How is the TikTok Shop referral fee calculated?", "TikTok's formula is rate x (customer payment + platform discount - tax). The shipping the buyer pays is included, discounts TikTok funds are added back, tax is taken out, and discounts you fund lower it. A $30 item with $4 shipping at 6% pays a $2.04 referral fee."),
        ("Is the TikTok Shop fee 6% or 8% in 2026?", "TikTok's US category table, dated October 8, 2026, lists 6% for most categories and 5% for five fine jewelry subcategories and pre-owned. TikTok's seller homepage also still says it charges a 6% commission on each sale, and its Q4 2026 LIVE auction fee policy, also dated October 8, 2026, links to that table as its standard platform fee. Some blogs report 8% from August 2026, but no TikTok page we found says so. Your settlement statement shows the rate you are actually charged; type it in the referral fee box under Edit fee rates."),
        ("Do creators earn commission on shipping and tax?", "No. TikTok calculates affiliate commission as (product price excluding tax - your discount) x rate. 15% on a $30 item with $4 shipping is $4.50. If the order is refunded before the creator is paid, usually 15 days after delivery or later if your settlement period is longer, the commission comes back to you."),
        ("What does TikTok Shop keep when an order is refunded?", "On a full refund it gives back the referral fee minus a refund admin fee of 20% of that fee, capped at $5 per SKU. On the $2.04 example that is $0.41. On a $500 item at 6% it would be $6, capped to $5. There is no admin fee on 'buy now, refund later' creator sample orders or on buyer cancellations before shipping that meet TikTok's auto-cancel criteria."),
    ],
    cta_head="Also selling on Etsy, Shopify, Amazon or eBay?",
    cta_text="The <strong>Seller Profit Sheet</strong> works out net profit for every product at once. Paste your Etsy or Shopify sales export (or type in Amazon and eBay sales) and it shows net profit per product after fees, labels, discounts, returns and ad spend, with a red LOSING MONEY flag on anything underwater. Excel and Google Sheets, one-time $14, no subscription.",
    related=["ebay-fee-calculator", "amazon-fba-calculator", "shopify-fee-calculator", "poshmark-fee-calculator", "roas-calculator", "profit-margin-calculator"],
    gig="profit",
    tests=[
        {"expect": {"rows": ["$34.00", "-$2.04", "-$4.50", "-$6.54", "19.2%", "-$13.00", "$0.41"], "keep": "$14.46",
                    "verdict": ["TikTok and the creator take 19.2%", "43%"]}},
        {"set": {"sp": "3.5"}, "expect": {"rows": "-$1.19", "keep": "$13.27"}},
        {"set": {"disc": "5"}, "expect": {"rows": ["$29.00", "-$1.74", "-$3.75"], "keep": "$10.51"}},
        {"set": {"aff": "0"}, "expect": {"rows": ["-$2.04", "6.0%"], "keep": "$18.96", "verdict": "TikTok takes 6.0%"}},
        {"set": {"item": "500.25", "ship": "0", "aff": "10", "cost": "480", "label": "0"}, "expect": {"rows": ["-$30.02", "-$50.03", "-$80.05", "$5.00"], "keep": "-$59.80", "verdict": "loses $59.80"}},
        {"set": {"item": "", "ship": ""}, "expect": {"keep": "$0.00", "rows": "Enter the item price", "verdict": "No sale entered"}},
    ],
)
