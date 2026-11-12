import { linkPreview } from "../link-preview.js";
const ATTACH_MARKER = "\n\n[ATTACH:";

// --- Helpers ---

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

// --- RSS Parser (regex-based, no DOMParser needed) ---

function parseRSS(xml) {
  const isAtom = /<feed[\s>]/.test(xml);
  const itemRe = isAtom
    ? /<entry[\s>]([\s\S]*?)<\/entry>/gi
    : /<item[\s>]([\s\S]*?)<\/item>/gi;

  const unescape = (s) => s
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1")
    .replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"').replace(/&#(\d+);/g, (_, c) => String.fromCharCode(Number(c)))
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCharCode(parseInt(h, 16)))
    .trim();

  const tag = (src, name) => {
    const m = new RegExp(`<${name}(?:\\s[^>]*)?>([\\s\\S]*?)<\\/${name}>`, "i").exec(src);
    return m ? unescape(m[1]) : null;
  };

  const attr = (src, name, attrName) => {
    const m = new RegExp(`<${name}[^>]+${attrName}=["']([^"']+)["']`, "i").exec(src);
    return m ? m[1] : null;
  };

  const items = [];
  let m;
  while ((m = itemRe.exec(xml)) !== null) {
    const el = m[1];
    const linkHref = attr(el, "link", "href");
    const linkText = tag(el, "link");
    const link = linkHref || (linkText && !linkText.startsWith("<") ? linkText : null);

    const mcUrl = attr(el, "media:content", "url") || attr(el, "media:content", "url");
    const mtUrl = attr(el, "media:thumbnail", "url");
    const encUrl = attr(el, "enclosure", "url");
    const encType = attr(el, "enclosure", "type");

    const contentEncoded = (() => {
      const ce = /<content:encoded[\s>]([\s\S]*?)<\/content:encoded>/i.exec(el);
      return ce ? unescape(ce[1]) : null;
    })();

    items.push({
      title: tag(el, "title"),
      link,
      guid: tag(el, "guid") || tag(el, "id"),
      isoDate: tag(el, "pubDate") || tag(el, "published") || tag(el, "updated"),
      contentSnippet: tag(el, "description") || tag(el, "summary"),
      content: contentEncoded || tag(el, "content"),
      enclosure: encUrl ? { url: encUrl, type: encType } : null,
      mediaContent: mcUrl ? { $: { url: mcUrl } } : null,
      mediaThumbnail: mtUrl ? { $: { url: mtUrl } } : null,
      mediaGroup: null,
    });
  }
  return items;
}

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
  const html = item.content || "";
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

// --- Forum worker fetch (uses service binding when available) ---

function forumFetch(path, options, env) {
  let fw = null;
  try { fw = env.FORUM_WORKER; } catch { fw = null; }
  if (fw) {
    return fw.fetch(new Request(`https://daboysforumip${path}`, options));
  }
  // Fall back to public URL (works for bot→main direction)
  const base = env.FORUM_WORKER_URL || "https://daboysforumip.coldbrainarchive.workers.dev";
  return fetch(`${base}${path}`, options);
}

// --- State (via forum worker) ---

async function loadState(env) {
  try {
    const res = await forumFetch("/bot-seen", {
      headers: { "x-bot-key": env.BOT_KEY }
    }, env);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return {
      seen: new Set((data.seen || []).map(e => e.startsWith("t:") ? e : normalizeUrl(e))),
      last_run: data.last_run || null
    };
  } catch (err) {
    // Never fall back to empty state — that makes every feed item look new and floods the forum
    console.error("Could not load state:", err.message);
    return null;
  }
}

async function saveState(seen, last_run, expected_last_run, env) {
  try {
    const res = await forumFetch("/bot-seen", {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-bot-key": env.BOT_KEY },
      body: JSON.stringify({ seen: [...seen].slice(-5000), last_run, expected_last_run })
    }, env);
    if (res.status === 409) {
      console.warn("State already updated by another instance — skipping save.");
      return false;
    }
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return true;
  } catch (err) {
    console.error("Could not save state:", err.message);
    return false;
  }
}

// --- Config ---

async function fetchConfig(env) {
  for (let i = 0; i < 3; i++) {
    try {
      const res = await forumFetch("/bot-config", {
        headers: { "x-bot-key": env.BOT_KEY }
      }, env);
      if (res.ok) {
        const data = await res.json();
        if (data.config) return data.config;
      } else {
        console.error(`fetchConfig attempt ${i + 1}: HTTP ${res.status}`);
      }
    } catch (err) {
      console.error(`fetchConfig attempt ${i + 1}: ${err.message}`);
    }
    if (i < 2) await new Promise(r => setTimeout(r, 5000));
  }
  return null;
}

