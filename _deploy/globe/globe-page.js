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
    kitCbs = [cb]; const s = document.createElement('script'); s.src = '/globe/birdkit.js?v=1377';
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
      .onGlobeReady(() => { const l = $('glLoad'); l && l.classList.add('gone'); setTimeout(() => l && l.remove(), 400); hiRes(); })
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
    // Esri close-up imagery switched off 2026-11-26 (too much data off Wi-Fi): EOX tiles only.
    try { new PerformanceObserver(list => { for (const e of list.getEntries()) if (e.name.includes('/globe-tile/')) pend = Math.max(0, pend - 1); busy(); }).observe({ type: 'resource', buffered: false }); } catch (e) {}
    // the library hides the whole-Earth image as soon as tiles switch on, which flashed black until they arrived:
    // keep it always showing underneath (a hair smaller, so tiles sit cleanly on top) — same imagery, so no seam
    const keepBase = () => { try { world.scene().traverse(o => { if (o && o.__globeObjType === 'globe' && o.children) { const g = o.children.find(m => m.isMesh); if (g && !g._kept) { g._kept = true; g.scale.setScalar(0.9992); g.renderOrder = -200; Object.defineProperty(g, 'visible', { get: () => true, set: () => {}, configurable: true }); } } }); } catch (e) {} };
    keepBase();
    let tilesOn = false, tuned = false, te = null, lastA = 9, outT = 0;
    const imagery = () => { const a = world.pointOfView().altitude;
      // zooming OUT: stop asking for new tiles (the ones already there stay; the whole-Earth image underneath has the
      // same colours) and resume once the zoom settles — otherwise every in-between level gets fetched and thrown away
      if (te && tilesOn && !document.body.classList.contains('hunting')) { if (a > lastA * 1.004) { te.tileUrl = null; clearTimeout(outT); outT = setTimeout(() => { if (tilesOn) { te.tileUrl = TILE; const v = world.pointOfView(); world.pointOfView({ ...v, altitude: v.altitude + 1e-5 }); } }, 250); } }
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
  // Test (2026-11-26): /globe/#esri uses Esri for the close levels 13-14 (same tile count as EOX), for that visit only.
  const HD_FROM = 13, HD_MAX = 15; let hdOn = /esri/.test(location.hash), tileEng = null, tileSrc = null;
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
      api('/hunt/fly', { brg }).then(x => { flyWait = Math.max(0, flyWait - 1); if (x.s === 200 && x.j.me && on && flyWait === 0) setMe(x.j.me); });
    }
    // the server's copy of a flight starts a moment later than the one the page drew, so swapping to it would make the
    // bird hop a few pixels: the difference is blended away over a third of a second instead
    function setMe(f) {
      const t = srv(), a = me && posAt(me, t), b = posAt(f, t);
      if (a && b && km(a, b) < 1) { const c0 = corrNow(); corr = { la: a[0] - b[0] + c0[0], lo: a[1] - b[1] + c0[1], t0: performance.now() }; }
      me = f;
    }
    const corrNow = () => { if (!corr) return [0, 0]; const k = 1 - (performance.now() - corr.t0) / 350; if (k <= 0) { corr = null; return [0, 0]; } const e = k * k * (3 - 2 * k); return [corr.la * e, corr.lo * e]; };
    // how far the bird is leaning into a turn (−1 left … 1 right): it tips in as the turn starts and levels out after
    const bankAt = (f, t) => { if (!f || f.b0 == null || f.b1 == null) return 0; fTurn(f); const u = (t - f.depart) / 1000, T = f._T;
      return T < 0.05 || u < 0 || u > T ? 0 : f._s * Math.min(1, T * TURN / 0.9); };
    // each bird's wings: flapping keeps its own rhythm; when a turn starts it finishes the beat it's in (until the wings
    // are fully out), then holds them out and leans into the turn smoothly, and picks the beat back up after
    const poses = new Map();
    function pose(id, moving, want, dt) {
      let P = poses.get(id); if (!P) { P = { ph: Math.random() * 6.283, hold: false, bk: 0 }; poses.set(id, P); }
      const rate = moving ? 13 : 4, top = Math.PI / 2, turning = Math.abs(want) > 0.02;
      if (!P.hold) { const before = P.ph; P.ph += dt * rate;
        if (turning && Math.floor((before - top) / 6.2832) !== Math.floor((P.ph - top) / 6.2832)) { P.ph = top + 6.2832 * Math.floor((P.ph - top) / 6.2832); P.hold = true; } }
      else if (!turning && Math.abs(P.bk) < 0.15) P.hold = false;
      P.bk += ((P.hold && turning ? want : 0) - P.bk) * (1 - Math.exp(-dt / 0.14));
      const f = Math.sin(P.ph), span = moving ? 0.55 + 0.45 * (0.5 + 0.5 * f) : 0.9 + 0.1 * (0.5 + 0.5 * f);
      return { span: P.hold ? (moving ? 1 : 1) : span, bk: P.bk };
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
    const ease = (cur, want, dt) => { if (cur == null) return want; let d = want - cur; d = Math.atan2(Math.sin(d), Math.cos(d)); return cur + d * (1 - Math.exp(-dt / 0.07)); };
    const myName = () => { try { return localStorage.getItem('_myUsername') || ''; } catch (e) { return ''; } };
    let on = false, me = null, birds = [], worms = new Map(), off = 0, balance = null, fx = [], target = null, raf = 0, pollT = 0, flySent = 0, flyWait = 0, corr = null, lastF = 0, frameMs = 16.7, zoomIn = null, extAt = 0, ang = -Math.PI / 2, angs = new Map(), asking = new Set(), seenTaken = new Set(), hintUntil = 0;
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
    const cx = cv.getContext('2d'); let W = 0, H = 0, DPR = 1;
    const size = () => { DPR = Math.min(2, devicePixelRatio || 1); W = innerWidth; H = innerHeight; cv.width = W * DPR; cv.height = H * DPR; cv.style.width = W + 'px'; cv.style.height = H + 'px'; };
    size(); addEventListener('resize', size);
    const pill = document.createElement('button'); pill.type = 'button'; pill.className = 'hunt-pill'; pill.innerHTML = `<span class="hf"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.0,5.91Q10.32,6.75 10.11,9.27Q3.6,10.95 0.66,14.31Q6.96,13.47 10.32,14.31L9.48,18.09L12.0,16.83L14.52,18.09L13.68,14.31Q17.04,13.47 23.34,14.31Q20.4,10.95 13.89,9.27Q13.68,6.75 12.0,5.91Z"/></svg></span>Take flight`; document.body.appendChild(pill);
    const bar = document.createElement('div'); bar.className = 'hunt-bar';
    bar.innerHTML = `<span class="hb-n"><span class="hw">${WORM_SVG}</span><b id="huntN">–</b></span><span class="hb-t" id="huntT">Tap to fly</span><button type="button" class="hb-x" aria-label="Land (leave Take flight)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button>`;
    document.body.appendChild(bar);
    for (const el of [pill, bar]) { el.addEventListener('pointerdown', ev => ev.stopPropagation()); }
    pill.addEventListener('click', () => { if (!tok()) { toast('Sign in to take flight', true); return; } enter(); });
    bar.querySelector('.hb-x').addEventListener('click', () => leave());

    // the pill shows only when zoomed in close (and sits just above the story cards)
    const pillCheck = () => { const a = world.pointOfView().altitude, show = !on && a < PILL_ALT && !$('sheet').classList.contains('in');
      if (show) { const st = $('strip'), top = st ? st.getBoundingClientRect().top : H - 120; pill.style.bottom = Math.max(16, H - top + 12) + 'px'; }
      pill.classList.toggle('in', show);
      if (on && a > EXIT_ALT) leave(); };
    world.controls().addEventListener('change', pillCheck); setInterval(pillCheck, 500);

    const col = name => { try { return window._ppKit ? window._ppKit.tagCol(name) : 'hsl(275, 72%, 68%)'; } catch (e) { return 'hsl(275, 72%, 68%)'; } };
    const shade = c => c.replace(/hsl\((\d+),\s*\d+%,\s*\d+%\)/, 'hsl($1, 48%, 42%)');

    function enter() {
      if (on) return; on = true; loadKit(() => {});
      document.body.classList.add('hunting'); pill.classList.remove('in'); bar.classList.add('in');
      try { closeSheet(); focusPin(null); world.arcsData([]); world.ringsData([]); } catch (e) {}
      // the screen stays on your bird, so the map can't be dragged or pinch-zoomed during the hunt (leave with the ×)
      const c = world.controls(); c.autoRotate = false; c.enableRotate = false; c.enableZoom = false;
      const v = world.pointOfView();
      $('huntN').textContent = balance == null ? '–' : balance; hintUntil = Date.now() + 4000;
      poll(true, [v.lat, v.lng]); loop();
    }
    function leave() {
      if (!on) return; on = false; document.body.classList.remove('hunting'); bar.classList.remove('in'); world.controls().enableRotate = true; world.controls().enableZoom = true; try { paint(); } catch (e) {}
      cancelAnimationFrame(raf); clearTimeout(pollT); cx.clearRect(0, 0, cv.width, cv.height); target = null; fx = []; pillCheck();
    }
    async function poll(start, at) {
      clearTimeout(pollT); if (!on) return;
      if (document.hidden) { pollT = setTimeout(() => poll(), 2000); return; }
      const t0 = Date.now(), sent = t0;
      const r = await api('/hunt/state', start ? { start: 1, lat: at[0], lng: at[1] } : {});
      if (!on) return;
      if (r.s === 401) { leave(); toast('Sign in to take flight', true); return; }
      if (r.s === 200 && r.j.now) {
        const t1 = Date.now(); clockSample(r.j.now - (t0 + t1) / 2, t1 - t0);
        if (sent > flySent && !flyWait && r.j.me && (!me || r.j.me.depart >= me.depart - 50)) setMe(r.j.me);   // a flight you just set wins over an older answer
        if (r.j.balance != null) setBal(r.j.balance);
        birds = r.j.birds || [];
        const now = srv(), ids = new Set((r.j.worms || []).map(w => w.id));
        // a worm that vanished early went to another bird: a little puff where it was
        for (const [id, w] of worms) if (!ids.has(id) && w.gone > now + 800 && !w.mine && w.at) fx.push({ k: 'poof', lat: w.at[0], lng: w.at[1], t0: performance.now(), gold: w.v > 1 });
        const next = new Map(); for (const w of r.j.worms || []) next.set(w.id, worms.get(w.id) || { ...w, seen: performance.now() }); worms = next;
        // starting: if your bird is still out somewhere else (you were hunting a moment ago), go to it
        // starting: your bird is already in the air — still flying from a moment ago, or it takes off on its last heading
        if (start && me) {
          if (me.arrive <= now || me.b1 == null) { let b0 = NaN; try { b0 = parseFloat(localStorage.getItem('pp_hunt_brg')); } catch (e) {} flyDir(isFinite(b0) ? b0 : Math.random() * 6.2832); }
          const v0 = world.pointOfView(); zoomIn = { la: v0.lat, lo: v0.lng, a: v0.altitude, t0: performance.now() }; }
      }
      pollT = setTimeout(() => poll(), 2000);
    }
    function setBal(n) { const el = $('huntN'); if (balance != null && n > balance) { el.parentElement.classList.remove('bump'); void el.offsetWidth; el.parentElement.classList.add('bump'); } balance = n; el.textContent = n; }

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
      if (!on || !down || !e.isPrimary) return; const d = down; down = null;
      if (d.n > 1 || Math.hypot(e.clientX - d.x, e.clientY - d.y) > 10 || Date.now() - d.t > 400 || !me) return;
      // tap anywhere: the bird turns and flies that way (and keeps going)
      const r = can.getBoundingClientRect(), g = groundAt(e.clientX - r.left, e.clientY - r.top, r); if (!g) return;
      // a tap right on the bird (within 14 px on screen) has no direction to give, so it's skipped
      const p = posAt(me, srv()), bs = sc(p[0], p[1]); if (bs && Math.hypot(e.clientX - r.left - bs.x, e.clientY - r.top - bs.y) < 14) return;
      flyDir(bearing(p, [g.lat, g.lng])); target = { lat: g.lat, lng: g.lng, t0: performance.now() };
    });

    async function tryCatch(w) {
      if (asking.has(w.id)) return; asking.add(w.id);
      const r = await api('/hunt/catch', { id: w.id });
      if (r.s === 200 && r.j.ok) { w.mine = true; worms.delete(w.id); fx.push({ k: 'catch', lat: w.at ? w.at[0] : w.lat, lng: w.at ? w.at[1] : w.lng, t0: performance.now(), v: r.j.value }); if (r.j.balance != null) setBal(r.j.balance); return; }
      if (r.s === 409) { worms.delete(w.id); if (!seenTaken.has(w.id)) { seenTaken.add(w.id); fx.push({ k: 'poof', lat: w.at ? w.at[0] : w.lat, lng: w.at ? w.at[1] : w.lng, t0: performance.now(), by: r.j.by, gold: w.v > 1 }); } return; }
      if (r.s === 410 || r.s === 404) { worms.delete(w.id); return; }
      setTimeout(() => asking.delete(w.id), 800);   // not close enough on the server's clock yet: try again in a moment
    }

    // ── drawing ──
    // right on the ground: anything drawn even a few km up slides against the map when the camera is this low
    const sc = (la, lo) => world.getScreenCoords(la, lo, 0);
    // a simple bird seen from above in the bird's colour; the beak points where it's going
    function drawBird(x, y, a, name, s, alpha, swoop, ps) {
      const c = cx, cl = col(name), dk = shade(cl), sw = swoop || 0, k = s * 0.8 * (1 - 0.2 * sw), bk = ps.bk, ab = Math.abs(bk), span = ps.span;
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
      const so = (8 - 7 * sw) * s;
      c.save(); c.translate(x + so * 0.4, y + so); c.rotate(a); c.scale(k, k); c.fillStyle = 'rgba(0,0,0,.22)'; shape(); c.fill(); c.restore();
      c.save(); c.translate(x, y); c.rotate(a); c.scale(k, k);
      shape(); c.fillStyle = cl; c.fill();
      // the lowered wing is a little in shadow
      if (ab > 0.05) { c.save(); c.beginPath(); c.rect(-30, bk > 0 ? roll + 5 : -45, 42, 40 + roll * 0); c.clip(); shape(); c.fillStyle = `rgba(0,0,0,${0.12 * ab})`; c.fill(); c.restore(); }
      c.beginPath(); c.moveTo(12, -1.8 + roll); c.lineTo(17, roll); c.lineTo(12, 1.8 + roll); c.closePath(); c.fillStyle = dk; c.fill();   // beak
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
      c.strokeStyle = gold ? '#c084fc' : '#f2a0a4'; c.lineWidth = 2.2; c.stroke();
      c.restore();
    }
    function drawEdge(x, y, gold, t) {
      // a worm off the screen: an arrow on the edge pointing at it
      const m = 26, topY = 80, botY = H - 90;
      const cx0 = W / 2, cy0 = (topY + botY) / 2, dx = x - cx0, dy = y - cy0;
      const sx = (W / 2 - m) / Math.abs(dx || 1e-6), sy = ((botY - topY) / 2) / Math.abs(dy || 1e-6), f = Math.min(sx, sy);
      const ex = cx0 + dx * f, ey = cy0 + dy * f, a = Math.atan2(dy, dx), pulse = 1;
      const c = cx; c.save(); c.translate(ex, ey); c.rotate(a); c.globalAlpha = pulse;
      c.beginPath(); c.moveTo(5, 0); c.lineTo(-3, -4); c.lineTo(-3, 4); c.closePath();
      c.fillStyle = gold ? 'rgba(192,132,252,.85)' : 'rgba(242,160,164,.75)'; c.fill(); c.restore();
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
      const inView = s => s && s.x > -30 && s.x < W + 30 && s.y > 60 && s.y < H - 70;
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
      for (const b of birds) { const q = posAt(b, now); if (!q || !front(q[0], q[1])) continue; const s = sc(q[0], q[1]); if (!inView(s)) continue;
        const moving = now < b.arrive, ahead = posAt(b, now + 250), s2 = ahead && sc(ahead[0], ahead[1]);
        let a = angs.get(b.u) ?? -Math.PI / 2; if (moving && s2 && Math.hypot(s2.x - s.x, s2.y - s.y) > 0.5) a = ease(a, Math.atan2(s2.y - s.y, s2.x - s.x), dt); angs.set(b.u, a);
        drawBird(s.x, s.y, a, b.u, 0.8, 0.92, 0, pose(b.u, moving, bankAt(b, now), dt));
        c.save(); c.font = '600 9.5px -apple-system,system-ui,sans-serif'; c.textAlign = 'center'; c.fillStyle = 'rgba(255,255,255,.75)'; c.shadowColor = 'rgba(0,0,0,.9)'; c.shadowBlur = 3; c.fillText(b.u, s.x, s.y + 26); c.restore(); }
      // effects: catches (your bird dives, the worm is pulled up, +1 / +5 rises) and worms another bird took
      let swoop = 0;
      fx = fx.filter(f => { const age = (performance.now() - f.t0) / 1000, s = sc(f.lat, f.lng); if (!s) return age < 1.4;
        if (f.k === 'catch') {
          if (age < 0.5) swoop = Math.max(swoop, Math.sin(Math.PI * age / 0.5));
          if (age < 0.35) { c.save(); c.globalAlpha = 1 - age / 0.35; c.translate(s.x, s.y - 12 * age / 0.35); c.scale(1 - age / 0.35, 1 - age / 0.35); c.beginPath(); c.moveTo(-5, 0); c.quadraticCurveTo(0, -3, 5, 0); c.strokeStyle = f.v > 1 ? '#c084fc' : '#f2a0a4'; c.lineWidth = 2.2; c.lineCap = 'round'; c.stroke(); c.restore(); }
          c.save(); c.globalAlpha = Math.max(0, 1 - Math.max(0, age - 0.7) / 0.7); c.font = '700 13px -apple-system,system-ui,sans-serif'; c.textAlign = 'center';
          c.fillStyle = f.v > 1 ? '#c084fc' : '#f2a0a4'; c.shadowColor = 'rgba(0,0,0,.8)'; c.shadowBlur = 3; c.fillText('+' + f.v, s.x, s.y - 18 - 16 * age); c.restore();
          return age < 1.4; }
        if (f.k === 'poof') {
          for (let i = 0; i < 5; i++) { const an = i / 5 * 6.283, d = 3 + 10 * age; c.beginPath(); c.arc(s.x + Math.cos(an) * d, s.y + Math.sin(an) * d * 0.6, Math.max(0, 1.6 * (1 - age / 1.2)), 0, 7); c.fillStyle = `rgba(160,120,90,${Math.max(0, 0.8 - age / 1.2)})`; c.fill(); }
          if (f.by) { c.save(); c.globalAlpha = Math.max(0, 1 - age / 1.6); c.font = '600 10.5px -apple-system,system-ui,sans-serif'; c.textAlign = 'center'; c.fillStyle = 'rgba(226,232,240,.85)'; c.shadowColor = 'rgba(0,0,0,.9)'; c.shadowBlur = 4; c.fillText(f.by + ' got it first', s.x, s.y - 18 - 10 * age); c.restore(); }
          return age < 1.6; }
        return false; });
      // your bird, on top of everything
      if (p) { const s = sc(pv[0], pv[1]);
        if (s) { const moving = now < me.arrive, ah = posAt(me, now + 250), s2 = ah && sc(ah[0] + cc[0], ah[1] + cc[1]);
          if (moving && s2 && Math.hypot(s2.x - s.x, s2.y - s.y) > 0.5) ang = ease(ang, Math.atan2(s2.y - s.y, s2.x - s.x), dt);
          else if (!moving) { // sitting still: the beak slowly turns toward the nearest worm
            let best = null, bd = 1e9; for (const w of worms.values()) { if (!w.at) continue; const d = km(p, w.at); if (d < bd) { bd = d; best = w; } }
            const ws = best && sc(best.at[0], best.at[1]);
            if (ws) { const want = Math.atan2(ws.y - s.y, ws.x - s.x); let d = want - ang; d = Math.atan2(Math.sin(d), Math.cos(d)); ang += d * 0.06; } }
          drawBird(s.x, s.y, ang, mine, 1, 1, swoop, pose('@me', moving, bankAt(me, now), dt)); } }
      // the screen moves with your bird (kept in the middle): aim at where it will be when the map is next drawn
      // (on entering it glides from where you were looking down to your bird at hunting height over ~1 s)
      if (p) { const tn = now + frameMs, pn = posAt(me, tn), c2 = corrNow(); let la = pn[0] + c2[0], lo = pn[1] + c2[1], al = null;
        if (zoomIn) { const k = Math.min(1, (performance.now() + frameMs - zoomIn.t0) / 1000), e = 1 - Math.pow(1 - k, 3), dl = ((lo - zoomIn.lo + 540) % 360) - 180;
          la = zoomIn.la + (la - zoomIn.la) * e; lo = zoomIn.lo + dl * e; al = zoomIn.a + (GAME_ALT - zoomIn.a) * e; if (k >= 1) zoomIn = null; }
        world.pointOfView(al == null ? { lat: la, lng: lo } : { lat: la, lng: lo, altitude: al }, 0); }
      if (pf > preAt) { preAt = pf + 400; preload(now); }
      // keep flying: a little before the far-ahead point is reached, carry on the same way
      if (p && me.b1 != null && me.arrive - now < 12000 && performance.now() > extAt) { extAt = performance.now() + 5000; flyDir(headAt(me, now)); }
      // the line under your worm count: day or night where your bird is
      const tEl = $('huntT'); if (tEl) { const hint = Date.now() < hintUntil; if (tEl.classList.contains('on') !== hint) tEl.classList.toggle('on', hint); }
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
