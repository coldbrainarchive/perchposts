// Sign-up nest: 5 eggs from the server (/nest), crack one with 3 taps to meet its bird; the hatching tap picks it.
// Fresh eggs only every 15 minutes (the server decides). Wrapped into the bundle by scripts/patch_v1083.py.
//   _ppNest(el, api, onPick) builds the nest inside el and returns a cleanup function.
//   _ppNestDev() is this browser's nest id, sent with /register (sign-up only accepts a name from its own nest).
//   _ppNestDone() forgets the nest after a sign-up.
const _ppNestCss = `
.ppn{display:flex;flex-direction:column;align-items:center;width:100%}
.ppn-wrap{position:relative;width:320px;height:222px;margin:-8px 0 4px;touch-action:manipulation;-webkit-user-select:none;user-select:none}
.ppn-wrap svg.ppn-l{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
.ppn .egg{position:absolute;width:60px;height:77px;transform-origin:50% 85%;cursor:pointer;-webkit-tap-highlight-color:transparent;border:0;padding:0;background:none}
.ppn .egg:focus-visible{outline:2px solid #c084fc;outline-offset:4px;border-radius:40%}
.ppn .egg svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none}
.ppn .shell-top{z-index:3;transition:transform .6s cubic-bezier(.3,.7,.4,1),opacity .6s}
.ppn .shell-bot{z-index:2}
.ppn .egg:not(.hatched) .shell-bot .half,.ppn .egg.hatched .shell-bot .whole{display:none}
.ppn .bird{position:absolute;z-index:1;pointer-events:none;left:50%;top:24px;width:113px;height:113px;margin:-56.5px 0 0 -56.5px;transform:scale(.2) translateY(36px);opacity:0}
.ppn .bird .face{position:relative;width:100%;height:100%;scale:var(--dir,1) 1;transition:scale .22s ease-in-out,filter .25s;transform-origin:50% 70%}
.ppn .bird .face img{width:100%;height:100%;display:block}
.ppn .bird .face img:not(.ok){visibility:hidden}   /* no empty picture frame while the bird is still being drawn */
.ppn .lid{position:absolute;border-radius:50%;transform:scaleY(0);transform-origin:50% 0;box-shadow:inset 0 -1.2px 0 rgba(0,0,0,.35),0 0 1.5px 1px transparent;opacity:0}
.ppn .lid.on{opacity:1}.ppn .lid.blink{animation:ppn-blink .17s ease-in-out}
.ppn .egg.hatched .shell-top{transform:translate(var(--fx),-60px) rotate(var(--fr));opacity:0}
.ppn .egg.hatched .bird{animation:ppn-pop .7s cubic-bezier(.3,1.6,.5,1) forwards}
.ppn .egg.sel .bird .face{filter:drop-shadow(0 0 6px var(--glow)) drop-shadow(0 0 2px var(--glow))}
.ppn .egg.wob{animation:ppn-wob .6s ease-in-out}
.ppn .egg.hit{animation:ppn-hit .35s ease-in-out}
.ppn .face.bob{animation:ppn-bob .45s ease-in-out}
.ppn .face.tilt{animation:ppn-tilt .7s ease-in-out}
.ppn .face.peek{animation:ppn-peek .8s ease-in-out}
@keyframes ppn-drop{0%{translate:0 var(--dy);animation-timing-function:cubic-bezier(.55,0,1,.45)}52%{translate:0 0;animation-timing-function:cubic-bezier(0,.55,.45,1)}68%{translate:0 -24px;animation-timing-function:cubic-bezier(.55,0,1,.45)}80%{translate:0 0;animation-timing-function:cubic-bezier(0,.55,.45,1)}90%{translate:0 -8px;animation-timing-function:cubic-bezier(.55,0,1,.45)}100%{translate:0 0}}
.ppn .egg.drop{animation:ppn-drop 1s both;pointer-events:none}
@media (prefers-reduced-motion:reduce){.ppn .egg.drop{animation:none}}
@keyframes ppn-roll{0%{translate:0 0;rotate:0deg;opacity:1;animation-timing-function:cubic-bezier(.3,0,.6,1)}22%{translate:calc(var(--rx) * .18) -16px;rotate:calc(var(--rr) * .15);animation-timing-function:cubic-bezier(.4,0,.9,.6)}80%{opacity:1}100%{translate:var(--rx) 120px;rotate:var(--rr);opacity:0}}
.ppn .egg.roll{animation:ppn-roll 1.1s both;pointer-events:none;z-index:950!important}
@media (prefers-reduced-motion:reduce){.ppn .egg.roll{animation:none;opacity:0}}
@keyframes ppn-blink{0%,100%{transform:scaleY(0)}45%,60%{transform:scaleY(1)}}
@keyframes ppn-wob{0%,100%{rotate:0deg}20%{rotate:-7deg}45%{rotate:6deg}70%{rotate:-3deg}85%{rotate:2deg}}
@keyframes ppn-hit{0%,100%{rotate:0deg;translate:0 0}25%{rotate:-9deg;translate:-1px 0}55%{rotate:8deg;translate:1px -2px}80%{rotate:-3deg}}
@keyframes ppn-pop{0%{transform:scale(.2) translateY(36px);opacity:0}35%{opacity:1}100%{transform:scale(1) translateY(0);opacity:1}}
@keyframes ppn-bob{0%,100%{translate:0 0}40%{translate:0 -5px}70%{translate:0 1px}}
@keyframes ppn-tilt{0%,100%{rotate:0deg}30%{rotate:-12deg}65%{rotate:9deg}}
@keyframes ppn-peek{0%,100%{translate:0 0}35%,65%{translate:0 6px}}
.ppn .crack{fill:none;stroke:#3a2a1c;stroke-width:1.4;stroke-linecap:round;stroke-linejoin:round;opacity:0;transition:opacity .15s}
.ppn-hint{min-height:18px;font-size:13.5px;font-weight:600;color:#94a3b8;text-align:center;margin:0 0 10px}
.ppn-hint b{color:#e2e8f0}
.ppn-tag{width:100%;box-sizing:border-box;min-height:58px;border-radius:12px;display:flex;align-items:center;gap:12px;padding:8px 14px;transition:background .35s,border-color .35s;border:1.5px solid transparent}
.ppn-tag.empty{border:1.5px dashed #3f4756;justify-content:center;color:#64748b;font-size:14px;font-weight:600}
.ppn-tag .tf{width:40px;height:40px;flex-shrink:0;display:flex;align-items:center;justify-content:center}
.ppn-tag .tf img{width:85px;height:85px;margin:-22.5px;display:block;max-width:none}
.ppn-tag .nm{flex:1;text-align:center;font-size:16px;font-weight:700;color:#0a0a0a;word-break:break-word;padding-right:40px}
.ppn.ppn-empty .ppn-wrap{cursor:pointer;-webkit-tap-highlight-color:transparent;touch-action:manipulation}.ppn-fresh{margin:4px auto 12px;background:#2a2116;color:#fde68a;border:1.5px solid #6b4f1d;border-radius:999px;padding:12px 26px;font-size:15px;font-weight:800;cursor:pointer;display:none;touch-action:manipulation}.ppn-fresh:disabled{opacity:.6;cursor:default}
@media (prefers-reduced-motion:reduce){.ppn .egg.wob,.ppn .egg.hit,.ppn .face.bob,.ppn .face.tilt,.ppn .face.peek,.ppn .lid.blink{animation:none}.ppn .egg.hatched .bird{animation:none;transform:none;opacity:1}.ppn .shell-top{transition:opacity .2s}}`;

