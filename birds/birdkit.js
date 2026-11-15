// Bird avatar kit: real emoji (recoloured with its own shading) + realistic traits + rules that read the username.
// Needs seg2.js (segment, S). Exposes window.birdkit = { draw(name, overrides) -> {url, traits}, ... }.
(function () {
  const PAD = 56;   // room around the emoji for tall crests and long beaks
  // ---------- colour (OKLab) ----------
  const toLin = v => { v /= 255; return v <= .04045 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); };
  const toSrgb = v => { v = v <= .0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - .055; return Math.max(0, Math.min(255, Math.round(v * 255))); };
  function oklab(r, g, b) { r = toLin(r); g = toLin(g); b = toLin(b);
    const l = Math.cbrt(.4122214708 * r + .5363325363 * g + .0514459929 * b), m = Math.cbrt(.2119034982 * r + .6806995451 * g + .1073969566 * b), s = Math.cbrt(.0883024619 * r + .2817188376 * g + .6299787005 * b);
    return [.2104542553 * l + .793617785 * m - .0040720468 * s, 1.9779984951 * l - 2.428592205 * m + .4505937099 * s, .0259040371 * l + .7827717662 * m - .808675766 * s]; }
  function fromOklab(L, a, b) { const l = Math.pow(L + .3963377774 * a + .2158037573 * b, 3), m = Math.pow(L - .1055613458 * a - .0638541728 * b, 3), s = Math.pow(L - .0894841775 * a - 1.291485548 * b, 3);
    return [toSrgb(4.0767416621 * l - 3.3077115913 * m + .2309699292 * s), toSrgb(-1.2684380046 * l + 2.6097574011 * m - .3413193965 * s), toSrgb(-.0041960863 * l - .7034186147 * m + 1.707614701 * s)]; }
  const css = (c, dL = 0, a = 1) => { const h = c[2] * Math.PI / 180, [r, g, b] = fromOklab(Math.max(0, Math.min(1, c[0] + dL)), c[1] * Math.cos(h), c[1] * Math.sin(h)); return `rgba(${r},${g},${b},${a})`; };
  function paint(D, px, target, weight) {
    if (!px || !px.length) return;
    let mL = 0, mC = 0; const lab = px.map(p => oklab(D[p * 4], D[p * 4 + 1], D[p * 4 + 2]));
    for (const c of lab) { mL += c[0]; mC += Math.hypot(c[1], c[2]); } mL /= px.length; mC /= px.length;
    const [tL, tC, tH] = target, hr = tH * Math.PI / 180;
    px.forEach((p, k) => {
      const [L, a, b] = lab[k], C = Math.hypot(a, b);
      const nL = Math.max(0, Math.min(1, tL + (L - mL) * .95));
      const nC = tC * Math.max(.25, Math.min(1.6, mC > .01 ? C / mC : 1)) * (1 - Math.max(0, (L - .9) * 4));
      const [r, g, bb] = fromOklab(nL, nC * Math.cos(hr), nC * Math.sin(hr)), w = weight ? weight[k] : 1, i = p * 4;
      D[i] += (r - D[i]) * w; D[i + 1] += (g - D[i + 1]) * w; D[i + 2] += (bb - D[i + 2]) * w;
    });
  }
  const meanCol = (D, px) => { let L = 0, a = 0, b = 0; for (const p of px) { const c = oklab(D[p * 4], D[p * 4 + 1], D[p * 4 + 2]); L += c[0]; a += c[1]; b += c[2]; } const n = px.length || 1; L /= n; a /= n; b /= n; return [L, Math.hypot(a, b), (Math.atan2(b, a) * 180 / Math.PI + 360) % 360]; };
  // box blur of a mask's alpha channel, two passes (looks close to a soft gaussian)
  function blurAlpha(md, W, rad) {
    const a = new Float32Array(W * W), t = new Float32Array(W * W); for (let p = 0; p < W * W; p++) a[p] = md[p * 4 + 3];
    for (let pass = 0; pass < 2; pass++) {
      for (let y = 0; y < W; y++) { let acc = 0; for (let x = -rad; x < W + rad; x++) { const add = x + rad < W && x + rad >= 0 ? a[y * W + x + rad] : 0, sub = x - rad - 1 >= 0 && x - rad - 1 < W ? a[y * W + x - rad - 1] : 0; acc += add - sub; if (x >= 0 && x < W) t[y * W + x] = acc / (2 * rad + 1); } }
      for (let x = 0; x < W; x++) { let acc = 0; for (let y = -rad; y < W + rad; y++) { const add = y + rad < W && y + rad >= 0 ? t[(y + rad) * W + x] : 0, sub = y - rad - 1 >= 0 && y - rad - 1 < W ? t[(y - rad - 1) * W + x] : 0; acc += add - sub; if (y >= 0 && y < W) a[y * W + x] = acc / (2 * rad + 1); } }
    }
    for (let p = 0; p < W * W; p++) md[p * 4 + 3] = a[p];
  }
  function hash(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function rng(seed) { let a = seed; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

  // ---------- colours named in usernames (OKLab lightness, chroma, hue) ----------
  const COLOUR = {
    red: [.6, .2, 27], scarlet: [.6, .21, 30], crimson: [.52, .19, 15], fiery: [.66, .19, 42], flame: [.68, .18, 50], coral: [.72, .14, 35], garnet: [.45, .15, 15], maroon: [.4, .12, 18],
    orange: [.74, .16, 58], rufous: [.58, .13, 50], rusty: [.56, .12, 48], ferruginous: [.55, .12, 45], cinnamon: [.62, .1, 60], copper: [.62, .12, 55], chestnut: [.45, .09, 45], tawny: [.66, .1, 70],
    fulvous: [.7, .11, 72], buff: [.82, .07, 80], golden: [.82, .15, 88], yellow: [.88, .16, 100], olive: [.58, .1, 115], green: [.64, .16, 145], emerald: [.6, .15, 160], malachite: [.58, .13, 165],
    turquoise: [.74, .12, 190], azure: [.68, .13, 240], blue: [.6, .17, 255], indigo: [.45, .16, 275], violet: [.6, .17, 300], purple: [.52, .18, 310], lilac: [.76, .09, 310], magenta: [.6, .22, 340],
    pink: [.78, .12, 350], brown: [.5, .07, 55], black: [.28, .02, 260], sooty: [.33, .02, 260], dark: [.35, .04, 260], dusky: [.45, .03, 260], slaty: [.5, .04, 250], ashy: [.68, .02, 250], grey: [.65, .01, 250],
    silvery: [.82, .02, 240], white: [.95, .01, 240], pale: [.88, .04, 90], velvet: [.4, .12, 330], oceanic: [.55, .12, 230], glossy: [.4, .1, 280], iridescent: [.55, .14, 200], arctic: [.92, .03, 220],
    alpine: [.85, .04, 230], siberian: [.82, .03, 230], royal: [.48, .17, 275], tropical: [.72, .17, 150], amazonian: [.62, .16, 150], sacred: [.88, .05, 95], elegant: [.6, .08, 330], painted: null,
  };
  // places: a colour range per region; each place takes its own spot in it (L, chroma, hue from-to)
  const REGION = {
    cold: [[.84, .9], [.02, .06], [190, 235], ["arctic", "siberian", "alpine", "tibetan", "mongolian", "himalayan", "mountain"]],
    desert: [[.66, .8], [.07, .12], [50, 85], ["african", "arabian", "cape", "australasian"]],
    jungle: [[.55, .72], [.11, .17], [125, 175], ["amazonian", "tropical", "andean", "bornean", "papuan", "javan", "sumatran"]],
    jewel: [[.5, .68], [.13, .19], [240, 360], ["asian", "oriental", "chinese", "burmese", "indian", "philippine"]],
    sea: [[.55, .72], [.09, .14], [195, 250], ["pacific", "island", "oceanic"]],
    temperate: [[.52, .7], [.06, .12], [20, 120], ["american", "northern", "southern", "eastern", "western", "european", "eurasian"]],
  };
  function placeColour(adj) {
    for (const [, [Lr, Cr, Hr, list]] of Object.entries(REGION)) { const i = list.indexOf(adj); if (i < 0) continue;
      const f = list.length > 1 ? i / (list.length - 1) : .5, h = hash(adj); return [Lr[0] + (Lr[1] - Lr[0]) * ((h % 97) / 96), Cr[0] + (Cr[1] - Cr[0]) * (((h >> 7) % 89) / 88), Hr[0] + (Hr[1] - Hr[0]) * f]; }
    return null; }
  // any other word (common, giant, little, melodious...) gets its own fixed shade from the word itself
  const wordColour = adj => { const h = hash("c:" + adj); return [.58 + (h % 23) / 100, .08 + ((h >> 5) % 8) / 100, (h >> 9) % 360]; };
  const PALETTE = [[.8, .14, 95], [.72, .12, 60], [.66, .13, 30], [.66, .13, 350], [.72, .11, 330], [.62, .12, 300], [.64, .12, 250], [.72, .1, 200], [.68, .13, 150], [.7, .14, 130], [.55, .06, 60], [.5, .09, 25]];

  // ---------- markings painted into the feathers (canvas pixels; G = box, real eye E, beak base B) ----------
  const ell = (m, x, y, rx, ry, rot = 0) => { m.beginPath(); m.ellipse(x, y, Math.max(.1, rx), Math.max(.1, ry), rot, 0, 7); m.fill(); };
  const curve = (m, a, c, b, w) => { m.lineWidth = w; m.lineCap = "round"; m.beginPath(); m.moveTo(...a); m.quadraticCurveTo(...c, ...b); m.stroke(); };
  const MARKS = {
    spots: (m, r, G) => { for (let i = 0; i < 4 + Math.floor(r() * 5); i++) ell(m, G.E.x + G.w * (.1 + r() * .4), G.y0 + G.h * (.12 + r() * .72), G.w * (.03 + r() * .035), G.w * (.03 + r() * .03), r() * 3); },
    speckles: (m, r, G) => { for (let i = 0; i < 30; i++) ell(m, G.B.x + (G.x1 - G.B.x) * r(), G.y0 + G.h * (.08 + r() * .84), G.w * .012, G.w * .012); },
    stripes: (m, r, G) => { for (let i = 0; i < 4; i++) { const sx = G.E.x + G.w * (.18 + i * .1); curve(m, [sx, G.y0], [sx + G.w * .06, G.y0 + G.h * .45], [sx - G.w * .04, G.y1], G.w * .035); } },
    streaks: (m, r, G) => { for (let i = 0; i < 9; i++) { const x = G.E.x + G.w * (.05 + r() * .45), y = G.y0 + G.h * (.3 + r() * .55); curve(m, [x, y], [x + G.w * .015, y + G.h * .05], [x - G.w * .01, y + G.h * .1], G.w * .018); } },
    bars: (m, r, G) => { for (let i = 0; i < 4; i++) { const y = G.y0 + G.h * (.18 + i * .2); curve(m, [G.E.x + G.w * .15, y], [G.E.x + G.w * .35, y - G.h * .05], [G.x1, y + G.h * .02], G.h * .05); } },
    scales: (m, r, G) => { m.lineWidth = G.w * .016; for (let row = 0; row < 4; row++) for (let i = 0; i < 4; i++) { m.beginPath(); m.arc(G.E.x + G.w * (.12 + i * .1 + (row % 2) * .05), G.y0 + G.h * (.25 + row * .17), G.w * .045, .2, Math.PI - .2); m.stroke(); } },
    mottled: (m, r, G) => { for (let i = 0; i < 7; i++) ell(m, G.B.x + (G.x1 - G.B.x) * r(), G.y0 + G.h * r(), G.w * (.05 + r() * .06), G.w * (.04 + r() * .05), r() * 3); m.filter = "none"; },
    cap: (m, r, G) => ell(m, G.E.x + G.w * .12, G.y0 - G.h * .04, G.w * .42, G.h * .28),
    "crown stripe": (m, r, G) => curve(m, [G.B.x + G.w * .06, G.y0 + G.h * .1], [G.E.x + G.w * .1, G.y0 - G.h * .06], [G.x1, G.y0 + G.h * .25], G.w * .06),
    "racing stripe": (m, r, G) => curve(m, [G.B.x + G.w * .02, G.y0 + G.h * .16], [G.E.x + G.w * .12, G.y0 - G.h * .02], [G.x1, G.y0 + G.h * .3], G.w * .12),
    "black hood": (m, r, G) => { m.beginPath(); m.moveTo(G.x0, G.E.y + G.E.r * 2.2); m.quadraticCurveTo(G.x0 + G.w * .6, G.E.y + G.E.r * .9, G.x1 + 4, G.E.y + G.E.r * 2.8); m.lineTo(G.x1 + 4, G.y0 - 4); m.lineTo(G.x0, G.y0 - 4); m.fill(); },
    nape: (m, r, G) => ell(m, G.x1, G.y0 + G.h * .45, G.w * .26, G.h * .42),
    "nape collar": (m, r, G) => { m.lineWidth = G.h * .09; m.beginPath(); m.ellipse(G.x0 + G.w * .62, G.y0 + G.h * .2, G.w * .5, G.h * .7, 0, .5, 2.7); m.stroke(); },
    "face mask": (m, r, G) => { const E = G.E;   // band through the eye, rounded at both ends; on songbirds it wraps the white eye patch
      const P = G.P || { x0: E.x - E.r * 1.3, x1: E.x + E.r * 1.3, y0: E.y - E.r * 1.3, y1: E.y + E.r * 1.3 };
      const m0 = E.r * .75, top = P.y0 - m0, bot = P.y1 + m0 * (G.P ? 1.25 : .8), hr = (bot - top) / 2, cy = (top + bot) / 2;
      const left = Math.max(G.B.x + E.r * .3, P.x0 - m0) , right = P.x1 + E.r * 3.2;
      m.beginPath(); m.moveTo(left + hr, top); m.lineTo(right - hr * .8, top + hr * .15);
      m.arc(right - hr * .8, cy, hr * .85, -Math.PI / 2, Math.PI / 2); m.lineTo(left + hr, bot);
      m.arc(left + hr, cy, hr, Math.PI / 2, Math.PI * 1.5); m.fill(); },
    "eye stripe": (m, r, G) => { m.lineWidth = G.E.r * 1.1; m.lineCap = "round"; m.beginPath(); m.moveTo(G.E.x - G.E.r * .2, G.E.y + G.E.r); m.quadraticCurveTo(G.E.x - G.E.r * .6, G.E.y + G.E.r * 3, G.E.x + G.E.r * .6, G.E.y + G.E.r * 4.6); m.stroke(); },   // falcon "tear" stripe down from the eye
    "eye ring": (m, r, G) => { m.lineWidth = G.E.r * .7; m.beginPath(); m.ellipse(G.E.x, G.E.y, G.E.r * 1.55, G.E.r * 1.65, 0, 0, 7); m.stroke(); },
    "eye crescent": (m, r, G) => { m.lineWidth = G.E.r * .6; m.lineCap = "round"; m.beginPath(); m.ellipse(G.E.x, G.E.y, G.E.r * 1.7, G.E.r * 1.8, 0, .35, Math.PI - .35); m.stroke(); },
    "eye wattle": (m, r, G) => { m.lineWidth = G.E.r * 1.15; m.beginPath(); m.ellipse(G.E.x, G.E.y, G.E.r * 1.8, G.E.r * 1.9, 0, 0, 7); m.stroke(); },
    "bare face": (m, r, G) => { m.beginPath(); m.ellipse(G.E.x - G.E.r * .5, G.E.y + G.E.r * 1.4, G.E.r * 3.4, G.E.r * 4, -.2, 0, 7); m.fill(); m.filter = "none"; },
    "cheek patch": (m, r, G) => ell(m, G.E.x + G.E.r * 2.6, G.E.y + G.E.r * 2.6, G.E.r * 1.9, G.E.r * 1.7),
    "white cheeks": (m, r, G) => ell(m, G.E.x + G.E.r * .8, G.E.y + G.E.r * 3, G.E.r * 2.6, G.E.r * 1.8, -.2),
    "cheek blush": (m, r, G) => { const x = G.E.x + G.E.r * .4, y = G.E.y + G.E.r * 2.4, g = m.createRadialGradient(x, y, 0, x, y, G.E.r * 2.2); g.addColorStop(0, "#000"); g.addColorStop(1, "rgba(0,0,0,0)"); m.fillStyle = g; m.fillRect(-600, -600, 2000, 2000); },
    "brow ridge": (m, r, G) => { m.beginPath(); m.moveTo(G.E.x - G.E.r * 2.2, G.E.y - G.E.r * .9); m.quadraticCurveTo(G.E.x, G.E.y - G.E.r * 3.2, G.E.x + G.E.r * 3, G.E.y - G.E.r * 1.3); m.quadraticCurveTo(G.E.x, G.E.y - G.E.r * 1.6, G.E.x - G.E.r * 2.2, G.E.y - G.E.r * .9); m.fill(); },
    eyebrow: (m, r, G) => curve(m, [G.E.x - G.E.r * 1.5, G.E.y - G.E.r * 1.6], [G.E.x + G.E.r * .5, G.E.y - G.E.r * 3], [G.E.x + G.E.r * 3, G.E.y - G.E.r * 1.7], G.E.r * .6),
    moustache: (m, r, G) => curve(m, [G.B.x - 2, G.B.y + G.E.r * .4], [G.E.x + G.E.r, G.B.y + G.E.r * 1.2], [G.E.x + G.E.r * 3.2, G.B.y + G.E.r * 2.6], G.E.r * .8),
    bib: (m, r, G) => ell(m, G.B.x + G.E.r * 1.2, G.B.y + G.E.r * 3, G.E.r * 2.4, G.E.r * 1.8),
    throat: (m, r, G) => ell(m, G.B.x + G.w * .12, G.y1, G.w * .32, G.h * .24),
    lores: (m, r, G) => ell(m, G.B.x + G.E.r * .8, G.B.y - G.E.r * .4, G.E.r * 1.4, G.E.r * 1.9),
    forehead: (m, r, G) => ell(m, G.B.x + G.E.r * 1.2, G.E.y - G.E.r * 2.4, G.E.r * 2.4, G.E.r * 1.5, -.4),
    "facial disc": (m, r, G) => { m.beginPath(); m.ellipse(G.E.x + G.E.r * .6, G.E.y + G.E.r * 1.2, G.E.r * 3.6, G.E.r * 4.2, 0, 0, 7); m.fill(); },
    "two-tone": (m, r, G) => { m.beginPath(); m.moveTo(G.x0, G.y0 + G.h * .62); m.quadraticCurveTo(G.x0 + G.w * .6, G.y0 + G.h * .48, G.x1 + 4, G.y0 + G.h * .7); m.lineTo(G.x1 + 4, G.y1 + 4); m.lineTo(G.x0, G.y1 + 4); m.fill(); },
    fade: (m, r, G) => { const g = m.createLinearGradient(0, G.y0, 0, G.y1); g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(.45, "rgba(0,0,0,0)"); g.addColorStop(1, "#000"); m.fillStyle = g; m.fillRect(-600, -600, 2000, 2000); },
  };
  // which markings use a light colour, a dark colour, or a skin colour
  const MARK_TONE = { "black hood": "dark", "face mask": "dark", "eye stripe": "dark", moustache: "dark", bib: "dark", "brow ridge": "dark", lores: "dark",
    "white cheeks": "white", "eye crescent": "white", "eye ring": "white", "facial disc": "white", "eye wattle": "skin", "bare face": "skin", "cheek blush": "blush", "cheek patch": "accent" };

  // ---------- feathers drawn on the head (behind it), with shading like the emoji ----------
  // a tapered feather: base (bx,by), length, angle (0 = up, + = toward the back), width; optional tip colour band
  function feather(x, bx, by, len, ang, wid, bend = 0) {
    x.save(); x.translate(bx, by); x.rotate(ang); x.beginPath(); x.moveTo(-wid, 2);
    x.bezierCurveTo(-wid * 1.1, -len * .45, -wid * .4 + bend, -len * .85, bend, -len); x.bezierCurveTo(wid * .5 + bend, -len * .8, wid * 1.05, -len * .4, wid, 2); x.closePath(); x.restore();
  }
  function shade(ctx, G, col, build, tip, opts = {}) {
    const t = document.createElement("canvas"); t.width = t.height = ctx.canvas.width; const x = t.getContext("2d"); x.translate(PAD, PAD);
    const g = x.createLinearGradient(G.x0 + G.w * .4, G.y0 - G.h * .45, G.x0 + G.w * .6, G.y0 + G.h * .2); g.addColorStop(0, css(col, .1)); g.addColorStop(1, css(col, -.12));
    x.fillStyle = g; x.strokeStyle = g; build(x);
    x.globalCompositeOperation = "source-atop";
    if (tip) { const tg = x.createLinearGradient(0, G.y0 - G.h * (opts.tipTop || .55), 0, G.y0 - G.h * (opts.tipBottom || .25)); tg.addColorStop(0, css(tip)); tg.addColorStop(.55, css(tip)); tg.addColorStop(.56, opts.band ? css(opts.band) : "rgba(0,0,0,0)"); tg.addColorStop(.75, opts.band ? css(opts.band) : "rgba(0,0,0,0)"); tg.addColorStop(.76, "rgba(0,0,0,0)"); x.fillStyle = tg; x.fillRect(-600, -600, 2000, 2000); }
    const hl = x.createRadialGradient(G.x0 + G.w * .45, G.y0 - G.h * .3, 0, G.x0 + G.w * .45, G.y0 - G.h * .3, G.w * .35); hl.addColorStop(0, "rgba(255,255,255,.32)"); hl.addColorStop(1, "rgba(255,255,255,0)");
    x.fillStyle = hl; x.fillRect(-600, -600, 2000, 2000);
    if (opts.shafts) { x.globalCompositeOperation = "source-atop"; x.strokeStyle = css(col, -.22, .55); x.lineWidth = 1; opts.shafts(x); }
    ctx.drawImage(t, -PAD, -PAD);
  }
  const fill = x => x.fill();
  const TOPS = {
    crest: { tone: "body", draw: (x, G) => { const bx = G.x0 + G.w * .6, by = G.y0 + G.h * .1; [[-.1, .26, -.45], [0, .33, -.1], [.1, .27, .3]].forEach(([dx, l, a]) => { feather(x, bx + dx * G.w, by, l * G.h, a, G.w * .045); fill(x); }); } },
    "fan crest": { tone: "orange", tip: "black", band: "white", draw: (x, G) => { const bx = G.x0 + G.w * .5, by = G.y0 + G.h * .14; for (let i = 0; i < 7; i++) { feather(x, bx + i * G.w * .045, by + i * G.h * .005, G.h * (.42 - Math.abs(i - 3) * .025), -.7 + i * .26, G.w * .042); fill(x); } }, tipTop: .62, tipBottom: .2 },
    mohawk: { tone: "light", draw: (x, G) => { for (let i = 0; i < 6; i++) { const bx = G.x0 + G.w * (.5 + i * .035), by = G.y0 + G.h * .1; x.save(); x.translate(bx, by); x.rotate(-.35 + i * .07); x.beginPath(); x.moveTo(-G.w * .025, 2); x.bezierCurveTo(-G.w * .04, -G.h * .3, -G.w * .1, -G.h * .5, -G.w * (.12 + i * .02), -G.h * (.6 - i * .03)); x.bezierCurveTo(-G.w * .05, -G.h * .42, -G.w * .01, -G.h * .25, G.w * .025, 2); x.fill(); x.restore(); } } },
    crown: { tone: "body", draw: (x, G) => { const cx = G.x0 + G.w * .58, cy = G.y0 + G.h * .16; x.lineCap = "round"; for (let i = 0; i < 15; i++) { const a = -1.1 + i * .16, len = G.h * (.38 + Math.sin(i * 1.7) * .03); const ex = cx + Math.sin(a) * len, ey = cy - Math.cos(a) * len; x.lineWidth = G.w * .012; x.beginPath(); x.moveTo(cx + Math.sin(a) * G.h * .08, cy - Math.cos(a) * G.h * .08); x.quadraticCurveTo(cx + Math.sin(a) * len * .6, cy - Math.cos(a) * len * .6 - 2, ex, ey); x.stroke(); x.beginPath(); x.ellipse(ex, ey, G.w * .03, G.w * .022, a, 0, 7); x.fill(); } } },
    "flame crest": { tone: "red", draw: (x, G) => { const bx = G.x0 + G.w * .45, by = G.y0 + G.h * .12; x.beginPath(); x.moveTo(bx, by); x.bezierCurveTo(bx + G.w * .05, by - G.h * .2, bx + G.w * .3, by - G.h * .3, bx + G.w * .62, by - G.h * .2); x.bezierCurveTo(bx + G.w * .45, by - G.h * .12, bx + G.w * .46, by - G.h * .04, bx + G.w * .5, by + G.h * .12); x.closePath(); x.fill(); },
      shafts: (x, G) => { const bx = G.x0 + G.w * .45, by = G.y0 + G.h * .12; for (let i = 0; i < 4; i++) { x.beginPath(); x.moveTo(bx + G.w * (.08 + i * .08), by - G.h * .02); x.quadraticCurveTo(bx + G.w * (.2 + i * .08), by - G.h * .15, bx + G.w * (.4 + i * .05), by - G.h * .18); x.stroke(); } } },
    "double crest": { tone: "dark", draw: (x, G) => { for (const [fx, a] of [[.5, -.2], [.66, .35]]) { for (let k = -1; k <= 1; k++) { feather(x, G.x0 + G.w * (fx + k * .015), G.y0 + G.h * .1, G.h * (.22 - Math.abs(k) * .04), a + k * .15, G.w * .03); fill(x); } } } },
    "feather spikes": { tone: "dark", tip: "pale", draw: (x, G) => { for (let i = 0; i < 6; i++) { const bx = G.x0 + G.w * (.72 + i * .03), by = G.y0 + G.h * (.18 + i * .07); feather(x, bx, by, G.h * (.42 - i * .03), .95 + i * .12, G.w * .016); fill(x); } }, tipTop: .45, tipBottom: .1 },
    frill: { tone: "accent", draw: (x, G) => { const cx = G.x0 + G.w * .66, cy = G.y0 + G.h * .55; for (let i = 0; i < 11; i++) { const a = -.5 + i * .19; feather(x, cx + Math.sin(a) * G.w * .34, cy - Math.cos(a) * G.h * .3, G.h * .2, a, G.w * .05); fill(x); } } },
    casque: { tone: "horn", draw: (x, G) => { const bx = G.x0 + G.w * .42, by = G.y0 + G.h * .12; x.beginPath(); x.moveTo(bx, by + G.h * .04); x.bezierCurveTo(bx + G.w * .02, by - G.h * .3, bx + G.w * .22, by - G.h * .42, bx + G.w * .34, by - G.h * .32); x.bezierCurveTo(bx + G.w * .4, by - G.h * .2, bx + G.w * .42, by - G.h * .05, bx + G.w * .44, by + G.h * .06); x.closePath(); x.fill(); } },
    "horned brow": { tone: "body", draw: (x, G) => { for (const [dx, a] of [[-.08, -.35], [.16, .2]]) { for (let k = 0; k < 3; k++) { feather(x, G.E.x + G.w * (dx + k * .025), G.y0 + G.h * .12, G.h * (.24 - k * .04), a + k * .1, G.w * .03); fill(x); } } } },
    "ear tufts": { tone: "body", draw: (x, G) => { for (const [fx, a] of [[.36, -.5], [.84, .5]]) { feather(x, G.x0 + fx * G.w, G.y0 + G.h * .16, G.h * .22, a, G.w * .06); fill(x); } } },
    tuft: { tone: "body", draw: (x, G) => { const bx = G.x0 + G.w * .6, by = G.y0 + G.h * .08; feather(x, bx, by, G.h * .2, .2, G.w * .05); fill(x); feather(x, bx + G.w * .05, by, G.h * .14, .7, G.w * .035); fill(x); } },
    plume: { tone: "body", draw: (x, G) => { feather(x, G.x0 + G.w * .62, G.y0 + G.h * .08, G.h * .5, 1.0, G.w * .035, -G.w * .05); fill(x); } },
  };
  // ---------- face & quirky features drawn on top ----------
  function glossy(ctx, col, build, G, cx, cy, rr) {
    const t = document.createElement("canvas"); t.width = t.height = ctx.canvas.width; const x = t.getContext("2d"); x.translate(PAD, PAD);
    const g = x.createRadialGradient(cx - rr * .3, cy - rr * .35, 0, cx, cy, rr * 1.2); g.addColorStop(0, css(col, .14)); g.addColorStop(.6, css(col)); g.addColorStop(1, css(col, -.14));
    x.fillStyle = g; build(x); x.globalCompositeOperation = "source-atop"; x.fillStyle = "rgba(255,255,255,.28)"; x.beginPath(); x.ellipse(cx - rr * .35, cy - rr * .4, rr * .3, rr * .18, -.5, 0, 7); x.fill(); ctx.drawImage(t, -PAD, -PAD);
  }
  const FACE = {};   // face extras (the wattle and the throat pouch were removed at the user's request)
  // ---------- beaks: the emoji's beak is removed and redrawn in its own colours, top/bottom shaded ----------
  // coordinates: base at (bx, by) on the head, beak points left. bh = base height, L = original beak length.
  const BEAKS = {
    hooked: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .5} C ${bx - L * .4} ${by - bh * .62} ${bx - L * .95} ${by - bh * .4} ${bx - L * 1.05} ${by + bh * .15} C ${bx - L * 1.08} ${by + bh * .45} ${bx - L * .95} ${by + bh * .55} ${bx - L * .9} ${by + bh * .3} C ${bx - L * .7} ${by + bh * .05} ${bx - L * .3} ${by + bh * .05} ${bx} ${by + bh * .05} Z`,
      lo: `M ${bx} ${by + bh * .05} C ${bx - L * .3} ${by + bh * .05} ${bx - L * .6} ${by + bh * .12} ${bx - L * .78} ${by + bh * .22} C ${bx - L * .5} ${by + bh * .5} ${bx - L * .2} ${by + bh * .5} ${bx} ${by + bh * .5} Z` }),
    oversized: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .75} C ${bx - L * .6} ${by - bh * 1.05} ${bx - L * 1.7} ${by - bh * .7} ${bx - L * 2.1} ${by + bh * .1} C ${bx - L * 1.4} ${by - bh * .05} ${bx - L * .6} ${by + bh * .05} ${bx} ${by + bh * .05} Z`,
      lo: `M ${bx} ${by + bh * .05} C ${bx - L * .6} ${by + bh * .05} ${bx - L * 1.4} ${by - bh * .02} ${bx - L * 2.1} ${by + bh * .1} C ${bx - L * 1.5} ${by + bh * .55} ${bx - L * .6} ${by + bh * .6} ${bx} ${by + bh * .55} Z`, bands: true }),
    crossed: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .5} C ${bx - L * .5} ${by - bh * .55} ${bx - L * .9} ${by - bh * .2} ${bx - L * .95} ${by + bh * .45} C ${bx - L * .78} ${by + bh * .1} ${bx - L * .4} ${by + bh * .02} ${bx} ${by + bh * .02} Z`,
      lo: `M ${bx} ${by + bh * .02} C ${bx - L * .4} ${by + bh * .1} ${bx - L * .75} ${by + bh * .2} ${bx - L * .92} ${by - bh * .45} C ${bx - L * .85} ${by + bh * .3} ${bx - L * .4} ${by + bh * .5} ${bx} ${by + bh * .5} Z` }),
    flat: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .32} C ${bx - L * .5} ${by - bh * .36} ${bx - L * 1.15} ${by - bh * .34} ${bx - L * 1.25} ${by - bh * .05} C ${bx - L * 1.3} ${by + bh * .1} ${bx - L * 1.15} ${by + bh * .12} ${bx - L * 1.1} ${by + bh * .1} C ${bx - L * .7} ${by + bh * .06} ${bx - L * .3} ${by + bh * .06} ${bx} ${by + bh * .06} Z`,
      lo: `M ${bx} ${by + bh * .06} C ${bx - L * .4} ${by + bh * .06} ${bx - L * .9} ${by + bh * .1} ${bx - L * 1.12} ${by + bh * .12} C ${bx - L * 1.05} ${by + bh * .3} ${bx - L * .4} ${by + bh * .32} ${bx} ${by + bh * .3} Z`, nail: true }),
    spoon: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .25} L ${bx - L * 1.1} ${by - bh * .1} C ${bx - L * 1.25} ${by - bh * .4} ${bx - L * 1.6} ${by - bh * .4} ${bx - L * 1.62} ${by + bh * .05} L ${bx} ${by + bh * .05} Z`,
      lo: `M ${bx} ${by + bh * .05} L ${bx - L * 1.62} ${by + bh * .05} C ${bx - L * 1.6} ${by + bh * .45} ${bx - L * 1.25} ${by + bh * .45} ${bx - L * 1.1} ${by + bh * .18} L ${bx} ${by + bh * .3} Z` }),
    curved: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .45} C ${bx - L * .5} ${by - bh * .55} ${bx - L * .8} ${by - bh * .3} ${bx - L * .9} ${by + bh * .3} C ${bx - L * .95} ${by + bh * .8} ${bx - L * 1.05} ${by + bh * 1.1} ${bx - L * 1.0} ${by + bh * 1.3} C ${bx - L * .8} ${by + bh * .8} ${bx - L * .55} ${by + bh * .1} ${bx} ${by + bh * .05} Z`,
      lo: `M ${bx} ${by + bh * .05} C ${bx - L * .5} ${by + bh * .15} ${bx - L * .75} ${by + bh * .7} ${bx - L * .98} ${by + bh * 1.28} C ${bx - L * .7} ${by + bh * 1.05} ${bx - L * .4} ${by + bh * .55} ${bx} ${by + bh * .5} Z`, darkTip: true }),
    chisel: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .38} L ${bx - L * 1.35} ${by + bh * .02} L ${bx} ${by + bh * .04} Z`, lo: `M ${bx} ${by + bh * .04} L ${bx - L * 1.35} ${by + bh * .02} L ${bx} ${by + bh * .4} Z` }),
    giant: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .85} C ${bx - L * .7} ${by - bh * 1.15} ${bx - L * 1.45} ${by - bh * .8} ${bx - L * 1.55} ${by + bh * .1} C ${bx - L * 1.62} ${by + bh * .45} ${bx - L * 1.5} ${by + bh * .55} ${bx - L * 1.42} ${by + bh * .35} C ${bx - L * 1.0} ${by + bh * .25} ${bx - L * .5} ${by + bh * .2} ${bx} ${by + bh * .2} Z`,
      lo: `M ${bx} ${by + bh * .2} C ${bx - L * .5} ${by + bh * .2} ${bx - L * 1.0} ${by + bh * .25} ${bx - L * 1.4} ${by + bh * .4} C ${bx - L * 1.1} ${by + bh * .95} ${bx - L * .5} ${by + bh * 1.0} ${bx} ${by + bh * .8} Z` }),
    needle: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .18} L ${bx - L * 2.1} ${by + bh * .05} L ${bx} ${by + bh * .04} Z`, lo: `M ${bx} ${by + bh * .04} L ${bx - L * 2.1} ${by + bh * .05} L ${bx} ${by + bh * .2} Z` }),
    dagger: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .36} C ${bx - L * .8} ${by - bh * .25} ${bx - L * 1.5} ${by - bh * .05} ${bx - L * 1.75} ${by + bh * .06} L ${bx} ${by + bh * .06} Z`, lo: `M ${bx} ${by + bh * .06} L ${bx - L * 1.75} ${by + bh * .06} C ${bx - L * 1.4} ${by + bh * .2} ${bx - L * .8} ${by + bh * .35} ${bx} ${by + bh * .4} Z` }),
    cone: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .62} C ${bx - L * .4} ${by - bh * .6} ${bx - L * .72} ${by - bh * .3} ${bx - L * .8} ${by + bh * .05} L ${bx} ${by + bh * .05} Z`, lo: `M ${bx} ${by + bh * .05} L ${bx - L * .8} ${by + bh * .05} C ${bx - L * .7} ${by + bh * .38} ${bx - L * .4} ${by + bh * .62} ${bx} ${by + bh * .62} Z` }),
    parrot: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .75} C ${bx - L * .55} ${by - bh * .95} ${bx - L * .95} ${by - bh * .45} ${bx - L * .9} ${by + bh * .45} C ${bx - L * .82} ${by + bh * .75} ${bx - L * .7} ${by + bh * .65} ${bx - L * .66} ${by + bh * .35} C ${bx - L * .5} ${by + bh * .1} ${bx - L * .25} ${by + bh * .1} ${bx} ${by + bh * .1} Z`,
      lo: `M ${bx} ${by + bh * .1} C ${bx - L * .25} ${by + bh * .1} ${bx - L * .45} ${by + bh * .2} ${bx - L * .55} ${by + bh * .35} C ${bx - L * .4} ${by + bh * .7} ${bx - L * .15} ${by + bh * .72} ${bx} ${by + bh * .62} Z` }),
    pouch: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .32} C ${bx - L * .9} ${by - bh * .3} ${bx - L * 1.7} ${by - bh * .2} ${bx - L * 1.95} ${by + bh * .02} C ${bx - L * 1.98} ${by + bh * .18} ${bx - L * 1.9} ${by + bh * .2} ${bx - L * 1.85} ${by + bh * .1} L ${bx} ${by + bh * .06} Z`,
      lo: `M ${bx} ${by + bh * .06} L ${bx - L * 1.85} ${by + bh * .1} C ${bx - L * 1.4} ${by + bh * 1.2} ${bx - L * .5} ${by + bh * 1.5} ${bx} ${by + bh * .9} Z`, pouchCol: true }),
    horn: (bx, by, bh, L) => ({ up: `M ${bx} ${by - bh * .55} C ${bx - L * .7} ${by - bh * .7} ${bx - L * 1.5} ${by - bh * .3} ${bx - L * 1.75} ${by + bh * .4} C ${bx - L * 1.3} ${by + bh * .1} ${bx - L * .6} ${by + bh * .05} ${bx} ${by + bh * .05} Z`,
      lo: `M ${bx} ${by + bh * .05} C ${bx - L * .6} ${by + bh * .05} ${bx - L * 1.2} ${by + bh * .15} ${bx - L * 1.6} ${by + bh * .38} C ${bx - L * 1.1} ${by + bh * .55} ${bx - L * .5} ${by + bh * .55} ${bx} ${by + bh * .5} Z`,
      casque: `M ${bx + bh * .2} ${by - bh * .55} C ${bx - L * .2} ${by - bh * 1.35} ${bx - L * .95} ${by - bh * 1.25} ${bx - L * 1.2} ${by - bh * .7} C ${bx - L * .85} ${by - bh * .55} ${bx - L * .4} ${by - bh * .6} ${bx} ${by - bh * .5} Z` }),
  };
  const darkTip = from => (O, W, bx, by, len) => { for (let q = 0; q < O.length; q += 4) { if (!O[q + 3]) continue; const x = (q / 4) % W; const t = (bx - x) / len; if (t > from) { const f = Math.min(1, (t - from) * 6); O[q] *= 1 - .8 * f; O[q + 1] *= 1 - .8 * f; O[q + 2] *= 1 - .78 * f; } } };
  const WARPS = {
    hooked: { k: 1.08, s: t => 1 + .1 * t, bend: t => .42 * Math.pow(t, 2.6) },
    parrot: { shift: .16, k: .9, s: t => 1.25, bend: t => .62 * Math.pow(t, 2.2), cutBottom: .62 },   // short rounded lower half under the hook
    oversized: { shift: .32, k: 1.45, s: t => 1.3 - .15 * t, paint: (D, parts) => { paint(D, parts.beakTop, [.84, .16, 85]); paint(D, parts.beakBottom, [.68, .17, 55]); }, after: darkTip(.86) },
    giant: { shift: .3, k: 1.2, s: t => 1.5 - .1 * t, bend: t => .18 * Math.pow(t, 3) },
    curved: { k: 1.3, s: t => .95 - .2 * t, bend: t => t < .45 ? 0 : .95 * (t - .45), after: darkTip(.72) },
    flat: { k: 1.22, s: t => .62 + .12 * t },
    spoon: { k: 1.4, s: t => t < .68 ? .5 : .5 + (t - .68) * 2.3 },
    chisel: { k: 1.35, s: t => 1 - .55 * t },
    needle: { k: 1.5, s: t => .42 - .22 * t },
    decurved: { k: 1.8, s: t => .62 - .38 * t, bend: t => .6 * Math.pow(t, 2.3) },   // slender, curving down toward the tip (bee-eaters, flycatchers)
    dagger: { k: 1.45, s: t => .78 - .25 * t },
    cone: { shift: .14, k: .78, s: t => 1.22 },
    pouch: { k: 1.45, s: t => .72 - .1 * t, pouch: true },
    longer: { k: 1.3, s: t => 1 - .2 * t },
    stubby: { k: .7, s: t => 1.1 },
  };
  function drawBeak(ctx, kind, geoB, bh, L, top, bot, opt) {
    const P = BEAKS[kind](geoB.x + 2, geoB.y, bh, L), path = s => new Path2D(s);
    const lin = (c, y0, y1, d0, d1) => { const g = ctx.createLinearGradient(0, y0, 0, y1); g.addColorStop(0, css(c, d0)); g.addColorStop(1, css(c, d1)); return g; };
    const yT = geoB.y - bh, yB = geoB.y + bh * 1.4;
    ctx.save();
    ctx.fillStyle = lin(P.pouchCol ? opt.pouch : bot, geoB.y, yB, -.02, -.1); ctx.fill(path(P.lo));
    ctx.fillStyle = lin(top, yT, geoB.y + bh * .2, .08, -.04); ctx.fill(path(P.up));
    if (P.casque) { ctx.fillStyle = lin(opt.casque || top, geoB.y - bh * 1.4, geoB.y - bh * .5, .06, -.06); ctx.fill(path(P.casque)); }
    if (P.bands) { ctx.save(); ctx.clip(path(P.up)); ctx.fillStyle = css(opt.band || [.62, .2, 30]); ctx.fillRect(geoB.x - L * 2.2, -600, L * .7, 2000); ctx.fillStyle = css([.25, .02, 260]); ctx.fillRect(geoB.x - L * 2.3, -600, L * .35, 2000); ctx.restore(); ctx.save(); ctx.clip(path(P.lo)); ctx.fillStyle = css([.25, .02, 260]); ctx.fillRect(geoB.x - L * 2.3, -600, L * .35, 2000); ctx.restore(); }
    if (P.darkTip) for (const s of [P.up, P.lo]) { ctx.save(); ctx.clip(path(s)); ctx.fillStyle = css([.22, .02, 260]); ctx.fillRect(-600, geoB.y + bh * .5, geoB.x - L * .78 + 600, 2000); ctx.restore(); }
    if (P.nail) { ctx.fillStyle = css(top, -.2); ctx.beginPath(); ctx.ellipse(geoB.x - L * 1.18, geoB.y - bh * .08, L * .06, bh * .1, 0, 0, 7); ctx.fill(); }
    // crease and highlight like the emoji's beak
    ctx.strokeStyle = css(bot, -.18, .7); ctx.lineWidth = 1; ctx.stroke(path(P.lo));
    ctx.save(); ctx.clip(path(P.up)); const hl = ctx.createLinearGradient(0, yT, 0, geoB.y); hl.addColorStop(0, "rgba(255,255,255,.35)"); hl.addColorStop(.5, "rgba(255,255,255,0)"); ctx.fillStyle = hl; ctx.fillRect(-600, -600, 2000, 2000); ctx.restore();
    ctx.restore();
  }

  // ---------- reading the username ----------
  const PART_RULES = {   // every body-part word does something of its own
    crowned: ["crown"], capped: ["cap"], crested: ["@crest"], plumed: ["@plume"], hooded: ["black hood"], headed: ["crown stripe"], masked: ["face mask"], browed: ["brow ridge"], eyed: ["eye ring"],
    cheeked: ["cheek patch"], eared: ["@ears"], faced: ["bare face"], fronted: ["forehead"], lored: ["lores"], billed: ["@beak"], throated: ["throat"], chinned: ["bib"], bibbed: ["bib"], gorgeted: ["iridescence"],
    necked: ["moustache"], collared: ["nape collar"], ringed: ["eye crescent"], naped: ["nape"], backed: ["two-tone"], mantled: ["white cheeks"], shouldered: ["racing stripe"], rumped: ["cheek blush"],
    breasted: ["two-tone"], chested: ["eyebrow"], bellied: ["fade"], vented: ["scales"], flanked: ["mottled"], sided: ["eye stripe"], spotted: ["spots"], speckled: ["speckles"], streaked: ["streaks"], striped: ["stripes"],
    banded: ["bars"], tipped: ["@tipped"], tailed: ["tuft"], winged: ["frill"], legged: ["feather spikes"], footed: ["eye wattle"],
  };
  const ADJ_RULES = { spotted: "spots", speckled: "speckles", streaked: "streaks", striped: "stripes", banded: "bars", barred: "bars", ringed: "nape collar", collared: "nape collar", crested: "@crest", hooded: "black hood",
    royal: "crown", sacred: "crown", elegant: "@plume", varied: "mottled", painted: "two-tone", glossy: "iridescence", iridescent: "iridescence", flame: "flame crest", fiery: "flame crest" };
  const SPECIES = [
    [/toucan|aracari/, { beak: "oversized" }], [/hornbill/, { beak: "oversized" }], [/eagle|hawk|goshawk|harrier|kite|buzzard|kestrel|skua/, { beak: "hooked", marks: ["brow ridge"] }],
    [/falcon/, { beak: "hooked", marks: ["eye stripe"] }], [/vulture/, { beak: "hooked", marks: ["bare face"] }], [/owl/, { beak: "parrot", marks: ["facial disc"], tops: ["horned brow"] }],
    [/duck|merganser|teal/, { beak: "flat" }], [/flamingo/, { beak: "curved" }], [/ibis|curlew/, { beak: "curved" }], [/woodpecker/, { beak: "chisel", tops: ["flame crest"] }], [/nuthatch|treecreeper/, { beak: "chisel" }],
    [/pelican/, { beak: "pouch" }], [/stork|heron|egret|bittern|crane|kingfisher|jacamar/, { beak: "dagger" }], [/hummingbird|sunbird|myzomela|honeyeater/, { beak: "needle", marks: ["iridescence"] }], [/bee-eater/, { beak: "decurved", marks: ["iridescence"] }], [/flycatcher/, { beak: "decurved" }],
    [/finch|grosbeak|bunting|sparrow|canary|waxbill|weaver|seedeater|conebill|parrotbill/, { beak: "cone" }], [/parrot|parakeet|lorikeet|cockatoo/, { beak: "parrot" }],
    [/cockatoo/, { tops: ["mohawk"] }], [/grebe/, { tops: ["double crest"] }], [/pigeon|dove/, { tops: ["crown"] }], [/pheasant/, { marks: ["eye wattle"] }], [/barbet|puffbird/, { marks: ["moustache"] }],
    [/nightjar/, { marks: ["mottled"] }], [/cormorant|booby/, { marks: ["bare face"] }], [/albatross|petrel|gull|tern/, { beak: "hooked" }], [/lapwing/, { tops: ["plume"] }],
  ];
  const EXTRAS = [["spots", 3], ["speckles", 3], ["cap", 3], ["cheek patch", 2], ["eye ring", 2], ["eye crescent", 2], ["eyebrow", 2], ["racing stripe", 1], ["scales", 1], ["mottled", 2], ["white cheeks", 2], ["moustache", 2],
    ["@crest", 2], ["tuft", 2], ["@cheek", 2], ["fan crest", 1], ["frill", 1], ["casque", 1], ["feather spikes", 1], ["throat", 1]];   // throat patch took the wattle's slot so every name keeps its own bird
  const pickW = (r, list) => { const tot = list.reduce((a, x) => a + x[1], 0); let v = r() * tot; for (const [k, w] of list) { v -= w; if (v <= 0) return k; } return list[0][0]; };
  const ROLL = { "@crest": ["crest", "fan crest", "mohawk", "flame crest", "double crest", "crown"], "@plume": ["plume", "feather spikes"], "@ears": ["ear tufts", "horned brow"], "@cheek": ["cheek patch", "white cheeks", "cheek blush"],
    "@eye": ["eye ring", "eye wattle", "eye crescent"], "@beak": ["#beakcol"], "@tipped": ["#tips"] };

  // real beak colours by family (OKLab L, chroma, hue). Families not listed keep the emoji's own beak.
  const BK = { black: [.27, .01, 260], slate: [.42, .02, 250], horn: [.8, .05, 75], yellow: [.86, .15, 98], orange: [.72, .16, 58], red: [.6, .19, 30], pink: [.78, .1, 5], rose: [.65, .08, 10], blue: [.62, .07, 235], ivory: [.88, .04, 90] };
  const BEAK_TINT = [
    [/toucan|aracari/, []],
    [/raven|drongo|magpie|jay|swift|swallow|martin|antbird|antshrike|kingfisher|hummingbird|sunbird|myzomela|honeyeater|cuckoo|monarch|waxwing|avocet|ibis|cotinga|pitta|bulbul|flowerpecker|dacnis|cockatoo|skua|grebe|cormorant|nightjar|drongo|shrike|bee-eater|flycatcher/, [BK.black, BK.black, BK.slate]],
    [/blackbird|thrush|mockingbird/, [BK.orange, BK.yellow, BK.black]],
    [/starling|gull|heron|egret|bittern|barbet|trogon|canary/, [BK.yellow, BK.yellow, BK.orange]],
    [/finch|grosbeak|bunting|sparrow|weaver|parrotbill|conebill|seedeater/, [BK.horn, BK.ivory, BK.pink, BK.yellow, BK.slate]],
    [/waxbill|merganser|stork|tern|rail|lorikeet|puffbird|jacana|oriole/, [BK.red, BK.red, BK.orange]],
    [/duck|teal|pelican|hornbill|plover|lapwing|penguin/, [BK.orange, BK.yellow, BK.slate]],
    [/flamingo/, [BK.pink]], [/pigeon|dove/, [BK.rose, BK.slate]], [/booby/, [BK.blue]], [/broadbill/, [BK.blue, BK.yellow]],
    [/eagle|hawk|goshawk|kite|buzzard|harrier|kestrel|falcon/, [BK.slate, BK.black]], [/vulture|albatross|petrel|parrot|parakeet|owl|crane/, [BK.horn, BK.ivory, BK.slate]],
    [/woodpecker|nuthatch|treecreeper|creeper/, [BK.slate, BK.black]], [/pheasant|francolin|bustard|coucal|sandpiper|snipe/, [BK.horn, BK.slate]],
  ];
  // the same clan rule as the live site (keeps everyone's clan)
  function clanOf(name) { let h = 0; for (let i = 0; i < name.length; i++) h = name.charCodeAt(i) + ((h << 5) - h); return ["🐤", "🐦", "🐧"][Math.abs(h) % 3]; }

  function describe(name) {
    const words = name.toLowerCase().split("-"), adj = words[0], part = words[1], species = words.slice(2).join("-");
    const r = rng(hash(name)), why = [], want = new Set(), o = { name, clan: clanOf(name), marks: [], tops: [], face: [] };
    const pc = placeColour(adj);
    o.body = COLOUR[adj] ? COLOUR[adj].slice() : pc || wordColour(adj);
    why.push(COLOUR[adj] ? `${adj} → colour` : pc ? `${adj} → regional colour` : `${adj} → its own shade`);
    // 3. species tunes the shade and picks the marking colour
    const hs = hash("s:" + species);
    o.body = [Math.max(.2, Math.min(.95, o.body[0] + ((hs % 9) - 4) * .012)), Math.max(.01, o.body[1] + (((hs >> 4) % 5) - 2) * .006), (o.body[2] + ((hs >> 8) % 25) - 12 + 360) % 360];
    o.markHue = (hs >> 13) % 360;
    {
      // marking colour from the part + species words, picked to sit well with the body (complement, triad, split or neighbour)
      const hm = hash("m:" + part + "|" + species), OFF = [180, 150, -150, 120, -120, 40, -40, 90, -90];
      o.markHue = Math.round((o.body[2] + OFF[hm % OFF.length] + ((hm >> 4) % 31) - 15 + 720) % 360);
      o.markDark = ((hm >> 9) & 1) === 1;
      // penguin back spot gets its own colour too
      const hk = hash("k:" + adj + "|" + part), SOFF = [0, 30, -30, 60, -60, 120, -120, 180];
      o.spotCol = [.62 + ((hk >> 3) % 24) / 100, .1 + ((hk >> 8) % 9) / 100, Math.round((o.body[2] + SOFF[hk % SOFF.length] + ((hk >> 12) % 21) - 10 + 720) % 360)];
      // natural beak colour for the species family
      for (const [re, cols] of BEAK_TINT) if (re.test(species)) { o.beakTint = cols[hs % cols.length]; break; }
    }
    const add = (k, reason) => { if (!k || want.has(k)) return; if (ROLL[k]) k = ROLL[k][Math.floor(r() * ROLL[k].length)]; if (k === "#beakcol") { o.beakCol = [.66 + r() * .1, .15, Math.floor(r() * 360)]; why.push(reason + " → bright beak"); return; }
      if (k === "#tips") { o.tipped = true; why.push(reason + " → coloured tips"); return; } if (k === "@extra") { k = pickW(r, EXTRAS); if (ROLL[k]) k = ROLL[k][Math.floor(r() * ROLL[k].length)]; }
      want.add(k); if (MARKS[k] || k === "iridescence") o.marks.push(k); else if (TOPS[k]) o.tops.push(k); else if (FACE[k]) o.face.push(k); if (reason) why.push(`${reason} → ${k}`); };
    // species first: its signature crest/beak wins over a generic word
    const sp = SPECIES.filter(([re]) => re.test(species));
    for (const [, s] of sp) { if (s.beak && !o.beak) { o.beak = s.beak; why.push(`${species} → ${s.beak} beak`); } (s.marks || []).forEach(k => add(k, species)); (s.tops || []).forEach(k => add(k, species)); (s.face || []).forEach(k => add(k, species)); }
    why.push(`${species} → shade + marking colour`);
    if (ADJ_RULES[adj]) add(ADJ_RULES[adj], adj);
    // if the species already has a head feather, a head-feather word gives a marking instead, so it still shows
    const BACKUP = { crowned: "cap", crested: "crown stripe", plumed: "eyebrow", eared: "brow ridge", tailed: "streaks", winged: "bars", legged: "speckles", masked: "lores" };
    for (let k of PART_RULES[part] || []) {
      const top = TOPS[k] || k === "@crest" || k === "@plume" || k === "@ears";
      if ((top && o.tops.length) || (k === "face mask" && o.clan !== "🐤")) { const b2 = BACKUP[part]; if (b2) add(b2, part); continue; }
      add(k, part); }
    // and the body-part word nudges the shade a touch, so two names never come out identical
    const hp = hash("p:" + part); o.body = [Math.max(.2, Math.min(.95, o.body[0] + ((hp % 7) - 3) * .007)), o.body[1], (o.body[2] + ((hp >> 5) % 7) - 3 + 360) % 360];
    // one more trait sometimes, for variety
    if (r() < .25) add(pickW(r, EXTRAS), "");
    if (o.tops.length > 1) o.tops = o.tops.slice(0, 1);
    if (o.clan !== "🐤" && o.marks.includes("face mask")) { o.marks = o.marks.filter(m => m !== "face mask"); for (let k = 0; k < why.length; k++) if (/face mask$/.test(why[k])) why[k] = why[k].replace(/face mask$/, "already masked (eye patch)"); }
    o.why = why; return o;
  }

  // ---------- drawing ----------
  const segs = {}; const seg = em => segs[em] || (segs[em] = segment(em));
  const BODYPART = { "🐤": "body", "🐦": "body", "🐧": "head" };
  function render(o) {
    const sg = seg(o.clan), { img, parts, geo } = sg, [x0, y0, x1, y1] = img.box, S2 = S;
    const G = { x0, y0, x1, y1, w: x1 - x0, h: y1 - y0, E: geo.eye, B: geo.beakBase };
    if (parts.patch && parts.patch.length) { let a = 999, b = 0, c = 999, d = 0; for (const p of parts.patch) { const x = p % S2, y = Math.floor(p / S2); a = Math.min(a, x); b = Math.max(b, x); c = Math.min(c, y); d = Math.max(d, y); } G.P = { x0: a, x1: b, y0: c, y1: d }; }
    const out = new ImageData(new Uint8ClampedArray(img.d.data), S2, S2), D = out.data, r = rng(hash(o.name + "#draw"));
    const em = o.clan, body = o.body, bp = parts[BODYPART[em]];
    const bodyT = em === "🐧" ? [Math.min(.36, body[0] * .45), body[1] * .55, body[2]] : body;
    paint(D, bp, bodyT);
    if (em === "🐧") paint(D, parts.spot, o.spotCol || [Math.min(.85, Math.max(.6, body[0] + .05)), Math.max(.1, Math.min(.18, body[1] * 1.2)), body[2]]);
    const mh = o.markHue == null ? (body[2] + 40) % 360 : o.markHue, mdk = o.markDark == null ? mh % 2 : o.markDark;
    const accent = [Math.max(.45, Math.min(.85, body[0] + (mdk ? -.18 : .14))), Math.min(.18, Math.max(.1, body[1] * 1.15)), mh];
    const tones = { dark: [.27, .02, body[2]], white: [.95, .01, 240], skin: [.62, .19, 25 + r() * 20], blush: [.74, .13, 15], accent: [.7, .16, 50 + r() * 20], body: [body[0] - .06, body[1], body[2]], light: [.9, .1, 98],
      orange: [.72, .13, 60], red: [.58, .2, 28], horn: [.55, .05, 60], pale: [.9, .02, 90] };
    // markings
    const paintable = [...bp, ...(parts.face || []), ...(parts.patch || [])];
    for (const k of o.marks) {
      if (k === "face mask" && em !== "🐤") continue;
      if (k === "iridescence") { // shimmering colour across the head
        const sel = bp.filter(() => true), wt = []; for (const p of sel) { const x = p % S2, y = Math.floor(p / S2); wt.push(.55 + .45 * Math.sin((x + y) * .12)); }
        paint(D, sel.filter((p, i) => wt[i] > .7), [bodyT[0], Math.min(.2, bodyT[1] + .06), (bodyT[2] + 70) % 360], wt.filter(w => w > .7).map(w => (w - .7) * 2.5)); continue; }
      const m = document.createElement("canvas"); m.width = m.height = S2; const mx = m.getContext("2d"); mx.fillStyle = mx.strokeStyle = "#000";
      MARKS[k](mx, r, G);
      const md = mx.getImageData(0, 0, S2, S2).data, sel = [], wt = [];
      // soft edges (Safari ignores canvas blur filters, so blur the mask ourselves)
      const SOFT = { "face mask": .14, mottled: .45, "bare face": .5, "black hood": .25, "cheek patch": .2, "white cheeks": .25, throat: .2, nape: .25, cap: .2, bib: .25, "facial disc": .3, "two-tone": .3, lores: .3, forehead: .3 };
      if (SOFT[k]) blurAlpha(md, S2, Math.max(1, Math.round(G.E.r * SOFT[k])));

      for (const p of (k === "face mask" && parts.patch ? bp : ["face mask", "black hood", "eye stripe", "eye ring", "eye crescent", "eye wattle", "bare face", "facial disc", "eyelashes", "white cheeks"].includes(k) ? paintable : bp)) { const a = md[p * 4 + 3] / 255; if (a > .02) { sel.push(p); wt.push(a * .95); } }
      paint(D, sel, MARK_TONE[k] ? tones[MARK_TONE[k]] : accent, wt);
    }
    if (o.beakTint && !o.beakCol) { const t = o.beakTint; paint(D, parts.beakTop, t); paint(D, parts.beakBottom, [Math.max(.2, t[0] - .1), t[1], t[2]]); }
    if (o.beakCol) { paint(D, parts.beakTop, o.beakCol); paint(D, parts.beakBottom, [o.beakCol[0] - .12, o.beakCol[1], o.beakCol[2]]); }
    // ---- beak: reshape the emoji's own beak. Nothing changes at the base; the change grows toward the tip ----
    let beakLayer = null, BW = null;
    if (o.beak && WARPS[o.beak]) {
      const spec = WARPS[o.beak], bx = geo.beakBase.x, by = geo.beakBase.y;
      if (spec.paint) spec.paint(D, parts, r);                       // e.g. toucan colours, before reshaping
      const top = new Uint8Array(S2 * S2), bot = new Uint8Array(S2 * S2);
      parts.beakTop.forEach(p => top[p] = 1); parts.beakBottom.forEach(p => bot[p] = 1);
      const both = new Uint8Array(S2 * S2); for (let p = 0; p < S2 * S2; p++) both[p] = top[p] | bot[p];
      let xmin = 999; for (const p of [...parts.beakTop, ...parts.beakBottom]) xmin = Math.min(xmin, p % S2);
      const L = bx - xmin, src = new Uint8ClampedArray(D);
      for (const p of [...parts.beakTop, ...parts.beakBottom]) D[p * 4 + 3] = 0;    // the reshaped beak replaces it
      const W = S2 + PAD * 2; beakLayer = new ImageData(W, W); const O = beakLayer.data;
      // smooth sample of the original beak (only beak pixels count)
      const samp = (xs, ys, mask) => { const x0 = Math.floor(xs), y0 = Math.floor(ys), fx = xs - x0, fy = ys - y0; let r0 = 0, g0 = 0, b0 = 0, a0 = 0;
        for (const [dx, dy, w] of [[0, 0, (1 - fx) * (1 - fy)], [1, 0, fx * (1 - fy)], [0, 1, (1 - fx) * fy], [1, 1, fx * fy]]) { const x = x0 + dx, y = y0 + dy; if (x < 0 || y < 0 || x >= S2 || y >= S2) continue; const p = y * S2 + x; if (!mask[p]) continue;
          const a = src[p * 4 + 3] / 255 * w; r0 += src[p * 4] * a; g0 += src[p * 4 + 1] * a; b0 += src[p * 4 + 2] * a; a0 += a; }
        return a0 > 0 ? [r0 / a0, g0 / a0, b0 / a0, a0] : null; };
      // the mouth line: average bottom edge of the upper half, column by column
      let crease = by; { const lowest = new Map(); for (const p of parts.beakTop) { const x = p % S2, y = Math.floor(p / S2); if (!lowest.has(x) || y > lowest.get(x)) lowest.set(x, y); }
        if (lowest.size) { let sum = 0; for (const v of lowest.values()) sum += v; crease = sum / lowest.size + .5; } }
      let botH = 1; for (const p of parts.beakBottom) botH = Math.max(botH, Math.floor(p / S2) - crease);
      const k = spec.k || 1, len = L * k, sh = Math.round((spec.shift || 0) * L);   // thick beaks slide back into the face
      // where the face starts on each row; a slid-back beak tucks under the face along this curve instead of a straight cut
      const faceLeft = new Int16Array(S2).fill(9999), isB = new Uint8Array(S2 * S2);
      for (const p of [...parts.beakTop, ...parts.beakBottom]) isB[p] = 1;
      for (let y = 0; y < S2; y++) for (let x = 0; x < S2; x++) { const p = y * S2 + x; if (!isB[p] && src[p * 4 + 3] > 160) { faceLeft[y] = x; break; } }
      const tuck = Math.max(2, sh * .55);
      for (let yy = Math.floor(by - L * 2.2); yy <= by + L * 2.2; yy++) for (let xx = Math.floor(bx - len - 4); xx <= bx; xx++) {
        // the first quarter of the beak is left exactly as the emoji draws it; stretching and reshaping ease in after that
        const d = bx - xx, A = L * .25; if (d < 0) continue;
        const ds = d <= A ? d : A + (d - A) * (L - A) / Math.max(1, len - A);
        const t = ds / L; if (t > 1.03) continue;
        const ease = spec.shift ? Math.min(1, t / .3) : Math.min(1, Math.max(0, (t - .2) / .35)), blend = ease * ease * (3 - 2 * ease);
        const xs = bx - ds, best = [];
        // one piece unless the halves bend apart (crossed); then each half on its own, and the whole beak fills any hairline gap
        // crossed: the upper half curving down, and a flipped copy of it curving up underneath (two halves that cross)
        const passes = spec.crossed ? [[top, spec.bendTop, false], [top, spec.bendBottom, true]] : [[both, spec.bend, false]];
        for (const [mask, bend, flip] of passes) {
          const sv = 1 + ((spec.s ? spec.s(t) : 1) - 1) * blend, bd = bend ? bend(t) * L * blend : 0, ys0 = by + (yy - bd - by) / sv;
          const ys = flip ? 2 * crease - ys0 : ys0;
          // parrots: the lower half stops short with a rounded end, so the hooked top hangs over it
          let m = mask; if (spec.cutBottom && !flip && ys > crease) { const u = Math.min(1, (ys - crease) / botH); if (t > spec.cutBottom * Math.sqrt(1 - u * u)) m = top; }
          const c = samp(xs, ys, m); if (c) { if (flip) { c[0] *= .82; c[1] *= .82; c[2] *= .82; } best.push(c); }
        }
        if (!best.length) continue;
        // where top and bottom overlap (crossed beaks), the top one shows
        const c = best[0], ox = xx + sh, q = ((yy + PAD) * W + (ox + PAD)) * 4; if (q < 0 || q >= O.length) continue;
        let fa = 1;
        if (sh && yy >= 0 && yy < S2 && faceLeft[yy] < 9999) { const lim = faceLeft[yy] + tuck - ox; if (lim < 0) continue; if (lim < 3) fa = lim / 3; }
        O[q] = c[0]; O[q + 1] = c[1]; O[q + 2] = c[2]; O[q + 3] = Math.min(255, c[3] * 255 * fa);
      }
      if (spec.after) spec.after(O, W, bx + PAD, by + PAD, len);    // e.g. dark tips
      // where the old beak was but the new one isn't, close the face over the gap using the feathers right next to it
      const isBeak = new Uint8Array(S2 * S2); for (const p of [...parts.beakTop, ...parts.beakBottom]) isBeak[p] = 1;
      // the head's own round outline (from its top, bottom and back), so the fill only rebuilds the head, never the air around the beak
      let hy0 = 999, hy1 = 0, hx1 = 0; for (let p = 0; p < S2 * S2; p++) if (!isBeak[p] && src[p * 4 + 3] > 200) { const x = p % S2, y = Math.floor(p / S2); hy0 = Math.min(hy0, y); hy1 = Math.max(hy1, y); hx1 = Math.max(hx1, x); }
      const hry = (hy1 - hy0) / 2, hcy = (hy0 + hy1) / 2, hrx = hry * 1.02, hcx = hx1 - hrx;
      const inHead = (x, y) => ((x - hcx) / hrx) ** 2 + ((y - hcy) / hry) ** 2 <= .97;
      for (let pass = 0; pass < 3; pass++) for (const p of [...parts.beakTop, ...parts.beakBottom]) {
        const x = p % S2, y = Math.floor(p / S2); if (!inHead(x, y) || D[p * 4 + 3] > 0) continue;
        const q = ((y + PAD) * W + (x + PAD)) * 4; if (O[q + 3] > 200) continue;          // the new beak covers it
        // nearest face pixel to the right or above
        let src2 = -1; for (let k = 1; k <= 10 && src2 < 0; k++) for (const n of [p + k, p - k * S2, p + k - k * S2]) if (n >= 0 && n < S2 * S2 && !isBeak[n] && D[n * 4 + 3] > 200) { src2 = n; break; }
        if (src2 < 0) for (const n of [p + 1, p - S2, p - 1]) if (n >= 0 && isBeak[n] && D[n * 4 + 3] > 200) { src2 = n; break; }   // grow from pixels filled this pass
        if (src2 < 0) continue;
        D[p * 4] = D[src2 * 4]; D[p * 4 + 1] = D[src2 * 4 + 1]; D[p * 4 + 2] = D[src2 * 4 + 2]; D[p * 4 + 3] = 255;
      }
      // top edge of the reshaped beak (so a hornbill horn can sit right on it)
      let topY = 999, topX = bx + sh; for (let q = 3; q < O.length; q += 4) if (O[q] > 128) { const y = Math.floor((q >> 2) / W) - PAD; if (y < topY) { topY = y; topX = ((q >> 2) % W) - PAD; } }
      BW = { bx: bx + sh, by, L, len, spec, topY };
    }
    // compose: feathers behind, then the bird, then beak and face features on top
    const c = document.createElement("canvas"); c.width = c.height = S2 + PAD * 2; const cx = c.getContext("2d"); cx.translate(PAD, PAD);
    for (const k of o.tops) { const T = TOPS[k]; shade(cx, G, tones[T.tone] || tones.body, x => T.draw(x, G), o.tipped ? accent : T.tip ? tones[T.tip] || [.2, .02, 260] : null, { tipTop: T.tipTop, tipBottom: T.tipBottom, band: T.band ? tones[T.band] : null, shafts: T.shafts ? x => T.shafts(x, G) : null }); }
    if (BW && BW.spec.pouch) glossy(cx, [.7, .15, 50], x => { x.beginPath(); x.moveTo(BW.bx, BW.by + 2); x.quadraticCurveTo(BW.bx - BW.len * .5, BW.by + BW.L * 1.1, BW.bx - BW.len * .95, BW.by + 3); x.lineTo(BW.bx, BW.by + 2); x.fill(); }, G, BW.bx - BW.len * .4, BW.by + BW.L * .4, BW.L * .7);
    const e = document.createElement("canvas"); e.width = e.height = S2; e.getContext("2d").putImageData(out, 0, 0); cx.drawImage(e, 0, 0);
    if (beakLayer) { const bc = document.createElement("canvas"); bc.width = bc.height = beakLayer.width; bc.getContext("2d").putImageData(beakLayer, 0, 0); cx.drawImage(bc, -PAD, -PAD); }
    for (const k of o.face) FACE[k](cx, G, [.56, .19, 22]);
    return c;
  }
  // pad so tall crests / long beaks fit, then return an image URL
  function draw(name, over) {
    const o = Object.assign(describe(name), over || {});
    const c = render(o);
    return { url: c.toDataURL(), o };
  }
  __bk = { draw, describe, render, seg, PAD, WARPS };
})();
