// Sharper birds: the parts are found on the 160px emoji exactly as before (seg1, from seg.js), then their outlines are
// scaled up smoothly onto a bigger copy of the same emoji (BASE, SC times the size). So every bird keeps its exact look,
// just drawn with SC times the pixels and soft edges between parts. With SC = 1 this is the old part finder unchanged.
const S = 160 * SC;
function segment(em) {
  const r = seg1(em); if (SC === 1) return r;
  const S1 = 160, c = document.createElement("canvas"); c.width = c.height = S; const x = c.getContext("2d", { willReadFrequently: true });
  x.drawImage(BASE[em], 0, 0, S, S); const d = x.getImageData(0, 0, S, S), A = d.data;
  let x0 = S, y0 = S, x1 = 0, y1 = 0; for (let y = 0; y < S; y++) for (let k = 0; k < S; k++) if (A[(y * S + k) * 4 + 3] > 20) { x0 = Math.min(x0, k); x1 = Math.max(x1, k); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
  const names = Object.keys(r.parts).filter(k => r.parts[k] && r.parts[k].length), lab1 = new Int8Array(S1 * S1).fill(-1);
  names.forEach((k, i) => { for (const p of r.parts[k]) lab1[p] = i; });
  const masks = names.map(k => { const m = new Float32Array(S1 * S1); for (const p of r.parts[k]) m[p] = 1; return m; });
  const out = {}; names.forEach(k => out[k] = []);
  const cl = v => v < 0 ? 0 : v > S1 - 1 ? S1 - 1 : v;
  for (let y = 0; y < S; y++) for (let xx = 0; xx < S; xx++) { const p = y * S + xx; if (A[p * 4 + 3] <= 8) continue;
    // which part this pixel belongs to: the strongest of the parts' smoothly scaled-up outlines
    const fx = (xx + .5) / SC - .5, fy = (y + .5) / SC - .5, ix = Math.floor(fx), iy = Math.floor(fy), tx = fx - ix, ty = fy - iy;
    const a0 = cl(ix), a1 = cl(ix + 1), b0 = cl(iy), b1 = cl(iy + 1);
    let best = -1, bv = .001;
    for (let i = 0; i < masks.length; i++) { const m = masks[i];
      const v = (m[b0 * S1 + a0] * (1 - tx) + m[b0 * S1 + a1] * tx) * (1 - ty) + (m[b1 * S1 + a0] * (1 - tx) + m[b1 * S1 + a1] * tx) * ty;
      if (v > bv) { bv = v; best = i; } }
    if (best < 0)   // a soft edge pixel the small emoji didn't have: the nearest part
      for (let rr = 1; rr <= 3 && best < 0; rr++) for (let dy = -rr; dy <= rr && best < 0; dy++) for (let dx = -rr; dx <= rr; dx++) { const q = cl(Math.round(fy) + dy) * S1 + cl(Math.round(fx) + dx); if (lab1[q] >= 0) { best = lab1[q]; break; } }
    if (best >= 0) out[names[best]].push(p); }
  const sc = v => (v + .5) * SC - .5;
  const geo = { eye: { x: sc(r.geo.eye.x), y: sc(r.geo.eye.y), r: r.geo.eye.r * SC }, beakBase: { x: sc(r.geo.beakBase.x), y: sc(r.geo.beakBase.y) } };
  out.beakTop = out.beakTop || []; out.beakBottom = out.beakBottom || [];
  return { img: { c, x, d, box: [x0, y0, x1, y1] }, parts: out, geo };
}
