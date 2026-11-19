import Parser from "rss-parser";
import { linkPreview } from "../link-preview.js";
import { writeFileSync, existsSync, readFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const RUNTIME_FILE = path.join(__dirname, "runtime.json");
const WORKER_URL   = "https://daboysforumip.coldbrainarchive.workers.dev";
const ATTACH_MARKER = "\n\n[ATTACH:";

const BOT_KEY = process.env.BOT_KEY;
const LOOKBACK_HOURS = 6;
if (!BOT_KEY) { console.error("BOT_KEY env var is required"); process.exit(1); }

// Links the bot never posts: CBS News videos and sponsored pages (/moneywatch/ and /essentials/
// are affiliate shopping guides; CBS's real business news lives under /news/), and CBS Sports' gambling
// sections (/betting/ and /prediction/ are sportsbook and prediction-market promotions; real sports news is under /nfl/news/ etc.)
const SKIPPED_LINKS = /\/\/www\.cbsnews\.com\/(?:video|moneywatch|essentials)\/|\/\/www\.cbssports\.com\/(?:betting|prediction)\//;
// Reads feed dates, including ones written like "18 November 2026 - 22:00" (NL Times)
const feedDate = s => { if (!s) return null; let d = new Date(s); if (isNaN(d)) d = new Date(String(s).replace(/\s+-\s+(?=\d{1,2}:\d{2})/, " ")); return isNaN(d) ? null : d; };
// Ads dressed as news, from any site: sign-up offers for betting and prediction apps, promo/coupon codes, sponsored pages
const PROMO_TEXT = /\b(?:promo|bonus|coupon|referral|voucher|discount)\s+codes?\b|\bbonus\s+bets?\b|\bfree\s+bets?\b|\bsign[- ]?up\s+(?:bonus|offer)s?\b|\bdeposit\s+match\b|\bodds\s+boosts?\b|\b(?:sponsored|paid)\s+(?:content|post|partner(?:ship)?)\b/i;
const isPromo = (...texts) => PROMO_TEXT.test(texts.filter(Boolean).join(" "));
// Entertainment is film/TV, music, games and arts, not celebrity gossip: skip stories about people's private lives
const GOSSIP_TEXT = /\b(?:dating|date\s+night|spotted|ex-(?:wife|husband|girlfriend|boyfriend)|wedding\s+(?:photos|dress)|divorc\w*|break[- ]?up|split\s+from|engaged|engagement\s+ring|pregnan\w*|baby\s+bump|red\s+carpet|net\s+worth|feud\w*|slams?|cheat(?:ed|ing)|boyfriend|girlfriend|romance\s+rumou?rs?|kardashian\w*|jenner|royal\s+family|bikini|shirtless|plastic\s+surgery|fashion\s+police|outfit|nip\s*slip)\b/i;
const isGossip = (...texts) => GOSSIP_TEXT.test(texts.filter(Boolean).join(" "));

function normalizeUrl(url) {
  if (!url) return url;
  try {
    const u = new URL(url);
    u.search = "";
    u.hash = "";
    return u.toString();
  } catch { return url; }
}

function titleKey(title) {
  if (!title) return null;
  return "t:" + title.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

// --- Seen URLs: stored in Worker KV via bot endpoints ---

async function loadState() {
  try {
    const res = await fetch(`${WORKER_URL}/bot-seen`, {
      headers: { "x-bot-key": BOT_KEY }
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    // Normalize stored URLs on load — skip t: title keys so spaces don't get percent-encoded
    return { seen: new Set((data.seen || []).map(e => e.startsWith("t:") ? e : normalizeUrl(e))), last_run: data.last_run || null };
  } catch (err) {
    // Never fall back to empty state — that makes every feed item look new and floods the forum
    console.error("Could not load state from Worker:", err.message);
    return null;
  }
}

async function saveState(seen, last_run, expected_last_run) {
  try {
    const res = await fetch(`${WORKER_URL}/bot-seen`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-bot-key": BOT_KEY },
      body: JSON.stringify({ seen: [...seen].slice(-5000), last_run, expected_last_run })
    });
    if (res.status === 409) {
      console.warn("State was already updated by another instance — this run may have posted duplicates.");
      return false;
    }
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return true;
  } catch (err) {
    console.error("Could not save state to Worker:", err.message);
    return false;
  }
}

// --- Runtime (interval tracking) ---

function loadRuntime() {
  if (!existsSync(RUNTIME_FILE)) return {};
  try { return JSON.parse(readFileSync(RUNTIME_FILE, "utf8")); }
  catch { return {}; }
}

function saveRuntime(data) {
  writeFileSync(RUNTIME_FILE, JSON.stringify(data));
}

// --- Config ---

async function fetchConfig(retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(`${WORKER_URL}/bot-config`, { headers: { "x-bot-key": BOT_KEY } });
      if (res.ok) {
        const data = await res.json();
        if (data.config) return data.config;
        console.error(`fetchConfig: ok but no config field: ${JSON.stringify(data)}`);
      } else {
        console.error(`fetchConfig attempt ${i + 1}: HTTP ${res.status} — ${await res.text()}`);
      }
    } catch (err) {
      console.error(`fetchConfig attempt ${i + 1}: ${err.message}`);
    }
    if (i < retries - 1) await new Promise(r => setTimeout(r, 5000));
  }
  return null;
}

// --- Helpers ---

function extractRSSImage(item) {
  const mc = item.mediaContent;
  if (mc) {
    const url = mc?.$ ? mc.$.url : mc?.url;
    if (url && /\.(jpe?g|png|webp|gif)/i.test(url)) return url;
  }
  const mt = item.mediaThumbnail;
  if (mt) {
    const url = mt?.$ ? mt.$.url : mt?.url;
    if (url) return url;
  }
  const mg = item.mediaGroup;
  if (mg) {
    const content = Array.isArray(mg["media:content"]) ? mg["media:content"][0] : mg["media:content"];
    const url = content?.$ ? content.$.url : null;
    if (url && /\.(jpe?g|png|webp|gif)/i.test(url)) return url;
  }
  if (item.enclosure?.url && /image/.test(item.enclosure.type || "")) return item.enclosure.url;
  const html = item.content || item["content:encoded"] || "";
  const match = html.match(/<img[^>]+src=["']([^"']+)/i);
  if (match) return match[1];
  return null;
}

// Link previews come from the site's shared preview code (../link-preview.js): honest name, oEmbed for
// YouTube/X/TikTok/Spotify, BBC via its feeds. The old Googlebot-style lookup only fills in anything missing,
// so no article ends up with less than before.
async function fetchOgData(url) {
  const n = await linkPreview(url, fetch, { addressFallback: false, timeoutMs: 10000 }).catch(() => null);
  if (n && n.title && n.description && n.image) return { title: n.title, description: n.description, image: n.image, url };
  const o = await fetchOgDataOld(url);
  if (!n) return o;
  if (!o) return { title: n.title, description: n.description, image: n.image, url };
  return { title: n.title || o.title, description: n.description || o.description, image: n.image || o.image, url };
}

async function fetchOgDataOld(url) {
  try {
    const res = await fetch(url, {
      headers: { "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)" },
      signal: AbortSignal.timeout(8000),
    });
    if (!res.ok) return null;
    const html = await res.text();
    const get = (prop) => {
      const m = html.match(new RegExp(`<meta[^>]+(?:property|name)=["']${prop}["'][^>]+content=["']([^"']+)["']`, "i"))
                || html.match(new RegExp(`<meta[^>]+content=["']([^"']+)["'][^>]+(?:property|name)=["']${prop}["']`, "i"));
      return m ? m[1].trim() : null;
    };
    const titleTag = html.match(/<title[^>]*>([^<]+)<\/title>/i)?.[1]?.trim() || null;
    return {
      title: get("og:title") || get("twitter:title") || titleTag || null,
      description: get("og:description") || get("description") || null,
      image: get("og:image") || get("twitter:image") || null,
      url,
    };
  } catch { return null; }
}

function decodeEntities(str) {
  if (!str) return str;
  return str
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, code) => String.fromCharCode(Number(code)))
    .replace(/&#x([0-9a-f]+);/gi, (_, hex) => String.fromCharCode(parseInt(hex, 16)));
}

function looksLikeSlug(str) {
  if (!str) return false;
  return !/\s/.test(str) && (str.includes('-') || str.includes('_')) && str.length > 20;
}

const BOARD_BOTS = {
  "general":        { username: "NewsBot",     browser_id: "bot-newsbot" },
  "sports":         { username: "SportsBot",   browser_id: "bot-sportsbot" },
  "science-nature": { username: "ScienceBot",  browser_id: "bot-sciencebot" },
  "nature":         { username: "NatureBot",   browser_id: "bot-naturebot" },
  // Entertainment posts as NewsBot: a new bot name would change the people-only posts index (HUMAN_POSTS)
  "entertainment":  { username: "NewsBot",     browser_id: "bot-newsbot" },
};

// --- Arranging an hour's batch (top of the site first) ---

// Takes turns between groups so no group bunches up: [a1,a2,b1,c1,c2] -> a1,b1,c1,a2,c2
function takeTurns(groups) {
  const out = [], qs = groups.map(g => [...g]);
  while (qs.some(q => q.length)) for (const q of qs) if (q.length) out.push(q.shift());
  return out;
}
function groupBy(list, key) {
  const m = new Map();
  for (const x of list) { const k = key(x); if (!m.has(k)) m.set(k, []); m.get(k).push(x); }
  return [...m.values()];
}
// Biggest tier first; inside a tier, outer groups take turns (starting point moves each hour so the
// same region doesn't always lead), and inside each outer group the inner groups take turns too.
// An outlet with many feeds (BBC has 19) mustn't fill a whole tier: each extra story from the same
// outlet drops one tier, so the big names stay near the top without crowding everyone else out.
const outletOf = j => { try { return new URL(j.feed.url).hostname.replace(/^(www|feeds|rss)\./, ""); } catch { return j.feed.url; } };
function byTier(list, outer, inner, turn) {
  const seenOutlet = new Map(), eff = new Map();
  for (const j of list) {
    const o = outletOf(j), n = seenOutlet.get(o) || 0;
    seenOutlet.set(o, n + 1);
    eff.set(j, Math.min(4, (Number.isFinite(j.feed.tier) ? j.feed.tier : 3) + n));
  }
  const tier = j => eff.get(j);
  const out = [];
  for (const t of [...new Set(list.map(tier))].sort((a, b) => a - b)) {
    let groups = groupBy(list.filter(j => tier(j) === t), outer).map(g => takeTurns(groupBy(g, inner)));
    if (groups.length) { const s = turn % groups.length; groups = [...groups.slice(s), ...groups.slice(0, s)]; }
    out.push(...takeTurns(groups));
  }
  return out;
}
function arrange(jobs, turn = new Date().getUTCHours()) {
  const tier = j => (Number.isFinite(j.feed.tier) ? j.feed.tier : 3);
  const world = jobs.filter(j => tier(j) === 0).sort((a, b) => (a.feed.top || 99) - (b.feed.top || 99));
  const rest = jobs.filter(j => tier(j) !== 0);
  const region = j => j.feed.continent || "—", country = j => j.feed.country || "—";
  const gen = byTier(rest.filter(j => j.board === "general"), region, country, turn);
  const sec = byTier(rest.filter(j => j.board !== "general"), j => j.board, region, turn);
  // Spread the other sections evenly through the general news
  const out = [...world];
  let g = 0, s = 0;
  while (g < gen.length || s < sec.length) {
    const takeSec = s < sec.length && (g >= gen.length || (s + 1) / (sec.length + 1) <= (g + 1) / (gen.length + 1));
    out.push(takeSec ? sec[s++] : gen[g++]);
  }
  return out;
}

async function createLog(runType) {
  try {
    const res = await fetch(`${WORKER_URL}/bot-log-create`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-bot-key": BOT_KEY },
      body: JSON.stringify({ run_type: runType }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return data.id || null;
  } catch (err) { console.error("Could not create log:", err.message); return null; }
}

async function finishLog(logId, { posted, postedArticles, skippedSeen, skippedBadTitle, postFailed, feedErrors }) {
  if (!logId) return;
  try {
    const res = await fetch(`${WORKER_URL}/bot-log-finish`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-bot-key": BOT_KEY },
      body: JSON.stringify({
        id: logId,
        posted,
        posted_articles: postedArticles,
        skipped_seen: skippedSeen,
        skipped_bad_title: skippedBadTitle,
        post_failed: postFailed,
        feed_errors: feedErrors,
      }),
    });
    if (!res.ok) console.error("Could not finish log:", await res.text());
  } catch (err) { console.error("Could not finish log:", err.message); }
}

async function postArticle({ content, board, continent, country }) {
  const bot = BOARD_BOTS[board] || BOARD_BOTS["general"];
  const body = JSON.stringify({
    title: "",
    content,
    board,
    username: bot.username,
    browser_id: bot.browser_id,
    continent: continent || null,
    country: country || null,
  });
  // A dropped connection must cost one article at most, never the whole run
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const res = await fetch(`${WORKER_URL}/create-post`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "x-bot-key": BOT_KEY },
        body,
        signal: AbortSignal.timeout(20000),
      });
      if (res.ok) return true;
      if (res.status === 409) return "duplicate";
      console.error(`  Failed to post: ${await res.text()}`);
      return false;
    } catch (err) {
      console.error(`  Could not reach the site (try ${attempt} of 2): ${err.cause?.code || err.message}`);
      if (attempt < 2) await new Promise(r => setTimeout(r, 2000));
    }
  }
  return false;
}

