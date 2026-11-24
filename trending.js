// Trending stories for the globe page (user's idea, 2026-11-23).
// Every hour: take the last 24h of news posts, group headlines about the same story (Workers AI embeddings,
// compared only when two headlines share a rarer word), and score each group by how many different outlets and
// countries cover it, plus activity on Perch Posts (flaps, chirps, shares, worms). The top stories are saved
// in globe_cache so the globe page opens instantly.
import { OUTLETS, COUNTRY_LL, BIG_COUNTRIES } from "./globe-data.js";

const STOP = new Set(("about after again against amid among also around back because been before being between both " +
  "could down during each every first from further have having here into just last latest like live made make many " +
  "more most much must near news next only other over own said same says should since some such than that their them " +
  "then there these they this those three through time today under until updates update very week what when where " +
  "which while will with would year years your report reports new two one four five call calls set sets get gets " +
  "says amp video watch photos year's world people city state government police").split(/\s+/));

function attachOf(content) {
  const m = String(content || "").match(/\[ATTACH:(\{.*\})\]/s);
  if (!m) return null;
  try { return JSON.parse(m[1]); } catch { return null; }
}
function hostOf(u) { try { return new URL(u).hostname.toLowerCase().replace(/^www\./, ""); } catch { return ""; } }
export function outletOf(url, country) {
  let h = hostOf(url);
  while (h) {
    const o = OUTLETS[`${h}|${country}`] || OUTLETS[h];
    if (o) return { name: o[0], city: o[1], lat: o[2], lng: o[3] };
    const i = h.indexOf(".");
    if (i < 0 || h.indexOf(".", i + 1) < 0) break;
    h = h.slice(i + 1);
  }
  const c = COUNTRY_LL[country];
  const host = hostOf(url);
  return c ? { name: host, city: country, lat: c[0], lng: c[1] } : null;
}
const words = t => [...new Set(String(t || "").toLowerCase().replace(/[’']/g, "").split(/[^\p{L}\p{N}]+/u).filter(w => w.length >= 4 && !STOP.has(w) && !/^\d+$/.test(w)))];
function norm(v) { let s = 0; for (const x of v) s += x * x; s = Math.sqrt(s) || 1; return v.map(x => x / s); }
function dot(a, b) { let s = 0; for (let i = 0; i < a.length; i++) s += a[i] * b[i]; return s; }

// ── Where a story happened (user's choice 2026-11-23): 1) ask the AI, accepted only when the place it names is in the
// headlines and its point is inside that country; 2) else the country most named across the headlines; 3) else the
// first outlet to report it.
const ALIAS = {
  "United States": ["American", "Americans", "U.S.", "US", "USA", "Washington", "White House", "Pentagon", "New York", "California", "Texas", "Florida"],
  "United Kingdom": ["British", "Britain", "UK", "U.K.", "England", "English", "Scotland", "Scottish", "Wales", "Welsh", "London", "Manchester", "Liverpool"],
  "Russia": ["Russian", "Russians", "Kremlin", "Moscow"], "Ukraine": ["Ukrainian", "Ukrainians", "Kyiv", "Kharkiv", "Odesa"],
  "China": ["Chinese", "Beijing", "Shanghai"], "India": ["Indian", "Delhi", "Mumbai"], "Israel": ["Israeli", "Israelis", "Tel Aviv"],
  "Palestine": ["Palestinian", "Palestinians", "Gaza", "West Bank"], "Iran": ["Iranian", "Tehran"], "Libya": ["Libyan", "Benghazi", "Tripoli"],
  "Indonesia": ["Indonesian", "Jakarta"], "Japan": ["Japanese", "Tokyo"], "France": ["French", "Paris"], "Germany": ["German", "Berlin"],
  "Italy": ["Italian", "Rome", "Milan"], "Spain": ["Spanish", "Madrid", "Barcelona"], "Turkey": ["Turkish", "Türkiye", "Istanbul", "Ankara", "Antalya"],
  "Syria": ["Syrian", "Damascus"], "Lebanon": ["Lebanese", "Beirut"], "Egypt": ["Egyptian", "Cairo"], "Saudi Arabia": ["Saudi", "Riyadh"],
  "Pakistan": ["Pakistani", "Islamabad", "Karachi"], "Afghanistan": ["Afghan", "Kabul"], "Brazil": ["Brazilian", "Rio de Janeiro", "Sao Paulo", "São Paulo"],
  "Mexico": ["Mexican"], "Canada": ["Canadian", "Ottawa", "Toronto"], "Australia": ["Australian", "Sydney", "Melbourne"], "Nigeria": ["Nigerian", "Lagos", "Abuja"],
  "South Africa": ["South African", "Johannesburg", "Cape Town"], "Kenya": ["Kenyan", "Nairobi"], "Sudan": ["Sudanese", "Khartoum"],
  "North Korea": ["North Korean", "Pyongyang"], "South Korea": ["South Korean", "Seoul"], "Taiwan": ["Taiwanese", "Taipei"], "Venezuela": ["Venezuelan", "Caracas"],
  "Philippines": ["Filipino", "Manila"], "Thailand": ["Thai", "Bangkok"], "Vietnam": ["Vietnamese", "Hanoi"], "Poland": ["Polish", "Warsaw"],
  "Greece": ["Greek", "Athens"], "Ireland": ["Irish", "Dublin"], "Netherlands": ["Dutch", "Amsterdam"], "Senegal": ["Senegalese"], "Morocco": ["Moroccan"],
  "Ethiopia": ["Ethiopian"], "Yemen": ["Yemeni", "Houthi", "Houthis"], "Iraq": ["Iraqi", "Baghdad"], "Qatar": ["Qatari", "Doha"],
  "United Arab Emirates": ["UAE", "Emirati", "Dubai", "Abu Dhabi"], "Bangladesh": ["Bangladeshi", "Dhaka"], "Argentina": ["Argentine", "Argentinian", "Buenos Aires"],
  "Colombia": ["Colombian", "Bogota", "Bogotá"], "Cuba": ["Cuban", "Havana"], "Haiti": ["Haitian"], "Myanmar": ["Burmese"], "Sri Lanka": ["Sri Lankan", "Colombo"],
};
const NAME_FIX = { "usa": "United States", "united states of america": "United States", "us": "United States", "uk": "United Kingdom", "great britain": "United Kingdom",
  "britain": "United Kingdom", "england": "United Kingdom", "scotland": "United Kingdom", "wales": "United Kingdom", "türkiye": "Turkey", "turkiye": "Turkey",
  "democratic republic of the congo": "DR Congo", "drc": "DR Congo", "czechia": "Czech Republic", "gaza": "Palestine", "gaza strip": "Palestine",
  "west bank": "Palestine", "palestinian territories": "Palestine", "uae": "United Arab Emirates", "republic of korea": "South Korea", "korea": "South Korea" };
const COUNTRIES = Object.keys(COUNTRY_LL);
// When only the country is known, big countries use their middle rather than the capital/biggest city
const MIDDLE = { "United States": [39.5, -98.4], "Canada": [56.0, -100.0], "Russia": [61.0, 96.0], "China": [34.5, 104.0], "Brazil": [-10.5, -51.9],
  "Australia": [-25.3, 134.0], "India": [22.5, 79.0], "Argentina": [-35.0, -64.5], "Mexico": [23.6, -102.5], "Kazakhstan": [48.0, 67.0],
  "Saudi Arabia": [24.0, 45.0], "Libya": [27.0, 17.5], "Algeria": [28.0, 2.6], "DR Congo": [-2.9, 23.6], "Sudan": [15.5, 30.0], "Iran": [32.4, 53.7] };
const countryPoint = c => MIDDLE[c] || COUNTRY_LL[c];
const reEsc = x => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const wordRe = new Map();
function hasWord(text, w) {
  if (!wordRe.has(w)) wordRe.set(w, new RegExp(`(?<![\\p{L}\\p{N}])${reEsc(w)}(?![\\p{L}\\p{N}])`, /^[A-Z.]{2,4}$/.test(w) ? "u" : "iu"));
  return wordRe.get(w).test(text);
}
const termsOf = c => [c, ...(ALIAS[c] || [])];
function fixCountry(c) {
  if (!c) return null;
  const k = String(c).trim().toLowerCase();
  return NAME_FIX[k] || COUNTRIES.find(x => x.toLowerCase() === k) || null;
}
function km(a, b, c, d) { const R = Math.PI / 180, x = Math.sin((c - a) * R / 2) ** 2 + Math.cos(a * R) * Math.cos(c * R) * Math.sin((d - b) * R / 2) ** 2; return 12742 * Math.asin(Math.sqrt(x)); }
async function storyPlace(env, items) {
  const texts = items.map(x => `${x.title} ${x.desc}`);
  const all = texts.join("  ");
  // Count which country the headlines name most (an outlet naming its own country counts half)
  const score = new Map();
  for (let i = 0; i < items.length; i++) for (const c of COUNTRIES) {
    if (termsOf(c).some(t => hasWord(texts[i], t))) score.set(c, (score.get(c) || 0) + (items[i].country === c ? 0.5 : 1));
  }
  const top = [...score.entries()].sort((a, b) => b[1] - a[1]);
  const strong = top.length && top[0][1] >= 2 && top[0][1] >= items.length * 0.35 && (!top[1] || top[0][1] >= top[1][1] * 1.3) ? top[0][0] : null;
  // 1) AI
  try {
    const lines = items.slice(0, 14).map(x => `- ${x.title}${x.desc ? " — " + x.desc.slice(0, 160) : ""}`).join("\n");
    const out = await env.AI.run("@cf/meta/llama-3.3-70b-instruct-fp8-fast", { max_tokens: 90, temperature: 0, messages: [
      { role: "system", content: "You find where a news event physically took place. Reply with JSON only, no other text: {\"city\": string or null, \"country\": string or null, \"lat\": number or null, \"lng\": number or null}. Use where the event happened, not where the reporters are. For news about one company (its boss, its results, its decisions), use the city of that company's headquarters. If there is no single physical place (online, worldwide policy, a person's statement), reply {\"city\": null, \"country\": null, \"lat\": null, \"lng\": null}." },
      { role: "user", content: `Headlines from different outlets about one story:\n${lines}` } ] });
    // some models hand back the JSON already parsed, others as text
    const res = out?.response;
    let j = res && typeof res === "object" ? res : null;
    if (!j) { const m = String(res || "").match(/\{[\s\S]*?\}/); j = m ? JSON.parse(m[0]) : null; }
    const country = fixCountry(j && j.country);
    if (country) {
      const city = j.city && String(j.city).trim().slice(0, 60) || null;
      // only places the headlines name, or (when they don't clearly point anywhere) a place the AI knows, like a venue
      const named = (city && hasWord(all, city)) || termsOf(country).some(t => hasWord(all, t));
      if (named || !strong) {
        const ref = COUNTRY_LL[country], lat = +j.lat, lng = +j.lng;
        const ok = city && isFinite(lat) && isFinite(lng) && Math.abs(lat) <= 90 && Math.abs(lng) <= 180 && km(lat, lng, ref[0], ref[1]) <= (BIG_COUNTRIES[country] || 700);
        const mid = countryPoint(country);
        return ok ? { name: `${city}, ${country}`, city, country, lat, lng, how: "ai" } : { name: country, city: null, country, lat: mid[0], lng: mid[1], how: "ai" };
      }
    }
  } catch (e) { console.error("storyPlace AI", e.message); }
  // 2) the country the headlines clearly point to
  if (strong) { const ref = countryPoint(strong); return { name: strong, city: null, country: strong, lat: ref[0], lng: ref[1], how: "names" }; }
  // 2b) no clear winner: the most-named country anyway, if the headlines name one at least twice
  if (top.length && top[0][1] >= 2) { const c = top[0][0], ref = countryPoint(c); return { name: c, city: null, country: c, lat: ref[0], lng: ref[1], how: "names" }; }
  // 3) where it was first reported
  const first = items.reduce((a, x) => (x.t < a.t ? x : a), items[0]);
  return { name: `${first.city}, ${first.country}`, city: first.city, country: first.country, lat: first.lat, lng: first.lng, how: "first", outlet: first.outlet };
}

export async function buildTrending(env, { dry = false, threshold = 0.8, merge = 0.85 } = {}) {
  const since = new Date(Date.now() - 24 * 3600e3).toISOString();
  const { results: rows = [] } = await env.DB.prepare(
    `SELECT id, content, country, created_at, share_count FROM posts INDEXED BY idx_posts_created_at
     WHERE created_at >= ? AND deleted = 0 AND (archived = 0 OR archived IS NULL) AND browser_id LIKE 'bot-%' ORDER BY created_at ASC LIMIT 4000`
  ).bind(since).all();
  const items = [];
  for (const r of rows) {
    const a = attachOf(r.content);
    if (!a || !a.title || !a.url) continue;
    const o = outletOf(a.url, r.country);
    if (!o) continue;
    items.push({ id: r.id, title: String(a.title).slice(0, 220), desc: String(a.description || "").slice(0, 200), url: a.url, image: a.image || null,
      country: r.country, t: r.created_at, shares: r.share_count || 0, outlet: o.name, city: o.city, lat: o.lat, lng: o.lng, w: words(a.title) });
  }
  if (items.length < 5) return { stories: [], items: items.length };
  // Embeddings, 100 headlines per call
  for (let i = 0; i < items.length; i += 100) {
    const batch = items.slice(i, i + 100);
    const out = await env.AI.run("@cf/baai/bge-small-en-v1.5", { text: batch.map(x => `${x.title}. ${x.desc}`.slice(0, 400)) });
    (out?.data || []).forEach((v, j) => { batch[j].v = norm(v); });
  }
  // Words used by too many headlines don't help find the same story
  const df = new Map();
  for (const x of items) for (const w of x.w) df.set(w, (df.get(w) || 0) + 1);
  const maxDf = Math.max(25, items.length * 0.03);
  const clusters = [], index = new Map();
  for (const x of items) {
    if (!x.v) continue;
    const keys = x.w.filter(w => df.get(w) <= maxDf);
    const cand = new Set();
    for (const w of keys) for (const ci of index.get(w) || []) cand.add(ci);
    let best = -1, bestS = threshold;
    for (const ci of cand) { const s = dot(x.v, clusters[ci].c); if (s >= bestS) { bestS = s; best = ci; } }
    if (best < 0) { best = clusters.length; clusters.push({ items: [], sum: new Array(x.v.length).fill(0), c: x.v }); }
    const cl = clusters[best];
    cl.items.push(x);
    for (let k = 0; k < x.v.length; k++) cl.sum[k] += x.v[k];
    cl.c = norm(cl.sum);
    for (const w of keys) { if (!index.has(w)) index.set(w, new Set()); index.get(w).add(best); }
  }
  // Second pass: groups that are the same event from different angles (e.g. "Huang returns as CEO" and "Wall Street
  // jumps as Huang returns") merge when their averaged headlines are close AND they share a rarer word.
  const merged = [];
  {
    const big = clusters.filter(cl => cl.items.length >= 2).sort((a, b) => b.items.length - a.items.length);
    const wordsOf = cl => new Set(cl.items.flatMap(x => x.w.filter(w => df.get(w) <= maxDf)));
    for (const cl of big) cl.ws = wordsOf(cl);
    for (let i = 0; i < big.length; i++) {
      const a = big[i]; if (a.gone) continue;
      for (let j = i + 1; j < big.length; j++) {
        const b = big[j]; if (b.gone) continue;
        if (dot(a.c, b.c) < merge) continue;
        let shared = 0; for (const w of b.ws) if (a.ws.has(w)) { shared++; if (shared >= 2) break; }
        if (shared < 2) continue;
        merged.push(`${a.items[0].title.slice(0, 50)}  <=  ${b.items[0].title.slice(0, 50)} (${dot(a.c, b.c).toFixed(2)})`);
        a.items.push(...b.items); for (let k = 0; k < a.sum.length; k++) a.sum[k] += b.sum[k]; a.c = norm(a.sum);
        for (const w of b.ws) a.ws.add(w); b.gone = true;
      }
    }
  }
  // Groups covered by 2+ outlets, then activity on the site
  let groups = clusters.filter(cl => !cl.gone).map(cl => ({ ...cl, outlets: new Set(cl.items.map(x => x.outlet)), countries: new Set(cl.items.map(x => x.country)) }))
    .filter(g => g.outlets.size >= 2);
  const ids = groups.flatMap(g => g.items.map(x => x.id));
  const eng = new Map();
  for (let i = 0; i < ids.length; i += 90) {
    const chunk = JSON.stringify(ids.slice(i, i + 90));
    const [c, v, w] = await Promise.all([
      env.DB.prepare(`SELECT post_id, COUNT(*) AS n FROM comments WHERE post_id IN (SELECT value FROM json_each(?)) AND deleted = 0 GROUP BY post_id`).bind(chunk).all(),
      env.DB.prepare(`SELECT post_id, COUNT(*) AS n FROM post_votes WHERE value > 0 AND post_id IN (SELECT value FROM json_each(?)) GROUP BY post_id`).bind(chunk).all(),
      env.DB.prepare(`SELECT post_id, COUNT(*) AS n FROM worms WHERE post_id IN (SELECT value FROM json_each(?)) GROUP BY post_id`).bind(chunk).all().catch(() => ({ results: [] })),
    ]);
    for (const r of c.results || []) eng.set(r.post_id, (eng.get(r.post_id) || 0) + 2 * r.n);
    for (const r of v.results || []) eng.set(r.post_id, (eng.get(r.post_id) || 0) + r.n);
    for (const r of w.results || []) eng.set(r.post_id, (eng.get(r.post_id) || 0) + 3 * r.n);
  }
  for (const g of groups) {
    g.eng = g.items.reduce((a, x) => a + (eng.get(x.id) || 0) + 2 * x.shares, 0);
    g.score = g.outlets.size + 1.5 * g.countries.size + 1.5 * Math.log2(1 + g.eng);
  }
  groups.sort((a, b) => b.score - a.score);
  const top = groups.slice(0, 12);
  const places = await Promise.all(top.map(g => storyPlace(env, g.items)));
  const stories = top.map((g, i) => {
    const rep = g.items.reduce((a, x) => (dot(x.v, g.c) > dot(a.v, g.c) ? x : a), g.items[0]);
    const seen = new Set(), posts = [];
    for (const x of [rep, ...g.items]) {
      if (seen.has(x.outlet)) continue;
      seen.add(x.outlet);
      posts.push({ id: x.id, title: x.title, desc: x.desc || null, url: x.url, image: x.image, outlet: x.outlet, country: x.country, city: x.city, lat: x.lat, lng: x.lng, t: x.t });
      if (posts.length >= 30) break;
    }
    return { rank: i + 1, title: rep.title, image: rep.image || (g.items.find(x => x.image) || {}).image || null,
      outlets: g.outlets.size, countries: g.countries.size, activity: g.eng, origin: places[i], posts };
  });
  const doc = { built_at: new Date().toISOString(), window_hours: 24, stories };
  if (!dry) await env.DB.prepare(`INSERT INTO globe_cache (k, v, at) VALUES ('trending', ?, ?) ON CONFLICT(k) DO UPDATE SET v = excluded.v, at = excluded.at`)
    .bind(JSON.stringify(doc), doc.built_at).run();
  return { ...doc, items: items.length, clusters: clusters.length, multi: groups.length, merged };
}
