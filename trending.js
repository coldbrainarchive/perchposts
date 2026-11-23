// Trending stories for the globe page (user's idea, 2026-11-23).
// Every hour: take the last 24h of news posts, group headlines about the same story (Workers AI embeddings,
// compared only when two headlines share a rarer word), and score each group by how many different outlets and
// countries cover it, plus activity on Perch Posts (flaps, chirps, shares, worms). The top stories are saved
// in globe_cache so the globe page opens instantly.
import { OUTLETS, COUNTRY_LL } from "./globe-data.js";

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

export async function buildTrending(env, { dry = false, threshold = 0.8 } = {}) {
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
  // Groups covered by 2+ outlets, then activity on the site
  let groups = clusters.map(cl => ({ ...cl, outlets: new Set(cl.items.map(x => x.outlet)), countries: new Set(cl.items.map(x => x.country)) }))
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
  const stories = groups.slice(0, 12).map((g, i) => {
    const rep = g.items.reduce((a, x) => (dot(x.v, g.c) > dot(a.v, g.c) ? x : a), g.items[0]);
    const seen = new Set(), posts = [];
    for (const x of [rep, ...g.items]) {
      if (seen.has(x.outlet)) continue;
      seen.add(x.outlet);
      posts.push({ id: x.id, title: x.title, url: x.url, image: x.image, outlet: x.outlet, country: x.country, city: x.city, lat: x.lat, lng: x.lng, t: x.t });
      if (posts.length >= 14) break;
    }
    return { rank: i + 1, title: rep.title, image: rep.image || (g.items.find(x => x.image) || {}).image || null,
      outlets: g.outlets.size, countries: g.countries.size, activity: g.eng, posts };
  });
  const doc = { built_at: new Date().toISOString(), window_hours: 24, stories };
  if (!dry) await env.DB.prepare(`INSERT INTO globe_cache (k, v, at) VALUES ('trending', ?, ?) ON CONFLICT(k) DO UPDATE SET v = excluded.v, at = excluded.at`)
    .bind(JSON.stringify(doc), doc.built_at).run();
  return { ...doc, items: items.length, clusters: clusters.length, multi: groups.length };
}
