// Builds link previews (title, description, picture) on our own server, replacing microlink.io, so nobody
// outside perchposts learns who is sharing which link (the linked site only sees Cloudflare).
//
//   linkPreview(url, fetch?, { addressFallback = true }) -> { url, title, description, image } | null
//
// How: YouTube, X/Twitter, TikTok and Spotify answer through their official oEmbed endpoints (their pages
// don't give previews to unknown visitors); everything else is read from the page's own preview tags
// (Open Graph / Twitter card / <title> / meta description), which sites publish for exactly this purpose.

// Our own name, plus the "facebookexternalhit" token that many sites look for before handing out preview tags.
const BOT_UA = "Mozilla/5.0 (compatible; PerchpostsBot/1.0; +https://perchposts.com) facebookexternalhit/1.1";
const BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15";
const MAX_BYTES = 1_500_000, TIMEOUT_MS = 6000, MAX_REDIRECTS = 5;

export async function linkPreview(raw, fetchImpl = fetch, opts = {}) {
  const addressFallback = opts.addressFallback !== false; // the news bots turn this off
  const timeout = opts.timeoutMs || TIMEOUT_MS;               // the news bots can wait longer than someone typing
  let u = normalize(raw);
  if (!u) return null;
  try {
    const special = await viaOEmbed(u, fetchImpl, timeout);
    if (special) return special;
  } catch (e) { /* fall through to the page */ }
  // Ask as our preview bot and as an ordinary browser at the same time; keep the fuller answer.
  // BBC always refuses Cloudflare's servers, so go straight to its news feeds.
  if (/(^|\.)bbc\.(co\.uk|com)$/.test(u.hostname)) {
    return (await bbcFromFeeds(u, fetchImpl).catch(() => null)) || (addressFallback ? fromAddress(u) : null);
  }
  // Answers as soon as either gives a complete preview, otherwise when both have finished.
  const score = p => (p ? (p.title && !generic(p) ? 2 : p.title ? 1 : 0) + (p.description ? 1 : 0) + (p.image ? 2 : 0) : -1);
  const results = await new Promise(resolve => {
    const got = [null, null]; let left = 2;
    [BOT_UA, BROWSER_UA].forEach((ua, i) => fromPage(u, ua, fetchImpl, timeout).catch(() => null).then(p => {
      got[i] = p; left--;
      if (score(p) >= 5 || !left) resolve(got.slice());
    }));
  });
  const [a, b] = results;
  let best = score(b) > score(a) ? mergePreview(b, a) : mergePreview(a, b);
  // Sites behind Cloudflare's bot protection refuse requests from Cloudflare's own servers (BBC, FT, …).
  if (!best || !best.title) {
    if (/(^|\.)bbc\.(co\.uk|com)$/.test(u.hostname)) { const f = await bbcFromFeeds(u, fetchImpl).catch(() => null); if (f) return f; }
    const s = addressFallback ? fromAddress(u) : null;
    if (s) return s;
  }
  if (best && /(^|\.)tiktok\.com$/.test(u.hostname) && generic(best)) {
    const who = /^\/@([^/]+)/.exec(u.pathname);
    best = { ...best, title: who ? `@${who[1]} on TikTok` : "TikTok video", description: "TikTok" };
  }
  return best && (best.title || best.image) ? best : null;
}

