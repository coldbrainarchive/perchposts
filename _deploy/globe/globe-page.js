// Perch Posts trending globe (2026-11-23). Pins = the outlets covering each of the top stories of the last 24h,
// placed on the outlet's home city. A numbered glow marks where each story happened (story.origin from the server).
// Tap a story or its marker to light it up (arcs spread from where it happened to every outlet); tap a pin to open it.
(function () {
  const API = 'https://daboysforumip.coldbrainarchive.workers.dev';
  const COLORS = ['#c084fc', '#2dd4bf', '#fbbf24', '#f87171', '#60a5fa', '#4ade80', '#fb923c', '#f472b6', '#a3e635', '#38bdf8', '#e879f9', '#facc15'];
  const ISO = { "Argentina": "AR", "Australia": "AU", "Bangladesh": "BD", "Brazil": "BR", "Canada": "CA", "Chile": "CL", "China": "CN", "Colombia": "CO", "Costa Rica": "CR", "Egypt": "EG", "Ethiopia": "ET", "Finland": "FI", "France": "FR", "Germany": "DE", "Ghana": "GH", "Greece": "GR", "Hong Kong": "HK", "India": "IN", "Indonesia": "ID", "Ireland": "IE", "Israel": "IL", "Italy": "IT", "Jamaica": "JM", "Japan": "JP", "Kazakhstan": "KZ", "Kenya": "KE", "Kuwait": "KW", "Mexico": "MX", "Myanmar": "MM", "Netherlands": "NL", "New Zealand": "NZ", "Nigeria": "NG", "Pakistan": "PK", "Philippines": "PH", "Poland": "PL", "Qatar": "QA", "Russia": "RU", "Saudi Arabia": "SA", "Serbia": "RS", "Singapore": "SG", "South Africa": "ZA", "South Korea": "KR", "Spain": "ES", "Sri Lanka": "LK", "Sweden": "SE", "Taiwan": "TW", "Tanzania": "TZ", "Thailand": "TH", "Turkey": "TR", "Ukraine": "UA", "United Arab Emirates": "AE", "United Kingdom": "GB", "United States": "US", "Uruguay": "UY", "Vietnam": "VN", "Lebanon": "LB", "Iran": "IR", "Iraq": "IQ", "Jordan": "JO", "Morocco": "MA", "Peru": "PE", "Venezuela": "VE", "Zimbabwe": "ZW", "Uganda": "UG", "Rwanda": "RW", "Malaysia": "MY", "Nepal": "NP", "Portugal": "PT", "Switzerland": "CH", "Belgium": "BE", "Austria": "AT", "Norway": "NO", "Denmark": "DK", "Czech Republic": "CZ", "Hungary": "HU", "Romania": "RO", "Bulgaria": "BG", "Croatia": "HR", "Cuba": "CU", "Dominican Republic": "DO", "Trinidad & Tobago": "TT", "Albania": "AL", "Andorra": "AD", "Belarus": "BY", "Bosnia & Herzegovina": "BA", "Cyprus": "CY", "Estonia": "EE", "Georgia": "GE", "Iceland": "IS", "Kosovo": "XK", "Latvia": "LV", "Liechtenstein": "LI", "Lithuania": "LT", "Luxembourg": "LU", "Malta": "MT", "Moldova": "MD", "Monaco": "MC", "Montenegro": "ME", "North Macedonia": "MK", "Slovakia": "SK", "Slovenia": "SI", "Algeria": "DZ", "Angola": "AO", "Benin": "BJ", "Botswana": "BW", "Burkina Faso": "BF", "Burundi": "BI", "Cameroon": "CM", "Chad": "TD", "Congo": "CG", "DR Congo": "CD", "Eritrea": "ER", "Eswatini": "SZ", "Gabon": "GA", "Gambia": "GM", "Guinea": "GN", "Liberia": "LR", "Libya": "LY", "Madagascar": "MG", "Malawi": "MW", "Mali": "ML", "Mauritania": "MR", "Mauritius": "MU", "Mozambique": "MZ", "Namibia": "NA", "Niger": "NE", "Senegal": "SN", "Sierra Leone": "SL", "Somalia": "SO", "South Sudan": "SS", "Sudan": "SD", "Togo": "TG", "Tunisia": "TN", "Zambia": "ZM", "Afghanistan": "AF", "Armenia": "AM", "Azerbaijan": "AZ", "Bhutan": "BT", "Brunei": "BN", "Cambodia": "KH", "Kyrgyzstan": "KG", "Laos": "LA", "Maldives": "MV", "Mongolia": "MN", "North Korea": "KP", "Tajikistan": "TJ", "Turkmenistan": "TM", "Uzbekistan": "UZ", "Bahamas": "BS", "Belize": "BZ", "El Salvador": "SV", "Guatemala": "GT", "Haiti": "HT", "Honduras": "HN", "Nicaragua": "NI", "Panama": "PA", "Bahrain": "BH", "Oman": "OM", "Palestine": "PS", "Syria": "SY", "Yemen": "YE", "Bolivia": "BO", "Ecuador": "EC", "Paraguay": "PY", "Fiji": "FJ", "Papua New Guinea": "PG", "Chile": "CL" };
  const flag = c => { const k = ISO[c]; return k ? String.fromCodePoint(...[...k].map(ch => 0x1f1e6 + ch.charCodeAt(0) - 65)) : ''; };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
  const ago = t => { const m = Math.max(1, Math.round((Date.now() - new Date(t).getTime()) / 60000)); return m < 60 ? m + 'm ago' : Math.round(m / 60) + 'h ago'; };
  const $ = id => document.getElementById(id);
  const siteOf = u => { try { return new URL(u).hostname.replace(/^www\./, ''); } catch (e) { return 'Website'; } };

  // Only the ‹ arrow leaves the globe: a side-swipe (Safari's back gesture) or the browser's back lands on the
  // same page instead, because we keep one extra history step and put it back whenever it's used up.
  (function stayOnGlobe() {
    try {
      history.replaceState({ ppGlobe: 'base' }, '');
      history.pushState({ ppGlobe: 'guard' }, '');
      addEventListener('popstate', () => { if (!leaving) history.pushState({ ppGlobe: 'guard' }, ''); });
    } catch (e) {}
    let leaving = false;
    document.querySelectorAll('a.back, a.home').forEach(a => a.addEventListener('click', ev => {
      ev.preventDefault(); leaving = true; location.replace(a.getAttribute('href') || '/');
    }));
  })();

  // Stars behind the globe
  (function stars() {
    const c = $('stars'), d = Math.min(2, devicePixelRatio || 1);
    const draw = () => { c.width = innerWidth * d; c.height = innerHeight * d; const x = c.getContext('2d'); x.clearRect(0, 0, c.width, c.height);
      for (let i = 0; i < 220; i++) { x.globalAlpha = Math.random() * 0.7 + 0.15; x.fillStyle = '#fff'; x.beginPath(); x.arc(Math.random() * c.width, Math.random() * c.height, Math.random() * 1.1 * d, 0, 7); x.fill(); } };
    draw(); addEventListener('resize', draw);
  })();

  let olQ = 0;
  let stories = [], pins = [], events = [], marks = [], sel = -1, world = null, pinTapAt = 0, foc = null, progScroll = 0, curList = [], rsAt = -1, pvOpen = false;
  const placeShort = o => o ? (o.how === 'first' ? `First: ${o.city || o.country}` : (o.city || o.country)) : '';

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

  // Where a story happened: a numbered glow that matches its card below
  function evEl(e) {
    const el = document.createElement('div');
    el.className = 'ev'; el.style.setProperty('--c', COLORS[e.s % COLORS.length]);
    const st = stories[e.s] || {};
    // overview preview: tiny photo + short headline beside the circle (placed/hidden by overviewLabels)
    el.innerHTML = `<b data-n="${e.s + 1}"></b><span class="lb">${esc(flag(e.country))} ${esc(e.name)}</span><span class="mini">${st.image ? `<img src="${esc(st.image)}" alt="" referrerpolicy="no-referrer">` : ''}<span>${esc(st.title || '')}</span></span>`;
    const mi = el.querySelector('.mini img'); mi && mi.addEventListener('error', () => mi.remove());
    el.addEventListener('pointerdown', ev => { ev.stopPropagation(); });
    el.addEventListener('click', ev => { ev.stopPropagation(); pinTapAt = Date.now(); closeSheet(); pick(e.s, true); });
    e.el = el;
    return el;
  }
  function pinEl(p) {
    if (p.kind === 'ev') return evEl(p);
    const el = document.createElement('div');
    el.className = 'pin'; el.style.setProperty('--c', COLORS[p.s % COLORS.length]);
    // the preview pinned to the outlet: ‹ › step through the story's outlets (list order); tapping the preview drops
    // down the article preview (summary + Open post / Read at source)
    el.innerHTML = `<i></i><span class="lb">${esc(p.outlet)}</span><div class="pv"><div class="pv-row"><button type="button" class="pv-nav" data-d="-1" aria-label="Previous outlet">‹</button>${p.image ? `<img src="${esc(p.image)}" alt="" referrerpolicy="no-referrer">` : ''}<span class="pt"><b>${esc(p.title)}</b><span>${esc(flag(p.country))} ${esc(p.outlet)} · ${esc(p.city)} · ${ago(p.t)}</span></span><button type="button" class="pv-nav" data-d="1" aria-label="Next outlet">›</button></div>
      <div class="pv-more"><a class="pv-site" href="${esc(p.url)}" target="_blank" rel="noopener noreferrer">${esc(siteOf(p.url))}</a>${p.desc ? `<p>${esc(p.desc)}</p>` : ''}<div class="pv-btns"><a class="btn pri" href="/post/${encodeURIComponent(p.id)}">View post</a></div></div></div>`;
    const im = el.querySelector('.pv img'); im && im.addEventListener('error', () => im.remove());
    el.addEventListener('pointerdown', ev => { ev.stopPropagation(); });
    el.addEventListener('click', ev => {
      ev.stopPropagation(); pinTapAt = Date.now();
      const nav = ev.target.closest('.pv-nav');
      if (nav) { stepOutlet(p, +nav.dataset.d); return; }
      if (ev.target.closest('.pv-btns a,.pv-site')) return;            // let the links open
      if (foc === p) { pvOpen = el.querySelector('.pv').classList.toggle('exp'); return; }
      focusPin(p, false);
    });
    p.el = el;
    return el;
  }

  // ‹ › on the preview: the previous / next outlet in the list order, flying the globe there
  function stepOutlet(p, d) {
    if (!curList.includes(p)) outlets(true);
    const i = curList.indexOf(p), n = curList.length;
    const q = curList[(i + d + n) % n];
    if (q && q !== p) focusPin(q, true);
    updateNav();
  }
  function updateNav() {
    const n = curList.length, i = curList.indexOf(foc);
    if (!foc || !foc.el) return;
    foc.el.querySelectorAll('.pv-nav').forEach(b => { b.style.visibility = n > 1 ? '' : 'hidden'; });
    const t = foc.el.querySelector('.pt span'); if (t && i >= 0) t.dataset.n = `${i + 1}/${n}`;
  }
  function focusPin(p, fly) {
    // an open drop-down stays open on the next outlet (‹ ›, list or pin) until you close it
    if (foc && foc.el) foc.el.querySelector('.pv')?.classList.remove('exp');
    if (!p) pvOpen = false;
    foc = p;
    if (p && p.el && pvOpen) p.el.querySelector('.pv').classList.add('exp');
    for (const q of pins) q.el && q.el.classList.toggle('focus', q === p);
    document.body.classList.toggle('focusing', !!p);
    document.querySelectorAll('.or').forEach(b => b.classList.toggle('on', b._p === p));
    if (!p) return;
    closeSheet();
    $('ol').classList.remove('open');
    // the pin sits a little below the middle so its preview (and the drop-down) has room above it
    if (fly && world) { world.controls().autoRotate = false; world.pointOfView({ lat: p.lat + 7, lng: p.lng, altitude: 1.5 }, 1000); }
    if (!curList.includes(p) && sel === p.s) outlets(true);
    updateNav();
  }
  let ord = 'near';
  try { ord = localStorage.getItem('pp_globe_order') === 'first' ? 'first' : 'near'; } catch (e) {}
  // slide the toggle's thumb under the active button (like the toggles on the rest of the site)
  function toggleUI(near, anim) {
    const el = $('olS'), th = el.querySelector('.tg-thumb'), bs = [...el.querySelectorAll('.sort-toggle-btn')];
    el.style.display = near ? '' : 'none';
    bs.forEach(b => b.classList.toggle('active', b.dataset.o === ord));
    const a = bs.find(b => b.dataset.o === ord); if (!a || !near) return;
    if (anim && el.classList.contains('no-anim')) { el.classList.remove('no-anim'); void el.offsetWidth; } else el.classList.toggle('no-anim', !anim);
    const er = el.getBoundingClientRect(), ar = a.getBoundingClientRect(), inner = er.width - el.clientLeft * 2;
    th.style.left = (a === bs[0] ? -1 : ar.left - er.left - el.clientLeft) + 'px';
    th.style.right = (a === bs[bs.length - 1] ? -1 : inner - (ar.right - er.left - el.clientLeft)) + 'px';
  }
  const kmBetween = (a, b, c, d) => { const R = Math.PI / 180, x = Math.sin((c - a) * R / 2) ** 2 + Math.cos(a * R) * Math.cos(c * R) * Math.sin((d - b) * R / 2) ** 2; return 12742 * Math.asin(Math.sqrt(x)); };
  // The selected story's outlets, nearest to where it happened first (earliest first when it has no place),
  // in a list that opens above the story cards. "First" marks whoever reported it earliest.
  function outlets(keep) {
    const ol = $('ol');
    if (sel < 0) { ol.classList.remove('on', 'open'); return; }
    const st = stories[sel], o = st.origin, near = o && o.how !== 'first' && isFinite(o.lat);
    const sp = pins.filter(p => p.s === sel);
    const firstP = sp.reduce((a, p) => (String(p.t) < String(a.t) ? p : a), sp[0]);
    // distance from the real place (pins are fanned out slightly, so use the outlet's own city)
    for (const p of sp) p.km = near ? kmBetween(+o.lat, +o.lng, p.lat0, p.lng0) : null;
    sp.sort(near && ord === 'near' ? (a, b) => a.km - b.km : (a, b) => String(a.t).localeCompare(String(b.t)));
    curList = sp;
    if (!keep) requestAnimationFrame(() => toggleUI(near, false));
    ol.style.setProperty('--c', COLORS[sel % COLORS.length]);
    ol.classList.add('on'); if (!keep) ol.classList.remove('open');
    $('olT').innerHTML = `See all ${sp.length} outlet${sp.length === 1 ? '' : 's'} <i>▴</i>`;
    // the list lives inside the selected story's card (the card grows up from the bottom)
    const slot = document.querySelectorAll('.sc')[sel]; slot && slot.querySelector('.sc-slot').appendChild(ol);
    $('olL').innerHTML = '';
    sp.forEach((p, k) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'or'; b._p = p;
      const dist = p.km == null ? '' : p.km < 60 ? ' · right there' : ` · ${Math.round(p.km / 10) * 10 >= 1000 ? Math.round(p.km / 100) * 100 : Math.round(p.km / 10) * 10}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + (p.km < 60 ? '' : ' km');
      b.innerHTML = `<span class="fl">${flag(p.country)}</span><span class="nm"><b>${esc(p.outlet)}</b><span>${esc(p.city)}${dist} · ${ago(p.t)}</span></span>${p === firstP ? '<span class="fs">First</span>' : ''}`;
      b.addEventListener('click', () => focusPin(p, true));
      $('olL').appendChild(b);
    });
  }
  // Overview previews: show as many as fit (up to 8, best-ranked first) without covering each other or another
  // story's circle; each tries the right side, then the left, else stays hidden until the globe turns
  function overviewLabels() {
    // only once you've zoomed in closer than the starting view (zoomed out, the globe stays clean)
    const near = world && world.pointOfView().altitude < ZOOM_PREVIEWS;
    document.body.classList.toggle('overview', sel < 0 && !!near);
    if (sel >= 0 || !near) return;
    const vw = innerWidth, top = 70, bottom = (document.querySelector('.strip')?.getBoundingClientRect().top || innerHeight) - 6;
    const front = events.filter(e => e.el && !e.el.classList.contains('back'));
    const circles = front.map(e => e.el.querySelector('b').getBoundingClientRect());
    const taken = [];
    let shown = 0;
    for (const e of [...events].sort((a, b) => a.s - b.s)) {
      const m = e.el && e.el.querySelector('.mini'); if (!m) continue;
      const ok = r => r.left >= 4 && r.right <= vw - 4 && r.top >= top && r.bottom <= bottom &&
        !taken.some(q => r.left < q.right + 4 && r.right > q.left - 4 && r.top < q.bottom + 3 && r.bottom > q.top - 3) &&
        !circles.some((c, i) => front[i] !== e && r.left < c.right + 2 && r.right > c.left - 2 && r.top < c.bottom + 2 && r.bottom > c.top - 2);
      let place = null;
      if (shown < 8 && !e.el.classList.contains('back')) {
        for (const side of ['right', 'left']) {
          m.classList.toggle('left', side === 'left');
          const r = m.getBoundingClientRect();
          if (ok(r)) { place = r; break; }
        }
      }
      m.classList.toggle('show', !!place);
      if (place) { taken.push(place); shown++; }
    }
  }
  const HOME_ALT = () => (innerWidth < 600 ? 2.9 : 2.2), ZOOM_PREVIEWS = innerWidth < 600 ? 2.3 : 1.8;
  setInterval(overviewLabels, 350);
  function paint() {
    setTimeout(overviewLabels, 30);
    for (const p of marks) { if (!p.el) continue; p.el.classList.toggle('dim', sel >= 0 && p.s !== sel); p.el.classList.toggle('big', p.s === sel); }
    document.querySelectorAll('.sc').forEach((b, i) => b.classList.toggle('on', i === sel));
    if (!world) return;
    if (sel < 0) { world.arcsData([]); world.ringsData([]); return; }
    // arcs spread out from where it happened (or from the first outlet when there's no place)
    const sp = pins.filter(p => p.s === sel), hub = events.find(e => e.s === sel) || sp[0], col = COLORS[sel % COLORS.length];
    world.arcsData(sp.filter(p => p !== hub).map(p => ({ startLat: hub.lat, startLng: hub.lng, endLat: p.lat, endLng: p.lng, color: col })));
    world.ringsData([{ lat: hub.lat, lng: hub.lng, color: col }]);
  }

  function pick(i, fly) {
    const was = sel;
    sel = i === sel ? -1 : i;
    focusPin(null);
    if (sel < 0 && was >= 0 && world) world.pointOfView({ altitude: innerWidth < 600 ? 2.9 : 2.2 }, 900);
    paint();
    outlets();
    if (sel < 0 || !world || !fly) return;
    const ev = events.find(e => e.s === sel), sp = pins.filter(p => p.s === sel).concat(ev ? [ev, ev, ev] : []);
    // (fallback) aim at the middle of its outlets; zoom out when they span the world
    let x = 0, y = 0, z = 0;
    for (const p of sp) { const la = p.lat * Math.PI / 180, lo = p.lng * Math.PI / 180; x += Math.cos(la) * Math.cos(lo); y += Math.cos(la) * Math.sin(lo); z += Math.sin(la); }
    const n = Math.hypot(x, y, z) / sp.length;
    world.controls().autoRotate = false;
    // centre on where the story happened (its numbered marker); only stories without a place frame their outlets
    if (ev) world.pointOfView({ lat: ev.lat, lng: ev.lng, altitude: innerWidth < 600 ? 2.4 : 2 }, 1200);
    else world.pointOfView({ lat: Math.atan2(z, Math.hypot(x, y)) * 180 / Math.PI, lng: Math.atan2(y, x) * 180 / Math.PI, altitude: n > 0.85 ? 1.7 : n > 0.5 ? 2.3 : 2.8 }, 1200);
    const card = document.querySelectorAll('.sc')[sel];
    if (card) { progScroll = Date.now(); card.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' }); }
  }

  // The story scroller: every outlet's version of the selected story, one per slide, swiped up/down like the post
  // scroller. The globe above flies to each outlet as you go. Order = the outlet list's order (Nearest / First).
  function slideHtml(p, k, n) {
    return `<section class="rsl" data-k="${k}">${p.image ? `<img class="hero" src="${esc(p.image)}" alt="" referrerpolicy="no-referrer">` : ''}
      <div class="bd"><div class="src">${flag(p.country)} ${esc(p.outlet)} · ${esc(p.city)}${p.km != null ? ` · ${p.km < 60 ? 'right there' : Math.round(p.km / (p.km >= 1000 ? 100 : 10)) * (p.km >= 1000 ? 100 : 10) + ' km'}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',') : ''} · ${ago(p.t)}</div>
      <h2>${esc(p.title)}</h2>${p.desc ? `<p class="ds">${esc(p.desc)}</p>` : ''}
      <div class="row"><a class="btn pri" href="/post/${encodeURIComponent(p.id)}">Open post</a><a class="btn" href="${esc(p.url)}" target="_blank" rel="noopener noreferrer">Read at source</a></div>
      ${k < n - 1 ? '<div class="rs-hint">Swipe up for the next outlet</div>' : '<div class="rs-hint">That’s every outlet on this story</div>'}</div></section>`;
  }
  function rsShow(k, fly) {
    const list = curList; if (!list[k]) return;
    rsAt = k;
    const p = list[k], st = stories[p.s];
    $('rsN').textContent = `${k + 1} / ${list.length}`;
    foc = p;
    for (const q of pins) q.el && q.el.classList.toggle('focus', q === p);
    document.querySelectorAll('.or').forEach(b => b.classList.toggle('on', b._p === p));
    // keep the outlet's pin in the strip of globe still visible above the scroller
    if (fly && world) { world.controls().autoRotate = false; world.pointOfView({ lat: p.lat - 24, lng: p.lng, altitude: 2.1 }, 800); }
  }
  function openPin(p) {
    if (sel !== p.s) pick(p.s, false);
    if (!curList.includes(p)) outlets(true);
    world && world.controls && (world.controls().autoRotate = false);
    const list = curList, k = Math.max(0, list.indexOf(p)), st = stories[p.s];
    $('sh').style.setProperty('--c', COLORS[p.s % COLORS.length]);
    $('sh').innerHTML = `<div class="grab"><i></i></div>
      <div class="rs-hd"><span class="rk">${st.rank}</span><span class="rs-tt">${esc(st.title)}</span><b id="rsN"></b></div>
      <div class="rs" id="rs">${list.map((q, i) => slideHtml(q, i, list.length)).join('')}</div>`;
    $('sh').querySelectorAll('img.hero').forEach(im => im.addEventListener('error', () => im.remove()));
    document.body.classList.add('reeling');
    $('sheet').classList.add('in');
    const rs = $('rs');
    requestAnimationFrame(() => { rs.scrollTop = k * rs.clientHeight; rsShow(k, true); });
    let t = 0;
    rs.addEventListener('scroll', () => { clearTimeout(t); t = setTimeout(() => { const i = Math.round(rs.scrollTop / rs.clientHeight); if (i !== rsAt) rsShow(i, true); }, 90); }, { passive: true });
  }
  function closeSheet() { $('sheet').classList.remove('in'); document.body.classList.remove('reeling'); }
  // tap the handle, drag it down, or tap the globe to close
  (function sheetGestures() {
    const s = $('sheet'); let y0 = null;
    s.addEventListener('click', e => { if (e.target.closest('.grab')) closeSheet(); });
    // drag down from the top bar (not the slides, which scroll) to close
    s.addEventListener('touchstart', e => { y0 = e.target.closest('.grab,.rs-hd') ? e.touches[0].clientY : null; }, { passive: true });
    s.addEventListener('touchmove', e => { if (y0 == null) return; const d = e.touches[0].clientY - y0; if (d > 0) s.firstElementChild.style.transform = `translateY(${d}px)`; }, { passive: true });
    s.addEventListener('touchend', e => { if (y0 == null) return; const d = (e.changedTouches[0].clientY - y0); s.firstElementChild.style.transform = ''; if (d > 70) closeSheet(); y0 = null; });
  })();

  (function olToggle() {
    // the Nearest / First toggle only shows while the list is open
    $('olT').addEventListener('click', () => { const o = $('ol').classList.toggle('open'); if (o) { const st = stories[sel], near = st && st.origin && st.origin.how !== 'first'; requestAnimationFrame(() => toggleUI(near, false)); } });
    $('olS').querySelectorAll('.sort-toggle-btn').forEach(b => b.addEventListener('click', () => {
      if (ord === b.dataset.o) return;
      ord = b.dataset.o; try { localStorage.setItem('pp_globe_order', ord); } catch (e) {}
      const f = foc;
      outlets(true); toggleUI(true, true);
      if (f) document.querySelectorAll('.or').forEach(r => r.classList.toggle('on', r._p === f));
    }));
  })();
  // While a story is selected, swiping the cards selects the one that lands in the middle (not when nothing's selected)
  (function swipeSelect() {
    let t = 0;
    $('strip').addEventListener('scroll', () => {
      clearTimeout(t);
      t = setTimeout(() => {
        if (sel < 0 || Date.now() - progScroll < 900) return;
        const st = $('strip'), mid = st.getBoundingClientRect().left + st.clientWidth / 2;
        let best = -1, bd = 1e9;
        document.querySelectorAll('.sc').forEach((c, i) => { const r = c.getBoundingClientRect(), d = Math.abs(r.left + r.width / 2 - mid); if (d < bd) { bd = d; best = i; } });
        if (best >= 0 && best !== sel) { closeSheet(); pick(best, true); }
      }, 160);
    }, { passive: true });
  })();
  function strip() {
    // each card: the story (tap to select) + a slot where the outlet list opens when it's the selected story
    $('strip').innerHTML = stories.map((s, i) => `<div class="sc" style="--c:${COLORS[i % COLORS.length]}">
      <div class="sc-top" role="button" tabindex="0">${s.image ? `<img src="${esc(s.image)}" alt="" referrerpolicy="no-referrer">` : '<span class="ph"></span>'}
      <span class="tx"><span class="hd">${esc(s.title)}</span><span class="mt"><span class="rk">${s.rank}</span><span class="pl">${s.origin ? `${flag(s.origin.country)} ${esc(s.origin.how === 'first' ? placeShort(s.origin) : s.origin.name)}` : ''}<span class="cnt">${s.origin ? ' · ' : ''}${s.outlets} outlets · ${s.countries} countries</span></span></span>
      <span class="mt2">${s.outlets} outlets · ${s.countries} countries</span></span></div>
      <div class="sc-slot"></div></div>`).join('');
    document.querySelectorAll('.sc-top').forEach((b, i) => b.addEventListener('click', () => { closeSheet(); pick(i, true); }));
    document.querySelectorAll('.sc img').forEach(im => im.addEventListener('error', () => { const ph = document.createElement('span'); ph.className = 'ph'; im.replaceWith(ph); }));
  }

  function start() {
    if (typeof Globe !== 'function') { $('empty').textContent = 'The globe couldn’t load on this device.'; return; }
    world = new Globe($('globe'), { animateIn: true })
      .backgroundColor('rgba(0,0,0,0)')
      .globeImageUrl('/globe/earth-blue-marble.jpg')
      .showAtmosphere(true).atmosphereColor('#8ab4ff').atmosphereAltitude(0.18)
      .htmlElementsData(marks).htmlLat('lat').htmlLng('lng').htmlAltitude(0.01).htmlElement(pinEl).htmlTransitionDuration(0)
      .htmlElementVisibilityModifier(() => {})
      .arcColor('color').arcStroke(0.45).arcDashLength(0.5).arcDashGap(0.25).arcDashAnimateTime(2200).arcAltitudeAutoScale(0.35)
      .ringColor(r => t => `rgba(${hexRgb(r.color)},${1 - t})`).ringMaxRadius(5).ringPropagationSpeed(2.5).ringRepeatPeriod(1100)
      // tapping the globe only closes an open article card or preview; a story is deselected by tapping it again
      // (its card or its circle), so a missed tap on the globe never throws you out of the story
      .onGlobeClick(() => {
        if (Date.now() - pinTapAt < 400) return;
        if ($('sheet').classList.contains('in')) { closeSheet(); return; }
        focusPin(null);
      });
    const c = world.controls(); c.autoRotate = true; c.autoRotateSpeed = 0.45; c.enableDamping = true;
    // Pins only show on the side of the Earth facing you (with a margin, so none float past the edge)
    const R = Math.PI / 180;
    const vis = () => { const v = world.pointOfView(), a = v.lat * R, b = v.lng * R;
      const hb = (document.querySelector('.top')?.getBoundingClientRect().bottom || 0) - 8;
      for (const p of marks) { if (!p.el) continue; const la = p.lat * R; const d = Math.sin(a) * Math.sin(la) + Math.cos(a) * Math.cos(la) * Math.cos(p.lng * R - b);
        // also hide markers sliding under the title bar
        const under = d >= 0.3 && p.el.getBoundingClientRect().top < hb && !p.el.classList.contains('focus');
        p.el.classList.toggle('back', d < 0.3 || under); } };
    c.addEventListener('change', vis); setTimeout(vis, 50); setInterval(vis, 500);
    world.renderer().domElement.addEventListener('pointerdown', () => { c.autoRotate = false; });
    c.addEventListener('change', () => { if (!olQ) olQ = requestAnimationFrame(() => { olQ = 0; overviewLabels(); }); });
    // double-tap: zoom in on that spot; when already close, zoom back out to the whole globe
    // no text-selection highlight from double-taps (Safari selects the whole page otherwise)
    document.addEventListener('dblclick', ev => { ev.preventDefault(); try { getSelection().removeAllRanges(); } catch (er) {} });
    (function doubleTap() {
      const cv = world.renderer().domElement; let down = null, last = null;
      cv.addEventListener('pointerdown', e => { down = { x: e.clientX, y: e.clientY, t: Date.now() }; });
      cv.addEventListener('pointerup', e => {
        if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 10 || Date.now() - down.t > 350) { down = null; return; }
        const now = Date.now();
        if (last && now - last.t < 330 && Math.hypot(e.clientX - last.x, e.clientY - last.y) < 40) {
          last = null; pinTapAt = now;
          try { getSelection().removeAllRanges(); } catch (er) {}
          const pov = world.pointOfView(), r = cv.getBoundingClientRect();
          if (pov.altitude < 0.75) { world.pointOfView({ altitude: HOME_ALT() }, 700); return; }
          const g = world.toGlobeCoords(e.clientX - r.left, e.clientY - r.top);
          world.pointOfView({ ...(g ? { lat: g.lat, lng: g.lng } : {}), altitude: Math.max(0.6, pov.altitude * 0.5) }, 700);
        } else last = { x: e.clientX, y: e.clientY, t: now };
        down = null;
      });
    })();
    const fit = () => { world.width(innerWidth).height(innerHeight); };
    fit(); addEventListener('resize', fit);
    world.pointOfView({ lat: 22, lng: 20, altitude: innerWidth < 600 ? 2.9 : 2.2 });
  }
  // Outlet labels: hide any that would overlap one already shown (checked a few times a second)
  function declutter() {
    const shown = [];
    for (const p of [...events, ...pins]) {
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
    pins = stories.flatMap((s, i) => s.posts.map(p => ({ ...p, s: i, lat0: p.lat, lng0: p.lng })));
    spread(pins);
    events = stories.map((s, i) => s.origin && isFinite(s.origin.lat) ? { kind: 'ev', s: i, lat: +s.origin.lat, lng: +s.origin.lng, name: s.origin.how === 'first' ? `First reported in ${s.origin.city}` : s.origin.name, country: s.origin.country } : null).filter(Boolean);
    spread(events);
    // story markers that sit close together (Liverpool, Manchester, London…) get nudged apart so each can be tapped
    for (let k = 0; k < 40; k++) for (let i = 0; i < events.length; i++) for (let j = i + 1; j < events.length; j++) {
      const A = events[i], B = events[j], cl = Math.cos(((A.lat + B.lat) / 2) * Math.PI / 180);
      let dx = (B.lng - A.lng) * cl, dy = B.lat - A.lat; const d = Math.hypot(dx, dy) || 0.01, min = 5;
      if (d >= min) continue; if (d < 0.02) { dx = 1; dy = 0.3; }
      const push = (min - d) / 2 / (Math.hypot(dx, dy) || 1);
      A.lat -= dy * push; B.lat += dy * push; A.lng -= dx * push / cl; B.lng += dx * push / cl;
    }
    marks = [...pins, ...events];
    if (d.built_at) $('sub').textContent = `Last 24 hours · ${stories.length} top stories · updated ${ago(d.built_at)}`;
    $('empty').remove();
    if (!stories.length) { $('sub').textContent = 'No trending stories yet — check back soon'; }
    strip(); start();
  }).catch(() => { $('empty').textContent = 'Couldn’t load the stories. Try again in a moment.'; });
})();
