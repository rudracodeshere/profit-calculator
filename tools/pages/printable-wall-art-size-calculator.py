PAGE = dict(
    gig="seo",
    slug="printable-wall-art-size-calculator",
    cat="Etsy tools",
    nav_name="Printable wall art size and DPI calculator",
    title="Printable Wall Art Size Calculator: Print Sizes, DPI and Pixels for Etsy",
    desc="Free print size and DPI calculator for Etsy printable wall art and print on demand. Enter your image's pixels to see every frame size it prints sharp at, which ratios need a crop, and the pixels each size needs.",
    h1="Printable wall art size and DPI calculator",
    lead="Enter your artwork's pixel size, or pick the file. You'll see the largest sharp print, every standard frame size from 4x6 to 24x36 and A1, which ones need a crop, and how many pixels each size needs. Nothing leaves your browser.",
    form="""      <label for="file">Pick an image <small>(optional, reads the pixel size only)</small></label>
      <input id="file" type="file" accept="image/*" style="width:100%;padding:8px;border:1px solid var(--line);border-radius:8px;background:#fff;font:inherit">
      <label for="w">Width</label>
      <div class="in"><input id="w" type="number" inputmode="numeric" min="1" step="1" value="1024"><span>px</span></div>
      <label for="h">Height</label>
      <div class="in"><input id="h" type="number" inputmode="numeric" min="1" step="1" value="1536"><span>px</span></div>
      <label for="dpi">Minimum quality</label>
      <select id="dpi" class="full">
        <option value="300" selected>300 DPI: sharp up close (what buyers expect)</option>
        <option value="200">200 DPI: fine on a wall</option>
        <option value="150">150 DPI: large posters seen from a distance</option>
      </select>""",
    out="""<div class="big"><span>Largest sharp print, no crop</span><b id="big"></b></div>
      <table aria-live="polite"><tbody id="rows"></tbody></table>
      <div id="verdict" class="verdict"></div>""",
    js="""var R=[[1,'1:1'],[1.25,'4:5'],[14/11,'11x14'],[4/3,'3:4'],[1.4,'5:7'],[Math.SQRT2,'ISO (A sizes)'],[1.5,'2:3'],[16/9,'16:9']];
var S=[['4x6','2:3',4,6],['8x12','2:3',8,12],['12x18','2:3',12,18],['16x24','2:3',16,24],['20x30','2:3',20,30],['24x36','2:3',24,36],
['6x8','3:4',6,8],['9x12','3:4',9,12],['12x16','3:4',12,16],['18x24','3:4',18,24],
['4x5','4:5',4,5],['8x10','4:5',8,10],['16x20','4:5',16,20],['24x30','4:5',24,30],
['5x7','5:7',5,7],['11x14','11x14',11,14],
['A5','ISO (A sizes)',5.83,8.27],['A4','ISO (A sizes)',8.27,11.69],['A3','ISO (A sizes)',11.69,16.54],['A2','ISO (A sizes)',16.54,23.39],['A1','ISO (A sizes)',23.39,33.11],
['8x8','1:1',8,8],['12x12','1:1',12,12],['20x20','1:1',20,20]];
var f1=function(x){return (Math.floor(x*10)/10).toFixed(1)};
var px=function(x){return Math.ceil(x-1e-9).toLocaleString('en-US')};
function ratioName(w,h){var r=Math.max(w,h)/Math.min(w,h),best='';R.forEach(function(k){if(Math.abs(r/k[0]-1)<0.006)best=k[1]});return best||('1:'+r.toFixed(2))}
function calc(){
  var w=Math.round(n('w')),h=Math.round(n('h')),d=parseFloat($('dpi').value);
  if(!w||!h){$('big').textContent='-';setRows([]);$('tbl').innerHTML='';verdict(false,'Enter the width and height in pixels, or pick the image file.');return}
  var land=w>h,rn=ratioName(w,h),fam=null,ok=0,h2='';
  S.forEach(function(s){
    var a=Math.min(s[2],s[3]),b=Math.max(s[2],s[3]),iw=land?b:a,ih=land?a:b;
    if(w==h&&s[1]!='1:1'){iw=a;ih=b}
    var ach=Math.min(w/iw,h/ih),crop=1-(iw*ih*ach*ach)/(w*h),good=ach>=d-1e-9;
    if(good)ok++;
    if(s[1]==rn&&good)fam=s;
    var st=good?(crop>0.01?'Sharp after '+pc(crop,0)+' crop':'Sharp')+' ('+Math.floor(ach)+' DPI)':'Too small ('+Math.floor(ach)+' DPI)';
    h2+='<tr><td>'+s[0]+(land?' landscape':'')+'</td><td>'+s[1]+'</td><td>'+px(iw*d)+' &times; '+px(ih*d)+'</td><td style="color:'+(good?(crop>0.01?'#a15c00':'var(--green)'):'var(--red)')+'">'+st+'</td></tr>';
  });
  $('tbl').innerHTML=h2;
  $('big').textContent=f1(w/d)+' \\u00d7 '+f1(h/d)+' in';
  var top=null;S.forEach(function(s){if(s[1]==rn&&(!top||s[3]>top[3]))top=s});
  var r=[['Your file',w.toLocaleString('en-US')+' \\u00d7 '+h.toLocaleString('en-US')+' px'],['Aspect ratio',rn+(w==h?' (square)':land?' (landscape)':' (portrait)')],['Largest print at '+d+' DPI',f1(w/d)+' \\u00d7 '+f1(h/d)+' in ('+f1(w/d*2.54)+' \\u00d7 '+f1(h/d*2.54)+' cm)'],['Standard sizes it prints sharp',ok+' of '+S.length]];
  if(top){var tw=land?top[3]:top[2],th=land?top[2]:top[3];r.push(['Pixels for '+top[0]+' at '+d+' DPI',px(tw*d)+' \\u00d7 '+px(th*d)+' px'])}
  setRows(r);
  if(!top)verdict(false,'This is not a standard frame ratio, so every frame size needs a crop. Resize the master file to 2:3, 3:4, 4:5, 11x14 or ISO first.');
  else if(!fam||Math.max(fam[2],fam[3])<10)verdict(false,'Too small to sell as wall art: at '+d+' DPI it only prints '+f1(w/d)+' \\u00d7 '+f1(h/d)+' in. Upscale it to at least '+px((land?top[3]:top[2])*d)+' \\u00d7 '+px((land?top[2]:top[3])*d)+' px to offer every '+rn+' size up to '+top[0]+'.');
  else if(fam!=top)verdict(true,'Prints sharp up to '+fam[0]+' in the '+rn+' ratio. For '+top[0]+' you need '+px((land?top[3]:top[2])*d)+' \\u00d7 '+px((land?top[2]:top[3])*d)+' px.');
  else verdict(true,'Big enough for every '+rn+' size up to '+top[0]+' at '+d+' DPI. Sizes in other ratios need a separate, re-cropped file.');
}
$('file').addEventListener('change',function(){var f=this.files&&this.files[0];if(!f)return;var u=URL.createObjectURL(f),i=new Image();i.onload=function(){$('w').value=i.naturalWidth;$('h').value=i.naturalHeight;URL.revokeObjectURL(u);calc()};i.src=u});""",
    note="Sizes in inches; A sizes are ISO 216 (A4 = 210 &times; 297 mm). \"Sharp after crop\" means the file covers that frame once trimmed to its ratio; the percentage is how much of the image gets cut. Etsy digital listings take up to 5 files of 20MB each (Etsy Help Center, October 2026).",
    body="""<h3>Every standard size for your file</h3>
<table class="wide"><thead><tr><th>Size (in)</th><th>Ratio</th><th>Pixels needed</th><th>Your file</th></tr></thead><tbody id="tbl"></tbody></table>
<h2>How print size, pixels and DPI fit together</h2>
<p>A printer lays down a fixed number of pixels per inch. Divide your image's pixels by that number and you get the largest print that stays sharp.</p>
<p class="formula">Largest print (inches) = pixels &divide; DPI</p>
<p class="formula">Pixels needed = print size (inches) &times; DPI</p>
<p>300 DPI is the standard for prints people look at up close. 200 DPI usually looks fine on a wall, and big posters viewed from across a room get away with 150. Most buyers of printables print at home or at a print shop and expect 300.</p>
<h2>Worked example: why AI art often fails as wall art</h2>
<p>A typical AI image is 1024 &times; 1536 pixels, a 2:3 portrait. At 300 DPI that prints at only <strong>3.4 &times; 5.1 inches</strong>, smaller than a 4x6 photo. It prints none of the 24 standard sizes in the table sharply. Selling it as a 24x36 poster means the buyer gets a blurry print and you get a refund request or a bad review.</p>
<p>To cover every 2:3 size up to 24x36 at 300 DPI, the master file needs <strong>7,200 &times; 10,800 pixels</strong>. Upscale first, check the detail at 100% zoom, then export.</p>
<h2>Which files to put in an Etsy printable listing</h2>
<p>Etsy lets a digital listing hold <strong>5 files of up to 20MB each</strong>. Five ratio files cover nearly every frame a buyer owns:</p>
<table class="wide"><thead><tr><th>File</th><th>Covers</th><th>Pixels at 300 DPI</th></tr></thead><tbody>
<tr><td>2:3</td><td>4x6, 8x12, 12x18, 16x24, 20x30, 24x36</td><td>7,200 &times; 10,800</td></tr>
<tr><td>3:4</td><td>6x8, 9x12, 12x16, 18x24</td><td>5,400 &times; 7,200</td></tr>
<tr><td>4:5</td><td>4x5, 8x10, 16x20, 24x30</td><td>7,200 &times; 9,000</td></tr>
<tr><td>11x14</td><td>11x14</td><td>3,300 &times; 4,200</td></tr>
<tr><td>ISO</td><td>A5, A4, A3, A2, A1</td><td>7,017 &times; 9,933</td></tr>
</tbody></table>
<p>A buyer prints a smaller size from the same file because the ratio is the same, so you don't need one file per size. Big 300 DPI files can pass 20MB as PNG; a high-quality JPG of the same image is usually far smaller. If you want to offer more than five files, a ZIP counts as one file but must also stay under 20MB.</p>
<h2>Print on demand works the same way</h2>
<p>Printify, Printful and Gelato all list a pixel size per product. A poster or canvas has the same math as a printable: inches &times; DPI. Shirts and mugs have their own print areas, so check the product's template, but the rule holds: if the file has fewer pixels than the print area needs, the print comes out soft.</p>""",
    faqs=[
        ("What size should printable wall art be for Etsy?", "Design at 300 DPI in a few master ratios rather than one file per size. A 2:3 file of 7,200 &times; 10,800 pixels covers 4x6 up to 24x36; add 3:4, 4:5, 11x14 and ISO files to cover the other common frames."),
        ("How many pixels do I need for an 8x10 print?", "2,400 &times; 3,000 pixels at 300 DPI, or 1,600 &times; 2,000 at 200 DPI."),
        ("How many pixels for a 24x36 poster?", "7,200 &times; 10,800 at 300 DPI. At 150 DPI, which works for a poster seen from a distance, it is 3,600 &times; 5,400."),
        ("Is 300 DPI the same as 300 PPI?", "For digital files, sellers use the terms the same way: how many image pixels land on each printed inch. The DPI number saved in a file's settings changes nothing on its own; only the pixel count matters."),
        ("How many files can I upload to an Etsy digital listing?", "Up to 5 files, each up to 20MB. A ZIP counts as one file."),
    ],
    related=["etsy-digital-download-calculator", "print-on-demand-profit-calculator", "etsy-title-tag-checker", "etsy-fee-calculator", "etsy-pricing-calculator"],
    cta_head="Selling printables? See which ones actually make money.",
    cta_text="The <strong>Seller Profit Sheet</strong> reads your Etsy sales export and shows what each listing kept after transaction fees, processing, listing renewals and Offsite Ads, so you can see which designs carry the shop and which ones to drop. Excel and Google Sheets, one-time $14, no subscription.",
    og_image="pins/pin-06.png",
    tests=[
        {"expect": {"big": ["3.4 × 5.1 in"], "rows": ["1,024 × 1,536 px", "2:3 (portrait)", "0 of 24", "7,200 × 10,800 px"], "verdict": ["Too small to sell as wall art"], "tbl": ["Too small (256 DPI)", "7,200 \u00d7 10,800"]}},
        {"set": {"w": "7200", "h": "10800"}, "expect": {"big": ["24.0 × 36.0 in"], "verdict": ["Big enough for every 2:3 size up to 24x36"], "tbl": ["Sharp (300 DPI)", "Sharp after 17% crop (300 DPI)"]}},
        {"set": {"w": "3000", "h": "2400"}, "expect": {"rows": ["4:5 (landscape)", "Pixels for 24x30 at 300 DPI", "9,000 × 7,200 px"], "verdict": ["Prints sharp up to 8x10"]}},
        {"set": {"w": "2400", "h": "3000", "dpi": "150"}, "expect": {"big": ["16.0 × 20.0 in"], "verdict": ["Prints sharp up to 16x20"]}},
        {"set": {"w": "1000", "h": "3000"}, "expect": {"rows": ["1:3.00"], "verdict": ["not a standard frame ratio"]}},
        {"set": {"w": "0"}, "expect": {"verdict": ["Enter the width and height"]}},
    ],
)
