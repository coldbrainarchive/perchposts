// Perch Posts trending globe (2026-11-23). Pins = the outlets covering each of the top stories of the last 24h,
// placed on the outlet's home city. Tap a story below to light it up (arcs between its outlets); tap a pin to open it.
(function () {
  const API = 'https://daboysforumip.coldbrainarchive.workers.dev';
  const COLORS = ['#c084fc', '#2dd4bf', '#fbbf24', '#f87171', '#60a5fa', '#4ade80', '#fb923c', '#f472b6', '#a3e635', '#38bdf8', '#e879f9', '#facc15'];
  const ISO = { "Argentina": "AR", "Australia": "AU", "Bangladesh": "BD", "Brazil": "BR", "Canada": "CA", "Chile": "CL", "China": "CN", "Colombia": "CO", "Costa Rica": "CR", "Egypt": "EG", "Ethiopia": "ET", "Finland": "FI", "France": "FR", "Germany": "DE", "Ghana": "GH", "Greece": "GR", "Hong Kong": "HK", "India": "IN", "Indonesia": "ID", "Ireland": "IE", "Israel": "IL", "Italy": "IT", "Jamaica": "JM", "Japan": "JP", "Kazakhstan": "KZ", "Kenya": "KE", "Kuwait": "KW", "Mexico": "MX", "Myanmar": "MM", "Netherlands": "NL", "New Zealand": "NZ", "Nigeria": "NG", "Pakistan": "PK", "Philippines": "PH", "Poland": "PL", "Qatar": "QA", "Russia": "RU", "Saudi Arabia": "SA", "Serbia": "RS", "Singapore": "SG", "South Africa": "ZA", "South Korea": "KR", "Spain": "ES", "Sri Lanka": "LK", "Sweden": "SE", "Taiwan": "TW", "Tanzania": "TZ", "Thailand": "TH", "Turkey": "TR", "Ukraine": "UA", "United Arab Emirates": "AE", "United Kingdom": "GB", "United States": "US", "Uruguay": "UY", "Vietnam": "VN", "Lebanon": "LB", "Iran": "IR", "Iraq": "IQ", "Jordan": "JO", "Morocco": "MA", "Peru": "PE", "Venezuela": "VE", "Zimbabwe": "ZW", "Uganda": "UG", "Rwanda": "RW", "Malaysia": "MY", "Nepal": "NP", "Portugal": "PT", "Switzerland": "CH", "Belgium": "BE", "Austria": "AT", "Norway": "NO", "Denmark": "DK", "Czech Republic": "CZ", "Hungary": "HU", "Romania": "RO", "Bulgaria": "BG", "Croatia": "HR", "Cuba": "CU", "Dominican Republic": "DO", "Trinidad & Tobago": "TT" };
  const flag = c => { const k = ISO[c]; return k ? String.fromCodePoint(...[...k].map(ch => 0x1f1e6 + ch.charCodeAt(0) - 65)) : ''; };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
  const ago = t => { const m = Math.max(1, Math.round((Date.now() - new Date(t).getTime()) / 60000)); return m < 60 ? m + 'm ago' : Math.round(m / 60) + 'h ago'; };
  const $ = id => document.getElementById(id);

  // Stars behind the globe
  (function stars() {
    const c = $('stars'), d = Math.min(2, devicePixelRatio || 1);
    const draw = () => { c.width = innerWidth * d; c.height = innerHeight * d; const x = c.getContext('2d'); x.clearRect(0, 0, c.width, c.height);
      for (let i = 0; i < 220; i++) { x.globalAlpha = Math.random() * 0.7 + 0.15; x.fillStyle = '#fff'; x.beginPath(); x.arc(Math.random() * c.width, Math.random() * c.height, Math.random() * 1.1 * d, 0, 7); x.fill(); } };
    draw(); addEventListener('resize', draw);
  })();

  let stories = [], pins = [], sel = -1, world = null, pinTapAt = 0;

  // Outlets in the same city fan out in a small ring so every pin can be tapped
  function spread(list) {
    const at = new Map();
    for (const p of list) { const k = p.lat.toFixed(1) + ',' + p.lng.toFixed(1); if (!at.has(k)) at.set(k, []); at.get(k).push(p); }
    for (const group of at.values()) {
      if (group.length < 2) continue;
      group.forEach((p, i) => { const a = (i / group.length) * Math.PI * 2, r = 0.9 + 0.35 * Math.floor(i / 8);
        p.lat += Math.sin(a) * r; p.lng += Math.cos(a) * r / Math.max(0.3, Math.cos(p.lat * Math.PI / 180)); });
    }
  }

  function pinEl(p) {
    const el = document.createElement('div');
    el.className = 'pin'; el.style.setProperty('--c', COLORS[p.s % COLORS.length]);
    el.innerHTML = `<i></i><span class="lb">${esc(p.outlet)}</span>`;
    el.addEventListener('pointerdown', ev => { ev.stopPropagation(); });
    el.addEventListener('click', ev => { ev.stopPropagation(); pinTapAt = Date.now(); openPin(p); });
    p.el = el;
    return el;
  }

  function paint() {
    for (const p of pins) { if (!p.el) continue; p.el.classList.toggle('dim', sel >= 0 && p.s !== sel); p.el.classList.toggle('big', p.s === sel); }
    document.querySelectorAll('.sc').forEach((b, i) => b.classList.toggle('on', i === sel));
    if (!world) return;
    if (sel < 0) { world.arcsData([]); world.ringsData([]); return; }
    const sp = pins.filter(p => p.s === sel), hub = sp[0], col = COLORS[sel % COLORS.length];
    world.arcsData(sp.slice(1).map(p => ({ startLat: hub.lat, startLng: hub.lng, endLat: p.lat, endLng: p.lng, color: col })));
    world.ringsData([{ lat: hub.lat, lng: hub.lng, color: col }]);
  }

  function pick(i, fly) {
    sel = i === sel ? -1 : i;
    paint();
    if (sel < 0 || !world || !fly) return;
    const sp = pins.filter(p => p.s === sel);
    // aim at the middle of its outlets (average of unit vectors), zoom out when they span the world
    let x = 0, y = 0, z = 0;
    for (const p of sp) { const la = p.lat * Math.PI / 180, lo = p.lng * Math.PI / 180; x += Math.cos(la) * Math.cos(lo); y += Math.cos(la) * Math.sin(lo); z += Math.sin(la); }
    const n = Math.hypot(x, y, z) / sp.length;
    world.controls().autoRotate = false;
    world.pointOfView({ lat: Math.atan2(z, Math.hypot(x, y)) * 180 / Math.PI, lng: Math.atan2(y, x) * 180 / Math.PI, altitude: n > 0.85 ? 1.7 : n > 0.5 ? 2.3 : 2.8 }, 1200);
    const card = document.querySelectorAll('.sc')[sel];
    card && card.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
  }

  function openPin(p) {
    const st = stories[p.s];
    if (sel !== p.s) pick(p.s, false);
    world && world.controls && (world.controls().autoRotate = false);
    $('sh').innerHTML = `<div class="grab"><i></i></div>${p.image ? `<img class="hero" src="${esc(p.image)}" alt="" referrerpolicy="no-referrer">` : ''}
      <div class="bd"><div class="src">${flag(p.country)} ${esc(p.outlet)} · ${esc(p.city)} · ${ago(p.t)}</div>
      <h2>${esc(p.title)}</h2>
      <div class="story">Part of #${st.rank} · covered by ${st.outlets} outlets in ${st.countries} countries</div>
      <div class="row"><a class="btn pri" href="/post/${encodeURIComponent(p.id)}">Open post</a><a class="btn" href="${esc(p.url)}" target="_blank" rel="noopener noreferrer">Read at source</a></div></div>`;
    const hi = $('sh').querySelector('img.hero'); hi && hi.addEventListener('error', () => hi.remove());
    $('sheet').classList.add('in');
  }
  function closeSheet() { $('sheet').classList.remove('in'); }
  // tap the handle, drag it down, or tap the globe to close
  (function sheetGestures() {
    const s = $('sheet'); let y0 = null;
    s.addEventListener('click', e => { if (e.target.closest('.grab')) closeSheet(); });
    s.addEventListener('touchstart', e => { y0 = e.touches[0].clientY; }, { passive: true });
    s.addEventListener('touchmove', e => { if (y0 == null) return; const d = e.touches[0].clientY - y0; if (d > 0) s.firstElementChild.style.transform = `translateY(${d}px)`; }, { passive: true });
    s.addEventListener('touchend', e => { if (y0 == null) return; const d = (e.changedTouches[0].clientY - y0); s.firstElementChild.style.transform = ''; if (d > 70) closeSheet(); y0 = null; });
  })();

  function strip() {
    $('strip').innerHTML = stories.map((s, i) => `<button type="button" class="sc" style="--c:${COLORS[i % COLORS.length]}">
      ${s.image ? `<img src="${esc(s.image)}" alt="" referrerpolicy="no-referrer">` : '<span class="ph"></span>'}
      <span class="tx"><span class="hd">${esc(s.title)}</span><span class="mt"><span class="rk">${s.rank}</span>${s.outlets} outlets · ${s.countries} countries</span></span></button>`).join('');
    document.querySelectorAll('.sc').forEach((b, i) => b.addEventListener('click', () => { closeSheet(); pick(i, true); }));
    document.querySelectorAll('.sc img').forEach(im => im.addEventListener('error', () => { const ph = document.createElement('span'); ph.className = 'ph'; im.replaceWith(ph); }));
  }

  function start() {
    if (typeof Globe !== 'function') { $('empty').textContent = 'The globe couldn’t load on this device.'; return; }
    world = new Globe($('globe'), { animateIn: true })
      .backgroundColor('rgba(0,0,0,0)')
      .globeImageUrl('/globe/earth-blue-marble.jpg')
      .showAtmosphere(true).atmosphereColor('#8ab4ff').atmosphereAltitude(0.18)
      .htmlElementsData(pins).htmlLat('lat').htmlLng('lng').htmlAltitude(0.01).htmlElement(pinEl).htmlTransitionDuration(0)
      .htmlElementVisibilityModifier(() => {})
      .arcColor('color').arcStroke(0.45).arcDashLength(0.5).arcDashGap(0.25).arcDashAnimateTime(2200).arcAltitudeAutoScale(0.35)
      .ringColor(r => t => `rgba(${hexRgb(r.color)},${1 - t})`).ringMaxRadius(5).ringPropagationSpeed(2.5).ringRepeatPeriod(1100)
      .onGlobeClick(() => { if (Date.now() - pinTapAt > 400) closeSheet(); });
    const c = world.controls(); c.autoRotate = true; c.autoRotateSpeed = 0.45; c.enableDamping = true;
    // Pins only show on the side of the Earth facing you (with a margin, so none float past the edge)
    const R = Math.PI / 180;
    const vis = () => { const v = world.pointOfView(), a = v.lat * R, b = v.lng * R;
      for (const p of pins) { if (!p.el) continue; const la = p.lat * R; const d = Math.sin(a) * Math.sin(la) + Math.cos(a) * Math.cos(la) * Math.cos(p.lng * R - b); p.el.classList.toggle('back', d < 0.3); } };
    c.addEventListener('change', vis); setTimeout(vis, 50); setInterval(vis, 500);
    world.renderer().domElement.addEventListener('pointerdown', () => { c.autoRotate = false; });
    const fit = () => { world.width(innerWidth).height(innerHeight); };
    fit(); addEventListener('resize', fit);
    world.pointOfView({ lat: 22, lng: 20, altitude: innerWidth < 600 ? 2.9 : 2.2 });
  }
  // Outlet labels: hide any that would overlap one already shown (checked a few times a second)
  function declutter() {
    const shown = [];
    for (const p of pins) {
      if (!p.el || !p.el.classList.contains('big')) continue;
      const lb = p.el.querySelector('.lb'); if (!lb) continue;
      lb.style.visibility = '';
      if (p.el.classList.contains('back')) continue;
      const r = lb.getBoundingClientRect();
      if (shown.some(q => r.left < q.right + 4 && r.right > q.left - 4 && r.top < q.bottom + 2 && r.bottom > q.top - 2)) lb.style.visibility = 'hidden';
      else shown.push(r);
    }
  }
  setInterval(() => { if (sel >= 0) declutter(); }, 250);
  function hexRgb(h) { const n = parseInt(h.slice(1), 16); return `${n >> 16 & 255},${n >> 8 & 255},${n & 255}`; }

  fetch(API + '/globe').then(r => r.json()).then(d => {
    stories = (d.stories || []);
    pins = stories.flatMap((s, i) => s.posts.map(p => ({ ...p, s: i })));
    spread(pins);
    if (d.built_at) $('sub').textContent = `Last 24 hours · ${stories.length} top stories · updated ${ago(d.built_at)}`;
    $('empty').remove();
    if (!stories.length) { $('sub').textContent = 'No trending stories yet — check back soon'; }
    strip(); start();
  }).catch(() => { $('empty').textContent = 'Couldn’t load the stories. Try again in a moment.'; });
})();
