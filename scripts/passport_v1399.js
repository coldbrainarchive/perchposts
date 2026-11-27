/* ── Passport (v1398, 2026-11-27) ── replaces the Bird ID card everywhere. Opens on the ID page; tap the right side
   to turn to the next page, the left side to go back (on the ID page that closes the cover; tap the cover to open it
   again). Stamp pages hold 6 stamps each and are added as stamps are earned, then one "more to come" page.
   Plain DOM drawn into a React-owned box (_PPass), using the site's own bird kit (_ppKit) for the photo. */
let _ppPassCssOn = false;
// paper fibres, leather grain and uneven stamp ink, each drawn once into a small picture
function _ppTextures() {
  const mk = (w, h, f) => { const c = document.createElement(`canvas`); c.width = w; c.height = h; f(c.getContext(`2d`), w, h); return c.toDataURL(); };
  const rnd = (() => { let a = 1234567; return () => { a = (a * 1103515245 + 12345) & 0x7fffffff; return a / 0x7fffffff; }; })();
  const paper = mk(220, 220, (x, w, h) => { for (let i = 0; i < 2600; i++) { x.fillStyle = `rgba(120,105,90,${.04 + rnd() * .1})`; x.fillRect(rnd() * w, rnd() * h, 1 + rnd() * 1.4, .6 + rnd()); }
    for (let i = 0; i < 90; i++) { x.strokeStyle = `rgba(110,95,80,${.05 + rnd() * .08})`; x.lineWidth = .5; x.beginPath(); const sx = rnd() * w, sy = rnd() * h, a = rnd() * 6.28, l = 3 + rnd() * 9; x.moveTo(sx, sy); x.quadraticCurveTo(sx + Math.cos(a) * l, sy + Math.sin(a) * l * .5, sx + Math.cos(a + .4) * l * 1.6, sy + Math.sin(a + .4) * l); x.stroke(); } });
  const leather = mk(200, 200, (x, w, h) => { for (let i = 0; i < 5200; i++) { const v = rnd(); x.fillStyle = v < .5 ? `rgba(0,0,0,${.08 + rnd() * .14})` : `rgba(170,185,255,${.04 + rnd() * .08})`; const r = .4 + rnd() * 1.3; x.beginPath(); x.arc(rnd() * w, rnd() * h, r, 0, 7); x.fill(); } });
  const ink = mk(160, 160, (x, w, h) => { x.fillStyle = `#000`; x.fillRect(0, 0, w, h); x.globalCompositeOperation = `destination-out`;
    for (let i = 0; i < 26; i++) { const g = x.createRadialGradient(0, 0, 0, 0, 0, 1); const cx = rnd() * w, cy = rnd() * h, r = 10 + rnd() * 30; x.save(); x.translate(cx, cy); x.scale(r, r); g.addColorStop(0, `rgba(0,0,0,${.15 + rnd() * .3})`); g.addColorStop(1, `rgba(0,0,0,0)`); x.fillStyle = g; x.fillRect(-1, -1, 2, 2); x.restore(); }   /* lighter pressure in patches */
    for (let i = 0; i < 1400; i++) { x.fillStyle = `rgba(0,0,0,${.5 + rnd() * .5})`; x.fillRect(rnd() * w, rnd() * h, .6 + rnd() * 1.2, .6 + rnd() * 1.2); } });   /* specks where the ink didn't take */
  return { paper, leather, ink };
}
function _ppPassCss() {
  if (_ppPassCssOn) return; _ppPassCssOn = true;
  const T = _ppTextures();
  const st = document.createElement(`style`);
  st.textContent = `@font-face{font-family:'PP Sig';src:url(/assets/fonts/mrs-saint-delafield.woff2) format('woff2');font-display:block}
.ppp{position:relative;width:100%;max-width:354px;text-align:left;line-height:normal;letter-spacing:normal;font-weight:normal;margin:0 auto;user-select:none;-webkit-user-select:none;-webkit-tap-highlight-color:transparent;cursor:pointer}
.ppp-in{position:absolute;left:0;top:0;width:354px;height:480px;transform-origin:0 0;perspective:1600px}
.ppp .ppp-in,.ppp .ppp-in *{text-align:left!important}
.ppp-spine{position:absolute;left:0;top:0;width:16px;height:480px;border-radius:6px 0 0 6px;background:linear-gradient(90deg,#0a0e2a 0%,#1b2452 45%,#121a44 75%,#090c24 100%);box-shadow:0 18px 40px rgba(0,0,0,.5),inset 0 0 0 1px rgba(255,255,255,.04)}
.ppp-spine::after{content:'';position:absolute;right:3px;top:10px;bottom:10px;width:1px;background:linear-gradient(#b98f39,#ecd17f,#b98f39);opacity:.55}
.ppp-book{position:absolute;left:14px;top:0;width:340px;height:480px;transform-style:preserve-3d}
.ppp-pg{position:absolute;inset:0;transform-origin:0 50%;backface-visibility:hidden;-webkit-backface-visibility:hidden}
.ppp-hint{text-align:center;font-size:11.5px;color:#64748b;margin-top:8px}
.ppp .cover{position:absolute;inset:0;border-radius:0 14px 14px 0;overflow:hidden;background:radial-gradient(130% 100% at 28% 18%,#24305e 0%,#18204a 45%,#10163a 75%,#0b1030 100%);box-shadow:0 18px 40px rgba(0,0,0,.55),inset 0 0 0 1px rgba(255,255,255,.05),inset -6px 0 10px rgba(0,0,0,.35),inset 10px 0 14px rgba(255,255,255,.04)}
.ppp .cover .grain,.ppp .cover .scuff,.ppp .cover .light,.ppp .cover .wear{position:absolute;inset:0}
.ppp .cover .grain{background:url(${T.leather});opacity:.9;mix-blend-mode:overlay}
.ppp .cover .wear{display:none}
.ppp .cover .scuff{background:radial-gradient(18% 9% at 80% 88%,rgba(190,200,255,.10),transparent 70%),radial-gradient(10% 4% at 22% 64%,rgba(190,200,255,.08),transparent 70%),radial-gradient(26% 6% at 50% 97%,rgba(0,0,0,.35),transparent 70%),radial-gradient(9% 9% at 2% 2%,rgba(200,210,255,.12),transparent 70%),radial-gradient(9% 9% at 99% 99%,rgba(200,210,255,.14),transparent 70%)}
.ppp .cover .light{background:linear-gradient(118deg,rgba(255,255,255,.07) 0%,rgba(255,255,255,0) 32%,rgba(0,0,0,0) 60%,rgba(0,0,0,.28) 100%)}
.ppp .gold{background:linear-gradient(175deg,#fbe9ad 0%,#e3c46d 32%,#b98f39 58%,#ecd17f 78%,#a8812e 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 1px 0 rgba(0,0,0,.6)) drop-shadow(0 -0.5px 0 rgba(255,240,200,.25))}
.ppp .cover .t{position:absolute;left:0;right:0;top:44px;text-align:center;font:700 38px 'Times New Roman',Georgia,serif;letter-spacing:.07em}
.ppp .cover .n{position:absolute;left:0;right:0;top:338px;text-align:center;font:italic 700 29px 'Times New Roman',Georgia,serif}
.ppp .cover .emb{position:absolute;left:50%;top:118px;width:190px;height:190px;margin-left:-95px;filter:drop-shadow(0 1.2px 0 rgba(0,0,0,.65)) drop-shadow(0 -0.6px 0 rgba(255,240,200,.25))}
.ppp .cover .chip2{position:absolute;left:50%;top:404px;width:50px;height:32px;margin-left:-25px}
.ppp .page{position:absolute;inset:0;border-radius:0 14px 14px 0;overflow:hidden;background:#f4f0e4;color:#2a2440;box-shadow:0 18px 40px rgba(0,0,0,.5),inset 16px 0 16px -10px rgba(0,0,0,.32)}
.ppp .page .tint{position:absolute;inset:0;background:radial-gradient(90% 70% at 25% 30%,rgba(206,186,236,.45),transparent 70%),radial-gradient(80% 70% at 80% 80%,rgba(168,220,214,.40),transparent 70%),radial-gradient(60% 50% at 85% 15%,rgba(250,214,180,.35),transparent 70%)}
.ppp .page .guil{position:absolute;inset:0}
.ppp .page .fib{position:absolute;inset:0;background:url(${T.paper});opacity:.9;mix-blend-mode:multiply}
.ppp .lbl{font:600 6.8px Helvetica,Arial,sans-serif;letter-spacing:.06em;color:#6f6590;text-transform:uppercase}
.ppp .val{font:700 11px 'Courier New',monospace;color:#1d1830;letter-spacing:.02em;margin:1px 0 7px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ppp .mrz{position:absolute;left:14px;right:10px;bottom:14px;font:700 11.2px 'OCR B','Courier New',monospace;letter-spacing:.04em;color:#1d1830;line-height:1.45;white-space:pre;overflow:hidden}
.ppp .pnum{position:absolute;right:14px;bottom:10px;font:700 10px Georgia,serif;color:#7a6f98}
.ppp .stamp{position:absolute;mix-blend-mode:multiply;-webkit-mask:url(${T.ink}) 0 0/160px 160px;mask:url(${T.ink}) 0 0/160px 160px;opacity:.92}
.ppp .ptitle{position:absolute;left:14px;top:12px;font:800 10px Georgia,serif;letter-spacing:.2em;color:#6f6590}
.ppp-leaf{position:absolute;inset:0;transform-origin:0 50%;transform-style:preserve-3d;-webkit-transform-style:preserve-3d}
.ppp-face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden}
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
function _ppCover() {
  return `<div class="cover"><div class="grain"></div><div class="wear"></div><div class="scuff"></div><div class="t gold">PASSPORT</div>
  <svg class="emb" viewBox="15 9 82 82"><defs><clipPath id="ppp-cf"><circle cx="56" cy="50" r="38"/></clipPath></defs><g fill="none" stroke="url(#ppp-gg)" stroke-width="2" clip-path="url(#ppp-cf)"><line x1="18" y1="50" x2="94" y2="50"/><path d="M 16 30 Q 56 37 96 30"/><path d="M 16 70 Q 56 63 96 70"/><path d="M 56 12 A 9.84 38 0 0 1 56 88"/><path d="M 56 12 A 9.84 38 0 0 0 56 88"/><path d="M 56 12 A 26.87 38 0 0 1 56 88"/><path d="M 56 12 A 26.87 38 0 0 0 56 88"/></g><circle cx="56" cy="50" r="38" fill="none" stroke="url(#ppp-gg)" stroke-width="4.2"/></svg>
  <div class="n gold">Perch Posts</div>
  <svg class="chip2" viewBox="0 0 50 32"><rect x="1" y="1" width="48" height="30" rx="3" fill="none" stroke="url(#ppp-gg)" stroke-width="2.4"/><line x1="1" y1="11" x2="49" y2="11" stroke="url(#ppp-gg)" stroke-width="2.2"/><line x1="1" y1="21" x2="49" y2="21" stroke="url(#ppp-gg)" stroke-width="2.2"/><circle cx="25" cy="16" r="6.5" fill="#141a40" stroke="url(#ppp-gg)" stroke-width="2.4"/></svg>
  <div class="light"></div></div>`;
}
// the ID page
function _ppIdPage(v) {
  const words = String(v.u).split(`-`), given = words.pop().toUpperCase(), sur = words.join(`-`).toUpperCase();   /* one-word names: just a given name */
  const sig = (words.map(w => w[0] ? w[0].toUpperCase() + `.` : ``).join(``) + ` ` + given.charAt(0) + given.slice(1).toLowerCase()).trim();
  const no = v.no ? `PP` + String(v.no).padStart(7, `0`) : `PP·······`;
  const iss = v.issued ? new Date(v.issued) : null, yymmdd = iss && !isNaN(iss) ? String(iss.getFullYear()).slice(2) + String(iss.getMonth() + 1).padStart(2, `0`) + String(iss.getDate()).padStart(2, `0`) : `000000`;
  const m1 = (`P<PPS` + (sur ? sur.replace(/-/g, `<`) + `<<` : ``) + given + `<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<`).slice(0, 38);
  const m2 = (no.replace(/·/g, `0`) + (v.no ? v.no % 10 : 0) + `PPS` + yymmdd + `4B` + String(v.stamps || 0).padStart(4, `0`) + `<<<<<<<<<<<<<<<<<<<<`).slice(0, 36) + String(v.pages || 0).padStart(2, `0`);
  const img = v.img ? _ppEsc(v.img) : ``;
  const cx = 287, cy = 281; let circ = ``; for (let k = 0; k < 30; k++) { const a = k / 30 * Math.PI * 2; circ += `<circle cx="${(cx + Math.cos(a) * 17).toFixed(2)}" cy="${(cy + Math.sin(a) * 17).toFixed(2)}" r="25"/>`; }
  let wave = ``; for (const [R0, A, N] of [[46, 2.4, 36], [50, 1.6, 48]]) { let d = ``; for (let t = 0; t <= Math.PI * 2 + .001; t += .01) { const r = R0 + A * Math.sin(N * t); d += (t ? `L` : `M`) + (cx + Math.cos(t) * r).toFixed(2) + ` ` + (cy + Math.sin(t) * r).toFixed(2); } wave += `<path d="${d}Z"/>`; }
  return `<div class="page">${_ppGuil(260)}
  <div style="position:absolute;left:14px;right:14px;top:14px;display:flex;justify-content:space-between;align-items:flex-start">
    <div><div style="font:800 12px Georgia,serif;letter-spacing:.12em;color:#3b2f6b">PERCH POSTS</div><div class="lbl" style="margin-top:2px">Passport / Passeport / Pasaporte</div></div>
    <svg width="26" height="26" viewBox="15 9 82 82"><circle cx="56" cy="50" r="38" fill="none" stroke="#5b4a9a" stroke-width="5"/><g fill="none" stroke="#5b4a9a" stroke-width="2.4"><line x1="18" y1="50" x2="94" y2="50"/><ellipse cx="56" cy="50" rx="12" ry="38"/><ellipse cx="56" cy="50" rx="26" ry="38"/></g></svg></div>
  <div style="position:absolute;left:14px;top:52px;width:104px;height:132px;border-radius:4px;background:linear-gradient(#dcd8e6,#c9c4d8);overflow:hidden;box-shadow:inset 0 0 0 1px rgba(0,0,0,.12)">${img ? `<img src="${img}" alt="" style="position:absolute;left:${v.hat ? 12 : -30}px;top:${v.hat ? 30 : -6}px;width:${v.hat ? 80 : 164}px;height:${v.hat ? 80 : 164}px;object-fit:contain">` : ``}</div>
  <svg style="position:absolute;left:0;top:0;width:340px;height:480px;pointer-events:none" viewBox="0 0 340 480"><g fill="none" stroke="url(#ppp-holo)" stroke-width=".45" opacity=".55">${circ}</g><g fill="none" stroke="url(#ppp-holo)" stroke-width=".5" opacity=".6">${wave}</g></svg>
  ${img ? `<img src="${img}" alt="" style="position:absolute;left:${v.hat ? 254 : 232}px;top:${v.hat ? 248 : 226}px;width:${v.hat ? 66 : 110}px;height:${v.hat ? 66 : 110}px;object-fit:contain;opacity:.22;filter:grayscale(1) contrast(1.3)">
    <div style="position:absolute;left:${v.hat ? 254 : 232}px;top:${v.hat ? 248 : 226}px;width:${v.hat ? 66 : 110}px;height:${v.hat ? 66 : 110}px;-webkit-mask:url('${img}') center/contain no-repeat;mask:url('${img}') center/contain no-repeat;background:linear-gradient(120deg,#ff6fd2 0%,#5fb8ff 28%,#5ff2b0 50%,#ffd85f 72%,#b47bff 100%);opacity:.55"></div>
    <div style="position:absolute;left:${v.hat ? 254 : 232}px;top:${v.hat ? 248 : 226}px;width:${v.hat ? 66 : 110}px;height:${v.hat ? 66 : 110}px;-webkit-mask:url('${img}') center/contain no-repeat;mask:url('${img}') center/contain no-repeat;background:linear-gradient(120deg,transparent 32%,rgba(255,255,255,.95) 46%,transparent 60%);opacity:.7"></div>` : ``}
  <div style="position:absolute;left:130px;top:50px;right:12px">
   <div style="display:flex;gap:14px"><div><div class="lbl">Type</div><div class="val">P</div></div><div><div class="lbl">Code</div><div class="val">PPS</div></div><div><div class="lbl">Passport No.</div><div class="val">${no}</div></div></div>
   <div class="lbl">Surname / Nom</div><div class="val">${_ppEsc(sur || `—`)}</div>
   <div class="lbl">Given names / Prénoms</div><div class="val">${_ppEsc(given)}</div>
   <div style="display:flex;gap:18px"><div><div class="lbl">Nationality</div><div class="val">${_ppEsc((v.clan || `—`).toUpperCase())}</div></div><div style="min-width:0"><div class="lbl">Plumage</div><div class="val" data-plum>${_ppEsc(v.plum || `—`)}</div></div></div>
   <div class="lbl">Rank</div><div class="val">${_ppEsc((v.rank || `—`).toUpperCase())}</div>
   <div class="lbl">Date of issue</div><div class="val">${v.issued ? _ppDate(v.issued) : `—`}</div></div>
  <div style="position:absolute;left:14px;top:196px;width:110px"><div class="lbl">Signature</div><div style="position:relative;height:40px;margin-top:-2px"><div style="position:absolute;left:-2px;top:-6px;font:400 32px 'PP Sig',cursive;color:#23236b;transform:rotate(-7deg);white-space:nowrap;letter-spacing:-.5px">${_ppEsc(sig)}</div>
   <svg width="118" height="40" style="position:absolute;left:-6px;top:2px;overflow:visible"><path d="M8 33 C 34 27, 58 31, 80 25 S 108 17, 114 21 C 106 27, 90 31, 74 33" fill="none" stroke="#23236b" stroke-width="1.15" stroke-linecap="round" opacity=".85"/></svg></div></div>
  <div style="position:absolute;left:14px;right:14px;top:248px;height:1px;background:rgba(80,60,140,.25)"></div>
  <div style="position:absolute;left:14px;top:262px;width:210px;display:grid;grid-template-columns:1fr 1fr;column-gap:14px"><div><div class="lbl">Flaps</div><div class="val">${_ppEsc(v.flaps ?? 0)}</div></div><div><div class="lbl">Worms</div><div class="val">${_ppEsc(v.worms ?? 0)}</div></div><div><div class="lbl">Stamps</div><div class="val">${v.stamps ?? `—`}</div></div><div><div class="lbl">Pages</div><div class="val">${v.pages ?? `—`}</div></div></div>
  <div class="mrz">${_ppEsc(m1)}
${_ppEsc(m2)}</div></div>`;
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
  oct: (c, icon, big, sm, date) => ({ w: 120, h: 120, svg: `<svg viewBox="-60 -60 120 120" width="120" height="120"><g fill="none" stroke="${c}" stroke-width="3"><polygon points="-24,-56 24,-56 56,-24 56,24 24,56 -24,56 -56,24 -56,-24"/></g>
    <g fill="${c}" font-family="Helvetica,Arial,sans-serif" font-weight="900" text-anchor="middle"><text y="-18" font-size="13">${icon}</text><text y="-2" font-size="${big.length > 9 ? 10 : 12}" letter-spacing="1.4">${_ppT(big, 12)}</text><text y="13" font-size="7.5" letter-spacing="1.6">${_ppT(sm, 18)}</text><text y="28" font-size="8.5">${_ppT(date)}</text></g></svg>` }),
};
const _ppTagInk = { General: `#475569`, Sports: `#15805a`, Science: `#0e7490`, Nature: `#4d7c0f`, Entertainment: `#be185d`, Random: `#c2410c`, Announcements: `#1e3a8a` };
function _ppStamp(s) {
  const S = _ppStampShapes, d = _ppDate(s.at), t = String(s.k).split(`:`), x = s.d || {};
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
function _ppStampPage(list, n) {
  let h = ``;
  list.forEach((s, i) => { const st = _ppStamp(s), hs = _ppHash(s.k), rot = (hs % 29) - 14, [cx, cy] = _ppSlots[i], jx = (hs >> 5) % 11 - 5, jy = (hs >> 9) % 11 - 5;
    h += `<div class="stamp" style="left:${cx - st.w / 2 + jx}px;top:${cy - st.h / 2 + jy}px;width:${st.w}px;height:${st.h}px;transform:rotate(${rot}deg)">${st.svg}</div>`; });
  return `<div class="page">${_ppGuil(180 + n * 20)}<div class="ptitle">VISAS · STAMPS</div>${h}<div class="pnum">${n + 1}</div></div>`;
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
  const build = () => { const st = data ? data.stamps : [], out = [_ppCover(), ``];
    for (let i = 0; i < st.length; i += 6) out.push(_ppStampPage(st.slice(i, i + 6), out.length - 1));
    pages = out; pages[1] = _ppIdPage(view()); };
  el.innerHTML = `<div class="ppp-in"><div class="ppp-spine"></div><div class="ppp-book"></div></div>`; const box = el.querySelector(`.ppp-book`), inner = el.firstChild;
  const fit = () => { const w = Math.min(354, el.clientWidth || 354), k = w / 354; inner.style.transform = `scale(${k})`; el.style.height = 480 * k + `px`; };
  const show = i => { box.innerHTML = ``; const pg = document.createElement(`div`); pg.className = `ppp-pg`; pg.innerHTML = pages[i + 1]; box.appendChild(pg); };
  // turning a page: the sheet lifts from its left edge and swings over (you see its plain back as it goes), the page
  // underneath is in its shadow until the sheet clears it. Back is the same in reverse.
  const turn = (to, fwd) => { if (busy || to < -1 || to > pages.length - 2) return;
    busy = true; const top = fwd ? idx : to, bottom = fwd ? to : idx;
    const under = document.createElement(`div`); under.className = `ppp-pg`; under.innerHTML = pages[bottom + 1];
    const shade = document.createElement(`div`); shade.className = `ppp-shade`; under.appendChild(shade);
    const leaf = document.createElement(`div`); leaf.className = `ppp-leaf`;
    leaf.innerHTML = `<div class="ppp-face">${pages[top + 1]}</div><div class="ppp-face ppp-back">${top === -1 ? `<div class="lining"></div>` : `<div class="page"><div class="tint"></div><div class="fib"></div></div>`}</div>`;
    box.innerHTML = ``; box.appendChild(under); box.appendChild(leaf);
    const ease = `cubic-bezier(.42,.0,.25,1)`, ms = 720;
    leaf.animate(fwd ? [{ transform: `rotateY(0deg)` }, { transform: `rotateY(-180deg)` }] : [{ transform: `rotateY(-180deg)` }, { transform: `rotateY(0deg)` }], { duration: ms, easing: ease, fill: `forwards` });
    const sh = shade.animate(fwd ? [{ opacity: .9 }, { opacity: 0 }] : [{ opacity: 0 }, { opacity: .9 }], { duration: ms, easing: ease, fill: `forwards` });
    sh.onfinish = () => { if (dead) return; idx = to; show(idx); busy = false; }; };
  const wiggle = () => { const pg = box.firstChild; if (pg && pg.animate) pg.animate([{ transform: `rotate(0)` }, { transform: `rotate(-1.4deg)` }, { transform: `rotate(1deg)` }, { transform: `rotate(0)` }], { duration: 320 }); };
  const onTap = e => { if (busy) return; const r = el.getBoundingClientRect(), right = e.clientX - r.left > r.width / 2;
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