// --- Main ---

async function run() {
  const runtime = loadRuntime();

  if (!process.env.FORCE_RUN) {
    const lastIntervalHours = runtime.interval_hours || 1;
    const intervalMs = lastIntervalHours * 60 * 60 * 1000;
    if (runtime.last_run) {
      const elapsed = Date.now() - new Date(runtime.last_run).getTime();
      if (elapsed < intervalMs) {
        const nextIn = Math.ceil((intervalMs - elapsed) / 60000);
        console.log(`Interval not reached — next run in ~${nextIn} min.`);
        return;
      }
    }
  }

  const config = await fetchConfig();
  if (!config) { console.error("Could not load bot config — aborting."); process.exit(1); }
  if (!config.enabled) { console.log("Bots are disabled in config — exiting."); return; }

  const parser = new Parser({
    customFields: {
      item: [
        ["media:content", "mediaContent", { keepArray: false }],
        ["media:thumbnail", "mediaThumbnail", { keepArray: false }],
        ["media:group", "mediaGroup", { keepArray: false }],
      ],
    },
  });

  const state = await loadState();
  if (!state) { console.error("Could not load seen state — aborting."); process.exit(1); }
  const { seen, last_run } = state;
  const isFirstRun = !last_run;
  console.log(`Loaded ${seen.size} seen entries. Last run: ${last_run || "never"}`);
  // First run: post exactly 1 per feed as baseline
  // Subsequent runs: post up to max_per_feed for any unseen articles
  const maxPerFeed = isFirstRun ? 1 : (config.max_per_feed || 1);
  const feeds = (config.feeds || []).filter(f => f.enabled !== false);
  // Feeds often add a story hours after its publish time, so look back 6 hours rather than to the last
  // run. Repeats are stopped by the seen list here and by the site's bot_links check (409).
  const oldestPubDate = new Date(Date.now() - LOOKBACK_HOURS * 3600000);
  let posted = 0;
  const stats = { feedErrors: [], skippedAlreadySeen: [], skippedBadTitle: [], postFailed: [] };
  const postedArticles = [];

  // Expire any stuck "running" logs from previous crashed runs
  await fetch(`${WORKER_URL}/bot-log-expire`, {
    method: "POST",
    headers: { "x-bot-key": BOT_KEY },
  }).catch(() => {});

  const runType = isFirstRun ? "first_run" : "subsequent";
  const logId = await createLog(runType);

  const FETCH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  };

  // The seen list normally saves at the end, so a run that dies would repost everything it posted.
  // Keeping last_run unchanged means the next run still looks back and picks up what this one missed.
  const saveProgress = async () => {
    if (!last_run) return;
    if (await saveState(seen, last_run, last_run)) console.log(`Saved progress: ${posted} article(s) won't be reposted.`);
  };
  const stopEarly = async () => {
    console.error("Run stopped early — saving progress.");
    await saveProgress();
    process.exit(1);
  };
  process.once("SIGINT", stopEarly);
  process.once("SIGTERM", stopEarly);

  // Each run gathers the whole hour first, arranges it, then releases it in one go at the top of the hour.
  // Order (top of the site first): the world desks (tier 0, by their "top" number), then everything else
  // from the biggest outlets (tier 1) down to the smallest (tier 4). Inside a tier the regions take turns,
  // and sports / entertainment / science / nature are spread evenly through the general news.
  const tierOf = f => (Number.isFinite(f.tier) ? f.tier : 3);
  const isWorld = f => tierOf(f) === 0;
  const collected = [];
  const keysOf = j => [j.url, j.tkey].filter(Boolean);
  // World desks gather first, so their stories aren't taken by a regional feed from the same outlet
  const order = [...feeds.filter(isWorld).sort((a, b) => (a.top || 99) - (b.top || 99)), ...feeds.filter(f => !isWorld(f))];

  // Fetch every feed's XML a few at a time (the slow part, opening each article, stays in order below)
  const xmlOf = new Map();
  {
    let next = 0;
    const worker = async () => {
      while (next < order.length) {
        const feed = order[next++];
        try {
          const res = await fetch(feed.url, { headers: FETCH_HEADERS, signal: AbortSignal.timeout(15000) });
          if (!res.ok) { xmlOf.set(feed, { error: `HTTP ${res.status}` }); continue; }
          xmlOf.set(feed, { xml: await res.text() });
        } catch (err) { xmlOf.set(feed, { error: err.message }); }
      }
    };
    await Promise.all(Array.from({ length: 8 }, worker));
  }

  const release = async () => {
    if (!collected.length) return;
    const list = arrange(collected);
    const payload = list.map(j => {
      const bot = BOARD_BOTS[j.board] || BOARD_BOTS["general"];
      return { content: j.content, board: j.board, username: bot.username, browser_id: bot.browser_id, continent: j.feed.continent || null, country: j.feed.country || null };
    });
    let out = null;
    for (let attempt = 1; attempt <= 3 && !out; attempt++) {
      try {
        const res = await fetch(`${WORKER_URL}/bot-release`, {
          method: "POST",
          headers: { "Content-Type": "application/json", "x-bot-key": BOT_KEY },
          body: JSON.stringify({ posts: payload }),
          signal: AbortSignal.timeout(60000),
        });
        if (res.ok) out = await res.json();
        else console.error(`  Release failed (try ${attempt} of 3): HTTP ${res.status} ${await res.text()}`);
      } catch (err) { console.error(`  Could not reach the site (try ${attempt} of 3): ${err.cause?.code || err.message}`); }
      if (!out && attempt < 3) await new Promise(r => setTimeout(r, 3000));
    }
    if (!out) {
      // Safety net: post one at a time, bottom first, so the top story still ends up on top
      console.error("  Batch release failed — posting one at a time instead.");
      const results = new Array(list.length);
      for (let i = list.length - 1; i >= 0; i--) {
        const j = list[i];
        const ok = await postArticle({ content: j.content, board: j.board, continent: j.feed.continent || null, country: j.feed.country || null });
        results[i] = ok === "duplicate" ? { duplicate: true } : { ok: !!ok };
      }
      out = { results };
    }
    list.forEach((j, i) => {
      const r = out?.results?.[i];
      if (r?.ok) {
        posted++;
        postedArticles.push({ title: decodeEntities(j.title), url: j.link, board: j.board, continent: j.feed.continent || null, country: j.feed.country || null });
      } else if (r?.duplicate) {
        stats.skippedAlreadySeen.push({ url: j.url, title: j.title });   // stays seen
      } else {
        stats.postFailed.push({ url: j.url, title: j.title });
        keysOf(j).forEach(k => seen.delete(k));                        // let a later run try it again
      }
    });
    // Log top of the site first
    list.forEach((j, i) => { if (out?.results?.[i]?.ok) console.log(`[${j.board}][${j.feed.continent || "—"}][${j.feed.country || "—"}] ${j.title}`); });
    collected.length = 0;
  };
  // A run that is stopped mid-way releases what it has instead of losing it
  process.removeAllListeners("SIGINT"); process.removeAllListeners("SIGTERM");
  const stopNow = async () => { console.error("Run stopped early — releasing what was gathered."); await release(); await saveProgress(); process.exit(1); };
  process.once("SIGINT", stopNow);
  process.once("SIGTERM", stopNow);

  try {
    for (const feed of order) {
      const got = xmlOf.get(feed);
      let feedData;
      if (!got || got.error) {
        const msg = `${feed.url} — ${got?.error || "not fetched"}`;
        console.error(`Could not fetch ${msg}`);
        stats.feedErrors.push(msg);
        continue;
      }
      try { feedData = await parser.parseString(got.xml); }
      catch (err) {
        const msg = `${feed.url} — ${err.message}`;
        console.error(`Could not fetch ${msg}`);
        stats.feedErrors.push(msg);
        continue;
      }

      let takenThisFeed = 0;

      for (const item of (feedData.items || []).slice(0, 15)) {
        try {
          if (takenThisFeed >= maxPerFeed) break;

          const url = normalizeUrl(item.link || item.guid);
          if (!url || SKIPPED_LINKS.test(url)) continue;

          // Some feeds send titles as objects; one bad item must not stop the whole run
          const rssTitle = typeof item.title === "string" ? item.title.trim() : null;
          const tkey = titleKey(rssTitle);

          // Seen check first — blocks re-posts even if feed updates the URL or pubDate
          if (seen.has(url) || (tkey && seen.has(tkey))) {
            stats.skippedAlreadySeen.push({ url, title: rssTitle || url });
            continue;
          }

          // Date filter — skip articles older than the lookback (only on subsequent runs)
          if (!isFirstRun) {
            const pubDate = item.isoDate ? new Date(item.isoDate) : feedDate(item.pubDate);
            if (!pubDate || isNaN(pubDate) || pubDate < oldestPubDate) continue;
          }

          const snippet = String(item.contentSnippet || item.summary || "").trim();
          if (isPromo(rssTitle, snippet)) continue;                      // ads and betting promos
          const board = feed.board || "general";
          const rssImage = extractRSSImage(item);

          const og = await fetchOgData(url);
          const resolvedTitle = looksLikeSlug(rssTitle) ? (og?.title || null) : (rssTitle || og?.title || null);
          if (!resolvedTitle || looksLikeSlug(resolvedTitle)) { stats.skippedBadTitle.push({ url, title: rssTitle || url }); continue; }
          if (isPromo(resolvedTitle, og?.description)) continue;
          if (board === "entertainment" && isGossip(resolvedTitle, og?.description || item.contentSnippet)) continue;

          const attachment = {
            type: "link",
            url: og?.url || url,
            title: decodeEntities(resolvedTitle),
            description: decodeEntities(og?.description || snippet || null),
            // Page code writes & as &amp; in links, and some image servers refuse that
            image: decodeEntities(og?.image || rssImage || null),
          };
          const content = ATTACH_MARKER + JSON.stringify(attachment) + "]";

          // Claim it now (so no later feed takes the same story); it goes out with the release
          const job = { content, board, feed, url, tkey, title: resolvedTitle, link: og?.url || url };
          keysOf(job).forEach(k => seen.add(k));
          collected.push(job);
          takenThisFeed++;
        } catch (err) {
          // One bad article must not stop the run
          console.error(`Skipped an article after an error: ${err.message}`);
          stats.postFailed.push({ url: String(item.link || item.guid || "unknown"), title: String(item.title || "unknown") });
        }
      }
    }

    // Hold everything until the top of the hour (runs start a few minutes early), then release it at once
    const t = new Date(), mins = t.getUTCMinutes();
    if (mins >= 45 && !process.env.NO_WAIT) {
      const topOfHour = new Date(t); topOfHour.setUTCHours(t.getUTCHours() + 1, 0, 0, 0);
      const wait = topOfHour - t;
      console.log(`Gathered ${collected.length} article(s); releasing in ${Math.round(wait / 1000)}s at ${topOfHour.toISOString()}`);
      await new Promise(r => setTimeout(r, wait));
    }
    await release();
  } catch (err) {
    await release().catch(() => {});
    await saveProgress();
    throw err;
  }

  const newLastRun = new Date().toISOString();
  const saved = await saveState(seen, newLastRun, last_run);
  if (saved) console.log(`Saved ${seen.size} seen URLs. Last run set to ${newLastRun}`);
  else console.warn(`State not saved — another instance beat this one.`);
  console.log(`\nDone — posted ${posted} new article(s).`);

  await finishLog(logId, {
    posted,
    postedArticles,
    skippedSeen: stats.skippedAlreadySeen.length,
    skippedBadTitle: stats.skippedBadTitle.length,
    postFailed: stats.postFailed.length,
    feedErrors: stats.feedErrors,
  });

  if (process.env.GITHUB_STEP_SUMMARY) {
    const { appendFileSync } = await import("fs");
    const time = new Date().toUTCString();
    const runType = isFirstRun ? "First Run (baseline)" : "Subsequent Run";

    const skipSection = (label, items) => {
      if (items.length === 0) return `**${label}:** none\n\n`;
      let out = `**${label} (${items.length}):**\n`;
      for (const { url, title } of items) out += `- [${title}](${url})\n`;
      return out + "\n";
    };

    let summary = `## News Bot Run — ${time}\n`;
    summary += `**Type:** ${runType}\n`;
    summary += `**Posted:** ${posted} article(s)\n\n`;

    if (!isFirstRun && posted === 0) {
      summary += `> No new articles since last run.\n\n`;
    }

    summary += `### Skipped\n`;
    summary += skipSection("Already seen", stats.skippedAlreadySeen);
    summary += skipSection("Bad/slug title", stats.skippedBadTitle);
    summary += skipSection("Post failed", stats.postFailed);

    if (stats.feedErrors.length > 0) {
      summary += `### Feed Errors (${stats.feedErrors.length})\n`;
      for (const e of stats.feedErrors) summary += `- \`${e}\`\n`;
      summary += "\n";
    } else {
      summary += `### Feed Errors\nNone\n\n`;
    }

    appendFileSync(process.env.GITHUB_STEP_SUMMARY, summary);
  }
}

run().catch(err => { console.error("Bot crashed:", err); process.exit(1); });
