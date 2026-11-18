// Site glue for the bird avatars. The patch script wraps seg.js + scale.js + birdkit.js into mkKit(SC, BASE) and adds this.
// Every device draws from the same saved base images, so a username gives the same bird everywhere.
// Tags are drawn at 2x (TAG_SC) and big birds (profile cards, Your Nest, the sign-up nest) at 3x (BIG_SC); the parts are
// always found on the 160px emoji, so both sizes are the same bird. The 3x images only load when a big bird is wanted.
//   _ppKit.get(name, clanEmoji, kind) kind "t" = tag bird, "f" = full big bird (the default)
//        -> null while drawing, then { f: full image URL, t: tag image URL (kind "t"), g: outline growth, fail }
//   _ppKit.sub(name, clanEmoji, fn, kind) -> call fn when that bird is ready; returns an unsubscribe function
//   _ppKit.tagCol(name) -> the username tag colour, matched to the bird
//   _ppKit.ready (base images loaded), _ppKit.eye(clanEmoji) -> eye position in the big bird, for the sign-up nest
const VER = 2, TAG_DISP = 16, TAG_OUTLINE = 1, TAG_SC = 2, BIG_SC = 3;
const BASE_FILES = [["🐤", "chick"], ["🐦", "songbird"], ["🐧", "penguin"]];
const BASE2 = {}, BASE3 = {}, kitT = mkKit(TAG_SC, BASE2), kitF = mkKit(BIG_SC, BASE3);
const loadSet = (into, suffix) => Promise.all(BASE_FILES.map(([em, f]) => new Promise((res, rej) => {
  const im = new Image(); im.onload = () => { into[em] = im; res(); }; im.onerror = rej; im.src = `/birds/${f}${suffix}.png?v=${VER}`;
})));
let ok = false, bigKit = null, bigLoad = null;
const ready = Promise.all([loadSet(BASE1, ""), loadSet(BASE2, "@2x")]).then(() => { ok = true; pump(); setTimeout(() => big(), 1500); }).catch(() => {
  // base images missing: every bird stays the plain emoji
  for (const r of cache.values()) r.done = r.fail = true;
  for (const s of subs.values()) s.forEach(f => f());
});
// the 3x images, the first time a big bird is wanted (if they can't load, big birds use the 2x drawing)
const big = () => bigLoad || (bigLoad = loadSet(BASE3, "@3x").then(() => bigKit = kitF, () => bigKit = kitT));

const cache = new Map(), subs = new Map(), queue = [];
let running = false;
const key = (n, c, kind) => (kind === "t" ? "t" : "f") + "|" + c + "|" + n;
function get(n, c, kind) {
  const k = key(n, c, kind), r = cache.get(k);
  if (r) return r.done ? r : null;
  cache.set(k, { done: false }); (kind === "t" ? queue.push : queue.unshift).call(queue, [n, c, kind === "t" ? "t" : "f"]); pump(); return null; // big birds first
}
function sub(n, c, fn, kind) { const k = key(n, c, kind); let s = subs.get(k); if (!s) subs.set(k, s = new Set()); s.add(fn); return () => s.delete(fn); }
function pump() { if (running || !ok || !queue.length) return; running = true; setTimeout(step, 0); }
const toUrl = cv => new Promise(res => cv.toBlob(b => res(b ? URL.createObjectURL(b) : cv.toDataURL()), "image/png"));
async function step() {
  const t0 = performance.now();
  while (queue.length && performance.now() - t0 < 12) {          // a little at a time so scrolling stays smooth
    const [n, c, kind] = queue.shift(), k = key(n, c, kind), r = cache.get(k);
    try { if (kind === "f" && c !== "A") await big(); Object.assign(r, await (c === "A" ? makeAdmin() : kind === "t" ? makeTag(n, c) : makeBig(n, c))); } catch (e) { r.fail = true; }
    r.done = true; (subs.get(k) || []).forEach(f => f());
  }
  running = false; pump();
}

