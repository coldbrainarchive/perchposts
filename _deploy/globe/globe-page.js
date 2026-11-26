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

  // Stars behind the globe
  (function stars() {
    const c = $('stars'), d = Math.min(2, devicePixelRatio || 1);
    const draw = () => { c.width = innerWidth * d; c.height = innerHeight * d; const x = c.getContext('2d'); x.clearRect(0, 0, c.width, c.height);
      for (let i = 0; i < 220; i++) { x.globalAlpha = Math.random() * 0.7 + 0.15; x.fillStyle = '#fff'; x.beginPath(); x.arc(Math.random() * c.width, Math.random() * c.height, Math.random() * 1.1 * d, 0, 7); x.fill(); } };
    draw(); addEventListener('resize', draw);
  })();

  let olQ = 0;
  let stories = [], pins = [], events = [], marks = [], sel = -1, world = null, pinTapAt = 0, foc = null, progScroll = 0, curList = [], rsAt = -1, pvOpen = true;
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
      <div class="pv-more"><a class="pv-site" href="${esc(p.url)}" target="_blank" rel="noopener noreferrer">${esc(siteOf(p.url))}</a>${p.desc ? `<p>${esc(p.desc)}</p>` : ''}<div class="pv-acts"><button type="button" class="pa fl" aria-label="Flap">${IC.flap}<b></b></button><a class="pa ch" href="/post/${encodeURIComponent(p.id)}?chat=1&via=card" aria-label="Chirps">${IC.chat}<b></b></a><button type="button" class="pa shr" aria-label="Share">${IC.share}<b></b></button></div></div></div>`;
    fillActs(p, el);
    const im = el.querySelector('.pv img'); im && im.addEventListener('error', () => im.remove());
    el.addEventListener('pointerdown', ev => { ev.stopPropagation(); });
    el.addEventListener('click', ev => {
      ev.stopPropagation(); pinTapAt = Date.now();
      const nav = ev.target.closest('.pv-nav');
      if (nav) { stepOutlet(p, +nav.dataset.d); return; }
      if (ev.target.closest('.pv-btns a,.pv-site,.pa.ch')) return;     // let the links open
      if (ev.target.closest('.pa.fl')) { flap(p); return; }
      if (ev.target.closest('.pa.shr')) { share(p); return; }
      if (foc === p) { pvOpen = el.querySelector('.pv').classList.toggle('exp'); return; }
      focusPin(p, false);
    });
    p.el = el;
    return el;
  }

  // Flaps · chirps · share on each article preview (in place of a View post button). Counts are live, loaded for a
  // story's articles when one of its pins is focused; chirps opens the post's chat; flap / share work right here.
  const IC = {
    flap: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 13.5C4 9.5 8.5 8.5 12 15C15.5 8.5 20 9.5 22 13.5"><animate attributeName="d" dur=".75s" begin="indefinite" fill="remove" calcMode="spline" keyTimes="0;.17;.33;.5;.67;.83;1" keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1" values="M2 13.5C4 9.5 8.5 8.5 12 15C15.5 8.5 20 9.5 22 13.5;M4.5 7C6 5 9.5 6 12 15C14.5 6 18 5 19.5 7;M2 13.5C4 9.5 8.5 8.5 12 15C15.5 8.5 20 9.5 22 13.5;M3 18C4.5 14.5 8.5 13 12 15C15.5 13 19.5 14.5 21 18;M2 13.5C4 9.5 8.5 8.5 12 15C15.5 8.5 20 9.5 22 13.5;M4.5 7C6 5 9.5 6 12 15C14.5 6 18 5 19.5 7;M2 13.5C4 9.5 8.5 8.5 12 15C15.5 8.5 20 9.5 22 13.5"/></path></svg>',
    chat: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 11.5c0 4.4-3.8 8-8.5 8-1.2 0-2.4-.2-3.4-.7L4 20l1.3-3.6c-1.1-1.4-1.8-3.1-1.8-4.9 0-4.4 3.8-8 8.5-8s8.5 3.6 8.5 8z"/></svg>',
    share: '<svg viewBox="5 5 14 14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M11 7h6v6"/></svg>',
    huddle: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 8.5c0 3.3-2.9 6-6.5 6-.9 0-1.8-.2-2.6-.5L2.5 15l1-2.6C2.9 11.3 2.5 10 2.5 8.5c0-3.3 2.9-6 6-6s6 2.7 6 6z"/><path d="M17 9.6c2.7.6 4.5 2.8 4.5 5.4 0 1.3-.4 2.5-1.1 3.4l.9 2.6-2.9-1c-.8.3-1.6.5-2.5.5-2.5 0-4.6-1.3-5.5-3.2"/></svg>',
    link: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
    up: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>'
  };
  const cnt = new Map(), asked = new Set();
  const tok = () => { try { return localStorage.getItem('auth_token') || ''; } catch (e) { return ''; } };
  const hdr = () => tok() ? { Authorization: 'Bearer ' + tok() } : {};
  function fillActs(p, el) {
    el = el || p.el; const c = cnt.get(p.id); if (!el || !c) return;
    const f = el.querySelector('.pa.fl'), ch = el.querySelector('.pa.ch'), sh = el.querySelector('.pa.shr');
    if (f) { f.querySelector('b').textContent = c.f; f.classList.toggle('on', !!c.m); }
    if (ch) ch.querySelector('b').textContent = c.c;
    if (sh && !sh.classList.contains('said')) sh.querySelector('b').textContent = c.s > 0 ? c.s : '';
  }
  function loadCounts(s) {
    const ids = pins.filter(q => q.s === s && q.id && !asked.has(q.id)).map(q => q.id).slice(0, 40);
    if (!ids.length) return;
    ids.forEach(id => asked.add(id));
    fetch(API + '/globe-counts?ids=' + ids.map(encodeURIComponent).join(','), { headers: hdr() }).then(r => r.json()).then(d => {
      for (const [id, c] of Object.entries(d.posts || {})) cnt.set(id, c);
      pins.forEach(q => ids.includes(q.id) && fillActs(q));
    }).catch(() => ids.forEach(id => asked.delete(id)));
  }
  function flap(p) {
    if (!tok()) { toast('Sign in to flap', true); return; }
    const c = cnt.get(p.id) || { f: 0, m: 0, c: 0, s: 0 }, v = c.m ? 0 : 1;
    if (v && p.el) p.el.querySelectorAll('.pa.fl animate').forEach(a => { try { a.endElement && a.endElement(); a.beginElement(); } catch (e) {} });
    let bid = ''; try { bid = localStorage.getItem('browser_id') || ''; if (!bid) { bid = crypto.randomUUID(); localStorage.setItem('browser_id', bid); } } catch (e) { bid = 'globe'; }
    cnt.set(p.id, { ...c, m: v, f: Math.max(0, c.f + (v ? 1 : -1)) }); fillActs(p);
    fetch(API + '/vote-post', { method: 'POST', headers: { 'Content-Type': 'application/json', ...hdr() }, body: JSON.stringify({ post_id: p.id, browser_id: bid, value: v, username: (() => { try { return localStorage.getItem('mod_name') || undefined; } catch (e) { return undefined; } })() }) })
      .then(r => r.json().then(j => ({ ok: r.ok, j }))).then(({ ok, j }) => {
        if (ok && j.success) cnt.set(p.id, { ...cnt.get(p.id), f: j.score, m: j.myVote === 1 ? 1 : 0 });
        else cnt.set(p.id, c);
        fillActs(p);
      }).catch(() => { cnt.set(p.id, c); fillActs(p); });
  }
  function share(p) {
    const u = location.origin + '/post/' + p.id;
    if (tok()) { shareSheet(p, u); return; }
    const say = t => { const b = p.el && p.el.querySelector('.pa.shr'); if (!b) return; b.classList.add('said'); b.querySelector('b').textContent = t;
      clearTimeout(b._sayT); b._sayT = setTimeout(() => { b.classList.remove('said'); fillActs(p); if (!cnt.get(p.id)) b.querySelector('b').textContent = ''; }, 1800); };
    (async () => {
      try {
        if (navigator.share) { await navigator.share({ url: u }); say('Shared'); }
        else if (navigator.clipboard && navigator.clipboard.writeText) { await navigator.clipboard.writeText(u); say('Copied'); }
        else say('Link ready');
      } catch (e) { if (!e || e.name !== 'AbortError') say('Share failed'); }
    })();
  }

  function shared(p, via) {
    fetch(API + '/share', { method: 'POST', headers: { 'Content-Type': 'application/json', ...hdr() }, body: JSON.stringify({ post_id: p.id, via }) })
      .then(r => r.ok ? r.json() : null).then(j => { if (j && j.share_count != null) { const c = cnt.get(p.id); if (c) { c.s = j.share_count; fillActs(p); } } }).catch(() => {});
  }
  // the site's Share sheet (_ShareSheet in the main bundle, v1377), copied one-for-one: tap or drag the top bar down to
  // close, tap outside / Escape closes, keyboard lift, "Sent ✓" / error inside the message bubble, "Copied ✓" button.
  const CHK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  function shareSheet(p, u) {
    if (document.querySelector('.ps-ov')) return;
    const id = p.id, url = u;
    let me = ''; try { me = (localStorage.getItem('_myUsername') || '').toLowerCase(); } catch (e) {}
    let hs = null, sel = [], msg = '', busy = false, note = '', copied = false, sent = '', err = '', gone = false;
    const ov = document.createElement('div'); ov.className = 'ps-ov';
    try { const m0 = localStorage.getItem('_myUsername'); if (m0 && window._ppKit) ov.style.setProperty('--me', window._ppKit.tagCol(m0)); } catch (e) {}
    ov.innerHTML = `<div class="ps-sheet" role="dialog" aria-label="Share"><div class="ps-grabz" role="button" aria-label="Close"><div class="ps-grab"></div></div><div class="ps-lbl">Send to a huddle</div><div class="ps-list"></div><div class="ps-msgw"></div><div class="ps-sep"></div><div class="ps-lns"></div><div class="ps-notew"></div></div>`;
    document.body.appendChild(ov);
    const $q = s => ov.querySelector(s), sheet = $q('.ps-sheet');
    const unkb = () => document.documentElement.classList.remove('ps-kb');
    const close = () => { unkb(); setTimeout(() => ov.remove(), 0); };
    const bye = () => { if (gone) return; gone = true; ov.classList.remove('in'); removeEventListener('keydown', k); vv && (vv.removeEventListener('resize', fit), vv.removeEventListener('scroll', fit)); setTimeout(close, 240); };
    const k = ev => { ev.key === 'Escape' && bye(); };
    addEventListener('keydown', k);
    requestAnimationFrame(() => ov.classList.add('in'));
    // keyboard: lift the sheet above it
    const vv = window.visualViewport;
    const fit = () => { const kb = Math.max(0, Math.round(innerHeight - vv.height - vv.offsetTop)); sheet.style.paddingBottom = kb > 40 ? `calc(16px + ${kb}px)` : ''; };
    if (vv) { fit(); vv.addEventListener('resize', fit); vv.addEventListener('scroll', fit); }
    ov.addEventListener('pointerdown', ev => ev.stopPropagation());
    ov.addEventListener('click', ev => { ev.stopPropagation(); bye(); });
    sheet.addEventListener('click', ev => ev.stopPropagation());
    // the top bar: tap closes; drag down closes (70px, or a quick flick)
    const gz = $q('.ps-grabz'); let dg = null;
    gz.addEventListener('click', bye);
    gz.addEventListener('touchstart', ev => { try { document.activeElement && document.activeElement.blur(); } catch (e) {} dg = { y: ev.touches[0].clientY, t: Date.now(), dy: 0 }; sheet.style.transition = 'none'; });
    gz.addEventListener('touchmove', ev => { if (!dg) return; dg.dy = Math.max(0, ev.touches[0].clientY - dg.y); sheet.style.transform = `translateY(${dg.dy}px)`; });
    const dE = () => { const d = dg; dg = null; if (!d) return; sheet.style.transition = ''; const v = d.dy / Math.max(1, Date.now() - d.t); if (d.dy > 70 || (d.dy > 18 && v > .5)) { sheet.style.transform = 'translateY(100%)'; bye(); } else sheet.style.transform = ''; };
    gz.addEventListener('touchend', dE); gz.addEventListener('touchcancel', dE);
    const done = t => { note = t; drawNote(); setTimeout(bye, 850); };

    const drawList = () => {
      const box = $q('.ps-list'), sx = box.querySelector('.ps-hds') ? box.querySelector('.ps-hds').scrollLeft : 0;
      box.innerHTML = hs === null ? `<div class="ps-empty">Loading…</div>` : !hs.length ? `<div class="ps-empty">You're not in any huddles yet.</div>` :
        `<div class="ps-hds">${hs.map(h => `<button type="button" class="ps-hd${sel.includes(h.id) ? ' on' : ''}" data-id="${esc(h.id)}" aria-pressed="${sel.includes(h.id)}"><span class="ps-av">${avHtml(h)}</span><span class="ps-nm">${esc(h.title)}</span></button>`).join('')}</div>`;
      if (sx && box.querySelector('.ps-hds')) box.querySelector('.ps-hds').scrollLeft = sx;
    };
    ov._redraw = drawList;
    const drawMsg = () => {
      const w = $q('.ps-msgw');
      if (!sel.length) { w.innerHTML = ''; return; }
      if (!w.firstChild) {
        w.innerHTML = `<div class="ps-msg"><div class="ps-bub"></div><button type="button" class="ps-send">${IC.up}</button></div>`;
        w.querySelector('.ps-send').addEventListener('click', send);
      }
      const bub = w.querySelector('.ps-bub'), sb = w.querySelector('.ps-send');
      bub.className = 'ps-bub' + (sent ? ' ok' : err ? ' bad' : '');
      sb.disabled = busy; sb.setAttribute('aria-label', sel.length > 1 ? `Send to ${sel.length} huddles` : 'Send');
      const mode = sent ? 's' : err ? 'e' : 'i';
      if (bub.dataset.m === mode && mode === 'i') return;
      bub.dataset.m = mode;
      if (sent) bub.innerHTML = `<span class="ps-sent" role="status"><span class="ps-chk">${CHK}</span>${esc(sent)}</span>`;
      else if (err) { bub.innerHTML = `<span class="ps-err" role="alert">${esc(err)}</span>`; bub.firstChild.addEventListener('click', () => { err = ''; drawMsg(); }); }
      else {
        bub.innerHTML = `<input type="search" name="search_ps_msg" autocomplete="off" enterkeyhint="send" placeholder="Add a message…" maxlength="1000">`;
        const inp = bub.firstChild; inp.value = msg;
        inp.addEventListener('input', () => { msg = inp.value; });
        inp.addEventListener('focus', () => document.documentElement.classList.add('ps-kb'));
        inp.addEventListener('blur', () => setTimeout(() => { const a = document.activeElement; if (!(a && a.closest && a.closest('.ps-sheet') && a.tagName === 'INPUT')) unkb(); }, 50));
        inp.addEventListener('keydown', ev => { if (ev.key === 'Enter') { ev.preventDefault(); send(); } });
      }
    };
    const drawLns = () => {
      $q('.ps-lns').innerHTML = (copied ? `<button type="button" class="ps-ln ok"><span class="ps-chk">${CHK}</span>Copied</button>` : `<button type="button" class="ps-ln" data-k="copy"><span style="display:inline-flex">${IC.link}</span>Copy link</button>`) +
        `<button type="button" class="ps-ln" data-k="more"><span style="display:inline-flex">${IC.share}</span>More…</button>`;
    };
    const drawNote = () => { $q('.ps-notew').innerHTML = note ? `<div class="ps-note" role="status">${esc(note)}</div>` : ''; };

    $q('.ps-list').addEventListener('click', ev => { const b = ev.target.closest('.ps-hd'); if (!b) return; const h = b.dataset.id; sel = sel.includes(h) ? sel.filter(x => x !== h) : [...sel, h]; drawList(); drawMsg(); });
    $q('.ps-lns').addEventListener('click', ev => { const b = ev.target.closest('[data-k]'); if (!b) return; b.dataset.k === 'copy' ? copy() : more(); });
    const copy = async () => { try { await navigator.clipboard.writeText(url); copied = true; drawLns(); shared(p, 'copy'); setTimeout(bye, 900); } catch (e) { err = "Couldn't copy the link"; drawMsg(); } };
    const more = async () => { try { if (navigator.share) { await navigator.share({ url }); shared(p, 'more'); bye(); } else { await navigator.clipboard.writeText(url); copied = true; drawLns(); shared(p, 'copy'); setTimeout(bye, 900); } } catch (e) {} };
    async function send() {
      if (!sel.length || busy) return; busy = true; err = ''; drawMsg();
      let ok = 0, er2 = ''; const att = '\n\n[ATTACH:' + JSON.stringify({ type: 'post', id }) + ']';
      let bid = ''; try { bid = localStorage.getItem('browser_id') || ''; if (!bid) { bid = crypto.randomUUID(); localStorage.setItem('browser_id', bid); } } catch (e) {}
      for (const h of sel) {
        try {
          const r = await fetch(API + '/add-comment', { method: 'POST', headers: { 'Content-Type': 'application/json', ...hdr() }, body: JSON.stringify({ content: msg.trim() + att, post_id: h, parent_comment_id: null, browser_id: bid }) });
          if (r.ok) ok++; else { const j = await r.json().catch(() => ({})); er2 = j.error || "Couldn't send"; }
        } catch (e) { er2 = "Couldn't send"; }
      }
      busy = false;
      if (ok) { shared(p, 'huddle'); const one = sel.length === 1 && (hs || []).find(x => x.id === sel[0]); try { document.activeElement && document.activeElement.blur(); } catch (e) {} sent = `Sent to ${one ? one.title : ok + ' huddles'}`; drawMsg(); setTimeout(bye, 1100); }
      else { err = er2 === 'Caged' ? "You're Caged: you can only chirp in The Cage" : er2; drawMsg(); }
    }
    drawList(); drawMsg(); drawLns(); drawNote();
    loadKit(() => { drawList(); try { const m0 = localStorage.getItem('_myUsername'); if (m0) ov.style.setProperty('--me', window._ppKit.tagCol(m0)); } catch (e) {} });
    fetch(API + '/my-huddles', { headers: hdr() }).then(r => r.ok ? r.json() : { huddles: [] }).then(x => { hs = x.huddles || []; drawList(); }).catch(() => { hs = []; drawList(); });
  }
  // huddle circles show the members' birds, like the site: two birds (or one), drawn by the site's bird kit
  let kitCbs = null;
  function loadKit(cb) {
    if (window._ppKit) return;
    if (kitCbs) { kitCbs.push(cb); return; }
    kitCbs = [cb]; const s = document.createElement('script'); s.src = '/globe/birdkit.js?v=1403';
    s.onload = () => { const l = kitCbs; kitCbs = []; l.forEach(f => f()); }; document.head.appendChild(s);
  }
  const admins = (() => { try { return new Set(JSON.parse(localStorage.getItem('_au') || '[]')); } catch (e) { return new Set(); } })();
  const kitWait = new Set();
  function face(name, z) {
    const l = String(name || '').toLowerCase();
    const K = window._ppKit; if (!K) return `<span style="display:inline-block;width:${z}px;height:${z}px"></span>`;
    const adm = admins.has(l); if (adm) name = 'admin';
    let h = 0; for (let i = 0; i < name.length; i++) h = name.charCodeAt(i) + ((h << 5) - h);
    const em = adm ? 'A' : ['🐤', '🐦', '🐧'][Math.abs(h) % 3], r = K.get(name, em, 't');
    if (adm && r && r.fail) return `<img src="/admin-bird.png" alt="" style="width:${z}px;height:${z}px;object-fit:contain;display:block">`;
    if (r && !r.fail && r.t) { const w = z * (1 + 2 * (r.g || 0)); return `<img src="${r.t}" alt="" draggable="false" style="width:${w}px;height:${w}px;margin:${-(w - z) / 2}px;display:block;max-width:none;pointer-events:none;flex-shrink:0">`; }
    if (!r && !kitWait.has(name)) { kitWait.add(name); K.sub(name, em, () => { const ov = document.querySelector('.ps-ov'); ov && ov._redraw && ov._redraw(); }, 't'); }
    return `<span style="display:inline-block;width:${z}px;height:${z}px"></span>`;
  }
  function avHtml(h) {
    let me = ''; try { me = (localStorage.getItem('_myUsername') || '').toLowerCase(); } catch (e) {}
    const o = (h.members || []).filter(n => n && n.toLowerCase() !== me).slice(0, 2);
    if (o.length === 2) return `<span class="ps-b ps-b1">${face(o[0], 26)}</span><span class="ps-b ps-b2">${face(o[1], 26)}</span>`;
    if (o.length === 1) return `<span class="ps-solo">${face(o[0], 34)}</span>`;
    return `<span class="ps-hi">${IC.huddle}</span>`;
  }

  // the site's "sign in" nudge (signed-out flap): a small toast with a Sign in button
  let toastT = 0;
  function toast(t, signIn) {
    let el = document.querySelector('.g-toast');
    if (!el) { el = document.createElement('div'); el.className = 'g-toast'; document.body.appendChild(el); el.addEventListener('pointerdown', ev => ev.stopPropagation()); }
    el.innerHTML = `<span>${esc(t)}</span>${signIn ? '<a href="/?signin=1">Sign in</a>' : ''}`;
    requestAnimationFrame(() => el.classList.add('in'));
    clearTimeout(toastT); toastT = setTimeout(() => el.classList.remove('in'), 2600);
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
    if (!p) pvOpen = true;  // opens expanded by default (user, 2026-11-24)
    foc = p;
    if (p && p.el && pvOpen) p.el.querySelector('.pv').classList.add('exp');
    for (const q of pins) q.el && q.el.classList.toggle('focus', q === p);
    document.body.classList.toggle('focusing', !!p);
    document.querySelectorAll('.or').forEach(b => b.classList.toggle('on', b._p === p));
    if (!p) return;
    loadCounts(p.s);
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
    $('olT').innerHTML = `See all ${sp.length} outlet${sp.length === 1 ? '' : 's'}`;
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
      <span class="tx"><span class="hd">${esc(s.title)}</span><span class="mt"><span class="rk">${s.rank}</span><span class="pl">${s.origin ? `${flag(s.origin.country)} ${esc(s.origin.how === 'first' ? placeShort(s.origin) : s.origin.name)}` : ''}<span class="cnt">${s.origin ? ' · ' : ''}${(s.posts || []).length || s.outlets} outlet${((s.posts || []).length || s.outlets) === 1 ? '' : 's'} · ${s.countries} countries</span></span></span>
      <span class="mt2">${(s.posts || []).length || s.outlets} outlet${((s.posts || []).length || s.outlets) === 1 ? '' : 's'} · ${s.countries} countries</span></span></div>
      <div class="sc-slot"></div></div>`).join('');
    document.querySelectorAll('.sc-top').forEach((b, i) => b.addEventListener('click', () => { closeSheet(); pick(i, true); }));
    document.querySelectorAll('.sc img').forEach(im => im.addEventListener('error', () => { const ph = document.createElement('span'); ph.className = 'ph'; im.replaceWith(ph); }));
  }

  function start() {
    if (typeof Globe !== 'function') { $('empty').textContent = 'The globe couldn’t load on this device.'; return; }
    world = new Globe($('globe'), { animateIn: true })
      .backgroundColor('rgba(0,0,0,0)')
      .globeImageUrl('/globe/earth-s2-4k.jpg')
      .onGlobeReady(() => { const l = $('glLoad'); l && l.classList.add('gone'); setTimeout(() => l && l.remove(), 400); hiRes();
        // the birds on the globe fade in once it's there (before, their dots showed through the half-loaded globe)
        setTimeout(() => document.body.classList.add('gl-ready'), 1700); })
      .globeTileEngineMaxLevel(14)
      .showAtmosphere(true).atmosphereColor('#8ab4ff').atmosphereAltitude(0.18)
      .htmlElementsData(marks).htmlLat('lat').htmlLng('lng').htmlAltitude(0.01).htmlElement(pinEl).htmlTransitionDuration(0)
      .htmlElementVisibilityModifier(() => {})
      .arcColor('color').arcStroke(0.45).arcDashLength(0.5).arcDashGap(0.25).arcDashAnimateTime(2200).arcAltitudeAutoScale(0.35)
      .ringColor(r => t => `rgba(${hexRgb(r.color)},${1 - t})`).ringMaxRadius(5).ringPropagationSpeed(2.5).ringRepeatPeriod(1100)
      // tapping the globe only closes an open article card or preview; a story is deselected by tapping it again
      // (its card or its circle), so a missed tap on the globe never throws you out of the story
      .onGlobeClick(() => {
        if (document.body.classList.contains('hunting') || Date.now() - pinTapAt < 400) return;
        if ($('sheet').classList.contains('in')) { closeSheet(); return; }
        focusPin(null);
      });
    if (location.hash === '#dbg') window._gw = world;   // test hook: lets an automated check move the camera (only with #dbg)
    const c = world.controls(); c.autoRotate = true; c.autoRotateSpeed = 0.45; c.enableDamping = true;
    // Pins only show on the side of the Earth facing you (with a margin, so none float past the edge)
    const R = Math.PI / 180;
    const vis = () => { if (inGame()) return; const v = world.pointOfView(), a = v.lat * R, b = v.lng * R;
      const hb = (document.querySelector('.top')?.getBoundingClientRect().bottom || 0) - 8;
      for (const p of marks) { if (!p.el) continue; const la = p.lat * R; const d = Math.sin(a) * Math.sin(la) + Math.cos(a) * Math.cos(la) * Math.cos(p.lng * R - b);
        // also hide markers sliding under the title bar
        const under = d >= 0.3 && p.el.getBoundingClientRect().top < hb && !p.el.classList.contains('focus');
        p.el.classList.toggle('back', d < 0.3 || under); } };
    c.addEventListener('change', vis); setTimeout(vis, 50); setInterval(vis, 500);
    world.renderer().domElement.addEventListener('pointerdown', () => { c.autoRotate = false; });
    c.addEventListener('change', () => { if (inGame()) return; if (!olQ) olQ = requestAnimationFrame(() => { olQ = 0; overviewLabels(); }); });
    // double-tap: zoom in on that spot; when already close, zoom back out to the whole globe
    // no text-selection highlight from double-taps (Safari selects the whole page otherwise)
    document.addEventListener('dblclick', ev => { ev.preventDefault(); try { getSelection().removeAllRanges(); } catch (er) {} });
    (function doubleTap() {
      const cv = world.renderer().domElement; let down = null, last = null;
      cv.addEventListener('pointerdown', e => { down = { x: e.clientX, y: e.clientY, t: Date.now() }; });
      cv.addEventListener('pointerup', e => {
        if (!down || document.body.classList.contains('hunting') || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 10 || Date.now() - down.t > 350) { down = null; return; }
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
    // Imagery is Sentinel-2 cloudless (EOX, CC BY-NC-SA) at every zoom, so nothing changes colour as you zoom:
    // a whole-Earth image (4K; computers swap to 8K once it has loaded in the background), then map tiles through
    // our worker (cached there; phones never contact EOX) once you zoom in past what the whole-Earth image can show.
    // Tiles are one level finer than the engine's default and only the ones in view load; a small bird shows while
    // they arrive. Switches with a little gap so it doesn't flicker.
    const BIG = matchMedia('(pointer: fine)').matches && innerWidth >= 900;
    const ON = BIG ? 0.5 : 0.85, OFF = ON + 0.15;
    let pend = 0, sbT = 0;
    const small = $('glLoadS');
    const busy = () => { clearTimeout(sbT); if (pend > 0) sbT = setTimeout(() => small && small.classList.toggle('on', pend > 0), 350); else small && small.classList.remove('on'); };
    // the closest levels (13+, Take flight height) use the sharp Esri imagery when the server has it switched on
    tileSrc = (x, y, l) => hdOn && l >= HD_FROM ? `${API}/globe-hd/${l}/${y}/${x}.jpg` : `${API}/globe-tile/${l}/${y}/${x}.jpg`;
    const TILE = (x, y, l) => { pend++; busy(); return tileSrc(x, y, l); };
    try { new PerformanceObserver(list => { for (const e of list.getEntries()) if (e.name.includes('/globe-tile/')) pend = Math.max(0, pend - 1); busy(); }).observe({ type: 'resource', buffered: false }); } catch (e) {}
    // the library hides the whole-Earth image as soon as tiles switch on, which flashed black until they arrived:
    // keep it always showing underneath (a hair smaller, so tiles sit cleanly on top) — same imagery, so no seam
    const keepBase = () => { try { world.scene().traverse(o => { if (o && o.__globeObjType === 'globe' && o.children) { const g = o.children.find(m => m.isMesh); if (g && !g._kept) { g._kept = true; g.scale.setScalar(0.9992); g.renderOrder = -200; Object.defineProperty(g, 'visible', { get: () => true, set: () => {}, configurable: true }); } } }); } catch (e) {} };
    keepBase();
    let tilesOn = false, tuned = false, te = null, lastA = 9, outT = 0;
    const imagery = () => { const a = world.pointOfView().altitude;
      // zooming OUT: stop asking for new tiles (the ones already there stay; the whole-Earth image underneath has the
      // same colours) and resume once the zoom settles — otherwise every in-between level gets fetched and thrown away
      if (te && tilesOn && !document.body.classList.contains('hunting')) { if (a > lastA * 1.004) { te.tileUrl = null; clearTimeout(outT); outT = setTimeout(() => { if (tilesOn) { te.tileUrl = TILE; try { te.updatePov(world.camera()); } catch (e) {} lastA = world.pointOfView().altitude; } }, 250); } }   // (asks the tiles to look again without moving the camera: the old 1e-5 nudge counted as another zoom-out very close in and crept the view outwards by itself)
      lastA = a;
      if (!tilesOn && a < ON) { tilesOn = true; keepBase(); world.globeTileEngineUrl(TILE);
        if (!tuned) { try { world.scene().traverse(o => { if (!tuned && o && Array.isArray(o.thresholds) && 'tileUrl' in o) { o.thresholds = o.thresholds.map((v, i) => 8 / Math.pow(2, i - 1)); tuned = true; te = o; tileEng = o; tileHooks(o); } }); } catch (e) {} } }
      else if (tilesOn && a > OFF) { tilesOn = false; clearTimeout(outT); world.globeTileEngineUrl(null); try { world.globeTileEngineClearCache(); } catch (e) {} pend = 0; busy(); } };
    world.controls().addEventListener('change', imagery); setInterval(imagery, 500);
    try { world.onZoom(() => { imagery(); }); } catch (e) {}  // also during animated flights (double-tap, story picks)
    mapOverlay();
    dayNight();
    hunt();
    const fit = () => { world.width(innerWidth).height(innerHeight); };
    fit(); addEventListener('resize', fit);
    world.pointOfView({ lat: 22, lng: 20, altitude: innerWidth < 600 ? 2.9 : 2.2 });
  }
  // Where the sun is overhead right now (NOAA approximation, good to a fraction of a degree)
  function subsolar(d = new Date()) {
    const R = Math.PI / 180, y0 = Date.UTC(d.getUTCFullYear(), 0, 0), day = Math.floor((d - y0) / 864e5);
    const hrs = d.getUTCHours() + d.getUTCMinutes() / 60 + d.getUTCSeconds() / 3600, g = 2 * Math.PI / 365 * (day - 1 + (hrs - 12) / 24);
    const eqt = 229.18 * (0.000075 + 0.001868 * Math.cos(g) - 0.032077 * Math.sin(g) - 0.014615 * Math.cos(2 * g) - 0.040849 * Math.sin(2 * g));
    const decl = 0.006918 - 0.399912 * Math.cos(g) + 0.070257 * Math.sin(g) - 0.006758 * Math.cos(2 * g) + 0.000907 * Math.sin(2 * g) - 0.002697 * Math.cos(3 * g) + 0.00148 * Math.sin(3 * g);
    return { lat: decl / R, lng: ((-15 * (hrs - 12 + eqt / 60)) + 540) % 360 - 180 };
  }
  const isDay = (lat, lng, s = subsolar()) => { const R = Math.PI / 180; return Math.sin(lat * R) * Math.sin(s.lat * R) + Math.cos(lat * R) * Math.cos(s.lat * R) * Math.cos((lng - s.lng) * R) > -0.0145; };
  // Sharp close-up imagery (Esri) for the closest levels: at Take flight height (~10 km up) it loads level 15 (~3 m a
  // pixel, about one map pixel per screen pixel on a phone), so houses and roads show. The engine uses the first level
  // whose threshold is at or below the altitude, so: level 13 from the Take flight pill down, 15 in the game, never 16.
  // Esri imagery for the close levels 13-14 (same tile count as EOX, ~1.5x the data, much sharper): the default since
  // 2026-11-26. Set hdOn to false to go back to EOX everywhere (the worker falls back to EOX by itself if the key lapses).
  const HD_FROM = 13, HD_MAX = 15; let hdOn = true, tileEng = null, tileSrc = null;
  function tuneHd(o) { const t = o.thresholds.slice(); while (t.length < 16) t.push(8 / Math.pow(2, t.length - 1));
    t[14] = 0.0018; t[15] = 0.0015; o.thresholds = t.slice(0, 16); }
  // Smoother map tiles (2026-11-25):
  // - the finer tiles always draw on top of the coarser ones the library keeps underneath while they load (same
  //   height, so on some phones' graphics chips the two would otherwise fight and flicker between sharp and blurry);
  // - in the game the camera moves every frame, and the library re-checks ~1,900 candidate tiles each time it moves:
  //   deciding what to load ~8 times a second is plenty. (Tiles far behind you are released by the patched library.)
  function tileHooks(o) {
    if (o._pp) return; o._pp = true;
    const lv = m => { const ph = m && m.geometry && m.geometry.parameters && m.geometry.parameters.phiLength; return ph ? Math.round(Math.log2(2 * Math.PI / ph)) : 0; };
    const add0 = o.add.bind(o); o.add = (...objs) => { for (const m of objs) if (m && m.isMesh) m.renderOrder = -100 + lv(m); return add0(...objs); };
    o.children.forEach(m => { if (m.isMesh) m.renderOrder = -100 + lv(m); });
    // In the game the library is shown a slightly bigger screen (~1.6 km more on every side), so tiles are asked for
    // a few seconds before they scroll into view instead of once they're already showing (on 5G that left a blank strip).
    const wide = cam => { try { if (!cam || !cam.isPerspectiveCamera) return cam; const c = cam.clone(), hv = Math.tan(cam.fov * Math.PI / 360),
      dist = cam.position.length() - world.getGlobeRadius(), R0 = world.getGlobeRadius(), hKm = dist / R0 * 6371 * hv, wKm = hKm * cam.aspect,
      kv = (hKm + 1.6) / hKm, kh = (wKm + 1.6) / wKm; c.fov = 360 / Math.PI * Math.atan(hv * kv); c.aspect = cam.aspect * kh / kv; c.updateProjectionMatrix(); return c; } catch (e) { return cam; } };
    const up0 = o.updatePov.bind(o); let last = 0, tmr = 0;
    o.updatePov = cam => { if (!inGame()) return up0(cam); const now = performance.now(); clearTimeout(tmr);
      if (now - last >= 120) { last = now; return up0(wide(cam)); } tmr = setTimeout(() => { last = performance.now(); up0(wide(cam)); }, 120 - (now - last)); };
  }
  // Night side: a see-through shell just above the map (so it also darkens the zoomed-in tiles) with a soft dusk band
  // and NASA Black Marble city lights (public domain). Built from the globe's own three.js classes; sun updates each minute.
  function dayNight() {
    const t = setInterval(() => {
      let g = null, atm = null;
      try { world.scene().traverse(o => { if (o.__globeObjType === 'globe' && o.children) g = g || o.children.find(m => m.isMesh); if (o.isMesh && o.material && o.material.type === 'ShaderMaterial' && !atm) atm = o; }); } catch (e) {}
      if (!g || !atm || !g.material || !g.material.map) return; clearInterval(t);
      const Mesh = g.constructor, Geo = g.geometry.constructor, Shader = atm.material.constructor, Tex = g.material.map.constructor;
      const R0 = (g.geometry.parameters && g.geometry.parameters.radius) || 100;
      const img = new Image(); img.crossOrigin = 'anonymous';
      img.onload = () => {
        const lights = new Tex(img); lights.needsUpdate = true; try { lights.colorSpace = g.material.map.colorSpace; } catch (e) {}
        // depthTest off: at a distance the shell and the globe are too close for the depth buffer to tell apart, which
        // made the night flicker in patches (z-fighting). Only the shell's near side draws (back faces are culled), so it
        // never shows through the globe.
        const mat = new Shader({ transparent: true, depthWrite: false, depthTest: false,
          uniforms: { sLat: { value: 0 }, sLng: { value: 0 }, fade: { value: 1 }, lights: { value: lights } },
          vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
          fragmentShader: 'uniform float sLat; uniform float sLng; uniform float fade; uniform sampler2D lights; varying vec2 vUv; void main(){ float lat = (vUv.y - 0.5) * 3.14159265; float lng = (vUv.x - 0.5) * 6.2831853; float d = sin(lat) * sin(sLat) + cos(lat) * cos(sLat) * cos(lng - sLng); float night = smoothstep(0.08, -0.16, d); vec3 L = texture2D(lights, vUv).rgb; float lum = dot(L, vec3(0.3,0.59,0.11)); lum = smoothstep(0.02, 0.24, lum); float a = night * max(0.7, lum) * fade; vec3 c = mix(vec3(0.01, 0.016, 0.05), vec3(1.0, 0.86, 0.58), lum); gl_FragColor = vec4(c, a); }' });
        const sh = new Mesh(new Geo(R0 * 1.0016, 128, 64), mat); sh.rotation.copy(g.rotation); sh.renderOrder = 2;
        g.parent.add(sh);
        const upd = () => { const s = subsolar(); mat.uniforms.sLat.value = s.lat * Math.PI / 180; mat.uniforms.sLng.value = s.lng * Math.PI / 180; };
        upd(); setInterval(upd, 60000);
        // zoomed in close the night fades to a faint tint (altitude 0.55 → 0.2), so the detail you zoomed in for shows
        const fd = () => { const a = world.pointOfView().altitude; mat.uniforms.fade.value = document.body.classList.contains('hunting') ? 0 : a >= 0.55 ? 1 : a <= 0.2 ? 0.22 : 0.22 + 0.78 * (a - 0.2) / 0.35; };
        world.controls().addEventListener('change', fd); fd(); setInterval(fd, 400);
      };
      img.src = '/globe/earth-night.jpg';
    }, 200);
  }
  // Header clock: UTC with a sun / moon for Greenwich. Tapping it drops down world times (east → west), each with
  // a sun / moon for whether it's day there and its offset from UTC; tapping a city spins the globe there.
  (function clocks() {
    const SUN = document.querySelector('.utc .ic-sun')?.outerHTML || '', MOON = document.querySelector('.utc .ic-moon')?.outerHTML || '';
    const CITIES = [['Auckland', -36.85, 174.76, 'Pacific/Auckland'], ['Sydney', -33.87, 151.21, 'Australia/Sydney'], ['Tokyo', 35.68, 139.69, 'Asia/Tokyo'], ['Beijing', 39.9, 116.4, 'Asia/Shanghai'], ['Singapore', 1.35, 103.82, 'Asia/Singapore'], ['Mumbai', 19.08, 72.88, 'Asia/Kolkata'], ['Dubai', 25.2, 55.27, 'Asia/Dubai'], ['Moscow', 55.76, 37.62, 'Europe/Moscow'], ['Nairobi', -1.29, 36.82, 'Africa/Nairobi'], ['Cairo', 30.04, 31.24, 'Africa/Cairo'], ['Paris', 48.86, 2.35, 'Europe/Paris'], ['Lagos', 6.52, 3.38, 'Africa/Lagos'], ['London', 51.51, -0.13, 'Europe/London'], ['São Paulo', -23.55, -46.63, 'America/Sao_Paulo'], ['New York', 40.71, -74.01, 'America/New_York'], ['Chicago', 41.88, -87.63, 'America/Chicago'], ['Mexico City', 19.43, -99.13, 'America/Mexico_City'], ['Los Angeles', 34.05, -118.24, 'America/Los_Angeles'], ['Honolulu', 21.31, -157.86, 'Pacific/Honolulu']];
    const time = tz => { try { return new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: tz }).format(new Date()); } catch (e) { return ''; } };
    const offset = tz => { try { const d = new Date(), f = new Intl.DateTimeFormat('en-US', { timeZone: tz, year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', hour12: false }).formatToParts(d), g = k => +f.find(x => x.type === k).value;
      const loc = Date.UTC(g('year'), g('month') - 1, g('day'), g('hour') % 24, g('minute')); return Math.round((loc - d.getTime()) / 6e4 / 15) * 15; } catch (e) { return 0; } };
    const offTxt = m => { if (!m) return '±0'; const s = m > 0 ? '+' : '−', a = Math.abs(m), h = Math.floor(a / 60), mm = a % 60; return s + h + (mm ? ':' + String(mm).padStart(2, '0') : ''); };
    const btn = $('utc'); const panel = document.createElement('div'); panel.className = 'wcp'; panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', 'World times'); document.body.appendChild(panel);
    const draw = () => { const s = subsolar(); const rows = CITIES.map(([n, la, lo, tz]) => ({ n, la, lo, t: time(tz), o: offset(tz), day: isDay(la, lo, s) })).sort((x, y) => y.o - x.o);
      const u = new Date(); panel.innerHTML = `<div class="wcp-h"><span>WORLD TIME</span><span><b>${String(u.getUTCHours()).padStart(2, '0')}:${String(u.getUTCMinutes()).padStart(2, '0')}</b> UTC</span></div>` + rows.map(r => `<button type="button" class="${r.day ? 'day' : 'night'}" data-la="${r.la}" data-lo="${r.lo}"><span class="ci">${r.day ? SUN : MOON}</span><span class="cn">${r.n}</span><span class="ct">${r.t}</span><span class="co">${offTxt(r.o)}</span></button>`).join(''); };
    const open = on => { panel.classList.toggle('in', on); btn.setAttribute('aria-expanded', on ? 'true' : 'false'); if (on) draw(); };
    btn.addEventListener('click', ev => { ev.stopPropagation(); open(!panel.classList.contains('in')); });
    btn.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); open(!panel.classList.contains('in')); } });
    panel.addEventListener('pointerdown', ev => ev.stopPropagation());
    panel.addEventListener('click', ev => { ev.stopPropagation(); const b = ev.target.closest('button[data-la]'); if (!b) return; open(false);
      if (world) { world.controls().autoRotate = false; world.pointOfView({ lat: +b.dataset.la, lng: +b.dataset.lo, altitude: innerWidth < 600 ? 1.6 : 1.3 }, 1400); } });
    document.addEventListener('pointerdown', ev => { if (panel.classList.contains('in') && !panel.contains(ev.target) && !btn.contains(ev.target)) open(false); }, true);
    addEventListener('keydown', ev => { if (ev.key === 'Escape') open(false); });
    // split-flap digits like the site's header clock: the old top half folds down, the new bottom half swings in
    const tEl = $('utcT'); let qs = [];
    if (tEl) { tEl.textContent = ''; qs = [...'00:00:00'].map((ch, i) => { const q = document.createElement('span'); q.className = 'q'; q.innerHTML = '<i></i>'; q._ch = ''; tEl.appendChild(q); return q; }); }
    const still = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
    // each changed digit drops in with a quick fade (a split-flap made of moving pieces made iOS skip painting the
    // pill behind them — a dark box over the globe)
    const flip = (q, ch) => { if (q._ch === ch) return; q._ch = ch; const i = q.querySelector('i'); i.textContent = ch;
      if (still()) return; q.classList.remove('tk'); void q.offsetWidth; q.classList.add('tk'); };
    // the digits (with seconds) flip every second; the sun / moon and the open panel only update on the minute
    const digits = () => { const d = new Date(), p2 = n => String(n).padStart(2, '0'), str = p2(d.getHours()) + ':' + p2(d.getMinutes()) + ':' + p2(d.getSeconds());  // the viewer's own local time
      [...str].forEach((ch, i) => { const q = qs[i]; if (!q || q._ch === ch) return; setTimeout(() => flip(q, ch), i >= 6 ? (i - 6) * 40 : i * 45); }); };
    const tick = () => { const d = new Date(), s = subsolar(d);
      { const h = d.getHours(); btn.classList.toggle('night', h < 6 || h >= 18); }
      try { const z = new Intl.DateTimeFormat('en-US', { timeZoneName: 'short' }).formatToParts(d).find(x => x.type === 'timeZoneName'); const zEl = $('utcZ'); if (zEl) zEl.textContent = z && z.value.length <= 7 ? z.value.replace(/^GMT\+0$/, 'GMT') : 'LOCAL'; } catch (e) {} if (panel.classList.contains('in')) draw(); };
    // checks every second so the minute flips on time; the panel redraws only when the minute changes
    let lastM = -1; const sec = () => { digits(); const m = new Date().getUTCMinutes(); if (m !== lastM) { lastM = m; tick(); } };
    digits(); tick(); lastM = new Date().getUTCMinutes();
    // line the updates up with the start of each second so the flip lands right on the second
    setTimeout(() => { sec(); setInterval(sec, 1000); }, 1000 - (Date.now() % 1000) + 15);
  })();
  function hiRes() {
    if (!(matchMedia('(pointer: fine)').matches && innerWidth >= 900)) return;
    const im = new Image(); im.onload = () => { try { world.globeImageUrl('/globe/earth-s2-8k.jpg'); } catch (e) {} };
    setTimeout(() => { im.src = '/globe/earth-s2-8k.jpg'; }, 1500);
  }
  // Map overlay (only when zoomed in close): Natural Earth borders on the globe + country / city names that fade in
  // as you get closer. Data (~190 KB gzipped) loads the first time you zoom in that far.
  // in the game the camera is only ~14 km up, so names and border lines go right down on the ground (from far away they
  // sit a little above it so the globe never covers them)
  const inGame = () => document.body.classList.contains('hunting');
  let mapAsk = null;   // the game calls this every frame so the names keep up with the moving view
  function mapOverlay() {
    const R = Math.PI / 180; let data = null, loading = false, band = -1, q = 0;
    const host = world.renderer().domElement.parentElement;
    const layer = document.createElement('div'); layer.className = 'map-lbl'; host.insertBefore(layer, world.renderer().domElement.nextSibling);
    const credit = document.createElement('div'); credit.className = 'map-credit'; credit.textContent = 'Imagery © EOX Sentinel-2 cloudless 2023 (Copernicus data) · Natural Earth'; document.body.appendChild(credit);
    const els = new Map(); let shown = [];
    const mk = (key, txt, cls) => { let e = els.get(key); if (!e) { e = document.createElement('div'); e.className = cls; e.textContent = txt; layer.appendChild(e); els.set(key, e); } return e; };
    // altitude bands → what shows
    const bandOf = a => a > 1.25 ? 0 : a > 0.9 ? 1 : a > 0.6 ? 2 : a > 0.38 ? 3 : a > 0.24 ? 4 : 5;
    const paths = () => {
      const b = bandOf(world.pointOfView().altitude), key = b + (inGame() ? 10 : 0); if (key === band) return; band = key;
      if (!data || b === 0) { world.pathsData([]); return; }
      const ln = data.b.map(p => ({ p, k: 'b' })).concat(b >= 3 ? data.s.map(p => ({ p, k: 's' })) : []);
      world.pathsData(ln).pathPoints('p').pathPointLat(p => p[1]).pathPointLng(p => p[0]).pathPointAlt(inGame() ? 0.00002 : 0.0012)
        .pathColor(d => d.k === 'b' ? `rgba(255,255,255,${[0, .35, .5, .55, .6, .6][b]})` : 'rgba(255,255,255,.28)')
        .pathStroke(d => d.k === 'b' ? (b >= 4 ? 1.1 : 0.7) : 0.5).pathDashLength(d => d.k === 's' ? 0.6 : 1).pathDashGap(d => d.k === 's' ? 0.4 : 0).pathTransitionDuration(0);
    };
    const draw = () => {
      q = 0; const pov = world.pointOfView(), a = pov.altitude, b = bandOf(a);
      layer.classList.toggle('on', !!data && b > 0); credit.classList.toggle('on', a < 1.25);
      { const esri = hdOn && tileEng && tileEng.level >= HD_FROM, txt = esri ? 'Imagery © Esri, Maxar, Earthstar Geographics, and the GIS User Community · Natural Earth' : 'Imagery © EOX Sentinel-2 cloudless 2023 (Copernicus data) · Natural Earth'; if (credit.textContent !== txt) credit.textContent = txt; }
      if (!data) { if (b > 0 && !loading) { loading = true; fetch('/globe/map-data.json').then(r => r.json()).then(d => { data = d; band = -1; paths(); draw(); }).catch(() => { loading = false; }); } return; }
      paths(); if (b === 0) { shown = []; return; }
      try { world.camera().updateMatrixWorld(); } catch (e) {}
      const la0 = pov.lat * R, lo0 = pov.lng * R, cap = inGame() ? Math.cos(15 / 6371) : Math.cos(Math.min(1.2, Math.acos(1 / (1 + a)) * 0.92));
      const want = [];
      const cRank = [0, 2, 4, 6, 9, 9][b], tRank = [-1, -1, 1, 3, 5, 6][b];
      for (const c of data.c) if (c[3] <= cRank) want.push({ k: 'c:' + c[0], t: c[0], lat: c[1], lng: c[2], cls: 'ml-c', pr: c[3] });
      for (const t of data.t) if (t[3] <= tRank) want.push({ k: 't:' + t[0] + t[1], t: t[0], lat: t[1], lng: t[2], cls: 'ml-t', pr: t[3] + 0.5 });
      want.sort((x, y) => x.pr - y.pr);
      const now = [], placed = [], seen = new Set(), W = innerWidth, H = innerHeight, top = (document.querySelector('.top')?.getBoundingClientRect().bottom || 0);
      // story pins and previews win: map names never sit under them
      if (!inGame()) for (const pe of document.querySelectorAll('.pin:not(.back), .ev:not(.back), .pin .pv, .ev .mini')) { const q = pe.getBoundingClientRect(); if (q.width && q.height) placed.push({ l: q.left - 2, r: q.right + 2, t: q.top - 2, b: q.bottom + 2 }); }
      const pinCount = placed.length;
      for (const w of want) {
        const la = w.lat * R, d = Math.sin(la0) * Math.sin(la) + Math.cos(la0) * Math.cos(la) * Math.cos(w.lng * R - lo0);
        if (d < cap) continue;
        const s = world.getScreenCoords(w.lat, w.lng, inGame() ? 0 : 0.001); if (!s || s.x < 4 || s.x > W - 4 || s.y < top + 6 || s.y > H - 10) continue;
        const e = mk(w.k, w.t, w.cls); const bw = e._w || (e._w = e.offsetWidth || w.t.length * 7), bh = 16;
        const r = { l: s.x - bw / 2 - 3, r: s.x + bw / 2 + 3, t: s.y - bh, b: s.y + 4 };
        if (placed.some(o => r.l < o.r && r.r > o.l && r.t < o.b && r.b > o.t)) continue;
        if (placed.length - pinCount > 70) break;
        placed.push(r); seen.add(w.k); now.push({ e, lat: w.lat, lng: w.lng }); e.style.transform = `translate(${s.x}px,${s.y}px)`; e.classList.add('on');
      }
      shown = now;
      for (const [k, e] of els) if (!seen.has(k)) e.classList.remove('on');
    };
    // keep the names glued to the map while it moves: same-frame reposition with an up-to-date camera matrix
    const glue = () => { if (!shown.length) return; try { world.camera().updateMatrixWorld(); } catch (e) {}
      for (const s of shown) { const p = world.getScreenCoords(s.lat, s.lng, inGame() ? 0 : 0.001); if (p) s.e.style.transform = `translate(${p.x}px,${p.y}px)`; } };
    let lastDraw = 0;
    const ask = fromGame => { if (inGame() && fromGame !== true) return; glue();
      if (inGame()) { if (performance.now() - lastDraw > 250) { lastDraw = performance.now(); draw(); } return; }
      if (q) return; const wait = Math.max(0, 140 - (performance.now() - lastDraw));
      q = setTimeout(() => requestAnimationFrame(() => { lastDraw = performance.now(); draw(); }), wait); };
    world.controls().addEventListener('change', ask); setInterval(ask, 600); ask(); mapAsk = ask;
  }

  // ── Take flight (worm hunt, 2026-11-25): a shared mini-game when zoomed in close. A "Take flight" pill appears; in the game your
  // bird (its face, wings in its colour, seen from above) flies at one fixed speed to wherever you tap and the view
  // follows it. Worms pop out of the ground now and then (more at night, near trending stories; gold ones are worth 5)
  // and go to the first bird to reach them. The server keeps every flight and checks every catch (worker /hunt/*).
  function hunt() {
    const SPEED = 0.35, CATCH_KM = 0.18, PILL_ALT = 0.0032, GAME_ALT = innerWidth < 600 ? 0.0016 : 0.00135, EXIT_ALT = 0.05;
    const R = Math.PI / 180, WORM_D = 'M5.3 2.4C3.9 4.5 4 7.6 6.6 7.8C9.4 8 12.6 4.3 16.3 3.9C19.3 3.6 20.6 6.7 18.3 8.7C15.9 10.6 10.6 10.9 8.1 13.2C5.9 15.4 7.4 19.3 11 19.4C14.5 19.5 18 17.6 20.7 15.8';
    const WORM_SVG = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${WORM_D}"/></svg>`;
    const km = (a, b) => { const d = Math.sin((b[0] - a[0]) * R / 2) ** 2 + Math.cos(a[0] * R) * Math.cos(b[0] * R) * Math.sin((b[1] - a[1]) * R / 2) ** 2; return 12742 * Math.asin(Math.min(1, Math.sqrt(d))); };
    // a flight: from a point, turn like a bird (at TURN rad/s) from heading b0 to b1, then fly straight on b1 at SPEED
    // (bearings clockwise from north; flat-map maths over these short distances — the same code runs on the globe page)
    const TURN = 120 * Math.PI / 180;
    const fTurn = f => { if (f._T == null) { let d = ((f.b1 - f.b0) % 6.283185307) + 6.283185307; d = (d % 6.283185307); if (d > Math.PI) d -= 6.283185307; f._s = d < 0 ? -1 : 1; f._T = Math.abs(d) / TURN; } return f; };
    const fOff = (f, u) => { fTurn(f); const T = f._T, s = f._s, ut = Math.min(u, T), bt = f.b0 + s * TURN * ut; let x = 0, y = 0;
      if (T > 0) { const k = SPEED / (s * TURN); x = k * (Math.cos(f.b0) - Math.cos(bt)); y = k * (Math.sin(bt) - Math.sin(f.b0)); }
      if (u > T) { x += SPEED * (u - T) * Math.sin(f.b1); y += SPEED * (u - T) * Math.cos(f.b1); }
      return [x, y, u < T ? bt : f.b1]; };
    const flyAt = (f, t) => { if (!f) return null; if (f.b0 == null || f.b1 == null) return f.to || f.from;
      const o = fOff(f, Math.max(0, Math.min(t, f.arrive) - f.depart) / 1000), la = Math.max(-84, Math.min(84, f.from[0] + o[1] / 111.2));
      return [la, ((f.from[1] + o[0] / (111.2 * Math.cos(f.from[0] * Math.PI / 180)) + 540) % 360) - 180]; };
    const headAt = (f, t) => f && f.b0 != null && f.b1 != null ? fOff(f, Math.max(0, Math.min(t, f.arrive) - f.depart) / 1000)[2] : null;
    const flyFor = T => (T + 14 / SPEED) * 1000;    // a flight lasts its turn plus 14 km straight on (the page carries on before then)
    const posAt = flyAt;
    // where a worm is: up for a few seconds crawling a little, then under, then up again a few km away (same code as the worker)
    const wormPlan = w => { let h = 2166136261; for (const ch of String(w.id)) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619); }
      let a = h >>> 0; const rnd = () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
      const segs = []; let t = w.born, x = 0, y = 0;
      while (t < w.gone) { const up = 4500 + rnd() * 3500, s = { a: t, b: Math.min(w.gone, t + up), x, y, hd: rnd() * 6.2832, ph: rnd() * 6.2832 }; segs.push(s);
        const e = wormOff(s, (s.b - s.a) / 1000), jd = rnd() * 6.2832, j = 0.09 + rnd() * 0.19; x = e[0] + Math.cos(jd) * j; y = e[1] + Math.sin(jd) * j; t += up + 2500 + rnd() * 3000; }
      return segs; };
    const wormOff = (s, u) => { const wob = 0.057 * Math.sin(u * 1.3 + s.ph); return [s.x + 0.04 * u * Math.cos(s.hd) - wob * Math.sin(s.hd), s.y + 0.04 * u * Math.sin(s.hd) + wob * Math.cos(s.hd)]; };
    const wormAt = (w, t) => { const segs = w._p || (w._p = wormPlan(w)), toLL = o => [w.lat + o[1] / 111.2, w.lng + o[0] / (111.2 * Math.cos(w.lat * Math.PI / 180))];
      for (const s of segs) { if (t >= s.a && t < s.b) { const ll = toLL(wormOff(s, (t - s.a) / 1000)); return { up: true, lat: ll[0], lng: ll[1], fromUp: t - s.a, toDown: s.b - t }; }
        if (t < s.a) { const ll = toLL([s.x, s.y]); return { up: false, lat: ll[0], lng: ll[1], toUp: s.a - t }; } }
      const l = segs[segs.length - 1], ll = l ? toLL(wormOff(l, (l.b - l.a) / 1000)) : [w.lat, w.lng]; return { up: false, lat: ll[0], lng: ll[1], toUp: Infinity }; };
    // the bird always flies: a tap sets a new heading; it glides round to it like a bird, then flies straight on
    const bearing = (a, b) => { const y = Math.sin((b[1] - a[1]) * R) * Math.cos(b[0] * R), x = Math.cos(a[0] * R) * Math.sin(b[0] * R) - Math.sin(a[0] * R) * Math.cos(b[0] * R) * Math.cos((b[1] - a[1]) * R); return Math.atan2(y, x); };
    function flyDir(brg) {
      const t = srv(), p = posAt(me, t), h = me && t < me.arrive ? headAt(me, t) : null;
      const f = fTurn({ from: p, to: p, b0: h == null ? brg : h, b1: brg, depart: t }); f.arrive = t + flyFor(f._T); me = f; flySent = Date.now(); flyWait++;
      try { localStorage.setItem('pp_hunt_brg', String(brg)); } catch (e) {}
      api('/hunt/fly', { brg, t }).then(x => { flyWait = Math.max(0, flyWait - 1); if (x.s === 200 && x.j.me && on && flyWait === 0) setMe(x.j.me); });
    }
    // the server's copy of a flight starts a moment later than the one the page drew, so swapping to it would make the
    // bird hop a few pixels: the difference is blended away over a third of a second instead
    function setMe(f) {
      if (f && f.depart) myDeps.add(f.depart);
      const t = srv(), a = me && posAt(me, t), b = posAt(f, t);
      if (a && b && km(a, b) < 1) { const c0 = corrNow(); corr = { la: a[0] - b[0] + c0[0], lo: a[1] - b[1] + c0[1], t0: performance.now() }; }
      me = f;
    }
    const corrNow = () => { if (!corr) return [0, 0]; const k = 1 - (performance.now() - corr.t0) / 350; if (k <= 0) { corr = null; return [0, 0]; } const e = k * k * (3 - 2 * k); return [corr.la * e, corr.lo * e]; };
    // how far the bird is leaning into a turn (−1 left … 1 right): it tips in as the turn starts and levels out after
    const bankAt = (f, t) => { if (!f || f.b0 == null || f.b1 == null) return 0; fTurn(f); const u = (t - f.depart) / 1000, T = f._T;
      return T < 0.05 || u < 0 || u > T ? 0 : f._s * Math.min(1, T * TURN / (Math.PI / 2)); };   // 1 = a turn of 90° or more
    // each bird's wings, made to look like a real bird: nothing switches on or off. The flapping has a strength (1 = full
    // beats, 0 = gliding) that eases up and down, so on a turn the beats fade out and slow while the wings float out
    // to a glide, and the lean grows as the flapping fades (a spring, so it tips in and levels out softly). Flying
    // straight it flap-glides like small birds do: a few beats, then a short glide.
    const poses = new Map();
    function pose(id, moving, want, dt) {
      let P = poses.get(id); if (!P) { P = { ph: Math.random() * 6.283, A: 1, bk: 0, bv: 0, beats: 0, nb: 4 + Math.random() * 4, glide: 0 }; poses.set(id, P); }
      // how big the turn is decides how much it glides: small corrections (under ~25°) keep flapping, just a touch
      // softer, with a slight tilt; from there the glide blends in, and turns of 90° or more glide all the way round
      const turning = Math.abs(want) > 0.02, size = Math.abs(want), u0 = Math.max(0, Math.min(1, (size - 0.28) / 0.72)), g = turning ? u0 * u0 * (3 - 2 * u0) : 0;
      if (P.glide > 0) P.glide -= dt;
      const tA = P.glide > 0 ? 0 : turning ? Math.min(1 - 0.07 * Math.min(1, size / 0.28), 1 - g) : 1;
      P.A += (tA - P.A) * (1 - Math.exp(-dt / (tA < P.A ? 0.11 : 0.2)));
      const before = P.ph; P.ph += dt * (moving ? 13 : 4) * (0.45 + 0.55 * P.A);
      if (Math.floor(before / 6.2832) !== Math.floor(P.ph / 6.2832)) { P.beats++;
        if (moving && !turning && P.beats >= P.nb) { P.beats = 0; P.nb = 4 + Math.random() * 4; P.glide = 0.45 + Math.random() * 0.5; } }
      if (turning) P.beats = 0;
      // the lean follows a soft spring: a slight tilt straight away for any turn, and for gliding turns more lean
      // as the flapping fades
      const tb = turning ? Math.sign(want) * (0.3 * Math.min(1, size / 0.28) + 0.7 * g * Math.max(0, Math.min(1, (1 - P.A) / Math.max(g, 0.01)))) : 0, w = P.bw = (P.bw || 10) + ((turning ? 4.5 + 5.5 * g : P.bw || 10) - (P.bw || 10)) * Math.min(1, dt * 8);
      for (let left = dt; left > 1e-4; left -= 0.01) { const h = Math.min(0.01, left); P.bv += ((tb - P.bk) * w * w - 2 * w * P.bv) * h; P.bk += P.bv * h; }
      const f = 0.5 + 0.5 * Math.sin(P.ph), flapSpan = moving ? 0.55 + 0.45 * f : 0.9 + 0.1 * f;
      return { span: 0.97 + (flapSpan - 0.97) * P.A, bk: Math.max(-1, Math.min(1, P.bk)), lift: P.A * (f - 0.5) };
    }
    // Load ahead: map tiles a few km in front of the bird (and either side) are fetched and decoded in the background
    // before they scroll on screen, so the map doesn't hitch decoding them mid-frame. Kept to the last 300.
    const pre = new Map(); let preAt = 0;
    function preload(now) {
      if (!tileEng || !tileSrc || !me || zoomIn) return; const L = tileEng.level, h = headAt(me, now), p = posAt(me, now); if (!L || h == null || !p) return;
      const Z = 2 ** L, kx = 111.2 * Math.cos(p[0] * R);
      for (const d of [4, 5.5]) for (const s0 of [-2, -0.7, 0.7, 2]) {
        const la = p[0] + (d * Math.cos(h) - s0 * Math.sin(h)) / 111.2, lo = p[1] + (d * Math.sin(h) + s0 * Math.cos(h)) / kx;
        const x = Math.floor((lo + 180) / 360 * Z), y = Math.floor((1 - Math.log(Math.tan(la * R) + 1 / Math.cos(la * R)) / Math.PI) / 2 * Z), url = tileSrc(x, y, L);
        if (pre.has(url)) continue;
        const im = new Image(); im.crossOrigin = 'anonymous'; im.src = url; if (im.decode) im.decode().catch(() => {}); pre.set(url, im);
        if (pre.size > 300) pre.delete(pre.keys().next().value);
      } }
    // headings on screen ease toward where the bird is going, so nothing snaps
    // (a spring, not a plain ease: the beak starts swinging gently and settles gently, so even small turns are smooth;
    // the 250 ms look-ahead it aims at makes up for the spring's lag)
    const angV = new Map();
    // every turn lines up gently over about a second (the user's choice); it aims ~0.6 s ahead along the path, which
    // makes up for the spring's lag, so on big turns the beak still points round the curve rather than trailing it
    const ease = (cur, want, dt, key) => { if (cur == null) return want; const w = 6;
      let v = angV.get(key) || 0, a = cur;
      for (let left = dt; left > 1e-4; left -= 0.01) { const h = Math.min(0.01, left); let e = want - a; e = Math.atan2(Math.sin(e), Math.cos(e)); v += (e * w * w - 2 * w * v) * h; a += v * h; }
      angV.set(key, v); return a; };
    // who you are: read from your sign-in itself (the remembered '_myUsername' can be left over from another account you
    // used in the same browser, which drew someone else's bird and colours for you)
    let myTok = null, myNm = '';
    const myName = () => { const tk = tok(); if (tk !== myTok) { myTok = tk; myNm = '';
        try { const b = tk && tk.split('.')[1]; if (b) { const pl = JSON.parse(decodeURIComponent(escape(atob(b.replace(/-/g, '+').replace(/_/g, '/'))))); myNm = pl.username || ''; } } catch (e) {}
        if (!myNm) try { myNm = localStorage.getItem('_myUsername') || ''; } catch (e) {} }
      return myNm; };
    let landed = false, birdsIn = false, on = false, me = null, birds = [], worms = new Map(), off = 0, balance = null, fx = [], target = null, raf = 0, pollT = 0, flySent = 0, flyWait = 0, corr = null, lastF = 0, frameMs = 16.7, zoomIn = null, extAt = 0, ang = -Math.PI / 2, angs = new Map(), asking = new Set(), seenTaken = new Set(), hintUntil = 0;
    const srv = () => Date.now() + off;
    // Server clock: on mobile data the round trip jitters, and taking each 2-second answer as-is nudged the bird (and so
    // the whole map) a few metres back or forward every time: the 'bounce'. Now the most trustworthy recent answer (the
    // fastest round trip of the last 8) is the target, and the clock drifts toward it at most 3% faster or slower.
    let offT = null, clk = [];
    const clockSample = (o, rtt) => { clk.push({ o, rtt }); if (clk.length > 8) clk.shift();
      const best = clk.reduce((a, b) => b.rtt < a.rtt ? b : a); offT = best.o;
      if (clk.length === 1 || Math.abs(offT - off) > 1500) off = offT; };
    const clockStep = dt => { if (offT == null) return; const d = offT - off, m = dt * 0.03; off += d > m ? m : d < -m ? -m : d; };
    const api = (path, body) => fetch(API + path, { method: 'POST', headers: { 'Content-Type': 'application/json', ...hdr() }, body: JSON.stringify(body || {}) }).then(async r => ({ s: r.status, j: await r.json().catch(() => ({})) })).catch(() => ({ s: 0, j: {} }));

    // pieces on the page: the pill, the game bar, and a see-through canvas over the globe the game draws on
    const host = world.renderer().domElement.parentElement;
    const cv = document.createElement('canvas'); cv.className = 'hunt-cv'; host.appendChild(cv);
    let cx = cv.getContext('2d'); let W = 0, H = 0, DPR = 1;
    const size = () => { DPR = Math.min(2, devicePixelRatio || 1); W = innerWidth; H = innerHeight; cv.width = W * DPR; cv.height = H * DPR; cv.style.width = W + 'px'; cv.style.height = H + 'px'; };
    size(); addEventListener('resize', size);
    const bar = document.createElement('div'); bar.className = 'hunt-bar';
    bar.innerHTML = `<span class="hb-n"><span class="hw">${WORM_SVG}</span><b id="huntN">–</b></span><span class="hb-t" id="huntT">Tap to fly</span><button type="button" class="hb-x" aria-label="Land (leave Take flight)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button>`;
    document.body.appendChild(bar);
    bar.addEventListener('pointerdown', ev => ev.stopPropagation());
    // ── the game's two bars (the user's layout "D", 2026-11-26) ──
    // Top: land ×, level + XP (placeholders until the XP rules are set), your bird's local time, worms. Bottom: the
    // nearest town and the country under your bird, how far you've flown, how far home is (with an arrow), and the map
    // and passport buttons (their panels open from the bottom-right; both are still to come). A short log rises above it.
    const ghTop = document.createElement('div'), ghBot = document.createElement('div'), ghLog = document.createElement('div'), ghPanel = document.createElement('div');
    ghTop.className = 'gh gh-top'; ghBot.className = 'gh gh-bot'; ghLog.className = 'gh-log'; ghPanel.className = 'gh-panel';
    const RING = 2 * Math.PI * 19;
    ghTop.innerHTML = `<button type="button" class="gh-x" aria-label="Land (leave Take flight)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
      <div class="gh-lvw"><div class="gh-lv"><svg viewBox="0 0 44 44"><circle cx="22" cy="22" r="19" fill="rgba(11,12,16,.35)" stroke="rgba(255,255,255,.14)" stroke-width="4"/><circle id="ghRing" cx="22" cy="22" r="19" fill="none" stroke="#c084fc" stroke-width="4" stroke-linecap="round" stroke-dasharray="0 ${RING}" transform="rotate(-90 22 22)"/></svg><small>LV</small><b id="ghLv">1</b></div><span class="gh-xpn" id="ghXpT"><em>0</em>/100 XP</span></div>
      <div class="gh-mid"><div class="gh-r1"><span class="gh-time" id="ghTime">–</span><span class="gh-worm" id="ghWormBox">${WORM_SVG}<b id="ghWorms">–</b></span></div>
        <div class="gh-en"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 2 4.5 13.5H11L10 22l8.5-11.5H12z" fill="currentColor"/></svg><div class="gh-enb"><i id="ghEn"></i></div><b id="ghEnT">100%</b></div></div>`;
    ghBot.innerHTML = `<div class="gh-place"><b id="ghPlace">–</b><small id="ghCountry">&nbsp;</small></div>
      <div class="gh-stat"><b id="ghFlown">0 km</b><small>FLOWN</small></div>
      <div class="gh-stat"><b><span id="ghHome">–</span> <i id="ghArrow">↑</i></b><small>HOME</small></div>
      <button type="button" class="gh-btn" id="ghMap" aria-label="Map"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M3 6.5l6-2.5 6 2.5 6-2.5v13.5l-6 2.5-6-2.5-6 2.5z"/><path d="M9 4v13.5M15 6.5V20"/></svg></button>
      <button type="button" class="gh-btn pass" id="ghPass" aria-label="Passport"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><rect x="5" y="3" width="14" height="18" rx="2.5"/><circle cx="12" cy="10.5" r="3.2"/><path d="M8.5 16.5h7"/></svg></button>`;
    for (const el of [ghTop, ghBot, ghLog, ghPanel]) { document.body.appendChild(el); el.addEventListener('pointerdown', ev => ev.stopPropagation()); }
    ghTop.querySelector('.gh-x').addEventListener('click', () => leave());
    let ghOpen = null;
    const PANELS = { map: ['Your travels', 'The map of everywhere your bird has seen, region by region, is coming next.'],
                     pass: ['Your passport', 'Your Bird ID and the stamps from your travels are coming soon.'] };
    const openPanel = k => { ghOpen = ghOpen === k ? null : k; $('ghMap').classList.toggle('on', ghOpen === 'map'); $('ghPass').classList.toggle('on', ghOpen === 'pass');
      ghPanel.classList.toggle('in', !!ghOpen); if (ghOpen) ghPanel.innerHTML = `<div style="opacity:.55;color:#c084fc">${ghOpen === 'map' ? $('ghMap').innerHTML : $('ghPass').innerHTML}</div><h3>${PANELS[ghOpen][0]}</h3><p>${PANELS[ghOpen][1]}</p>`; };
    $('ghMap').addEventListener('click', () => openPanel('map')); $('ghPass').addEventListener('click', () => openPanel('pass'));
    // the log: short lines that rise above the bottom bar and fade (the newest at the bottom, three at most)
    function ghEvent(tag, text, colour) { const d = document.createElement('div'); d.innerHTML = `<span style="background:${colour}">${tag}</span>`; d.appendChild(document.createTextNode(text));
      ghLog.appendChild(d); while (ghLog.children.length > 3) ghLog.firstChild.remove();
      setTimeout(() => { d.style.opacity = '0'; setTimeout(() => d.remove(), 650); }, 6500); }
    // towns for "where you are" (the same list the map's names come from)
    let towns = null; const loadTowns = () => { if (towns) return; towns = []; fetch('/globe/map-data.json').then(r => r.json()).then(d => { towns = [...(d.c || []), ...(d.t || [])].map(t => [t[0], +t[1], +t[2]]); }).catch(() => { towns = null; }); };
    // ── stamina (a TEST, 2026-11-26): flying uses it and rest refills it slowly (a quarter of the bar per 24 hours).
    // Once a day the bird has dinner: the server takes one worm from your balance and the bar is filled (mealIn). When it runs out mid-flight the bird
    // eats a worm from your real worm balance (the site's currency, the user's decision) and it's full again; with no
    // worms left it lands and can't take off until it has a worm (or has rested). The bar itself is kept on this
    // device for now; the worm it eats is spent on the server (/hunt/eat). Starving comes later. ──
    const EN_MAX = 150, EN_REST = EN_MAX / 4 / 864e5;   // km of flying when full; km per ms of rest (a quarter of the bar a day)
    // ── water (2026-11-26): landing on water means treading water: the bird can't move and it uses stamina at 3/4 of
    // the flying rate, even while you're away. Run out in the water (or over it) and the bird drowns and comes back
    // at its home spot. Land vs water comes from /globe/water/: the world in 5° squares at 0.01° (~1 km), made from
    // Natural Earth's land, minor islands and lakes; index.json says which squares are all land (L), all water (W)
    // or mixed (M, a 1-bit picture: white = land). Only the squares around your bird are fetched. ──
    const SWIM = 0.75 * SPEED / 1000;   // km of stamina per ms while treading water
    const WATER = { idx: null, busy: false, tiles: new Map() };
    function isWater(lat, lng) {   // true / false, or null while that bit of the map is still loading
      if (!WATER.idx) { if (!WATER.busy) { WATER.busy = true; fetch('/globe/water/index.json').then(r => r.json()).then(j => { WATER.idx = j; }).catch(() => {}).finally(() => { WATER.busy = false; }); } return null; }
      const x0 = (((lng + 180) % 360) + 360) % 360, y0 = Math.min(179.999, Math.max(0, 90 - lat)), ty = Math.floor(y0 / 5), tx = Math.min(71, Math.floor(x0 / 5)), kind = WATER.idx.m[ty * 72 + tx];
      if (kind === 'W') return true; if (kind === 'L') return false;
      const key = ty + '_' + tx; let t = WATER.tiles.get(key);
      if (!t) { WATER.tiles.set(key, 'wait'); const im = new Image(); im.onload = () => { const c = document.createElement('canvas'); c.width = c.height = 500; const x = c.getContext('2d'); x.drawImage(im, 0, 0);
          const d = x.getImageData(0, 0, 500, 500).data, a = new Uint8Array(250000); for (let i = 0; i < 250000; i++) a[i] = d[i * 4] > 127 ? 1 : 0; WATER.tiles.set(key, a); };
        im.onerror = () => WATER.tiles.delete(key); im.src = '/globe/water/' + key + '.png'; return null; }
      if (t === 'wait') return null;
      const cx2 = Math.min(499, Math.floor((x0 - tx * 5) * 100)), cy2 = Math.min(499, Math.floor((y0 - ty * 5) * 100));
      return !t[cy2 * 500 + cx2];
    }
    let wet = false, drowning = null, noWater = 0, overW = false, overWAt = 0;
    let enKm = EN_MAX, enAt = Date.now(), enTired = false, eating = false;
    try { const o = JSON.parse(localStorage.getItem('pp_energy') || 'null'); if (o && isFinite(o.km)) { wet = !!o.wet; const away = Math.max(0, Date.now() - o.at); enKm = Math.max(0, Math.min(EN_MAX, o.km + (wet ? -away * SWIM : away * EN_REST))); } } catch (e) {}
    const enSave = () => { try { localStorage.setItem('pp_energy', JSON.stringify({ km: enKm, at: Date.now(), wet })); } catch (e) {} };
    // the bird drowns: it sinks (ripples, fading), then the server puts it back at its home spot
    function drown() {
      if (drowning) return; drowning = { t0: performance.now() }; peck = null;
      ghEvent('Drowned', 'out of stamina in the water · back home', '#60a5fa');
      setTimeout(() => { api('/hunt/drown').then(r => { const ok = r.s === 200 && r.j.me;
        if (ok) { setMe(r.j.me); if (r.j.st) { gSt = r.j.st; gStAt = r.j.now; } if (r.j.balance != null) setBal(r.j.balance); wet = false; landed = true; enKm = EN_MAX; enTired = false; enSave(); ghEvent('Home', 'washed up at home · stamina full, no worms', '#fcd34d'); }
        else { wet = false; noWater = Date.now() + 120000; }   // the server's coarser map says land here (a small lake): count it as land
        drowning = null; }); }, 1700);
    }
    const enAdd = km => { enKm = Math.max(0, Math.min(EN_MAX, enKm + km)); };
    // dinner from the server (/hunt/me or /hunt/state): a full bar, told in the log (now, or as soon as you're playing)
    let mealNote = null;
    const mealIn = j => { const m = j && j.meal; if (!m) return; if (j.balance != null) setBal(j.balance);
      if (m.ate > 0) { enKm = EN_MAX; enAt = Date.now(); enTired = false; enSave(); mealNote = ['Dinner', 'ate a worm · stamina full', '#e8555c']; }
      else mealNote = ['Hungry', 'no worm for dinner · resting only', '#f87171'];
      if (on) { ghEvent(...mealNote); mealNote = null; } };
    // drowned while you were away (the server sank it when its stamina ran out): full bar, no worms, told in the log
    const drownedIn = j => { if (!j || !j.drowned) return; if (j.balance != null) setBal(j.balance); enKm = EN_MAX; enAt = Date.now(); wet = false; enTired = false; enSave();
      const n = j.drowned.lost; mealNote = ['Drowned', `while you were away · washed up at home${n ? ` · lost all ${n} worm${n === 1 ? '' : 's'}` : ''}`, '#60a5fa']; if (on) { ghEvent(...mealNote); mealNote = null; } };
    const outOfWorms = () => { if (!landed) landNow(); ghEvent('Out of worms', 'catch or earn a worm to fly again', '#f87171'); };
    // eat one worm: stamina back to full, then carry on (then() takes off again if you were standing)
    function eatWorm(then, fail, quiet) {
      if (eating) return; if (balance != null && balance < 1) { enTired = true; if (!quiet) outOfWorms(); if (fail) fail(); return; }
      eating = true;
      api('/hunt/eat').then(r => { eating = false;
        if (r.s === 200 && r.j.ok) { enKm = EN_MAX; enTired = false; enSave(); if (r.j.balance != null) setBal(r.j.balance); ghEvent('−1', 'Ate a worm · stamina full', '#e8555c'); if (then) then(); return; }
        if (r.j.balance != null) setBal(r.j.balance); enTired = true; if (fail) fail(); if (!quiet) outOfWorms(); });
    }
    // out of stamina mid-flight: the bird lands, ducks its head to gobble a worm (a big peck, then a little one), and
    // takes off again the way it was going once the worm is eaten and the animation has played
    let peck = null; const PECK_MS = 1500;
    function eatStop() {
      if (eating || peck) return;
      if (balance != null && balance < 1) { enTired = true; outOfWorms(); return; }
      const h = headAt(me, srv()) ?? me.b1 ?? 0; landNow(true);
      const pk = peck = { t0: performance.now(), res: null };
      const go = () => { if (peck !== pk || pk.res == null || performance.now() - pk.t0 < PECK_MS) return; peck = null; if (pk.res && on && landed) { landed = false; flyDir(h); } };
      eatWorm(() => { pk.res = true; go(); }, () => { if (peck === pk) peck = null; });
      setTimeout(go, PECK_MS + 30);
    }
    let gSt = null, gStAt = 0, ghNext = 0, ghTown = '', ghTownAt = 0, ghTopB = 70, ghBotT = 0, met = new Set();
    const regionName = (() => { try { return new Intl.DisplayNames(['en'], { type: 'region' }); } catch (e) { return null; } })();
    const flag = cc => cc && cc.length === 2 ? String.fromCodePoint(...[...cc.toUpperCase()].map(ch => 127397 + ch.charCodeAt(0))) : '';
    function ghUpdate(now, p) {
      const pf = performance.now(); if (pf < ghNext) return; ghNext = pf + 250;
      const rt = ghTop.getBoundingClientRect(), rb = ghBot.getBoundingClientRect(); ghTopB = rt.bottom; ghBotT = rb.top || H;
      ghLog.style.bottom = (H - ghBotT + 10) + 'px'; ghPanel.style.bottom = (H - ghBotT + 10) + 'px';
      // your bird's local time
      if (gSt && gSt.tz) { try { const d = new Date(now), parts = new Intl.DateTimeFormat('en-GB', { timeZone: gSt.tz, hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZoneName: 'short' }).formatToParts(d);
        const g = t => (parts.find(x => x.type === t) || {}).value || '', hr = +g('hour'), sun = hr >= 6 && hr < 18;
        $('ghTime').innerHTML = `${sun ? '☀︎' : '☾'} ${g('hour')}:${g('minute')}<s>:${g('second')}</s><em>${g('timeZoneName').replace(/^GMT\+0$/, 'GMT')}</em>`; } catch (e) {} }
      // where you are
      if (p) { loadTowns(); let best = null, bd = 25; if (towns && towns.length) for (const t of towns) { if (Math.abs(t[1] - p[0]) > 0.3) continue; const d = km(p, [t[1], t[2]]); if (d < bd) { bd = d; best = t[0]; } }
        const name = best || 'Open country'; if ($('ghPlace').textContent !== name) $('ghPlace').textContent = name;
        if (best && best !== ghTown) { if (ghTown && pf > ghTownAt) ghEvent('Over', best, '#93c5fd'); ghTown = best; ghTownAt = pf + 4000; }
        const cc = gSt && gSt.cc, cn = cc ? `${flag(cc)} ${(regionName && regionName.of(cc) || cc).toUpperCase()}` : ' '; if ($('ghCountry').textContent !== cn) $('ghCountry').textContent = cn; }
      // how far you've flown: the server's total, carried on while you fly
      if (gSt) { const fl = gSt.flown + (me && now < me.arrive && me.b1 != null ? SPEED * Math.max(0, Math.min(now, me.arrive) - Math.max(gStAt, me.depart)) / 1000 : 0);
        $('ghFlown').textContent = fl < 10 ? fl.toFixed(1) + ' km' : Math.round(fl) + ' km'; }
      // how far home is, and which way (the map is always north-up)
      if (gSt && gSt.home && p) { const d = km(p, gSt.home); $('ghHome').textContent = d < 0.1 ? 'Home' : d < 10 ? d.toFixed(1) + ' km' : Math.round(d) + ' km';
        $('ghArrow').style.transform = `rotate(${bearing(p, gSt.home) * 180 / Math.PI}deg)`; $('ghArrow').style.visibility = d < 0.1 ? 'hidden' : ''; }
      // energy: flying drains it, standing still refills it slowly
      { const t = Date.now(), dms = Math.max(0, t - enAt); enAt = t;
        const flying = me && now < me.arrive && me.b1 != null && !landed, w = p ? isWater(p[0], p[1]) : null;   // (also fetches the map around you)
        if (!flying && w != null && w !== wet && !(w && Date.now() < noWater)) { wet = w; if (wet && enKm > 0 && !drowning) ghEvent('Treading water', 'uses stamina', '#60a5fa'); enSave(); }
        if (flying && w != null) { if (w && !overW && Date.now() > overWAt) { overWAt = Date.now() + 60000; ghEvent('Over water', 'run out of worms here, you will drown', '#60a5fa'); } overW = w; }   // flying out over water: a short warning (at most once a minute, so coastlines don't spam it)
        if (flying) { if (wet) { wet = false; } enAdd(-SPEED * Math.min(5000, dms) / 1000); }
        else if (wet) enAdd(-SWIM * Math.min(5000, dms)); else enAdd(dms * EN_REST);   // (rest counts all the time you were away)
        if (flying && enKm <= 0 && !enTired) { if (w === true) { landNow(true); wet = true; ghEvent('Splash', 'out of stamina over water', '#60a5fa'); } else eatStop(); }   // over water: falls in (then eats, below); over land: lands, eats, flies on
        else if (!flying && wet && enKm <= 0 && !eating && !drowning) eatWorm(null, drown, true);   // treading water: eats a worm and keeps going; no worms left: drowns
        if (enKm > 3) enTired = false;
        const pc = enKm / EN_MAX, el = $('ghEn'); el.style.width = (pc * 100).toFixed(1) + '%';
        el.style.background = pc > .5 ? '#4ade80' : pc > .2 ? '#facc15' : '#f87171'; $('ghEnT').textContent = Math.ceil(pc * 100) + '%';
        if (Math.random() < .1) enSave(); }
      // level / XP: placeholders until the XP rules are decided
      $('ghWorms').textContent = balance == null ? '–' : balance;
    }
    // your own bird on the globe is the way in (no button): an invisible tap target sits on it when it shows as a bird
    const myBtn = document.createElement('button'); myBtn.type = 'button'; myBtn.className = 'hunt-me'; myBtn.setAttribute('aria-label', 'Take flight'); document.body.appendChild(myBtn);
    // your dot, zoomed out: drawn inside the globe area (moved like the map's place names, so it stays fixed to the map on
    // phones) on a layer above the story pins; the button above is only the invisible place to tap
    const meDot = document.createElement('div'); meDot.className = 'me-dot'; host.appendChild(meDot);
    myBtn.addEventListener('pointerdown', ev => ev.stopPropagation());
    // tapping your dot (zoomed out) flies the view down to your bird; tapping your bird (zoomed in) takes off
    let myBtnMode = 'bird', myBtnAt = null, dotFly = null;
    // the flight down to your bird is driven here, a frame at a time (on iPhones the globe's own animated move could stop
    // partway or twitch back and forth)
    function dotFlyStep() {
      if (!dotFly) return; const k = Math.min(1, (performance.now() - dotFly.t0) / 2000), e = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
      const dl = ((dotFly.lo - dotFly.lo0 + 540) % 360) - 180, la = dotFly.la0 + (dotFly.la - dotFly.la0) * e, lo = dotFly.lo0 + dl * e;
      const al = Math.exp(Math.log(dotFly.a0) + (Math.log(GAME_ALT) - Math.log(dotFly.a0)) * e);   // zoom evenly (in steps that feel the same at every height)
      world.pointOfView({ lat: la, lng: lo, altitude: al }, 0); if (k >= 1) dotFly = null;
    }
    world.renderer().domElement.addEventListener('pointerdown', () => { dotFly = null; });   // touching the map stops the flight
    myBtn.addEventListener('click', () => { if (!tok() || tko || on) return;
      if (myBtnMode === 'dot' && myBtnAt) { const c = world.controls(); c.autoRotate = false; const v = world.pointOfView(); dotFly = { la0: v.lat, lo0: v.lng, a0: v.altitude, la: myBtnAt[0], lo: myBtnAt[1], t0: performance.now() }; return; }   // all the way down to playing height
      tko = { t0: performance.now(), wet: !!(mine && mine.wet && mine.wet > Date.now() + dotsOff) }; });
    bar.querySelector('.hb-x').addEventListener('click', () => leave());


    // a bird's colour: its own body colour, the same as its logo bird (everyone, admins and mods too — the user's
    // choice 2026-11-26). The beak is a darker shade of it.
    const roles = new Map(), cols = new Map();
    const ADMIN_COL = [155, 184, 185];   // the admin bird's blue-grey (admins' logo is that picture, not a generated bird)
    const col = name => { if (roles.get(name) === 'admin') return ADMIN_COL; let v = cols.get(name); if (v) return v;
      try { if (window._ppKit && window._ppKit.bodyCol) { v = window._ppKit.bodyCol(name); cols.set(name, v); return v; } } catch (e) {}
      return [94, 234, 212]; };
    const css = c => `rgb(${c[0]},${c[1]},${c[2]})`, shade = c => c[0] + c[1] + c[2] > 600 ? [150, 150, 158] : c.map(x => Math.round(x * 0.55));

    function enter() {
      if (on) return; on = true; birdsIn = false; landed = false; loadKit(() => {});
      document.body.classList.add('hunting'); myBtn.classList.remove('in'); bar.classList.add('in');
      try { closeSheet(); focusPin(null); world.arcsData([]); world.ringsData([]); } catch (e) {}
      // the screen stays on your bird, so the map can't be dragged or pinch-zoomed during the hunt (leave with the ×)
      const c = world.controls(); c.autoRotate = false; c.enableRotate = false; c.enableZoom = false; c.enableDamping = false;   // no leftover drift from a swipe or pinch
      const v = world.pointOfView();
      $('huntN').textContent = balance == null ? '–' : balance; hintUntil = Date.now() + 4000;
      ghLog.innerHTML = ''; ghTown = ''; met = new Set(); ghNext = 0; { const away = Math.max(0, Date.now() - enAt); enAdd(wet ? -away * SWIM : away * EN_REST); } enAt = Date.now(); if (mealNote) { const n = mealNote; mealNote = null; setTimeout(() => ghEvent(...n), 600); }   // rested while you were away
      // (your bird's spot is already known from the globe, so the dive down to it starts at once, not after the server answers)
      if (mine && mine.me) { me = { ...mine.me }; zoomIn = { la: v.lat, lo: v.lng, a: v.altitude, t0: performance.now() }; }
      poll(true, [v.lat, v.lng]); loop();
    }
    const TZ = (() => { try { return Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) { return ''; } })();
    // pausing: the server stops the bird where it is (also when the page is hidden or closed mid-flight)
    // stopping over water (leaving mid-flight too) means the bird is in the water: it falls in and treads water
    const wetHere = () => { const q = me && posAt(me, srv()); if (q && !drowning && isWater(q[0], q[1]) === true && !(Date.now() < noWater)) wet = true; };
    const pauseNow = keep => (wetHere(), fetch(API + '/hunt/pause', { method: 'POST', keepalive: !!keep, headers: { 'Content-Type': 'application/json', ...hdr() }, body: JSON.stringify({ col: kitCol(), leaving: 1, wet: wet && !drowning, en: enKm / EN_MAX, t: srv() }) })
      .then(r => r.json()).then(j => { if (j && j.me) { myDeps.add(j.me.depart); mine = { me: j.me, home: null, wet: j.wet || 0 }; if (on && document.hidden) me = j.me; } }).catch(() => {}));
    function leave() {
      if (!on) return; on = false; if (ghOpen) openPanel(ghOpen); document.body.classList.remove('hunting'); bar.classList.remove('in'); world.controls().enableRotate = true; world.controls().enableZoom = true; world.controls().enableDamping = true; try { paint(); } catch (e) {}
      cancelAnimationFrame(raf); clearTimeout(pollT); cx.clearRect(0, 0, cv.width, cv.height); target = null; fx = [];
      wetHere(); if (me) mine = { me: { ...me, from: posAt(me, srv()), to: posAt(me, srv()), b0: headAt(me, srv()) ?? me.b1, b1: headAt(me, srv()) ?? me.b1, depart: srv(), arrive: srv() }, home: null,
        wet: wet && !drowning ? Date.now() + dotsOff + enKm / SWIM : 0 };   // in the water: drowning on the globe straight away (the server's answer confirms it a moment later)
      pauseNow(); enSave(); idleRaf = requestAnimationFrame(idle);
    }
    function landNow(quiet) {
      const t = srv(), p = posAt(me, t), h = headAt(me, t) ?? me.b1 ?? 0; landed = true;
      setMe({ from: p, to: p, b0: h, b1: h, depart: t, arrive: t }); flySent = Date.now(); flyWait++;
      fetch(API + '/hunt/pause', { method: 'POST', headers: { 'Content-Type': 'application/json', ...hdr() }, body: JSON.stringify({ col: kitCol(), t }) }).then(r => r.json())
        .then(j => { flyWait = Math.max(0, flyWait - 1); if (j && j.me && on && landed) { setMe(j.me); if (j.st) { gSt = j.st; gStAt = j.now; } } }).catch(() => { flyWait = Math.max(0, flyWait - 1); });
      if (!quiet) ghEvent('Landed', ghTown || 'here', '#fcd34d');
    }
    addEventListener('pagehide', () => { try { if (on) pauseNow(true); } catch (e) {} });
    document.addEventListener('visibilitychange', () => {
      if (!on) { if (!document.hidden) { loadMine(); loadDots(); } return; }
      if (document.hidden) pauseNow(true);
      else if (me && !landed) { const h = headAt(me, srv()); flyDir(h != null ? h : (me.b1 ?? 0)); }
    });
    async function poll(start, at) {
      clearTimeout(pollT); if (!on) return;
      if (document.hidden) { pollT = setTimeout(() => poll(), 2000); return; }
      const t0 = Date.now(), sent = t0;
      const r = await api('/hunt/state', start ? { start: 1, tz: TZ, lat: at[0], lng: at[1], col: kitCol(), en: enKm / EN_MAX } : { col: kitCol(), en: enKm / EN_MAX });
      if (!on) return;
      if (r.s === 401) { leave(); toast('Sign in to take flight', true); return; }
      if (r.s === 200 && r.j.now) {
        const t1 = Date.now(); clockSample(r.j.now - (t0 + t1) / 2, t1 - t0);
        if (sent > flySent && !flyWait && r.j.me && (!me || r.j.me.depart >= me.depart - 50)) { const q1 = me && posAt(me, srv()), q2 = posAt(r.j.me, srv()); if (!q1 || !q2 || km(q1, q2) > 0.04 || Math.abs((r.j.me.b1 ?? 0) - (me.b1 ?? 0)) > 0.01) setMe(r.j.me); }   // a flight you just set wins over an older answer; and the same flight (within 40 m) is left alone so your bird never slides
        if (r.j.balance != null) setBal(r.j.balance);
        if (r.j.st) { gSt = r.j.st; gStAt = r.j.now; } mealIn(r.j);
        { const pp = me && posAt(me, srv()); if (pp) for (const b of r.j.birds || []) { if (!b.a || met.has(b.u)) continue; const q = posAt(b, srv()); if (q && km(pp, q) < 3) { met.add(b.u); ghEvent('Met', b.u, '#6ee7b7'); } } }
        birdsIn = true; birds = r.j.birds || []; for (const b of birds) { if (b.r) roles.set(b.u, b.r); else roles.delete(b.u); }
        { const mn = myName(); if (mn) { if (r.j.role) roles.set(mn, r.j.role); else roles.delete(mn); } }
        const now = srv(), ids = new Set((r.j.worms || []).map(w => w.id));
        // a worm that vanished early went to another bird: a little puff where it was
        for (const [id, w] of worms) if (!ids.has(id) && w.gone > now + 800 && !w.mine && w.at) fx.push({ k: 'poof', lat: w.at[0], lng: w.at[1], t0: performance.now(), gold: w.v > 1 });
        const next = new Map(); for (const w of r.j.worms || []) next.set(w.id, worms.get(w.id) || { ...w, seen: performance.now() }); worms = next;
        // starting: if your bird is still out somewhere else (you were hunting a moment ago), go to it
        // starting: your bird is already in the air — still flying from a moment ago, or it takes off on its last heading
        if (start && me) {
          if (me.arrive <= now || me.b1 == null) { let b0 = me.b1 != null ? me.b1 : NaN; if (!isFinite(b0)) try { b0 = parseFloat(localStorage.getItem('pp_hunt_brg')); } catch (e) {} flyDir(isFinite(b0) ? b0 : Math.random() * 6.2832); }
          if (!zoomIn) { const v0 = world.pointOfView(); zoomIn = { la: v0.lat, lo: v0.lng, a: v0.altitude, t0: performance.now() }; } }
      }
      pollT = setTimeout(() => poll(), 2000);
    }
    function setBal(n) { const el = $('huntN'); if (balance != null && n > balance) { const wb = $('ghWormBox'); if (wb) { wb.classList.remove('bump'); void wb.offsetWidth; wb.classList.add('bump'); } el.parentElement.classList.remove('bump'); void el.offsetWidth; el.parentElement.classList.add('bump'); } balance = n; el.textContent = n; }

    // the spot on the ground under a point on the screen. (The library's toGlobeCoords hits the first thing in the scene,
    // and the night layer floats ~10 km up, which at hunting height pulled every tap about two-thirds of the way in
    // toward the bird.) This finds where the line from the camera through the tap meets the ground itself.
    function groundAt(x, y, r) {
      const cam = world.camera(), V = cam.position.constructor, rad = world.getGlobeRadius();
      const o = cam.position.clone(), d = new V(x / r.width * 2 - 1, -(y / r.height) * 2 + 1, 0.5).unproject(cam).sub(o).normalize();
      const b = o.dot(d), c = o.dot(o) - rad * rad, disc = b * b - c; if (disc < 0) return null;
      const t = -b - Math.sqrt(disc), q = o.add(d.multiplyScalar(t)), gc = world.toGeoCoords({ x: q.x, y: q.y, z: q.z });
      return gc && isFinite(gc.lat) ? { lat: gc.lat, lng: gc.lng } : null;
    }
    // tap the map to fly there (drags still move the map; a pinch doesn't count as a tap)
    let down = null;
    const can = world.renderer().domElement;
    can.addEventListener('pointerdown', e => { if (!on) return; down = e.isPrimary ? { x: e.clientX, y: e.clientY, t: Date.now(), n: 1 } : (down && (down.n = 2), down); });
    can.addEventListener('pointerup', e => {
      if (!on || !down || !e.isPrimary) return; const d = down; down = null; if (drowning) return;
      if (d.n > 1 || Math.hypot(e.clientX - d.x, e.clientY - d.y) > 10 || Date.now() - d.t > 400 || !me) return;
      // tap anywhere: the bird turns and flies that way (and keeps going)
      const r = can.getBoundingClientRect(), g = groundAt(e.clientX - r.left, e.clientY - r.top, r); if (!g) return;
      // a tap on your own bird lands it right where it is (wings folded, standing on the ground); tap it again to take off
      // the way it's facing, or tap anywhere else to take off that way
      const p = posAt(me, srv()), bs = sc(p[0], p[1]);
      if (bs && Math.hypot(e.clientX - r.left - bs.x, e.clientY - r.top - bs.y) < 26) {
        const up = () => { landed = false; const h = headAt(me, srv()); flyDir(h != null ? h : (me.b1 ?? 0)); };
        if (!landed) landNow(); else if (enKm > 0.5) up(); else eatWorm(up);
        return; }
      const go = () => { landed = false; flyDir(bearing(p, [g.lat, g.lng])); target = { lat: g.lat, lng: g.lng, t0: performance.now() }; };
      if (landed && enKm <= 0.5) { eatWorm(go); return; }
      go();
    });

    async function tryCatch(w) {
      if (asking.has(w.id)) return; asking.add(w.id);
      const r = await api('/hunt/catch', { id: w.id });
      if (r.s === 200 && r.j.ok) { w.mine = true; worms.delete(w.id); ghEvent('+' + (r.j.value || 1), r.j.value > 1 ? 'Caught a rare worm' : 'Caught a worm', r.j.value > 1 ? '#c084fc' : '#e8555c'); fx.push({ k: 'catch', lat: w.at ? w.at[0] : w.lat, lng: w.at ? w.at[1] : w.lng, t0: performance.now(), v: r.j.value }); if (r.j.balance != null) setBal(r.j.balance); return; }
      if (r.s === 409) { worms.delete(w.id); if (!seenTaken.has(w.id)) { seenTaken.add(w.id); fx.push({ k: 'poof', lat: w.at ? w.at[0] : w.lat, lng: w.at ? w.at[1] : w.lng, t0: performance.now(), by: r.j.by, gold: w.v > 1 }); } return; }
      if (r.s === 410 || r.s === 404) { worms.delete(w.id); return; }
      setTimeout(() => asking.delete(w.id), 800);   // not close enough on the server's clock yet: try again in a moment
    }

    // ── drawing ──
    // right on the ground: anything drawn even a few km up slides against the map when the camera is this low
    const sc = (la, lo) => world.getScreenCoords(la, lo, 0);
    // a simple bird seen from above in the bird's colour; the beak points where it's going
    // each player's head seen from above ("B" size without eyes, the user's pick 2026-11-26): colours taken from their own
    // logo bird (crown, a lighter face toward the beak, the beak itself, and their crest if they have one). Admins get the
    // top hat seen from above. Worked out once per player from their logo picture.
    const heads = new Map();
    function headInfo(n) {
      if (!n) return null; const adm = roles.get(n) === 'admin', key = (adm ? 'A:' : '') + n, v = heads.get(key);
      if (v !== undefined) return v && v.crown ? v : null;
      const K = window._ppKit; if (!K || !K.describe || !kitReady) return null; heads.set(key, 'wait');
      (async () => {
        let im; if (adm) { im = new Image(); im.src = '/admin-bird.png'; await im.decode(); }
        else { const em = clanOf(n), g = await new Promise(res => { const x = K.get(n, em, 'f'); if (x && (x.f || x.fail)) return res(x); K.sub(n, em, () => res(K.get(n, em, 'f')), 'f'); setTimeout(() => res(null), 10000); });
          if (!g || g.fail || !g.f) return null; im = new Image(); im.src = g.f; await im.decode(); }
        const W = im.naturalWidth, H2 = im.naturalHeight, c = document.createElement('canvas'); c.width = W; c.height = H2; const x = c.getContext('2d'); x.drawImage(im, 0, 0);
        const D = x.getImageData(0, 0, W, H2).data; let x0 = W, y0 = H2, x1 = 0, y1 = 0;
        for (let yy = 0; yy < H2; yy += 2) for (let xx = 0; xx < W; xx += 2) if (D[(yy * W + xx) * 4 + 3] > 120) { if (xx < x0) x0 = xx; if (xx > x1) x1 = xx; if (yy < y0) y0 = yy; if (yy > y1) y1 = yy; }
        const bw = x1 - x0, bh = y1 - y0, avg = (fx0, fx1, fy0, fy1) => { let r = 0, gg = 0, b = 0, k = 0;
          for (let yy = Math.round(y0 + bh * fy0); yy < y0 + bh * fy1; yy += 2) for (let xx = Math.round(x0 + bw * fx0); xx < x0 + bw * fx1; xx += 2) { const i = (yy * W + xx) * 4; if (D[i + 3] > 200) { r += D[i]; gg += D[i + 1]; b += D[i + 2]; k++; } }
          return k ? [r / k, gg / k, b / k] : null; };
        if (adm) return { crown: avg(.45, .8, .62, .78) || [155, 184, 185], face: avg(.2, .45, .62, .8) || [190, 205, 210], beak: avg(0, .14, .78, .92) || [150, 150, 158], hat: true };
        const d = K.describe(n);
        return { crown: avg(.45, .85, .18, .38) || [120, 120, 120], face: avg(.18, .42, .38, .62) || [200, 200, 200], beak: avg(0, .12, .45, .7) || [60, 60, 60], crest: d.tops && d.tops.length ? avg(.35, .75, 0, .14) : null };
      })().then(o => heads.set(key, o || 'fail')).catch(() => heads.set(key, 'fail'));
      return null;
    }
    // drawn in the bird's own (unscaled) units: the head sits over the plain bird's head and beak
    function drawHead(c, L, roll, dip) {
      const hx = 9, hy = roll, r = 4.3, rgb = v => `rgb(${v.map(Math.round).join(',')})`;
      c.save(); c.translate(hx + 7 * (dip || 0), hy); if (dip) c.scale(1 - 0.3 * dip, 1 - 0.3 * dip);   // ducking down to the ground: forward and a little further away
      if (L.crest) { c.fillStyle = rgb(L.crest); for (const a of [-.5, 0, .5]) { c.save(); c.rotate(a); c.beginPath(); c.ellipse(-r * 1.15, 0, r * .95, r * .32, 0, 0, 7); c.fill(); c.restore(); } }
      c.beginPath(); c.arc(0, 0, r, 0, 7); c.fillStyle = rgb(L.crown); c.fill();
      c.save(); c.beginPath(); c.arc(0, 0, r, 0, 7); c.clip(); c.beginPath(); c.ellipse(r * .75, 0, r * .75, r * .95, 0, 0, 7); c.fillStyle = rgb(L.face); c.fill(); c.restore();
      c.beginPath(); c.arc(0, 0, r, 0, 7); c.lineWidth = .8; c.strokeStyle = 'rgba(0,0,0,.35)'; c.stroke();
      c.beginPath(); c.moveTo(r * .92, -r * .32); c.lineTo(r * 1.75, 0); c.lineTo(r * .92, r * .32); c.closePath(); c.fillStyle = rgb(L.beak); c.fill(); c.lineWidth = .5; c.strokeStyle = 'rgba(0,0,0,.35)'; c.stroke();
      if (L.hat) { c.beginPath(); c.arc(-r * .2, 0, r * .78, 0, 7); c.fillStyle = '#16171c'; c.fill(); c.lineWidth = 1.1; c.strokeStyle = '#d4af37'; c.stroke();   // top hat from above: crown with a gold band
        c.beginPath(); c.arc(-r * .2, 0, r * .45, 0, 7); c.fillStyle = '#26272e'; c.fill(); }
      c.restore();
    }
    function drawBird(x, y, a, name, s, alpha, swoop, ps, colIn) {
      const c = cx, c0 = colIn || col(name), cl = css(c0), dk = css(shade(c0)), sw = swoop || 0, k = s * 0.8 * (1 - 0.2 * sw), bk = ps.bk, ab = Math.abs(bk), span = ps.span;
      // in a turn it glides with its wings out; seen from above, the wing it leans toward looks shorter
      const qL = span * (bk < 0 ? 1 - 0.4 * ab : 1 - 0.05 * ab), qR = span * (bk > 0 ? 1 - 0.4 * ab : 1 - 0.05 * ab), roll = bk * 2;
      const shape = () => { c.beginPath();
        c.moveTo(12, roll);                                                // head
        c.quadraticCurveTo(10, -4 + roll, 4, -4.5 + roll);
        c.quadraticCurveTo(0, -20 * qL, -8, -27 * qL);                     // left wing tip
        c.quadraticCurveTo(-6, -12 * qL, -8, -4 + roll);
        c.lineTo(-17, -6 + roll); c.lineTo(-14, roll); c.lineTo(-17, 6 + roll); c.lineTo(-8, 4 + roll);   // tail
        c.quadraticCurveTo(-6, 12 * qR, -8, 27 * qR);                      // right wing tip
        c.quadraticCurveTo(0, 20 * qR, 4, 4.5 + roll);
        c.quadraticCurveTo(10, 4 + roll, 12, roll); c.closePath(); };
      c.save(); c.globalAlpha = alpha;
      const so = (8 - 7 * sw) * s * (1 + 0.12 * (ps.lift || 0));   // the shadow bobs a little with each beat
      c.save(); c.translate(x + so * 0.4, y + so); c.rotate(a); c.scale(k, k); c.fillStyle = 'rgba(0,0,0,.22)'; shape(); c.fill(); c.restore();
      c.save(); c.translate(x, y); c.rotate(a); c.scale(k, k);
      shape(); c.fillStyle = cl; c.fill(); c.lineJoin = 'round'; c.lineWidth = 0.8 / k; c.strokeStyle = 'rgba(8,10,14,.35)'; c.stroke();   // a thin dark outline, so the bird stands out on busy maps
      // the lowered wing is a little in shadow
      if (ab > 0.05) { c.save(); c.beginPath(); c.rect(-30, bk > 0 ? roll + 5 : -45, 42, 40 + roll * 0); c.clip(); shape(); c.fillStyle = `rgba(0,0,0,${0.12 * ab})`; c.fill(); c.restore(); }
      { const L = headInfo(name), dp = ps.dip || 0; if (L) drawHead(c, L, roll, dp);   // the player's own head on top, once it's ready (it has its own beak)
        else { c.save(); c.translate(7 * dp, 0); c.beginPath(); c.moveTo(12, -1.8 + roll); c.lineTo(17, roll); c.lineTo(12, 1.8 + roll); c.closePath(); c.fillStyle = dk; c.fill(); c.restore(); } }   // beak
      c.restore(); c.restore();
    }
    // a worm: a tiny wiggling squiggle (rare purple ones are worth 5)
    function drawWorm(x, y, w, t, e) {
      const c = cx, gold = w.v > 1, n = Math.max(1, Math.round(8 * e));
      // half in the ground while coming up / going down: a little hole and a shorter worm
      if (e < 1) { c.beginPath(); c.arc(x - 5, y, 1.8, 0, 7); c.fillStyle = `rgba(60,38,20,${0.7 * (1 - e)})`; c.fill(); }
      c.save(); c.globalAlpha = Math.max(0.3, e); c.beginPath();
      for (let i = 0; i <= n; i++) { const f = i / 8, px = x - 5 + f * 10, py = y + Math.sin(t * 4 + f * 6) * 1.6; i ? c.lineTo(px, py) : c.moveTo(px, py); }
      c.lineCap = 'round'; c.lineJoin = 'round';
      c.strokeStyle = 'rgba(0,0,0,.35)'; c.lineWidth = 3.6; c.stroke();
      c.strokeStyle = gold ? '#c084fc' : '#e8555c'; c.lineWidth = 2.2; c.stroke();
      c.restore();
    }
    function drawEdge(x, y, gold, t) {
      // a worm off the screen: an arrow on the edge pointing at it
      const m = 26, topY = ghTopB + 22, botY = (ghBotT || H) - 26;
      const cx0 = W / 2, cy0 = (topY + botY) / 2, dx = x - cx0, dy = y - cy0;
      const sx = (W / 2 - m) / Math.abs(dx || 1e-6), sy = ((botY - topY) / 2) / Math.abs(dy || 1e-6), f = Math.min(sx, sy);
      const ex = cx0 + dx * f, ey = cy0 + dy * f, a = Math.atan2(dy, dx), pulse = 1;
      const c = cx; c.save(); c.translate(ex, ey); c.rotate(a); c.globalAlpha = pulse;
      c.beginPath(); c.moveTo(5, 0); c.lineTo(-3, -4); c.lineTo(-3, 4); c.closePath();
      c.fillStyle = gold ? 'rgba(192,132,252,.85)' : 'rgba(232,85,92,.75)'; c.fill(); c.restore();
    }
    // ── out of the game: your bird and everyone else's on the globe ──
    // Zoomed out, every bird is a small dot in its colour (anyone can see them; colours only, never names); yours is
    // bigger, solid and ringed in white. Zoomed in a fair way, birds show as they look in the game: flying ones fly,
    // stopped ones sleep curled up in a little nest. Yours sleeps in its nest where you left it (before your first
    // flight, over your home city); tap it and it wakes, flaps up out of the nest, and the game carries on from there.
    const ICON_ALT = 0.25;
    // Birds, nests and name pills that sit on the map are each drawn into their own small picture element and moved with
    // a transform, the same way as the map's place names. (On iPhones the see-through drawing layer reaches the screen a
    // frame apart from the map, so anything drawn on it that moves with the map shook against it; the place names never
    // did.) The game layer keeps your own bird, which stays in the middle, and things fixed to the screen.
    const spLayer = document.createElement('div'); spLayer.className = 'hunt-sp'; host.insertBefore(spLayer, cv);
    const sprites = new Map(), SPR = Math.min(3, Math.max(1, devicePixelRatio || 1)); let spFrame = 0;
    function intoSprite(key, w, h, x, y, fn) {
      w = Math.ceil(w / 8) * 8; h = Math.ceil(h / 8) * 8;
      let sp = sprites.get(key); if (!sp) { const el = document.createElement('canvas'); spLayer.appendChild(el); sp = { el, ctx: el.getContext('2d') }; sprites.set(key, sp); }
      if (sp.w !== w || sp.h !== h) { sp.w = w; sp.h = h; sp.el.width = Math.ceil(w * SPR); sp.el.height = Math.ceil(h * SPR); sp.el.style.width = w + 'px'; sp.el.style.height = h + 'px'; sp.src = null; }
      if (sp.used !== spFrame - 1 && sp.el.style.display === 'none') sp.el.style.display = '';
      sp.used = spFrame;
      if (fn) { const old = cx; cx = sp.ctx; try { cx.setTransform(SPR, 0, 0, SPR, 0, 0); cx.clearRect(0, 0, w, h); fn(w / 2, h / 2); } finally { cx = old; } }
      sp.el.style.transform = `translate3d(${x - w / 2}px,${y - h / 2}px,0)`; return sp;
    }
    // a name pill: the pill picture only needs copying in when it changes
    function pillSprite(n, x, y) { const nl = nameImg(n), sp = intoSprite('p:' + n, nl._w, nl._h, x, y, null);
      if (sp.src !== nl) { sp.src = nl; const g = sp.ctx; g.setTransform(SPR, 0, 0, SPR, 0, 0); g.clearRect(0, 0, sp.w, sp.h); g.drawImage(nl, (sp.w - nl._w) / 2, (sp.h - nl._h) / 2, nl._w, nl._h); } }
    function spritesEnd() { for (const sp of sprites.values()) if (sp.used !== spFrame && sp.el.style.display !== 'none') sp.el.style.display = 'none'; spFrame++; }
    let mine = null, dots = [], dotsOff = 0, dotsAt = 0, idleRaf = 0, idleLast = 0, tko = null;
    // (your own bird is in the public list too, maybe a few seconds out of date: it's recognised by its flights' start times)
    const myDeps = new Set(), isMine = d => myDeps.has(d.depart);
    const kitCol = () => { try { const n = myName(); return window._ppKit && window._ppKit.bodyCol && n ? window._ppKit.bodyCol(n).join(',') : undefined; } catch (e) { return undefined; } };
    const loadMine = () => { if (!tok()) { mine = null; return; }
      api('/hunt/me', { tz: TZ, col: kitCol(), en: enKm / EN_MAX }).then(r => { if (r.s !== 200 || !r.j) return; mealIn(r.j); drownedIn(r.j); mine = { me: r.j.me, home: r.j.home, wet: r.j.wet || 0 }; if (r.j.me) myDeps.add(r.j.me.depart);
        const mn = myName(); if (mn) { if (r.j.role) roles.set(mn, r.j.role); else roles.delete(mn); }
        if (!window._ppKit) loadKit(() => { if (r.j.me) api('/hunt/me', { tz: TZ, col: kitCol(), en: enKm / EN_MAX }); }); }); };
    const parseCol = c => { const v = typeof c === 'string' ? c.split(',').map(Number) : null; return v && v.length === 3 && v.every(x => x >= 0 && x <= 255) ? v : [214, 218, 226]; };
    // (signed in, the list also has each bird's name and role, so sleeping birds show their owner's own logo bird)
    const loadDots = () => fetch(API + '/hunt/dots', { headers: hdr() }).then(r => r.json()).then(j => { if (!j || !Array.isArray(j.b)) return; dotsOff = j.now - Date.now();
      dotsAt = j.now; dots = j.b.map((d, i) => ({ i, from: [d[0], d[1]], to: [d[0], d[1]], b0: d[2], b1: d[3], depart: d[4], arrive: d[5], col: parseCol(d[6]), u: d[7] || null, wet: d[9] === 1 }));
      for (const d of j.b) if (d[7]) { if (d[8]) roles.set(d[7], d[8]); else if (d[7] !== myName()) roles.delete(d[7]); } }).catch(() => {});
    // (a bird can be paused on someone else's phone at any moment: the dots are fetched every 8 s and a moving one is only
    // carried on for up to 8 s past the latest news of it, so a stopped bird's dot doesn't keep drifting away)
    loadMine(); loadDots(); setInterval(() => { if (!document.hidden) loadDots(); }, 8000); setInterval(() => { if (!document.hidden && !on) loadMine(); }, 30000);
    // a stopped bird sleeps in a little woven nest: twigs all round the rim and down into the bowl, with the rim's shadow
    // falling into it for depth. The bird is curled up in its own colour: round and fluffed, one wing folded over its
    // back, head turned and tucked onto its shoulder, breathing slowly, with little z's drifting up.
    const lift = (cl, f) => cl.map(v => Math.max(0, Math.min(255, Math.round(v * f))));
    function drawNest(x, y, k, alpha) {
      const c = cx; c.save(); c.globalAlpha = alpha == null ? 1 : alpha; c.translate(x, y); c.scale(k * 1.15, k * 1.15); c.lineCap = 'round';
      c.beginPath(); c.ellipse(1.5, 3.5, 15.5, 12.5, 0, 0, 7); c.fillStyle = 'rgba(0,0,0,.3)'; c.fill();                                        // shadow on the ground
      let g = c.createRadialGradient(-4, -4, 2, 0, 0, 16); g.addColorStop(0, '#94653b'); g.addColorStop(1, '#6a4425');
      c.beginPath(); c.ellipse(0, 0, 15, 12.5, 0, 0, 7); c.fillStyle = g; c.fill();                                                             // rim
      // the bowl: the same woven twigs, darker the deeper they go
      c.save(); c.beginPath(); c.ellipse(0, 0.6, 10.2, 8.2, 0, 0, 7); c.clip();
      g = c.createRadialGradient(0, 1.5, 1, 0, 0.6, 10.5); g.addColorStop(0, '#6f4a28'); g.addColorStop(1, '#8a5f37'); c.fillStyle = g; c.fill();
      for (let i = 0; i < 26; i++) { const r = 2 + (i % 5) * 1.8, a0 = i * 0.73 + (i % 4) * 0.5, l = 0.7 + (i % 3) * 0.3;
        c.beginPath(); c.ellipse(0, 0.8, r, r * 0.8, 0, a0, a0 + l); c.strokeStyle = i % 2 ? 'rgba(170,122,78,.6)' : 'rgba(110,74,42,.55)'; c.lineWidth = 0.9 + (i % 3) * 0.25; c.stroke(); }
      g = c.createLinearGradient(0, -8, 0, 4); g.addColorStop(0, 'rgba(0,0,0,.3)'); g.addColorStop(1, 'rgba(0,0,0,0)');                     // the rim's shadow inside
      c.fillStyle = g; c.fillRect(-11, -9, 22, 14); c.restore();
      for (let i = 0; i < 22; i++) { const a0 = i * 0.2856 + (i % 3) * 0.4, r = 11.2 + (i % 4) * 0.9, l = 0.5 + (i % 5) * 0.08;          // rim twigs
        c.beginPath(); c.ellipse(0, 0, r, r * 0.83, 0, a0, a0 + l); c.strokeStyle = i % 2 ? '#b0814f' : '#8f6238'; c.lineWidth = 1.1 + (i % 3) * 0.35; c.stroke(); }
      c.restore();
    }
    // each player's own logo bird with its eyes shut, for their sleeper (made once per player): the sign-up nest's eyelid
    // (same spot, coloured from the feathers just above the eye, with a soft edge) and a smooth sleepy lash line, then
    // trimmed to the bird. Admins use the admin bird (top hat) picture, like their logo everywhere else.
    const sleepy = new Map(), ADMIN_EYE = { x: 160, y: 272, r: 30, w: 369, h: 438 };
    function sleepyLogo(n) {
      const adm = roles.get(n) === 'admin', key = (adm ? 'A:' : '') + n, v = sleepy.get(key);
      if (v !== undefined) return v instanceof HTMLCanvasElement ? v : null;
      const K = window._ppKit; if (!K || !K.eye || !kitReady) return null; sleepy.set(key, 'wait');
      (async () => {
        let src, e;
        if (adm) { const im = new Image(); im.src = '/admin-bird.png'; await im.decode(); const W = Math.max(im.width, im.height), sx = W / ADMIN_EYE.h;
          src = document.createElement('canvas'); src.width = src.height = W; src.getContext('2d').drawImage(im, (W - im.width) / 2, (W - im.height) / 2);
          e = { x: ADMIN_EYE.x * sx + (W - im.width) / 2, y: ADMIN_EYE.y * sx + (W - im.height) / 2, r: ADMIN_EYE.r * sx, W }; }
        else { const em = clanOf(n), g = await new Promise(res => { const x = K.get(n, em, 'f'); if (x && (x.f || x.fail)) return res(x); K.sub(n, em, () => res(K.get(n, em, 'f')), 'f'); setTimeout(() => res(null), 10000); });
          if (!g || g.fail || !g.f) return null; src = new Image(); src.src = g.f; await src.decode(); e = K.eye(em); }
        const W = e.W, c = document.createElement('canvas'); c.width = c.height = W; const x = c.getContext('2d'); x.drawImage(src, 0, 0, W, W);
        let R = 0, G = 0, B = 0, m = 0;
        for (const [dx, dy] of [[0, -1.32], [-.45, -1.25], [.45, -1.25], [0, -1.45]]) { const q = x.getImageData(Math.round(e.x + dx * e.r), Math.round(e.y + dy * e.r), 1, 1).data; if (q[3] > 200) { R += q[0]; G += q[1]; B += q[2]; m++; } }
        const c0 = m ? [R / m | 0, G / m | 0, B / m | 0] : [200, 200, 200], d = e.r * 2.3;
        x.save(); x.shadowColor = css(c0); x.shadowBlur = d * .18;
        const gr = x.createRadialGradient(e.x, e.y - d * .22, d * .05, e.x, e.y, d * .52); gr.addColorStop(0, css(c0.map(v => Math.min(255, v * 1.06 | 0)))); gr.addColorStop(.6, css(c0)); gr.addColorStop(1, css(c0.map(v => v * .9 | 0)));
        x.beginPath(); x.arc(e.x, e.y, d / 2, 0, 7); x.fillStyle = gr; x.fill(); x.restore();
        x.save(); x.lineCap = 'round'; x.strokeStyle = 'rgba(40,30,26,.78)'; const L = d * .34, yy = e.y + d * .02;
        x.beginPath(); x.moveTo(e.x - L, yy); x.quadraticCurveTo(e.x, yy + d * .26, e.x + L, yy); x.lineWidth = Math.max(1.6, d * .065); x.stroke();
        x.beginPath(); x.moveTo(e.x - L * .55, yy + d * .07); x.quadraticCurveTo(e.x, yy + d * .2, e.x + L * .55, yy + d * .07); x.lineWidth = Math.max(1.6, d * .09); x.stroke(); x.restore();
        const D = x.getImageData(0, 0, W, W).data; let x0 = W, y0 = W, x1 = 0, y1 = 0;
        for (let yy2 = 0; yy2 < W; yy2++) for (let xx = 0; xx < W; xx++) if (D[(yy2 * W + xx) * 4 + 3] > 40) { if (xx < x0) x0 = xx; if (xx > x1) x1 = xx; if (yy2 < y0) y0 = yy2; if (yy2 > y1) y1 = yy2; }
        const side = Math.max(x1 - x0, y1 - y0) * 1.04, o = document.createElement('canvas'); o.width = o.height = Math.max(1, Math.ceil(side));
        o.getContext('2d').drawImage(c, (x0 + x1) / 2 - side / 2, (y0 + y1) / 2 - side / 2, side, side, 0, 0, side, side); return o;
      })().then(o => sleepy.set(key, o || 'fail')).catch(() => sleepy.set(key, 'fail'));
      return null;
    }
    function drawDrowning(x, y, a, cl, k, t, seed, name) {
      const c = cx, T = t + seed;
      for (let i = 0; i < 3; i++) { const ph = (T * 0.9 + i / 3) % 1;
        c.beginPath(); c.ellipse(x, y, (7 + ph * 20) * k, (7 + ph * 20) * k * 0.8, 0, 0, 7); c.strokeStyle = `rgba(220,236,255,${(1 - ph) * 0.5})`; c.lineWidth = 1.2; c.stroke(); }
      const cyc = T % 2.6, burst = cyc < 0.9 ? Math.sin(Math.PI * cyc / 0.9) : 0, flap = burst * (0.5 + 0.5 * Math.sin(T * 22));   // every few seconds a weak, frantic burst of flapping
      const under = 0.5 + 0.5 * Math.sin(T * 1.3), rock = Math.sin(T * 2.3) * 0.12;
      drawBird(x, y + under * 1.2 * k, a + rock, name, 0.9 * k, 1 - 0.3 * under, 1, { span: 0.32 + 0.5 * flap, bk: 0, lift: flap }, cl);
      c.save(); c.translate(x, y + under * 1.2 * k); c.rotate(a + rock);   // mostly under the surface
      const g = c.createRadialGradient(-6 * k, 0, 1, -6 * k, 0, 12 * k); g.addColorStop(0, 'rgba(30,62,92,.6)'); g.addColorStop(1, 'rgba(30,62,92,0)');
      c.beginPath(); c.ellipse(-6 * k, 0, 12 * k, 8 * k, 0, 0, 7); c.fillStyle = g; c.fill(); c.restore();
      c.fillStyle = 'rgba(235,245,255,.85)';
      if (burst > 0.15) for (let i = 0; i < 5; i++) { const an = i * 1.26 + T * 3, r = (9 + 5 * burst) * k; c.beginPath(); c.arc(x + Math.cos(an) * r, y + Math.sin(an) * r * 0.8 - burst * 3 * k, 1.1 * k, 0, 7); c.fill(); }   // splashes
      for (let i = 0; i < 2; i++) { const u = (T * 0.7 + i * 0.5) % 1; c.globalAlpha = (1 - u) * 0.8; c.beginPath(); c.arc(x + (6 + i * 3) * k * Math.cos(a), y + (6 + i * 3) * k * Math.sin(a) - u * 8 * k, (0.8 + u) * k, 0, 7); c.strokeStyle = 'rgba(235,245,255,.9)'; c.lineWidth = 0.7; c.stroke(); } c.globalAlpha = 1;   // bubbles
    }
    function drawSleeper(x, y, a, cl, k, t, seed, zs, alpha, name) {
      // asleep in the nest ("B5", the user's pick): a round body in the bird's colour with a little tail, the player's own
      // logo bird as the head with its eyes shut (a plain soft head when we don't know whose bird it is), and a wing
      // wrapped round the front like a blanket. Head on the left with the beak pointing out of the nest; breathing slowly.
      cx.save(); if (alpha != null) cx.globalAlpha = alpha;
      const c = cx, br = 1 + 0.03 * Math.sin(t * 2.1 + seed), lg = name ? sleepyLogo(name) : null, adm = name && roles.get(name) === 'admin';
      const G = (col, x0, y0, r, hi, lo) => { const g = c.createRadialGradient(x0 - r * 0.35, y0 - r * 0.45, r * 0.1, x0, y0, r * 1.05); g.addColorStop(0, css(lift(col, hi))); g.addColorStop(0.65, css(col)); g.addColorStop(1, css(lift(col, lo))); return g; };
      c.save(); c.translate(x, y); c.scale(-k * br, k * br);
      // body, tail and wing are drawn smaller (BS), shrunk toward the neck so the head stays on and the same size
      const BS = 1.0, small = f => { c.save(); c.translate(3, -1); c.scale(BS, BS); c.translate(-3, 1); f(); c.restore(); };
      small(() => {
      c.save(); c.translate(-6.5, 0.8); c.scale(1.0, 0.85); c.translate(8.5, -0.8);   // tucked 2 units further in under the body, 15% narrower (and stretched a little longer from its base)
      c.beginPath(); c.moveTo(-8.5, -2.4); c.quadraticCurveTo(-13, -2.4, -18, -5); c.quadraticCurveTo(-15.4, 0.6, -18, 6.2); c.quadraticCurveTo(-13, 4.2, -8.5, 4); c.closePath();   // tail: swept out like the flying bird's (option 4, 2026-11-26)
      c.fillStyle = css(lift(cl, 0.8)); c.fill(); c.lineJoin = 'round'; c.lineWidth = 0.7; c.strokeStyle = 'rgba(8,10,14,.3)'; c.stroke(); c.restore();
      c.beginPath(); c.moveTo(5.6, 1.4); c.bezierCurveTo(5.6, -6.6, -3, -6.6, -7.5, -2.2); c.quadraticCurveTo(-11.4, 0.8, -7.5, 4.4); c.bezierCurveTo(-3, 9.4, 5.6, 9.4, 5.6, 1.4); c.fillStyle = G(cl, -1.6, 1.4, 7.6, 1.18, 0.82); c.fill();   // body: round at the front, a longer back running into the tail
      });
      if (lg) { const hs = adm ? 20.7 : 17.5;   /* 8% smaller, 2026-11-26 */ c.save(); c.translate(adm ? 4.4 : 4.6, adm ? -8.2 : -4.4); /* the admin picture has its top hat above the head, so it sits higher to put the face where everyone else's is */ c.scale(-1, 1); c.rotate(-0.3); c.drawImage(lg, -hs / 2, -hs / 2, hs, hs); c.restore(); }
      else { const hc = lift(cl, 1.4); c.beginPath(); c.arc(4.4, -3.6, 5.15, 0, 7); c.fillStyle = G(hc, 4.4, -3.6, 5.15, 1.12, 0.92); c.fill(); }   // head
      small(() => { c.beginPath(); c.moveTo(-8.4, 2.2); c.quadraticCurveTo(-3.2, 10, 5.4, 3.6); c.quadraticCurveTo(1, 1.6, -1.8, 1.9); c.quadraticCurveTo(-5.8, 1.7, -8.4, 2.2); c.fillStyle = css(lift(cl, 0.86)); c.fill(); });   // wing
      c.restore();
      if (zs) { c.save(); c.fillStyle = '#e2e8f0'; c.shadowColor = 'rgba(0,0,0,.85)'; c.shadowBlur = 3;
        for (let i = 0; i < 2; i++) { const u = ((t + seed + i * 1.3) % 2.6) / 2.6; c.globalAlpha = Math.sin(Math.PI * u) * 0.85;
          c.font = `700 ${(6 + 4 * u) * Math.max(0.55, k)}px -apple-system,system-ui,sans-serif`; c.fillText('z', x + 11 * k + 8 * u * k, y - 10 * k - 14 * u * k); }
        c.restore(); }
      cx.restore();
    }
    const idleAng = new Map();
    function idle(ts) {
      if (on) return; idleRaf = requestAnimationFrame(idle); dotFlyStep();
      const dt = idleLast ? Math.min(0.1, Math.max(0, ts - idleLast) / 1000) : 0.016; idleLast = ts;
      const cr = cv.getBoundingClientRect(), c = cx; c.setTransform(DPR, 0, 0, DPR, 0, 0); c.clearRect(0, 0, W, H);
      try { world.camera().updateMatrixWorld(); } catch (e) {}
      const v = world.pointOfView(), cosCap = Math.cos(Math.acos(1 / (1 + v.altitude)) * 0.97), tn = Date.now() + dotsOff, t = performance.now() / 1000;
      // birds are drawn to the map's scale: exactly game size at game height, smaller as you zoom out (and bigger if you
      // zoom in past it, up to 2x); once a bird would be too small to make out it's a dot
      const km2 = Math.min(2, GAME_ALT / v.altitude), close = km2 >= 0.4;
      const front = (la, lo) => Math.sin(v.lat * R) * Math.sin(la * R) + Math.cos(v.lat * R) * Math.cos(la * R) * Math.cos((lo - v.lng) * R) > cosCap;
      const scr = (la, lo) => front(la, lo) ? world.getScreenCoords(la, lo, 0) : null;
      const onScr = s => s && s.x > -30 && s.x < W + 30 && s.y > -30 && s.y < H + 30;
      const mn = myName(), mp = mine && (mine.me ? flyAt(mine.me, tn) : mine.home);
      // everyone else
      for (const d of dots) { const tq = Math.min(tn, dotsAt + 8000), q = flyAt(d, tq); if (!q) continue;
        if (isMine(d) || (d.u && d.u === mn) || (mp && km(mp, q) < 0.05)) continue;   // that's you
        const s = scr(q[0], q[1]); if (!onScr(s)) continue;
        if (!close) { // everyone else: a solid dot in their colour with a thin light edge (easy to spot, but smaller than yours)
          c.beginPath(); c.arc(s.x, s.y, 4.1, 0, 7); c.fillStyle = 'rgba(0,0,0,.4)'; c.fill();
          c.beginPath(); c.arc(s.x, s.y, 3.4, 0, 7); c.fillStyle = 'rgba(255,255,255,.8)'; c.fill();
          c.beginPath(); c.arc(s.x, s.y, 2.6, 0, 7); c.fillStyle = css(d.col); c.fill(); continue; }
        const flying = tq < d.arrive, hd = headAt(d, tq), a0 = hd != null ? hd - Math.PI / 2 : -Math.PI / 2;
        const sk = 'o:' + (d.u || d.i), sz = 76 * Math.max(0.5, km2);
        if (!flying && d.wet) { intoSprite(sk, sz, sz, s.x, s.y, (x, y) => drawDrowning(x, y, a0, d.col, 0.8 * km2, t, d.i * 0.77, d.u)); continue; }
        if (!flying) { intoSprite(sk, sz, sz, s.x, s.y, (x, y) => { drawNest(x, y, 0.8 * km2); drawSleeper(x, y, a0, d.col, 0.8 * km2, t, d.i * 0.77, true, null, d.u); }); continue; }
        let a = idleAng.get(d.i) ?? a0; a = ease(a, a0, dt, 'dot' + d.i); idleAng.set(d.i, a);
        const ps = pose('dot' + d.i, true, bankAt(d, tq), dt); intoSprite(sk, sz, sz, s.x, s.y, (x, y) => drawBird(x, y, a, d.u || '', 0.8 * km2, 0.92, 0, ps, d.col)); }
      // you
      let show = false, dotOn = false;
      if (mn && mp) { const s = scr(mp[0], mp[1]);
        if (onScr(s)) { const cl = col(mn);
          if (!close) { // you: bigger, ringed in white, with a soft glow that slowly pulses so you can always find yourself. It's
            // the button itself that draws it, so it sits above the story pins and can always be tapped
            const mc = css(cl); if (meDot._mc !== mc) { meDot._mc = mc; meDot.style.setProperty('--mc', mc); meDot.style.setProperty('--mg', `rgba(${cl[0]},${cl[1]},${cl[2]},.6)`); }
            meDot.style.transform = `translate3d(${s.x}px,${s.y}px,0)`; dotOn = true;
            show = true; myBtnMode = 'dot'; myBtnAt = mp; myBtn.style.transform = `translate(${cr.left + s.x - 24}px,${cr.top + s.y - 24}px)`; }
          else { const hd = mine.me ? headAt(mine.me, tn) : null, a = hd != null ? hd - Math.PI / 2 : -Math.PI / 2;
            const msz = 96 * Math.max(0.5, km2);
            const myWet = mine.wet && mine.wet > Date.now() + dotsOff;
            if (!tko && myWet) intoSprite('me', msz, msz, s.x, s.y, (x, y) => drawDrowning(x, y, a, cl, 0.8 * km2, t, 0, mn));
            else if (!tko) intoSprite('me', msz, msz, s.x, s.y, (x, y) => { drawNest(x, y, 0.8 * km2); drawSleeper(x, y, a, cl, 0.8 * km2, t, 0, true, null, mn); });   // same size as everyone else's nest
            else { // waking up: the wings open, it flaps hard and lifts off (its shadow drops away), the nest fades out
              const u = (performance.now() - tko.t0) / 1000, e = Math.min(1, u / 0.9), ez = e * e * (3 - 2 * e), sw = 1 - 1.4 * ez;
              const ps = pose('@tko', true, 0, dt * 1.6), fin = Math.min(1, u / 0.25); ps.span = 0.32 + (ps.span - 0.32) * fin;
              intoSprite('me', msz, msz, s.x, s.y, (x, y) => {
                if (tko.wet) { const k = 0.8 * km2; for (let i = 0; i < 3; i++) { const ph = (t * 0.9 + i / 3) % 1;   // out of the water: no nest, just the ripples it leaves behind, fading
                    cx.beginPath(); cx.ellipse(x, y, (7 + ph * 20) * k, (7 + ph * 20) * k * 0.8, 0, 0, 7); cx.strokeStyle = `rgba(220,236,255,${(1 - ph) * 0.5 * (1 - ez)})`; cx.lineWidth = 1.2; cx.stroke(); } }
                else { drawNest(x, y, 0.8 * km2, 1 - ez);
                  if (fin < 1) drawSleeper(x, y, a, cl, 0.8 * km2, t, 0, false, 1 - fin, mn); }   // the sleeping bird uncurls into the flying one
                drawBird(x, y - 6 * ez * km2, a, mn, km2 * (0.8 + 0.2 * ez) / (1 - 0.2 * sw), tko.wet ? 1 : fin, sw, ps, cl); });   // grows to its game size as it lifts off
              if (u > 0.95) { tko = null; enter(); } }
            show = !tko; myBtnMode = 'bird'; myBtn.style.transform = `translate(${cr.left + s.x - 24}px,${cr.top + s.y - 24}px)`; } } }
      if (myBtn.classList.contains('in') !== show) myBtn.classList.toggle('in', show);
      if (meDot.classList.contains('on') !== dotOn) meDot.classList.toggle('on', dotOn);
      { const lb = myBtnMode === 'dot' ? 'Go to my bird' : 'Take flight'; if (myBtn.getAttribute('aria-label') !== lb) myBtn.setAttribute('aria-label', lb); }
      spritesEnd();
    }
    idleRaf = requestAnimationFrame(idle);
    // a player's name under their bird: drawn once into a little image and then moved as a picture, so it glides with
    // the map (text redrawn at a slightly different fraction of a pixel every frame shimmered)
    // other players' names as the site's user pills ("N1", the user's pick): a dark pill with their little tag bird and
    // their name in their tag colour (admins white, mods purple, like everywhere else on the site). Drawn once into a
    // small image (redrawn when the tag bird arrives) and moved as a picture, so it glides with the map.
    const names = new Map(), faceWait = new Set();
    // (the bird kit must have finished starting up before it's asked for a bird: the admin bird asked for too early came
    // out blank and stayed blank, which is why borbie's pill had an empty space)
    let kitReady = false; const kitWatch = setInterval(() => { const K = window._ppKit; if (K && K.ready) { clearInterval(kitWatch); Promise.resolve(K.ready).then(() => { kitReady = true; names.clear(); }).catch(() => {}); } }, 200);
    const clanOf = n => { let h = 0; for (let i = 0; i < n.length; i++) h = n.charCodeAt(i) + ((h << 5) - h); return ['🐤', '🐦', '🐧'][Math.abs(h) % 3]; };
    const tagColOf = n => { const r = roles.get(n); if (r === 'admin') return '#ffffff'; if (r === 'mod') return '#c084fc'; try { return window._ppKit ? window._ppKit.tagCol(n) : '#dbe4ee'; } catch (e) { return '#dbe4ee'; } };
    const adminFace = { g: 0, _im: null };
    function tagFace(n) {
      if (roles.get(n) === 'admin') { if (!adminFace._im) { adminFace._im = new Image(); adminFace._im.onload = () => names.clear(); adminFace._im.src = '/admin-bird.png'; }
        return adminFace._im.complete && adminFace._im.naturalWidth ? adminFace : null; }   // admins: the admin bird picture itself
      const K = window._ppKit; if (!K || !kitReady) return null; const adm = false, nm = n, em = clanOf(n);
      const r = K.get(nm, em, 't'); if (r && !r.fail && r.t) { if (!r._im) { r._im = new Image(); r._im.onload = () => names.delete(n); r._im.src = r.t; } return r._im.complete && r._im.naturalWidth ? r : null; }
      if (!r && !faceWait.has(nm)) { faceWait.add(nm); K.sub(nm, em, () => names.delete(n), 't'); } return null; }
    function nameImg(n) { let im = names.get(n); if (im && im._col === tagColOf(n)) return im;
      im = document.createElement('canvas'); const f = '700 7.8px -apple-system,system-ui,sans-serif', m =   // (smaller, 2026-11-26, so it doesn't outweigh the bird)
        document.createElement('canvas').getContext('2d'); m.font = f;
      const face = tagFace(n), tc = tagColOf(n), tw = Math.ceil(m.measureText(n).width), fw = face ? 10 : 0, pw = tw + fw + (face ? 11 : 10), w = pw + 2, h = 15, k = Math.min(3, Math.max(2, devicePixelRatio || 1));
      im.width = w * k; im.height = h * k; im._w = w; im._h = h; im._col = tc;
      const g = im.getContext('2d'); g.scale(k, k); const x0 = 1, y0 = 1, ph = 13, r = 6.5;
      g.beginPath(); g.moveTo(x0 + r, y0); g.arcTo(x0 + pw, y0, x0 + pw, y0 + ph, r); g.arcTo(x0 + pw, y0 + ph, x0, y0 + ph, r); g.arcTo(x0, y0 + ph, x0, y0, r); g.arcTo(x0, y0, x0 + pw, y0, r); g.closePath();
      g.fillStyle = 'rgba(22,25,32,.88)'; g.fill();
      if (face) { const z = 10, w2 = z * (1 + 2 * (face.g || 0)), iw = face._im.naturalWidth, ih = face._im.naturalHeight, sc2 = w2 / Math.max(iw, ih);
        g.drawImage(face._im, x0 + 4 - (w2 - z) / 2 + (w2 - iw * sc2) / 2, y0 + 1.5 - (w2 - z) / 2 + (w2 - ih * sc2) / 2, iw * sc2, ih * sc2); }
      g.font = f; g.fillStyle = tc; g.textBaseline = 'middle'; g.fillText(n, x0 + (face ? 4 + fw + 2.5 : 5), y0 + ph / 2 + 0.5);
      names.set(n, im); return im; }
    // in the game: other players within 100 km who are off the screen get an arrow at the edge with how far away they are
    function drawBirdEdge(x, y, name, d) {
      const m = 30, topY = ghTopB + 26, botY = (ghBotT || H) - 30, cx0 = W / 2, cy0 = (topY + botY) / 2, dx = x - cx0, dy = y - cy0;
      const f = Math.min((W / 2 - m) / Math.abs(dx || 1e-6), ((botY - topY) / 2) / Math.abs(dy || 1e-6)), ex = cx0 + dx * f, ey = cy0 + dy * f, a = Math.atan2(dy, dx), cl = css(col(name));
      const c = cx; c.save(); c.translate(ex, ey); c.save(); c.rotate(a); c.beginPath(); c.moveTo(7, 0); c.lineTo(-3, -5); c.lineTo(-3, 5); c.closePath();
      c.fillStyle = cl; c.shadowColor = 'rgba(0,0,0,.8)'; c.shadowBlur = 3; c.fill(); c.restore();
      c.font = '600 10px -apple-system,system-ui,sans-serif'; c.textAlign = 'center'; c.fillStyle = 'rgba(255,255,255,.9)'; c.shadowColor = 'rgba(0,0,0,.9)'; c.shadowBlur = 3;
      c.fillText(d < 10 ? d.toFixed(1) + ' km' : Math.round(d) + ' km', -Math.cos(a) * 18, -Math.sin(a) * 18 + 3.5); c.restore();
    }
    // the game's own smooth clock: advances by the screen's frame time and is only gently pulled toward the real clock
    // (reading the wall clock each frame wobbles by a few ms, and the bird and map wobbled with it)
    let camT = null;
    function loop(ts) {
      raf = requestAnimationFrame(loop); if (!on) return;
      const pf = ts || performance.now(), dt = lastF ? Math.min(0.1, Math.max(0, pf - lastF) / 1000) : 0.016; lastF = pf;
      { const s0 = srv(); if (camT == null || Math.abs(s0 - camT) > 500) camT = s0; else { camT += dt * 1000; camT += (s0 - camT) * 0.04; } }
      const now = camT, p = me && posAt(me, now);
      frameMs += (Math.min(50, Math.max(8, dt * 1000)) - frameMs) * 0.1; clockStep(Math.min(50, dt * 1000));
      const cc = corrNow(), pv = p && [p[0] + cc[0], p[1] + cc[1]];   // where the bird is drawn (p is where it really is)
      // The globe draws the map earlier in each frame than this loop runs, so everything here is drawn with the camera the
      // map was just drawn with, and only at the end is the camera moved on for the next frame: map, bird, worms and names
      // always move together.
      try { world.camera().updateMatrixWorld(); } catch (e) {}
      if (mapAsk) mapAsk(true);   // map names follow the moving view every frame
      const c = cx, t = performance.now() / 1000, mine = myName();
      c.setTransform(DPR, 0, 0, DPR, 0, 0); c.clearRect(0, 0, W, H);
      const v = world.pointOfView(), cosCap = Math.cos(Math.acos(1 / (1 + v.altitude)) * 0.95);
      const front = (la, lo) => Math.sin(v.lat * R) * Math.sin(la * R) + Math.cos(v.lat * R) * Math.cos(la * R) * Math.cos((lo - v.lng) * R) > cosCap;
      const inView = s => s && s.x > -30 && s.x < W + 30 && s.y > ghTopB - 10 && s.y < (ghBotT || H) + 10;
      // where you tapped: a small ring that fades out
      if (target) { const s = sc(target.lat, target.lng), age = (performance.now() - target.t0) / 1000;
        if (age > 0.6) target = null; else if (s) { c.save(); c.globalAlpha = 0.7 * (1 - age / 0.6); c.strokeStyle = '#fff'; c.lineWidth = 1.5;
          c.beginPath(); c.arc(s.x, s.y, 6 + 14 * age, 0, 7); c.stroke(); c.restore(); } }
      // worms: only there while they're above ground (arrows point to the ones that are up off the screen)
      for (const w of worms.values()) {
        if (w.gone <= now) { worms.delete(w.id); continue; }
        const q = wormAt(w, now);
        if (!q.up) { // about to come up: the dirt stirs a little
          if (q.toUp < 600) { const s = sc(q.lat, q.lng); if (s && inView(s)) { c.save(); c.globalAlpha = 0.6 * (1 - q.toUp / 600); c.fillStyle = '#6b4424'; for (let i = 0; i < 3; i++) { c.beginPath(); c.arc(s.x + Math.cos(t * 9 + i * 2.1) * 2.5, s.y + Math.sin(t * 9 + i * 2.1) * 1.5, 1.3, 0, 7); c.fill(); } c.restore(); } }
          continue; }
        w.at = [q.lat, q.lng];
        if (!front(q.lat, q.lng)) continue;
        const s = sc(q.lat, q.lng); if (!s) continue;
        if (inView(s)) drawWorm(s.x, s.y, w, t, Math.min(1, q.fromUp / 450, q.toDown / 450)); else drawEdge(s.x, s.y, w.v > 1, t);
        if (p && km(p, [q.lat, q.lng]) < CATCH_KM) tryCatch(w);
      }
      // other birds
      for (const b of birds) { const q = posAt(b, now); if (!q || !front(q[0], q[1])) continue; const s = sc(q[0], q[1]); if (!s) continue;
        if (!inView(s)) { const d = p ? km(p, q) : 0; if (d < 100 && b.a) drawBirdEdge(s.x, s.y, b.u, d); continue; }
        const moving = now < b.arrive, ahead = posAt(b, now + 600), s2 = ahead && sc(ahead[0], ahead[1]);
        if (!moving && b.a) { const ha = headAt(b, now), aa = ha != null ? ha - Math.PI / 2 : -Math.PI / 2; intoSprite('b:' + b.u, 76, 76, s.x, s.y, (x, y) => drawBird(x, y, aa, b.u, 1, 0.92, 1, { span: 0.32, bk: 0, lift: 0 }));
          pillSprite(b.u, s.x, s.y + 20); continue; }   // playing but landed: standing on the ground
        if (!moving && b.w) { const ha = headAt(b, now); intoSprite('b:' + b.u, 76, 76, s.x, s.y, (x, y) => drawDrowning(x, y, ha != null ? ha - Math.PI / 2 : 0, col(b.u), 0.8, t, b.u.length, b.u)); pillSprite(b.u, s.x, s.y + 20); continue; }
        if (!moving) { intoSprite('b:' + b.u, 76, 76, s.x, s.y, (x, y) => { drawNest(x, y, 0.8); drawSleeper(x, y, 0, col(b.u), 0.8, t, b.u.length, true, null, b.u); });
          pillSprite(b.u, s.x, s.y + 17); continue; }
        let a = angs.get(b.u) ?? -Math.PI / 2; if (moving && s2 && Math.hypot(s2.x - s.x, s2.y - s.y) > 0.5) a = ease(a, Math.atan2(s2.y - s.y, s2.x - s.x), dt, b.u); angs.set(b.u, a);
        const ps = pose(b.u, moving, bankAt(b, now), dt); intoSprite('b:' + b.u, 76, 76, s.x, s.y, (x, y) => drawBird(x, y, a, b.u, 0.8, 0.92, 0, ps));
        pillSprite(b.u, s.x, s.y + 20); }
      // until the game's first answer arrives (with names), the nests the globe already knew about stay on the screen
      if (!birdsIn) { const tq = Math.min(Date.now() + dotsOff, dotsAt + 8000);
        for (const d of dots) { if (tq < d.arrive || isMine(d) || (d.u && d.u === myName())) continue; const q = flyAt(d, tq); if (!q || (p && km(p, q) < 0.05) || !front(q[0], q[1])) continue;
          const s = sc(q[0], q[1]); if (!inView(s)) continue; const hd = headAt(d, tq); intoSprite('o:' + (d.u || d.i), 76, 76, s.x, s.y, (x, y) => { if (d.wet) { drawDrowning(x, y, hd != null ? hd - Math.PI / 2 : 0, d.col, 0.8, t, d.i * 0.77, d.u); return; } drawNest(x, y, 0.8); drawSleeper(x, y, hd != null ? hd - Math.PI / 2 : 0, d.col, 0.8, t, d.i * 0.77, true, null, d.u); }); } }
      // effects: catches (your bird dives, the worm is pulled up, +1 / +5 rises) and worms another bird took
      let swoop = 0;
      fx = fx.filter(f => { const age = (performance.now() - f.t0) / 1000, s = sc(f.lat, f.lng); if (!s) return age < 1.4;
        if (f.k === 'catch') {
          if (age < 0.5) swoop = Math.max(swoop, Math.sin(Math.PI * age / 0.5));
          if (age < 0.35) { c.save(); c.globalAlpha = 1 - age / 0.35; c.translate(s.x, s.y - 12 * age / 0.35); c.scale(1 - age / 0.35, 1 - age / 0.35); c.beginPath(); c.moveTo(-5, 0); c.quadraticCurveTo(0, -3, 5, 0); c.strokeStyle = f.v > 1 ? '#c084fc' : '#e8555c'; c.lineWidth = 2.2; c.lineCap = 'round'; c.stroke(); c.restore(); }
          c.save(); c.globalAlpha = Math.max(0, 1 - Math.max(0, age - 0.7) / 0.7); c.font = '700 13px -apple-system,system-ui,sans-serif'; c.textAlign = 'center';
          c.fillStyle = f.v > 1 ? '#c084fc' : '#e8555c'; c.shadowColor = 'rgba(0,0,0,.8)'; c.shadowBlur = 3; c.fillText('+' + f.v, s.x, s.y - 18 - 16 * age); c.restore();
          return age < 1.4; }
        if (f.k === 'poof') {
          for (let i = 0; i < 5; i++) { const an = i / 5 * 6.283, d = 3 + 10 * age; c.beginPath(); c.arc(s.x + Math.cos(an) * d, s.y + Math.sin(an) * d * 0.6, Math.max(0, 1.6 * (1 - age / 1.2)), 0, 7); c.fillStyle = `rgba(160,120,90,${Math.max(0, 0.8 - age / 1.2)})`; c.fill(); }
          if (f.by) { c.save(); c.globalAlpha = Math.max(0, 1 - age / 1.6); c.font = '600 10.5px -apple-system,system-ui,sans-serif'; c.textAlign = 'center'; c.fillStyle = 'rgba(226,232,240,.85)'; c.shadowColor = 'rgba(0,0,0,.9)'; c.shadowBlur = 4; c.fillText(f.by + ' got it first', s.x, s.y - 18 - 10 * age); c.restore(); }
          return age < 1.6; }
        return false; });
      // your bird, on top of everything
      if (p) { const s = sc(pv[0], pv[1]);
        if (s) { const moving = now < me.arrive, ah = posAt(me, now + 600), s2 = ah && sc(ah[0] + cc[0], ah[1] + cc[1]);
          if (moving && s2 && Math.hypot(s2.x - s.x, s2.y - s.y) > 0.5) ang = ease(ang, Math.atan2(s2.y - s.y, s2.x - s.x), dt, '@me');
          else if (!moving && !peck) { // sitting still: the beak slowly turns toward the nearest worm
            let best = null, bd = 1e9; for (const w of worms.values()) { if (!w.at) continue; const d = km(p, w.at); if (d < bd) { bd = d; best = w; } }
            const ws = best && sc(best.at[0], best.at[1]);
            if (ws) { const want = Math.atan2(ws.y - s.y, ws.x - s.x); let d = want - ang; d = Math.atan2(Math.sin(d), Math.cos(d)); ang += d * 0.06; } }
          if (!moving && !swoop && (wet || drowning)) {   // treading water: ripples spreading out, bobbing and rocking, sitting low; drowning: sinks and fades
            const u = drowning ? Math.min(1, (performance.now() - drowning.t0) / 1600) : 0, c = cx;
            for (let i = 0; i < 3; i++) { const ph = (t * (drowning ? 1.4 : 0.55) + i / 3) % 1;
              c.beginPath(); c.ellipse(s.x, s.y, 8 + ph * 24, (8 + ph * 24) * 0.8, 0, 0, 7); c.strokeStyle = `rgba(220,236,255,${(1 - ph) * 0.42})`; c.lineWidth = 1.3; c.stroke(); }
            const bob = Math.sin(t * 2.4) * 0.7, rock = Math.sin(t * 1.7) * 0.07, k2 = 1.1 * (1 - 0.5 * u);
            drawBird(s.x, s.y + bob, ang + rock, mine, k2, 1 - 0.95 * u, 1, { span: 0.32, bk: 0, lift: 0 });
            c.save(); c.translate(s.x, s.y + bob); c.rotate(ang + rock);   // the back half under the surface
            const g2 = c.createRadialGradient(-10 * k2, 0, 1, -10 * k2, 0, 9 * k2); g2.addColorStop(0, `rgba(30,62,92,${0.42 + 0.4 * u})`); g2.addColorStop(1, 'rgba(30,62,92,0)');
            c.beginPath(); c.ellipse(-10 * k2, 0, 9 * k2, 6 * k2, 0, 0, 7); c.fillStyle = g2; c.fill(); c.restore(); }
          else if (landed && !moving && !swoop) { let dip = 0;
            if (peck) { const u = Math.min(1, (performance.now() - peck.t0) / PECK_MS);   // a big peck, then a little one
              dip = u < .5 ? Math.sin(Math.PI * u / .5) : u < .85 ? .55 * Math.sin(Math.PI * (u - .5) / .35) : 0;
              if (u < .42) { const e = u < .15 ? 1 : 1 - (u - .15) / .27, wx = s.x + Math.cos(ang) * 22, wy = s.y + Math.sin(ang) * 22;   // the worm lying out in front of the beak, slurped up from the end nearest it
                cx.save(); cx.translate(wx, wy); cx.rotate(ang + Math.PI); cx.scale(.8, .8); drawWorm(0, 0, { v: 1 }, t, Math.max(.05, e)); cx.restore(); } }
            drawBird(s.x, s.y, ang, mine, 1.25, 1, 1, { span: 0.32, bk: 0, lift: 0, dip }); }   // landed: wings folded, standing on the ground
          else drawBird(s.x, s.y, ang, mine, 1, 1, swoop, pose('@me', moving, bankAt(me, now), dt)); } }
      // the screen moves with your bird (kept in the middle): aim at where it will be when the map is next drawn
      // (on entering it glides from where you were looking down to your bird at hunting height over ~1 s)
      if (p) { const tn = now + frameMs, pn = posAt(me, tn), c2 = corrNow(); let la = pn[0] + c2[0], lo = pn[1] + c2[1], al = null;
        if (zoomIn) { const k = Math.min(1, (performance.now() + frameMs - zoomIn.t0) / 1000), e = 1 - Math.pow(1 - k, 3), dl = ((lo - zoomIn.lo + 540) % 360) - 180;
          la = zoomIn.la + (la - zoomIn.la) * e; lo = zoomIn.lo + dl * e; al = zoomIn.a + (GAME_ALT - zoomIn.a) * e; if (k >= 1) zoomIn = null; }
        // (the height is set every frame too: if anything else nudges the camera out, e.g. leftover zoom momentum from a
        // pinch just before take-off, it's back at game height straight away)
        world.pointOfView({ lat: la, lng: lo, altitude: al == null ? GAME_ALT : al }, 0); }
      if (pf > preAt) { preAt = pf + 400; preload(now); }
      // keep flying: a little before the far-ahead point is reached, carry on the same way
      if (p && !landed && me.b1 != null && me.arrive - now < 12000 && performance.now() > extAt) { extAt = performance.now() + 5000; flyDir(headAt(me, now)); }
      // the line under your worm count: day or night where your bird is
      const tEl = $('huntT'); if (tEl) { const hint = Date.now() < hintUntil; if (tEl.classList.contains('on') !== hint) tEl.classList.toggle('on', hint); }
      spritesEnd();
      ghUpdate(now, p);
    }
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
    // you've seen these stories: clears the "new stories" dot on the site's globe logo
    try { const old = JSON.parse(localStorage.getItem('pp_globe_seen') || '[]'); const ids = stories.flatMap(st => (st.posts || []).map(p => p.id));
      localStorage.setItem('pp_globe_seen', JSON.stringify([...new Set([...ids, ...old])].slice(0, 1500))); } catch (e) {}
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
    if (d.built_at) $('sub').textContent = `${stories.length} stories · ${ago(d.built_at)}`;
    $('empty').remove();
    if (!stories.length) { $('sub').textContent = 'No trending stories yet — check back soon'; }
    strip(); start();
  }).catch(() => { $('empty').textContent = 'Couldn’t load the stories. Try again in a moment.'; });
})();
