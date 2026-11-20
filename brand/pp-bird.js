// Bird-globe logo drawn from a pose, so it can move like a real 3D head.
// pose: { th: head turn in degrees (0 = facing left, 180 = facing right), tilt: degrees, jaw: beak opening in degrees,
//         wink: 0..1 (1 = eye closed), look: [dx, dy] pupil offset }
(function (root) {
  const F = "#14151b", L = "#c084fc", CX = 56, CY = 50, R = 38, D = Math.PI / 180;
  const MERIDIANS = Array.from({ length: 12 }, (_, k) => 15 + 30 * k);   // evenly spaced all the way round
  // eye A is the one we see; eye B is the other side of the head (mirror about the beak axis)
  const EYE_LAT = Math.asin(15.2 / R), EYE_COS = Math.cos(EYE_LAT), EYE_A = Math.asin(-11.5 / (R * EYE_COS)) / D;
  const EYES = [{ lon: EYE_A, px: 0.28 }, { lon: -180 - EYE_A, px: -0.28 }];
  const BEAK_LAT = Math.asin(-6 / R);
  const f = n => Math.round(n * 100) / 100;

  // lines on the sides of the head (where the beak sits); hidden at rest, they fade in as the head turns
  const SIDE_MERIDIANS = [64.6, 88.1, 111.6, -64.6, -88.1, -111.6];
  function meridians(th) {
    let s = "";
    const extra = Math.abs(Math.sin(th * D));
    const one = (lam, op) => {
      const p = (lam + th) * D;
      if (Math.cos(p) <= 0.001 || op < 0.02) return "";  // behind the globe
      const rx = Math.abs(R * Math.sin(p)), o = op < 1 ? ` opacity="${f(op)}"` : "";
      return rx < 0.4 ? `<line x1="${CX}" y1="${CY - R}" x2="${CX}" y2="${CY + R}"${o}/>`
        : `<path d="M ${CX} ${CY - R} A ${f(rx)} ${R} 0 0 ${Math.sin(p) > 0 ? 1 : 0} ${CX} ${CY + R}"${o}/>`;
    };
    for (const lam of MERIDIANS) s += one(lam, 1);
    return s;
  }

  function eyes(pose) {
    let s = "";
    for (const e of EYES) {
      const p = (e.lon + pose.th) * D, c = Math.cos(p);
      if (c <= 0.04) continue;
      const x = CX + R * EYE_COS * Math.sin(p), y = CY - R * Math.sin(EYE_LAT);
      const rx = Math.max(8.5 * c, 1.2);
      if (pose.wink > 0.5) {
        s += `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rx + 2.1)}" ry="10.6" fill="${F}"/>` +
          `<path d="M ${f(x - 7.5 * c)} 33.5 Q ${f(x)} 41.5 ${f(x + 7.5 * c)} 33.5" fill="none" stroke="${L}" stroke-width="3.8" stroke-linecap="round"/>`;
        continue;
      }
      const lk = pose.look || [0, 0];
      const px = x + (e.px * 8.5 + lk[0]) * c, py = y - 0.28 * 8.5 + lk[1];
      s += `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rx)}" ry="8.5" fill="${F}" stroke="${L}" stroke-width="3.6"/>` +
        `<ellipse cx="${f(px)}" cy="${f(py)}" rx="${f(Math.max(2.55 * c, 0.6))}" ry="2.55" fill="${L}"/>`;
    }
    return s;
  }

  // ---- 3D beak: the drawn beak outline, lofted into a solid (oval slices) and rotated with the head ----
  const bz = (a, b, c, d, t) => { const u = 1 - t; return u * u * u * a + 3 * u * u * t * b + 3 * u * t * t * c + t * t * t * d; };
  const toFinal = (x, y) => [32 + (x - 32) * 1.3, 54 + (y - 54) * 1.3];
  const OUT = (() => {
    const segs = [[7.3, 59, 10, 51.5, 17, 44, 21.7, 43.1], [21.7, 43.1, 25.5, 42.4, 31, 49.5, 32.4, 54.5],
      [32.4, 54.5, 33.2, 58.6, 29.5, 63.8, 25, 64.9], [25, 64.9, 19, 64.6, 11.5, 61.2, 7.3, 59]];
    const pts = [];
    for (const g of segs) for (let k = 0; k < 24; k++) { const t = k / 24; pts.push(toFinal(bz(g[0], g[2], g[4], g[6], t), bz(g[1], g[3], g[5], g[7], t))); }
    return pts;
  })();
  const MOUTH = (() => { const p = []; for (let k = 0; k <= 16; k++) { const t = k / 16; p.push(toFinal(bz(7.6, 14, 23, 31.6, t), bz(59, 57, 55.8, 56.2, t))); } return p; })();
  const XMIN = Math.min(...OUT.map(p => p[0])), XMAX = Math.max(...OUT.map(p => p[0]));
  function slice(X) {                                 // top/bottom of the outline at x = X
    let lo = Infinity, hi = -Infinity;
    for (let i = 0; i < OUT.length; i++) {
      const a = OUT[i], b = OUT[(i + 1) % OUT.length];
      if ((a[0] - X) * (b[0] - X) > 0 || a[0] === b[0]) continue;
      const y = a[1] + (b[1] - a[1]) * (X - a[0]) / (b[0] - a[0]); lo = Math.min(lo, y); hi = Math.max(hi, y);
    }
    return lo === Infinity ? null : { yc: (lo + hi) / 2, h: (hi - lo) / 2 };
  }
  const STATIONS = []; for (let k = 1; k < 28; k++) { const X = XMIN + (XMAX - XMIN) * k / 28; const sl = slice(X); if (sl) STATIONS.push({ X, ...sl }); }
  const SEAM_X = 19.5;                                 // where the beak meets the head
  function hull(P) {
    P = P.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    const cr = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]), lo = [], hi = [];
    for (const p of P) { while (lo.length > 1 && cr(lo[lo.length - 2], lo[lo.length - 1], p) <= 0) lo.pop(); lo.push(p); }
    for (let i = P.length - 1; i >= 0; i--) { const p = P[i]; while (hi.length > 1 && cr(hi[hi.length - 2], hi[hi.length - 1], p) <= 0) hi.pop(); hi.push(p); }
    return lo.slice(0, -1).concat(hi.slice(0, -1));
  }
  function beak(pose) {
    const th = pose.th * D, side = Math.abs(Math.sin(th));
    const pitch = -24 * D * side;                      // beak dips a little as it points toward us
    const px = XMAX, py = 56;
    const place = (x, y, z) => {                       // beak space -> page (pitch, then turn with the head)
      const x1 = px + (x - px) * Math.cos(pitch) - (y - py) * Math.sin(pitch), y1 = py + (x - px) * Math.sin(pitch) + (y - py) * Math.cos(pitch);
      return [CX + (x1 - CX) * Math.cos(th) + z * Math.sin(th), y1, z * Math.cos(th) - (x1 - CX) * Math.sin(th)];
    };
    const W = 0.85, pts = [];
    for (const p of OUT) pts.push(place(p[0], p[1], 0));
    for (const st of STATIONS) for (let k = 0; k < 16; k++) { const a = k / 16 * 2 * Math.PI; pts.push(place(st.X, st.yc + st.h * Math.cos(a), st.h * W * Math.sin(a))); }
    const H = hull(pts.map(p => [p[0], p[1]]));
    const outline = "M " + H.map(p => `${f(p[0])} ${f(p[1])}`).join(" L ") + " Z";
    // mouth line on whichever side of the beak faces us
    const mouthOn = sgn => {
      const q = MOUTH.map(([x, y]) => { const sl = slice(x) || { yc: y, h: 0.01 }; const r = Math.max(0, 1 - ((y - sl.yc) / Math.max(sl.h, 0.01)) ** 2);
        return place(x, y, sgn * sl.h * W * Math.sqrt(r)); });
      const op = Math.min(1, Math.max(0, (Math.abs(Math.cos(th)) - 0.3) / 0.35));   // gone while the beak points at us
      return op <= 0 ? "" : `<path d="M ${q.map(p => `${f(p[0])} ${f(p[1])}`).join(" L ")}" stroke-width="2.2154"${op < 1 ? ` opacity="${f(op)}"` : ""}/>`;
    };
    // near side goes on top of the beak; the far side and the seam go behind it, so the beak hides them
    let lines = "", back = "";
    const c = Math.cos(th);
    if (c >= 0) { lines += mouthOn(1); back += mouthOn(-1); } else { lines += mouthOn(-1); back += mouthOn(1); }
    // seam ring and top ridge only show while turning
    if (side > 0.03) {
      const sl = slice(SEAM_X); let seam = "", on = false;
      for (let k = 0; k <= 32; k++) { const a = k / 32 * 2 * Math.PI, p = place(SEAM_X, sl.yc + sl.h * Math.cos(a), sl.h * W * Math.sin(a));
        const nz = Math.sin(a) * Math.cos(th);           // which way this bit of the ring faces
        if (nz > -0.05) { seam += `${on ? " L" : " M"} ${f(p[0])} ${f(p[1])}`; on = true; } else on = false; }
      back += `<path d="${seam}" stroke-width="1.8" opacity="${f(side)}"/>`;
    }
    return `<g fill="none" stroke="${L}" stroke-linecap="round" stroke-linejoin="round">${back}</g>` +
      `<path d="${outline}" fill="${F}" stroke="${L}" stroke-width="3.0077" stroke-linejoin="round"/>` +
      `<g fill="none" stroke="${L}" stroke-linecap="round" stroke-linejoin="round">${lines}</g>`;
  }

  function crest(th) {
    const c = Math.cos(th * D), s = Math.max(Math.abs(c), 0.24) * (c < 0 ? -1 : 1);
    const st = `fill="${F}" stroke="${L}" stroke-width="2.5185" stroke-linejoin="round"`;
    return `<g transform="translate(57 14) scale(${f(1.35 * s)} 1.35) translate(-57 -14)">` +
      `<path d="M 50 14.5 C 47 9 47 4 50 1 C 52 6 53 10 54.5 13 Z" ${st}/><path d="M 54 13 C 53 6 55 0 59 -3 C 60 3 60 8 59.5 12.5 Z" ${st}/>` +
      `<path d="M 59 12.8 C 61 7 64 3 69 2 C 67 7 65 11 63.5 13.8 Z" ${st}/></g>`;
  }

  // pose.grow: 0 = plain globe, 1 = crest, eye and beak fully out (they grow from where they join the head)
  const grown = (g, x, y, inner) => g <= 0.01 ? "" : g >= 0.999 ? inner : `<g transform="translate(${x} ${y}) scale(${f(g)}) translate(${-x} ${-y})">${inner}</g>`;
  function body(pose, id) {
    const g = pose.grow == null ? 1 : pose.grow;
    return `${grown(g, 56, 13, crest(pose.th))}<circle cx="${CX}" cy="${CY}" r="${R}" fill="${F}"/>` +
      `<g fill="none" stroke="${L}" stroke-width="1.6" clip-path="url(#c${id})"><line x1="18" y1="50" x2="94" y2="50"/>` +
      `<path d="M 16 30 Q 56 37 96 30"/><path d="M 16 70 Q 56 63 96 70"/>${pose.noMer ? "" : meridians(pose.th)}</g>` +
      `<g clip-path="url(#c${id})">${grown(g, 44.5, 34.8, eyes(pose))}</g><circle cx="${CX}" cy="${CY}" r="${R}" fill="none" stroke="${L}" stroke-width="4.6"/>${grown(g, 19, 56, beak(pose))}`;
  }

  let uid = 0;
  function svg(pose, id, opt) {
    id = id || ++uid; opt = opt || {};
    const b = body(pose, id);
    if (opt.glow === false) return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${opt.viewBox || "0 -10 100 110"}"><defs>` +
      `<clipPath id="c${id}"><circle cx="${CX}" cy="${CY}" r="${R}"/></clipPath></defs>${b}</svg>`;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${opt.viewBox || "0 -10 100 110"}" overflow="visible"><defs>` +
      `<clipPath id="c${id}"><circle cx="${CX}" cy="${CY}" r="${R}"/></clipPath>` +
      `<filter id="h${id}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>` +
      `<filter id="n${id}" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur in="SourceGraphic" stdDeviation="1.6" result="a"/>` +
      `<feGaussianBlur in="SourceGraphic" stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="a"/></feMerge></filter></defs>` +
      `<g transform="translate(${f(pose.dx || 0)} ${f(pose.dy || 0)}) rotate(${f(pose.tilt || 0)} 50 88)"><circle cx="56" cy="48" r="40" fill="${L}" opacity="0.5" filter="url(#h${id})"/>` +
      `<g filter="url(#n${id})">${b}</g>${b}</g></svg>`;
  }

  // ---- animations: each maps t (0..1) to a pose ----
  const ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  const seg = (t, a, b) => Math.min(1, Math.max(0, (t - a) / (b - a)));
  const REST = { th: 0, tilt: 0, jaw: 0, wink: 0, look: [0, 0], grow: 0 };
  const MOVES = {
    wink: { ms: 1100, at: t => ({ ...REST, tilt: -7 * Math.sin(Math.PI * ease(seg(t, 0, 1))), wink: t > .3 && t < .62 ? 1 : 0 }) },
    look: { ms: 2200, at: t => {
      const k = [[0, 0, 0], [.15, -5, 2], [.35, -5, 2], [.5, 2, 4], [.7, 2, 4], [.85, 0, 0], [1, 0, 0]];
      let i = 0; while (i < k.length - 2 && t > k[i + 1][0]) i++;
      const u = ease(seg(t, k[i][0], k[i + 1][0]));
      const tl = t < .5 ? -3 * Math.sin(Math.PI * seg(t, .1, .45)) : 3 * Math.sin(Math.PI * seg(t, .45, .85));
      return { ...REST, tilt: tl, look: [k[i][1] + (k[i + 1][1] - k[i][1]) * u, k[i][2] + (k[i + 1][2] - k[i][2]) * u] };
    } },
    turn: { ms: 5800, at: (t, el) => {
      // turn (0-.13), inspect the "p" (.13-.5), peck twice (.5-.74), hold (.74-.86), turn back (.86-1)
      const th = t < .13 ? 180 * ease(seg(t, 0, .13)) : t < .86 ? 180 : 180 * (1 - ease(seg(t, .86, 1)));
      let tilt = (t < .13 ? -4 * Math.sin(Math.PI * seg(t, 0, .13)) : t > .86 ? 4 * Math.sin(Math.PI * seg(t, .86, 1)) : 0);
      const reach = (el && el._ppReach) || 0;
      // inspecting: lean back, cock the head one way then the other, eye drops to the letter
      const lean = t > .15 && t < .5 ? Math.sin(Math.PI * seg(t, .15, .5)) : 0;
      const cock = t > .17 && t < .47 ? Math.sin(2 * Math.PI * seg(t, .17, .47)) : 0;
      const eye = t > .2 && t < .5 ? Math.sin(Math.PI * seg(t, .2, .5)) : 0;
      let d = 0, hit = 0;
      for (const [a, b] of [[.5, .61], [.63, .74]]) {
        if (t >= a && t <= b) { const u = seg(t, a, b); d = u < .32 ? ease(u / .32) : 1 - ease((u - .32) / .68); if (u >= .3 && u <= .42) hit = a; }
      }
      return { ...REST, th, tilt: tilt - 4 * lean + 6 * cock + 9 * d, dx: reach * d - 3 * lean, dy: 2 * d - 1 * lean,
        look: [2.2 * eye, 2.6 * eye], hit };
    } },
  };

  const G_IN = 520, G_HOLD = 160, G_OUT = 460;
  const popOut = x => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };  // slight overshoot
  function play(el, name, done) {
    const m = MOVES[name]; if (!m || el._ppBusy) return;
    el._ppBusy = true; const id = el._ppId || (el._ppId = ++uid); const t0 = performance.now();
    const total = G_IN + G_HOLD + m.ms + G_HOLD + G_OUT;
    const step = now => {
      const e = Math.min(total, now - t0), t = Math.min(1, Math.max(0, (e - G_IN - G_HOLD) / m.ms));
      const after = e - (G_IN + G_HOLD + m.ms + G_HOLD);
      const grow = e < G_IN ? popOut(e / G_IN) : after > 0 ? 1 - ease(Math.min(1, after / G_OUT)) : 1;
      const pose = { ...m.at(t, el), grow };
      el.innerHTML = svg(pose, id);
      if (pose.hit && el._ppLastHit !== pose.hit) { el._ppLastHit = pose.hit; el.dispatchEvent(new CustomEvent("ppbird-peck", { bubbles: true })); }
      if (e < total) requestAnimationFrame(step); else { el.innerHTML = svg(REST, id); el._ppBusy = false; el._ppLastHit = 0; done && done(); }
    };
    requestAnimationFrame(step);
  }

  function reachTo(el, target, overlap) {
    const a = el.getBoundingClientRect(), b = target.getBoundingClientRect();
    if (!a.height || !b.width) return 0;
    const k = Math.min(a.width / 100, a.height / 110), x0 = a.left + (a.width - 100 * k) / 2;
    // beak tip when facing right sits at about x = 112 in the drawing
    return Math.max(0, (b.left + (overlap || 1.5) - (x0 + 112 * k)) / k);
  }
  root.ppBird = { svg, play, reachTo, MOVES: Object.keys(MOVES), REST };
})(typeof window !== "undefined" ? window : globalThis);
