/* ── Passport (v1415, 2026-11-27 - sharp worm crest on iPhone) ── replaces the Bird ID card everywhere. Opens on the ID page; tap the right side
   to turn to the next page, the left side to go back (on the ID page that closes the cover; tap the cover to open it
   again). Stamp pages hold 6 stamps each and are added as stamps are earned, then one "more to come" page.
   Plain DOM drawn into a React-owned box (_PPass), using the site's own bird kit (_ppKit) for the photo. */
let _ppPassCssOn = false, _ppTex = null;
// paper fibres, leather grain and uneven stamp ink, each drawn once into a small picture
function _ppTextures() {
  const mk = (w, h, f) => { const c = document.createElement(`canvas`); c.width = w; c.height = h; f(c.getContext(`2d`), w, h); return c.toDataURL(); };
  const rnd = (() => { let a = 1234567; return () => { a = (a * 1103515245 + 12345) & 0x7fffffff; return a / 0x7fffffff; }; })();
  const paper = mk(220, 220, (x, w, h) => { for (let i = 0; i < 2600; i++) { x.fillStyle = `rgba(120,105,90,${.04 + rnd() * .1})`; x.fillRect(rnd() * w, rnd() * h, 1 + rnd() * 1.4, .6 + rnd()); }
    for (let i = 0; i < 90; i++) { x.strokeStyle = `rgba(110,95,80,${.05 + rnd() * .08})`; x.lineWidth = .5; x.beginPath(); const sx = rnd() * w, sy = rnd() * h, a = rnd() * 6.28, l = 3 + rnd() * 9; x.moveTo(sx, sy); x.quadraticCurveTo(sx + Math.cos(a) * l, sy + Math.sin(a) * l * .5, sx + Math.cos(a + .4) * l * 1.6, sy + Math.sin(a + .4) * l); x.stroke(); } });
  const wrapD = (w, h, x0, y0, r, fn) => { for (const dx of [-w, 0, w]) for (const dy of [-h, 0, h]) if (x0 + dx > -r && x0 + dx < w + r && y0 + dy > -r && y0 + dy < h + r) fn(x0 + dx, y0 + dy); };
  const leather = mk(200, 200, (x, w, h) => { const len = 3, wid = 1.4, gap = 1.9, ang = -0.45, rows = Math.round(h / gap), cols = Math.round(w / (len * 0.9));
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) { const cx = (c + (r % 2) * .5) * w / cols + (rnd() - .5) * .8, cy = r * h / rows + (rnd() - .5) * .8, L = len * (0.8 + rnd() * .4), Wd = wid * (0.8 + rnd() * .5), a = ang + (rnd() - .5) * .35, lo = .30 * (0.7 + rnd() * .6), hi = .10 * (0.5 + rnd());
      wrapD(w, h, cx, cy, L + 2, (px, py) => { x.save(); x.translate(px, py); x.rotate(a);
        x.fillStyle = `rgba(0,0,0,${lo})`; x.beginPath(); x.ellipse(0, Wd * .45, L / 2, Wd / 2, 0, 0, 7); x.fill();
        x.fillStyle = `rgba(205,215,255,${hi})`; x.beginPath(); x.ellipse(0, -Wd * .2, L / 2 * .85, Wd / 2 * .7, 0, 0, 7); x.fill(); x.restore(); }); } });
  const ink = mk(160, 160, (x, w, h) => { x.fillStyle = `#000`; x.fillRect(0, 0, w, h); x.globalCompositeOperation = `destination-out`;
    for (let i = 0; i < 26; i++) { const g = x.createRadialGradient(0, 0, 0, 0, 0, 1); const cx = rnd() * w, cy = rnd() * h, r = 10 + rnd() * 30; x.save(); x.translate(cx, cy); x.scale(r, r); g.addColorStop(0, `rgba(0,0,0,${.15 + rnd() * .3})`); g.addColorStop(1, `rgba(0,0,0,0)`); x.fillStyle = g; x.fillRect(-1, -1, 2, 2); x.restore(); }   /* lighter pressure in patches */
    for (let i = 0; i < 1400; i++) { x.fillStyle = `rgba(0,0,0,${.5 + rnd() * .5})`; x.fillRect(rnd() * w, rnd() * h, .6 + rnd() * 1.2, .6 + rnd() * 1.2); } });   /* specks where the ink didn't take */
  return { paper, leather, ink };
}
function _ppPassCss() {
  if (_ppPassCssOn) return; _ppPassCssOn = true;
  const T = _ppTex = _ppTextures();
  const st = document.createElement(`style`);
  st.textContent = `@font-face{font-family:'PP Sig';src:url(/assets/fonts/mrs-saint-delafield.woff2) format('woff2');font-display:block}
.ppp{position:relative;width:100%;max-width:354px;text-align:left;line-height:normal;letter-spacing:normal;font-weight:normal;margin:0 auto;user-select:none;-webkit-user-select:none;-webkit-tap-highlight-color:transparent;cursor:pointer}
.ppp-in{position:absolute;left:0;top:0;width:354px;height:480px;transform-origin:0 0;perspective:1600px}
.ppp .ppp-in,.ppp .ppp-in *{text-align:left!important}
.ppp .cover .t,.ppp .cover .n{text-align:center!important}
.ppp-spine{position:absolute;left:0;top:0;width:16px;height:480px;border-radius:6px 0 0 6px;background:radial-gradient(130% 100% at 28% 18%,#2c3a62 0%,#222e52 45%,#1b2545 80%,#161e3a 100%) 0 0/354px 480px;box-shadow:0 6px 14px rgba(0,0,0,.45)}
.ppp-spine::before{content:'';position:absolute;inset:0;border-radius:inherit;background:url(${T.leather}) 0 0/200px 200px}
.ppp-spine::after{content:'';position:absolute;inset:0;border-radius:6px 0 0 6px;background:repeating-linear-gradient(90deg,#ebe5d7 0 1px,#d6cfbd 1px 2px);box-shadow:inset -7px 0 8px -5px rgba(0,0,0,.4);opacity:0;transition:opacity .22s}
.ppp-in.paper .ppp-spine::after{opacity:1}
.ppp-book{position:absolute;left:14px;top:0;width:340px;height:480px;perspective:1600px}
.ppp-book{clip-path:inset(-24px -24px -24px 0)}
.ppp-book.covering{clip-path:inset(-24px -24px -24px -14px)}

.ppp-pg{position:absolute;inset:0;transform-origin:0 50%;backface-visibility:hidden;-webkit-backface-visibility:hidden}
.ppp-hint{text-align:center;font-size:11.5px;color:#64748b;margin-top:8px}
.ppp .cover{position:absolute;top:0;right:0;bottom:0;left:-14px;border-radius:6px 14px 14px 6px;overflow:hidden;background:radial-gradient(130% 100% at 28% 18%,#2c3a62 0%,#222e52 45%,#1b2545 80%,#161e3a 100%);box-shadow:0 6px 14px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.05),inset -1px 0 0 rgba(255,255,255,.05),inset 0 -1px 0 rgba(255,255,255,.05),inset -6px 0 10px rgba(0,0,0,.35)}
.ppp .cover .grain,.ppp .cover .scuff,.ppp .cover .light,.ppp .cover .wear{position:absolute;inset:0}
.ppp .cover .grain{background:url(${T.leather}) 0 0/200px 200px}
.ppp .cover .wear{display:none}
.ppp .cover .scuff{display:none}
.ppp .cover .light{background:linear-gradient(160deg,rgba(255,255,255,.035) 0%,rgba(255,255,255,0) 45%,rgba(0,0,0,.12) 100%)}
.ppp .gold{background:url(${T.leather}) 0 var(--gy,0)/200px 200px,linear-gradient(175deg,#e8cd85 0%,#d4ae5a 45%,#c19a48 70%,#d9bb6c 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 -1px 0 rgba(0,0,0,.55)) drop-shadow(0 .9px 0 rgba(255,236,190,.13))}
.ppp .cover .t{--gy:-44px}.ppp .cover .n{--gy:-338px}.ppp .cover .u{--gy:-34px}
.ppp .silver{background:url(${T.leather}) 0 var(--gy,0)/200px 200px,linear-gradient(175deg,#f4f6f8 0%,#c9d0d6 45%,#9aa4ad 70%,#dfe4e8 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 -1px 0 rgba(0,0,0,.55)) drop-shadow(0 .9px 0 rgba(255,255,255,.13))}
.ppp .cover .u{position:absolute;left:0;right:0;top:34px;text-align:center!important;font:700 12px 'Times New Roman',Georgia,serif;letter-spacing:.34em;padding-left:.34em}
.ppp-in[data-clan=Puffer] .cover,.ppp-in[data-clan=Puffer] .ppp-spine{background-image:radial-gradient(130% 100% at 28% 18%,#24474d 0%,#1a363b 45%,#132a2e 80%,#0d1e21 100%)!important}
.ppp-in[data-clan=Pecker] .cover,.ppp-in[data-clan=Pecker] .ppp-spine{background-image:radial-gradient(130% 100% at 28% 18%,#6e2a35 0%,#5a1f29 45%,#4a1820 80%,#381118 100%)!important}
.ppp .cover .t{position:absolute;left:0;right:0;top:44px;text-align:center;font:700 38px 'Times New Roman',Georgia,serif;letter-spacing:.07em}
.ppp .cover .n{position:absolute;left:0;right:0;top:338px;text-align:center;font:italic 700 29px 'Times New Roman',Georgia,serif}
.ppp .cover .emb{position:absolute;left:50%;top:100px;width:224px;height:224px;margin-left:-112px;filter:drop-shadow(0 -1.1px 0 rgba(0,0,0,.55)) drop-shadow(0 .9px 0 rgba(255,236,190,.13))}
.ppp .cover .chip2{position:absolute;left:50%;top:404px;width:50px;height:32px;margin-left:-25px;filter:drop-shadow(0 -1.1px 0 rgba(0,0,0,.55)) drop-shadow(0 .9px 0 rgba(255,236,190,.13))}
.ppp .page{position:absolute;inset:0;border-radius:0 14px 14px 0;overflow:hidden;background:#f4f0e4;color:#2a2440;box-shadow:0 6px 14px rgba(0,0,0,.45),inset 16px 0 16px -10px rgba(0,0,0,.32)}
.ppp .page .tint{position:absolute;inset:0;background:radial-gradient(90% 70% at 25% 30%,rgba(206,186,236,.45),transparent 70%),radial-gradient(80% 70% at 80% 80%,rgba(168,220,214,.40),transparent 70%),radial-gradient(60% 50% at 85% 15%,rgba(250,214,180,.35),transparent 70%)}
.ppp .page .guil{position:absolute;inset:0}
.ppp .page .fib{position:absolute;inset:0;background:url(${T.paper});opacity:.9;mix-blend-mode:multiply}
.ppp .lbl{font:600 6.8px Helvetica,Arial,sans-serif;letter-spacing:.06em;color:#6f6590;text-transform:uppercase}
.ppp .val{font:700 11px 'Courier New',monospace;color:#1d1830;letter-spacing:.02em;margin:1px 0 7px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ppp .rks{position:absolute;box-sizing:border-box;mix-blend-mode:multiply;-webkit-mask:url(${T.ink}) 0 0/160px 160px;mask:url(${T.ink}) 0 0/160px 160px;opacity:.9;color:var(--c)}
.ppp .rks .ti{font:900 9.4px Helvetica,Arial,sans-serif;letter-spacing:.14em;color:var(--c);text-align:left}
.ppp .rks .de{font:700 6.3px/1.3 Helvetica,Arial,sans-serif;letter-spacing:.05em;text-transform:uppercase;color:var(--c);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;text-align:left}
.ppp .rkA{left:22px;width:206px;top:350px;height:52px;display:flex;align-items:center;gap:7px;padding:0 9px;border:1.8px dashed var(--c);border-radius:10px;transform:rotate(-1.6deg)}
.ppp .rkA .em{flex:none;width:27px;height:27px;border:1.3px solid var(--c);border-radius:50%;display:flex;align-items:center;justify-content:center}
.ppp .rkA .tx{min-width:0}.ppp .rkA .ti{margin-bottom:2px}
.ppp .mrz{position:absolute;left:14px;right:10px;bottom:14px;font:700 11.2px 'OCR B','Courier New',monospace;letter-spacing:.04em;color:#1d1830;line-height:1.45;white-space:pre;overflow:hidden}
.ppp .pnum{position:absolute;right:14px;bottom:10px;font:700 10px Georgia,serif;color:#7a6f98}
.ppp .stamp{position:absolute;mix-blend-mode:multiply;-webkit-mask:url(${T.ink}) 0 0/160px 160px;mask:url(${T.ink}) 0 0/160px 160px;opacity:.92}
.ppp .parms{position:absolute;right:14px;top:8px;opacity:.75}
.ppp-in[data-clan=Percher] .page{background:#f0f1f4}.ppp-in[data-clan=Percher] .page .tint{background:radial-gradient(90% 70% at 25% 30%,rgba(176,192,236,.5),transparent 70%),radial-gradient(80% 70% at 80% 80%,rgba(190,206,240,.42),transparent 70%),radial-gradient(60% 50% at 85% 15%,rgba(220,214,244,.4),transparent 70%)}
.ppp-in[data-clan=Puffer] .page{background:#eef3f0}.ppp-in[data-clan=Puffer] .page .tint{background:radial-gradient(90% 70% at 25% 30%,rgba(164,214,200,.5),transparent 70%),radial-gradient(80% 70% at 80% 80%,rgba(176,222,214,.44),transparent 70%),radial-gradient(60% 50% at 85% 15%,rgba(206,232,222,.42),transparent 70%)}
.ppp-in[data-clan=Pecker] .page{background:#f7efe6}.ppp-in[data-clan=Pecker] .page .tint{background:radial-gradient(90% 70% at 25% 30%,rgba(240,186,190,.45),transparent 70%),radial-gradient(80% 70% at 80% 80%,rgba(246,214,170,.42),transparent 70%),radial-gradient(60% 50% at 85% 15%,rgba(250,204,196,.38),transparent 70%)}
.ppp .ptitle{position:absolute;left:14px;top:12px;font:800 10px Georgia,serif;letter-spacing:.2em;color:#6f6590}
.ppp-leaf{position:absolute;inset:0;transform-origin:0 50%}
.ppp-face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;isolation:isolate}
.ppp .page,.ppp .cover{isolation:isolate}
.ppp-leaf .page{background:#f4f0e4}
.ppp-back{transform:rotateY(180deg)}
.ppp-shade{position:absolute;inset:0;border-radius:0 14px 14px 0;background:linear-gradient(90deg,rgba(0,0,0,.42),rgba(0,0,0,.12));pointer-events:none}
.ppp .lining{position:absolute;inset:0;border-radius:0 14px 14px 0;background:linear-gradient(90deg,#0d1236,#171f4b);box-shadow:inset 0 0 0 1px rgba(255,255,255,.05)}
.ppp .more{position:absolute;left:30px;right:30px;top:200px;text-align:center;font:italic 600 14px Georgia,serif;color:#7a6f98;line-height:1.5}`;
  document.head.appendChild(st);
  const d = document.createElement(`div`);
  d.innerHTML = `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
 <filter id="ppp-leather" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="4" seed="7" result="t"/><feDiffuseLighting in="t" surfaceScale="1.6" lighting-color="#8f9bd8" result="l"><feDistantLight azimuth="235" elevation="52"/></feDiffuseLighting><feComposite in="l" in2="SourceGraphic" operator="in"/></filter>
 <filter id="ppp-rub"><feTurbulence type="fractalNoise" baseFrequency=".018" numOctaves="3" seed="3"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .6  0 0 0 0 .8  0 0 0 -2.6 1.25"/></filter>
 <filter id="ppp-paper"><feTurbulence type="fractalNoise" baseFrequency=".6" numOctaves="3" seed="11"/><feColorMatrix values="0 0 0 0 .55 0 0 0 0 .5 0 0 0 0 .45 0 0 0 .55 0"/></filter>
 <filter id="ppp-ink" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="2" seed="5" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" result="d"/>
   <feTurbulence type="fractalNoise" baseFrequency=".09" numOctaves="2" seed="9" result="blot"/><feColorMatrix in="blot" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3.2 -1.05" result="pres"/>
   <feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="2" result="sp"/><feColorMatrix in="sp" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 -1.7" result="spk"/>
   <feComposite in="pres" in2="spk" operator="arithmetic" k2="1" k3="1"/><feComponentTransfer result="m"><feFuncA type="linear" slope=".9" intercept=".1"/></feComponentTransfer>
   <feComposite in="d" in2="m" operator="in"/></filter>
 <linearGradient id="ppp-gg" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="#fbe9ad"/><stop offset=".35" stop-color="#e3c46d"/><stop offset=".6" stop-color="#b98f39"/><stop offset=".8" stop-color="#ecd17f"/><stop offset="1" stop-color="#a8812e"/></linearGradient>
 <linearGradient id="ppp-gs" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#d3d9de"/><stop offset=".6" stop-color="#8f99a2"/><stop offset=".8" stop-color="#e6ebef"/><stop offset="1" stop-color="#7f8992"/></linearGradient>
 <linearGradient id="ppp-holo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff6fd2"/><stop offset=".25" stop-color="#5fb8ff"/><stop offset=".5" stop-color="#5ff2b0"/><stop offset=".75" stop-color="#ffd85f"/><stop offset="1" stop-color="#b47bff"/></linearGradient>
</defs></svg>`;
  document.body.appendChild(d.firstChild);
}
const _ppEsc = s => String(s == null ? `` : s).replace(/[&<>"]/g, c => ({ "&": `&amp;`, "<": `&lt;`, ">": `&gt;`, '"': `&quot;` })[c]);
const _ppMon = [`JAN`, `FEB`, `MAR`, `APR`, `MAY`, `JUN`, `JUL`, `AUG`, `SEP`, `OCT`, `NOV`, `DEC`];
const _ppDate = iso => { const d = new Date(iso); return isNaN(d) ? `—` : `${String(d.getDate()).padStart(2, `0`)} ${_ppMon[d.getMonth()]} ${d.getFullYear()}`; };
const _ppHash = s => { let h = 0; for (let i = 0; i < s.length; i++) h = s.charCodeAt(i) + ((h << 5) - h); return Math.abs(h); };
// fine interlaced wave lines and a rosette, printed on every page
const _ppGuilMemo = new Map();
function _ppGuil(hue) {
  if (_ppGuilMemo.has(hue)) return _ppGuilMemo.get(hue);
  let p = ``;
  for (let k = 0; k < 26; k++) { let d = ``; for (let x = 0; x <= 340; x += 4) { const y = 40 + k * 16 + Math.sin(x / 23 + k * .7) * 7 + Math.sin(x / 57 + k) * 5; d += (x ? `L` : `M`) + x + ` ` + y.toFixed(1); } p += `<path d="${d}" fill="none" stroke="hsla(${hue + k * 3},45%,55%,.22)" stroke-width=".6"/>`; }
  for (let k = 0; k < 14; k++) { let d = ``; for (let a = 0; a <= 360; a += 3) { const r = 46 + k * 5 + Math.sin(a * Math.PI / 180 * 12 + k) * 4, t = a * Math.PI / 180; d += (a ? `L` : `M`) + (250 + Math.cos(t) * r).toFixed(1) + ` ` + (180 + Math.sin(t) * r * .8).toFixed(1); } p += `<path d="${d}" fill="none" stroke="hsla(${hue + 40},40%,50%,.16)" stroke-width=".5"/>`; }
  const out = `<div class="tint"></div><svg class="guil" viewBox="0 0 340 480">${p}</svg><div class="fib"></div>`; _ppGuilMemo.set(hue, out); return out;
}
// each clan is its own country: the passport you carry is your nationality (clan comes from the base bird you hatched)
const _ppClans = {
  Percher: { bg: `#eef0f5`, pb: `#d6ddef,#c3cce5`, hue: 225, sh: 180, t: `PERCHERS`, code: `PCH`, ink: `#3b2f6b`, foil: `gg`, dot: `#141a40`, emb: `<path d="M18 64 Q52 54 94 36 M33.3 59.2 Q41.7 55.2 40.6 46.1 Q32.2 50.0 33.3 59.2 Z M45.0 55.2 Q49.7 63.2 58.7 61.2 Q54.0 53.3 45.0 55.2 Z M57.1 50.9 Q65.2 46.6 63.7 37.4 Q55.6 41.7 57.1 50.9 Z M69.5 46.1 Q74.5 53.8 83.5 51.6 Q78.5 43.8 69.5 46.1 Z M82.4 40.9 Q90.4 36.3 88.6 27.2 Q80.6 31.8 82.4 40.9 Z M94.0 36.0 Q101.7 38.1 106.2 31.5 Q98.5 29.4 94.0 36.0 Z"/>` },
  Puffer: { bg: `#e6f0ec`, pb: `#d4e6e1,#bfd7d1`, hue: 170, sh: 165, t: `PUFFERS`, code: `PFR`, ink: `#1d5560`, foil: `gs`, dot: `#0c1b1f`, emb: `<path d="M56 50 L56.0 23.0 M56.0 36.5 L61.4 30.6 M56.0 36.5 L50.6 30.6 M56.0 28.9 L60.0 24.5 M56.0 28.9 L52.0 24.5 M56 50 L79.4 36.5 M67.7 43.2 L75.5 44.9 M67.7 43.2 L70.2 35.6 M74.2 39.5 L80.1 40.7 M74.2 39.5 L76.1 33.8 M56 50 L79.4 63.5 M67.7 56.8 L70.2 64.4 M67.7 56.8 L75.5 55.1 M74.2 60.5 L76.1 66.2 M74.2 60.5 L80.1 59.3 M56 50 L56.0 77.0 M56.0 63.5 L50.6 69.4 M56.0 63.5 L61.4 69.4 M56.0 71.1 L52.0 75.5 M56.0 71.1 L60.0 75.5 M56 50 L32.6 63.5 M44.3 56.8 L36.5 55.1 M44.3 56.8 L41.8 64.4 M37.8 60.5 L31.9 59.3 M37.8 60.5 L35.9 66.2 M56 50 L32.6 36.5 M44.3 43.2 L41.8 35.6 M44.3 43.2 L36.5 44.9 M37.8 39.5 L35.9 33.8 M37.8 39.5 L31.9 40.7"/><circle cx="56" cy="50" r="4"/>` },
  Pecker: { bg: `#f3e3de`, pb: `#efd8da,#e2c3c7`, hue: 350, sh: 330, t: `PECKERS`, code: `PKR`, ink: `#7a2433`, foil: `gg`, dot: `#2a0c12`, emb: `<path d="M26.0 72.0 L25.8 71.0 L25.7 70.0 L25.6 69.1 L25.5 68.2 L25.4 67.3 L25.4 66.4 L25.4 65.6 L25.5 64.8 L25.6 64.0 L25.7 63.2 L25.8 62.4 L26.0 61.7 L26.2 61.0 L26.4 60.3 L26.6 59.7 L26.9 59.0 L27.2 58.4 L27.5 57.9 L27.8 57.3 L28.1 56.8 L28.5 56.3 L28.9 55.8 L29.3 55.3 L29.7 54.9 L30.1 54.5 L30.6 54.1 L31.0 53.8 L31.5 53.5 L32.0 53.2 L32.5 52.9 L33.0 52.6 L33.5 52.4 L34.0 52.2 L34.6 52.0 L35.1 51.9 L35.6 51.8 L36.2 51.7 L36.7 51.6 L37.3 51.6 L37.9 51.6 L38.4 51.6 L39.0 51.6 L39.5 51.7 L40.1 51.8 L40.6 51.9 L41.2 52.0 L41.7 52.2 L42.3 52.4 L42.8 52.6 L43.3 52.9 L43.8 53.2 L44.3 53.5 L44.8 53.8 L45.3 54.2 L45.8 54.6 L46.3 55.0 L46.7 55.5 L47.2 56.0 L47.6 56.5 L48.0 57.0 L48.4 57.5 L48.8 58.0 L49.2 58.4 L49.7 58.9 L50.1 59.3 L50.5 59.8 L50.9 60.2 L51.4 60.6 L51.8 61.0 L52.3 61.4 L52.7 61.7 L53.2 62.1 L53.7 62.4 L54.1 62.7 L54.6 63.0 L55.0 63.3 L55.5 63.6 L56.0 63.9 L56.5 64.1 L56.9 64.3 L57.4 64.5 L57.9 64.7 L58.3 64.9 L58.8 65.1 L59.3 65.2 L59.8 65.3 L60.2 65.4 L60.7 65.5 L61.2 65.6 L61.6 65.6 L62.1 65.7 L62.5 65.7 L63.0 65.7 L63.5 65.6 L63.9 65.6 L64.3 65.5 L64.8 65.4 L65.2 65.3 L65.6 65.2 L66.1 65.0 L66.5 64.8 L66.9 64.6 L67.3 64.4 L67.7 64.2 L68.1 63.9 L68.5 63.6 L68.9 63.3 L69.2 63.0 L69.6 62.6 L70.0 62.2 L70.3 61.8 L70.7 61.4 L71.0 60.9 L71.3 60.4 L71.6 59.9 L71.9 59.4 L72.2 58.8 L72.5 58.2 L72.7 57.6 L73.0 57.0 L73.2 56.5 L73.4 55.9 L73.6 55.4 L73.7 54.8 L73.9 54.3 L74.1 53.7 L74.2 53.2 L74.4 52.7 L74.5 52.1 L74.7 51.6 L74.8 51.1 L74.9 50.6 L75.1 50.0 L75.2 49.5 L75.3 49.0 L75.4 48.5 L75.6 48.0 L75.7 47.5 L75.8 47.0 L75.9 46.5 L76.0 46.0 L76.2 45.5 L76.3 45.0 L76.4 44.5 L76.6 44.1 L76.7 43.6 L76.8 43.1 L77.0 42.7 L77.1 42.2 L77.2 41.8 L77.4 41.3 L77.6 40.9 L77.7 40.4 L77.9 40.0 L78.1 39.6 L78.3 39.1 L78.4 38.7 L78.6 38.3 L78.9 37.9 L79.1 37.5 L79.3 37.1 L79.5 36.7 L79.8 36.4 L80.0 36.0 L80.3 35.6 L80.6 35.3 L80.9 34.9 L81.2 34.6 L81.5 34.2 L81.8 33.9 L82.2 33.6 L82.5 33.3 L82.9 32.9 L83.3 32.6 L83.7 32.4 L84.1 32.1 L84.6 31.8 L85.0 31.5 L85.5 31.3 L86.0 31.0" stroke-width="7.5"/><path d="M20.8 67.1 L30.1 67.0 M21.5 60.3 L30.5 62.7 M24.6 53.8 L32.1 59.2 M30.2 48.8 L34.7 57.0 M37.7 46.9 L37.9 56.2 M45.2 48.6 L41.1 57.0 M51.0 53.3 L43.9 59.3 M54.3 57.0 L48.0 63.8 M57.9 59.6 L53.4 67.7 M61.5 60.9 L60.2 70.1 M64.5 60.6 L68.1 69.2 M66.9 58.6 L74.2 64.4 M68.8 55.0 L77.5 58.2 M70.2 50.1 L79.2 52.5 M71.6 44.8 L80.6 47.0 M73.3 39.0 L82.0 42.2 M76.5 33.0 L84.0 38.5" stroke="__BG__" stroke-width="1.3"/>` },
};
const _ppClanOf = c => _ppClans[c] || _ppClans.Percher;
const _ppArms = (K, F, eye) => `<g fill="none" stroke="${F}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><defs><clipPath id="ppp-gcl"><circle cx="60" cy="60" r="38.7"/></clipPath></defs><circle cx="60" cy="60" r="40" stroke-width="3.4"/><g stroke-width="1.8" clip-path="url(#ppp-gcl)"><line x1="20" y1="60" x2="100" y2="60"/><path d="M17.9 38.9 Q60.0 46.3 102.1 38.9 M17.9 81.1 Q60.0 73.7 102.1 81.1"/><ellipse cx="60" cy="60" rx="10.36" ry="40"/><ellipse cx="60" cy="60" rx="28.28" ry="40"/></g></g>`;
function _ppCover(clan) {
  const K = _ppClanOf(clan), F = `url(#ppp-${K.foil})`, fc = K.foil === `gs` ? `silver` : `gold`;
  return `<div class="cover"><div class="grain"></div><div class="t ${fc}">PASSPORT</div>
  <svg class="emb" viewBox="0 0 120 120"><defs><pattern id="ppp-gte" patternUnits="userSpaceOnUse" x="-34.82" y="-53.57" width="107.14" height="107.14"><image href="${(_ppTex||{}).leather||``}" width="107.14" height="107.14"/></pattern></defs>${_ppArms(K, F, fc === `silver` ? `#c9d0d6` : `#d4ae5a`)}<g opacity=".55">${_ppArms(K, `url(#ppp-gte)`, `none`)}</g></svg>
  <div class="n ${fc}">${K.t.charAt(0) + K.t.slice(1).toLowerCase()}</div>
  <svg class="chip2" viewBox="0 0 50 32"><defs><pattern id="ppp-gtc" patternUnits="userSpaceOnUse" x="-152" y="-404" width="200" height="200"><image href="${(_ppTex||{}).leather||``}" width="200" height="200"/></pattern></defs><rect x="1" y="1" width="48" height="30" rx="3" fill="none" stroke="${F}" stroke-width="2.4"/><line x1="1" y1="11" x2="49" y2="11" stroke="${F}" stroke-width="2.2"/><line x1="1" y1="21" x2="49" y2="21" stroke="${F}" stroke-width="2.2"/><circle cx="25" cy="16" r="6.5" fill="none" stroke="${F}" stroke-width="2.4"/><g opacity=".55"><rect x="1" y="1" width="48" height="30" rx="3" fill="none" stroke="url(#ppp-gtc)" stroke-width="2.4"/><line x1="1" y1="11" x2="49" y2="11" stroke="url(#ppp-gtc)" stroke-width="2.2"/><line x1="1" y1="21" x2="49" y2="21" stroke="url(#ppp-gtc)" stroke-width="2.2"/><circle cx="25" cy="16" r="6.5" fill="none" stroke="url(#ppp-gtc)" stroke-width="2.4"/></g></svg>
  <div class="light"></div></div>`;
}
// the ID page
function _ppIdPage(v) {
  const K = _ppClanOf(v.clan);
  const words = String(v.u).split(`-`), given = words.pop().toUpperCase(), sur = words.join(`-`).toUpperCase();   /* one-word names: just a given name */
  const sig = (words.map(w => w[0] ? w[0].toUpperCase() + `.` : ``).join(``) + ` ` + given.charAt(0) + given.slice(1).toLowerCase()).trim();
  const no = v.no ? `PP` + String(v.no).padStart(7, `0`) : `PP·······`;
  const iss = v.issued ? new Date(v.issued) : null, yymmdd = iss && !isNaN(iss) ? String(iss.getFullYear()).slice(2) + String(iss.getMonth() + 1).padStart(2, `0`) + String(iss.getDate()).padStart(2, `0`) : `000000`;
  const m1 = (`P<` + K.code + (sur ? sur.replace(/-/g, `<`) + `<<` : ``) + given + `<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<`).slice(0, 38);
  const m2 = (no.replace(/·/g, `0`) + (v.no ? v.no % 10 : 0) + K.code + yymmdd + `4B` + String(v.stamps || 0).padStart(4, `0`) + `<<<<<<<<<<<<<<<<<<<<`).slice(0, 36) + String(v.pages || 0).padStart(2, `0`);
  const img = v.img ? _ppEsc(v.img) : ``;
  const cx = 287, cy = 281; let circ = ``; for (let k = 0; k < 30; k++) { const a = k / 30 * Math.PI * 2; circ += `<circle cx="${(cx + Math.cos(a) * 17).toFixed(2)}" cy="${(cy + Math.sin(a) * 17).toFixed(2)}" r="25"/>`; }
  let wave = ``; for (const [R0, A, N] of [[46, 2.4, 36], [50, 1.6, 48]]) { let d = ``; for (let t = 0; t <= Math.PI * 2 + .001; t += .01) { const r = R0 + A * Math.sin(N * t); d += (t ? `L` : `M`) + (cx + Math.cos(t) * r).toFixed(2) + ` ` + (cy + Math.sin(t) * r).toFixed(2); } wave += `<path d="${d}Z"/>`; }
  return `<div class="page">${_ppGuil(K.hue)}
  <div style="position:absolute;left:14px;right:14px;top:14px;display:flex;justify-content:space-between;align-items:flex-start">
    <div><div class="lbl">Perch Posts</div><div style="font:800 13px Georgia,serif;letter-spacing:.14em;color:${K.ink};margin-top:1px">${K.t}</div><div class="lbl" style="margin-top:1px">Passport / Passeport / Pasaporte</div></div>
    <svg width="30" height="30" viewBox="14 8 84 84"><g fill="none" stroke="${K.ink}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">${K.emb.replace(/__EYE__/g, K.ink).replace(/__BG__/g, K.bg)}</g></svg></div>
  <div style="position:absolute;left:14px;top:52px;width:104px;height:132px;border-radius:4px;background:linear-gradient(${K.pb});overflow:hidden;box-shadow:inset 0 0 0 1px rgba(0,0,0,.12)">${img ? `<img src="${img}" alt="" style="position:absolute;left:${v.hat ? 20 : -13}px;top:${v.hat ? 34 : 1}px;width:${v.hat ? 64 : 130}px;height:${v.hat ? 64 : 130}px;object-fit:contain">` : ``}</div>
  <svg style="position:absolute;left:0;top:0;width:340px;height:480px;pointer-events:none" viewBox="0 0 340 480"><g fill="none" stroke="url(#ppp-holo)" stroke-width=".45" opacity=".55">${circ}</g><g fill="none" stroke="url(#ppp-holo)" stroke-width=".5" opacity=".6">${wave}</g></svg>
  ${img ? `<img src="${img}" alt="" style="position:absolute;left:${v.hat ? 254 : 232}px;top:${v.hat ? 248 : 226}px;width:${v.hat ? 66 : 110}px;height:${v.hat ? 66 : 110}px;object-fit:contain;opacity:.22;filter:grayscale(1) contrast(1.3)">
    <div style="position:absolute;left:${v.hat ? 254 : 232}px;top:${v.hat ? 248 : 226}px;width:${v.hat ? 66 : 110}px;height:${v.hat ? 66 : 110}px;-webkit-mask:url('${img}') center/contain no-repeat;mask:url('${img}') center/contain no-repeat;background:linear-gradient(120deg,#ff6fd2 0%,#5fb8ff 28%,#5ff2b0 50%,#ffd85f 72%,#b47bff 100%);opacity:.55"></div>
    <div style="position:absolute;left:${v.hat ? 254 : 232}px;top:${v.hat ? 248 : 226}px;width:${v.hat ? 66 : 110}px;height:${v.hat ? 66 : 110}px;-webkit-mask:url('${img}') center/contain no-repeat;mask:url('${img}') center/contain no-repeat;background:linear-gradient(120deg,transparent 32%,rgba(255,255,255,.95) 46%,transparent 60%);opacity:.7"></div>` : ``}
  <div style="position:absolute;left:130px;top:50px;right:12px">
   <div style="display:flex;gap:14px"><div><div class="lbl">Type</div><div class="val">P</div></div><div><div class="lbl">Code</div><div class="val">${K.code}</div></div><div><div class="lbl">Passport No.</div><div class="val">${no}</div></div></div>
   <div class="lbl">Surname / Nom</div><div class="val">${_ppEsc(sur || `—`)}</div>
   <div class="lbl">Given names / Prénoms</div><div class="val">${_ppEsc(given)}</div>
   <div style="display:flex;gap:18px"><div><div class="lbl">Nationality</div><div class="val">${_ppEsc((v.clan || `—`).toUpperCase())}</div></div><div style="min-width:0"><div class="lbl">Plumage</div><div class="val" data-plum>${_ppEsc(v.plum || `—`)}</div></div></div>
   <div class="lbl">Rank</div><div class="val">${_ppEsc((v.rank || `—`).toUpperCase())}</div>
   <div class="lbl">Date of issue</div><div class="val">${v.issued ? _ppDate(v.issued) : `—`}</div></div>
  <div style="position:absolute;left:14px;top:196px;width:110px"><div class="lbl">Signature</div><div style="position:relative;height:40px;margin-top:-2px"><div style="position:absolute;left:-2px;top:-6px;font:400 32px 'PP Sig',cursive;color:#23236b;transform:rotate(-7deg);white-space:nowrap;letter-spacing:-.5px">${_ppEsc(sig)}</div>
   <svg width="118" height="40" style="position:absolute;left:-6px;top:2px;overflow:visible"><path d="M8 33 C 34 27, 58 31, 80 25 S 108 17, 114 21 C 106 27, 90 31, 74 33" fill="none" stroke="#23236b" stroke-width="1.15" stroke-linecap="round" opacity=".85"/></svg></div></div>
  <div style="position:absolute;left:14px;right:14px;top:248px;height:1px;background:rgba(80,60,140,.25)"></div>
  <div style="position:absolute;left:14px;top:262px;width:210px;display:grid;grid-template-columns:1fr 1fr;column-gap:14px"><div><div class="lbl">Flaps</div><div class="val">${_ppEsc(v.flaps ?? 0)}</div></div><div><div class="lbl">Worms</div><div class="val">${_ppEsc(v.worms ?? 0)}</div></div><div><div class="lbl">Stamps</div><div class="val">${v.stamps ?? `—`}</div></div><div><div class="lbl">Pages</div><div class="val">${v.pages ?? `—`}</div></div></div>
  ${_ppRankBox(v)}
  <div class="mrz">${_ppEsc(m1)}
${_ppEsc(m2)}</div></div>`;
}
// rank stamp on the ID page, under the counts: the rank's emblem, title and description in its own ink (picked style: A with a dashed border)
const _ppRankIco = {
  Endangered: `<path d="M8 3 C8 8 12 10 12 12 C12 14 8 16 8 21 M16 3 C16 8 12 10 12 12 C12 14 16 16 16 21 M7 3 H17 M7 21 H17 M10 19.5 Q12 17.5 14 19.5"/>`,
  Hatchling: `<path d="M12 3 C7.5 3 5 9 5 14 A7 7 0 0 0 19 14 C19 9 16.5 3 12 3 Z"/><path d="M5.6 11.5 L8.5 13.5 L10.5 10.5 L13 13.5 L15.3 10.5 L18.4 12.6"/>`,
  Nestling: `<path d="M3 13 Q12 23 21 13 Z"/><path d="M6 16 L10 14 M18 16 L14 14"/><circle cx="12" cy="9" r="2.8"/><path d="M14.6 8.6 L17 9.4 L14.6 10.1"/>`,
  Fledgling: `<path d="M8 19 V14.8 M8 19 L4.8 16.0 M8 19 L11.2 16.0 M8 19 V20.8"/><path d="M16 12 V7.8 M16 12 L12.8 9.0 M16 12 L19.2 9.0 M16 12 V13.8"/>`,
  Forager: `<path d="M3 16 C5 11 7 11 9 15 S13 19 15 15 S19 10 21 12.5"/><circle cx="20" cy="11.6" r=".7" fill="currentColor" stroke="none"/>`,
  'Bird of Prey': `<path d="M5 21 C5 12 8 5.5 14 5.5 C17 5.5 19 7.5 20 9.5 L22 12.5 L19 12.6 C18 14 16 14.6 14 14 C12.4 15.8 11.4 18 11.2 21"/><path d="M12.5 8.4 L16.5 8.2"/><circle cx="15.6" cy="9.8" r=".9" fill="currentColor" stroke="none"/>`,
  'Mixed-Flock Attendant': `<path d="M3 9 Q5 7 7 9 Q9 7 11 9 M13 6 Q15 4 17 6 Q19 4 21 6 M8 15.5 Q10 13.5 12 15.5 Q14 13.5 16 15.5"/>`,
  'Seasoned Migrant': `<path d="M10.4 7 L12 5.6 L13.6 7 M6.4 11 L8 9.6 L9.6 11 M14.4 11 L16 9.6 L17.6 11 M2.4 15 L4 13.6 L5.6 15 M18.4 15 L20 13.6 L21.6 15"/><path d="M12 19 V12" stroke-dasharray="1.5 1.8"/>`,
  'Continental Migrant': `<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12 H21 M4.5 7.5 Q12 9.5 19.5 7.5 M4.5 16.5 Q12 14.5 19.5 16.5"/>`,
  'Peak Plumage': `<path d="M19 3 C11 4 6 10 6 18 C14 18 19 12 19 3 Z"/><path d="M4 21 L15 8 M8.5 15.5 L12 15.5 M10.5 13 L14.5 12.8"/>`,
  'Master Layer': `<path d="M3 13 H21 Q12 23 3 13 Z"/><ellipse cx="8" cy="10.2" rx="2.2" ry="2.8"/><ellipse cx="12" cy="9" rx="2.2" ry="2.8"/><ellipse cx="16" cy="10.2" rx="2.2" ry="2.8"/>`,
  'Legendary Brood': `<path d="M4 17 L3 8 L8 12 L12 5 L16 12 L21 8 L20 17 Z M4 20.5 H20"/><circle cx="12" cy="13.5" r="1.3"/>`,
};
const _ppInk = c => { const h = c.replace(`#`, ``), n = parseInt(h, 16), m = (v, d) => Math.round(v * .42 + d * .58);
  return `rgb(${m(n >> 16 & 255, 0x1d)},${m(n >> 8 & 255, 0x18)},${m(n & 255, 0x30)})`; };
function _ppRankBox(v) {
  const R = typeof _RANKS !== `undefined` ? _RANKS : null; if (!R) return ``;
  const w = Number(v.worms) || 0; let i = R.findIndex(r => r.n === v.rank); if (i < 0) i = R.findIndex(r => w >= r.min && w <= r.max); if (i < 0) return ``;
  const r = R[i], c = _ppInk(r.c);
  return `<div class="rks rkA" style="--c:${c}"><div class="em"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="${c}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" style="color:${c};display:block">${_ppRankIco[r.n] || ``}</svg></div><div class="tx"><div class="ti">${_ppEsc(r.n.toUpperCase())}</div><div class="de">${_ppEsc(r.d)}</div></div></div>`;
}

// ── stamps: each kind has its own shape and ink ──
let _ppSid = 0;
const _ppT = (s, n) => _ppEsc(String(s).toUpperCase().slice(0, n || 22));
const _ppStampShapes = {
  circle: (c, top, bot, mid, small, dashed) => { const id = `ppr${++_ppSid}`;
    return { w: 128, h: 128, svg: `<svg viewBox="-64 -64 128 128" width="128" height="128"><defs><path id="${id}" d="M -46,0 A 46,46 0 1 1 46,0 A 46,46 0 1 1 -46,0"/></defs><g fill="none" stroke="${c}" stroke-width="3"><circle r="60"${dashed ? ` stroke-dasharray="6 3"` : ``}/><circle r="54" stroke-width="1.4"/><circle r="34" stroke-width="1.6"/></g>
    <g fill="${c}" font-family="Helvetica,Arial,sans-serif" font-weight="800"><text font-size="${top.length > 14 ? 10 : 12}" letter-spacing="2.2"><textPath href="#${id}" startOffset="25%" text-anchor="middle">${_ppT(top)}</textPath></text><text font-size="9" letter-spacing="1.8"><textPath href="#${id}" startOffset="75%" text-anchor="middle">${_ppT(bot)}</textPath></text>
    <text y="-4" font-size="10" text-anchor="middle">${_ppT(mid, 12)}</text><text y="10" font-size="11" text-anchor="middle">${_ppT(small, 12)}</text></g></svg>` }; },
  rect: (c, big, sm, date) => ({ w: 152, h: 100, svg: `<svg viewBox="0 0 152 100" width="152" height="100"><g fill="none" stroke="${c}" stroke-width="3.2"><rect x="3" y="3" width="146" height="94" rx="4"/><rect x="9" y="9" width="134" height="82" rx="2" stroke-width="1.3"/></g>
    <g fill="${c}" font-family="Helvetica,Arial,sans-serif" font-weight="900" text-anchor="middle"><text x="76" y="37" font-size="${big.length > 10 ? 15 : 20}" letter-spacing="2.5">${_ppT(big, 14)}</text><text x="76" y="52" font-size="8" letter-spacing="3">${_ppT(sm, 22)}</text><line x1="22" y1="60" x2="130" y2="60" stroke="${c}" stroke-width="1.2"/><text x="76" y="78" font-size="11" letter-spacing="1">${_ppT(date)}</text></g></svg>` }),
  tri: (c, big, sm, date) => ({ w: 134, h: 120, svg: `<svg viewBox="0 0 134 120" width="134" height="120"><g fill="none" stroke="${c}" stroke-width="3"><path d="M67 5 L129 114 L5 114 Z"/><path d="M67 18 L117 106 L17 106 Z" stroke-width="1.2"/></g>
    <g fill="${c}" font-family="Helvetica,Arial,sans-serif" font-weight="900" text-anchor="middle"><text x="67" y="68" font-size="${big.length > 9 ? 11 : 15}" letter-spacing="1.2">${_ppT(big, 14)}</text><text x="67" y="83" font-size="10" letter-spacing="1.5">${_ppT(sm)}</text><text x="67" y="98" font-size="8.5">${_ppT(date)}</text></g></svg>` }),
  oval: (c, top, mid, date) => ({ w: 176, h: 104, svg: `<svg viewBox="0 0 176 104" width="176" height="104"><g fill="none" stroke="${c}" stroke-width="3"><ellipse cx="88" cy="52" rx="84" ry="48"/><ellipse cx="88" cy="52" rx="76" ry="40" stroke-width="1.2" stroke-dasharray="3 3"/></g>
    <g fill="${c}" font-family="Helvetica,Arial,sans-serif" font-weight="900" text-anchor="middle"><text x="88" y="35" font-size="10" letter-spacing="5">${_ppT(top)}</text><text x="88" y="56" font-size="${mid.length > 20 ? 9.5 : 11.5}">${_ppEsc(String(mid).slice(0, 30))}</text><text x="88" y="73" font-size="9" letter-spacing="1">${_ppT(date)}</text></g></svg>` }),
  // rank seal: the rank's emblem in the middle, its name round the top, the date round the bottom
  seal: (c, name, date, ico) => { const id = `ppr${++_ppSid}`, n = String(name).length, fs = n > 16 ? 7.4 : n > 11 ? 8.8 : 11, ls = n > 16 ? 1 : n > 11 ? 1.5 : 2.2;
    return { w: 128, h: 128, svg: `<svg viewBox="-64 -64 128 128" width="128" height="128"><defs><path id="${id}" d="M -46,0 A 46,46 0 1 1 46,0 A 46,46 0 1 1 -46,0"/><path id="${id}b" d="M -51.5,0 A 51.5,51.5 0 0 0 51.5,0"/></defs><g fill="none" stroke="${c}"><circle r="60" stroke-width="2.6" stroke-dasharray="7 4"/><circle r="54" stroke-width="1.4"/><circle r="31" stroke-width="1.8"/></g>
    <g fill="${c}" font-family="Helvetica,Arial,sans-serif" font-weight="800"><text font-size="${fs}" letter-spacing="${ls}"><textPath href="#${id}" startOffset="25%" text-anchor="middle">${_ppT(name, 24)}</textPath></text><text font-size="8.6" letter-spacing="1.8"><textPath href="#${id}b" startOffset="50%" text-anchor="middle">${_ppT(date)}</textPath></text></g>
    <g transform="translate(-19 -19) scale(1.58)" fill="none" stroke="${c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="color:${c}">${ico}</g></svg>` }; },
  oct: (c, icon, big, sm, date) => ({ w: 120, h: 120, svg: `<svg viewBox="-60 -60 120 120" width="120" height="120"><g fill="none" stroke="${c}" stroke-width="3"><polygon points="-24,-56 24,-56 56,-24 56,24 24,56 -24,56 -56,24 -56,-24"/></g>
    <g fill="${c}" font-family="Helvetica,Arial,sans-serif" font-weight="900" text-anchor="middle"><text y="-18" font-size="13">${icon}</text><text y="-2" font-size="${big.length > 9 ? 10 : 12}" letter-spacing="1.4">${_ppT(big, 12)}</text><text y="13" font-size="7.5" letter-spacing="1.6">${_ppT(sm, 18)}</text><text y="28" font-size="8.5">${_ppT(date)}</text></g></svg>` }),
};
const _ppTagInk = { General: `#475569`, Sports: `#15805a`, Science: `#0e7490`, Nature: `#4d7c0f`, Entertainment: `#be185d`, Random: `#c2410c`, Announcements: `#1e3a8a` };
function _ppStamp(s) {
  const S = _ppStampShapes, d = _ppDate(s.at), t = String(s.k).split(`:`), x = s.d || {};
  if (t[0] === `rank`) { const R = typeof _RANKS !== `undefined` ? _RANKS.find(r => r.n === t[1]) : null;
    return S.seal(R ? _ppInk(R.c) : `#334155`, t[1], d, _ppRankIco[t[1]] || ``); }
  if (t[0] === `tag`) { const c = _ppTagInk[t[1]] || `#334155`;
    return t[2] === `1` ? S.circle(c, t[1], `★ first post ★`, d.slice(0, 6), d.slice(7)) : t[2] === `50` ? S.tri(c, t[1], `50 posts`, d) : S.rect(c, t[1], `100 posts`, d); }
  switch (s.k) {
    case `post1`: return S.circle(`#2d4fb8`, `first post`, `★ perch posts ★`, d.slice(0, 6), d.slice(7));
    case `chirp1`: return S.oval(`#0f7f86`, `first chirp`, `♪ CHIRP CHIRP ♪`, d);
    case `huddle`: return S.oct(`#c2620f`, `◆`, `huddle up`, `first huddle`, d);
    case `generous`: return S.circle(`#c2620f`, `generous`, `first worm given`, `♥`, d.slice(0, 6), true);
    case `rewarded`: return S.circle(`#b0306b`, `rewarded`, `first worm received`, `★`, d.slice(0, 6), true);
    case `tagged`: return S.oval(`#6b2fa8`, `tagged`, x.by ? `by @${x.by}` : `@ you`, d);
    case `popular`: return S.circle(`#a16207`, `popular`, `25 flaps`, `▲`, d.slice(0, 6));
    case `chatterbox`: return S.rect(`#0f7f86`, `chatterbox`, `100 chirps`, d);
    case `nightowl`: return S.oct(`#222433`, `☾`, `night owl`, x.time ? `posted at ${x.time}` : `posted 2–5 am`, d);
    case `streak`: return S.rect(`#15805a`, `7 day streak`, `posted every day`, d);
    case `globetrotter`: return S.circle(`#1f6fb2`, `globetrotter`, `5 countries`, `◉`, d.slice(0, 6));
    case `cage`: return S.rect(`#b8233a`, `detained`, `held in the cage`, d);
    case `staff`: return S.oval(`#7c3aed`, `staff`, x.role === `admin` ? `ADMINISTRATOR` : `MODERATOR`, d);
  }
  return S.circle(`#334155`, s.label || s.k, ``, d.slice(0, 6), d.slice(7));
}
// six stamps to a page, each pressed at its own angle (always the same for the same stamp)
const _ppSlots = [[88, 104], [248, 98], [92, 248], [250, 244], [92, 392], [248, 388]];
function _ppStampPage(list, n, clan) {
  const K = _ppClanOf(clan);
  let h = ``;
  list.forEach((s, i) => { const st = _ppStamp(s), hs = _ppHash(s.k), rot = (hs % 29) - 14, [cx, cy] = _ppSlots[i], jx = (hs >> 5) % 11 - 5, jy = (hs >> 9) % 11 - 5;
    h += `<div class="stamp" style="left:${cx - st.w / 2 + jx}px;top:${cy - st.h / 2 + jy}px;width:${st.w}px;height:${st.h}px;transform:rotate(${rot}deg)">${st.svg}</div>`; });
  return `<div class="page">${_ppGuil(K.sh + n * 20)}<div class="ptitle">VISAS · STAMPS</div><svg width="24" height="24" viewBox="14 8 84 84" class="parms"><g fill="none" stroke="${K.ink}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">${K.emb.replace(/__EYE__/g, K.ink).replace(/__BG__/g, K.bg)}</g></svg>${h}<div class="pnum">${n + 1}</div></div>`;
}
// the passport photo's main body colour, as a plumage name
const _ppPlumNames = [[`TEAL`, [40, 150, 140]], [`EMERALD`, [30, 140, 80]], [`NAVY`, [30, 50, 110]], [`SKY BLUE`, [90, 170, 230]], [`CRIMSON`, [190, 30, 50]], [`GOLDEN`, [230, 180, 40]], [`RUST`, [180, 90, 40]], [`VIOLET`, [130, 80, 200]], [`ROSE`, [230, 120, 160]], [`SLATE`, [100, 110, 125]], [`SNOW`, [235, 235, 235]], [`RAVEN`, [30, 30, 35]], [`OLIVE`, [120, 130, 50]], [`TAWNY`, [190, 140, 90]], [`LILAC`, [190, 160, 220]], [`SAND`, [215, 195, 150]], [`SILVER`, [175, 185, 190]], [`POWDER BLUE`, [160, 195, 215]], [`PINE`, [30, 75, 60]], [`MIDNIGHT`, [25, 35, 65]], [`CORAL`, [240, 120, 100]], [`LIME`, [160, 210, 60]], [`PLUM`, [110, 40, 90]], [`CHESTNUT`, [120, 60, 35]], [`CHARCOAL`, [60, 62, 68]]];
function _ppPlumage(src, cb) {
  const im = new Image(); im.onload = () => { try { const c = document.createElement(`canvas`); c.width = c.height = 48; const x = c.getContext(`2d`); x.drawImage(im, 0, 0, 48, 48);
    const D = x.getImageData(0, 0, 48, 48).data, bins = new Map();
    for (let i = 0; i < D.length; i += 4) { if (D[i + 3] < 200) continue; const mx = Math.max(D[i], D[i + 1], D[i + 2]), mn = Math.min(D[i], D[i + 1], D[i + 2]); if (mx < 45 || mn > 225) continue;   /* outlines, eyes, hats and shine aren't plumage */ const k = (D[i] >> 5) + `,` + (D[i + 1] >> 5) + `,` + (D[i + 2] >> 5), b = bins.get(k) || [0, 0, 0, 0]; b[0] += D[i]; b[1] += D[i + 1]; b[2] += D[i + 2]; b[3]++; bins.set(k, b); }
    let best = null; for (const b of bins.values()) if (!best || b[3] > best[3]) best = b; if (!best) return;
    const col = [best[0] / best[3], best[1] / best[3], best[2] / best[3]];
    cb(_ppPlumNames.reduce((a, n) => { const d = n[1].reduce((s, v, k) => s + (v - col[k]) ** 2, 0); return d < a[1] ? [n[0], d] : a; }, [``, 1e12])[0]); } catch (e) {} };
  im.src = src;
}
function _ppPassMount(el, p) {
  _ppPassCss();
  let dead = false, idx = 0, busy = false, data = null, img = null, plum = null, pages = [];
  const em = [`🐤`, `🐦`, `🐧`][_ppHash(p.u) % 3];
  const view = () => ({ hat: p.hat, u: p.u, no: data && data.no, issued: (data && data.issued) || p.issued, clan: p.clan, rank: p.rank, flaps: p.flaps, worms: p.worms,
    stamps: data ? data.stamps.length : null, pages: data ? pages.length - 2 : null, img, plum });
  // pages: the cover, the ID page, then six stamps to a page (no blank page at the end)
  const build = () => { const st = data ? data.stamps : [], out = [_ppCover(p.clan), ``];
    for (let i = 0; i < st.length; i += 6) out.push(_ppStampPage(st.slice(i, i + 6), out.length - 1, p.clan));
    pages = out; pages[1] = _ppIdPage(view()); };
  el.innerHTML = `<div class="ppp-in" data-clan="${_ppEsc(p.clan || ``)}"><div class="ppp-spine"></div><div class="ppp-book"></div></div>`; const box = el.querySelector(`.ppp-book`), inner = el.firstChild;
  const fit = () => { const w = Math.min(354, el.clientWidth || 354), k = w / 354; inner.style.transform = `scale(${k})`; el.style.height = 480 * k + `px`; };
  // each page is made once and the same piece is moved around (so its pictures never reload as you flip)
  const made = new Map();
  const pageNode = i => { let n = made.get(i); if (!n || n._h !== pages[i + 1]) { n = document.createElement(`div`); n.style.cssText = `position:absolute;inset:0`; n.innerHTML = pages[i + 1]; n._h = pages[i + 1]; made.set(i, n); } return n; };
  const show = i => { inner.classList.toggle(`paper`, i >= 1); box.classList.toggle(`covering`, i === -1); box.innerHTML = ``; const pg = document.createElement(`div`); pg.className = `ppp-pg`; pg.appendChild(pageNode(i)); box.appendChild(pg); };
  // turning a page: the sheet lifts from its left edge and swings over (you see its plain back as it goes), the page
  // underneath is in its shadow until the sheet clears it. Back is the same in reverse.
  const turn = (to, fwd) => { if (busy || to < -1 || to > pages.length - 2) return;
    busy = true; const top = fwd ? idx : to, bottom = fwd ? to : idx;
    const under = document.createElement(`div`); under.className = `ppp-pg`; under.appendChild(pageNode(bottom));
    const shade = document.createElement(`div`); shade.className = `ppp-shade`; under.appendChild(shade);
    const leaf = document.createElement(`div`); leaf.className = `ppp-leaf`;
    box.classList.toggle(`covering`, top === -1); leaf.style.transformOrigin = top === -1 ? `-14px 50%` : `0 50%`;   /* the cover hinges at the spine's outer edge */
    leaf.appendChild(pageNode(top));   // one solid sheet: it swings to edge-on at the spine and tucks behind it (its back never shows)
    box.innerHTML = ``; box.appendChild(under); box.appendChild(leaf); box.classList.add(`turning`); if (!fwd) inner.classList.toggle(`paper`, to >= 1);   /* going back: what's on the left changes as the page lifts off it */
    const ms = 560, ease = fwd ? `cubic-bezier(.5,0,.75,.6)` : `cubic-bezier(.25,.4,.5,1)`;
    leaf.animate(fwd ? [{ transform: `rotateY(0deg)` }, { transform: `rotateY(-92deg)` }] : [{ transform: `rotateY(-92deg)` }, { transform: `rotateY(0deg)` }], { duration: ms, easing: ease, fill: `forwards` });
    const sh = shade.animate(fwd ? [{ opacity: .9 }, { opacity: 0 }] : [{ opacity: 0 }, { opacity: .9 }], { duration: ms, easing: ease, fill: `forwards` });
    sh.onfinish = () => { if (dead) return; idx = to;
      if (fwd) { leaf.remove(); shade.remove(); inner.classList.toggle(`paper`, idx >= 1); box.classList.toggle(`covering`, idx === -1); }
      else { under.remove(); leaf.getAnimations().forEach(a => a.cancel()); leaf.className = `ppp-pg`; }
      busy = false; }; };
  const wiggle = () => { if (el.animate) el.animate([{ transform: `translateX(0)` }, { transform: `translateX(-7px)` }, { transform: `translateX(6px)` }, { transform: `translateX(-3px)` }, { transform: `translateX(0)` }], { duration: 360, easing: `ease-out` }); };
  const onTap = e => { e.stopPropagation(); if (busy) return; const r = el.getBoundingClientRect(), right = e.clientX - r.left > r.width / 2;
    if (idx === -1) { turn(0, true); return; }   // closed: tap the cover to open it
    if (right) { if (idx >= pages.length - 2) wiggle(); else turn(idx + 1, true); } else turn(idx - 1, false); };
  el.addEventListener(`click`, onTap);
  build(); show(idx); fit(); const ro = typeof ResizeObserver !== `undefined` ? new ResizeObserver(fit) : null; ro && ro.observe(el);
  // the photo or plumage arrived: only the ID page is redrawn (and only shown again if it's the page open)
  const idAgain = () => { if (dead) return; pages[1] = _ppIdPage(view()); if (idx === 0 && !busy) show(0); };
  const setImg = (src, final) => { if (dead || !src || (img && !final)) return; img = src; idAgain(); if (final) _ppPlumage(src, n => { if (dead) return; plum = n; idAgain(); }); };
  // the bird's own logo (admins: the admin bird). The small version shows straight away while the full one is made.
  if (p.hat) setImg(`/admin-bird.png`, true);
  else try { const f = _ppKit.get(p.u, em, `f`); if (f && f.f) setImg(f.f, true);
    else { const t = _ppKit.get(p.u, em, `t`); if (t && t.t) setImg(t.t, false); _ppKit.sub(p.u, em, () => { const r2 = _ppKit.get(p.u, em, `f`); if (r2 && r2.f) setImg(r2.f, true); }, `f`); } } catch (e) {}
  fetch(`${R}/passport?u=${encodeURIComponent(p.u)}`).then(r => r.json()).then(j => { if (dead || !j || !j.stamps) return; data = j; build();
      // opened from a "you earned a stamp" notification: go to the page that stamp is on
      const go = window._ppPassGo; if (go && p.own) { window._ppPassGo = null; const i = j.stamps.findIndex(s => s.k === go); if (i >= 0) { show(idx); setTimeout(() => turn(1 + Math.floor(i / 6), true), 350); return; } }
      if (!busy) { if (idx > pages.length - 2) idx = pages.length - 2; show(idx); } }).catch(() => {});
  return () => { dead = true; el.removeEventListener(`click`, onTap); ro && ro.disconnect(); };
}
function _PPass(p) {
  const r = (0, _.useRef)(null);
  (0, _.useEffect)(() => { const el = r.current; if (!el) return; return _ppPassMount(el, p); }, [p.u, p.flaps, p.worms, p.rank, p.clan, p.hat]);
  return (0, L.jsxs)(`div`, { style: { padding: p.pad || 0 }, children: [(0, L.jsx)(`div`, { ref: r, className: `ppp` }), p.btn ? (0, L.jsx)(`div`, { style: { marginTop: 14 }, children: p.btn }) : null] });
}