function normalize(raw) {
  let s = String(raw || "").trim();
  if (!s) return null;
  if (!/^https?:\/\//i.test(s)) s = "https://" + s;
  let u;
  try { u = new URL(s); } catch { return null; }
  if (!safeUrl(u)) return null;
  u.hash = "";
  return u;
}

// No private / local / odd addresses (the worker can't reach private networks anyway, but be strict).
function safeUrl(u) {
  if (u.protocol !== "https:" && u.protocol !== "http:") return false;
  if (u.username || u.password) return false;
  if (u.port && u.port !== "80" && u.port !== "443") return false;
  const h = u.hostname.toLowerCase().replace(/\.$/, "");
  if (!h.includes(".") || h === "localhost" || /\.(local|internal|localhost|lan|home|arpa)$/.test(h)) return false;
  if (/(^|\.)workers\.dev$/.test(h) && h.startsWith("daboysforumip")) return false;
  if (/^\d+\.\d+\.\d+\.\d+$/.test(h)) {
    const [a, b] = h.split(".").map(Number);
    if (a === 10 || a === 127 || a === 0 || (a === 169 && b === 254) || (a === 172 && b >= 16 && b <= 31) || (a === 192 && b === 168) || (a === 100 && b >= 64 && b <= 127) || a >= 224) return false;
  }
  if (h.includes(":") || h.startsWith("[")) return false; // IPv6 literals: not needed for previews
  return true;
}

// ── Sites that only preview through oEmbed ──────────────────────────────────
async function viaOEmbed(u, fetchImpl, timeout = TIMEOUT_MS) {
  const h = u.hostname.replace(/^www\.|^m\./, "");
  const getJson = async (endpoint) => {
    const r = await fetchImpl(endpoint, { headers: { "User-Agent": BOT_UA, Accept: "application/json" }, signal: AbortSignal.timeout(timeout) });
    return r.ok ? r.json() : null;
  };
  if (h === "youtube.com" || h === "youtu.be" || h === "music.youtube.com") {
    const id = youtubeId(u);
    if (!id) return null;
    const j = await getJson(`https://www.youtube.com/oembed?format=json&url=${encodeURIComponent(`https://www.youtube.com/watch?v=${id}`)}`);
    if (!j?.title) return null;
    return { url: `https://www.youtube.com/watch?v=${id}`, title: j.title, description: j.author_name ? `${j.author_name} · YouTube` : "YouTube", image: `https://i.ytimg.com/vi/${id}/hqdefault.jpg` };
  }
  if (h === "x.com" || h === "twitter.com" || h === "mobile.twitter.com" || h === "fxtwitter.com" || h === "vxtwitter.com") {
    // X no longer offers oEmbed; fxtwitter is an open tweet-preview service. Only the tweet's address goes to it.
    const m = /^\/([A-Za-z0-9_]{1,15})\/status(?:es)?\/(\d+)/.exec(u.pathname);
    if (!m) return null;
    const j = await getJson(`https://api.fxtwitter.com/${m[1]}/status/${m[2]}`);
    const t = j?.tweet;
    if (!t) return null;
    const media = t.media?.photos?.[0]?.url || t.media?.videos?.[0]?.thumbnail_url || t.media?.all?.[0]?.thumbnail_url || t.media?.all?.[0]?.url || null;
    const who = t.author ? `${t.author.name} (@${t.author.screen_name})` : "Post";
    return { url: `https://x.com/${t.author?.screen_name || m[1]}/status/${m[2]}`, title: `${who} on X`, description: t.text ? clip(t.text.replace(/\s+/g, " ").trim(), 600) : null, image: media || t.author?.avatar_url || null };
  }
  if (h === "tiktok.com" || h === "vm.tiktok.com") {
    const j = await getJson(`https://www.tiktok.com/oembed?url=${encodeURIComponent(u.href)}`);
    if (!j?.title && !j?.thumbnail_url) return null;
    return { url: u.href, title: j.title || (j.author_name ? `${j.author_name} on TikTok` : "TikTok"), description: j.author_name ? `${j.author_name} · TikTok` : "TikTok", image: j.thumbnail_url || null };
  }
  if (h === "open.spotify.com") {
    const j = await getJson(`https://open.spotify.com/oembed?url=${encodeURIComponent(u.href)}`);
    if (!j?.title) return null;
    return { url: u.href, title: j.title, description: "Spotify", image: j.thumbnail_url || null };
  }
  return null;
}
function youtubeId(u) {
  const h = u.hostname.replace(/^www\.|^m\./, "");
  if (h === "youtu.be") return u.pathname.slice(1).split("/")[0] || null;
  if (u.searchParams.get("v")) return u.searchParams.get("v");
  const m = /^\/(shorts|embed|live|v)\/([A-Za-z0-9_-]{6,})/.exec(u.pathname);
  return m ? m[2] : null;
}

// ── Everything else: the page's own preview tags ────────────────────────────
async function fromPage(start, ua, fetchImpl, timeout = TIMEOUT_MS) {
  let u = start, res;
  for (let hop = 0; hop <= MAX_REDIRECTS; hop++) {
    res = await fetchImpl(u.href, {
      redirect: "manual",
      headers: { "User-Agent": ua, Accept: "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5", "Accept-Language": "en-IE,en;q=0.9" },
      signal: AbortSignal.timeout(timeout),
    });
    if (res.status >= 300 && res.status < 400 && res.headers.get("location")) {
      const next = new URL(res.headers.get("location"), u);
      if (!safeUrl(next)) return null;
      try { res.body?.cancel(); } catch {}
      u = next;
      continue;
    }
    break;
  }
  if (!res || !res.ok) { try { res?.body?.cancel(); } catch {} return null; }
  const type = (res.headers.get("content-type") || "").toLowerCase();
  if (type.startsWith("image/")) { try { res.body?.cancel(); } catch {} return { url: u.href, title: null, description: null, image: u.href }; }
  if (!type.includes("html")) { try { res.body?.cancel(); } catch {} return null; }
  const html = await readHead(res);
  return parse(html, u);
}

// Read until </head> (where preview tags live) or MAX_BYTES, whichever comes first.
async function readHead(res) {
  const reader = res.body.getReader(), dec = new TextDecoder();
  let html = "", n = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    n += value.length; html += dec.decode(value, { stream: true });
    if (/<\/head\s*>/i.test(html) || n > MAX_BYTES) { try { await reader.cancel(); } catch {} break; }
  }
  return html;
}

function parse(html, base) {
  const metas = {};
  for (const tag of html.match(/<meta\b[^>]*>/gi) || []) {
    const attr = name => { const m = new RegExp(`\\b${name}\\s*=\\s*("([^"]*)"|'([^']*)'|([^\\s"'>]+))`, "i").exec(tag); return m ? (m[2] ?? m[3] ?? m[4] ?? "") : null; };
    const key = (attr("property") || attr("name") || attr("itemprop") || "").toLowerCase().trim();
    const val = attr("content");
    if (key && val != null && !(key in metas)) metas[key] = decode(val).trim();
  }
  const pick = (...ks) => { for (const k of ks) if (metas[k]) return metas[k]; return null; };
  const titleTag = (() => { const m = /<title[^>]*>([\s\S]*?)<\/title>/i.exec(html); return m ? decode(m[1]).replace(/\s+/g, " ").trim() : null; })();
  const title = pick("og:title", "twitter:title", "title") || titleTag || null;
  const description = pick("og:description", "twitter:description", "description") || null;
  let image = pick("og:image:secure_url", "og:image", "og:image:url", "twitter:image", "twitter:image:src", "image", "thumbnailurl");
  if (!image) { const m = /<link\b[^>]*rel=["']image_src["'][^>]*>/i.exec(html); const h = m && /href=["']([^"']+)["']/i.exec(m[0]); if (h) image = decode(h[1]); }
  let url = pick("og:url") || base.href;
  try { if (image) image = new URL(image, base).href; } catch { image = null; }
  try { url = new URL(url, base).href; } catch { url = base.href; }
  if (image && !/^https?:/i.test(image)) image = null;
  return { url, title: clip(title, 300), description: clip(description, 600), image };
}

// BBC articles: look the link up in BBC's own news feeds (title, summary, picture), remembered for 5 minutes.
const BBC_FEEDS = ["news", "news/world", "news/uk", "news/england", "news/northern_ireland", "news/scotland", "news/wales", "news/business",
  "news/politics", "news/health", "news/education", "news/science_and_environment", "news/technology", "news/entertainment_and_arts",
  "news/world/europe", "news/world/us_and_canada", "sport", "sport/football"].map(p => `https://feeds.bbci.co.uk/${p}/rss.xml`);
let bbcCache = { at: 0, items: [] };
async function bbcFromFeeds(u, fetchImpl) {
  const id = (u.pathname.match(/([a-z0-9]{8,}|\d{6,})\/?$/i) || [])[1];
  if (!id) return null;
  if (Date.now() - bbcCache.at > 5 * 60 * 1000) {
    const texts = await Promise.all(BBC_FEEDS.map(f => fetchImpl(f, { headers: { "User-Agent": BOT_UA }, signal: AbortSignal.timeout(TIMEOUT_MS) }).then(r => (r.ok ? r.text() : "")).catch(() => "")));
    const items = [];
    for (const xml of texts) for (const it of xml.match(/<item>[\s\S]*?<\/item>/g) || []) {
      const tag = n => { const m = new RegExp(`<${n}[^>]*>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\/${n}>`).exec(it); return m ? decode(m[1]).trim() : null; };
      const thumb = /<media:thumbnail[^>]*url="([^"]+)"/.exec(it);
      items.push({ link: tag("link") || "", title: tag("title"), description: tag("description"), image: thumb ? thumb[1].replace(/\/standard\/\d+\//, "/standard/976/").replace(/\/ace\/standard\/\d+\//, "/ace/standard/976/") : null });
    }
    if (items.length) bbcCache = { at: Date.now(), items };
  }
  const hit = bbcCache.items.find(i => i.link.split("?")[0].replace(/\/$/, "").endsWith(id));
  return hit && hit.title ? { url: u.href, title: hit.title, description: hit.description, image: hit.image } : null;
}

// Last resort for sites that won't talk to us: a readable title from the address itself (no picture).
function fromAddress(u) {
  const segs = u.pathname.split("/").filter(Boolean).map(s => decodeURIComponent(s).replace(/\.(html?|php|aspx?|ece)$/i, ""));
  const slug = segs.reverse().find(s => /[a-z]-[a-z]/i.test(s) && (s.match(/[a-z]+/gi) || []).length >= 3 && !/^[0-9a-f-]{20,}$/i.test(s));
  if (!slug) return null;
  const words = slug.replace(/[-_+]+/g, " ").replace(/\b\d{5,}\b/g, "").replace(/\s+/g, " ").trim();
  if (words.length < 12) return null;
  const site = u.hostname.replace(/^www\./, "");
  return { url: u.href, title: words.charAt(0).toUpperCase() + words.slice(1), description: site, image: null };
}

// Pages some sites give to every visitor ("Visit TikTok…", a bare site name) aren't worth preferring.
function generic(p) { return !p.title || /^(instagram|tiktok|reddit|amazon(\.com)?|x|twitter)$/i.test(p.title.trim()) || /^visit tiktok/i.test(p.title); }

function mergePreview(a, b) {
  if (!a) return b;
  if (!b) return a;
  return { url: a.url || b.url, title: a.title || b.title, description: a.description || b.description, image: a.image || b.image };
}
const clip = (s, n) => (s && s.length > n ? s.slice(0, n - 1).trimEnd() + "…" : s);

const NAMED = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", ndash: "–", mdash: "—", hellip: "…", lsquo: "‘", rsquo: "’", ldquo: "“", rdquo: "”", eacute: "é", egrave: "è", aacute: "á", agrave: "à", ouml: "ö", uuml: "ü", auml: "ä", ccedil: "ç", ntilde: "ñ", oacute: "ó", iacute: "í", uacute: "ú", pound: "£", euro: "€", copy: "©", reg: "®", trade: "™", middot: "·", bull: "•" };
function decode(s) {
  return String(s)
    .replace(/&#(\d+);/g, (_, d) => { try { return String.fromCodePoint(Number(d)); } catch { return ""; } })
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => { try { return String.fromCodePoint(parseInt(h, 16)); } catch { return ""; } })
    .replace(/&([a-z]+);/gi, (m, n) => NAMED[n.toLowerCase()] ?? m);
}