// the big bird: the whole bird at 3x (profile cards, Your Nest, the sign-up nest)
function makeBig(n, c) { const o = bigKit.describe(n); o.clan = c; return toUrl(bigKit.render(o)).then(f => ({ f })); }
// the tag bird at 2x: cropped to emoji size, 1px dark outline
const TAG_SIDE = Math.round(160 * TAG_SC * .8 * 1.08);
function makeTag(n, c) {
  const K = kitT, o = K.describe(n); o.clan = c;
  const full = K.render(o), PAD = K.PAD, b = K.seg(c).img.box;
  const side = TAG_SIDE, cx = PAD + (b[0] + b[2]) / 2, cy = PAD + (b[1] + b[3]) / 2;
  const crop = document.createElement("canvas"); crop.width = crop.height = side; const x = crop.getContext("2d");
  x.drawImage(full, cx - side / 2, cy - side / 2, side, side, 0, 0, side, side);
  const fd = Math.round(side * .07); x.globalCompositeOperation = "destination-out";
  const edge = (x0, y0, x1, y1, rx, ry, rw, rh) => { const g = x.createLinearGradient(x0, y0, x1, y1); g.addColorStop(0, "#000"); g.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = g; x.fillRect(rx, ry, rw, rh); };
  edge(0, 0, fd, 0, 0, 0, fd, side); edge(side, 0, side - fd, 0, side - fd, 0, fd, side); edge(0, 0, 0, fd, 0, 0, side, fd); edge(0, side, 0, side - fd, 0, side - fd, side, fd);
  const { cv: tag, g } = outlined(crop);
  return Promise.all([toUrl(full), toUrl(tag)]).then(([f, t]) => ({ f, t, g }));
}
// 1px (at tag size) dark outline around a square image. Faint or hair-thin bits (bristles, soft fades, crest tips)
// are left out of the outline's shape, so it stays a clean, even line instead of smudging around them.
function outlined(src) {
  const side = src.width, k = side / TAG_DISP, rr = TAG_OUTLINE * k, E = 3 * TAG_SC, pad = Math.ceil(rr) + 1, W = side + pad * 2;
  const a = src.getContext("2d").getImageData(0, 0, side, side).data;
  let m = new Uint8Array(W * W);
  for (let y = 0; y < side; y++) for (let x = 0; x < side; x++) m[(y + pad) * W + x + pad] = a[(y * side + x) * 4 + 3] > 140 ? 1 : 0;
  // shrink the shape by E px (drops anything thinner than ~2E), then the outline is grown back by rr + E
  for (const [dx, dy] of [[1, 0], [0, 1]]) {
    const o = new Uint8Array(W * W);
    for (let y = 0; y < W; y++) for (let x = 0; x < W; x++) { let v = 1;
      for (let t = -E; t <= E && v; t++) { const xx = x + dx * t, yy = y + dy * t; v = xx >= 0 && yy >= 0 && xx < W && yy < W ? m[yy * W + xx] : 0; }
      o[y * W + x] = v; }
    m = o;
  }
  const sil = document.createElement("canvas"); sil.width = sil.height = W; const sx = sil.getContext("2d"), id = sx.createImageData(W, W);
  for (let p = 0; p < W * W; p++) if (m[p]) { id.data[p * 4] = 11; id.data[p * 4 + 1] = 12; id.data[p * 4 + 2] = 16; id.data[p * 4 + 3] = 255; }
  sx.putImageData(id, 0, 0);
  const cv = document.createElement("canvas"); cv.width = cv.height = W; const cx = cv.getContext("2d"), R = rr + E;
  cx.drawImage(sil, 0, 0);
  for (let i = 0; i < 48; i++) for (const f of [.35, .7, 1]) cx.drawImage(sil, Math.cos(i / 48 * 6.283) * R * f, Math.sin(i / 48 * 6.283) * R * f);
  cx.drawImage(src, pad, pad);
  return { cv, g: pad / side };   // g: outline growth per side, as a share of the image size
}
// the admin bird for tags: same outline, made once from /admin-bird.png
function makeAdmin() {
  return new Promise((res, rej) => { const im = new Image(); im.onload = () => {
    const side = TAG_SIDE, c = document.createElement("canvas"); c.width = c.height = side;
    const s = Math.min(side / im.width, side / im.height), w = im.width * s, h = im.height * s;
    c.getContext("2d").drawImage(im, (side - w) / 2, (side - h) / 2, w, h);
    const { cv, g } = outlined(c); toUrl(cv).then(t => res({ t, f: t, g })); }; im.onerror = rej; im.src = "/admin-bird.png"; });
}

// where the eye sits in a full image of that clan (the sign-up nest puts an eyelid there for blinking)
function eye(c) { const K = bigKit || kitT, s = K.seg(c), g = s.geo.eye, P = K.PAD; return { x: g.x + P, y: g.y + P, r: g.r, W: s.img.d.width + P * 2 }; }

// tag colour: the bird's body colour (grey/white/black birds use their marking colour), never mod purple
function okToRgb(L, C, h) { const a = C * Math.cos(h * Math.PI / 180), b = C * Math.sin(h * Math.PI / 180);
  const l = (L + .3963377774 * a + .2158037573 * b) ** 3, m = (L - .1055613458 * a - .0638541728 * b) ** 3, s = (L - .0894841775 * a - 1.291485548 * b) ** 3;
  const g = v => { v = Math.max(0, Math.min(1, v)); return v <= .0031308 ? 12.92 * v : 1.055 * v ** (1 / 2.4) - .055; };
  return [g(4.0767416621 * l - 3.3077115913 * m + .2309699292 * s), g(-1.2684380046 * l + 2.6097574011 * m - .3413193965 * s), g(-.0041960863 * l - .7034186147 * m + 1.707614701 * s)]; }
function hueOf([r, g, b]) { const M = Math.max(r, g, b), m = Math.min(r, g, b), d = M - m; if (!d) return 0;
  const h = M === r ? ((g - b) / d) % 6 : M === g ? (b - r) / d + 2 : (r - g) / d + 4; return (h * 60 + 360) % 360; }
const fixPurple = h => h >= 232 && h <= 328 ? (h < 280 ? 218 : 336) : h;
const cols = new Map();
function tagCol(n) {
  let v = cols.get(n); if (v) return v;
  const o = kitT.describe(n), h = o.body[1] < .05 ? hueOf(okToRgb(.7, .12, o.markHue)) : hueOf(okToRgb(...o.body));
  v = `hsl(${Math.round(fixPurple(h))}, 72%, 68%)`; cols.set(n, v); return v;
}
