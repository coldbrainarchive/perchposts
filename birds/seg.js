// Part finding (site version): reads the saved base images in BASE, not the device emoji font.
// Part finding v2: eye first, then the white patch grown out from the eye, beak (split top/bottom),
// penguin face/spot, and EVERYTHING left over is the body/head, so no pixel keeps a stray original colour.
const S = 160;
function render(em) {
  const c = document.createElement("canvas"); c.width = c.height = S;
  const x = c.getContext("2d", { willReadFrequently: true });
  x.drawImage(BASE[em], 0, 0, S, S);   // the saved Apple emoji (same pixels on every device)
  const d = x.getImageData(0, 0, S, S);
  let x0 = S, y0 = S, x1 = 0, y1 = 0;
  for (let y = 0; y < S; y++) for (let k = 0; k < S; k++) if (d.data[(y * S + k) * 4 + 3] > 20) { x0 = Math.min(x0, k); x1 = Math.max(x1, k); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
  return { c, x, d, box: [x0, y0, x1, y1] };
}
const lab = (r, g, b) => { const f = v => { v /= 255; return v > .04045 ? Math.pow((v + .055) / 1.055, 2.4) : v / 12.92; };
  const R = f(r), G = f(g), B = f(b), X = (R * .4124 + G * .3576 + B * .1805) / .95047, Y = R * .2126 + G * .7152 + B * .0722, Z = (R * .0193 + G * .1192 + B * .9505) / 1.08883;
  const h = t => t > .008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116; return [116 * h(Y) - 16, 500 * (h(X) - h(Y)), 200 * (h(Y) - h(Z))]; };
const chroma = c => Math.hypot(c[1], c[2]);
// grow a region from seeds while ok(pixel, neighbour) holds
function grow(img, seeds, ok, taken) {
  const D = img.d.data, L = img.lab, seen = new Uint8Array(S * S), out = [], st = [];
  for (const s of seeds) if (s >= 0 && !taken[s] && D[s * 4 + 3] > 30 && ok(L[s], L[s])) { seen[s] = 1; st.push(s); }
  while (st.length) {
    const p = st.pop(); out.push(p); const px = p % S;
    for (const q of [px > 0 ? p - 1 : -1, px < S - 1 ? p + 1 : -1, p - S, p + S]) {
      if (q < 0 || q >= S * S || seen[q] || taken[q] || D[q * 4 + 3] < 30) continue;
      if (ok(L[q], L[p])) { seen[q] = 1; st.push(q); }
    }
  }
  for (const p of out) taken[p] = 1;
  return out;
}
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
// where things are on each emoji (fractions of its box)
const LAYOUT = {
  "🐤": { eye: [.45, .36], beak: [[.08, .62], [.14, .66], [.12, .56]], beakMaxX: .32, body: "body" },
  "🐦": { eye: [.47, .33], beak: [[.07, .64], [.12, .58], [.12, .7]], beakMaxX: .33, patch: true, body: "body" },
  "🐧": { eye: [.43, .36], beak: [[.12, .64], [.16, .58]], beakMaxX: .31, face: [[.42, .75], [.42, .55]], spot: [[.84, .3]], body: "head" },
};
function segment(em) {
  const img = render(em); img.lab = []; const D = img.d.data;
  for (let p = 0; p < S * S; p++) img.lab[p] = lab(D[p * 4], D[p * 4 + 1], D[p * 4 + 2]);
  const [x0, y0, x1, y1] = img.box, w = x1 - x0, h = y1 - y0, at = (fx, fy) => Math.round(y0 + fy * h) * S + Math.round(x0 + fx * w);
  const lay = LAYOUT[em], taken = new Uint8Array(S * S), parts = {};
  // 1. eye: darkest pixel near the anchor, then everything dark connected to it
  const ec = at(...lay.eye); let best = ec, bl = 999;
  for (let dy = -14; dy <= 14; dy++) for (let dx = -14; dx <= 14; dx++) { const p = ec + dy * S + dx; if (img.lab[p] && D[p * 4 + 3] > 200 && img.lab[p][0] < bl) { bl = img.lab[p][0]; best = p; } }
  parts.eye = grow(img, [best], (c, prev) => c[0] < 42 && Math.abs(c[0] - prev[0]) < 18, taken);
  // eye centre / size
  let ex = 0, ey = 0; for (const p of parts.eye) { ex += p % S; ey += Math.floor(p / S); } ex /= parts.eye.length || 1; ey /= parts.eye.length || 1;
  const er = Math.sqrt((parts.eye.length || 1) / Math.PI);
  for (let y = Math.floor(ey - er - 1); y <= ey + er + 1; y++) for (let x = Math.floor(ex - er - 1); x <= ex + er + 1; x++) {
    const p = y * S + x; if (!taken[p] && Math.hypot(x - ex, y - ey) <= er * .95 && D[p * 4 + 3] > 8) { taken[p] = 1; parts.eye.push(p); } }
  // 2. songbird: white patch = bright, nearly colourless pixels connected to the ring around the eye
  if (lay.patch) {
    const ring = []; for (let a = 0; a < 64; a++) for (const k of [1.4, 2.4, 3.4]) { const rx = Math.round(ex + Math.cos(a / 64 * 6.283) * (er + k)), ry = Math.round(ey + Math.sin(a / 64 * 6.283) * (er + k)); ring.push(ry * S + rx); }
    const body0 = img.lab[at(.8, .6)], bodyC = chroma(body0);
    // patch pixels are much less coloured than the head: compare chroma (and hue direction) with the head colour
    parts.patch = grow(img, ring, (c, prev) => c[0] > 52 && chroma(c) < Math.max(4, bodyC * .45) && Math.abs(c[0] - prev[0]) < 9, taken);
  }
  // 3. penguin face (white) and the coloured spot
  if (lay.face) parts.face = grow(img, lay.face.map(f => at(...f)), (c, prev) => c[0] > 45 && chroma(c) < 12 && Math.abs(c[0] - prev[0]) < 14, taken);
  if (lay.spot) { const s0 = img.lab[at(...lay.spot[0])]; parts.spot = grow(img, lay.spot.map(f => at(...f)), (c, prev) => Math.hypot(c[1] - s0[1], c[2] - s0[2]) < 32 && dist(c, prev) < 14, taken); }
  // 4. beak: grown from the tip area by colour, then split into top / bottom by brightness
  const b0 = img.lab[at(...lay.beak[0])];
  const bx = x0 + lay.beakMaxX * w;
  // a pixel only counts as beak if its colour (ignoring light/dark) is nearer the beak's than the head's
  const headRef = img.lab[at(.78, .6)], abd = (c, r) => Math.hypot(c[1] - r[1], c[2] - r[2]);
  const beakish = c => abd(c, b0) < abd(c, headRef) * (lay.body === "head" ? 1 : .9);
  const inBeak = p => (p % S) <= bx;
  const beakTaken = taken.slice(); for (let p = 0; p < S * S; p++) if (!inBeak(p)) beakTaken[p] = 1;   // the fill can't leave the beak area
  const beak = grow(img, lay.beak.map(f => at(...f)), (c, prev) => beakish(c) && Math.hypot(c[1] - b0[1], c[2] - b0[2]) < (em === "🐦" ? 9 : 22) && dist(c, prev) < 13 && (em !== "🐦" || c[0] > 30), beakTaken);
  for (const p of beak) taken[p] = 1;
  // edge pixels of the beak the fill missed (anti-aliasing at the tip and lower edge): unclaimed pixels touching the beak
  for (let pass = 0; pass < 5; pass++) {
    const add = [];
    for (const p of beak) for (const q of [p - 1, p + 1, p - S, p + S]) if (q >= 0 && q < S * S && !taken[q] && D[q * 4 + 3] > 8 && inBeak(q) && (D[q * 4 + 3] < 200 || beakish(img.lab[q]))) { taken[q] = 1; add.push(q); }
    beak.push(...add);
  }
  if (beak.length) {
    // the line between top and bottom halves: the darkest-to-lightest jump, found by splitting at the median brightness
    const Ls = beak.map(p => img.lab[p][0]).sort((a, b) => a - b), mid = (Ls[Math.floor(Ls.length * .3)] + Ls[Math.floor(Ls.length * .7)]) / 2;
    // first guess by brightness, then smooth it (majority of nearby beak pixels) so each half is one solid piece
    const lab0 = new Int8Array(S * S).fill(-1); for (const p of beak) lab0[p] = img.lab[p][0] >= mid ? 1 : 0;
    for (let pass = 0; pass < 3; pass++) {
      const nxt = lab0.slice();
      for (const p of beak) { let t = 0, n = 0; const px = p % S;
        for (let dy = -3; dy <= 3; dy++) for (let dx = -3; dx <= 3; dx++) { if (px + dx < 0 || px + dx >= S) continue; const q = p + dy * S + dx; if (q >= 0 && q < S * S && lab0[q] >= 0) { t += lab0[q]; n++; } }
        nxt[p] = t * 2 > n ? 1 : 0; }
      lab0.set(nxt);
    }
    parts.beakTop = beak.filter(p => lab0[p] === 1); parts.beakBottom = beak.filter(p => lab0[p] === 0);
  }
  // where the eye and beak base really are (canvas pixels), so face traits line up exactly
  let bmx = -1, bys = 0, bn = 0; for (const p of beak) { const x = p % S; if (x > bmx) bmx = x; }
  for (const p of beak) if (p % S >= bmx - 3) { bys += Math.floor(p / S); bn++; }
  const geo = { eye: { x: ex, y: ey, r: er }, beakBase: { x: bmx, y: bn ? bys / bn : ey + er * 3 } };
  // 5. everything else is the body/head, highlights included
  const rest = []; for (let p = 0; p < S * S; p++) if (!taken[p] && D[p * 4 + 3] > 8) rest.push(p);
  parts[lay.body] = rest; parts.beakTop = parts.beakTop || []; parts.beakBottom = parts.beakBottom || [];
  return { img, parts, geo };
}