let _ppNestMem = null;
function _ppNestDev() {
  try { let d = localStorage.getItem("pp_nest_dev"); if (!/^[0-9a-f]{32}$/.test(d || "")) { d = _ppNewDev(); localStorage.setItem("pp_nest_dev", d); } return d; }
  catch (e) { return _ppNestMem || (_ppNestMem = _ppNewDev()); }
}
function _ppNewDev() { const a = new Uint8Array(16); crypto.getRandomValues(a); return Array.from(a, b => b.toString(16).padStart(2, "0")).join(""); }
function _ppNestDone() { try { localStorage.removeItem("pp_nest"); localStorage.removeItem("pp_nest_dev"); } catch (e) {} _ppNestMem = null; }

// Egg looks: each name gets its own egg (same name -> same egg everywhere), patterns from real eggs:
// plain, fine speckles, big blotches, a ring of spots round the wide end, scribbles, or blotches + speckles.
// Markings are mostly a darker shade of the bird's colour, sometimes dark brown/black; name words give hints.
const _ppEggs = (() => {
const rngE = s => () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296;
const hashE = n => { let h = 0; for (let i = 0; i < n.length; i++) h = n.charCodeAt(i) + ((h << 5) - h); return Math.abs(h); };
const f1e = v => v.toFixed(1);
const PATTERNS = ["plain", "fine", "blotch", "ring", "scribble", "mixed"];
const PW = { plain: 1, fine: 2, blotch: 2, ring: 1.5, scribble: 1.2, mixed: 1.5 };
// which pattern a name gets: hints from its words first, otherwise a weighted pick from its hash
function eggPattern(name) {
  const w = name.split("-"), r = rngE(hashE(name + "#egg"));
  if (/^(spotted|speckled)$/.test(w[1]) || /^(spotted|speckled)$/.test(w[0])) return r() < .5 ? "fine" : "mixed";
  if (/^(streaked|striped|barred|banded)$/.test(w[1]) || /^(streaked|striped|barred|banded)$/.test(w[0])) return "scribble";
  if (/^(black|sooty|dark|dusky|slaty)$/.test(w[0])) return r() < .6 ? "fine" : "mixed";     // dark names: dark speckles, never plain
  const tot = PATTERNS.reduce((a, k) => a + PW[k], 0); let v = r() * tot;
  for (const k of PATTERNS) { v -= PW[k]; if (v <= 0) return k; } return "fine";
}
// a whole nest: no two eggs with the same pattern if it can be helped
function nestPatterns(names) { const used = new Set(); return names.map(n => { let p = eggPattern(n);
  if (used.has(p)) { const r = rngE(hashE(n + "#alt")), free = PATTERNS.filter(k => !used.has(k)); p = free[Math.floor(r() * free.length)] || p; }
  used.add(p); return p; }); }
// markings: mostly a darker shade of the bird's colour; some eggs get dark brown/black speckles ("black", "sooty" names always do)
function eggInk(name, h) { const r = rngE(hashE(name + "#ink")), w = name.split("-");
  const dark = /^(black|sooty|dark|dusky|slaty)$/.test(w[0]) || r() < .28;
  return dark ? (r() < .5 ? "hsl(25,28%,16%)" : "hsl(20,12%,9%)") : `hsl(${h},${Math.round(42 + r() * 18)}%,${Math.round(30 + r() * 14)}%)`; }
function eggMarks(name, h, pattern) {
  const r = rngE(hashE(name + "#marks")), ink = eggInk(name, h); let s = "";
  const dot = (x, y, rx, ry, op, rot) => `<ellipse cx="${f1e(x)}" cy="${f1e(y)}" rx="${f1e(rx)}" ry="${f1e(ry)}" transform="rotate(${Math.round(rot || 0)} ${f1e(x)} ${f1e(y)})" fill="${ink}" fill-opacity="${op.toFixed(2)}"/>`;
  const anywhere = () => [5 + r() * 40, 6 + r() * 54];
  const lower = () => { const y = 30 + Math.pow(r(), .7) * 30; return [6 + r() * 38, y]; };   // more toward the wide end
  if (pattern === "fine" || pattern === "mixed") { const n = pattern === "fine" ? 55 + r() * 35 : 30 + r() * 15;
    for (let k = 0; k < n; k++) { const [x, y] = r() < .6 ? lower() : anywhere(), d = .35 + r() * .75; s += dot(x, y, d, d * (.7 + r() * .5), .55 + r() * .4, r() * 180); } }
  if (pattern === "blotch" || pattern === "mixed") { const n = pattern === "blotch" ? 4 + r() * 4 : 2 + r() * 2;
    let b = ""; for (let k = 0; k < n; k++) { const [x, y] = anywhere(), d = 2.5 + r() * 4; b += dot(x, y, d, d * (.6 + r() * .5), .55 + r() * .3, r() * 180); }
    s += `<g filter="url(#ppn-eb)">${b}</g>`; }
  if (pattern === "ring") { for (let k = 0; k < 38 + r() * 20; k++) { const a = r() * 6.283, y = 41 + Math.sin(a) * 4 + (r() - .5) * 5, x = 25 + Math.cos(a) * 22 * (r() * .4 + .6), d = .5 + r() * 1.6;
      s += dot(x, y, d, d * (.6 + r() * .5), .5 + r() * .45, r() * 180); }
    for (let k = 0; k < 8; k++) { const [x, y] = anywhere(), d = .4 + r() * .5; s += dot(x, y, d, d, .5, 0); } }
  if (pattern === "scribble") { for (let k = 0; k < 5 + r() * 4; k++) { let [x, y] = anywhere(), p = `M${f1e(x)} ${f1e(y)}`;
      for (let j = 0; j < 3; j++) { const nx = x + (r() - .5) * 14, ny = y + (r() - .5) * 8; p += ` Q${f1e((x + nx) / 2 + (r() - .5) * 8)} ${f1e((y + ny) / 2 + (r() - .5) * 8)} ${f1e(nx)} ${f1e(ny)}`; x = nx; y = ny; }
      s += `<path d="${p}" fill="none" stroke="${ink}" stroke-width="${f1e(.6 + r() * .7)}" stroke-linecap="round" stroke-opacity="${(.6 + r() * .35).toFixed(2)}"/>`; }
    for (let k = 0; k < 10; k++) { const [x, y] = anywhere(), d = .4 + r() * .6; s += dot(x, y, d, d, .6, 0); } }
  return s;
}
return { nestPatterns, eggMarks };
})();

