// Load every generated page in Chromium, fail on JS errors, empty results, or failed spec tests.
// Run: python3 tools/build_pages.py --tests > /tmp/t.json && node tools/check_pages.js /tmp/t.json
const { chromium } = require(process.env.PW || '/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const root = path.resolve(__dirname, '..');
const specs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
(async () => {
  const b = await chromium.launch({ executablePath: fs.existsSync('/opt/pw-browsers/chromium') ? undefined : undefined });
  let fail = 0;
  for (const s of specs) {
    const pg = await b.newPage({ viewport: { width: 390, height: 900 } });
    const errs = [];
    pg.on('pageerror', e => errs.push(String(e)));
    pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await pg.goto('file://' + path.join(root, s.slug, 'index.html'));
    const txt = await pg.evaluate(() => document.querySelector('.card').innerText);
    const overflow = await pg.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    const probs = [...errs];
    if (overflow) probs.push('horizontal overflow at 390px');
    if (/NaN|undefined|Infinity/.test(txt)) probs.push('bad value in output: ' + (txt.match(/.{0,40}(NaN|undefined|Infinity).{0,20}/) || [''])[0]);
    for (const [i, t] of (s.tests || []).entries()) {
      await pg.reload();
      for (const [id, v] of Object.entries(t.set || {})) {
        await pg.evaluate(([id, v]) => {
          const el = document.getElementById(id);
          if (el.type === 'checkbox') el.checked = !!v; else el.value = v;
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
        }, [id, v]);
      }
      for (const id of t.click || []) await pg.click('#' + id);
      for (const [id, want] of Object.entries(t.expect || {})) {
        const got = await pg.evaluate(id => { const e = document.getElementById(id); return e ? e.innerText : '(missing #' + id + ')'; }, id);
        for (const w of [].concat(want)) if (!got.includes(w)) probs.push(`test ${i}: #${id} lacks "${w}" | got: ${got.replace(/\s+/g, ' ').slice(0, 300)}`);
      }
    }
    console.log((probs.length ? 'FAIL ' : 'ok   ') + s.slug + (probs.length ? '\n  ' + probs.join('\n  ') : ''));
    if (probs.length) fail++;
    await pg.close();
  }
  await b.close();
  process.exit(fail ? 1 : 0);
})();