// --- Post ---

const BOARD_BOTS = {
  "general":        { username: "NewsBot",     browser_id: "bot-newsbot" },
  "sports":         { username: "SportsBot",   browser_id: "bot-sportsbot" },
  "science-nature": { username: "ScienceBot",  browser_id: "bot-sciencebot" },
};

async function postArticle({ content, board, continent, country }, env) {
  const bot = BOARD_BOTS[board] || BOARD_BOTS["general"];
  const res = await forumFetch("/create-post", {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-bot-key": env.BOT_KEY },
    body: JSON.stringify({
      title: "",
      content,
      board,
      username: bot.username,
      browser_id: bot.browser_id,
      continent: continent || null,
      country: country || null,
    }),
  });
  if (!res.ok) { console.error(`Failed to post: ${await res.text()}`); return false; }
  return true;
}

// --- Logging ---

async function createLog(env, runType) {
  try {
    const res = await forumFetch("/bot-log-create", {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-bot-key": env.BOT_KEY },
      body: JSON.stringify({ run_type: runType })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return data.id || null;
  } catch (err) { console.error("Could not create log:", err.message); return null; }
}

async function finishLog(env, logId, { posted, postedArticles, skippedSeen, skippedBadTitle, postFailed, feedErrors }) {
  if (!logId) return;
  try {
    const res = await forumFetch("/bot-log-finish", {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-bot-key": env.BOT_KEY },
      body: JSON.stringify({
        id: logId,
        posted,
        posted_articles: postedArticles,
        skipped_seen: skippedSeen,
        skipped_bad_title: skippedBadTitle,
        post_failed: postFailed,
        feed_errors: feedErrors,
      })
    });
    if (!res.ok) console.error("Could not finish log:", await res.text());
  } catch (err) { console.error("Could not finish log:", err.message); }
}

// --- Main ---

async function run(env) {
  console.log("[run] started, FORUM_WORKER bound:", !!env.FORUM_WORKER);
  const config = await fetchConfig(env);
  console.log("[run] fetchConfig result:", config ? "ok" : "null");
  if (!config) { console.error("Could not load bot config — aborting."); return; }
  if (!config.enabled) { console.log("Bots are disabled in config — exiting."); return; }

  const state = await loadState(env);
  if (!state) { console.error("Could not load seen state — aborting."); return; }
  const { seen, last_run } = state;
  const isFirstRun = !last_run;
  console.log(`Loaded ${seen.size} seen entries. Last run: ${last_run || "never"}`);

  const runType = isFirstRun ? "first_run" : "subsequent";
  const logId = await createLog(env, runType);

  const maxPerFeed = isFirstRun ? 1 : (config.max_per_feed || 1);
  const feeds = (config.feeds || []).filter(f => f.enabled !== false);
  // Look back 6 hours, like index.js: feeds often add a story hours after its publish time
  const oldestPubDate = new Date(Date.now() - 6 * 3600000);
  let posted = 0;
  let skippedSeen = 0;
  let skippedBadTitle = 0;
  let postFailed = 0;
  const postedArticles = [];
  const feedErrors = [];

  const FETCH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  };

  for (const feed of feeds) {
    let items;
    try {
      const res = await fetch(feed.url, { headers: FETCH_HEADERS });
      if (!res.ok) { feedErrors.push(`${feed.url} — HTTP ${res.status}`); continue; }
      const xml = await res.text();
      items = parseRSS(xml);
    } catch (err) { feedErrors.push(`${feed.url} — ${err.message}`); continue; }

    let postedThisFeed = 0;

    for (const item of (items || []).slice(0, 15)) {
      if (postedThisFeed >= maxPerFeed) break;

      const url = normalizeUrl(item.link || item.guid);
      if (!url || SKIPPED_LINKS.test(url)) continue;

      // Some feeds send titles as objects; one bad item must not stop the whole run
      const rssTitle = typeof item.title === "string" ? item.title.trim() : null;
      const tkey = titleKey(rssTitle);

      if (seen.has(url) || (tkey && seen.has(tkey))) { skippedSeen++; continue; }

      if (!isFirstRun) {
        const pubDate = item.isoDate ? new Date(item.isoDate) : null;
        if (!pubDate || isNaN(pubDate) || pubDate < oldestPubDate) continue;
      }

      const snippet = String(item.contentSnippet || "").trim();
      const board = feed.board || "general";
      const rssImage = extractRSSImage(item);

      const og = await fetchOgData(url);
      const resolvedTitle = looksLikeSlug(rssTitle) ? (og?.title || null) : (rssTitle || og?.title || null);
      if (!resolvedTitle || looksLikeSlug(resolvedTitle)) { skippedBadTitle++; continue; }

      const attachment = {
        type: "link",
        url: og?.url || url,
        title: decodeEntities(resolvedTitle),
        description: decodeEntities(og?.description || snippet || null),
        image: og?.image || rssImage || null,
      };
      const content = ATTACH_MARKER + JSON.stringify(attachment) + "]";

      const ok = await postArticle({ content, board, continent: feed.continent || null, country: feed.country || null }, env);
      if (ok) {
        seen.add(url);
        if (tkey) seen.add(tkey);
        posted++;
        postedThisFeed++;
        postedArticles.push({ title: decodeEntities(resolvedTitle), url: og?.url || url, board, continent: feed.continent || null, country: feed.country || null });
        console.log(`[${board}][${feed.continent || "—"}][${feed.country || "—"}] ${resolvedTitle}`);
        await new Promise(r => setTimeout(r, 500));
      } else {
        postFailed++;
      }
    }
  }

  const newLastRun = new Date().toISOString();
  const saved = await saveState(seen, newLastRun, last_run, env);
  if (saved) console.log(`Saved ${seen.size} seen entries. Last run: ${newLastRun}`);
  else console.warn("State not saved — another instance beat this one.");

  await finishLog(env, logId, { posted, postedArticles, skippedSeen, skippedBadTitle, postFailed, feedErrors });

  if (feedErrors.length) console.error("Feed errors:\n" + feedErrors.join("\n"));
  console.log(`Done — posted ${posted} article(s).`);
}

async function dispatchGitHubAction(env) {
  const pat = env.GITHUB_PAT;
  const repo = env.GITHUB_REPO || "coldbrainarchive/perchposts";
  if (!pat) { console.error("GITHUB_PAT not set — cannot dispatch"); return; }
  const res = await fetch(`https://api.github.com/repos/${repo}/actions/workflows/news-bot.yml/dispatches`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${pat}`,
      "Accept": "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "Content-Type": "application/json",
      "User-Agent": "daboysforum-bot-worker",
    },
    body: JSON.stringify({ ref: "main" }),
  });
  if (!res.ok) {
    const text = await res.text();
    console.error(`GitHub dispatch failed: ${res.status} — ${text}`);
  } else {
    console.log("GitHub Actions workflow dispatched successfully");
  }
}

export default {
  async scheduled(event, env, ctx) {
    ctx.waitUntil(dispatchGitHubAction(env));
  },

  // Allow cron-style trigger via service binding (main worker uses ctx.waitUntil on this)
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const key = request.headers.get("x-bot-key");
    if (key !== env.BOT_KEY) return new Response("Unauthorized", { status: 401 });
    if (url.pathname === "/run-sync") {
      // Called via service binding with ctx.waitUntil on the caller side — run synchronously
      await run(env);
      return new Response("Bot run complete", { status: 200 });
    }
    if (url.pathname === "/run-sync-debug") {
      const steps = [];
      try {
        const config = await fetchConfig(env);
        steps.push({ step: "fetchConfig", ok: !!config, enabled: config?.enabled });
        if (!config || !config.enabled) return Response.json({ steps });
        const state = await loadState(env);
        steps.push({ step: "loadState", ok: !!state, seenCount: state?.seen?.size, lastRun: state?.last_run });
        if (!state) return Response.json({ steps });
        const logId = await createLog(env, "sync_debug");
        steps.push({ step: "createLog", logId });
        if (logId) {
          await finishLog(env, logId, { posted: 0, postedArticles: [], skippedSeen: 0, skippedBadTitle: 0, postFailed: 0, feedErrors: ["sync_debug"] });
          steps.push({ step: "finishLog", done: true });
        }
        return Response.json({ steps });
      } catch (err) {
        return Response.json({ steps, error: err.message, stack: err.stack }, { status: 500 });
      }
    }
    if (url.pathname === "/run") {
      // Legacy: fire-and-forget via waitUntil
      ctx.waitUntil(run(env));
      return new Response("Bot run triggered", { status: 200 });
    }
    return new Response("News Bot Worker", { status: 200 });
  }
};