function _ppNest(root, api, onPick) {
  if (!document.getElementById("ppn-css")) { const st = document.createElement("style"); st.id = "ppn-css"; st.textContent = _ppNestCss; document.head.appendChild(st); }
  const NS = "http://www.w3.org/2000/svg", rng = s => () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296;
  const hashStr = n => { let h = 0; for (let i = 0; i < n.length; i++) h = n.charCodeAt(i) + ((h << 5) - h); return Math.abs(h); };
  const clanOf = n => ["🐤", "🐦", "🐧"][hashStr(n) % 3];
  const hueOf = n => +(_ppKit.tagCol(n).match(/hsl\((\d+)/) || [0, 0])[1];
  const f1 = v => v.toFixed(1);
  let alive = true; const timers = new Set();
  const later = (f, ms) => { const t = setTimeout(() => { timers.delete(t); if (alive) f(); }, ms); timers.add(t); };

  root.className = "ppn";
  root.innerHTML = `<div class=ppn-wrap><svg class=ppn-l viewBox="0 0 320 222"></svg><div></div><svg class=ppn-l viewBox="0 0 320 222" style="z-index:900"></svg></div>
    <button type=button class=ppn-fresh>Tap to get your eggs</button><div class=ppn-hint></div><div class="ppn-tag empty">Crack an egg to meet your bird</div>`;
  const [back, box, front] = root.querySelector(".ppn-wrap").children, freshBtn = root.querySelector(".ppn-fresh"),
    hint = root.querySelector(".ppn-hint"), tag = root.querySelector(".ppn-tag");

  // ---------- the nest: woven all the way through, no bare floor ----------
  const K = .88, CX = 160, CY = 132, RX = 152 * K, RY = 94 * K, BX = CX, BY = CY - 6, BRX = RX * .7, BRY = RY * .62;
  const RIM = ["#5a3a1e", "#6b4423", "#7a5230", "#8b5e34", "#a0703f", "#b98a52", "#4a2f17", "#c49a63"];
  const INNER = ["#4a2f17", "#5a3a1e", "#6b4423", "#7a5230", "#8b5e34", "#9a6a3a"];
  function strand(x, y, dx, dy, len, bend, w, col, hi) {
    const x0 = x - dx * len / 2, y0 = y - dy * len / 2, x1 = x + dx * len / 2, y1 = y + dy * len / 2, mx = x - dy * bend, my = y + dx * bend;
    let s = `<path d="M${f1(x0)} ${f1(y0)} Q${f1(mx)} ${f1(my)} ${f1(x1)} ${f1(y1)}" stroke="${col}" stroke-width="${f1(w)}" stroke-linecap="round" fill="none"/>`;
    if (hi) s += `<path d="M${f1(x0)} ${f1(y0 - w * .3)} Q${f1(mx)} ${f1(my - w * .3)} ${f1(x1)} ${f1(y1 - w * .3)}" stroke="#e2bd85" stroke-opacity=".32" stroke-width="${f1(w * .35)}" stroke-linecap="round" fill="none"/>`;
    return s;
  }
  function ring(r, n, cx, cy, rx, ry, t0, t1, pal, keep, wmin, wmax, lmin, lmax) {
    let s = "";
    for (let i = 0; i < n; i++) {
      const a = r() * Math.PI * 2, t = t0 + r() * (t1 - t0); if (keep && !keep(a, t)) continue;
      const x = cx + rx * t * Math.cos(a), y = cy + ry * t * Math.sin(a);
      let dx = -rx * Math.sin(a), dy = ry * Math.cos(a); const L = Math.hypot(dx, dy) || 1; dx /= L; dy /= L;
      const tilt = (r() - .5) * 1.1, c = Math.cos(tilt), sn = Math.sin(tilt); [dx, dy] = [dx * c - dy * sn, dx * sn + dy * c];
      s += strand(x, y, dx, dy, lmin + r() * (lmax - lmin), (r() - .5) * 14, wmin + r() * (wmax - wmin), pal[Math.floor(r() * pal.length)], r() < .3);
    }
    return s;
  }
  back.innerHTML = `<defs><filter id=ppn-eb x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation=".45"/></filter>
    <radialGradient id=ppn-shade cx=50% cy=50% r=50%><stop offset=0 stop-color="#000" stop-opacity=".55"/><stop offset=1 stop-color="#000" stop-opacity="0"/></radialGradient>
    <radialGradient id=ppn-depth cx=50% cy=62% r=58%><stop offset=0 stop-color="#000" stop-opacity="0"/><stop offset=.75 stop-color="#000" stop-opacity=".18"/><stop offset=1 stop-color="#000" stop-opacity=".42"/></radialGradient>
    <linearGradient id=ppn-wall x1=0 y1=0 x2=0 y2=1><stop offset=0 stop-color="#000" stop-opacity=".38"/><stop offset=.45 stop-color="#000" stop-opacity="0"/></linearGradient></defs>
    <ellipse cx="${CX}" cy="${CY + 12}" rx="${RX + 6}" ry="${RY * .62}" fill="url(#ppn-shade)"/>
    <ellipse cx="${CX}" cy="${CY}" rx="${RX * .98}" ry="${RY * .98}" fill="#5e3f21"/>
    <ellipse cx="${BX}" cy="${BY}" rx="${BRX}" ry="${BRY}" fill="#6b4626"/>` +
    ring(rng(41), 330, BX, BY, BRX, BRY, 0, 1.02, INNER, null, 1.3, 2.6, 14, 34) +
    ring(rng(42), 140, BX, BY, BRX, BRY, 0, .8, ["#8b5e34", "#a0703f", "#b98a52"], null, 1, 1.8, 10, 24) +
    `<ellipse cx="${BX}" cy="${BY}" rx="${BRX * 1.02}" ry="${BRY * 1.02}" fill="url(#ppn-depth)"/><ellipse cx="${BX}" cy="${BY}" rx="${BRX}" ry="${BRY}" fill="url(#ppn-wall)"/>` +
    ring(rng(7), 440, CX, CY, RX, RY, .62, 1.02, RIM, null, 1.6, 4.2, 26 * K, 72 * K);
  front.innerHTML = ring(rng(31), 300, CX, CY, RX, RY, .7, 1.02, RIM, a => Math.sin(a) > .25, 1.6, 4.2, 26 * K, 72 * K);

  // ---------- eggs ----------
  const SPOTS = [[99, 96], [160, 90], [221, 96], [129, 136], [191, 136]];
  const EGG = "M25 2 C40 2 48 26 48 40 C48 54 38 62 25 62 C12 62 2 54 2 40 C2 26 10 2 25 2Z";
  function crackFor(i, name) {
    const r = rng(hashStr(name) + i * 7919), n = 5 + Math.floor(r() * 4), amp = 2.5 + r() * 3.5, cy = 29 + r() * 7, tilt = (r() - .5) * 12;
    const zig = []; for (let k = 0; k <= n; k++) { const x = k * 50 / n; zig.push([x, cy + tilt * (x / 50 - .5) + (k % 2 ? -amp : amp) * (.6 + r() * .6)]); }
    const P = pts => pts.map((p, k) => (k ? "L" : "M") + f1(p[0]) + " " + f1(p[1])).join(" ");
    const k0 = 1 + Math.floor(r() * (n - 2)), part = zig.slice(Math.max(0, k0 - 1), k0 + 2);
    const m = zig[k0], fork = (p, up) => `M${f1(p[0])} ${f1(p[1])} l${f1((r() - .5) * 7)} ${f1((up ? -1 : 1) * (3 + r() * 4))}`;
    const first = P(part) + " " + fork(m, r() < .5);
    const second = P(zig) + " " + fork(zig[1 + Math.floor(r() * (n - 1))], true) + " " + fork(zig[1 + Math.floor(r() * (n - 1))], false);
    const fx = Math.round((r() - .5) * 52), fr = Math.round((fx >= 0 ? 1 : -1) * (25 + r() * 30));
    return { zig, first, second, fx, fr };
  }
  function eggSVG(i, name, part, ck, pattern) {
    const h = hueOf(name), sp = _ppEggs.eggMarks(name, h, pattern);   // same markings on both halves (seeded by the name)
    const clipPts = part === "top" ? [[0, -10], [50, -10], ...ck.zig.slice().reverse()] : [...ck.zig, [50, 80], [0, 80]];
    const id = `ppn${i}${part}`;
    return `<svg class="shell-${part}" viewBox="0 0 50 64"><defs><clipPath id="${id}"><polygon points="${clipPts.map(p => f1(p[0]) + "," + f1(p[1])).join(" ")}"/></clipPath>
      <radialGradient id="g${id}" cx="36%" cy="30%" r="75%"><stop offset="0" stop-color="hsl(${h},40%,97%)"/><stop offset=".55" stop-color="hsl(${h},32%,88%)"/><stop offset="1" stop-color="hsl(${h},24%,68%)"/></radialGradient>
      <clipPath id="e${id}"><path d="${EGG}"/></clipPath></defs>
      ${part === "bot" ? `<g class=whole><path d="${EGG}" fill="url(#g${id})"/><g clip-path="url(#e${id})">${sp}</g></g>` : ""}
      <g clip-path="url(#${id})" class="${part === "bot" ? "half" : ""}"><path d="${EGG}" fill="url(#g${id})"/><g clip-path="url(#e${id})">${sp}</g></g>
      ${part === "top" ? `<g clip-path="url(#e${id})"><path class="crack c1" d="${ck.first}"/><path class="crack c2" d="${ck.second}"/></g>` : ""}</svg>`;
  }
  // the straws between the eggs are always there (empty nest too), so eggs drop in between them instead of straws popping in
  function weaves() {
    if (box.querySelector(".ppn-weave")) return;
    SPOTS.forEach(([x, y], i) => { const w = document.createElementNS(NS, "svg"); w.setAttribute("class", "ppn-l ppn-weave"); w.setAttribute("viewBox", "0 0 320 222");
      w.style.zIndex = 2 * Math.round(y) + 1; w.innerHTML = weaveFor(i, x, y); box.appendChild(w); });
  }
  function weaveFor(i, x, y) {
    const r = rng(500 + i * 31); let s = "";
    for (let k = 0; k < 5; k++) {
      const yy = y + 20 + r() * 16, xx = x + (r() - .5) * 26, a = (r() - .5) * .5;
      s += strand(xx, yy, Math.cos(a), Math.sin(a), 30 + r() * 28, 3 + r() * 5, 1.4 + r() * 1.6, RIM[Math.floor(r() * RIM.length)], r() < .45);
    }
    return s;
  }

  // ---------- state: names and the clock come from the server; taps and the pick are kept in this browser ----------
  let nest = null, eggs = [], dropNext = false, busy = false, leaving = false;   // a nest starts empty: tap for eggs; after 15 minutes the eggs go (names released) and it's empty again
  const dirs = [], unsubs = [];
  const save = () => { try { localStorage.setItem("pp_nest", JSON.stringify(nest)); } catch (e) {} };
  const loadLocal = () => { try { return JSON.parse(localStorage.getItem("pp_nest")); } catch (e) { return null; } };
  function pick(i) { nest.sel = i; onPick(i == null ? "" : nest.names[i]); }
  // an empty nest: just the button (and why, if it timed out)
  function empty(msg) {
    unsubs.splice(0).forEach(u => u()); box.querySelectorAll(".egg").forEach(e => e.remove()); eggs = []; nest = null; weaves();
    try { localStorage.removeItem("pp_nest"); } catch (e) {}
    onPick(""); tag.className = "ppn-tag empty"; tag.style.background = ""; tag.style.borderColor = ""; tag.textContent = "Your bird will appear here";
    busy = false; root.classList.add("ppn-empty"); freshBtn.style.display = "none"; hint.style.display = ""; hint.textContent = msg || "Tap nest to get your eggs";
  }
  // peek: only look for a nest that's still running (page load); otherwise lay new eggs
  function get(fresh, peek) {
    if (fresh) { busy = true; hint.style.display = ""; hint.textContent = "Laying your eggs…"; }
    fetch(`${api}/nest`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ device: _ppNestDev(), fresh: !!fresh, peek: !!peek }) })
      .then(r => r.json().then(j => { if (!r.ok || (!Array.isArray(j.names) && j.names !== null)) throw new Error(j.error || "nest"); return j; }))
      .then(j => {
        if (!alive) return;
        if (!j.names) return empty("");
        if (j.left_ms <= 0) return empty("Lots of new birds on this network right now. Try again in a few minutes.");
        const old = loadLocal(), same = old && Array.isArray(old.names) && old.names.join() === j.names.join();
        nest = same ? old : { names: j.names, taps: j.names.map(() => 0), sel: null };
        nest.until = Date.now() + j.left_ms; save(); busy = false; root.classList.remove("ppn-empty"); freshBtn.style.display = "none"; hint.style.display = ""; dropNext = !!fresh && !same;
        _ppKit.ready.then(() => { if (alive) render(); });
      })
      .catch(() => { if (!alive) return; busy = false; hint.style.display = ""; hint.innerHTML = `Couldn't get your eggs. <b style="cursor:pointer;text-decoration:underline">Try again</b>`; hint.querySelector("b").onclick = () => get(fresh, peek); });
  }
  function render() {
    unsubs.splice(0).forEach(u => u()); box.querySelectorAll(".egg").forEach(e => e.remove()); eggs = []; weaves();
    const pats = _ppEggs.nestPatterns(nest.names);   // no two eggs in a nest with the same pattern
    nest.names.forEach((name, i) => {
      const [x, y] = SPOTS[i], clan = clanOf(name), b = document.createElement("button"), ck = crackFor(i, name), z = 2 * Math.round(y);
      // the outer birds face the middle of the nest (left ones look right, right ones look left); the middle one by its name
      dirs[i] = i === 0 || i === 3 ? -1 : i === 2 || i === 4 ? 1 : hashStr(name + "dir") % 2 ? -1 : 1;
      b.type = "button"; b.className = "egg"; b.style.left = (x - 30) + "px"; b.style.top = (y - 38) + "px"; b.style.zIndex = z;
      b.style.transform = `rotate(${[-8, 4, 10, -5, 7][i]}deg)`;
      b.style.setProperty("--glow", _ppKit.tagCol(name)); b.style.setProperty("--fx", ck.fx + "px"); b.style.setProperty("--fr", ck.fr + "deg");
      b.setAttribute("aria-label", "Egg " + (i + 1));
      b.innerHTML = eggSVG(i, name, "bot", ck, pats[i]) + `<div class=bird><div class=face style="--dir:${dirs[i]}"><img alt=""><i class=lid></i></div></div>` + eggSVG(i, name, "top", ck, pats[i]);
      b.onclick = () => tap(i);
      box.appendChild(b); eggs.push(b);
      setStage(i, true);
      const img = b.querySelector(".bird img");
      const want = () => { const r = _ppKit.get(name, clan, "f"); if (r && !r.fail && !img.getAttribute("src")) { img.onload = () => img.classList.add("ok"); img.src = r.f; fitLid(b.querySelector(".lid"), r.f, clan); if (nest.sel === i) update(); } return r; };
      if (!want()) unsubs.push(_ppKit.sub(name, clan, want, "f"));
    });
    if (nest.sel != null && !(nest.taps[nest.sel] >= 3)) nest.sel = null;
    pick(nest.sel); update();
    if (dropNext) { dropNext = false;   // new eggs fall in from the top of the screen and bounce into the nest
      eggs.forEach((b, i) => { const r = b.getBoundingClientRect(); b.style.setProperty("--dy", -(r.bottom + 40) + "px"); b.style.animationDelay = (i * 140) + "ms"; b.classList.add("drop");
        b.addEventListener("animationend", e => { if (e.animationName === "ppn-drop") { b.classList.remove("drop"); b.style.animationDelay = ""; } }); }); }
  }
  function setStage(i, quiet) {
    const b = eggs[i], t = nest.taps[i];
    b.querySelector(".c1").style.opacity = t === 1 ? 1 : 0;
    b.querySelector(".c2").style.opacity = t >= 2 ? 1 : 0;
    b.classList.toggle("hatched", t >= 3);
    if (t >= 3) b.setAttribute("aria-label", nest.names[i]);
    b.classList.toggle("sel", nest.sel === i);
    if (quiet && t >= 3) { const d = b.querySelector(".bird"); d.style.animation = "none"; d.style.opacity = 1; d.style.transform = "none"; }
  }
  function tap(i) {
    const b = eggs[i];
    if (nest.taps[i] < 3) {
      nest.taps[i]++; b.classList.remove("hit", "wob"); void b.offsetWidth; if (nest.taps[i] < 3) b.classList.add("hit");
      if (nest.taps[i] === 3) pick(i);          // the hatching tap also picks that bird
    } else { pick(i); move(i, "bob"); }
    save();
    eggs.forEach((e, k) => setStage(k, false));
    update();
  }
  function update() {
    if (!nest) return;
    const hatched = nest.taps.filter(t => t >= 3).length;
    if (nest.sel != null) {
      const n = nest.names[nest.sel], c = clanOf(n), r = _ppKit.get(n, c, "f"), col = _ppKit.tagCol(n);
      tag.className = "ppn-tag"; tag.style.background = col; tag.style.borderColor = col; tag.innerHTML = "";
      const f = document.createElement("span"); f.className = "tf";
      if (r && !r.fail) { const im = document.createElement("img"); im.src = r.f; im.alt = ""; f.appendChild(im); } else { f.style.fontSize = "34px"; f.textContent = c; }
      const nm = document.createElement("span"); nm.className = "nm"; nm.textContent = n;
      tag.append(f, nm);
    } else { tag.className = "ppn-tag empty"; tag.style.background = ""; tag.style.borderColor = ""; tag.textContent = "Crack an egg to meet your bird"; }
    const left = nest.until - Date.now(), ss = Math.max(0, Math.ceil(left / 1000)), clock = `${Math.floor(ss / 60)}:${String(ss % 60).padStart(2, "0")}`;
    if (left <= 0) {   // time's up: the eggs roll out of the nest, then it's empty
      if (leaving) return; leaving = true; hint.textContent = "";
      eggs.forEach((b, i) => { const out = SPOTS[i][0] < 160 ? -1 : SPOTS[i][0] > 160 ? 1 : (i % 2 ? 1 : -1);
        b.style.setProperty("--rx", out * (190 + i * 12) + "px"); b.style.setProperty("--rr", out * (420 + i * 40) + "deg"); b.style.animationDelay = (i * 110) + "ms"; b.classList.remove("hit", "wob", "drop"); b.classList.add("roll"); });
      later(() => { leaving = false; empty("Tap nest to get new eggs"); }, 1100 + eggs.length * 110 + 60); return;
    }
    hint.innerHTML = `<span style="color:#475569">New nest in <b style="color:#94a3b8">${clock}</b></span>`;   // just the clock
  }
  function fitLid(lid, url, clan) {
    const e = _ppKit.eye(clan), pct = v => (v / e.W * 100) + "%", d = e.r * 2.35;
    Object.assign(lid.style, { left: pct(e.x - d / 2), top: pct(e.y - d / 2), width: pct(d), height: pct(d) });
    const im = new Image(); im.onload = () => {
      const c = document.createElement("canvas"); c.width = c.height = e.W; const x = c.getContext("2d"); x.drawImage(im, 0, 0);
      let R = 0, G = 0, B = 0, n = 0;
      for (const [dx, dy] of [[0, -1.32], [-.45, -1.25], [.45, -1.25], [0, -1.45]]) { const p = x.getImageData(Math.round(e.x + dx * e.r), Math.round(e.y + dy * e.r), 1, 1).data; if (p[3] > 200) { R += p[0]; G += p[1]; B += p[2]; n++; } }
      if (n) { const c0 = `rgb(${R / n | 0},${G / n | 0},${B / n | 0})`; lid.style.background = `radial-gradient(circle at 50% 35%, ${c0} 55%, color-mix(in srgb, ${c0} 82%, #000) 100%)`; lid.classList.add("on"); }
    }; im.src = url;
  }
  // blinking, moving about, and the unhatched eggs wobbling now and then
  function blinkLoop(i) {
    const lid = nest && eggs[i] && eggs[i].querySelector(".lid");
    if (lid && nest.taps[i] >= 3) { const go = () => { lid.classList.remove("blink"); void lid.offsetWidth; lid.classList.add("blink"); };
      go(); if (Math.random() < .25) later(go, 260); }
    later(() => blinkLoop(i), 2200 + Math.random() * 4200);
  }
  function move(i, kind) {
    const egg = eggs[i]; if (!egg) return; const img = egg.querySelector(".bird .face");
    if (kind === "look") { dirs[i] = -dirs[i]; img.style.setProperty("--dir", dirs[i]); return; }
    img.classList.remove("bob", "tilt", "peek"); void img.offsetWidth; img.classList.add(kind);
  }
  function birdLoop() {
    const h = nest ? nest.taps.map((t, i) => t >= 3 ? i : -1).filter(i => i >= 0) : [];
    if (h.length) { const i = h[Math.floor(Math.random() * h.length)], r = Math.random(); move(i, r < .45 ? "bob" : r < .82 ? "tilt" : "peek"); /* no turning around: it was a flat mirror flip */ }
    later(birdLoop, 700 + Math.random() * 1600);
  }
  function wobbleLoop() {
    const un = nest && !leaving ? eggs.filter((e, i) => nest.taps[i] < 3 && !e.classList.contains("hit") && !e.classList.contains("drop")) : [];
    if (un.length) { const e = un[Math.floor(Math.random() * un.length)]; e.classList.remove("wob"); void e.offsetWidth; e.classList.add("wob"); }
    later(wobbleLoop, 1600 + Math.random() * 2600);
  }
  root.querySelector(".ppn-wrap").addEventListener("click", () => { if (!nest && !busy) get(true); });   // an empty nest is the button
  weaves(); get(false, true);
  later(wobbleLoop, 1500); later(birdLoop, 1000); for (let i = 0; i < 5; i++) later(() => blinkLoop(i), 800 + Math.random() * 3000);
  const tick = setInterval(update, 1000);
  return () => { alive = false; clearInterval(tick); timers.forEach(clearTimeout); unsubs.forEach(u => u()); };
}
