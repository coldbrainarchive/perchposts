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
// are affiliate shopping guides; CBS's real business news lives under /news/)
const SKIPPED_LINKS = /\/\/www\.cbsnews\.com\/(?:video|moneywatch|essentials)\//;

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
};

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

  try {
    for (const feed of feeds) {
      let feedData;
      try {
        const res = await fetch(feed.url, { headers: FETCH_HEADERS, signal: AbortSignal.timeout(15000) });
        if (!res.ok) {
          const msg = `${feed.url} — HTTP ${res.status}`;
          console.error(`Could not fetch ${msg}`);
          stats.feedErrors.push(msg);
          continue;
        }
        const xml = await res.text();
        feedData = await parser.parseString(xml);
      } catch (err) {
        const msg = `${feed.url} — ${err.message}`;
        console.error(`Could not fetch ${msg}`);
        stats.feedErrors.push(msg);
        continue;
      }

      let postedThisFeed = 0;

      for (const item of (feedData.items || []).slice(0, 15)) {
        try {
          if (postedThisFeed >= maxPerFeed) break;

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
            const pubDate = item.isoDate ? new Date(item.isoDate) : item.pubDate ? new Date(item.pubDate) : null;
            if (!pubDate || isNaN(pubDate) || pubDate < oldestPubDate) continue;
          }


          const snippet = String(item.contentSnippet || item.summary || "").trim();
          const board = feed.board || "general";
          const rssImage = extractRSSImage(item);

          const og = await fetchOgData(url);
          const resolvedTitle = looksLikeSlug(rssTitle) ? (og?.title || null) : (rssTitle || og?.title || null);
          if (!resolvedTitle || looksLikeSlug(resolvedTitle)) { stats.skippedBadTitle.push({ url, title: rssTitle || url }); continue; }

          const attachment = {
            type: "link",
            url: og?.url || url,
            title: decodeEntities(resolvedTitle),
            description: decodeEntities(og?.description || snippet || null),
            // Page code writes & as &amp; in links, and some image servers refuse that
            image: decodeEntities(og?.image || rssImage || null),
          };
          const content = ATTACH_MARKER + JSON.stringify(attachment) + "]";

          const ok = await postArticle({ content, board, continent: feed.continent || null, country: feed.country || null });
          if (ok === "duplicate") {
            // The site already has this article, usually an old live blog that was updated
            seen.add(url);
            if (tkey) seen.add(tkey);
            stats.skippedAlreadySeen.push({ url, title: resolvedTitle });
          } else if (ok) {
            seen.add(url);
            if (tkey) seen.add(tkey);
            posted++;
            postedThisFeed++;
            postedArticles.push({ title: decodeEntities(resolvedTitle), url: og?.url || url, board, continent: feed.continent || null, country: feed.country || null });
            console.log(`[${board}][${feed.continent || "—"}][${feed.country || "—"}] ${resolvedTitle}`);
            await new Promise(r => setTimeout(r, 300));
          } else {
            stats.postFailed.push({ url, title: resolvedTitle });
          }
        } catch (err) {
          // One bad article must not stop the run
          console.error(`Skipped an article after an error: ${err.message}`);
          stats.postFailed.push({ url: String(item.link || item.guid || "unknown"), title: String(item.title || "unknown") });
        }
      }
    }
  } catch (err) {
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
