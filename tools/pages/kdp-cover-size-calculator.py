PAGE = dict(
    result_url=None,
    gig=None,
    cta_head=None,
    slug="kdp-cover-size-calculator",
    cat="Print & design sizes",
    nav_name="KDP cover size and spine width calculator",
    title="KDP Cover Size Calculator: Paperback Spine Width and Full Cover Dimensions",
    desc="Free KDP paperback cover size calculator. Enter trim size, page count and paper type to get the spine width, full wrap cover dimensions with bleed in inches, mm and pixels at 300 DPI, and whether spine text is allowed.",
    h1="KDP cover size and spine width calculator",
    lead="For Amazon KDP paperbacks, including low-content books like journals, planners and coloring books. Enter the trim size, page count and paper, and you get the spine width and the exact full-wrap cover size to set your canvas to.",
    form="""      <label for="trim">Trim size</label>
      <select id="trim" class="full">
        <option value="5x8">5 &times; 8 in</option><option value="5.06x7.81">5.06 &times; 7.81 in</option><option value="5.25x8">5.25 &times; 8 in</option>
        <option value="5.5x8.5">5.5 &times; 8.5 in</option><option value="6x9" selected>6 &times; 9 in</option><option value="6.14x9.21">6.14 &times; 9.21 in</option>
        <option value="6.69x9.61">6.69 &times; 9.61 in</option><option value="7x10">7 &times; 10 in</option><option value="7.44x9.69">7.44 &times; 9.69 in</option>
        <option value="7.5x9.25">7.5 &times; 9.25 in</option><option value="8x10">8 &times; 10 in</option><option value="8.25x6">8.25 &times; 6 in (landscape)</option>
        <option value="8.25x8.25">8.25 &times; 8.25 in</option><option value="8.5x8.5">8.5 &times; 8.5 in</option><option value="8.5x11">8.5 &times; 11 in</option>
        <option value="8.27x11.69">8.27 &times; 11.69 in (A4)</option><option value="custom">Custom size</option>
      </select>
      <div id="cust" style="display:none"><label for="tw">Custom trim width &times; height</label>
      <div class="in"><input id="tw" style="width:0" type="number" inputmode="decimal" min="0" step="0.01" value="6"><span>&times;</span><input id="th" style="width:0" type="number" inputmode="decimal" min="0" step="0.01" value="9"><span>in</span></div></div>
      <label for="pages">Page count <small>(final interior pages, not sheets)</small></label>
      <div class="in"><input id="pages" type="number" inputmode="numeric" min="0" step="1" value="300"><span>pages</span></div>
      <label for="paper">Paper</label>
      <select id="paper" class="full">
        <option value="0.002252">Black and white, white paper</option>
        <option value="0.0025">Black and white, cream paper</option>
        <option value="0.002252">Standard color</option>
        <option value="0.002347">Premium color</option>
      </select>""",
    out="""<div class="big"><span>Full cover size with bleed</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""var B=0.125;
var i3=function(x){return x.toFixed(3).replace(/0+$/,'').replace(/\\.$/,'')+'"'};
var mm=function(x){return (x*25.4).toFixed(1)+' mm'};
var px=function(x){return Math.round(x*300).toLocaleString('en-US')};
function calc(){
  var t=$('trim').value,cu=t=='custom';$('cust').style.display=cu?'':'none';
  var w=cu?n('tw'):parseFloat(t.split('x')[0]),h=cu?n('th'):parseFloat(t.split('x')[1]),pg=Math.round(n('pages')),k=parseFloat($('paper').value);
  if(!w||!h||!pg){$('big').textContent='-';setRows([]);verdict(false,'Enter the trim size and page count.');return}
  var sp=pg*k,cw=B+w+sp+w+B,ch=B+h+B;
  $('big').textContent=i3(cw)+' \\u00d7 '+i3(ch);
  setRows([['Spine width',i3(sp)+' ('+mm(sp)+')'],['Full cover width',i3(cw)+' ('+mm(cw)+')'],['Full cover height',i3(ch)+' ('+mm(ch)+')'],
    ['Canvas at 300 DPI',px(cw)+' \\u00d7 '+px(ch)+' px'],['Back cover',i3(B)+' to '+i3(B+w)+' from the left'],
    ['Spine',i3(B+w)+' to '+i3(B+w+sp)],['Front cover',i3(B+w+sp)+' to '+i3(cw-B)],['Bleed',i3(B)+' on every outside edge']]);
  if(pg<79)verdict(false,'No spine text: KDP needs at least 79 pages for text on the spine. Leave the spine blank or use a solid color.');
  else verdict(true,'Spine text is allowed. Keep it at least 0.0625" from each spine edge, so the text area is '+i3(sp-0.125)+' wide.');
}""",
    note="Formulas from KDP's paperback cover help page (checked October 2026): spine = page count &times; 0.002252\" (white paper and standard color), 0.0025\" (cream) or 0.002347\" (premium color); 0.125\" bleed on the top, bottom and outside edges; spine text needs 79+ pages. Paperback only; hardcover covers use different dimensions.",
    body="""<h2>The KDP cover formula</h2>
<p class="formula">Spine width = page count &times; paper thickness per page</p>
<p class="formula">Cover width = bleed + back cover + spine + front cover + bleed</p>
<p class="formula">Cover height = bleed + trim height + bleed</p>
<p>Bleed is 0.125 inches. Paper thickness per page is 0.002252" for white paper and standard color, 0.0025" for cream, and 0.002347" for premium color. Use the final interior page count, not the number of sheets.</p>
<h2>Worked example</h2>
<p>A 6 &times; 9 inch paperback with 300 pages on white paper has a spine of 300 &times; 0.002252 = <strong>0.676"</strong>. The full cover is 0.125 + 6 + 0.676 + 6 + 0.125 = <strong>12.926" wide</strong> and 9 + 0.25 = <strong>9.25" tall</strong>, which is a 3,878 &times; 2,775 pixel canvas at 300 DPI.</p>
<p>The same book on cream paper gets a 0.75" spine and a 13" wide cover. If you switch paper after designing, the spine and the front cover position both move, so redo the cover canvas.</p>
<h2>Low-content books: journals, planners, logbooks</h2>
<p>Many low-content books are 100 to 120 pages, so the spine is only about 0.23 to 0.27 inches. Spine text is allowed from 79 pages, but on a thin spine keep it short and small, at least 0.0625" from each spine edge. Under 79 pages, KDP doesn't allow spine text at all.</p>
<p>Making the interior as a printable? The <a href="../printable-wall-art-size-calculator/">print size and DPI calculator</a> shows the pixels each page size needs at 300 DPI.</p>""",
    faqs=[
        ("How do I calculate spine width for KDP?", "Multiply the page count by 0.002252 inches for white paper or standard color, 0.0025 for cream, or 0.002347 for premium color. 300 pages on white paper gives a 0.676 inch spine."),
        ("What size is a KDP cover for a 6x9 book?", "It depends on the page count. With 300 white pages the full cover is 12.926 &times; 9.25 inches including bleed. With 120 white pages it is 12.52 &times; 9.25 inches."),
        ("How much bleed does a KDP cover need?", "0.125 inches (3.2 mm) on the top, bottom and outside edges, which adds 0.25 inches to the width and 0.25 inches to the height."),
        ("How many pages do I need for spine text on KDP?", "At least 79 pages. Text must also sit at least 0.0625 inches from each edge of the spine."),
        ("What pixel size should a KDP cover be?", "The full cover size in inches times 300. A 6 &times; 9 book with 300 white pages needs a 3,878 &times; 2,775 pixel canvas."),
    ],
    related=["printable-wall-art-size-calculator", "dtf-transfer-size-chart", "gumroad-fee-calculator", "etsy-digital-download-calculator"],
    og_image="pins/pin-06.png",
    tests=[
        {"expect": {"big": ['12.926" × 9.25"'], "rows": ['0.676" (17.2 mm)', "3,878 × 2,775 px", '6.801" to 12.801"'], "verdict": ["Spine text is allowed", '0.551"']}},
        {"set": {"paper": "0.0025"}, "expect": {"big": ['13" × 9.25"'], "rows": ['0.75"']}},
        {"set": {"pages": "120"}, "expect": {"big": ['12.52" × 9.25"']}},
        {"set": {"pages": "60"}, "expect": {"verdict": ["No spine text"]}},
        {"set": {"trim": "8.5x11", "pages": "100"}, "expect": {"big": ['17.475" × 11.25"']}},
        {"set": {"trim": "custom", "tw": "5", "th": "7"}, "expect": {"big": ['10.926" × 7.25"']}},
        {"set": {"pages": "0"}, "expect": {"verdict": ["Enter the trim size"]}},
    ],
)
