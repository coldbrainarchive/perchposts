import { stripMedia, stripIsoBmffStream } from "./media-strip.js";
import { linkPreview } from "./link-preview.js";
import NEST_WORDS from "./birds/lists.json";
import { buildTrending } from "./trending.js";
import LAND_MASK from "./land-mask.js";

// Is this spot land? (worm hunt) Reads one row of the land map (decoded once per row and kept while the worker lives).
let LAND_ROWS = null; const LAND_ROW = new Map();
function isLand(lat, lng) {
  if (!LAND_ROWS) LAND_ROWS = LAND_MASK.split(";");
  const H = LAND_ROWS.length, W = 8192, y = Math.min(H - 1, Math.max(0, Math.floor((90 - lat) / 180 * H))), x = Math.min(W - 1, Math.max(0, Math.floor((((lng + 180) % 360 + 360) % 360) / 360 * W)));
  let ends = LAND_ROW.get(y);
  if (!ends) { ends = []; let at = 0; for (const r of LAND_ROWS[y].split(".")) { at += parseInt(r, 36); ends.push(at); } LAND_ROW.set(y, ends); }
  let i = 0; while (i < ends.length && ends[i] <= x) i++;
  return i % 2 === 1;   // runs alternate sea, land, sea… so odd runs are land
}

// Sign-up nests: 5 usernames (eggs) per device, a fresh set only every 15 minutes, and only names never offered to
// that device before. Clearing the browser makes a new device, so each network (keyed IP hash) gets at most
// NEST_NET_CAP new nests per 15 minutes; past that, a new device shares the network's latest nest.
const NEST_WAIT = 15 * 60000, NEST_NET_CAP = 4, NEST_KEEP = 2 * 86400000;
// Word pairs that read as a slur about people are never handed out: a nationality or people word with "eyed"/"faced",
// "black/yellow/brown-faced", and "oriental" in any name
const NEST_PEOPLE = new Set(["african", "american", "amazonian", "andean", "arabian", "asian", "australasian", "bornean", "burmese", "chinese", "eurasian", "european",
  "himalayan", "indian", "javan", "mongolian", "oriental", "pacific", "papuan", "philippine", "siberian", "sumatran", "tibetan"]);
const nestBlocked = n => { const [a, b] = String(n).toLowerCase().split("-");
  return a === "oriental" || ((b === "eyed" || b === "faced") && NEST_PEOPLE.has(a)) || (b === "faced" && ["black", "yellow", "brown"].includes(a)); };
const nestName = () => { const p = a => a[Math.floor(Math.random() * a.length)]; for (;;) { const n = `${p(NEST_WORDS.A)}-${p(NEST_WORDS.B)}-${p(NEST_WORDS.C)}`; if (!nestBlocked(n)) return n; } };

export default {
  async fetch(request, env, ctx) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization, x-bot-key"
    };
    try {
      return await handleRequest(request, env, ctx, corsHeaders);
    } catch (err) {
      console.error("unhandled:", err && (err.stack || err.message));
      return new Response(JSON.stringify({ error: "Something went wrong. Please try again." }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" }
      });
    }
  },

  // Hourly: make sure the read-saving indexes exist (self-heals if they go missing,
  // and retries automatically if D1 is still over its daily limit).
  async scheduled(event, env, ctx) {
    ctx.waitUntil(ensureIndexes(env, event));
    // Globe page: rebuild the 24h trending stories every hour
    ctx.waitUntil(buildTrending(env).catch(e => console.error("buildTrending", e.message)));
  }
};

const LOGIN_TRIES = 10, LOCK_MINUTES = 15;

// Posts written by people. Queries must repeat this text exactly to use idx_posts_human_activity.
const HUMAN_POSTS = `username NOT IN ('NewsBot','ScienceBot','NatureBot','SportsBot')`;

// Mirrors the feed_indexes, paged_feeds and mod_lists migrations in d1/migrations — indexes only, never touches rows.
const INDEX_STATEMENTS = [
  `DROP INDEX IF EXISTS idx_posts_deleted`,
  `CREATE INDEX IF NOT EXISTS idx_posts_feed_created  ON posts(pinned_global DESC, pinned DESC, created_at DESC)`,
  `CREATE INDEX IF NOT EXISTS idx_posts_feed_activity ON posts(pinned_global DESC, pinned DESC, last_activity DESC)`,
  `CREATE INDEX IF NOT EXISTS idx_posts_browser_id     ON posts(browser_id)`,
  `CREATE INDEX IF NOT EXISTS idx_posts_username       ON posts(username)`,
  `CREATE INDEX IF NOT EXISTS idx_posts_mod_user_id    ON posts(mod_user_id)`,
  `CREATE INDEX IF NOT EXISTS idx_posts_created_at     ON posts(created_at DESC)`,
  `CREATE INDEX IF NOT EXISTS idx_comments_browser_id  ON comments(browser_id)`,
  `CREATE INDEX IF NOT EXISTS idx_comments_username    ON comments(username)`,
  `CREATE INDEX IF NOT EXISTS idx_comments_mod_user_id ON comments(mod_user_id)`,
  `CREATE INDEX IF NOT EXISTS idx_posts_human_activity ON posts(last_activity DESC) WHERE ${HUMAN_POSTS}`,
  `CREATE INDEX IF NOT EXISTS idx_bot_logs_status      ON bot_logs(status, started_at)`,
  `CREATE INDEX IF NOT EXISTS idx_posts_deleted_list   ON posts(created_at DESC) WHERE deleted = 1`,
  `CREATE INDEX IF NOT EXISTS idx_posts_archived_list  ON posts(created_at DESC) WHERE archived = 1 AND deleted = 0`,
  `CREATE INDEX IF NOT EXISTS idx_posts_huddles        ON posts(pinned_global DESC, pinned DESC, created_at DESC) WHERE is_huddle = 1`,
  `CREATE INDEX IF NOT EXISTS idx_posts_frozen_list    ON posts(created_at DESC) WHERE frozen = 1 AND deleted = 0`,
  `CREATE INDEX IF NOT EXISTS idx_comments_post_created ON comments(post_id, created_at)`,
  `CREATE INDEX IF NOT EXISTS idx_comments_pinned      ON comments(post_id) WHERE pinned = 1`,
];
const REQUIRED_INDEXES = ["idx_posts_feed_created", "idx_posts_feed_activity", "idx_posts_username", "idx_comments_username",
  "idx_posts_human_activity", "idx_bot_logs_status", "idx_posts_deleted_list", "idx_posts_archived_list", "idx_posts_huddles",
  "idx_comments_post_created", "idx_comments_pinned", "idx_posts_frozen_list"];

// BOT-KEYS-START
const TRACKING_PARAMS = /^(utm_|at_|cmp|ns_|fbclid|gclid|ref$|ocid|traffic_source|smid|ito|sr_share|mc_)/i;
const REPEAT_TITLE_DAYS = 6; // under a week, so weekly columns and podcasts can still post

// Two links to the same article can differ by http/https, www, tracking codes or a trailing slash.
// Broken and home page links aren't one article, so they return null.
function articleKey(link) {
  if (!link || link.includes("undefined")) return null;
  let u;
  try { u = new URL(link); } catch { return null; }
  const path = u.pathname.replace(/\/+$/, "");
  if (path.length < 12) return null;
  let host = u.hostname.toLowerCase().replace(/^www\./, "");
  if (host === "bbc.com") host = "bbc.co.uk";
  const query = [...u.searchParams].filter(([k]) => !TRACKING_PARAMS.test(k)).map(([k, v]) => `${k}=${v}`).sort().join("&");
  return `l:${host}${path}${query ? `?${query}` : ""}`;
}

function headlineKey(title) {
  const t = String(title || "").toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
  return t.length >= 20 ? `t:${t}` : null;
}
// BOT-KEYS-END

function botPostKeys(content) {
  const at = (content || "").indexOf("[ATTACH:");
  if (at < 0) return { link: null, title: null };
  try {
    const a = JSON.parse(content.slice(at + 8, content.lastIndexOf("]")));
    return { link: articleKey(a.url), title: headlineKey(a.title) };
  } catch { return { link: null, title: null }; }
}

// Claims the article in one step, so two runs at once can't both post it. A problem here must never
// stop the bots posting, so it logs and lets the post through.
async function claimBotPost(env, keys, now) {
  const claimed = [];
  try {
    if (keys.link) {
      const r = await env.DB.prepare(`INSERT OR IGNORE INTO bot_links (url, created_at) VALUES (?, ?)`).bind(keys.link, now).run();
      if (r.meta.changes === 0) return { duplicate: true, claimed };
      claimed.push(keys.link);
    }
    if (keys.title) {
      const cutoff = new Date(Date.now() - REPEAT_TITLE_DAYS * 86400000).toISOString();
      const r = await env.DB.prepare(
        `INSERT INTO bot_links (url, created_at) VALUES (?, ?) ON CONFLICT(url) DO UPDATE SET created_at = excluded.created_at WHERE bot_links.created_at < ?`
      ).bind(keys.title, now, cutoff).run();
      if (r.meta.changes === 0) return { duplicate: true, claimed };
      claimed.push(keys.title);
    }
  } catch (err) {
    console.error("create-post: could not check for repeats:", err.message);
  }
  return { duplicate: false, claimed };
}

// Turnstile. Tokens are single use, and anything unexpected counts as failing the check.
async function passesBotCheck(env, token, ip, action) {
  const hostnames = (env.TURNSTILE_HOSTNAMES || "").split(",").map(h => h.trim()).filter(Boolean);
  if (typeof token !== "string" || !token || token.length > 2048 || !hostnames.length || !env.TURNSTILE_SECRET) return false;
  try {
    const form = new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: token });
    if (ip) form.set("remoteip", ip);
    const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form,
      signal: AbortSignal.timeout(10000)
    });
    if (!res.ok) return false;
    const result = await res.json();
    return result.success === true && result.action === action && hostnames.includes(result.hostname);
  } catch (err) {
    console.error("passesBotCheck:", err.message);
    return false;
  }
}

// Chirp counts for just the posts being returned, so feeds never need to fetch every chirp on the site
// Huddles inbox: for each huddle, the last chirp, and how many chirps (and from whom) arrived since you last read
// it. "Last read" is the later of your saved read spot (huddle_reads) and your own last chirp there.
async function addHuddleInbox(env, rows, name) {
  if (!rows.length || !name) return rows;
  const me = name.toLowerCase(), ids = rows.map(p => p.id);
  try {
    const { results: rd = [] } = await env.DB.prepare(
      `SELECT post_id, read_at FROM huddle_reads WHERE username = ? AND post_id IN (${ids.map(() => "?").join(",")})`
    ).bind(me, ...ids).all();
    const readAt = new Map(rd.map(r => [r.post_id, r.read_at]));
    const first = await env.DB.batch(ids.flatMap(id => [
      env.DB.prepare(`SELECT username, content, created_at FROM comments WHERE post_id = ? AND deleted = 0 ORDER BY created_at DESC LIMIT 1`).bind(id),
      env.DB.prepare(`SELECT MAX(created_at) AS t FROM comments WHERE post_id = ? AND deleted = 0 AND LOWER(username) = ?`).bind(id, me)
    ]));
    const base = ids.map((id, i) => {
      const mine = first[2 * i + 1].results?.[0]?.t || null, r = readAt.get(id) || null;
      return (r && (!mine || r > mine) ? r : mine) || "";
    });
    const fresh = await env.DB.batch(ids.map((id, i) => env.DB.prepare(
      `SELECT username, COUNT(*) AS n, MAX(created_at) AS t FROM comments WHERE post_id = ? AND deleted = 0 AND created_at > ?
         AND username IS NOT NULL AND username != '__system__' AND LOWER(username) != ? GROUP BY username`
    ).bind(id, base[i], me)));
    rows.forEach((p, i) => {
      const last = first[2 * i].results?.[0] || null, fr = (fresh[i].results || []).sort((a, b) => (a.t < b.t ? 1 : -1));
      p.hx = {
        unread: fr.reduce((a, r) => a + r.n, 0),
        fresh: fr.map(r => r.username),
        nt: fr.length ? fr[0].t : null, // newest unread chirp, so a device that already read past it can clear the badge
        last: last ? { u: last.username, c: String(last.content || "").slice(0, 400), t: last.created_at } : null
      };
    });
  } catch (err) {
    console.error("huddle inbox unavailable:", err.message);
  }
  return rows;
}

async function addCommentCounts(env, posts) {
  if (!posts.length) return posts;
  try {
    const { results } = await env.DB.prepare(
      `SELECT post_id, COUNT(*) AS n FROM comments WHERE post_id IN (${ID_LIST}) AND deleted = 0 AND (username IS NULL OR username != '__system__') GROUP BY post_id`
    ).bind(JSON.stringify(posts.map(p => p.id))).all();
    const counts = Object.fromEntries((results || []).map(r => [r.post_id, r.n]));
    return posts.map(p => ({ ...p, comment_count: counts[p.id] || 0 }));
  } catch (err) {
    console.error("addCommentCounts:", err.message);
    return posts;
  }
}

async function ensureIndexes(env, event) {
  try {
    const { results } = await env.DB.prepare(
      `SELECT name FROM sqlite_master WHERE type = 'index'`
    ).all();
    const have = new Set((results || []).map(r => r.name));
    if (REQUIRED_INDEXES.every(n => have.has(n)) && !have.has("idx_posts_deleted")) return;
    // Building an index reads the whole posts table (~2 rows read per post), so only do it in
    // the run just after the daily D1 limits reset at 00:00 UTC.
    if (new Date(event.scheduledTime).getUTCHours() !== 0) {
      console.log("ensureIndexes: indexes missing, will build in the 00:05 UTC run");
      return;
    }
    await env.DB.batch(INDEX_STATEMENTS.map(s => env.DB.prepare(s)));
    await env.DB.prepare(`PRAGMA optimize`).run();
    console.log("ensureIndexes: indexes applied");
  } catch (err) {
    console.error("ensureIndexes failed (will retry next hour):", err.message);
  }
}

// ── JWT ─────────────────────────────────────────────────────────────────────

async function signJWT(payload, secret) {
  const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const body   = btoa(JSON.stringify(payload));
  const data   = `${header}.${body}`;
  const key = await crypto.subtle.importKey(
    "raw", new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(data));
  const sigB64 = btoa(String.fromCharCode(...new Uint8Array(sig)))
    .replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
  return `${data}.${sigB64}`;
}

async function verifyJWT(token, secret) {
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  try {
    const key = await crypto.subtle.importKey(
      "raw", new TextEncoder().encode(secret),
      { name: "HMAC", hash: "SHA-256" }, false, ["verify"]
    );
    const pad = s => s + "=".repeat((4 - s.length % 4) % 4);
    const sigBytes = Uint8Array.from(
      atob(pad(parts[2].replace(/-/g, "+").replace(/_/g, "/"))),
      c => c.charCodeAt(0)
    );
    const valid = await crypto.subtle.verify(
      "HMAC", key, sigBytes, new TextEncoder().encode(`${parts[0]}.${parts[1]}`)
    );
    if (!valid) return null;
    const payload = JSON.parse(atob(pad(parts[1])));
    if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) return null;
    return payload;
  } catch { return null; }
}

// ── Password ─────────────────────────────────────────────────────────────────

async function hashPassword(password) {
  const enc = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveBits"]);
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const bits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", hash: "SHA-256", salt, iterations: 100000 },
    keyMaterial, 256
  );
  const toHex = b => Array.from(b).map(x => x.toString(16).padStart(2, "0")).join("");
  return toHex(salt) + ":" + toHex(new Uint8Array(bits));
}

async function verifyPassword(password, stored) {
  const [saltHex, hashHex] = stored.split(":");
  const salt = new Uint8Array(saltHex.match(/.{2}/g).map(b => parseInt(b, 16)));
  const enc = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", hash: "SHA-256", salt, iterations: 100000 },
    keyMaterial, 256
  );
  const toHex = b => Array.from(b).map(x => x.toString(16).padStart(2, "0")).join("");
  return toHex(new Uint8Array(bits)) === hashHex;
}

// ── Row helpers ───────────────────────────────────────────────────────────────

const POST_BOOL_FIELDS    = ["is_mod", "is_admin", "moderator", "deleted", "archived", "frozen", "pinned", "pinned_global", "locked", "is_huddle"];
const COMMENT_BOOL_FIELDS = ["is_mod", "is_admin", "moderator", "deleted", "pinned"];

const EXTINCT_NAME = "Extinct Bird";
const RESERVED_NAMES = new Set(["extinct bird", "__system__", "newsbot", "sciencebot", "naturebot", "sportsbot"]);

function boolify(row, fields) {
  if (!row) return row;
  const out = { ...row };
  for (const f of fields) if (f in out) out[f] = out[f] === 1 || out[f] === true;
  return out;
}

// ── Paged post lists ──────────────────────────────────────────────────────────
// The posts table holds every bot article ever posted, so list queries must never scan it.
// Pages run newest-first by rowid (insertion order) with a ?before=<rowid> cursor; the
// Flock/activity view sorts by last_activity, so its cursor is ?before=<last_activity>.

// D1 allows 100 bound values per query, and a busy account or chat has more ids than that, so a list
// goes in as one JSON value: IN (${ID_LIST}) with .bind(JSON.stringify(ids))
const ID_LIST = `SELECT value FROM json_each(?)`;
const LIVE_POSTS = `deleted = 0 AND (archived = 0 OR archived IS NULL) AND (is_huddle = 0 OR is_huddle IS NULL)`;
// Search alerts (saved searches with alert:true), cached per isolate for a minute
let ALERT_RULES = null, ALERT_RULES_AT = 0;
const ALERT_BOTS = ["NewsBot", "ScienceBot", "NatureBot", "SportsBot"];
const BOARD_NAMES = { general: "General", sports: "Sports", "science-nature": "Science", nature: "Nature", entertainment: "Entertainment", random: "Random", announcements: "Announcements", cage: "The Cage" };
// country/continent have no index: scan at most this many recent rows per page
const REGION_WINDOW = 4000;
// Each country's home region, matching the page's country list exactly. Every bot feed has a country
// (the outlet's home) and a region (what it covers): BBC Africa is United Kingdom + Africa.
const REGION_COUNTRIES = {
  "Europe": [
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia & Herzegovina", "Bulgaria", "Croatia", "Cyprus",
    "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hungary",
    "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta",
    "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal",
    "Romania", "Russia", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine",
    "United Kingdom"
  ],
  "Africa": [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Chad", "Congo",
    "DR Congo", "Egypt", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Kenya",
    "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique",
    "Namibia", "Niger", "Nigeria", "Rwanda", "Senegal", "Sierra Leone", "Somalia", "South Africa",
    "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
  ],
  "Asia": [
    "Afghanistan", "Armenia", "Azerbaijan", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "Hong Kong", "India",
    "Indonesia", "Japan", "Kazakhstan", "Kyrgyzstan", "Laos", "Malaysia", "Maldives", "Mongolia",
    "Myanmar", "Nepal", "North Korea", "Pakistan", "Philippines", "Singapore", "South Korea", "Sri Lanka",
    "Taiwan", "Tajikistan", "Thailand", "Turkmenistan", "Uzbekistan", "Vietnam"
  ],
  "North America": [
    "Bahamas", "Belize", "Canada", "Costa Rica", "Cuba", "Dominican Republic", "El Salvador", "Guatemala",
    "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Trinidad & Tobago", "United States"
  ],
  "Middle East": [
    "Bahrain", "Iran", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon", "Oman", "Palestine", "Qatar",
    "Saudi Arabia", "Syria", "Turkey", "United Arab Emirates", "Yemen"
  ],
  "South America": [
    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Paraguay", "Peru", "Uruguay",
    "Venezuela"
  ],
  "Australia/Oceania": [
    "Australia", "Fiji", "New Zealand", "Papua New Guinea"
  ],
};
const COUNTRY_REGION = Object.fromEntries(
  Object.entries(REGION_COUNTRIES).flatMap(([region, list]) => list.map(c => [c, region]))
);
// A post's region: its own tag, else its country's home region
const regionOf = p => p.continent || COUNTRY_REGION[p.country] || null;
// World desks (tagged "World") count for both World and their outlet's home region: BBC World shows in Europe too
const inRegion = (p, region) => regionOf(p) === region || (p.continent === "World" && COUNTRY_REGION[p.country] === region);
// Region tabs also show posts whose headline, description or text names the region or one of its
// countries, so a BBC story about Kenya shows under Africa. Whole words, exact case, never the link.
const REGION_WORDS = {
  "Africa": ["Africa"], "Europe": ["Europe"], "Asia": ["Asia"], "Middle East": ["Middle East"],
  "North America": ["North America"], "South America": ["South America", "Latin America"],
  "Australia/Oceania": ["Oceania"]
};
// Names that mostly mean something else (US state, people, Thanksgiving) are left to tags
const NAME_SKIP = new Set(["Georgia", "Jordan", "Chad", "Turkey"]);
// How headlines write a country, when that differs from its pill name
const NAME_AS = { "Bosnia & Herzegovina": ["Bosnia"], "Trinidad & Tobago": ["Trinidad"], "Turkey": ["Türkiye"] };
// Pattern pieces for a name; Guinea skips "Papua New Guinea"
const namePiece = n => n === "Guinea" ? "(?<!New )Guinea" : n.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const regionTerms = region => [
  ...(REGION_WORDS[region] || []),
  ...(REGION_COUNTRIES[region] || []).flatMap(c => NAME_AS[c] || (NAME_SKIP.has(c) ? [] : [c]))
];
// A country pill uses the same rule for its own name (skipped names included: the pill asked for it)
const countryTerms = country => [...new Set([country, ...(NAME_AS[country] || [])])];
const namePatterns = new Map();
function namesPattern(key, terms) {
  if (!namePatterns.has(key)) {
    namePatterns.set(key, new RegExp(`(?<![\\p{L}\\p{N}])(?:${terms.map(namePiece).join("|")})(?![\\p{L}\\p{N}])`, "u"));
  }
  return namePatterns.get(key);
}
const regionWordPattern = region => namesPattern(`r:${region}`, regionTerms(region));
const countryNamePattern = country => namesPattern(`c:${country}`, countryTerms(country));
// Rows whose title or text may contain one of the names (LIKE ignores case; the pattern decides)
const MAYBE_NAMES = `EXISTS (SELECT 1 FROM json_each(?) WHERE (COALESCE(title, '') || ' ' || COALESCE(content, '')) LIKE '%' || value || '%')`;
// Headline, description and any text a person typed. Never the link or image URL.
function readableText(post) {
  const content = post.content || "";
  const parts = [post.title || "", content.split("[ATTACH")[0]];
  const attach = content.match(/\[ATTACH:(\{.*\})\]/s);
  if (attach) {
    try {
      const { title, description } = JSON.parse(attach[1]);
      parts.push(title || "", description || "");
    } catch { /* malformed attachment: use the rest */ }
  }
  return parts.join(" ");
}
// A country pill keeps to that country's home region, so BBC Africa stays out of the UK pill.
// World desks (NYT World, BBC World...) are tagged "World", which is no other region, so they stay in.
const inHomeRegion = (p, country) =>
  p.country === country && (!p.continent || p.continent === "World" || !COUNTRY_REGION[country] || p.continent === COUNTRY_REGION[country]);
const regionWhere = region => ({
  sql: `(continent = ? OR ((continent IS NULL OR continent = 'World') AND country IN (${ID_LIST})))`,
  params: [region, JSON.stringify(REGION_COUNTRIES[region] || [])]
});
const countryWhere = country => COUNTRY_REGION[country]
  ? { sql: `(country = ? AND (continent IS NULL OR continent = 'World' OR continent = ?))`, params: [country, COUNTRY_REGION[country]] }
  : { sql: `country = ?`, params: [country] };

function boardVariants(board) {
  const lower = board.trim().toLowerCase();
  const slug = Object.keys(BOARD_NAMES).find(k => k === lower || BOARD_NAMES[k].toLowerCase() === lower);
  return [...new Set([board.trim(), lower, ...(slug ? [slug, BOARD_NAMES[slug]] : [])])];
}

function usernameVariants(username) {
  const lower = username.trim().toLowerCase();
  return [...new Set([username.trim(), lower, lower.charAt(0).toUpperCase() + lower.slice(1)])];
}

async function getPostsPage(env, { activity, board, continent, country, username, before, limit }) {
  const boards = board ? boardVariants(board) : null;
  const users = username ? usernameVariants(username) : null;
  const boardSet = boards && new Set(boards.map(b => b.toLowerCase()));
  const userSet = users && new Set(users.map(u => u.toLowerCase()));
  const matchesBoardAndUser = p =>
    (!boardSet || boardSet.has((p.board || "").toLowerCase())) &&
    (!userSet || userSet.has((p.username || "").toLowerCase()));
  const matches = p =>
    matchesBoardAndUser(p) &&
    (!continent || inRegion(p, continent)) &&
    (!country || inHomeRegion(p, country));
  const page = posts => posts.map(p => boolify(p, POST_BOOL_FIELDS));

  if (activity) {
    // Flock: posts by people, plus bot posts that have comments — both small sets
    const cond = [LIVE_POSTS];
    const params = [];
    if (before) { cond.push("last_activity < ?"); params.push(before); }
    const where = cond.join(" AND ");
    const [commented, human, shared] = await Promise.all([
      env.DB.prepare(
        `SELECT rowid AS _rid, * FROM posts WHERE id IN (SELECT post_id FROM comments WHERE deleted = 0) AND ${where} ORDER BY last_activity DESC LIMIT ?`
      ).bind(...params, limit).all(),
      // INDEXED BY fails fast instead of scanning every post if the index is missing
      env.DB.prepare(
        `SELECT rowid AS _rid, * FROM posts INDEXED BY idx_posts_human_activity WHERE ${HUMAN_POSTS} AND ${where} ORDER BY last_activity DESC LIMIT ?`
      ).bind(...params, limit).all().catch(err => {
        console.error("get-posts activity: human posts unavailable:", err.message);
        return { results: [] };
      }),
      // Shared posts (a share counts as activity, so a shared news story shows up in Flock)
      env.DB.prepare(
        `SELECT rowid AS _rid, * FROM posts WHERE id IN (SELECT post_id FROM post_shares) AND ${where} ORDER BY last_activity DESC LIMIT ?`
      ).bind(...params, limit).all().catch(() => ({ results: [] }))
    ]);
    const c = commented.results || [], h = human.results || [], s = shared.results || [];
    const byId = new Map([...h, ...c, ...s].map(p => [p.id, p]));
    const scanned = [...byId.values()]
      .sort((a, b) => String(b.last_activity || "").localeCompare(String(a.last_activity || "")))
      .slice(0, limit);
    const more = c.length === limit || h.length === limit || s.length === limit;
    return { posts: page(scanned.filter(matches)), next_before: more && scanned.length ? scanned[scanned.length - 1].last_activity : null };
  }

  const cursor = before ? parseInt(before, 10) : null;
  if (before && !Number.isFinite(cursor)) return { posts: [], next_before: null };
  const below = cursor ? " AND rowid < ?" : "";
  const belowParams = cursor ? [cursor] : [];

  if ((continent || country) && !users) {
    // Scan a bounded window of recent rows (light columns only), then load the matching posts.
    // A region tab also flags rows that may name the region (LIKE ignores case; the pattern decides).
    const words = continent && !country ? regionTerms(continent) : [];
    const maybe = words.length
      ? `, ${MAYBE_NAMES} AS _m`
      : "";
    const { results: win = [] } = await env.DB.prepare(
      `SELECT rowid AS _rid, board, username, continent, country${maybe} FROM posts WHERE ${LIVE_POSTS}${below} ORDER BY rowid DESC LIMIT ?`
    ).bind(...(words.length ? [JSON.stringify(words)] : []), ...belowParams, REGION_WINDOW).all();
    const hits = win.filter(p => matches(p) || (p._m && matchesBoardAndUser(p))).slice(0, limit);
    let posts = [];
    if (hits.length) {
      const { results = [] } = await env.DB.prepare(
        `SELECT rowid AS _rid, * FROM posts WHERE rowid IN (${hits.map(() => "?").join(",")}) ORDER BY rowid DESC`
      ).bind(...hits.map(p => p._rid)).all();
      posts = words.length ? results.filter(p => matches(p) || regionWordPattern(continent).test(readableText(p))) : results;
    }
    const next_before = hits.length === limit ? hits[hits.length - 1]._rid
      : win.length === REGION_WINDOW ? win[win.length - 1]._rid : null;
    return { posts: page(posts), next_before };
  }

  // Indexed lookups: by username if given (most selective), else by board, else plain rowid order
  const [col, values] = users ? ["username", users] : boards ? ["board", boards] : [null, [null]];
  const lists = await Promise.all(values.map(v =>
    env.DB.prepare(
      `SELECT rowid AS _rid, * FROM posts WHERE ${col ? `${col} = ? AND ` : ""}${LIVE_POSTS}${below} ORDER BY rowid DESC LIMIT ?`
    ).bind(...(col ? [v] : []), ...belowParams, limit).all().then(r => r.results || [])
  ));
  const byId = new Map(lists.flat().map(p => [p.id, p]));
  const scanned = [...byId.values()].sort((a, b) => b._rid - a._rid).slice(0, limit);
  const more = lists.some(l => l.length === limit);
  return { posts: page(scanned.filter(matches)), next_before: more && scanned.length ? scanned[scanned.length - 1]._rid : null };
}


// ── Main ──────────────────────────────────────────────────────────────────────

async function handleRequest(request, env, ctx, corsHeaders) {
  const url = new URL(request.url);

  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  // IP addresses are never stored. Mods can match the same address for bans through a keyed hash: with the
  // secret IP_HASH_KEY it can't be turned back into an address (a plain hash could, by trying all 4 billion).
  const ip = request.headers.get("CF-Connecting-IP") || "0.0.0.0";
  let ip_hash = null;
  if (env.IP_HASH_KEY) {
    const hk = await crypto.subtle.importKey("raw", new TextEncoder().encode(env.IP_HASH_KEY), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
    const sig = await crypto.subtle.sign("HMAC", hk, new TextEncoder().encode(ip));
    ip_hash = Array.from(new Uint8Array(sig)).map(b => b.toString(16).padStart(2, "0")).join("");
  }

  const body = (request.method !== "GET" && request.method !== "HEAD" && url.pathname !== "/upload") ? await request.json().catch(() => ({})) : {};
  const now = new Date().toISOString();
  // Strip ":admin"/":mod" role suffix stored by frontend — return plain username
  const normMember = m => { const ci = (m || "").lastIndexOf(":"); if (ci > 0) { const r = m.slice(ci + 1); if (r === "admin" || r === "mod") return m.slice(0, ci); } return m || ""; };
  const isHuddleMember = (post, name) => {
    if (!name) return false;
    const lower = name.toLowerCase();
    if (lower === (post.username || post.owner || "").toLowerCase()) return true;
    return JSON.parse(post.huddle_members || "[]").some(m => normMember(m).toLowerCase() === lower);
  };
  const huddleLine = (post_id, text, when) => env.DB.prepare(
    `INSERT INTO comments (id, content, post_id, parent_comment_id, username, ip_hash, browser_id, is_mod, is_admin, moderator, mod_user_id, created_at) VALUES (?, ?, ?, NULL, '__system__', NULL, NULL, 0, 0, 0, NULL, ?)`
  ).bind(crypto.randomUUID(), text, post_id, when).run().catch(() => {});
  // A huddle outlives its creator: it passes to the longest-standing member, and only ends if nobody's left
  const passHuddleOn = async (post, when) => {
    const members = JSON.parse(post.huddle_members || "[]");
    if (!members.length) {
      await env.DB.prepare(`UPDATE posts SET deleted = 1 WHERE id = ?`).bind(post.id).run();
      return null;
    }
    const next = normMember(members[0]);
    await env.DB.prepare(`UPDATE posts SET username = ?, browser_id = NULL, mod_user_id = NULL, is_mod = 0, is_admin = 0, moderator = 0, huddle_members = ? WHERE id = ?`)
      .bind(next, JSON.stringify(members.slice(1)), post.id).run();
    await huddleLine(post.id, `👑 ${next} now runs the huddle`, when);
    await upsertNotif(next, JSON.stringify({ text: `You now run "${post.title || "Huddle"}"`, postId: post.id }), post.id);
    // Requests waiting on the old owner now wait on the new one
    const { results: waiting = [] } = await env.DB.prepare(
      `SELECT * FROM huddle_requests WHERE post_id = ? AND status = 'pending' AND kind IN ('add', 'remove') AND created_at > ?`
    ).bind(post.id, requestCutoff()).all().catch(() => ({ results: [] }));
    for (const rq of waiting) await upsertNotif(next, requestMessage(rq, post), post.id);
    return next;
  };

  // ── Huddle invitations and requests ──
  // invite: someone is asked to join (they accept or decline).
  // add / remove: a member asks the owner to invite or remove someone (the owner approves or denies).
  // Nothing changes until it's answered; unanswered requests expire after 7 days.
  const REQUEST_DAYS = 7;
  // Notification rows (ids) for invitations / requests this bird still has to answer
  const waitingOn = async name => {
    const { results: rows = [] } = await env.DB.prepare(`SELECT id, message FROM system_notifications WHERE user_id = ? AND message LIKE '%"req":"%'`).bind(name).all();
    const byReq = new Map();
    for (const r of rows) { try { const q = JSON.parse(r.message).req; if (q) byReq.set(r.id, q); } catch {} }
    if (!byReq.size) return [];
    const { results: rqs = [] } = await env.DB.prepare(
      `SELECT r.id, r.kind, r.target, p.username AS owner FROM huddle_requests r JOIN posts p ON p.id = r.post_id AND p.deleted = 0 WHERE r.id IN (${ID_LIST}) AND r.status = 'pending' AND r.created_at > ?`
    ).bind(JSON.stringify([...new Set(byReq.values())]), requestCutoff()).all();
    const lower = name.toLowerCase();
    const live = new Set(rqs.filter(r => (r.kind === "invite" ? r.target : r.owner || "").toLowerCase() === lower).map(r => r.id));
    return [...byReq].filter(([, q]) => live.has(q)).map(([id]) => id);
  };
  function requestCutoff() { return new Date(Date.now() - REQUEST_DAYS * 864e5).toISOString(); }
  function requestMessage(rq, post) {
    const title = post.title || "Huddle";
    const text = rq.kind === "invite" ? `${rq.from_user} invited you to "${title}"`
      : rq.kind === "add" ? `${rq.from_user} wants to invite ${rq.target} to "${title}"`
      : `${rq.from_user} wants to remove ${rq.target} from "${title}"`;
    return JSON.stringify({ text, postId: post.id, req: rq.id, ...(rq.preview ? { preview: rq.preview } : {}) });
  }
  // First line of the huddle's opening (oldest pinned) chirp, for invites
  const huddlePreview = async postId => {
    const row = await env.DB.prepare(`SELECT content FROM comments WHERE post_id = ? AND pinned = 1 AND deleted = 0 AND username != '__system__' ORDER BY created_at LIMIT 1`).bind(postId).first().catch(() => null);
    if (!row) return null;
    const raw = String(row.content || ""), cut = raw.search(/\n\n\[ATTACH/);
    let text = (cut >= 0 ? raw.slice(0, cut) : raw).replace(/\s+/g, " ").trim();
    if (!text && cut >= 0) {
      const tail = raw.slice(cut);
      if (/"type":"video"/.test(tail)) text = "🎬 Video";
      else if (/"type":"image"/.test(tail)) text = "📷 Photo";
      else {
        let label = "";
        try {
          const att = JSON.parse(tail.slice(tail.indexOf(":") + 1, tail.lastIndexOf("]")));
          label = String(att.title || "").trim() || new URL(att.url).hostname.replace(/^www\./, "");
        } catch {}
        text = "🔗 " + (label || "Link");
      }
    }
    return text ? (text.length > 80 ? text.slice(0, 79).trimEnd() + "…" : text) : null;
  };
  const accountRole = async name => {
    const row = await env.DB.prepare(`SELECT role FROM mod_users WHERE LOWER(username) = ? AND deleted_at IS NULL LIMIT 1`).bind(String(name).toLowerCase()).first();
    return row && (row.role === "admin" || row.role === "mod") ? row.role : null;
  };
  const pendingRequest = (postId, kind, target) => env.DB.prepare(
    `SELECT * FROM huddle_requests WHERE post_id = ? AND kind = ? AND LOWER(target) = ? AND status = 'pending' AND created_at > ? LIMIT 1`
  ).bind(postId, kind, String(target).toLowerCase(), requestCutoff()).first();
  const newRequest = async (post, kind, from, target, role) => {
    const rq = { id: crypto.randomUUID(), post_id: post.id, kind, from_user: from, target, target_role: role || null, status: "pending", created_at: now };
    if (kind === "invite") rq.preview = await huddlePreview(post.id);
    await env.DB.prepare(`INSERT INTO huddle_requests (id, post_id, kind, from_user, target, target_role, status, created_at) VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)`)
      .bind(rq.id, post.id, kind, from, target, rq.target_role, now).run();
    await upsertNotif(kind === "invite" ? target : post.username, requestMessage(rq, post), post.id);
    return rq;
  };
  // Invite someone (no-op if they're already in or already invited)
  const sendInvite = async (post, from, target) => {
    if (isHuddleMember(post, target) || await pendingRequest(post.id, "invite", target)) return null;
    return newRequest(post, "invite", from, target, await accountRole(target));
  };
  // Deleting keeps the password and the list of huddles left, so an admin can bring the account back
  const retireAccount = async (account, when, by) => {
    const name = account.username;
    const left = [];
    if (name) {
      const { results } = await env.DB.prepare(
        `SELECT * FROM posts INDEXED BY idx_posts_huddles WHERE is_huddle = 1 AND deleted = 0 AND (username = ? OR huddle_members LIKE ?)`
      ).bind(name, `%"${name}%`).all();
      for (const huddle of results || []) {
        if ((huddle.username || "").toLowerCase() === name.toLowerCase()) {
          await huddleLine(huddle.id, `👋 ${name} left the huddle`, when); // shows as Extinct Bird until they come back
          left.push({ id: huddle.id, ended: !await passHuddleOn(huddle, when) });
        } else {
          const members = JSON.parse(huddle.huddle_members || "[]");
          const rest = members.filter(m => normMember(m).toLowerCase() !== name.toLowerCase());
          if (rest.length === members.length) continue;
          await env.DB.prepare(`UPDATE posts SET huddle_members = ? WHERE id = ?`).bind(JSON.stringify(rest), huddle.id).run();
          await huddleLine(huddle.id, `👋 ${name} left the huddle`, when); // shows as Extinct Bird until they come back
          left.push({ id: huddle.id });
        }
      }
    }
    await env.DB.prepare(`UPDATE mod_users SET deleted_at = ?, deleted_by = ?, left_huddles = ? WHERE id = ?`)
      .bind(when, by, JSON.stringify(left), account.id).run();
  };
  const restoreAccount = async (account, when) => {
    const name = account.username;
    for (const spot of JSON.parse(account.left_huddles || "[]")) {
      const huddle = await env.DB.prepare(`SELECT * FROM posts WHERE id = ? AND is_huddle = 1`).bind(spot.id).first();
      if (!huddle) continue;
      if (spot.ended && huddle.deleted && huddle.username === name) {
        await env.DB.prepare(`UPDATE posts SET deleted = 0 WHERE id = ?`).bind(spot.id).run();
        continue;
      }
      if (huddle.deleted || isHuddleMember(huddle, name)) continue;
      const members = JSON.parse(huddle.huddle_members || "[]");
      members.push(name);
      await env.DB.prepare(`UPDATE posts SET huddle_members = ? WHERE id = ?`).bind(JSON.stringify(members), spot.id).run();
      await huddleLine(spot.id, `👋 ${name} is back in the huddle`, when);
    }
    await env.DB.prepare(`UPDATE mod_users SET deleted_at = NULL, deleted_by = NULL, left_huddles = NULL WHERE id = ?`).bind(account.id).run();
  };

  // Upsert a notification.
  // Comment notifications carry dk:"comment" and deduplicate with each other (one rolling notif per post).
  // Member notifications (added, invited, left) have no dk field and always create a fresh entry.
  async function upsertNotif(userId, message, postId) {
    const isComment = message.includes('"dk":"comment"');
    if (postId && isComment) {
      const existing = await env.DB.prepare(
        `SELECT id FROM system_notifications WHERE user_id = ? AND message LIKE ? AND message LIKE ? LIMIT 1`
      ).bind(userId, `%"postId":"${postId}"%`, '%"dk":"comment"%').first();
      if (existing) {
        await env.DB.prepare(`UPDATE system_notifications SET message = ?, created_at = ? WHERE id = ?`)
          .bind(message, now, existing.id).run().catch(() => {});
        return;
      }
    }
    await env.DB.prepare(`INSERT INTO system_notifications (id, user_id, message) VALUES (?, ?, ?)`)
      .bind(crypto.randomUUID(), userId, message).run();
  }

  // ── Search alerts ── a new post is checked against every saved search with its bell on (same rules as the
  // search bar). Each alert keeps ONE notification that counts up ("3 new posts"); once read, the next match
  // starts it again at 1. Not your own posts, huddles or The Cage; birds' posts are checked after the AI check.
  async function loadAlertRules() {
    if (ALERT_RULES && Date.now() - ALERT_RULES_AT < 60000) return ALERT_RULES;
    const { results = [] } = await env.DB.prepare(`SELECT username, saved_searches FROM mod_users WHERE deleted_at IS NULL AND username IS NOT NULL AND saved_searches LIKE '%"alert":true%'`).all();
    const rules = [];
    for (const r of results) {
      let items = [];
      try { items = JSON.parse(r.saved_searches || "[]"); } catch (e) {}
      for (const it of Array.isArray(items) ? items : []) if (it && it.alert && it.qs) rules.push({ who: r.username, qs: it.qs, p: new URLSearchParams(it.qs) });
    }
    ALERT_RULES = rules; ALERT_RULES_AT = Date.now();
    return rules;
  }
  function alertMatches(post, p) {
    const bot = ALERT_BOTS.includes(post.username) || String(post.browser_id || "").startsWith("bot-");
    if (p.get("flock") === "1" && bot) return false;
    const b = (p.get("board") || "").toLowerCase();
    if (b === "botnews") { if (!bot) return false; }
    else if (b === "activity") { if (bot) return false; }
    else if (b) {
      const v = boardVariants(b).map(x => x.toLowerCase());
      if (!v.includes(String(post.board || "").toLowerCase()) && !v.includes(String(post.community_id || "").toLowerCase())) return false;
    }
    const bf = p.get("bot");
    if (bf === "hide" && bot) return false;
    if (bf && bf !== "hide" && !bot) return false;
    const ut = (p.get("utag") || "").toLowerCase();
    if (ut && (post.utag || "") !== ut) return false;
    const us = (p.get("user") || "").toLowerCase();
    if (us && String(post.username || "").toLowerCase() !== us) return false;
    const country = p.get("country") || "", region = p.get("continent") || "", q = (p.get("q") || "").trim();
    const text = readableText(post);
    if (country && q && q.toLowerCase() === country.toLowerCase()) {
      // a country pill searching its own name: the country's posts, or ones that name it
      if (!inHomeRegion(post, country) && !countryNamePattern(country).test(text)) return false;
    } else {
      if (country && !inHomeRegion(post, country)) return false;
      if (q && !text.toLowerCase().includes(q.toLowerCase())) return false;
    }
    if (region && !country && !inRegion(post, region)) return false;
    return true;
  }
  async function alertNotify(who, qs, post) {
    const row = await env.DB.prepare(`SELECT id, message, created_at FROM system_notifications WHERE user_id = ? AND message LIKE ? ORDER BY created_at DESC LIMIT 1`)
      .bind(who, `%"alert":${JSON.stringify(qs).replace(/[%_]/g, "_")}%`).first().catch(() => null);
    let n = 1;
    if (row) {
      let old = {};
      try { old = JSON.parse(row.message); } catch (e) {}
      if (old.alert === qs) {
        const [rd, st] = await Promise.all([
          env.DB.prepare(`SELECT notif_time FROM notif_reads WHERE user_key = ? AND notif_id = ?`).bind(who, `hsys-${row.id}`).first(),
          env.DB.prepare(`SELECT seen_at FROM notif_state WHERE user_key = ?`).bind(who).first(),
        ]);
        const read = (rd && rd.notif_time >= row.created_at) || (st && st.seen_at && st.seen_at >= row.created_at);
        if (!read) n = (old.n || 1) + 1;
      }
    }
    const title = readableText(post).replace(/\s+/g, " ").trim().slice(0, 90);
    const msg = JSON.stringify({ text: `${n} new post${n === 1 ? "" : "s"} for your saved search`, icon: "SEARCH", alert: qs, n, link: `/?${qs}`, preview: title || undefined });
    if (row) await env.DB.prepare(`UPDATE system_notifications SET message = ?, created_at = ? WHERE id = ?`).bind(msg, now, row.id).run();
    else await env.DB.prepare(`INSERT INTO system_notifications (id, user_id, message, created_at) VALUES (?, ?, ?, ?)`).bind(crypto.randomUUID(), who, msg, now).run();
  }
  async function checkAlerts(postOrId) {
    try {
      const rules = await loadAlertRules();
      if (!rules.length) return;
      let post = postOrId;
      if (typeof postOrId === "string") post = await env.DB.prepare(`SELECT id, title, content, username, browser_id, board, community_id, continent, country, utag, is_huddle, deleted FROM posts WHERE id = ?`).bind(postOrId).first();
      if (!post || post.deleted || post.is_huddle) return;
      if (["cage", "the cage"].includes(String(post.community_id || post.board || "").toLowerCase())) return;
      const by = String(post.username || "").toLowerCase(), done = new Set();
      for (const r of rules) {
        if (String(r.who).toLowerCase() === by) continue;
        const k = r.who + "\n" + r.qs;
        if (done.has(k) || !alertMatches(post, r.p)) continue;
        done.add(k);
        await alertNotify(r.who, r.qs, post).catch(e => console.error("alertNotify", e.message));
      }
    } catch (e) { console.error("checkAlerts", e.message); }
  }

  // @tags in a post or chirp: notify each tagged bird (up to 5 per post/chirp) that exists and can see it.
  // Huddles: members only. Not yourself, not extinct birds, and nothing from caged birds. The notification
  // opens the post, or jumps to the chirp (targetId -> /post/<id>?highlight=<chirp id>).
  async function notifyMentions({ by, text, postId, commentId }) {
    try {
      if (!by || !postId) return;
      const raw = String(text || "");
      const me = by.toLowerCase();
      const names = [...new Set([...raw.matchAll(/(^|[^\w@])@([a-z][a-z0-9-]{1,40})/gi)].map(m => m[2].toLowerCase()))].filter(n => n !== me).slice(0, 5);
      if (!names.length) return;
      if (!isModerator && await isJailed()) return;
      const { results = [] } = await env.DB.prepare(`SELECT username FROM mod_users WHERE lower(username) IN (${names.map(() => "?").join(",")}) AND deleted_at IS NULL`).bind(...names).all();
      if (!results.length) return;
      const post = await env.DB.prepare(`SELECT is_huddle, huddle_members, username FROM posts WHERE id = ?`).bind(postId).first();
      if (!post) return;
      const extinct = await extinctNames();
      const preview = raw.replace(/\s+/g, " ").trim().slice(0, 80);
      for (const { username: who } of results) {
        if (!who || extinct.has(who)) continue;
        if (post.is_huddle && !isHuddleMember(post, who)) continue;
        const onYours = commentId && (post.username || "").toLowerCase() === who.toLowerCase();
        const msg = JSON.stringify({ text: `${by} tagged you in ${commentId ? (onYours ? "a chirp on your post" : "a chirp") : "a post"}`, postId, targetId: commentId || undefined, preview, icon: "AT" });
        await env.DB.prepare(`INSERT INTO system_notifications (id, user_id, message) VALUES (?, ?, ?)`).bind(crypto.randomUUID(), who, msg).run();
      }
    } catch (e) { console.error("notifyMentions", e); }
  }

  // Other people's browser IDs go out scrambled (same scramble each time, so grouping still works);
  // your own (sent as ?bid=) comes back as is, so the page can tell which votes/reactions are yours.
  async function maskBid(id, mine) {
    if (!id) return id;
    if (mine && id === mine) return id;
    const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(env.IP_HASH_KEY || env.JWT_SECRET || "pp"), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
    const s = new Uint8Array(await crypto.subtle.sign("HMAC", k, new TextEncoder().encode("bid:" + id)));
    return "x" + Array.from(s.slice(0, 12)).map(b => b.toString(16).padStart(2, "0")).join("");
  }

  // Unexpected errors: details go to the server log, people just see a plain message
  function serverError(err) {
    console.error("server error:", err && (err.stack || err.message));
    return json({ error: "Something went wrong. Please try again." }, 500);
  }

  function json(data, status = 200) {
    return new Response(JSON.stringify(data), {
      status,
      headers: { ...corsHeaders, "Content-Type": "application/json" }
    });
  }

  // ── Auth ────────────────────────────────────────────────────────────────────

  async function getAuthUser() {
    const authHeader = request.headers.get("Authorization");
    if (!authHeader?.startsWith("Bearer ")) return null;
    const token = authHeader.slice(7);
    const user = await verifyJWT(token, env.JWT_SECRET);
    if (user?.sub) {
      const account = await env.DB.prepare(`SELECT deleted_at, see_all_huddles, role, password_changed_at FROM mod_users WHERE id = ?`).bind(user.sub).first();
      if (!account || account.deleted_at) return null;
      // A password change signs out every login made before it
      if (account.password_changed_at && (!user.iat || user.iat * 1000 < Date.parse(account.password_changed_at))) return null;
      // The role always comes from the account, so promotions and demotions apply immediately
      user.role = account.role || "user";
      user.see_all_huddles = !!account.see_all_huddles;
      const now = new Date().toISOString();
      ctx.waitUntil(
        env.DB.prepare("UPDATE mod_users SET last_active = ? WHERE id = ?")
          .bind(now, user.sub).run()
      );
    }
    return user;
  }

  const botKey = request.headers.get("x-bot-key");
  const isBot = !!(botKey && env.BOT_KEY && botKey === env.BOT_KEY);

  const authUser = await getAuthUser();
  const isAdmin = authUser?.role === "admin";
  const isModerator = authUser?.role === "mod" || authUser?.role === "admin";
  // Only admins who switched it on in the mod panel can see and open huddles they aren't in; mods can't
  const seeAllHuddles = isAdmin && !!authUser?.see_all_huddles;
  const isMember = false; // members are anonymous for now

  // Who is asking comes from the login token only, never from a name or browser id in the request:
  // browser ids are public in every response, so they prove nothing. Signed out, username is null.
  let username = null;
  if (isBot) {
    username = (typeof body.username === "string" && body.username.trim()) || "NewsBot";
  } else if (isModerator) {
    username = authUser.username || "Mod";
  } else if (authUser) {
    username = authUser.username || null;
  }
  const signInRequired = () => json({ error: "Sign in required" }, 401);
  // Deleted accounts show as Extinct Bird everywhere. Real names only appear in the Mod Panel's own data.
  let extinct = null;
  const extinctNames = async () => {
    if (!extinct) {
      const { results } = await env.DB.prepare(`SELECT username FROM mod_users WHERE deleted_at IS NOT NULL`).all();
      extinct = new Set((results || []).map(r => r.username));
    }
    return extinct;
  };
  const scrubNames = (text, names) => {
    if (typeof text !== "string") return text;
    for (const name of names) {
      if (text.includes(name)) text = text.replace(new RegExp(`(?<![\\w-])${name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?![\\w-])`, "g"), EXTINCT_NAME);
    }
    return text;
  };
  // ip_hash is for mods handling bans, so public responses leave it out
  const publicRows = async rows => {
    const names = await extinctNames();
    return rows.map(({ ip_hash, ...visible }) => {
      const row = isModerator ? { ...visible, ip_hash } : visible;
      if (row.username === "__system__") return { ...row, content: scrubNames(row.content, names) };
      return names.has(row.username) ? { ...row, username: EXTINCT_NAME, browser_id: null, is_mod: false, moderator: false, mod_user_id: null } : row;
    });
  };

  // ── D1 helpers ───────────────────────────────────────────────────────────────

  // Site switches (mod panel → Flock). signup_limit: off (unlimited) | day | week — 4 new accounts per network
  const SIGNUP_CAP = 4, SIGNUP_WINDOWS = { day: 86400000, week: 7 * 86400000 };
  async function siteSetting(key, dflt) {
    try { return (await env.DB.prepare(`SELECT value FROM site_settings WHERE key = ?`).bind(key).first())?.value ?? dflt; } catch { return dflt; }
  }

  // ── Content checks (public posts and chirps from members; not bots, mods, huddles or DMs) ──────────
  // 1. Slurs are refused outright. Swearing is fine ("fuck", "cunt" etc. are never blocked): only words that
  //    are hate slurs. Catches look-alike spellings (n1gg3r), stretched letters and spaced-out letters.
  // 2. With the "AI check" switch on (mod panel → Settings), Llama Guard reads each one right after it's
  //    posted. If it's flagged for hate, threats or sexual abuse, the post/chirp is hidden, the bird goes to
  //    The Cage, and mods get a notification. Mod panel → Flagged: "Not bad" undoes both, "Confirm" keeps them.
  const userText = (...parts) => parts.map(p => String(p || "").split(/\s*\[ATTACH/)[0]).join("\n").trim();
  // ── User tags (#biking) ── one word: 2–20 letters/numbers, no emoji or spaces, no swearing or slurs (tags are
  // public labels anyone can browse, so unlike posts, swearing is blocked here), not on the admin's blocked list.
  const TAG_BAD_ANY = /fuck|shit|cunt|bitch|whore|slut|twat|nigg|fagg|retard|porn|dildo|jizz|pussy|bastard|bollock|asshole|dickhead|cocksuck|motherf/;
  const TAG_BAD_WORD = /^(?:rape\w*|rapist\w*|wank\w*|piss\w*|cock|cocks|dick|dicks|ass|arse|tits|cum|nazis?|penis|vagina|boobs?|fag|fags|hoe|hoes)$/;
  async function cleanTag(raw) {
    const t = String(raw || "").trim().replace(/^#+/, "").toLowerCase();
    if (!t) return { tag: null };
    if (!/^[a-z0-9]{2,20}$/.test(t)) return { error: "A tag is one word: 2–20 letters or numbers, no spaces, symbols or emoji" };
    if (TAG_BAD_ANY.test(t) || TAG_BAD_WORD.test(t) || hasSlur(t)) return { error: "That tag isn't allowed" };
    if (await env.DB.prepare(`SELECT 1 FROM blocked_tags WHERE tag = ?`).bind(t).first()) return { error: "That tag isn't allowed" };
    return { tag: t };
  }
  const setPostTag = async (postId, tag, createdAt) => {
    await env.DB.batch([
      env.DB.prepare(`UPDATE posts SET utag = ? WHERE id = ?`).bind(tag, postId),
      env.DB.prepare(`DELETE FROM post_tags WHERE post_id = ?`).bind(postId),
      ...(tag ? [env.DB.prepare(`INSERT INTO post_tags (tag, post_id, created_at) VALUES (?, ?, ?)`).bind(tag, postId, createdAt)] : []),
    ]);
  };
  const SLUR_WORD = /^(?:n+i+g{2,}(?:e+r+|a+h?|u+h+)[sz]?|kikes?|spics?|wetbacks?|gooks?|ragheads?|towelheads?|jigaboos?|zipperheads?|beaners?|pakis?|dark(?:ie|y)s?|fagg?ots?|boongs?)$/;
  const SLUR_PAIR = /^(?:porchmonkeys?|sandn+i+g{2,}(?:e+r+|a+h?)[sz]?)$/;
  function hasSlur(text) {
    let t = String(text || "").normalize("NFKD").replace(/[̀-ͯ​-‏⁠﻿]/g, "").toLowerCase();
    t = t.replace(/[0]/g, "o").replace(/[1!|]/g, "i").replace(/3/g, "e").replace(/[4@]/g, "a").replace(/[5$]/g, "s").replace(/7/g, "t");
    t = t.replace(/([a-z])\1{2,}/g, "$1$1");
    const words = t.split(/[^a-z]+/).filter(Boolean);
    for (let i = 0; i < words.length; i++) {
      if (SLUR_WORD.test(words[i])) return true;
      if (i + 1 < words.length && SLUR_PAIR.test(words[i] + words[i + 1])) return true;
    }
    // s p a c e d / d.o.t.t.e.d letters
    let run = "";
    for (const w of [...words, ""]) {
      if (w.length === 1) { run += w; continue; }
      if (run.length >= 4 && (SLUR_WORD.test(run) || SLUR_PAIR.test(run))) return true;
      run = "";
    }
    return false;
  }
  // Photos, videos and GIFs in a post or chirp (uploaded files live under /media/). Caged birds can't post them.
  const hasMedia = text => /\[ATTACHMENTS:|\[ATTACH:\s*\{\s*"type"\s*:\s*"(?:image|images|video|gif)"|\/media\//.test(String(text || ""));
  const CAGED_MEDIA = "You’re Caged! Caged birds can't post photos or videos.";
  const SLUR_MSG = "That has a slur in it, so it wasn't posted. Swearing is fine here, slurs aren't.";
  const AI_FLAG_CATS = { S1: "violent threats", S3: "sex crimes", S4: "child sexual abuse", S9: "weapons of mass harm", S10: "hate speech" };
  async function aiCheck({ kind, id, postId, text, uname, bid }) {
    try {
      if (!env.AI || !text || text.length < 2) return;
      if ((await siteSetting("ai_check", "off")) !== "on") return;
      const r = await env.AI.run("@cf/meta/llama-guard-3-8b", { messages: [{ role: "user", content: text.slice(0, 4000) }] });
      let cats = [];
      if (r && typeof r.response === "object" && r.response) { if (r.response.safe === false) cats = r.response.categories || []; }
      else { const m = String(r?.response || "").trim().match(/^unsafe\b([\s\S]*)$/i); if (m) cats = m[1].match(/S\d+/g) || []; }
      cats = [...new Set(cats.map(c => String(c).trim().toUpperCase()))].filter(c => AI_FLAG_CATS[c]);
      if (!cats.length) return;
      const table = kind === "post" ? "posts" : "comments";
      const hid = (await env.DB.prepare(`UPDATE ${table} SET deleted = 1 WHERE id = ? AND deleted = 0`).bind(id).run()).meta.changes > 0 ? 1 : 0;
      const already = uname ? await env.DB.prepare(`SELECT 1 FROM jailed WHERE username = ? LIMIT 1`).bind(uname).first() : null;
      let caged = 0;
      if (uname && !already) {
        await env.DB.prepare(`INSERT OR IGNORE INTO jailed (id, browser_id, username, ip_hash, created_at) VALUES (?, ?, ?, NULL, ?)`)
          .bind(crypto.randomUUID(), bid || null, uname, new Date().toISOString()).run();
        caged = 1;
      }
      const why = cats.map(c => AI_FLAG_CATS[c]).join(", ");
      await env.DB.prepare(`INSERT INTO ai_flags (id, kind, target_id, post_id, username, browser_id, categories, excerpt, hid, caged, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'open', ?)`)
        .bind(crypto.randomUUID(), kind, id, postId || null, uname || null, bid || null, cats.join(","), text.slice(0, 600), hid, caged, new Date().toISOString()).run();
      const { results: mods = [] } = await env.DB.prepare(`SELECT username FROM mod_users WHERE role IN ('admin', 'mod') AND deleted_at IS NULL AND username IS NOT NULL`).all();
      const msg = JSON.stringify({
        // Starts with the plain name, so the notification shows that bird's picture
        text: `${uname || "Someone"} had a ${kind === "post" ? "post" : "chirp"} flagged for ${why}. It's hidden and they're in The Cage. Review it in Mod Panel → Flagged.`,
        postId: postId || undefined, icon: "SHIELD", preview: text.slice(0, 80),
      });
      for (const m of mods) await env.DB.prepare(`INSERT INTO system_notifications (id, user_id, message) VALUES (?, ?, ?)`).bind(crypto.randomUUID(), m.username, msg).run();
    } catch (err) {
      console.error("ai check failed:", err && err.message);
    }
  }

  async function isBanned() {
    if (isAdmin) return false; // nothing can lock an admin out, including a shared browser or IP
    const bid = (body.browser_id || "").trim();
    // Mods are only banned by their own account or browser, never by someone else's IP ban
    const conditions = isModerator ? ["username = ?"] : ["ip_hash = ?", "username = ?"];
    const params = isModerator ? [username] : [ip_hash, username];
    if (bid) { conditions.push("browser_id = ?"); params.push(bid); }
    const row = await env.DB.prepare(
      `SELECT 1 FROM bans WHERE ${conditions.join(" OR ")} LIMIT 1`
    ).bind(...params).first();
    return !!row;
  }

  async function isJailed() {
    if (isAdmin) return false;
    const bid = (body.browser_id || "").trim();
    const uname = (username || "").trim();
    if (!bid && !uname) return false;
    const conditions = [];
    const params = [];
    if (bid) { conditions.push("browser_id = ?"); params.push(bid); }
    if (uname) { conditions.push("username = ?"); params.push(uname); }
    const row = await env.DB.prepare(
      `SELECT 1 FROM jailed WHERE ${conditions.join(" OR ")} LIMIT 1`
    ).bind(...params).first();
    return !!row;
  }

  async function bumpPost(post_id) {
    await env.DB.prepare(`UPDATE posts SET last_activity = ? WHERE id = ?`).bind(now, post_id).run();
  }

  // Worms you have: what you had before trading (worm_start) + worms received - worms given
  async function wormBalance(name) {
    if (!name) return 0;
    const r = await env.DB.prepare(`SELECT COALESCE((SELECT worm_start FROM mod_users WHERE username = ?1), 0)
      + (SELECT COUNT(*) FROM worms WHERE receiver = ?1) - (SELECT COUNT(*) FROM worms WHERE giver = ?1) AS b`).bind(name).first();
    return Math.max(0, r?.b || 0);
  }

  // The bird number on each post: people who flapped it (worms are counted separately, see /worm-counts).
  // m: 1 = you flapped, 2 = you gave worms but didn't flap, 0 = nothing. Also the worms you gave.
  async function postResp(ids, me) {
    const out = {};
    for (let i = 0; i < ids.length; i += 30) {
      const chunk = ids.slice(i, i + 30), ph = chunk.map(() => "?").join(",");
      const { results = [] } = await env.DB.prepare(
        `SELECT post_id, COUNT(DISTINCT COALESCE(username, 'b:' || browser_id)) AS n FROM post_votes WHERE value > 0 AND post_id IN (${ph}) GROUP BY post_id`
      ).bind(...chunk).all();
      for (const id of chunk) out[id] = { n: 0, m: 0, emoji: null, worms: 0 };
      for (const r of results) out[r.post_id].n = r.n;
      if (me) {
        const [{ results: f = [] }, { results: w = [] }] = await Promise.all([
          env.DB.prepare(`SELECT post_id FROM post_votes WHERE username = ? AND value > 0 AND post_id IN (${ph})`).bind(me, ...chunk).all(),
          env.DB.prepare(`SELECT post_id, COUNT(*) AS c FROM worms WHERE giver = ? AND post_id IN (${ph}) GROUP BY post_id`).bind(me, ...chunk).all()]);
        for (const r of w) out[r.post_id].worms = r.c;
        const flapped = new Set(f.map(r => r.post_id));
        for (const id of chunk) { const o = out[id]; o.m = flapped.has(id) ? 1 : (o.emoji || o.worms) ? 2 : 0; }
      }
    }
    return out;
  }

  async function getPostVoteSummary(postId, browserId) {
    const { results } = await env.DB.prepare(
      `SELECT value, browser_id FROM post_votes WHERE post_id = ?`
    ).bind(postId).all();
    const score = (results || []).reduce((s, v) => s + (v.value || 0), 0);
    const myVote = (results || []).find(v => v.browser_id === browserId)?.value || 0;
    return { score, myVote, voteCount: (results || []).length };
  }

  // ── /media/<key> ─────────────────────────────────────────────────────────────

  if (url.pathname.startsWith("/media/")) {
    // Served by the perchposts-media worker through Workers Cache (nearby copies, byte ranges from cache).
    if (env.MEDIA_SVC && (request.method === "GET" || request.method === "HEAD")) {
      try {
        const res = await env.MEDIA_SVC.fetch(request);
        if (res.status < 500) return res;
      } catch (err) {
        console.error("media worker unavailable, serving directly", err.message);
      }
    }
    let key = url.pathname.slice("/media/".length);
    if (!key) return new Response("Not found", { status: 404 });
    // ?thumb=1 → the small copy of an older photo if one was made, otherwise the photo itself
    if (url.searchParams.get("thumb") === "1" && !key.startsWith("thumbs/")) {
      const small = await env.MEDIA.head(`thumbs/${key}.jpg`).catch(() => null);
      if (small) key = `thumbs/${key}.jpg`;
    }
    try {
      // Videos on iPhone are fetched in pieces (Range requests); answer with 206 + just that piece.
      const want = (request.headers.get("range") || "").trim();
      const rm = /^bytes=(\d*)-(\d*)$/.exec(want);
      let range = null;
      if (rm && (rm[1] !== "" || rm[2] !== "")) {
        if (rm[1] === "") range = { suffix: Number(rm[2]) };
        else range = rm[2] === "" ? { offset: Number(rm[1]) } : { offset: Number(rm[1]), length: Number(rm[2]) - Number(rm[1]) + 1 };
        if ((range.length !== undefined && range.length <= 0) || range.suffix === 0) range = null;
      }
      const head = await env.MEDIA.head(key);
      if (!head) return new Response("Not found", { status: 404 });
      const size = head.size;
      const headers = new Headers();
      head.writeHttpMetadata(headers);
      headers.set("etag", head.httpEtag);
      headers.set("cache-control", "public, max-age=31536000, immutable");
      headers.set("access-control-allow-origin", "*");
      headers.set("access-control-expose-headers", "content-range, content-length, accept-ranges");
      headers.set("accept-ranges", "bytes");
      headers.set("x-content-type-options", "nosniff");
      headers.set("content-security-policy", "default-src 'none'; sandbox");
      // Already have it? (the file never changes)
      const inm = request.headers.get("if-none-match");
      if (inm && !range && inm.split(",").some(t => t.trim().replace(/^W\//, "") === head.httpEtag)) {
        return new Response(null, { status: 304, headers });
      }
      if (range) {
        const start = range.suffix !== undefined ? Math.max(0, size - range.suffix) : range.offset;
        if (start >= size) {
          headers.set("content-range", `bytes */${size}`);
          return new Response(null, { status: 416, headers });
        }
        const end = range.length !== undefined ? Math.min(size - 1, start + range.length - 1) : size - 1;
        headers.set("content-range", `bytes ${start}-${end}/${size}`);
        headers.set("content-length", String(end - start + 1));
        if (request.method === "HEAD") return new Response(null, { status: 206, headers });
        const part = await env.MEDIA.get(key, { range: { offset: start, length: end - start + 1 } });
        if (!part) return new Response("Not found", { status: 404 });
        return new Response(part.body, { status: 206, headers });
      }
      headers.set("content-length", String(size));
      if (request.method === "HEAD") return new Response(null, { headers });
      const object = await env.MEDIA.get(key);
      if (!object) return new Response("Not found", { status: 404 });
      return new Response(object.body, { headers });
    } catch (err) {
      return new Response("Error", { status: 500 });
    }
  }

  // ── /upload ───────────────────────────────────────────────────────────────────

  if (url.pathname === "/upload" && request.method === "POST") {
    if (!username) return signInRequired();
    if (!isModerator && await isJailed()) return json({ error: CAGED_MEDIA }, 403);
    const ALLOWED = /^(image\/(jpeg|png|gif|webp)|video\/(mp4|webm|quicktime))$/;
    const MAX_VIDEO = 100_000_000, MAX_IMAGE = 50_000_000;   // 100 MB videos, 50 MB photos (photos are shrunk on the phone first)
    const reqType = (request.headers.get("content-type") || "").split(";")[0].trim().toLowerCase();
    if (reqType && reqType !== "multipart/form-data") {
      // The file itself is the body (?name=original-name). Videos stream straight into storage, cleaned on the way.
      try {
        if (!ALLOWED.test(reqType)) return json({ error: "Unsupported file type" }, 400);
        const len = Number(request.headers.get("content-length") || 0);
        if (!len) return json({ error: "Missing file size" }, 411);
        const isVideo = reqType.startsWith("video/");
        if (len > (isVideo ? MAX_VIDEO : MAX_IMAGE)) return json({ error: isVideo ? "Video too large (max 100 MB)" : "Photo too large (max 50 MB)" }, 413);
        const name = url.searchParams.get("name") || "file";
        const ext = name.split(".").pop().toLowerCase().replace(/[^a-z0-9]/g, "") || (isVideo ? "mp4" : "jpg");
        const key = `${crypto.randomUUID()}.${ext}`;
        const meta = { httpMetadata: { contentType: reqType, cacheControl: "public, max-age=31536000, immutable" } };
        if (isVideo && reqType !== "video/webm") {
          const { readable, writable } = new FixedLengthStream(len);
          const piping = request.body.pipeThrough(stripIsoBmffStream()).pipeTo(writable);
          await Promise.all([env.MEDIA.put(key, readable, meta), piping]);
        } else {
          const buf = new Uint8Array(await request.arrayBuffer());
          if (buf.length !== len) return json({ error: "Upload incomplete" }, 400);
          await env.MEDIA.put(key, stripMedia(buf, reqType).bytes, meta);
        }
        return json({ url: `${url.origin}/media/${key}` });
      } catch (err) {
        return serverError(err);
      }
    }
    try {
      const formData = await request.formData();
      const file = formData.get("file");
      if (!file) return json({ error: "No file provided" }, 400);

      // Older pages send the file wrapped in a form; that path holds the file in memory twice, so it stays at 50 MB.
      if (!ALLOWED.test(file.type)) return json({ error: "Unsupported file type" }, 400);

      const MAX_SIZE = 50 * 1024 * 1024; // 50 MB
      if (file.size > MAX_SIZE) return json({ error: "File too large (max 50 MB)" }, 400);
      const buffer = await file.arrayBuffer();

      const ext = (file.name || "file").split(".").pop().toLowerCase().replace(/[^a-z0-9]/g, "") || "bin";
      const key = `${crypto.randomUUID()}.${ext}`;

      // No location, phone model, dates etc. leave with the file
      const clean = stripMedia(new Uint8Array(buffer), file.type).bytes;
      await env.MEDIA.put(key, clean, {
        httpMetadata: { contentType: file.type, cacheControl: "public, max-age=31536000, immutable" }
      });

      return json({ url: `${url.origin}/media/${key}` });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /nest ─────────────────────────────────────────────────────────────────────
  // body: { device: 32 hex chars made by the browser, fresh: true to ask for new eggs }

  if (url.pathname === "/nest" && request.method === "POST") {
    const dev = body.device;
    if (typeof dev !== "string" || !/^[0-9a-f]{32}$/.test(dev)) return json({ error: "Bad device" }, 400);
    try {
      const out = r => json({ names: JSON.parse(r.names), left_ms: Math.max(0, NEST_WAIT - (Date.now() - Date.parse(r.issued_at))) });
      const row = await env.DB.prepare(`SELECT names, prev, issued_at FROM nests WHERE device = ?`).bind(dev).first();
      if (row && JSON.parse(row.names).some(nestBlocked)) {          // nests handed out before the blocked pairs: swap those names
        const fixed = JSON.parse(row.names).map(n => nestBlocked(n) ? nestName() : n); row.names = JSON.stringify(fixed);
        await env.DB.prepare(`UPDATE nests SET names = ? WHERE device = ?`).bind(row.names, dev).run();
      }
      // a nest lasts NEST_WAIT (15 min); after that it times out and the device gets new eggs, so names don't sit in limbo
      if (row && Date.now() - Date.parse(row.issued_at) < NEST_WAIT) return out(row);
      // the page asks with peek on load: an empty nest until the person taps for eggs
      if (body.peek) return json({ names: null, left_ms: 0 });
      const since = new Date(Date.now() - NEST_WAIT).toISOString();
      if (ip_hash && (await siteSetting("signup_limit", "off")) !== "off") {
        const { n } = await env.DB.prepare(`SELECT COUNT(*) AS n FROM nests WHERE net = ? AND issued_at > ?`).bind(ip_hash, since).first();
        if (n >= NEST_NET_CAP) {
          if (row) return out(row);
          const last = await env.DB.prepare(`SELECT names, issued_at FROM nests WHERE net = ? ORDER BY issued_at DESC LIMIT 1`).bind(ip_hash).first();
          await env.DB.prepare(`INSERT OR REPLACE INTO nests (device, net, names, prev, issued_at) VALUES (?, ?, ?, NULL, ?)`).bind(dev, ip_hash, last.names, last.issued_at).run();
          return out(last);
        }
      }
      // new names: not offered to this device before, and not anyone's username
      const seen = new Set(row ? [...JSON.parse(row.names), ...JSON.parse(row.prev || "[]")] : []);
      const names = [];
      for (let tries = 0; names.length < 5 && tries < 6; tries++) {
        const want = new Set(); while (want.size < 5 - names.length) { const n = nestName(); if (!seen.has(n) && !names.includes(n)) want.add(n); }
        const list = [...want], taken = new Set(((await env.DB.prepare(`SELECT LOWER(username) AS u FROM mod_users WHERE LOWER(username) IN (${list.map(() => "?").join(",")})`).bind(...list).all()).results || []).map(r => r.u));
        names.push(...list.filter(n => !taken.has(n)));
      }
      const prev = row ? JSON.stringify([...seen].slice(-200)) : null;
      await env.DB.prepare(`INSERT OR REPLACE INTO nests (device, net, names, prev, issued_at) VALUES (?, ?, ?, ?, ?)`).bind(dev, ip_hash, JSON.stringify(names), prev, now).run();
      if (Math.random() < .05) await env.DB.prepare(`DELETE FROM nests WHERE issued_at < ?`).bind(new Date(Date.now() - NEST_KEEP).toISOString()).run();
      return json({ names, left_ms: NEST_WAIT });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /site-settings ── mods can see them, admins change them ─────────────────────
  if (url.pathname === "/site-settings") {
    if (!isModerator) return json({ error: "Not allowed" }, 403);
    try {
      if (request.method === "POST") {
        if (!isAdmin) return json({ error: "Only admins can change this" }, 403);
        if (body.signup_limit !== undefined) {
          if (!["off", "day", "week"].includes(body.signup_limit)) return json({ error: "Bad value" }, 400);
          await env.DB.prepare(`INSERT INTO site_settings (key, value) VALUES ('signup_limit', ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value`).bind(body.signup_limit).run();
        }
        if (body.ai_check !== undefined) {
          if (!["on", "off"].includes(body.ai_check)) return json({ error: "Bad value" }, 400);
          await env.DB.prepare(`INSERT INTO site_settings (key, value) VALUES ('ai_check', ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value`).bind(body.ai_check).run();
        }
      }
      return json({ signup_limit: await siteSetting("signup_limit", "off"), ai_check: await siteSetting("ai_check", "off"), cap: SIGNUP_CAP, can_edit: isAdmin });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /ping ── visitor counter. Open, visible pages POST {vid, d} every 2 minutes. vid = the device's random
  // browser id, d = the visitor's local date. Who is signed in comes from the token only. No IP is stored.
  // presence: one row per device (last_seen); daily_visits: one row per device per day.
  if (url.pathname === "/ping" && request.method === "POST") {
    try {
      const vid = typeof body.vid === "string" ? body.vid : "";
      if (isBot || !/^[A-Za-z0-9_-]{8,64}$/.test(vid)) return json({ ok: true });
      // Crawlers and automated browsers render the page and ping with a fresh device id every visit, so one crawl
      // looked like dozens of guests (2026-11-22). Known bot user agents are not counted; the page itself also
      // skips the ping when navigator.webdriver is set.
      const ua = request.headers.get("user-agent") || "";
      if (!ua || body.wd === true || /bot\b|bot\/|crawl|spider|slurp|googlebot|google-inspectiontool|bingbot|bingpreview|applebot|yandex|baidu|duckduck|petalbot|ahrefs|semrush|mj12|dotbot|bytespider|gptbot|claudebot|anthropic|perplexity|ccbot|amazonbot|facebookexternalhit|meta-externalagent|twitterbot|discordbot|slackbot|telegrambot|whatsapp|linkedinbot|pinterest|headlesschrome|lighthouse|pagespeed|phantomjs|puppeteer|playwright|selenium|python|curl|wget|node-fetch|axios|go-http|java\//i.test(ua)) return json({ ok: true, skipped: true });
      const now = new Date(), iso = now.toISOString();
      let day = typeof body.d === "string" && /^\d{4}-\d{2}-\d{2}$/.test(body.d) ? body.d : iso.slice(0, 10);
      if (!(Math.abs(Date.parse(day + "T12:00:00Z") - now.getTime()) < 2.5 * 86400000)) day = iso.slice(0, 10);
      const who = authUser?.username || null;
      await env.DB.batch([
        env.DB.prepare(`INSERT INTO presence (vid, username, last_seen) VALUES (?, ?, ?) ON CONFLICT(vid) DO UPDATE SET username = excluded.username, last_seen = excluded.last_seen`).bind(vid, who, iso),
        env.DB.prepare(`INSERT INTO daily_visits (day, vid, username) VALUES (?, ?, ?) ON CONFLICT(day, vid) DO UPDATE SET username = excluded.username WHERE daily_visits.username IS NULL AND excluded.username IS NOT NULL`).bind(day, vid, who),
      ]);
      return json({ ok: true });
    } catch (err) {
      return json({ ok: false });
    }
  }

  // ── /visitors ── admins: who is online now (pinged in the last 3 minutes), today's visitors and the last
  // 14 days (or ?by=month / ?by=year), split into members (signed in) and guests. ?d=<admin's local date>; ?hide_me=1 leaves out the
  // admin's own visits, including their devices while signed out (any device that was ever signed in as them).
  if (url.pathname === "/visitors") {
    if (!isAdmin) return json({ error: "Not allowed" }, 403);
    try {
      const me = authUser.username || "";
      const hideMe = url.searchParams.get("hide_me") === "1";
      const dq = url.searchParams.get("d");
      const today = dq && /^\d{4}-\d{2}-\d{2}$/.test(dq) ? dq : new Date().toISOString().slice(0, 10);
      const from = new Date(Date.parse(today + "T00:00:00Z") - 13 * 86400000).toISOString().slice(0, 10);
      const notMe = hideMe ? ` AND (username IS NULL OR username != ?) AND vid NOT IN (SELECT vid FROM daily_visits WHERE username = ?)` : "";
      const meB = hideMe ? [me, me] : [];
      const cut = new Date(Date.now() - 3 * 60000).toISOString();
      // ?on=<date>: the "Today" box shows that day instead (calendar in the panel)
      const oq = url.searchParams.get("on");
      const onDay = oq && /^\d{4}-\d{2}-\d{2}$/.test(oq) ? oq : today;
      const [on, td, days] = await env.DB.batch([
        env.DB.prepare(`SELECT vid, username FROM presence WHERE last_seen >= ?${notMe}`).bind(cut, ...meB),
        env.DB.prepare(`SELECT vid, username FROM daily_visits WHERE day = ?${notMe}`).bind(onDay, ...meB),
        env.DB.prepare(`SELECT day, COUNT(DISTINCT username) AS members, SUM(username IS NULL) AS guests FROM daily_visits WHERE day >= ? AND day <= ?${notMe} GROUP BY day ORDER BY day DESC`).bind(from, today, ...meB),
      ]);
      const split = rows => {
        const members = [...new Set(rows.filter(r => r.username).map(r => r.username))].sort((a, b) => a.localeCompare(b));
        return { members, guests: rows.filter(r => !r.username).length };
      };
      // Tidy up presence older than a day. daily_visits is kept forever (all-time history, user's choice).
      ctx.waitUntil(env.DB.prepare(`DELETE FROM presence WHERE last_seen < ?`).bind(new Date(Date.now() - 86400000).toISOString()).run().catch(() => {}));
      // ?by=month (last 12 months) or ?by=year (every year): unique members / guests in each period
      const by = url.searchParams.get("by");
      let periods = null;
      if (by === "month" || by === "year") {
        const len = by === "month" ? 7 : 4;
        const pFrom = by === "month" ? new Date(Date.UTC(+today.slice(0, 4), +today.slice(5, 7) - 12, 1)).toISOString().slice(0, 7) : "0000";
        const { results = [] } = await env.DB.prepare(
          `SELECT substr(day, 1, ${len}) AS day, COUNT(DISTINCT username) AS members, COUNT(DISTINCT CASE WHEN username IS NULL THEN vid END) AS guests, COUNT(*) AS visits FROM daily_visits WHERE substr(day, 1, ${len}) > ?${notMe} GROUP BY 1 ORDER BY 1 DESC`
        ).bind(pFrom, ...meB).all();
        periods = results;
      }
      return json({ online: split(on.results || []), today: { day: onDay, ...split(td.results || []) }, first_day: (await env.DB.prepare(`SELECT MIN(day) AS d FROM daily_visits`).first())?.d || today, days: days.results || [], periods, by: periods ? by : "day", hide_me: hideMe });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /ai-flags ── what the AI check flagged (mods). POST {id, verdict: "ok" | "confirm"} reviews one ─────────
  if (url.pathname === "/ai-flags") {
    if (!isModerator) return json({ error: "Not allowed" }, 403);
    try {
      if (request.method === "POST") {
        // Mods flag; deciding (put back or keep hidden) is for admins
        if (!isAdmin) return json({ error: "Only admins can review flags" }, 403);
        const f = await env.DB.prepare(`SELECT * FROM ai_flags WHERE id = ?`).bind(String(body.id || "")).first();
        if (!f) return json({ error: "Not found" }, 404);
        if (!["ok", "confirm"].includes(body.verdict)) return json({ error: "Bad value" }, 400);
        if (body.verdict === "ok") {
          // Not bad: put the post/chirp back, and let the bird out of The Cage if the AI put them there
          // (and nothing else of theirs is still waiting for review)
          if (f.hid) await env.DB.prepare(`UPDATE ${f.kind === "post" ? "posts" : "comments"} SET deleted = 0 WHERE id = ?`).bind(f.target_id).run();
          if (f.caged && f.username) {
            const other = await env.DB.prepare(`SELECT 1 FROM ai_flags WHERE username = ? AND id != ? AND status IN ('open', 'confirmed') LIMIT 1`).bind(f.username, f.id).first();
            if (!other) await env.DB.prepare(`DELETE FROM jailed WHERE username = ?`).bind(f.username).run();
          }
        }
        await env.DB.prepare(`UPDATE ai_flags SET status = ?, reviewed_by = ?, reviewed_at = ? WHERE id = ?`)
          .bind(body.verdict === "ok" ? "ok" : "confirmed", username, now, f.id).run();
      }
      const { results = [] } = await env.DB.prepare(`SELECT * FROM ai_flags ORDER BY created_at DESC LIMIT 100`).all();
      return json({ flags: results.map(f => ({ ...f, why: f.categories === "MOD" ? `flagged by ${f.flagged_by || "a mod"}${f.reason ? `: ${f.reason}` : ""}` : String(f.categories || "").split(",").map(c => AI_FLAG_CATS[c] || c).join(", ") })),
        ai_check: await siteSetting("ai_check", "off"), can_review: !!isAdmin });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /register ─────────────────────────────────────────────────────────────────

  if (url.pathname === "/register" && request.method === "POST") {
    const { username: uname, password, browser_id: bid } = body;
    if (!uname || !password) return json({ error: "Missing fields" }, 400);
    if (uname.length < 2 || uname.length > 30) return json({ error: "Username must be 2-30 characters" }, 400);
    if (password.length < 6) return json({ error: "Password must be at least 6 characters" }, 400);
    if (RESERVED_NAMES.has(uname.trim().toLowerCase())) return json({ error: "Username already taken" }, 409);
    if (!await passesBotCheck(env, body.turnstile, request.headers.get("CF-Connecting-IP"), "signup")) {
      return json({ error: "Bot check failed. Please try again." }, 403);
    }
    try {
      // the name has to be one of the eggs in this device's nest
      const nd = typeof body.nest_device === "string" && /^[0-9a-f]{32}$/.test(body.nest_device) ? body.nest_device : null;
      const nestRow = nd && await env.DB.prepare(`SELECT names, issued_at FROM nests WHERE device = ?`).bind(nd).first();
      if (!nestRow || !JSON.parse(nestRow.names).includes(uname.trim())) return json({ error: "Pick a bird from your nest. If the page has been open a long time, reload it." }, 400);
      if (Date.now() - Date.parse(nestRow.issued_at) > NEST_WAIT + 60000) return json({ error: "Your nest timed out. Pick a bird from your new eggs." }, 400);
      if (nestBlocked(uname.trim())) return json({ error: "That name isn't available any more. Please pick another bird from your nest." }, 400);
      // Retired names stay taken: the site knows people by name, so a reused one would inherit someone's posts
      const existing = await env.DB.prepare(`SELECT id FROM mod_users WHERE LOWER(username) = LOWER(?)`).bind(uname.trim()).first();
      if (existing) return json({ error: "Username already taken" }, 409);
      // Sign-up limit (mod panel switch): at most SIGNUP_CAP new birds per network per day / week
      const lim = await siteSetting("signup_limit", "off");
      if (SIGNUP_WINDOWS[lim] && ip_hash) {
        const since = new Date(Date.now() - SIGNUP_WINDOWS[lim]).toISOString();
        const { n } = await env.DB.prepare(`SELECT COUNT(*) AS n FROM signups WHERE net = ? AND created_at > ?`).bind(ip_hash, since).first();
        if (n >= SIGNUP_CAP) return json({ error: `${SIGNUP_CAP} birds have already hatched on this network ${lim === "day" ? "today" : "this week"}. Please try again later.` }, 429);
      }
      const id = crypto.randomUUID();
      const hash = await hashPassword(password);
      await env.DB.prepare(
        `INSERT INTO mod_users (id, email, password_hash, username, role, created_at) VALUES (?, ?, ?, ?, 'user', ?)`
      ).bind(id, `${uname.trim().toLowerCase()}@users.local`, hash, uname.trim(), now).run();
      await env.DB.prepare(`DELETE FROM nests WHERE device = ?`).bind(nd).run();
      await env.DB.prepare(`INSERT INTO signups (net, created_at) VALUES (?, ?)`).bind(ip_hash || null, now).run().catch(() => {});
      if (bid) {
        await env.DB.prepare(`UPDATE posts SET username = ? WHERE browser_id = ? AND is_mod = 0 AND username IS NULL`).bind(uname.trim(), bid).run();
        await env.DB.prepare(`UPDATE comments SET username = ? WHERE browser_id = ? AND is_mod = 0 AND username IS NULL`).bind(uname.trim(), bid).run();
      }
      const token = await signJWT(
        { sub: id, role: "user", username: uname.trim(), iat: Math.floor(Date.now() / 1000), exp: Math.floor(Date.now() / 1000) + 86400 * 90 },
        env.JWT_SECRET
      );
      return json({ token, user: { id, role: "user", username: uname.trim() } });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /login ────────────────────────────────────────────────────────────────────

  if (url.pathname === "/login" && request.method === "POST") {
    const { username: uname, password } = body;
    if (!uname || !password) return json({ error: "Missing fields" }, 400);
    try {
      const user = await env.DB.prepare(
        `SELECT * FROM mod_users WHERE username = ? AND deleted_at IS NULL`
      ).bind(uname.trim()).first();
      if (!user) return json({ error: "Invalid credentials" }, 401);
      // 10 wrong passwords in a row lock the account for 15 minutes (mods/admins can unlock it in the mod panel)
      const lockedMsg = until => {
        const mins = Math.max(1, Math.ceil((new Date(until) - Date.now()) / 60000));
        return `Too many wrong passwords. This account is locked for ${mins} more minute${mins === 1 ? "" : "s"}. Try again later, or ask an admin to unlock it.`;
      };
      if (user.locked_until && user.locked_until > now) return json({ error: lockedMsg(user.locked_until), locked: true }, 423);
      const ok = await verifyPassword(password, user.password_hash).catch(() => false);
      if (!ok) {
        const row = await env.DB.prepare(`UPDATE mod_users SET failed_logins = failed_logins + 1 WHERE id = ? RETURNING failed_logins`).bind(user.id).first();
        if ((row?.failed_logins || 0) >= LOGIN_TRIES) {
          const until = new Date(Date.now() + LOCK_MINUTES * 60000).toISOString();
          await env.DB.prepare(`UPDATE mod_users SET failed_logins = 0, locked_until = ? WHERE id = ?`).bind(until, user.id).run();
          const { results: admins = [] } = await env.DB.prepare(`SELECT username FROM mod_users WHERE role = 'admin' AND deleted_at IS NULL AND username IS NOT NULL`).all();
          const msg = JSON.stringify({ text: `${user.username}'s account was locked for ${LOCK_MINUTES} minutes after ${LOGIN_TRIES} wrong passwords. You can unlock it in the mod panel.`, icon: "🔒" });
          await Promise.all(admins.map(a => upsertNotif(a.username, msg))).catch(err => console.error("lock notify failed", err.message));
          return json({ error: lockedMsg(until), locked: true }, 423);
        }
        return json({ error: "Invalid credentials" }, 401);
      }
      if (user.failed_logins || user.locked_until) await env.DB.prepare(`UPDATE mod_users SET failed_logins = 0, locked_until = NULL WHERE id = ?`).bind(user.id).run();
      const token = await signJWT(
        { sub: user.id, role: user.role, username: user.username, iat: Math.floor(Date.now() / 1000), exp: Math.floor(Date.now() / 1000) + 86400 * 90 },
        env.JWT_SECRET
      );
      return json({ token, user: { id: user.id, role: user.role, username: user.username } });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /update-password ──────────────────────────────────────────────────────────

  if (url.pathname === "/update-password" && request.method === "POST") {
    if (!authUser) return json({ error: "Unauthorized" }, 401);
    const { newPassword, currentPassword } = body;
    if (!newPassword) return json({ error: "Missing newPassword" }, 400);
    if (!currentPassword) return json({ error: "Enter your current password" }, 400);
    if (String(newPassword).length < 6) return json({ error: "Password must be at least 6 characters" }, 400);
    try {
      const acct = await env.DB.prepare(`SELECT id, username, role, password_hash FROM mod_users WHERE id = ? AND deleted_at IS NULL`).bind(authUser.sub).first();
      if (!acct) return json({ error: "Unauthorized" }, 401);
      if (!(await verifyPassword(currentPassword, acct.password_hash).catch(() => false))) return json({ error: "Your current password isn't right" }, 403);
      const hash = await hashPassword(newPassword);
      const changedAt = new Date(Math.floor(Date.now() / 1000) * 1000).toISOString(); // whole seconds, like login times
      await env.DB.prepare(`UPDATE mod_users SET password_hash = ?, password_changed_at = ?, failed_logins = 0, locked_until = NULL WHERE id = ?`)
        .bind(hash, changedAt, acct.id).run();
      // Every other login is now signed out; this device gets a fresh one
      const t = Math.floor(Date.now() / 1000) + 3;
      const token = await signJWT({ sub: acct.id, role: acct.role, username: acct.username, iat: t, exp: t + 86400 * 90 }, env.JWT_SECRET);
      return json({ success: true, token });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /create-post ──────────────────────────────────────────────────────────────

  if (url.pathname === "/create-post") {
    if (!username) return signInRequired();
    try {
      const isHuddle = body.is_huddle === true || body.is_huddle === 1;
      if (!isHuddle && !body.content) return json({ error: "Missing fields" }, 400);
      if (isHuddle && !body.huddle_members) return json({ error: "Missing huddle_members" }, 400);
      const caged = !isBot && !isModerator && await isJailed();
      // Caged birds can only write in The Cage: no starting huddles either
      if (caged && isHuddle) return json({ error: "Caged" }, 403);
      if (caged && hasMedia(body.content)) return json({ error: CAGED_MEDIA }, 403);
      if (caged) {
        // Cage posts have no country or region (the page doesn't offer one; this covers anything sent directly)
        body.country = null;
        body.continent = null;
        body.board = "The Cage";
        body.category = "The Cage";
        body.community_id = "cage";
      } else if (!isBot && await isBanned()) {
        return json({ error: "Banned", _debug: { username, browser_id: (body.browser_id||"").trim() } }, 403);
      }
      if (isHuddle) {
        body.board = "Huddles";
        body.community_id = "feedback";
        body.content = body.content || "";
      }
      if (!body.board) body.board = "General";
      // Only the admin and mods post in Announcements (bot feeds are set up by the admin)
      if (!isModerator && !isBot && [body.board, body.category, body.community_id].some(v => String(v || "").trim().toLowerCase() === "announcements")) {
        return json({ error: "Only mods can post in Announcements" }, 403);
      }
      // The Cage is for caged birds (and mods); everyone else can still chirp on Cage posts
      if (!caged && !isModerator && !isBot && [body.board, body.category, body.community_id].some(v => ["cage", "the cage"].includes(String(v || "").trim().toLowerCase()))) {
        return json({ error: "Only caged birds can post in The Cage" }, 403);
      }
      const checked = !isBot && !isModerator && !isHuddle;
      if (checked && hasSlur(userText(body.title, body.content))) return json({ error: SLUR_MSG }, 400);
      // One user tag per post (birds' public posts only; not bots, huddles or The Cage)
      let utag = null;
      if (body.user_tag && !isBot && !isHuddle && !caged) {
        const r = await cleanTag(body.user_tag);
        if (r.error) return json({ error: r.error }, 400);
        utag = r.tag;
      }
      // Every bird post needs a tag: a perch tag, or a flock tag. With only a flock tag (board_auto) the post is filed
      // under Random behind the scenes, and pages hide that Random pill (the author didn't pick it).
      const boardAuto = !isBot && !isHuddle && !caged && body.board_auto === true;
      if (boardAuto) {
        if (!utag) return json({ error: "Add a tag" }, 400);
        body.board = "Random"; body.category = "Random"; body.community_id = "random";
      }
      // Bots can't post an article twice
      let botClaim = null;
      if (isBot) {
        botClaim = await claimBotPost(env, botPostKeys(body.content), now);
        if (botClaim.duplicate) return json({ success: false, duplicate: true }, 409);
      }
      // A new huddle starts with just its owner; the birds picked get invites to accept or decline
      const invitees = isHuddle ? [...new Set((Array.isArray(body.huddle_members) ? body.huddle_members : []).map(normMember).filter(n => n && n.toLowerCase() !== username.toLowerCase()))] : [];
      const huddleMembers = isHuddle ? "[]" : null;
      const id = crypto.randomUUID();
      await env.DB.prepare(`
        INSERT INTO posts (id, title, content, username, ip_hash, browser_id, last_activity,
          is_mod, is_admin, moderator, mod_user_id, continent, country, board, community_id,
          is_huddle, huddle_members, created_at, utag, board_auto)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `).bind(
        id,
        body.title || null,
        body.content,
        username,
        ip_hash,
        body.browser_id || null,
        now,
        isModerator ? 1 : 0,
        isAdmin ? 1 : 0,
        isModerator ? 1 : 0,
        isModerator ? (authUser.sub ?? null) : null,
        body.continent || null,
        body.country || null,
        body.board,
        body.community_id || null,
        isHuddle ? 1 : 0,
        huddleMembers,
        now,
        utag,
        boardAuto ? 1 : 0
      ).run().catch(async err => {
        // The post didn't save, so the article can be tried again next run
        for (const key of botClaim?.claimed || []) {
          await env.DB.prepare(`DELETE FROM bot_links WHERE url = ?`).bind(key).run().catch(() => {});
        }
        throw err;
      });
      if (utag) await env.DB.prepare(`INSERT INTO post_tags (tag, post_id, created_at) VALUES (?, ?, ?)`).bind(utag, id, now).run();
      // The huddle's opening message: the owner's first chirp, pinned
      const first = isHuddle && typeof body.first_chirp === "string" && body.first_chirp.trim() ? body.first_chirp.slice(0, 8000) : null;
      if (first) {
        await env.DB.prepare(`INSERT INTO comments (id, content, post_id, parent_comment_id, username, ip_hash, browser_id, is_mod, is_admin, moderator, mod_user_id, created_at, pinned) VALUES (?, ?, ?, NULL, ?, ?, ?, ?, ?, ?, ?, ?, 1)`)
          .bind(crypto.randomUUID(), first, id, username, ip_hash, body.browser_id || null, isModerator ? 1 : 0, isAdmin ? 1 : 0, isModerator ? 1 : 0, isModerator ? (authUser.sub ?? null) : null, now).run();
      }
      // Invite the birds picked for the huddle
      if (isHuddle && invitees.length) {
        const extinct = await extinctNames();
        const newPost = { id, title: body.title || null, username, huddle_members: "[]" };
        for (const name of invitees) if (!extinct.has(name)) await sendInvite(newPost, username, name);
      }
      if (checked) ctx.waitUntil(aiCheck({ kind: "post", id, postId: id, text: userText(body.title, body.content), uname: username, bid: body.browser_id }).catch(() => {}).then(() => checkAlerts(id)));
      else if (!isHuddle) ctx.waitUntil(checkAlerts(id));
      ctx.waitUntil(notifyMentions({ by: username, text: userText(body.title, body.content, first), postId: id }));
      const post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ?`).bind(id).first();
      return json({ success: true, post: boolify(post, POST_BOOL_FIELDS) });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /bot-release ───────────────────────────────────────────────────────────────
  // The news bots gather a whole hour, then release it here in one go, so it lands all at once.
  // posts[] comes top-first; each gets a timestamp 1 ms apart so the feed shows them in that order.
  if (url.pathname === "/bot-release" && request.method === "POST") {
    if (!isBot) return json({ error: "Unauthorized" }, 401);
    try {
      const list = Array.isArray(body.posts) ? body.posts.slice(0, 400) : [];
      const base = Date.now();
      const results = [], stmts = [], claims = [];
      // Check every post for repeats in ONE database call. One call per post took ~20 s for an hour's batch, so
      // posts stamped :00:00 only showed up around :00:20 and the "new posts" pill came late.
      const keysOf = list.map(p => botPostKeys((p || {}).content));
      const cutoff = new Date(Date.now() - REPEAT_TITLE_DAYS * 86400000).toISOString();
      const cstmts = [], cidx = [];
      keysOf.forEach((k, i) => {
        if (!(list[i] || {}).content) return;
        const at = new Date(base - i).toISOString();
        if (k.link) { cidx.push([i, "link"]); cstmts.push(env.DB.prepare(`INSERT OR IGNORE INTO bot_links (url, created_at) VALUES (?, ?)`).bind(k.link, at)); }
        if (k.title) { cidx.push([i, "title"]); cstmts.push(env.DB.prepare(
          `INSERT INTO bot_links (url, created_at) VALUES (?, ?) ON CONFLICT(url) DO UPDATE SET created_at = excluded.created_at WHERE bot_links.created_at < ?`
        ).bind(k.title, at, cutoff)); }
      });
      let pre = null;
      if (cstmts.length) {
        try {
          const rs = await env.DB.batch(cstmts);
          pre = new Map();
          rs.forEach((r, j) => {
            const [i, kind] = cidx[j], c = pre.get(i) || { duplicate: false, claimed: [] };
            if (r.meta.changes === 0) c.duplicate = true; else c.claimed.push(keysOf[i][kind]);
            pre.set(i, c);
          });
        } catch (err) { console.error("bot-release: batched repeat check failed, checking one by one:", err.message); pre = null; }
      }
      for (let i = 0; i < list.length; i++) {
        const p = list[i] || {};
        if (!p.content) { results.push({ ok: false, error: "Missing content" }); continue; }
        const at = new Date(base - i).toISOString();
        const claim = pre ? (pre.get(i) || { duplicate: false, claimed: [] }) : await claimBotPost(env, keysOf[i], at);
        if (claim.duplicate) { results.push({ ok: false, duplicate: true }); continue; }
        claims.push(...(claim.claimed || []));
        const id = crypto.randomUUID();
        stmts.push(env.DB.prepare(`
          INSERT INTO posts (id, title, content, username, ip_hash, browser_id, last_activity,
            is_mod, is_admin, moderator, mod_user_id, continent, country, board, community_id,
            is_huddle, huddle_members, created_at)
          VALUES (?, NULL, ?, ?, ?, ?, ?, 0, 0, 0, NULL, ?, ?, ?, NULL, 0, NULL, ?)
        `).bind(id, p.content, (typeof p.username === "string" && p.username.trim()) || "NewsBot", ip_hash,
          p.browser_id || null, at, p.continent || null, p.country || null, p.board || "General", at));
        results.push({ ok: true, id });
      }
      if (stmts.length) {
        // One batch: the whole hour appears together, or (if it fails) not at all and can be tried again.
        // The feed lists newest rowid first, so the bottom post is written first and the top post last.
        await env.DB.batch(stmts.reverse()).catch(async err => {
          for (const key of claims) await env.DB.prepare(`DELETE FROM bot_links WHERE url = ?`).bind(key).run().catch(() => {});
          throw err;
        });
      }
      if (stmts.length) ctx.waitUntil((async () => { for (const r of results) if (r.ok && r.id) await checkAlerts(r.id); })());
      return json({ success: true, posted: stmts.length, results });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /get-post ──────────────────────────────────────────────────────────────────

  if (url.pathname === "/get-post") {
    try {
      const id = url.searchParams.get("id");
      if (!id) return json({ error: "Missing id" }, 400);
      let post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ? AND deleted = 0`).bind(id).first();
      if (!post && isModerator) {
        post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ?`).bind(id).first();
      }
      if (!post) return json({ error: "Not found" }, 404);
      if ((post.archived || post.deleted) && !isModerator) return json({ error: "Not found" }, 404);
      // Huddle access control
      if (post.is_huddle) {
        if (!seeAllHuddles && !isHuddleMember(post, username)) {
          return json({ error: "not_member", huddle: true }, 403);
        }
        const { results: pend = [] } = await env.DB.prepare(
          `SELECT id, from_user, target, created_at FROM huddle_requests WHERE post_id = ? AND kind = 'invite' AND status = 'pending' AND created_at > ? ORDER BY created_at`
        ).bind(post.id, requestCutoff()).all().catch(() => ({ results: [] }));
        post.huddle_pending = pend;
      }
      const sp = url.searchParams;
      const pageSize = Math.min(parseInt(sp.get("limit") || "0") || 0, 200);
      const paged = pageSize > 0;
      let comments, from = null;
      if (paged) {
        // from is the oldest chirp the page holds, "" meaning all of them. It only ever moves back.
        const chirpAt = async (older, skip) => (await env.DB.prepare(
          `SELECT created_at FROM comments WHERE post_id = ? AND deleted = 0${older ? " AND created_at < ?" : ""} ORDER BY created_at DESC LIMIT 1 OFFSET ?`
        ).bind(...(older ? [id, older, skip] : [id, skip])).first())?.created_at || "";
        const reachBack = async at => { if (at && (from === "" ? false : at < from)) from = await chirpAt(at, 19); };
        from = sp.has("from") ? sp.get("from") : null;
        if (sp.get("all") === "1") from = "";
        else {
          if (from === null) from = await chirpAt(null, pageSize - 1);
          if (sp.get("older") === "1" && from) from = await chirpAt(from, pageSize - 1);
          // Notifications and Find need their chirp on the page before they can jump to it
          const to = sp.get("to"), toUser = sp.get("to_user");
          if (to) {
            const row = await env.DB.prepare(`SELECT created_at, pinned FROM comments WHERE id = ? AND post_id = ? AND deleted = 0`).bind(to, id).first();
            if (row && !row.pinned) await reachBack(row.created_at); // pinned chirps are always on the page
          }
          if (toUser) {
            const row = await env.DB.prepare(`SELECT created_at FROM comments WHERE post_id = ? AND username = ? AND deleted = 0 ORDER BY created_at DESC LIMIT 1`).bind(id, toUser).first();
            if (row) await reachBack(row.created_at); else from = "";
          }
        }
        const [{ results: page }, { results: pins }] = await Promise.all([
          env.DB.prepare(`SELECT * FROM comments WHERE post_id = ? AND deleted = 0 AND created_at >= ? ORDER BY created_at ASC`).bind(id, from).all(),
          env.DB.prepare(`SELECT * FROM comments WHERE post_id = ? AND pinned = 1 AND deleted = 0`).bind(id).all()
        ]);
        const inPage = new Set((page || []).map(c => c.id));
        comments = [...(pins || []).filter(c => !inPage.has(c.id)), ...(page || [])];
      } else {
        comments = (await env.DB.prepare(`SELECT * FROM comments WHERE post_id = ? AND deleted = 0 ORDER BY created_at ASC`).bind(id).all()).results || [];
      }
      // Here rather than a separate request: listing every chirp id in a URL fails on long chats,
      // and this keeps huddle reactions behind the member check above
      // Top chirps of the whole conversation (posts and huddles; no cap — user 2026-11-25): score = emoji reactions + 1.5 per worm (user's call,
      // 2026-11-25: straight 1.5 per worm, not per giver); 1+ reaction or worm while the site is small; newest wins ties.
      // They may be older than the loaded page, so their reactions ride along below
      const { results: topRows } = await env.DB.prepare(
        `SELECT * FROM (SELECT c.*, (SELECT COUNT(*) FROM comment_reactions r WHERE r.comment_id = c.id) AS rx_count,
                (SELECT COUNT(*) FROM worms w WHERE w.comment_id = c.id) AS worm_count
           FROM comments c WHERE c.post_id = ? AND c.deleted = 0)
         WHERE rx_count + worm_count > 0 ORDER BY rx_count + 1.5 * worm_count DESC, created_at DESC`
      ).bind(id).all();
      const top = topRows || [];
      // Most replied chirps (1+ replies while the site is small), for the preview's "Most replied" section
      const { results: repRows } = await env.DB.prepare(
        `SELECT c.*, COUNT(r.id) AS reply_count FROM comments c JOIN comments r ON r.parent_comment_id = c.id AND r.deleted = 0 WHERE c.post_id = ? AND c.deleted = 0 GROUP BY c.id HAVING COUNT(r.id) >= 1 ORDER BY reply_count DESC, c.created_at DESC`
      ).bind(id).all();
      const replied = repRows || [];
      const rxIds = [...new Set([...comments.map(c => c.id), ...top.map(c => c.id), ...replied.map(c => c.id)])];
      const { results: reactions } = await env.DB.prepare(
        `SELECT comment_id, browser_id, emoji, username FROM comment_reactions WHERE comment_id IN (${ID_LIST})`
      ).bind(JSON.stringify(rxIds)).all();
      const payload = {
        post: (await publicRows([boolify(post, POST_BOOL_FIELDS)]))[0],
        comments: await publicRows(comments.map(c => boolify(c, COMMENT_BOOL_FIELDS))),
        reactions: reactions || [],
        top: await publicRows(top.map(c => boolify(c, COMMENT_BOOL_FIELDS))),
        replied: await publicRows(replied.map(c => boolify(c, COMMENT_BOOL_FIELDS)))
      };
      // Open pages poll this, so a chat that hasn't changed sends a few bytes instead of every chirp
      const digest = await crypto.subtle.digest("SHA-1", new TextEncoder().encode(JSON.stringify(payload)));
      const version = [...new Uint8Array(digest)].map(b => b.toString(16).padStart(2, "0")).join("");
      if (sp.get("v") === version) return json({ unchanged: true });
      if (!paged) return json({ ...payload, version });
      // Only worked out when something changed, because counting reads every chirp
      const have = new Set(comments.map(c => c.id));
      const parents = [...new Set(comments.map(c => c.parent_comment_id).filter(p => p && !have.has(p)))];
      const [total, older, quoted] = await Promise.all([
        env.DB.prepare(`SELECT COUNT(*) AS n FROM comments WHERE post_id = ? AND deleted = 0 AND (username IS NULL OR username != '__system__')`).bind(id).first(),
        from ? env.DB.prepare(`SELECT 1 FROM comments WHERE post_id = ? AND deleted = 0 AND created_at < ? LIMIT 1`).bind(id, from).first() : null,
        parents.length ? env.DB.prepare(`SELECT * FROM comments WHERE id IN (${ID_LIST}) AND deleted = 0`).bind(JSON.stringify(parents)).all() : { results: [] }
      ]);
      return json({
        ...payload, version, from,
        has_more: !!older,
        comment_total: total?.n || 0,
        // Chirps quoted by replies on this page but older than it, for the quote and nothing else
        quoted: await publicRows((quoted.results || []).map(c => boolify(c, COMMENT_BOOL_FIELDS)))
      });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /get-posts ─────────────────────────────────────────────────────────────────

  if (url.pathname === "/get-posts") {
    try {
      const board    = url.searchParams.get("board") || null;
      const continent = url.searchParams.get("continent") || null;
      const country  = url.searchParams.get("country") || null;
      const username = url.searchParams.get("username") || null;
      const activityFilter = url.searchParams.get("activity") === "1";
      const limit    = activityFilter ? 10000 : Math.min(parseInt(url.searchParams.get("limit") || "50"), 10000);
      const offset   = parseInt(url.searchParams.get("offset") || "0");
      const search   = url.searchParams.get("search") || null;
      const sortBy   = url.searchParams.get("sort") === "activity" ? "last_activity" : "created_at";

      const BOTS = ['NewsBot','ScienceBot','NatureBot','SportsBot'];

      const isHuddleBoard = board && (board.toLowerCase() === "feedback" || board.toLowerCase() === "huddles");
      const since = url.searchParams.get("since") || null;
      const until = url.searchParams.get("until") || null;
      const before = url.searchParams.get("before") || null;

      // Most flaps / Most chirps: posts from the last day / week / all time ranked by flaps or chirps
      // (sort=flaps|chirps, range=day|week|all, default week). post_votes and comments are small, so rank
      // there, then load those posts. Each post gets a "rank" field with its count.
      // Profile "Activity" tab (?activity_by=, or the older ?flapped_by=): posts the person flapped, fed worms
      // (to the post or one of its chirps) or chirped on, newest action first. Each post gets act {f, w, c}:
      // flapped (0/1), worms given, chirps written. Huddles are left out by LIVE_POSTS.
      const flappedBy = url.searchParams.get("activity_by") || url.searchParams.get("flapped_by");
      if (flappedBy) {
        const pageLimit = Math.min(parseInt(url.searchParams.get("limit") || "50") || 50, 100);
        const { results: fl = [] } = await env.DB.prepare(
          `SELECT post_id, MAX(t) AS created_at, SUM(k = 'f') AS f, SUM(k = 'w') AS w, SUM(k = 'c') AS c FROM (
             SELECT post_id, created_at AS t, 'f' AS k FROM post_votes WHERE username = ? AND value > 0
             UNION ALL SELECT post_id, created_at, 'w' FROM worms WHERE giver = ? AND post_id IS NOT NULL
             UNION ALL SELECT cm.post_id, w.created_at, 'w' FROM worms w JOIN comments cm ON cm.id = w.comment_id WHERE w.giver = ? AND w.post_id IS NULL
             UNION ALL SELECT post_id, created_at, 'c' FROM comments WHERE username = ? AND deleted = 0)
           GROUP BY post_id${before ? " HAVING MAX(t) < ?" : ""} ORDER BY created_at DESC LIMIT ?`
        ).bind(flappedBy, flappedBy, flappedBy, flappedBy, ...(before ? [before] : []), pageLimit).all();
        const acts = new Map(fl.map(r => [r.post_id, { f: r.f ? 1 : 0, w: r.w || 0, c: r.c || 0 }]));
        const when = new Map(fl.map(r => [r.post_id, r.created_at])), ids = [...when.keys()], rows = [];
        for (let i = 0; i < ids.length; i += 90) {
          const chunk = ids.slice(i, i + 90);
          const { results = [] } = await env.DB.prepare(`SELECT rowid AS _rid, * FROM posts WHERE id IN (${chunk.map(() => "?").join(",")}) AND ${LIVE_POSTS}`).bind(...chunk).all();
          rows.push(...results);
        }
        rows.sort((a, b) => (when.get(b.id) || "").localeCompare(when.get(a.id) || ""));
        const posts = await publicRows(await addCommentCounts(env, rows.map(p => ({ ...boolify(p, POST_BOOL_FIELDS), flapped_at: when.get(p.id), act: acts.get(p.id) }))));
        return json({ posts, next_before: fl.length === pageLimit ? fl[fl.length - 1].created_at : null });
      }

      // ?utag=<tag>: posts with that user tag, newest first (through post_tags, never a scan of posts)
      const utagQ = String(url.searchParams.get("utag") || "").trim().replace(/^#+/, "").toLowerCase();
      if (utagQ) {
        if (!/^[a-z0-9]{2,20}$/.test(utagQ)) return json({ posts: [], next_before: null });
        const pageLimit = Math.min(parseInt(url.searchParams.get("limit") || "50") || 50, 100);
        const { results = [] } = await env.DB.prepare(
          `SELECT rowid AS _rid, * FROM posts WHERE id IN (SELECT post_id FROM post_tags WHERE tag = ?${before ? " AND created_at < ?" : ""} ORDER BY created_at DESC LIMIT ?) AND ${LIVE_POSTS} ORDER BY created_at DESC`
        ).bind(utagQ, ...(before ? [before] : []), pageLimit).all();
        return json({ posts: await publicRows(await addCommentCounts(env, results.map(p => boolify(p, POST_BOOL_FIELDS)))), next_before: results.length === pageLimit ? results[results.length - 1].created_at : null });
      }

      const rankSort = url.searchParams.get("sort");
      if (rankSort === "flaps" || rankSort === "chirps") {
        const range = url.searchParams.get("range");
        // Optional window from the Time filter: rank_until = end of the picked day / hour (ISO). Then
        // day = that day, week = the 7 days ending there, all = everything before it. Without it, windows end now.
        const ru = url.searchParams.get("rank_until");
        const rankUntil = ru && !isNaN(Date.parse(ru)) ? new Date(ru).toISOString() : null;
        const endMs = rankUntil ? Date.parse(rankUntil) : Date.now();
        const since = range === "all" ? "" : new Date(endMs - (range === "day" ? 1 : 7) * 86400000).toISOString();
        const untilSql = rankUntil ? " AND created_at < ?" : "";
        // Count the flaps / chirps made in the range (on posts of any age): "Most chirps today" = the posts
        // that got the most chirps today. Before, it only looked at posts created in the range.
        const { results: top = [] } = await env.DB.prepare(rankSort === "flaps"
          ? `SELECT post_id, COUNT(DISTINCT COALESCE(username, 'b:' || browser_id)) AS n FROM post_votes WHERE value > 0 AND created_at >= ?${untilSql} GROUP BY post_id ORDER BY n DESC LIMIT 500`
          : `SELECT post_id, COUNT(*) AS n FROM comments WHERE deleted = 0 AND (username IS NULL OR username != '__system__') AND created_at >= ?${untilSql} GROUP BY post_id ORDER BY n DESC LIMIT 500`
        ).bind(since, ...(rankUntil ? [rankUntil] : [])).all();
        const countOf = new Map(top.map(r => [r.post_id, r.n]));
        const ids = [...countOf.keys()];
        const rows = [];
        for (let i = 0; i < ids.length; i += 90) {
          const chunk = ids.slice(i, i + 90);
          const { results = [] } = await env.DB.prepare(
            `SELECT rowid AS _rid, * FROM posts WHERE id IN (${chunk.map(() => "?").join(",")}) AND ${LIVE_POSTS}`
          ).bind(...chunk).all();
          rows.push(...results);
        }
        rows.sort((a, b) => (countOf.get(b.id) || 0) - (countOf.get(a.id) || 0));
        const posts = await publicRows(await addCommentCounts(env, rows.map(p => ({ ...boolify(p, POST_BOOL_FIELDS), rank: countOf.get(p.id) || 0 }))));
        return json({ posts, next_before: null });
      }

      // Hide bots: every post by a person (a small set, read through the partial index)
      if (url.searchParams.get("people") === "1") {
        const { results = [] } = await env.DB.prepare(
          `SELECT rowid AS _rid, * FROM posts INDEXED BY idx_posts_human_activity WHERE ${HUMAN_POSTS} AND ${LIVE_POSTS} ORDER BY last_activity DESC LIMIT 500`
        ).all();
        return json({ posts: await publicRows(await addCommentCounts(env, results.map(p => boolify(p, POST_BOOL_FIELDS)))), next_before: null });
      }

      // Bot News space: only the bots' posts, newest first. Most posts are bot posts, so walking the created_at
      // index stops after one page; ?before=<created_at> pages back.
      if (url.searchParams.get("bots") === "1") {
        const pageLimit = Math.min(parseInt(url.searchParams.get("limit") || "50") || 50, 100);
        const { results = [] } = await env.DB.prepare(
          `SELECT rowid AS _rid, * FROM posts INDEXED BY idx_posts_created_at WHERE username IN (${BOTS.map(() => "?").join(",")}) AND ${LIVE_POSTS}${before ? " AND created_at < ?" : ""} ORDER BY created_at DESC LIMIT ?`
        ).bind(...BOTS, ...(before ? [before] : []), pageLimit).all();
        return json({ posts: await publicRows(await addCommentCounts(env, results.map(p => boolify(p, POST_BOOL_FIELDS)))), next_before: results.length === pageLimit ? results[results.length - 1].created_at : null });
      }

      // Filtered views and "load older" pages read one page at a time instead of scanning every post
      if (!search && !since && !until && !isHuddleBoard && (activityFilter || board || continent || country || username || before)) {
        const pageLimit = Math.min(parseInt(url.searchParams.get("limit") || "50") || 50, 100);
        const page = await getPostsPage(env, { activity: activityFilter, board, continent, country, username, before, limit: pageLimit });
        return json({ ...page, posts: await publicRows(await addCommentCounts(env, page.posts)) });
      }

      // INDEXED BY fails fast instead of scanning every post if the index is missing
      let q = `SELECT rowid AS _rid, * FROM posts${isHuddleBoard ? " INDEXED BY idx_posts_huddles" : ""} WHERE deleted = 0 AND (archived = 0 OR archived IS NULL)`;
      const params = [];
      if (activityFilter) {
        const placeholders = BOTS.map(() => '?').join(',');
        q += ` AND (username NOT IN (${placeholders}) OR id IN (SELECT DISTINCT post_id FROM comments WHERE deleted = 0) OR id IN (SELECT post_id FROM post_shares))`;
        params.push(...BOTS);
      }
      if (isHuddleBoard) {
        // Huddles board: only is_huddle posts, filtered by JWT-authenticated username only (no spoofable query param)
        q += ` AND is_huddle = 1`;
        const huddleUsername = authUser?.username || null;
        if (!seeAllHuddles) {
          if (huddleUsername) {
            // Members are stored as "name" or, for admins and mods, "name:admin" / "name:mod"
            q += ` AND (LOWER(username) = LOWER(?) OR (huddle_members IS NOT NULL AND (LOWER(huddle_members) LIKE LOWER(?) OR LOWER(huddle_members) LIKE LOWER(?))))`;
            params.push(huddleUsername, `%"${huddleUsername}"%`, `%"${huddleUsername}:%`);
          } else {
            q += ` AND 1 = 0`; // not authenticated = no results
          }
        }
      } else {
        // All other boards: exclude huddle posts
        q += ` AND (is_huddle = 0 OR is_huddle IS NULL)`;
        if (board) { q += ` AND (LOWER(community_id) = LOWER(?) OR LOWER(board) = LOWER(?))`;  params.push(board, board); }
      }
      if (!isHuddleBoard && continent) { const w = regionWhere(continent); q += ` AND ${w.sql}`; params.push(...w.params); }
      // A country chip searches for its own name, and keeps that country's feed articles too
      const chipSearch = !!search && !!country && search.toLowerCase() === country.toLowerCase();
      const cw = country && countryWhere(country);
      if (!isHuddleBoard && country && !chipSearch) { q += ` AND ${cw.sql}`; params.push(...cw.params); }
      if (username && isHuddleBoard) {
        // In Huddles, a bird pill finds every huddle that bird is in (owner or member, "name" or "name:role")
        const un = username.toLowerCase();
        q += ` AND (LOWER(username) = ? OR (huddle_members IS NOT NULL AND (LOWER(huddle_members) LIKE ? OR LOWER(huddle_members) LIKE ?)))`;
        params.push(un, `%"${un}"%`, `%"${un}:%`);
      } else if (username)  { q += ` AND LOWER(username) = ?`;  params.push(username.toLowerCase()); }
      // A country pill: its tagged posts, plus posts naming the country by the region tabs' rule
      if (chipSearch) { q += ` AND (${MAYBE_NAMES} OR ${cw.sql})`; params.push(JSON.stringify(countryTerms(country)), ...cw.params); }
      else if (search) { q += ` AND (title LIKE ? OR content LIKE ?)`; params.push(`%${search}%`, `%${search}%`); }
      if (since) { q += ` AND created_at >= ?`; params.push(since); }
      if (until) { q += ` AND created_at < ?`;  params.push(until); }
      q += ` ORDER BY pinned_global DESC, pinned DESC, ${sortBy} DESC, created_at DESC LIMIT ? OFFSET ?`;
      params.push(limit, offset);

      const { results } = await env.DB.prepare(q).bind(...params).all();
      const nextBefore = (results || []).length >= limit ? results[results.length - 1]._rid : null;
      const rows = chipSearch
        ? (results || []).filter(p => inHomeRegion(p, country) || countryNamePattern(country).test(readableText(p)))
        : results || [];
      // Country pills always include that country's Flock posts, which the limit would otherwise
      // cut once enough newer articles mention the country. Both sets are small.
      if (chipSearch && !offset) {
        const [human, commented] = await Promise.all([
          env.DB.prepare(`SELECT rowid AS _rid, * FROM posts INDEXED BY idx_posts_human_activity WHERE ${HUMAN_POSTS} AND ${cw.sql} AND ${LIVE_POSTS}`).bind(...cw.params).all(),
          env.DB.prepare(`SELECT rowid AS _rid, * FROM posts WHERE ${cw.sql} AND id IN (SELECT post_id FROM comments WHERE deleted = 0) AND ${LIVE_POSTS}`).bind(...cw.params).all()
        ]).catch(err => {
          console.error("get-posts country pill: flock posts unavailable:", err.message);
          return [{ results: [] }, { results: [] }];
        });
        const have = new Set(rows.map(p => p.id));
        for (const p of [...(human.results || []), ...(commented.results || [])]) {
          if (!have.has(p.id)) { have.add(p.id); rows.push(p); }
        }
      }
      if (isHuddleBoard && authUser?.username) await addHuddleInbox(env, rows, authUser.username);
      return json({
        posts: await publicRows(await addCommentCounts(env, rows.map(p => boolify(p, POST_BOOL_FIELDS)))),
        next_before: nextBefore
      });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /get-comments-index ───────────────────────────────────────────────────────

  if (url.pathname === "/get-comments-index") {
    try {
      const { results } = await env.DB.prepare(
        `SELECT c.id, c.post_id, c.parent_comment_id FROM comments c JOIN posts p ON p.id = c.post_id
         WHERE c.deleted = 0 AND (c.username IS NULL OR c.username != '__system__') AND (p.is_huddle = 0 OR p.is_huddle IS NULL)`
      ).all();
      return json(results || []);
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /bot-config ───────────────────────────────────────────────────────────────

  if (url.pathname === "/bot-config") {
    if (!isAdmin && !isBot) return json({ error: "Unauthorized" }, 401);
    if (request.method === "GET") {
      const row = await env.DB.prepare(`SELECT config FROM bot_config WHERE id = 1`).first();
      try {
        return json({ config: row?.config ? JSON.parse(row.config) : null });
      } catch { return json({ config: null }); }
    }
    if (!isAdmin) return json({ error: "Unauthorized" }, 401);
    if (!body.config) return json({ error: "Missing config" }, 400);
    try {
      await env.DB.prepare(`UPDATE bot_config SET config = ?, updated_at = ? WHERE id = 1`)
        .bind(JSON.stringify(body.config), now).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /update-post ──────────────────────────────────────────────────────────────

  if (url.pathname === "/update-post") {
    if (!isBot) return json({ error: "Unauthorized" }, 401);
    if (!body.post_id || !body.content) return json({ error: "Missing fields" }, 400);
    try {
      await env.DB.prepare(`UPDATE posts SET content = ? WHERE id = ?`)
        .bind(body.content, body.post_id).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /purge-deleted ────────────────────────────────────────────────────────────

  if (url.pathname === "/purge-deleted") {
    // Switched off: deleted posts (and their photos) are kept unless an admin uses Delete forever.
    return json({ error: "Disabled: deleted posts are kept. Use Delete forever in the admin controls." }, 410);
    if (!isBot) return json({ error: "Unauthorized" }, 401);
    try {
      const { results } = await env.DB.prepare(
        `SELECT id FROM posts WHERE deleted = 1 LIMIT 100`
      ).all();
      if (!results || results.length === 0) return json({ success: true, purged: 0 });
      const ids = results.map(p => p.id);
      const placeholders = ids.map(() => "?").join(",");
      await env.DB.prepare(`DELETE FROM post_votes WHERE post_id IN (${placeholders})`).bind(...ids).run();
      await env.DB.prepare(`DELETE FROM comments WHERE post_id IN (${placeholders})`).bind(...ids).run();
      await env.DB.prepare(`DELETE FROM posts WHERE id IN (${placeholders})`).bind(...ids).run();
      return json({ success: true, purged: ids.length });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /delete-post ──────────────────────────────────────────────────────────────

  if (url.pathname === "/delete-post") {
    if (!isBot) return json({ error: "Unauthorized" }, 401);
    if (!body.post_id) return json({ error: "Missing fields" }, 400);
    try {
      await env.DB.prepare(`UPDATE posts SET deleted = 1 WHERE id = ?`).bind(body.post_id).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /add-comment ──────────────────────────────────────────────────────────────

  if (url.pathname === "/add-comment") {
    if (!username) return signInRequired();
    try {
      if (!body.content || !body.post_id) return json({ error: "Missing fields" }, 400);
      if (await isBanned()) return json({ error: "Banned" }, 403);
      const target = await env.DB.prepare(`SELECT is_huddle, huddle_members, username AS owner, locked, frozen FROM posts WHERE id = ?`).bind(body.post_id).first();
      if (target?.locked || target?.frozen) return json({ error: target.frozen ? "This post is archived" : "This post is locked" }, 403);
      if (target?.is_huddle && !seeAllHuddles && !isHuddleMember(target, username)) return json({ error: "Not a member of this huddle" }, 403);
      if (!isModerator && await isJailed()) {
        const post = await env.DB.prepare(`SELECT board, community_id FROM posts WHERE id = ?`).bind(body.post_id).first();
        const postBoard = (post?.board || post?.community_id || "").toLowerCase();
        if (!post || (postBoard !== "cage" && postBoard !== "the cage")) return json({ error: "Caged" }, 403);
        if (hasMedia(body.content)) return json({ error: CAGED_MEDIA }, 403);
      }
      const checked = !isModerator && !!target && !target.is_huddle;
      if (checked && hasSlur(userText(body.content))) return json({ error: SLUR_MSG }, 400);
      const parentCommentId = typeof body.parent_comment_id === "string" && body.parent_comment_id.trim()
        ? body.parent_comment_id.trim() : null;
      const id = crypto.randomUUID();
      await env.DB.prepare(`
        INSERT INTO comments (id, content, post_id, parent_comment_id, username, ip_hash, browser_id,
          is_mod, is_admin, moderator, mod_user_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `).bind(
        id, body.content, body.post_id, parentCommentId, username, ip_hash,
        body.browser_id || null,
        isModerator ? 1 : 0,
        isAdmin ? 1 : 0,
        isModerator ? 1 : 0,
        isModerator ? (authUser.sub ?? null) : null,
        now
      ).run();
      if (checked) ctx.waitUntil(aiCheck({ kind: "chirp", id, postId: body.post_id, text: userText(body.content), uname: username, bid: body.browser_id }));
      ctx.waitUntil(notifyMentions({ by: username, text: userText(body.content), postId: body.post_id, commentId: id }));
      await bumpPost(body.post_id);
      // Notify huddle members on new comment
      const huddlePost = await env.DB.prepare(`SELECT is_huddle, huddle_members, title, username AS post_username FROM posts WHERE id = ?`).bind(body.post_id).first();
      if (huddlePost && huddlePost.is_huddle) {
        const hMembers = JSON.parse(huddlePost.huddle_members || "[]").map(normMember);
        const allNotify = [...hMembers];
        if (huddlePost.post_username && !allNotify.includes(huddlePost.post_username)) allNotify.push(huddlePost.post_username);
        const huddleTitle = huddlePost.title || "Huddle";
        for (const mu of allNotify) {
          if (!mu || mu === username) continue;
          const notifMsg = JSON.stringify({ text: `${username || "Someone"} commented in "${huddleTitle}"`, postId: body.post_id, dk: "comment" });
          await upsertNotif(mu, notifMsg, body.post_id);
        }
      }
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /invite-to-huddle ─────────────────────────────────────────────────────────

  if (url.pathname === "/invite-to-huddle") {
    try {
      if (!username) return signInRequired();
      if (!isModerator && await isJailed()) return json({ error: "Caged" }, 403);
      const { post_id, invite_username } = body;
      if (!post_id || !invite_username) return json({ error: "Missing fields" }, 400);
      const post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ? AND deleted = 0`).bind(post_id).first();
      if (!post || !post.is_huddle) return json({ error: "Not found" }, 404);
      if (post.frozen) return json({ error: "This huddle is archived" }, 403);
      if (!seeAllHuddles && !isHuddleMember(post, username)) return json({ error: "Unauthorized" }, 403);
      const target = normMember(invite_username);
      if (!target) return json({ error: "Missing fields" }, 400);
      if ((await extinctNames()).has(target)) return json({ error: "That bird is extinct" }, 404);
      const exists = await env.DB.prepare(`SELECT username FROM mod_users WHERE LOWER(username) = ? AND deleted_at IS NULL LIMIT 1`).bind(target.toLowerCase()).first();
      if (!exists) return json({ error: "No bird by that name" }, 404);
      if (isHuddleMember(post, target)) return json({ error: "Already in the huddle" }, 400);
      if (await pendingRequest(post_id, "invite", target)) return json({ error: `${target} already has an invite` }, 400);
      const isOwner = username.toLowerCase() === (post.username || "").toLowerCase();
      // The owner (and mods) invite straight away; anyone else asks the owner first
      if (isOwner || isModerator) {
        await sendInvite(post, username, target);
        return json({ success: true, pending: true, kind: "invite", message: `Invite sent to ${target}` });
      }
      if (await pendingRequest(post_id, "add", target)) return json({ error: `Someone already asked to invite ${target}` }, 400);
      await newRequest(post, "add", username, target, null);
      return json({ success: true, pending: true, kind: "add", message: `Asked ${post.username} to invite ${target}` });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /huddle-respond: accept / decline an invite, or approve / deny a member's request ──
  if (url.pathname === "/huddle-respond" && request.method === "POST") {
    try {
      if (!username) return signInRequired();
      const rq = await env.DB.prepare(`SELECT * FROM huddle_requests WHERE id = ?`).bind(String(body.req_id || "")).first();
      if (!rq) return json({ error: "Not found" }, 404);
      const me = username.toLowerCase();
      const post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ? AND deleted = 0`).bind(rq.post_id).first();
      const owner = (post?.username || "").toLowerCase();
      const mine = rq.kind === "invite" ? rq.target.toLowerCase() === me : owner === me;
      if (!mine) return json({ error: rq.kind === "invite" ? "This invite isn't for you" : "Only the huddle's owner can answer this" }, 403);
      if (rq.status !== "pending") return json({ success: true, status: rq.status });
      const settle = st => env.DB.prepare(`UPDATE huddle_requests SET status = ?, decided_at = ? WHERE id = ?`).bind(st, now, rq.id).run();
      if (!post || !post.is_huddle) { await settle("expired"); return json({ error: "This huddle doesn't exist anymore", status: "expired" }, 410); }
      if (post.frozen) return json({ error: "This huddle is archived" }, 403);
      if (rq.created_at < requestCutoff()) { await settle("expired"); return json({ error: "This request expired", status: "expired" }, 410); }
      const yes = body.accept === true, title = post.title || "Huddle";
      const tell = (who, text) => who && who.toLowerCase() !== me ? upsertNotif(who, JSON.stringify({ text, postId: post.id }), post.id) : null;
      let status;
      if (rq.kind === "invite") {
        if (yes) {
          if (!isHuddleMember(post, rq.target)) {
            const members = JSON.parse(post.huddle_members || "[]");
            members.push(rq.target_role ? `${rq.target}:${rq.target_role}` : rq.target);
            await env.DB.prepare(`UPDATE posts SET huddle_members = ?, last_activity = ? WHERE id = ?`).bind(JSON.stringify(members), now, post.id).run();
          }
          await huddleLine(post.id, `👋 ${rq.target} joined the huddle`, now);
          await tell(rq.from_user, `${rq.target} accepted your invite to "${title}"`);
          if (owner !== rq.from_user.toLowerCase()) await tell(post.username, `${rq.target} joined "${title}"`);
          status = "accepted";
        } else {
          await huddleLine(post.id, `🚫 ${rq.target} declined the invite`, now);
          await tell(rq.from_user, `${rq.target} declined your invite to "${title}"`);
          if (owner !== rq.from_user.toLowerCase()) await tell(post.username, `${rq.target} declined the invite to "${title}"`);
          status = "declined";
        }
      } else if (rq.kind === "add") {
        if (yes) {
          await sendInvite(post, rq.from_user, rq.target);
          await tell(rq.from_user, `${post.username} approved inviting ${rq.target} to "${title}"`);
          status = "approved";
        } else {
          await tell(rq.from_user, `${post.username} said no to inviting ${rq.target} to "${title}"`);
          status = "denied";
        }
      } else {
        if (yes) {
          const members = JSON.parse(post.huddle_members || "[]");
          const rest = members.filter(m => normMember(m).toLowerCase() !== rq.target.toLowerCase());
          if (rest.length !== members.length) {
            await env.DB.prepare(`UPDATE posts SET huddle_members = ? WHERE id = ?`).bind(JSON.stringify(rest), post.id).run();
            await huddleLine(post.id, `💨 ${rq.target} was removed from the huddle`, now);
            await tell(rq.target, `You were removed from "${title}"`);
          }
          await tell(rq.from_user, `${post.username} removed ${rq.target} from "${title}" as you asked`);
          status = "approved";
        } else {
          await tell(rq.from_user, `${post.username} kept ${rq.target} in "${title}"`);
          status = "denied";
        }
      }
      await settle(status);
      return json({ success: true, status, postId: post.id });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /huddle-cancel: the owner (or whoever sent it) takes back a pending invite ──
  if (url.pathname === "/huddle-cancel" && request.method === "POST") {
    try {
      if (!username) return signInRequired();
      const rq = await env.DB.prepare(`SELECT * FROM huddle_requests WHERE id = ?`).bind(String(body.req_id || "")).first();
      if (!rq || rq.status !== "pending") return json({ error: "Not found" }, 404);
      const post = await env.DB.prepare(`SELECT username FROM posts WHERE id = ?`).bind(rq.post_id).first();
      const me = username.toLowerCase();
      if (me !== rq.from_user.toLowerCase() && me !== (post?.username || "").toLowerCase() && !isModerator) return json({ error: "Unauthorized" }, 403);
      await env.DB.prepare(`UPDATE huddle_requests SET status = 'cancelled', decided_at = ? WHERE id = ?`).bind(now, rq.id).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /edit-huddle-title ────────────────────────────────────────────────────────

  if (url.pathname === "/edit-huddle-title") {
    try {
      if (!username) return signInRequired();
      if (!isModerator && await isJailed()) return json({ error: "Caged" }, 403);
      const { post_id, title } = body;
      if (!post_id) return json({ error: "Missing post_id" }, 400);
      const post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ? AND deleted = 0`).bind(post_id).first();
      if (!post || !post.is_huddle) return json({ error: "Not found" }, 404);
      if (post.frozen) return json({ error: "This huddle is archived" }, 403);
      const isCreator = username.toLowerCase() === (post.username || "").toLowerCase();
      if (!isCreator && !isModerator) return json({ error: "Unauthorized" }, 403);
      await env.DB.prepare(`UPDATE posts SET title = ? WHERE id = ?`).bind(title || null, post_id).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /leave-huddle ────────────────────────────────────────────────────────────

  if (url.pathname === "/leave-huddle") {
    try {
      const { post_id } = body;
      if (!post_id) return json({ error: "Missing post_id" }, 400);
      const leavingUser = username || null;
      if (!leavingUser) return json({ error: "Must be logged in to leave a huddle" }, 401);
      const post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ? AND deleted = 0`).bind(post_id).first();
      if (!post || !post.is_huddle) return json({ error: "Not found" }, 404);
      if (post.frozen) return json({ error: "This huddle is archived" }, 403);
      if (post.username && post.username.toLowerCase() === leavingUser.toLowerCase()) {
        await huddleLine(post_id, `👋 ${leavingUser} left the huddle`, now);
        const next = await passHuddleOn(post, now);
        return json({ success: true, deleted: !next });
      }
      // For members: remove from huddle_members
      const members = JSON.parse(post.huddle_members || "[]");
      const newMembers = members.filter(m => normMember(m).toLowerCase() !== leavingUser.toLowerCase());
      if (newMembers.length === members.length) {
        return json({ error: "Not a member of this huddle" }, 403);
      }
      await env.DB.prepare(`UPDATE posts SET huddle_members = ? WHERE id = ?`)
        .bind(JSON.stringify(newMembers), post_id).run();
      await env.DB.prepare(`INSERT INTO comments (id, content, post_id, parent_comment_id, username, ip_hash, browser_id, is_mod, is_admin, moderator, mod_user_id, created_at) VALUES (?, ?, ?, NULL, '__system__', NULL, NULL, 0, 0, 0, NULL, ?)`)
        .bind(crypto.randomUUID(), `👋 ${leavingUser} left the huddle`, post_id, now).run().catch(() => {});
      // Notify all remaining members (+ creator) that someone left
      const leaveTitle = post.title || "Huddle";
      const remaining = [...newMembers.map(normMember), post.username].filter(Boolean);
      for (const mu of remaining) {
        if (!mu || mu === leavingUser) continue;
        const leaveMsg = JSON.stringify({ text: `${leavingUser} left "${leaveTitle}"`, postId: post_id });
        await upsertNotif(mu, leaveMsg, post_id);
      }
      // Notify the leaver so they see it in their own panel
      await upsertNotif(leavingUser, JSON.stringify({ text: `You left "${leaveTitle}"`, postId: post_id }), post_id);
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /remove-from-huddle ───────────────────────────────────────────────────────

  if (url.pathname === "/remove-from-huddle") {
    try {
      if (!username) return signInRequired();
      const { post_id, remove_username } = body;
      if (!post_id || !remove_username) return json({ error: "Missing fields" }, 400);
      const effectiveUsername = username;
      const post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ? AND deleted = 0`).bind(post_id).first();
      if (!post || !post.is_huddle) return json({ error: "Not found" }, 404);
      if (post.frozen) return json({ error: "This huddle is archived" }, 403);
      const isCreator = effectiveUsername.toLowerCase() === (post.username || "").toLowerCase();
      const members = JSON.parse(post.huddle_members || "[]");
      const targetMember = members.find(m => normMember(m).toLowerCase() === remove_username.toLowerCase());
      if (!targetMember) return json({ error: "Not a member" }, 404);
      if (!isCreator && !isModerator) {
        // Members ask the owner, who approves or denies it
        if (!isHuddleMember(post, effectiveUsername)) return json({ error: "Unauthorized" }, 403);
        const target = normMember(targetMember);
        if (target.toLowerCase() === effectiveUsername.toLowerCase()) return json({ error: "Use Leave to leave the huddle" }, 400);
        const r = targetMember.slice(targetMember.lastIndexOf(":") + 1);
        if (targetMember.includes(":") && (r === "admin" || r === "mod")) return json({ error: "Cannot remove mods or admins" }, 403);
        if (await pendingRequest(post_id, "remove", target)) return json({ error: `Someone already asked to remove ${target}` }, 400);
        await newRequest(post, "remove", effectiveUsername, target, null);
        return json({ success: true, pending: true, kind: "remove", message: `Asked ${post.username} to remove ${target}` });
      }
      // OP cannot remove mods or admins
      if (isCreator && !isModerator) {
        const lastColon = targetMember.lastIndexOf(":");
        const targetRole = lastColon > 0 ? targetMember.slice(lastColon + 1) : null;
        if (targetRole === "admin" || targetRole === "mod") return json({ error: "Cannot remove mods or admins" }, 403);
      }
      const newMembers = members.filter(m => normMember(m).toLowerCase() !== remove_username.toLowerCase());
      await env.DB.prepare(`UPDATE posts SET huddle_members = ? WHERE id = ?`).bind(JSON.stringify(newMembers), post_id).run();
      const sysContent = `💨 ${remove_username} was removed from the huddle`;
      const sysId = crypto.randomUUID();
      await env.DB.prepare(`INSERT INTO comments (id, content, post_id, parent_comment_id, username, ip_hash, browser_id, is_mod, is_admin, moderator, mod_user_id, created_at) VALUES (?, ?, ?, NULL, '__system__', NULL, NULL, 0, 0, 0, NULL, ?)`)
        .bind(sysId, sysContent, post_id, now).run().catch(() => {});
      const huddleTitle = post.title || "Huddle";
      await upsertNotif(remove_username, JSON.stringify({ text: `You were removed from "${huddleTitle}"`, postId: post_id }), post_id);
      const remaining = [...newMembers.map(normMember), post.username].filter(Boolean);
      for (const mu of remaining) {
        if (!mu || mu === effectiveUsername || mu === remove_username) continue;
        await upsertNotif(mu, JSON.stringify({ text: `${effectiveUsername} removed ${remove_username} from "${huddleTitle}"`, postId: post_id }), post_id);
      }
      // Notify the actor (remover) so they see it in their own panel
      await upsertNotif(effectiveUsername, JSON.stringify({ text: `You removed ${remove_username} from "${huddleTitle}"`, postId: post_id }), post_id);
      const updatedPost = { ...post, huddle_members: JSON.stringify(newMembers) };
      return json({ success: true, post: boolify(updatedPost, POST_BOOL_FIELDS), systemComment: { id: sysId, content: sysContent, username: "__system__", created_at: now, parent_comment_id: null, browser_id: null, is_mod: 0 } });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /pin-huddle-comment ───────────────────────────────────────────────────────

  if (url.pathname === "/pin-huddle-comment") {
    try {
      if (!username) return signInRequired();
      const { post_id, comment_id, pinned } = body;
      if (!post_id || !comment_id || pinned === undefined) return json({ error: "Missing fields" }, 400);
      const effectiveUsername = username;
      const post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ? AND deleted = 0`).bind(post_id).first();
      if (!post) return json({ error: "Post not found" }, 404);
      if (post.frozen) return json({ error: "This post is archived" }, 403);
      // The post's creator (OP) may pin/unpin their own chirps on their own post; mods use mod-action
      const isCreator = effectiveUsername.toLowerCase() === (post.username || "").toLowerCase();
      if (!isCreator && !isModerator) return json({ error: "Unauthorized" }, 403);
      if (!isModerator) {
        const cm = await env.DB.prepare(`SELECT username FROM comments WHERE id = ? AND post_id = ? AND deleted = 0`).bind(comment_id, post_id).first();
        if (!cm) return json({ error: "Chirp not found" }, 404);
        if ((cm.username || "").toLowerCase() !== effectiveUsername.toLowerCase()) return json({ error: "You can only pin your own chirps" }, 403);
      }
      await env.DB.prepare(`UPDATE comments SET pinned = ? WHERE id = ? AND post_id = ?`).bind(pinned ? 1 : 0, comment_id, post_id).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /vote-post ────────────────────────────────────────────────────────────────

  // ── /hunt/* ── the globe's worm hunt (shared). Each signed-in bird flies at one fixed speed; the server keeps
  // every flight (from, to, departure, arrival) so it always knows where a bird can really be. Worms are rare, appear
  // near birds that are hunting (more at night and near trending stories), last ~30 s and go to the first bird that
  // reaches them. A catch only counts if the bird's own flight passes within reach of the worm — scripts can't
  // teleport. Caught worms land in the normal worm balance (a worms row from '__hunt__', no post).
  if (url.pathname.startsWith("/hunt/") && request.method === "POST") {
    if (!username || isBot) return signInRequired();
    const HS = env.HUNT_FAST ? 1 : 0;                       // local testing only: worms appear quickly
    const SPEED = 0.5;                                    // km per second (a phone screen at hunt zoom in ~12 s; Ireland in ~9 min)
    const REACH = 0.3;                                    // km — a worm this close to your flight path is caught
    const LIFE = 40000, GOLD_LIFE = 30000, NEAR = 25;     // worm life (ms); what you can see around you (km)
    // a worm comes up, crawls a little, goes back under, and comes up again a few km away (same code on the globe page)
    const wormPlan = w => { let h = 2166136261; for (const ch of String(w.id)) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619); }
      let a = h >>> 0; const rnd = () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
      const segs = []; let t = w.born, x = 0, y = 0;
      while (t < w.gone) { const up = 4500 + rnd() * 3500, s = { a: t, b: Math.min(w.gone, t + up), x, y, hd: rnd() * 6.2832, ph: rnd() * 6.2832 }; segs.push(s);
        const e = wormOff(s, (s.b - s.a) / 1000), jd = rnd() * 6.2832, j = 0.13 + rnd() * 0.27; x = e[0] + Math.cos(jd) * j; y = e[1] + Math.sin(jd) * j; t += up + 2500 + rnd() * 3000; }
      return segs; };
    const wormOff = (s, u) => { const wob = 0.08 * Math.sin(u * 1.3 + s.ph); return [s.x + 0.055 * u * Math.cos(s.hd) - wob * Math.sin(s.hd), s.y + 0.055 * u * Math.sin(s.hd) + wob * Math.cos(s.hd)]; };
    const wormAt = (w, t) => { const segs = w._p || (w._p = wormPlan(w)), toLL = o => [w.lat + o[1] / 111.2, w.lng + o[0] / (111.2 * Math.cos(w.lat * Math.PI / 180))];
      for (const s of segs) { if (t >= s.a && t < s.b) { const ll = toLL(wormOff(s, (t - s.a) / 1000)); return { up: true, lat: ll[0], lng: ll[1], fromUp: t - s.a, toDown: s.b - t }; }
        if (t < s.a) { const ll = toLL([s.x, s.y]); return { up: false, lat: ll[0], lng: ll[1], toUp: s.a - t }; } }
      const l = segs[segs.length - 1], ll = l ? toLL(wormOff(l, (l.b - l.a) / 1000)) : [w.lat, w.lng]; return { up: false, lat: ll[0], lng: ll[1], toUp: Infinity }; };
    const R = Math.PI / 180, now = Date.now();
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
    const flyFor = T => (T + 40 / SPEED) * 1000;    // a flight lasts its turn plus 40 km straight on (the page carries on before then)
    const posAt = (b, t) => b ? flyAt(flight(b), t) : null;
    const okLL = (la, lo) => Number.isFinite(la) && Number.isFinite(lo) && Math.abs(la) <= 85 && Math.abs(lo) <= 180;
    const flight = b => b && { from: [b.from_lat, b.from_lng], to: [b.to_lat, b.to_lng], b0: b.brg0 ?? null, b1: b.brg1 ?? null, depart: b.depart_at, arrive: b.arrive_at };
    try {
      let me = await env.DB.prepare(`SELECT * FROM hunt_birds WHERE username = ?`).bind(username).first();
      if (url.pathname === "/hunt/state") {
        // a new bird starts where you're looking; so does one that's been away 45 s+ when you start hunting again
        // (it can't be seen or catch anything while away, so moving it then gains nothing)
        if (!me || (body.start && me.seen_at < now - 45000 && okLL(+body.lat, +body.lng))) {
          const la = +body.lat, lo = +body.lng; if (!okLL(la, lo)) return json({ error: "Where are you?" }, 400);
          await env.DB.prepare(`INSERT OR REPLACE INTO hunt_birds (username, from_lat, from_lng, to_lat, to_lng, depart_at, arrive_at, seen_at, spawn_at, brg0, brg1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)`)
            .bind(username, la, lo, la, lo, now, now, now, now).run();
          me = { username, from_lat: la, from_lng: lo, to_lat: la, to_lng: lo, depart_at: now, arrive_at: now, seen_at: now, spawn_at: now };
        }
        const p = posAt(me, now);
        // occasionally a worm pops up near you: about one every ~90 s of hunting at night, ~3 min by day, a bit more
        // near trending stories; never more than 2 around you at once (within 6 km)
        const { results: live = [] } = await env.DB.prepare(`SELECT id, lat, lng, value, born_at, gone_at FROM hunt_worms WHERE gone_at > ? AND caught_by IS NULL`).bind(now).all();
        const around = live.filter(w => km(p, [w.lat, w.lng]) < 6).length;
        const dt = Math.min(10000, Math.max(0, now - (me.spawn_at || now)));
        let spawned = null;
        if (around < 2 && live.length < 300 && dt > 0) {
          const d = new Date(now), y0 = Date.UTC(d.getUTCFullYear(), 0, 0), day = Math.floor((now - y0) / 864e5), hrs = d.getUTCHours() + d.getUTCMinutes() / 60;
          const g = 2 * Math.PI / 365 * (day - 1 + (hrs - 12) / 24), decl = 0.006918 - 0.399912 * Math.cos(g) + 0.070257 * Math.sin(g) - 0.006758 * Math.cos(2 * g) + 0.000907 * Math.sin(2 * g);
          const eqt = 229.18 * (0.000075 + 0.001868 * Math.cos(g) - 0.032077 * Math.sin(g) - 0.014615 * Math.cos(2 * g) - 0.040849 * Math.sin(2 * g)), sLng = -15 * (hrs - 12 + eqt / 60);
          const night = Math.sin(p[0] * R) * Math.sin(decl) + Math.cos(p[0] * R) * Math.cos(decl) * Math.cos((p[1] - sLng) * R) < 0;
          let story = null;
          try { const gc = await env.DB.prepare(`SELECT v FROM globe_cache WHERE k = 'trending'`).first(); const st = gc ? (JSON.parse(gc.v).stories || []) : [];
            for (const s of st) { const o = s.origin || s; const ll = [o.lat ?? s.lat, o.lng ?? s.lng]; if (okLL(+ll[0], +ll[1]) && km(p, ll) < 6) { story = ll; break; } } } catch (e) {}
          const mean = (HS ? 5000 : (night ? 90000 : 180000)) * (story ? 0.7 : 1);
          if (Math.random() < dt / mean) {
            let base = p, r0 = 1, r1 = 4;
            if (story && Math.random() < 0.5) { base = story; r0 = 0.25; r1 = 1.75; }
            // worms only come up on land, at least 0.7 km in from any shore (they crawl a little); over open sea, none come
            const ring = (c, b, d) => { const la = Math.asin(Math.sin(c[0] * R) * Math.cos(d) + Math.cos(c[0] * R) * Math.sin(d) * Math.cos(b));
              return [la / R, (((c[1] * R + Math.atan2(Math.sin(b) * Math.sin(d) * Math.cos(c[0] * R), Math.cos(d) - Math.sin(c[0] * R) * Math.sin(la))) / R + 540) % 360) - 180]; };
            let spot = null;
            for (let k = 0; k < 10 && !spot; k++) { const q = ring(base, Math.random() * 2 * Math.PI, (r0 + Math.random() * (r1 - r0)) / 6371);
              if (Math.abs(q[0]) < 84 && isLand(q[0], q[1]) && [0, 1, 2, 3, 4, 5].every(i => { const e = ring(q, i * Math.PI / 3, 0.7 / 6371); return isLand(e[0], e[1]); })) spot = q; }
            const gold = Math.random() < 0.06, w = spot && { id: crypto.randomUUID(), lat: spot[0], lng: spot[1], value: gold ? 5 : 1, born_at: now, gone_at: now + (gold ? GOLD_LIFE : LIFE) };
            if (w) { await env.DB.prepare(`INSERT INTO hunt_worms (id, lat, lng, value, born_at, gone_at) VALUES (?, ?, ?, ?, ?, ?)`).bind(w.id, w.lat, w.lng, w.value, w.born_at, w.gone_at).run(); live.push(w); spawned = w.id; }
          }
        }
        await env.DB.prepare(`UPDATE hunt_birds SET seen_at = ?, spawn_at = ? WHERE username = ?`).bind(now, now, username).run();
        const { results: birds = [] } = await env.DB.prepare(`SELECT * FROM hunt_birds WHERE seen_at > ? AND username != ?`).bind(now - 45000, username).all();
        if (Math.random() < 0.02) ctx.waitUntil(env.DB.prepare(`DELETE FROM hunt_worms WHERE gone_at < ?`).bind(now - 3600e3).run().catch(() => {}));
        return json({ now, me: flight(me), balance: await wormBalance(username),
          birds: birds.filter(b => km(p, posAt(b, now)) < 50).slice(0, 30).map(b => ({ u: b.username, ...flight(b) })),
          worms: live.filter(w => km(p, [w.lat, w.lng]) < NEAR).map(w => ({ id: w.id, lat: w.lat, lng: w.lng, v: w.value, born: w.born_at, gone: w.gone_at })), spawned });
      }
      if (!me) return json({ error: "Start the hunt first" }, 400);
      if (url.pathname === "/hunt/fly") {
        // a new heading: the bird turns from the way it's going now (gliding round), then flies straight on
        const brg = +body.brg; if (!Number.isFinite(brg) || Math.abs(brg) > 100) return json({ error: "Bad heading" }, 400);
        const f0 = flight(me), p = posAt(me, now), h = now < me.arrive_at ? headAt(f0, now) : null;
        const f = fTurn({ from: p, to: p, b0: h == null ? brg : h, b1: brg, depart: now }); f.arrive = now + Math.round(flyFor(f._T));
        await env.DB.prepare(`UPDATE hunt_birds SET from_lat = ?, from_lng = ?, to_lat = ?, to_lng = ?, brg0 = ?, brg1 = ?, depart_at = ?, arrive_at = ?, seen_at = ? WHERE username = ?`)
          .bind(p[0], p[1], p[0], p[1], f.b0, f.b1, now, f.arrive, now, username).run();
        return json({ now, me: { from: p, to: p, b0: f.b0, b1: f.b1, depart: now, arrive: f.arrive } });
      }
      if (url.pathname === "/hunt/catch") {
        const w = await env.DB.prepare(`SELECT * FROM hunt_worms WHERE id = ?`).bind(String(body.id || "")).first();
        if (!w) return json({ error: "No worm" }, 404);
        if (w.caught_by) return json({ taken: true, by: w.caught_by === username ? null : w.caught_by }, 409);
        if (w.gone_at < now - 1500) return json({ gone: true }, 410);
        // where could this bird have been over the last 2.5 s? (allows for the phone being a moment behind)
        // the worm has to be above ground, and your bird within reach of it, at the same moment
        const ww = { id: w.id, lat: w.lat, lng: w.lng, born: w.born_at, gone: w.gone_at };
        let near = Infinity; for (let k = 0; k <= 20; k++) { const t = now - 2500 + k * 125; const q = wormAt(ww, t); if (!q.up) continue; near = Math.min(near, km(posAt(me, t), [q.lat, q.lng])); }
        if (near > REACH) return json({ far: true, km: Math.round(near) }, 400);
        const up = await env.DB.prepare(`UPDATE hunt_worms SET caught_by = ?, caught_at = ? WHERE id = ? AND caught_by IS NULL`).bind(username, now, w.id).run();
        if (!up.meta || !up.meta.changes) return json({ taken: true }, 409);
        const iso = new Date(now).toISOString(), ins = env.DB.prepare(`INSERT INTO worms (id, giver, receiver, post_id, comment_id, created_at) VALUES (?, '__hunt__', ?, NULL, NULL, ?)`);
        await env.DB.batch(Array.from({ length: w.value }, () => ins.bind(crypto.randomUUID(), username, iso)));
        return json({ ok: true, value: w.value, balance: await wormBalance(username) });
      }
      return json({ error: "Not found" }, 404);
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /give-worm ─────────────────────────────────────────────────────────────
  // body: { post_id } or { comment_id }. One worm per call (people can give as many as they like); it goes to the
  // post's author, or for a chirp to whoever wrote the chirp. Bots, system lines and archived posts can't get worms.
  if (url.pathname === "/give-worm" && request.method === "POST") {
    if (!username) return signInRequired();
    try {
      if (await isBanned()) return json({ error: "Banned" }, 403);
      let receiver = null, post = null, postId = null, commentId = null;
      if (body.comment_id) {
        const cm = await env.DB.prepare(`SELECT id, username, post_id, deleted FROM comments WHERE id = ?`).bind(String(body.comment_id)).first();
        if (!cm || cm.deleted) return json({ error: "That chirp is gone" }, 404);
        receiver = cm.username; commentId = cm.id;
        post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ?`).bind(cm.post_id).first();
      } else if (body.post_id) {
        post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ?`).bind(String(body.post_id)).first();
        receiver = post && post.username; postId = post && post.id;
      } else return json({ error: "Missing post_id or comment_id" }, 400);
      if (!post || post.deleted) return json({ error: "That post is gone" }, 404);
      if (post.frozen) return json({ error: "This post is archived" }, 403);
      if (post.is_huddle && !isHuddleMember(post, username)) return json({ error: "Not found" }, 404);
      if (!receiver || receiver === "__system__" || ["NewsBot", "ScienceBot", "NatureBot", "SportsBot"].includes(receiver) || String(post.browser_id || "").startsWith("bot-") && postId)
        return json({ error: "Worms only go to people" }, 400);
      const count = Math.max(1, Math.min(50, parseInt(body.count) || 1));
      if (receiver.toLowerCase() === username.toLowerCase()) return json({ error: "You can't give worms to yourself" }, 400);
      const have = await wormBalance(username);
      if (have < count) return json({ error: have ? `You only have ${have} worm${have === 1 ? "" : "s"}` : "You don't have any worms to give", balance: have }, 400);
      const ins = env.DB.prepare(`INSERT INTO worms (id, giver, receiver, post_id, comment_id, created_at) VALUES (?, ?, ?, ?, ?, ?)`);
      await env.DB.batch(Array.from({ length: count }, () => ins.bind(crypto.randomUUID(), username, receiver, postId, commentId, now)));
      await bumpPost(post.id); // worms count as activity: the post rises in Flock
      const col = commentId ? "comment_id" : "post_id", id = commentId || postId;
      const r = await env.DB.prepare(`SELECT COUNT(*) AS n, SUM(CASE WHEN giver = ? THEN 1 ELSE 0 END) AS m FROM worms WHERE ${col} = ?`).bind(username, id).first();
      const pr = postId ? (await postResp([postId], username))[postId] : null;
      return json({ success: true, worms: r?.n || 0, mine: r?.m || 0, given: count, balance: have - count, ...(pr ? { score: pr.n, myVote: pr.m } : {}) });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /worm-givers?comment_id= or ?post_id= ── who gave worms, with how many each (newest first)
  if (url.pathname === "/worm-givers") {
    try {
      const cid = url.searchParams.get("comment_id"), pid = url.searchParams.get("post_id");
      if (!cid && !pid) return json({ givers: [] });
      const postId = pid || (await env.DB.prepare(`SELECT post_id FROM comments WHERE id = ?`).bind(cid).first())?.post_id;
      const post = postId && await env.DB.prepare(`SELECT id, deleted, is_huddle, huddle_members, username FROM posts WHERE id = ?`).bind(postId).first();
      if (!post || post.deleted || (post.is_huddle && !seeAllHuddles && !isHuddleMember(post, username))) return json({ givers: [] });
      const { results = [] } = await env.DB.prepare(`SELECT giver AS username, COUNT(*) AS c, MAX(created_at) AS t FROM worms WHERE ${cid ? "comment_id" : "post_id"} = ? GROUP BY giver ORDER BY t DESC`).bind(cid || pid).all();
      const extinct = await extinctNames();
      return json({ givers: results.map(r => ({ username: extinct.has(r.username) ? EXTINCT_NAME : r.username, c: r.c })) });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /my-worms ── how many worms you have to give
  if (url.pathname === "/my-worms") {
    if (!username) return signInRequired();
    try { return json({ balance: await wormBalance(username) }); } catch (err) { return serverError(err); }
  }

  // ── /post-responses?post_ids=a,b ── the bird number for each post (people who responded) and what you did
  // ── /globe-counts?ids= ── the globe page's article previews show flaps / chirps / shares (user's request,
  // 2026-11-24): { posts: { id: { f: flaps, m: 1 if you flapped, c: chirps, s: shares } } }
  if (url.pathname === "/globe-counts") {
    try {
      const ids = (url.searchParams.get("ids") || "").split(",").filter(Boolean).slice(0, 40);
      if (!ids.length) return json({ posts: {} });
      const [pr, { results: cc = [] }, { results: sc = [] }] = await Promise.all([
        postResp(ids, username),
        env.DB.prepare(`SELECT post_id, COUNT(*) AS n FROM comments WHERE post_id IN (${ID_LIST}) AND deleted = 0 AND (username IS NULL OR username != '__system__') GROUP BY post_id`).bind(JSON.stringify(ids)).all(),
        env.DB.prepare(`SELECT id, share_count FROM posts WHERE id IN (${ID_LIST})`).bind(JSON.stringify(ids)).all()]);
      const c = Object.fromEntries(cc.map(r => [r.post_id, r.n])), s = Object.fromEntries(sc.map(r => [r.id, r.share_count || 0]));
      const posts = {};
      for (const id of ids) posts[id] = { f: pr[id]?.n || 0, m: pr[id]?.m === 1 ? 1 : 0, c: c[id] || 0, s: s[id] || 0 };
      return json({ posts });
    } catch (err) {
      return serverError(err);
    }
  }

  if (url.pathname === "/post-responses") {
    try {
      const ids = (url.searchParams.get("post_ids") || "").split(",").filter(Boolean).slice(0, 120);
      return json({ posts: ids.length ? await postResp(ids, username) : {} });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /react-post ── body: { post_id, emoji }. One emoji per person per post: the same one again removes it,
  // a different one replaces it. Answers with the new people-count and what you did.
  if (url.pathname === "/react-post" && request.method === "POST") {
    if (!username) return signInRequired();
    try {
      if (await isBanned()) return json({ error: "Banned" }, 403);
      return json({ error: "Posts take flaps and worms" }, 400);
      const emoji = String(body.emoji || "").slice(0, 16);
      const post = await env.DB.prepare(`SELECT id, deleted, frozen, is_huddle FROM posts WHERE id = ?`).bind(String(body.post_id || "")).first();
      if (!post || post.deleted) return json({ error: "That post is gone" }, 404);
      if (post.frozen) return json({ error: "This post is archived" }, 403);
      if (post.is_huddle) return json({ error: "Huddle posts don't take reactions" }, 400);
      const cur = await env.DB.prepare(`SELECT id, emoji FROM post_reactions WHERE post_id = ? AND username = ?`).bind(post.id, username).first();
      if (cur && cur.emoji === emoji) await env.DB.prepare(`DELETE FROM post_reactions WHERE id = ?`).bind(cur.id).run();
      else if (cur) await env.DB.prepare(`UPDATE post_reactions SET emoji = ?, created_at = ? WHERE id = ?`).bind(emoji, now, cur.id).run();
      else await env.DB.prepare(`INSERT INTO post_reactions (id, post_id, username, emoji, created_at) VALUES (?, ?, ?, ?, ?)`).bind(crypto.randomUUID(), post.id, username, emoji, now).run();
      const pr = (await postResp([post.id], username))[post.id];
      return json({ success: true, score: pr.n, myVote: pr.m, emoji: pr.emoji });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /post-reactions?post_id= ── who did what on a post: one row per person (flapped, emoji, worms given)
  if (url.pathname === "/post-reactions") {
    try {
      const pid = url.searchParams.get("post_id") || "";
      const post = await env.DB.prepare(`SELECT id, deleted, is_huddle, huddle_members, username FROM posts WHERE id = ?`).bind(pid).first();
      if (!post || post.deleted || (post.is_huddle && !seeAllHuddles && !isHuddleMember(post, username))) return json({ people: [] });
      const e = [];
      const [{ results: f = [] }, { results: w = [] }] = await Promise.all([
        env.DB.prepare(`SELECT username, created_at FROM post_votes WHERE post_id = ? AND value > 0 AND username IS NOT NULL`).bind(pid).all(),
        env.DB.prepare(`SELECT giver AS username, COUNT(*) AS c, MAX(created_at) AS created_at FROM worms WHERE post_id = ? GROUP BY giver`).bind(pid).all()]);
      const by = new Map(), row = u => by.get(u) || (by.set(u, { username: u, flap: false, emoji: null, worms: 0, t: "" }), by.get(u));
      for (const r of f) { const o = row(r.username); o.flap = true; if (r.created_at > o.t) o.t = r.created_at; }
      for (const r of e) { const o = row(r.username); o.emoji = r.emoji; if (r.created_at > o.t) o.t = r.created_at; }
      for (const r of w) { const o = row(r.username); o.worms = r.c; if (r.created_at > o.t) o.t = r.created_at; }
      const extinct = await extinctNames();
      const people = [...by.values()].sort((a, b) => b.t.localeCompare(a.t)).map(o => extinct.has(o.username) ? { ...o, username: EXTINCT_NAME } : o);
      return json({ people });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /worm-counts ───────────────────────────────────────────────────────────
  // body: { posts: [ids], comments: [ids] } -> { posts: { id: { n, m } }, comments: { id: { n, m } } }  (n = total, m = given by you)
  if (url.pathname === "/worm-counts" && request.method === "POST") {
    try {
      const out = { posts: {}, comments: {} };
      for (const [key, col] of [["posts", "post_id"], ["comments", "comment_id"]]) {
        const ids = (Array.isArray(body[key]) ? body[key] : []).map(String).slice(0, 300);
        for (let i = 0; i < ids.length; i += 90) {
          const chunk = ids.slice(i, i + 90);
          const { results = [] } = await env.DB.prepare(
            `SELECT ${col} AS id, COUNT(*) AS n, SUM(CASE WHEN giver = ? THEN 1 ELSE 0 END) AS m FROM worms WHERE ${col} IN (${chunk.map(() => "?").join(",")}) GROUP BY ${col}`
          ).bind(username || "", ...chunk).all();
          for (const r of results) out[key][r.id] = { n: r.n, m: r.m || 0, g: [] };
          // who gave (newest first), so the page can show the list without another request
          const have = chunk.filter(id => out[key][id]);
          if (have.length) {
            const { results: gv = [] } = await env.DB.prepare(
              `SELECT ${col} AS id, giver AS username, COUNT(*) AS c, MAX(created_at) AS t FROM worms WHERE ${col} IN (${have.map(() => "?").join(",")}) GROUP BY ${col}, giver ORDER BY t DESC`
            ).bind(...have).all();
            for (const r of gv) out[key][r.id].g.push({ username: r.username, c: r.c });
          }
        }
      }
      return json(out);
    } catch (err) {
      return serverError(err);
    }
  }

  if (url.pathname === "/vote-post") {
    if (!username) return signInRequired();
    try {
      if (!body.post_id || !body.browser_id || ![1, 0].includes(body.value))
        return json({ error: "Missing or invalid fields" }, 400);
      if (await isBanned()) return json({ error: "Banned" }, 403);
      const votedPost = await env.DB.prepare(`SELECT frozen, username FROM posts WHERE id = ?`).bind(body.post_id).first();
      if (votedPost?.frozen) return json({ error: "This post is archived" }, 403);
      // no flapping your own post (everyone can see who flapped)
      if (body.value === 1 && votedPost?.username && votedPost.username.toLowerCase() === username.toLowerCase())
        return json({ error: "You can't flap your own post" }, 400);

      // Read current state BEFORE write to avoid D1 eventual-consistency race
      const [existing, preSummary] = await Promise.all([
        // Your vote is found by your account, never by a device id the request sends (those are visible on posts)
        env.DB.prepare(`SELECT id, value FROM post_votes WHERE post_id = ? AND username = ?`).bind(body.post_id, username).first(),
        getPostVoteSummary(body.post_id, body.browser_id),
      ]);
      const prevValue = existing?.value || 0;
      const prevScore = preSummary.score;
      const prevCount = preSummary.voteCount;

      if (body.value === 0) {
        // remove every flap row you have on this post: older flaps were saved once per device, so one person
        // can have several rows, and deleting just one left the post still flapped
        if (existing?.id) {
          await env.DB.prepare(`DELETE FROM post_votes WHERE post_id = ? AND username = ?`).bind(body.post_id, username).run();
        }
        const pr = (await postResp([body.post_id], username))[body.post_id];
        return json({ success: true, score: pr.n, myVote: pr.m, voteCount: pr.n });
      }

      // Flaps belong to the account. The table still has the old one-per-device rule UNIQUE(post_id, browser_id), so the
      // row's browser_id is the account ("u:<name>"), not the device: otherwise a second account on the same phone
      // couldn't flap a post the first account had flapped (the insert failed and nothing happened)
      if (existing?.id) {
        await env.DB.prepare(`UPDATE post_votes SET value = ?, username = ?, ip_hash = NULL, is_mod = ?, mod_user_id = ? WHERE id = ?`)
          .bind(body.value, username, isModerator ? 1 : 0, isModerator ? authUser.sub : null, existing.id).run();
      } else {
        await env.DB.prepare(`
          INSERT INTO post_votes (id, post_id, browser_id, value, username, ip_hash, is_mod, mod_user_id, created_at)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        `).bind(crypto.randomUUID(), body.post_id, "u:" + username.toLowerCase(), body.value, username, null,
            isModerator ? 1 : 0, isModerator ? authUser.sub : null, now).run();
      }
      await bumpPost(body.post_id);
      const pr = (await postResp([body.post_id], username))[body.post_id];
      return json({ success: true, score: pr.n, myVote: pr.m, voteCount: pr.n });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /get-votes ────────────────────────────────────────────────────────────────

  if (url.pathname === "/get-votes") {
    try {
      const postIds = (url.searchParams.get("post_ids") || "").split(",").filter(Boolean);
      if (!postIds.length) return json({ votes: [] });
      const placeholders = ID_LIST;
      const { results } = await env.DB.prepare(
        `SELECT post_id, value, browser_id FROM post_votes WHERE post_id IN (${placeholders})`
      ).bind(JSON.stringify(postIds)).all();
      const bid = url.searchParams.get("bid") || "";
      const votes = [];
      for (const v of results || []) votes.push({ post_id: v.post_id, value: v.value, browser_id: await maskBid(v.browser_id, bid) });
      return json({ votes });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /get-reactions ────────────────────────────────────────────────────────────

  if (url.pathname === "/get-reactions") {
    try {
      const commentIds = (url.searchParams.get("comment_ids") || "").split(",").filter(Boolean);
      if (!commentIds.length) return json({ reactions: [] });
      const placeholders = ID_LIST;
      const { results } = await env.DB.prepare(
        `SELECT cr.comment_id, cr.browser_id, cr.emoji, cr.username, cr.created_at, p.is_huddle, p.huddle_members, p.username AS owner
         FROM comment_reactions cr LEFT JOIN comments c ON c.id = cr.comment_id LEFT JOIN posts p ON p.id = c.post_id
         WHERE cr.comment_id IN (${placeholders})`
      ).bind(JSON.stringify(commentIds)).all();
      const bid = url.searchParams.get("bid") || "";
      const out = [];
      for (const r of results || []) {
        if (r.is_huddle && !seeAllHuddles && !isHuddleMember({ huddle_members: r.huddle_members, username: r.owner }, username)) continue;
        out.push({ comment_id: r.comment_id, browser_id: await maskBid(r.browser_id, bid), emoji: r.emoji, username: r.username, created_at: r.created_at });
      }
      return json({ reactions: out });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /react-comment ────────────────────────────────────────────────────────────

  if (url.pathname === "/react-comment") {
    try {
      if (!username) return signInRequired();
      if (!body.comment_id || !body.browser_id || !body.emoji) return json({ error: "Missing fields" }, 400);
      // One emoji only: any emoji works (picker or keyboard), but no text smuggled in as a "reaction"
      const em = String(body.emoji);
      if (em.length > 32 || !/\p{Extended_Pictographic}|\p{Regional_Indicator}|⃣/u.test(em)
          || /[\p{L}\s<>]/u.test(em) || /\p{N}/u.test(em.replace(/[0-9#*]️?⃣/gu, ""))) {
        return json({ error: "Not an emoji" }, 400);
      }
      if (await isBanned()) return json({ error: "Banned" }, 403);
      const reactedPost = await env.DB.prepare(`SELECT p.id, p.frozen FROM comments c JOIN posts p ON p.id = c.post_id WHERE c.id = ?`).bind(body.comment_id).first();
      if (reactedPost?.frozen) return json({ error: "This post is archived" }, 403);
      // One reaction per bird per chirp (like iMessage): reacting replaces your previous emoji there.
      // Matched by the signed-in account only (never a client-sent device id), so it holds across your
      // devices and nobody can remove someone else's reaction.
      const mine = `comment_id = ? AND username = ?`;
      if (body.action === "remove") {
        await env.DB.prepare(`DELETE FROM comment_reactions WHERE ${mine} AND emoji = ?`).bind(body.comment_id, username, em).run();
      } else {
        await env.DB.prepare(`DELETE FROM comment_reactions WHERE ${mine} AND emoji != ?`).bind(body.comment_id, username, em).run();
        const existing = await env.DB.prepare(`SELECT id FROM comment_reactions WHERE ${mine} AND emoji = ? LIMIT 1`).bind(body.comment_id, username, em).first();
        if (!existing) {
          await env.DB.prepare(`
            INSERT INTO comment_reactions (id, comment_id, browser_id, emoji, username, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
          `).bind(crypto.randomUUID(), body.comment_id, body.browser_id, em, username, now).run();
          if (reactedPost?.id) await bumpPost(reactedPost.id); // a new chirp reaction counts as activity (Flock)
        }
      }
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /delete-account ──────────────────────────────────────────────────────────

  if (url.pathname === "/delete-account" && request.method === "POST") {
    if (!authUser?.sub) return signInRequired();
    try {
      const account = await env.DB.prepare(`SELECT id, username, role, password_hash FROM mod_users WHERE id = ? AND deleted_at IS NULL`).bind(authUser.sub).first();
      if (!account) return signInRequired();
      if (account.role === "admin") return json({ error: "Admin accounts can't be deleted" }, 403);
      if (typeof body.password !== "string" || !await verifyPassword(body.password, account.password_hash)) {
        return json({ error: "Wrong password" }, 403);
      }
      await retireAccount(account, now, "self");
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── Account Trash (admin only) ───────────────────────────────────────────────

  if (url.pathname === "/get-trash") {
    if (!isAdmin) return json({ error: "Unauthorized" }, 401);
    const { results } = await env.DB.prepare(
      `SELECT id, username, role, deleted_at, deleted_by FROM mod_users WHERE deleted_at IS NOT NULL AND purged_at IS NULL ORDER BY deleted_at DESC`
    ).all();
    return json({ accounts: results || [] });
  }

  if (url.pathname === "/restore-member" && request.method === "POST") {
    if (!isAdmin) return json({ error: "Unauthorized" }, 401);
    try {
      const account = await env.DB.prepare(`SELECT id, username, left_huddles FROM mod_users WHERE id = ? AND deleted_at IS NOT NULL AND purged_at IS NULL`).bind(body.user_id || "").first();
      if (!account) return json({ error: "Not in the Trash" }, 404);
      await restoreAccount(account, now);
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // Forever means no way back. The name stays retired and their posts stay as Extinct Bird.
  if (url.pathname === "/purge-member" && request.method === "POST") {
    if (!isAdmin) return json({ error: "Unauthorized" }, 401);
    try {
      const account = await env.DB.prepare(`SELECT id, username FROM mod_users WHERE id = ? AND deleted_at IS NOT NULL AND purged_at IS NULL`).bind(body.user_id || "").first();
      if (!account) return json({ error: "Not in the Trash" }, 404);
      await env.DB.prepare(`UPDATE mod_users SET purged_at = ?, password_hash = '', email = ?, left_huddles = NULL WHERE id = ?`)
        .bind(now, `retired-${account.id}@users.local`, account.id).run();
      if (account.username) await env.DB.prepare(`DELETE FROM system_notifications WHERE user_id = ?`).bind(account.username).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /get-members ──────────────────────────────────────────────────────────────

  if (url.pathname === "/get-members") {
    if (!isModerator) return json({ error: "Unauthorized" }, 401);
    try {
      const { results } = await env.DB.prepare(`
        SELECT m.id, m.email, m.username, m.role, m.created_at, m.last_active, m.deleted_at, m.failed_logins, m.locked_until,
          (SELECT p.ip_hash FROM posts p WHERE p.username = m.username AND p.ip_hash IS NOT NULL ORDER BY p.created_at DESC LIMIT 1) as ip_hash,
          (SELECT p.browser_id FROM posts p WHERE p.username = m.username AND p.browser_id IS NOT NULL ORDER BY p.created_at DESC LIMIT 1) as browser_id,
          MAX(0, m.worm_start + (SELECT COUNT(*) FROM worms w WHERE w.receiver = m.username) - (SELECT COUNT(*) FROM worms w WHERE w.giver = m.username)) as worm_count
        FROM mod_users m WHERE m.deleted_at IS NULL ORDER BY m.last_active DESC, m.created_at DESC`).all();
      // Flaps (like on the bird card): flaps other people gave each bird's posts. Starts from post_votes (small) and
      // looks each post up by id, so the posts table is never scanned.
      const { results: fl = [] } = await env.DB.prepare(`SELECT p.username AS u, COUNT(DISTINCT v.post_id || '|' || COALESCE(v.username, 'b:' || v.browser_id)) AS n
        FROM post_votes v CROSS JOIN posts p ON p.id = v.post_id
        WHERE v.value > 0 AND p.deleted = 0 AND p.username IS NOT NULL AND (v.username IS NULL OR v.username != p.username) GROUP BY p.username`).all();
      const flapsOf = new Map(fl.map(r => [r.u, r.n]));
      const members = (results || []).map(u => ({
        id: u.id,
        email: u.email,
        created_at: u.created_at,
        last_active: u.last_active || null,
        worm_count: u.worm_count || 0,
        flaps: flapsOf.get(u.username) || 0,
        failed_logins: u.failed_logins || 0,
        locked_until: u.locked_until && u.locked_until > now ? u.locked_until : null,
        user_metadata: { username: u.username, role: u.role, ip_hash: u.ip_hash || null, browser_id: u.browser_id || null }
      }));
      return json({ members });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /update-member ────────────────────────────────────────────────────────────

  // Mods and admins can lift a login lock (and reset the wrong-password count) from the mod panel
  if (url.pathname === "/unlock-member" && request.method === "POST") {
    if (!isModerator) return json({ error: "Unauthorized" }, 401);
    if (!body.user_id) return json({ error: "Missing user_id" }, 400);
    const row = await env.DB.prepare(`UPDATE mod_users SET failed_logins = 0, locked_until = NULL WHERE id = ? RETURNING username`).bind(body.user_id).first();
    if (!row) return json({ error: "Not found" }, 404);
    return json({ success: true, username: row.username });
  }

  if (url.pathname === "/update-member") {
    if (!isAdmin) return json({ error: "Unauthorized" }, 401);
    const { user_id, role } = body;
    if (!user_id || !role) return json({ error: "Missing fields" }, 400);
    if (!["user", "mod", "admin"].includes(role)) return json({ error: "Invalid role" }, 400);
    try {
      const target = await env.DB.prepare(`SELECT role FROM mod_users WHERE id = ?`).bind(user_id).first();
      if (target?.role === "admin" && !isAdmin) return json({ error: "Cannot modify an admin" }, 403);
      await env.DB.prepare(`UPDATE mod_users SET role = ? WHERE id = ?`).bind(role, user_id).run();
      const prevRole = target?.role;
      if (prevRole !== role) {
        let notifMsg = null;
        if (role === "mod") notifMsg = `You've been made a mod. Sign out and back in to activate your new role.`;
        else if (prevRole === "mod" && role === "user") notifMsg = `Your mod role has been removed.`;
        if (notifMsg) {
          const notifId = crypto.randomUUID();
          await env.DB.prepare(`INSERT INTO system_notifications (id, user_id, message) VALUES (?, ?, ?)`)
            .bind(notifId, user_id, notifMsg).run();
        }
      }
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /delete-member ────────────────────────────────────────────────────────────

  if (url.pathname === "/delete-member") {
    if (!isAdmin) return json({ error: "Unauthorized" }, 401);
    const { user_id } = body;
    if (!user_id) return json({ error: "Missing fields" }, 400);
    try {
      const target = await env.DB.prepare(`SELECT role, username FROM mod_users WHERE id = ? AND deleted_at IS NULL`).bind(user_id).first();
      if (!target) return json({ error: "User not found" }, 404);
      if (target.role === "admin") return json({ error: "Cannot delete an admin" }, 403);
      await retireAccount({ id: user_id, username: target.username }, now, "mod");
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /mod-action ───────────────────────────────────────────────────────────────

  if (url.pathname === "/mod-action") {
    try {
      if (!isModerator) return json({ error: "Unauthorized" }, 401);
      if (!body.type) return json({ error: "Missing type" }, 400);
      const t = body.type;
      // Mods can't touch an admin's post at all. Checks the author's account too, not just the post's flag.
      if (body.post_id && !isAdmin) {
        const owner = await env.DB.prepare(`SELECT p.is_admin, m.role FROM posts p LEFT JOIN mod_users m ON m.username = p.username WHERE p.id = ?`).bind(body.post_id).first();
        if (owner?.is_admin || owner?.role === "admin") return json({ error: "Mods can't change an admin's post" }, 403);
      }
      const frozenOnly = ["delete_post", "pin_post", "lock_post"];
      if (body.post_id && frozenOnly.includes(t)) {
        const target = await env.DB.prepare(`SELECT frozen FROM posts WHERE id = ?`).bind(body.post_id).first();
        if (target?.frozen) return json({ error: "Unarchive this post first" }, 403);
      }
      if (body.comment_id) {
        const target = await env.DB.prepare(`SELECT p.frozen FROM comments c JOIN posts p ON p.id = c.post_id WHERE c.id = ?`).bind(body.comment_id).first();
        if (target?.frozen) return json({ error: "Unarchive this post first" }, 403);
      }
      if (body.comment_id && !isAdmin) {
        const owner = await env.DB.prepare(`SELECT c.is_admin, m.role FROM comments c LEFT JOIN mod_users m ON m.username = c.username WHERE c.id = ?`).bind(body.comment_id).first();
        if (owner?.is_admin || owner?.role === "admin") return json({ error: "Mods can't change an admin's chirp" }, 403);
      }
      // Mods: pin, lock, cage and flag. Archiving, restoring and banning are for admins.
      if (!isAdmin && ["archive_post", "unarchive_post", "hide_archive", "restore_post", "ban", "unban"].includes(t)) {
        return json({ error: "Only admins can do that" }, 403);
      }
      // Caging lifts a ban, so a mod can't cage a banned bird (that would unban them)
      if (!isAdmin && t === "jail") {
        const cond = [], args = [];
        if (body.username) { cond.push("username = ?"); args.push(body.username); }
        if (body.browser_id) { cond.push("browser_id = ?"); args.push(body.browser_id); }
        if (cond.length && await env.DB.prepare(`SELECT 1 FROM bans WHERE ${cond.join(" OR ")} LIMIT 1`).bind(...args).first()) {
          return json({ error: "They're banned. Only an admin can change that." }, 403);
        }
      }
      if (!isAdmin && ["ban", "jail"].includes(t) && body.username) {
        const target = await env.DB.prepare(`SELECT role FROM mod_users WHERE LOWER(username) = LOWER(?)`).bind(body.username).first();
        if (target?.role === "admin") return json({ error: "Mods can't do that to an admin" }, 403);
      }
      if (t === "ban") {
        // Banning removes cage — the two states are mutually exclusive
        if (body.username)   await env.DB.prepare(`DELETE FROM jailed WHERE username = ?`).bind(body.username).run();
        if (body.browser_id) await env.DB.prepare(`DELETE FROM jailed WHERE browser_id = ?`).bind(body.browser_id).run();
        if (body.ip_hash)    await env.DB.prepare(`DELETE FROM jailed WHERE ip_hash = ?`).bind(body.ip_hash).run();
        // A ban is for the account (and its browser). The IP is only banned when asked for explicitly:
        // it blocks everyone on that network (school, cafe, mobile carrier), like a 4chan-style ban.
        await env.DB.prepare(`INSERT INTO bans (id, username, browser_id, ip_hash, created_at) VALUES (?, ?, ?, ?, ?)`)
          .bind(crypto.randomUUID(), body.username || null, body.browser_id || null, body.ban_ip === true ? (body.ip_hash || null) : null, now).run();
      }
      if (t === "unban") {
        if (body.username)   await env.DB.prepare(`DELETE FROM bans WHERE username = ?`).bind(body.username).run();
        if (body.browser_id) await env.DB.prepare(`DELETE FROM bans WHERE browser_id = ?`).bind(body.browser_id).run();
        if (body.ip_hash)    await env.DB.prepare(`DELETE FROM bans WHERE ip_hash = ?`).bind(body.ip_hash).run();
      }
      if (t === "jail") {
        // Caging removes ban — the two states are mutually exclusive
        if (body.username)   await env.DB.prepare(`DELETE FROM bans WHERE username = ?`).bind(body.username).run();
        if (body.browser_id) await env.DB.prepare(`DELETE FROM bans WHERE browser_id = ?`).bind(body.browser_id).run();
        if (body.ip_hash)    await env.DB.prepare(`DELETE FROM bans WHERE ip_hash = ?`).bind(body.ip_hash).run();
        await env.DB.prepare(`INSERT OR IGNORE INTO jailed (id, browser_id, username, ip_hash, created_at) VALUES (?, ?, ?, ?, ?)`)
          .bind(crypto.randomUUID(), body.browser_id || null, body.username || null, body.ip_hash || null, now).run();
      }
      if (t === "unjail") {
        if (body.username)   await env.DB.prepare(`DELETE FROM jailed WHERE username = ?`).bind(body.username).run();
        if (body.browser_id) await env.DB.prepare(`DELETE FROM jailed WHERE browser_id = ?`).bind(body.browser_id).run();
        if (body.ip_hash)    await env.DB.prepare(`DELETE FROM jailed WHERE ip_hash = ?`).bind(body.ip_hash).run();
      }
      // Mods flag; only admins delete (a mod can still delete their own post or chirp)
      if (t === "flag_post" || t === "flag_comment") {
        const isPost = t === "flag_post", tid = String((isPost ? body.post_id : body.comment_id) || "");
        if (!tid) return json({ error: "Missing fields" }, 400);
        const row = await env.DB.prepare(isPost
          ? `SELECT p.id, p.id AS post_id, p.username, p.browser_id, p.title, p.content, p.is_mod, p.is_admin, m.role FROM posts p LEFT JOIN mod_users m ON m.username = p.username WHERE p.id = ?`
          : `SELECT c.id, c.post_id, c.username, c.browser_id, NULL AS title, c.content, c.is_mod, c.is_admin, m.role FROM comments c LEFT JOIN mod_users m ON m.username = c.username WHERE c.id = ?`).bind(tid).first();
        if (!row) return json({ error: "Not found" }, 404);
        if (row.username && row.username === username) return json({ error: "That's yours. Delete it instead." }, 400);
        if (row.is_mod || row.is_admin || row.role === "mod" || row.role === "admin") return json({ error: "Mods and admins can't be flagged" }, 403);
        const hid = (await env.DB.prepare(`UPDATE ${isPost ? "posts" : "comments"} SET deleted = 1 WHERE id = ? AND deleted = 0`).bind(tid).run()).meta.changes > 0 ? 1 : 0;
        // Cage the author (real bird accounts only, not news bots), unless they're already in
        let caged = 0;
        const isBird = row.username && row.role === "user" && !String(row.browser_id || "").startsWith("bot-");
        // (a banned bird stays banned: that's stricter than The Cage)
        const banned = isBird && !!await env.DB.prepare(`SELECT 1 FROM bans WHERE username = ? LIMIT 1`).bind(row.username).first();
        if (isBird && !banned && !await env.DB.prepare(`SELECT 1 FROM jailed WHERE username = ? LIMIT 1`).bind(row.username).first()) {
          await env.DB.prepare(`INSERT OR IGNORE INTO jailed (id, browser_id, username, ip_hash, created_at) VALUES (?, ?, ?, NULL, ?)`)
            .bind(crypto.randomUUID(), row.browser_id || null, row.username, now).run();
          caged = 1;
        }
        const reason = String(body.reason || "").replace(/\s+/g, " ").trim().slice(0, 200);
        const excerpt = [row.title, userText(row.content)].filter(Boolean).join("\n").slice(0, 600);
        await env.DB.prepare(`INSERT INTO ai_flags (id, kind, target_id, post_id, username, browser_id, categories, excerpt, hid, caged, status, created_at, flagged_by, reason) VALUES (?, ?, ?, ?, ?, ?, 'MOD', ?, ?, ?, 'open', ?, ?, ?)`)
          .bind(crypto.randomUUID(), isPost ? "post" : "chirp", tid, row.post_id || null, row.username || null, row.browser_id || null, excerpt, hid, caged, now, username, reason || null).run();
        const { results: admins = [] } = await env.DB.prepare(`SELECT username FROM mod_users WHERE role = 'admin' AND deleted_at IS NULL AND username IS NOT NULL`).all();
        const msg = JSON.stringify({
          // Starts with the plain name, so the notification shows that bird's picture
          text: `${row.username || "Someone"} had a ${isPost ? "post" : "chirp"} flagged by ${username}${reason ? ` ("${reason}")` : ""}. It's hidden${banned ? " (they're already banned)" : isBird ? " and they're in The Cage" : ""}. Review it in Mod Panel → Flagged.`,
          postId: row.post_id || undefined, icon: "SHIELD", preview: excerpt.slice(0, 80),
        });
        for (const a of admins) if (a.username !== username) await env.DB.prepare(`INSERT INTO system_notifications (id, user_id, message) VALUES (?, ?, ?)`).bind(crypto.randomUUID(), a.username, msg).run();
        return json({ success: true, caged });
      }
      if ((t === "delete_post" || t === "delete_comment") && !isAdmin) {
        const own = await env.DB.prepare(t === "delete_post" ? `SELECT username FROM posts WHERE id = ?` : `SELECT username FROM comments WHERE id = ?`).bind(t === "delete_post" ? body.post_id : body.comment_id).first();
        if (!own || !username || own.username !== username) return json({ error: "Mods can flag this. Only admins can delete it." }, 403);
      }
      if (t === "delete_post") {
        const _dp = await env.DB.prepare(`SELECT is_admin FROM posts WHERE id = ?`).bind(body.post_id).first();
        if (_dp?.is_admin && !isAdmin) return json({ error: "Cannot delete an admin post" }, 403);
        await env.DB.prepare(`UPDATE posts SET deleted = 1 WHERE id = ?`).bind(body.post_id).run();
      }
      if (t === "archive_post") {
        const _ap = await env.DB.prepare(`SELECT is_admin FROM posts WHERE id = ?`).bind(body.post_id).first();
        if (_ap?.is_admin && !isAdmin) return json({ error: "Cannot archive an admin post" }, 403);
        await env.DB.prepare(`UPDATE posts SET frozen = 1 WHERE id = ?`).bind(body.post_id).run();
      }
      if (t === "unarchive_post") {
        await env.DB.prepare(`UPDATE posts SET frozen = 0, archived = 0 WHERE id = ?`).bind(body.post_id).run();
      }
      if (t === "hide_archive") {
        await env.DB.prepare(`UPDATE posts SET archived = ? WHERE id = ? AND frozen = 1`).bind(body.hidden ? 1 : 0, body.post_id).run();
      }
      if (t === "restore_post") {
        await env.DB.prepare(`UPDATE posts SET deleted = 0, archived = CASE WHEN frozen = 1 THEN archived ELSE 0 END WHERE id = ?`).bind(body.post_id).run();
      }
      if (t === "permanent_delete_post") {
        if (!isAdmin) return json({ error: "Unauthorized" }, 401);
        const _pdc = await env.DB.prepare(`SELECT id FROM comments WHERE post_id = ?`).bind(body.post_id).all();
        const _pdcIds = (_pdc.results || []).map(c => c.id);
        if (_pdcIds.length) {
          await env.DB.prepare(`DELETE FROM comment_reactions WHERE comment_id IN (${ID_LIST})`).bind(JSON.stringify(_pdcIds)).run();
        }
        // Delete forever also removes the photos/videos (and their small copies) from storage
        const _pdp = await env.DB.prepare(`SELECT content FROM posts WHERE id = ?`).bind(body.post_id).first();
        const _pdcc = await env.DB.prepare(`SELECT content FROM comments WHERE post_id = ?`).bind(body.post_id).all();
        const _mediaKeys = new Set();
        for (const txt of [_pdp?.content, ...(_pdcc.results || []).map(r => r.content)]) {
          for (const m of String(txt || "").matchAll(/\/media\/([A-Za-z0-9][A-Za-z0-9._-]*)/g)) { _mediaKeys.add(m[1]); _mediaKeys.add(`thumbs/${m[1]}.jpg`); }
        }
        await env.DB.prepare(`DELETE FROM post_votes WHERE post_id = ?`).bind(body.post_id).run();
        await env.DB.prepare(`DELETE FROM comments WHERE post_id = ?`).bind(body.post_id).run();
        await env.DB.prepare(`DELETE FROM posts WHERE id = ?`).bind(body.post_id).run();
        if (_mediaKeys.size) {
          await env.MEDIA.delete([..._mediaKeys]).catch(err => console.error("media delete failed", err.message));
          // and the cached copies Cloudflare keeps near viewers
          if (env.MEDIA_SVC) await env.MEDIA_SVC.fetch("https://media/__purge", { method: "POST", body: JSON.stringify({ keys: [..._mediaKeys].filter(k => !k.startsWith("thumbs/")) }) }).catch(err => console.error("media cache purge failed", err.message));
        }
      }
      if (t === "delete_comment") {
        const _dc = await env.DB.prepare(`SELECT is_admin FROM comments WHERE id = ?`).bind(body.comment_id).first();
        if (_dc?.is_admin && !isAdmin) return json({ error: "Cannot delete an admin comment" }, 403);
        await env.DB.prepare(`UPDATE comments SET deleted = 1 WHERE id = ?`).bind(body.comment_id).run();
      }
      if (t === "pin_post") {
        await env.DB.prepare(`UPDATE posts SET pinned = ?, pinned_global = ? WHERE id = ?`)
          .bind(body.pinned ? 1 : 0, body.pinned_global ? 1 : 0, body.post_id).run();
      }
      if (t === "pin_comment") {
        await env.DB.prepare(`UPDATE comments SET pinned = ? WHERE id = ?`)
          .bind(body.pinned ? 1 : 0, body.comment_id).run();
      }
      if (t === "lock_post") {
        await env.DB.prepare(`UPDATE posts SET locked = ? WHERE id = ?`)
          .bind(body.locked ? 1 : 0, body.post_id).run();
      }
      if (t === "clear_username") {
        if (!isAdmin) return json({ error: "Unauthorized" }, 401);
        await env.DB.prepare(`UPDATE posts SET username = NULL WHERE browser_id = ?`).bind(body.browser_id).run();
        await env.DB.prepare(`UPDATE comments SET username = NULL WHERE browser_id = ?`).bind(body.browser_id).run();
      }
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /get-mod-data ─────────────────────────────────────────────────────────────

  if (url.pathname === "/get-mod-data") {
    if (!isModerator) return json({ error: "Unauthorized" }, 401);
    try {
      const [postsRes, commentsRes, bansRes, jailedRes, deletedRes, archivedRes] = await Promise.all([
        env.DB.prepare(`SELECT * FROM posts WHERE deleted = 0 AND (archived = 0 OR archived IS NULL) ORDER BY created_at DESC LIMIT 500`).all(),
        env.DB.prepare(`SELECT * FROM comments WHERE deleted = 0 ORDER BY created_at DESC LIMIT 1000`).all(),
        env.DB.prepare(`SELECT * FROM bans ORDER BY created_at DESC`).all(),
        env.DB.prepare(`SELECT * FROM jailed ORDER BY created_at DESC`).all(),
        env.DB.prepare(`SELECT id, title, board, username, browser_id, created_at, content, is_admin FROM posts WHERE deleted = 1 ORDER BY created_at DESC LIMIT 100`).all(),
        env.DB.prepare(`SELECT id, title, board, username, browser_id, created_at, content, archived, frozen, is_admin FROM posts WHERE frozen = 1 AND deleted = 0 ORDER BY created_at DESC LIMIT 100`).all(),
      ]);
      return json({
        posts:    (postsRes.results    || []).map(p => boolify(p, POST_BOOL_FIELDS)),
        comments: (commentsRes.results || []).map(c => boolify(c, COMMENT_BOOL_FIELDS)),
        bans:     bansRes.results    || [],
        jailed:   jailedRes.results  || [],
        deletedPosts:   deletedRes.results   || [],
        archivedPosts:  archivedRes.results  || [],
      });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /check-jailed ─────────────────────────────────────────────────────────────

  if (url.pathname === "/check-jailed") {
    try {
      const bid   = (url.searchParams.get("browser_id") || body.browser_id || "").trim();
      const uname = (url.searchParams.get("username")   || "").trim();
      if (!bid && !uname) return json({ jailed: false });
      const conditions = [];
      const params = [];
      if (bid)   { conditions.push("browser_id = ?"); params.push(bid); }
      if (uname) { conditions.push("username = ?");   params.push(uname); }
      const row = await env.DB.prepare(
        `SELECT 1 FROM jailed WHERE ${conditions.join(" OR ")} LIMIT 1`
      ).bind(...params).first();
      return json({ jailed: !!row });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /search-users ─────────────────────────────────────────────────────────────

  // ── /tags ── user tag suggestions (?q=prefix) and this week's popular tags (?popular=1). Counts live posts.
  if (url.pathname === "/tags") {
    try {
      const q = String(url.searchParams.get("q") || "").trim().replace(/^#+/, "").toLowerCase().slice(0, 20);
      if (url.searchParams.get("popular") === "1") {
        const since = new Date(Date.now() - 7 * 86400000).toISOString();
        const { results = [] } = await env.DB.prepare(
          `SELECT t.tag, COUNT(*) AS n FROM post_tags t JOIN posts p ON p.id = t.post_id WHERE t.created_at >= ? AND p.deleted = 0 GROUP BY t.tag ORDER BY n DESC, MAX(t.created_at) DESC LIMIT 12`
        ).bind(since).all();
        return json({ tags: results });
      }
      if (!/^[a-z0-9]{1,20}$/.test(q)) return json({ tags: [] });
      const { results = [] } = await env.DB.prepare(
        `SELECT t.tag, COUNT(*) AS n FROM post_tags t JOIN posts p ON p.id = t.post_id WHERE t.tag >= ? AND t.tag < ? AND p.deleted = 0 GROUP BY t.tag ORDER BY n DESC LIMIT 8`
      ).bind(q, q + "\uffff").all();
      return json({ tags: results });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /feed-proxy?url= ── the news bot runs on GitHub's servers, which some outlets block (The Guardian answers
  // 403 since 2026-11-23). For those outlets only, the bot fetches the RSS through here (Cloudflare's network).
  // Bot key (or mods, for testing) and an allow-list of hosts, so it can't be used to fetch anything else.
  if (url.pathname === "/feed-proxy") {
    if (!isBot && !isModerator) return json({ error: "Unauthorized" }, 401);
    const FEED_PROXY_HOSTS = ["www.theguardian.com", "theguardian.com"];
    let target;
    try { target = new URL(String(url.searchParams.get("url") || "")); } catch { return json({ error: "Bad url" }, 400); }
    if (target.protocol !== "https:" || !FEED_PROXY_HOSTS.includes(target.hostname)) return json({ error: "Host not allowed" }, 403);
    try {
      const r = await fetch(target.toString(), { headers: { "User-Agent": "Mozilla/5.0 (compatible; PerchPostsNews/1.0; +https://perchposts.com)", "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8" }, cf: { cacheTtl: 300 } });
      const body = (await r.text()).slice(0, 3_000_000);
      return new Response(body, { status: r.status, headers: { ...corsHeaders, "Content-Type": r.headers.get("content-type") || "application/xml" } });
    } catch (err) {
      return json({ error: "Fetch failed" }, 502);
    }
  }

  // ── /globe-tile/z/y/x.jpg ── sharper globe imagery when zoomed in: Sentinel-2 cloudless 2023 by EOX
  // (CC BY-NC-SA 4.0, credited on the globe; site is non-commercial). Fetched here so visitors' phones never contact
  // EOX, and kept in the edge cache for 30 days. Web-Mercator tiles, zoom 0–14 only.
  const gt = url.pathname.match(/^\/globe-tile\/(\d{1,2})\/(\d{1,5})\/(\d{1,5})\.jpg$/);
  if (gt && request.method === "GET") {
    const z = +gt[1], y = +gt[2], x = +gt[3], n = 2 ** z;
    if (z > 14 || y >= n || x >= n) return new Response("Not found", { status: 404, headers: corsHeaders });
    const key = new Request(`https://perchposts-tiles.cache/s2c-2023/${z}/${y}/${x}.jpg`);
    const hit = await caches.default.match(key);
    if (hit) return hit;
    try {
      const up = await fetch(`https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2023_3857/default/g/${z}/${y}/${x}.jpg`, { cf: { cacheTtl: 2592000, cacheEverything: true } });
      if (!up.ok) return new Response("Tile unavailable", { status: up.status === 404 ? 404 : 502, headers: corsHeaders });
      const res = new Response(up.body, { headers: { ...corsHeaders, "Access-Control-Allow-Origin": "*", "Content-Type": up.headers.get("content-type") || "image/jpeg", "Cache-Control": "public, max-age=2592000, immutable" } }); // EOX sends plain-colour PNGs for all-sea/ice tiles
      ctx.waitUntil(caches.default.put(key, res.clone()));
      return res;
    } catch (err) {
      return new Response("Tile unavailable", { status: 502, headers: corsHeaders });
    }
  }

  // ── /globe ── the saved trending stories (public). /globe-build: mods (or the bot key) rebuild now; ?dry=1 only shows.
  if (url.pathname === "/globe") {
    try {
      const row = await env.DB.prepare(`SELECT v, at FROM globe_cache WHERE k = 'trending'`).first();
      if (!row || Date.now() - new Date(row.at).getTime() > 3 * 3600e3) ctx.waitUntil(buildTrending(env).catch(e => console.error("buildTrending", e.message)));
      return new Response(row ? row.v : JSON.stringify({ built_at: null, stories: [] }), { headers: { ...corsHeaders, "Content-Type": "application/json", "Cache-Control": "public, max-age=300" } });
    } catch (err) {
      return serverError(err);
    }
  }
  // ── /globe-sig ── tiny summary for the globe logo's "new stories" dot: for each top story, the ids of its
  // earliest 5 posts (stable while the story grows). The page compares them with what you saw on the globe.
  if (url.pathname === "/globe-sig") {
    try {
      const row = await env.DB.prepare(`SELECT v FROM globe_cache WHERE k = 'trending'`).first();
      let d = { built_at: null, stories: [] };
      try { d = JSON.parse(row?.v || "{}"); } catch (e) {}
      const s = (d.stories || []).map(st => [...(st.posts || [])].sort((a, b) => String(a.t).localeCompare(String(b.t))).slice(0, 5).map(p => p.id));
      // where each story happened, for the little story dots on the site's globe logo
      const o = (d.stories || []).map(st => st.origin && isFinite(st.origin.lat) ? [Math.round(st.origin.lat * 10) / 10, Math.round(st.origin.lng * 10) / 10] : null);
      return new Response(JSON.stringify({ b: d.built_at || null, s, o }), { headers: { ...corsHeaders, "Content-Type": "application/json", "Cache-Control": "public, max-age=300" } });
    } catch (err) {
      return serverError(err);
    }
  }
  if (url.pathname === "/globe-build") {
    if (!isModerator && !isBot) return json({ error: "Unauthorized" }, 401);
    try {
      const dry = url.searchParams.get("dry") === "1", th = parseFloat(url.searchParams.get("t") || "0.8"), mg = parseFloat(url.searchParams.get("m") || "0.85");
      const r = await buildTrending(env, { dry, threshold: th >= 0.5 && th <= 0.99 ? th : 0.8, merge: mg >= 0.5 && mg <= 0.99 ? mg : 0.85 });
      return json(dry ? { ...r, stories: r.stories.map(s => ({ rank: s.rank, title: s.title, outlets: s.outlets, countries: s.countries, activity: s.activity, origin: s.origin, posts: s.posts.map(p => `${p.outlet} (${p.city}): ${p.title}`) })), merged: r.merged } : { built_at: r.built_at, stories: r.stories.length, items: r.items, clusters: r.clusters, multi: r.multi });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /huddle-search?q= ── keywords in your huddles: the huddle's title/opening message, or any chirp in it.
  // Each result carries hit_comment = the FIRST chirp that says it (oldest), so opening the huddle can jump there.
  // Only huddles you're in (admins with "see all huddles" on: all), like the Huddles list.
  if (url.pathname === "/huddle-search") {
    if (!authUser?.username) return signInRequired();
    try {
      const q = String(url.searchParams.get("q") || "").trim().slice(0, 100);
      if (q.length < 2) return json({ posts: [] });
      const me = authUser.username;
      let hq = `SELECT rowid AS _rid, * FROM posts INDEXED BY idx_posts_huddles WHERE is_huddle = 1 AND deleted = 0 AND (archived = 0 OR archived IS NULL)`;
      const hp = [];
      if (!seeAllHuddles) {
        hq += ` AND (LOWER(username) = LOWER(?) OR (huddle_members IS NOT NULL AND (LOWER(huddle_members) LIKE LOWER(?) OR LOWER(huddle_members) LIKE LOWER(?))))`;
        hp.push(me, `%"${me}"%`, `%"${me}:%`);
      }
      const { results: huddles = [] } = await env.DB.prepare(hq + ` LIMIT 500`).bind(...hp).all();
      if (!huddles.length) return json({ posts: [] });
      const like = `%${q.replace(/[%_\\]/g, m => "\\" + m)}%`;
      const ids = huddles.map(h => h.id), firstHit = new Map();
      const ql = q.toLowerCase();
      // Only what people wrote counts: no system lines (joined/left...), no link or share data inside a chirp
      const said = c => String(c || "").split("[ATTACH")[0];
      for (let i = 0; i < ids.length; i += 90) {
        const chunk = ids.slice(i, i + 90);
        const { results = [] } = await env.DB.prepare(
          `SELECT post_id, id, username, content, created_at AS at FROM comments WHERE post_id IN (${chunk.map(() => "?").join(",")}) AND deleted = 0 AND content LIKE ? ESCAPE '\\' AND (username IS NULL OR username != '__system__') ORDER BY created_at ASC LIMIT 3000`
        ).bind(...chunk, like).all();
        for (const r of results) if (!firstHit.has(r.post_id) && said(r.content).toLowerCase().includes(ql)) firstHit.set(r.post_id, r);
      }
      const rows = huddles.filter(h => firstHit.has(h.id) || `${h.title || ""} ${h.content || ""}`.toLowerCase().includes(ql))
        .map(h => ({ ...h, hit_comment: firstHit.get(h.id)?.id || null }))
        .sort((a, b) => String(b.last_activity || "").localeCompare(String(a.last_activity || "")));
      await addHuddleInbox(env, rows, me);
      // The card's preview shows the chirp that matched (not the latest one), cut so the keyword is in view
      for (const h of rows) {
        const r = firstHit.get(h.id);
        if (!r || !h.hx) continue;
        let c = String(r.content || "").split("[ATTACH")[0].replace(/\s+/g, " ").trim();
        const at = c.toLowerCase().indexOf(ql);
        if (at > 40) c = "…" + c.slice(at - 30);
        h.hx.last = { u: r.username, c: c.slice(0, 400), t: r.at };
      }
      return json({ posts: await publicRows(await addCommentCounts(env, rows.map(p => boolify(p, POST_BOOL_FIELDS)))) });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /saved-searches ── the signed-in bird's saved searches (up to 5). GET → {items}; POST {items:[{qs, def}]} replaces
  // them. qs keeps only the search bar's filter keys; at most one is the default (def).
  if (url.pathname === "/saved-searches") {
    if (!authUser?.sub) return signInRequired();
    try {
      const KEYS = ["flock", "board", "continent", "country", "utag", "user", "bot", "q"];
      const tidy = raw => {
        const src = new URLSearchParams(String(raw || "").slice(0, 600)), out = new URLSearchParams();
        for (const k of KEYS) { const v = String(src.get(k) || "").trim().slice(0, k === "q" ? 120 : 80); if (v) out.set(k, v); }
        return out.toString();
      };
      if (request.method === "POST") {
        const seen = new Set(), items = [];
        let hasDef = false;
        for (const it of Array.isArray(body.items) ? body.items : []) {
          const qs = tidy(it && it.qs);
          if (!qs || seen.has(qs)) continue;
          seen.add(qs);
          const def = !!(it.def && !hasDef);
          if (def) hasDef = true;
          items.push(it.alert ? { qs, def, alert: true } : { qs, def });
          if (items.length === 5) break;
        }
        await env.DB.prepare(`UPDATE mod_users SET saved_searches = ? WHERE id = ?`).bind(JSON.stringify(items), authUser.sub).run();
        ALERT_RULES = null;
        return json({ items });
      }
      const row = await env.DB.prepare(`SELECT saved_searches FROM mod_users WHERE id = ?`).bind(authUser.sub).first();
      let items = [];
      try { items = JSON.parse(row?.saved_searches || "[]"); } catch (e) {}
      return json({ items: Array.isArray(items) ? items : [] });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /share ── POST {post_id, via: huddle|copy|more}: a signed-in bird shared a public post. Counts once per bird per
  // post (posts.share_count, shown beside Share) and the first share bumps last_activity so the post shows in Flock.
  if (url.pathname === "/share" && request.method === "POST") {
    if (!authUser?.username) return signInRequired();
    try {
      const id = String(body.post_id || "").slice(0, 80);
      const via = ["huddle", "copy", "more"].includes(body.via) ? body.via : "more";
      const post = await env.DB.prepare(`SELECT id, share_count FROM posts WHERE id = ? AND ${LIVE_POSTS}`).bind(id).first();
      if (!post) return json({ error: "Not found" }, 404);
      const r = await env.DB.prepare(`INSERT OR IGNORE INTO post_shares (post_id, username, via, created_at) VALUES (?, ?, ?, ?)`)
        .bind(id, authUser.username.toLowerCase(), via, now).run();
      if (!r.meta?.changes) return json({ counted: false, share_count: post.share_count || 0 });
      await env.DB.prepare(`UPDATE posts SET share_count = share_count + 1, last_activity = ? WHERE id = ?`).bind(now, id).run();
      return json({ counted: true, share_count: (post.share_count || 0) + 1 });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /post-tags ── POST {post_id, board:{slug,name}|null, continent, country, tag}: admins change all of a post's tags
  // at once from the post page (user's request, 2026-11-23). Birds' posts and news bot posts; not huddles or The Cage.
  // Every post keeps at least one tag; news posts always keep a perch tag and never get a flock tag.
  if (url.pathname === "/post-tags" && request.method === "POST") {
    if (!isAdmin) return json({ error: "Only admins can change a post's tags" }, 403);
    try {
      const post = await env.DB.prepare(`SELECT id, username, browser_id, is_huddle, deleted, created_at, board, community_id, utag FROM posts WHERE id = ?`).bind(String(body.post_id || "")).first();
      if (!post || post.deleted || post.is_huddle) return json({ error: "Not found" }, 404);
      const isCage = v => ["cage", "the cage"].includes(String(v || "").trim().toLowerCase());
      if (isCage(post.community_id) || isCage(post.board)) return json({ error: "Cage posts keep their Cage tag" }, 400);
      const bot = String(post.browser_id || "").startsWith("bot-") || /Bot$/.test(post.username || "");
      const b = body.board && typeof body.board === "object" ? body.board : null;
      const slug = b ? String(b.slug || "").trim().toLowerCase() : "", name = b ? String(b.name || "").trim() : "";
      if (b && (!/^[a-z0-9-]{1,40}$/.test(slug) || !name || name.length > 40)) return json({ error: "Unknown perch tag" }, 400);
      if (b && (isCage(slug) || isCage(name) || ["feedback", "huddles"].includes(slug))) return json({ error: "That perch tag can't be picked here" }, 400);
      const clean = v => { const s = String(v || "").trim(); return s && s.length <= 60 ? s : null; };
      const country = clean(body.country), continent = clean(body.continent);
      const r = await cleanTag(body.tag);
      if (r.error) return json({ error: r.error }, 400);
      const tag = r.tag;
      if (bot && tag) return json({ error: "News posts can't have a flock tag" }, 400);
      if (bot && !b) return json({ error: "News posts need a perch tag" }, 400);
      if (!b && !tag) return json({ error: "A post needs at least one tag" }, 400);
      // Bot posts store the slug in board (as the bots send it); birds' posts store the name + slug.
      // With only a flock tag the post is filed under Random behind the scenes (board_auto), like New Post.
      const nb = b ? (bot ? slug : name) : "Random", nc = b ? (bot ? post.community_id : slug) : "random", auto = b ? 0 : 1;
      await env.DB.prepare(`UPDATE posts SET board = ?, community_id = ?, board_auto = ?, continent = ?, country = ? WHERE id = ?`)
        .bind(nb, nc, auto, continent, country, post.id).run();
      if ((post.utag || null) !== tag) await setPostTag(post.id, tag, post.created_at);
      return json({ success: true, board: nb, community_id: nc, board_auto: auto, continent, country, utag: tag });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /post-tag ── POST {post_id, tag}: admins add/change/remove a post's flock tag (tag "" removes).
  if (url.pathname === "/post-tag" && request.method === "POST") {
    if (!authUser?.username) return signInRequired();
    try {
      const post = await env.DB.prepare(`SELECT id, username, browser_id, is_huddle, deleted, created_at, board, community_id FROM posts WHERE id = ?`).bind(String(body.post_id || "")).first();
      if (!post || post.deleted || post.is_huddle) return json({ error: "Not found" }, 404);
      if (String(post.browser_id || "").startsWith("bot-") || /Bot$/.test(post.username || "") || ["cage", "the cage"].includes(String(post.community_id || post.board || "").toLowerCase())) return json({ error: "This post can't have a tag" }, 400);
      const mine = (post.username || "").toLowerCase() === authUser.username.toLowerCase();
      const r = await cleanTag(body.tag);
      if (r.error) return json({ error: r.error }, 400);
      // After posting, only admins can change or remove a flock tag (user's call, 2026-11-23)
      if (!isAdmin) return json({ error: "Only admins can change a flock tag" }, 403);
      await setPostTag(post.id, r.tag, post.created_at);
      return json({ success: true, utag: r.tag });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /blocked-tags ── admins: GET the list; POST {tag, block: true|false}. Blocking also strips it from every post.
  if (url.pathname === "/blocked-tags") {
    if (!isAdmin) return json({ error: "Not allowed" }, 403);
    try {
      if (request.method === "POST") {
        const t = String(body.tag || "").trim().replace(/^#+/, "").toLowerCase();
        if (!/^[a-z0-9]{2,20}$/.test(t)) return json({ error: "Bad tag" }, 400);
        if (body.block === false) await env.DB.prepare(`DELETE FROM blocked_tags WHERE tag = ?`).bind(t).run();
        else await env.DB.batch([
          env.DB.prepare(`INSERT OR IGNORE INTO blocked_tags (tag, blocked_by, created_at) VALUES (?, ?, ?)`).bind(t, authUser.username, now),
          env.DB.prepare(`UPDATE posts SET utag = NULL WHERE id IN (SELECT post_id FROM post_tags WHERE tag = ?)`).bind(t),
          env.DB.prepare(`DELETE FROM post_tags WHERE tag = ?`).bind(t),
        ]);
      }
      const { results = [] } = await env.DB.prepare(`SELECT tag, blocked_by, created_at FROM blocked_tags ORDER BY created_at DESC`).all();
      return json({ blocked: results });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /my-huddles ── the huddles you own or are in (for Share → Send to a huddle), most recently active first.
  // Never other people's huddles, even for admins with "see all huddles" on.
  if (url.pathname === "/my-huddles") {
    if (!authUser?.username) return signInRequired();
    try {
      const me = authUser.username;
      const { results = [] } = await env.DB.prepare(
        `SELECT id, title, username, huddle_members, last_activity FROM posts INDEXED BY idx_posts_huddles
         WHERE is_huddle = 1 AND deleted = 0 AND (archived = 0 OR archived IS NULL) AND (frozen = 0 OR frozen IS NULL)
           AND (LOWER(username) = LOWER(?) OR LOWER(huddle_members) LIKE LOWER(?) OR LOWER(huddle_members) LIKE LOWER(?))
         ORDER BY last_activity DESC LIMIT 40`
      ).bind(me, `%"${me}"%`, `%"${me}:%`).all();
      const huddles = results.filter(p => isHuddleMember(p, me)).map(p => ({
        id: p.id, title: p.title || "Huddle",
        members: [...new Set([p.username, ...JSON.parse(p.huddle_members || "[]").map(normMember)].filter(Boolean))],
      }));
      return json({ huddles });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /share-card?id= ── what a post shared into a huddle shows: title, photo, site, live flap / chirp counts.
  // Public posts only (huddles never show as a shared card).
  if (url.pathname === "/share-card") {
    try {
      const id = String(url.searchParams.get("id") || "").slice(0, 80);
      const p = id && await env.DB.prepare(`SELECT id, title, content, username, is_huddle, deleted, archived, board, community_id, share_count FROM posts WHERE id = ?`).bind(id).first();
      if (!p || p.is_huddle || p.deleted || (p.archived && !isModerator)) return json({ gone: true });
      const [f, c] = await env.DB.batch([
        env.DB.prepare(`SELECT COUNT(DISTINCT COALESCE(username, 'b:' || browser_id)) AS n FROM post_votes WHERE post_id = ? AND value > 0`).bind(id),
        env.DB.prepare(`SELECT COUNT(*) AS n FROM comments WHERE post_id = ? AND deleted = 0 AND (username IS NULL OR username != '__system__')`).bind(id),
      ]);
      let image = null, site = null, text = "";
      const raw = String(p.content || ""), at = raw.search(/\s*\[ATTACH/);
      text = (at >= 0 ? raw.slice(0, at) : raw).trim().slice(0, 160);
      const m = raw.match(/\[ATTACH(?:MENTS)?:([\s\S]*)\]\s*$/);
      let lt = "";
      if (m) { try { const a = JSON.parse(m[1]); const one = Array.isArray(a) ? a[0] : a; image = one?.image || (one?.type === "image" ? one.url : null) || null; if (one?.url && one.type === "link") { site = new URL(one.url).hostname.replace(/^www\./, ""); lt = one.title || ""; if (!text) text = String(one.description || "").slice(0, 160); } } catch {} }
      const names = await extinctNames();
      return json({ id, title: p.title || lt || "", text, image, site, by: names.has(p.username) ? EXTINCT_NAME : (p.username || null), board: p.board || p.community_id || null, flaps: f.results?.[0]?.n || 0, chirps: c.results?.[0]?.n || 0, shares: p.share_count || 0 });
    } catch (err) {
      return serverError(err);
    }
  }

  if (url.pathname === "/search-users") {
    const q = (url.searchParams.get("q") || "").trim();
    if (!q) return json({ users: [] });
    const { results } = await env.DB.prepare(
      `SELECT username, role FROM mod_users WHERE username LIKE ? AND username IS NOT NULL AND deleted_at IS NULL ORDER BY username ASC LIMIT 20`
    ).bind(`%${q}%`).all();
    return json({ users: results || [] });
  }

  // ── /user-stats ───────────────────────────────────────────────────────────────

  if (url.pathname === "/user-stats") {
    try {
      const browser_id = url.searchParams.get("browser_id") || "";
      const mod_user_id = url.searchParams.get("mod_user_id") || null;
      const uname = url.searchParams.get("username") || null;
      if (uname && (uname === EXTINCT_NAME || (await extinctNames()).has(uname))) return json({ joined_at: null, worm_count: 0, extinct: true });

      // Joined date
      let joined_at = null;
      if (mod_user_id) {
        const u = await env.DB.prepare(`SELECT created_at FROM mod_users WHERE id = ?`).bind(mod_user_id).first();
        joined_at = u?.created_at || null;
      } else if (uname) {
        const u = await env.DB.prepare(`SELECT created_at FROM mod_users WHERE username = ?`).bind(uname).first();
        joined_at = u?.created_at || null;
        if (!joined_at) {
          const fp = await env.DB.prepare(`SELECT created_at FROM posts WHERE username = ? ORDER BY created_at ASC LIMIT 1`).bind(uname).first();
          joined_at = fp?.created_at || null;
        }
      } else if (browser_id) {
        const fp = await env.DB.prepare(`SELECT created_at FROM posts WHERE browser_id = ? ORDER BY created_at ASC LIMIT 1`).bind(browser_id).first();
        const fc = await env.DB.prepare(`SELECT created_at FROM comments WHERE browser_id = ? ORDER BY created_at ASC LIMIT 1`).bind(browser_id).first();
        const dates = [fp?.created_at, fc?.created_at].filter(Boolean).sort();
        joined_at = dates[0] || null;
      }

      // Worm count: worms other people have given this person (on their posts and chirps)
      const wname = uname || (mod_user_id ? (await env.DB.prepare(`SELECT username FROM mod_users WHERE id = ?`).bind(mod_user_id).first())?.username : null);
      const worm_count = await wormBalance(wname);
      const modRow = uname ? await env.DB.prepare(`SELECT role FROM mod_users WHERE username = ?`).bind(uname).first() : null;
      const role = modRow?.role || null;
      // Flaps: like karma, the flaps other people gave this person's posts. post_votes is small, so read it and look
      // each post up by id (never scan posts).
      const flaps = wname ? ((await env.DB.prepare(`SELECT COUNT(DISTINCT v.post_id || '|' || COALESCE(v.username, 'b:' || v.browser_id)) AS n FROM post_votes v JOIN posts p ON p.id = v.post_id
        WHERE v.value > 0 AND p.username = ?1 AND p.deleted = 0 AND (v.username IS NULL OR v.username != ?1)`).bind(wname).first())?.n || 0) : 0;
      return json({ joined_at, worm_count, role, flaps });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /send-dm ──────────────────────────────────────────────────────────────────

  if (url.pathname === "/send-dm") {
    if (!authUser?.username) return json({ error: "Unauthorized" }, 401);
    const { to_username, content: dmContent, reply_to_id: dmReplyId } = body;
    if (!to_username || !dmContent?.trim()) return json({ error: "Missing fields" }, 400);
    if (to_username === authUser.username) return json({ error: "Cannot message yourself" }, 400);
    // Caged birds can only write in The Cage
    if (!isModerator && await isJailed()) return json({ error: "Caged" }, 403);
    await env.DB.prepare(
      `INSERT INTO private_messages (id, from_username, to_username, content, created_at, reply_to_id) VALUES (?, ?, ?, ?, ?, ?)`
    ).bind(crypto.randomUUID(), authUser.username, to_username, dmContent.trim(), now, dmReplyId || null).run();
    return json({ success: true });
  }

  // ── /dm-inbox ─────────────────────────────────────────────────────────────────

  if (url.pathname === "/dm-inbox") {
    if (!authUser?.username) return json({ error: "Unauthorized" }, 401);
    const me = authUser.username;
    const { results } = await env.DB.prepare(`
      SELECT contact,
        MAX(created_at) as last_at,
        SUM(CASE WHEN from_username != ? AND read_at IS NULL THEN 1 ELSE 0 END) as unread,
        (SELECT content FROM private_messages m2
         WHERE (m2.from_username=contact AND m2.to_username=?) OR (m2.from_username=? AND m2.to_username=contact)
         ORDER BY m2.created_at DESC LIMIT 1) as last_content
      FROM (
        SELECT CASE WHEN from_username=? THEN to_username ELSE from_username END as contact, created_at, from_username, read_at
        FROM private_messages WHERE from_username=? OR to_username=?
      ) GROUP BY contact ORDER BY last_at DESC
    `).bind(me, me, me, me, me, me).all();
    const convs = results || [];
    if (convs.length) {
      const placeholders = convs.map(() => '?').join(',');
      const { results: roles } = await env.DB.prepare(
        `SELECT username, role FROM mod_users WHERE username IN (${placeholders})`
      ).bind(...convs.map(c => c.contact)).all();
      const roleMap = Object.fromEntries((roles || []).map(r => [r.username, r.role]));
      convs.forEach(c => {
        c.is_admin = roleMap[c.contact] === 'admin';
        c.is_mod   = roleMap[c.contact] === 'mod';
      });
    }
    return json({ conversations: convs });
  }

  // ── /dm-thread ────────────────────────────────────────────────────────────────

  if (url.pathname === "/dm-thread") {
    if (!authUser?.username) return json({ error: "Unauthorized" }, 401);
    const me = authUser.username;
    const withUser = url.searchParams.get("with") || body.with;
    if (!withUser) return json({ error: "Missing 'with'" }, 400);
    const { results } = await env.DB.prepare(`
      SELECT id, from_username, to_username, content, created_at, read_at, reply_to_id
      FROM private_messages
      WHERE (from_username=? AND to_username=?) OR (from_username=? AND to_username=?)
      ORDER BY created_at ASC
    `).bind(me, withUser, withUser, me).all();
    const msgs = results || [];
    if (msgs.length) {
      // Attach sender role info (admin/mod) for correct avatar rendering
      const senders = [...new Set(msgs.map(m => m.from_username))];
      if (senders.length) {
        const sph = senders.map(() => '?').join(',');
        const { results: roles } = await env.DB.prepare(
          `SELECT username, role FROM mod_users WHERE username IN (${sph})`
        ).bind(...senders).all();
        const roleMap = Object.fromEntries((roles || []).map(r => [r.username, r.role]));
        msgs.forEach(m => {
          m.is_admin = roleMap[m.from_username] === 'admin';
          m.is_mod   = roleMap[m.from_username] === 'mod';
        });
      }
      const msgIds = msgs.map(m => m.id);
      const ph = msgIds.map(() => '?').join(',');
      const { results: rxs } = await env.DB.prepare(
        `SELECT message_id, from_username, emoji FROM dm_reactions WHERE message_id IN (${ph})`
      ).bind(...msgIds).all();
      const rxMap = {};
      (rxs || []).forEach(r => {
        if (!rxMap[r.message_id]) rxMap[r.message_id] = [];
        rxMap[r.message_id].push({ from_username: r.from_username, emoji: r.emoji });
      });
      msgs.forEach(m => { m.reactions = rxMap[m.id] || []; });
      // Attach reply_to content for quoted replies
      const replyIds = msgs.filter(m => m.reply_to_id).map(m => m.reply_to_id);
      if (replyIds.length) {
        const rph = replyIds.map(() => '?').join(',');
        const { results: rmsgs } = await env.DB.prepare(
          `SELECT id, from_username, content FROM private_messages WHERE id IN (${rph})`
        ).bind(...replyIds).all();
        const replyMap = Object.fromEntries((rmsgs || []).map(r => [r.id, r]));
        msgs.forEach(m => { if (m.reply_to_id) m.reply_to = replyMap[m.reply_to_id] || null; });
      }
    }
    await env.DB.prepare(`UPDATE private_messages SET read_at=? WHERE to_username=? AND from_username=? AND read_at IS NULL`)
      .bind(now, me, withUser).run();
    return json({ messages: msgs });
  }

  // ── /dm-react ─────────────────────────────────────────────────────────────────

  if (url.pathname === "/dm-react") {
    if (!authUser?.username) return json({ error: "Unauthorized" }, 401);
    const { message_id, emoji } = body;
    if (!message_id || !emoji) return json({ error: "Missing fields" }, 400);
    const existing = await env.DB.prepare(
      `SELECT id FROM dm_reactions WHERE message_id=? AND from_username=? AND emoji=?`
    ).bind(message_id, authUser.username, emoji).first();
    if (existing) {
      await env.DB.prepare(`DELETE FROM dm_reactions WHERE id=?`).bind(existing.id).run();
    } else {
      await env.DB.prepare(
        `INSERT INTO dm_reactions (id, message_id, from_username, emoji, created_at) VALUES (?,?,?,?,?)`
      ).bind(crypto.randomUUID(), message_id, authUser.username, emoji, now).run();
    }
    return json({ success: true });
  }

  // ── /delete-dm ────────────────────────────────────────────────────────────────

  if (url.pathname === "/delete-dm") {
    if (!authUser?.username) return json({ error: "Unauthorized" }, 401);
    const { message_id } = body;
    if (!message_id) return json({ error: "Missing message_id" }, 400);
    await env.DB.prepare(
      `DELETE FROM private_messages WHERE id=? AND from_username=?`
    ).bind(message_id, authUser.username).run();
    return json({ success: true });
  }

  // ── /check-role ───────────────────────────────────────────────────────────────

  if (url.pathname === "/check-role") {
    if (!authUser) return json({ error: "Unauthorized" }, 401);
    try {
      const user = await env.DB.prepare(`SELECT role FROM mod_users WHERE id = ?`).bind(authUser.sub).first();
      if (!user) return json({ role_mismatch: false });
      return json({ role_mismatch: user.role !== authUser.role, current_role: user.role });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /clear-notifications ─────────────────────────────────────────────────────

  if (url.pathname === "/clear-notifications") {
    try {
      const clearUserId = authUser?.username || null;
      if (!clearUserId) return signInRequired();
      // Delete all non-watermark notifications for this user, except invitations / requests still waiting on them
      const keep = await waitingOn(clearUserId);
      await env.DB.prepare(`DELETE FROM system_notifications WHERE user_id = ? AND message != '__cleared__' AND id NOT IN (${ID_LIST})`).bind(clearUserId, JSON.stringify(keep)).run();
      // Upsert a cleared watermark so future fetches know the cutoff time
      const existing = await env.DB.prepare(`SELECT id FROM system_notifications WHERE user_id = ? AND message = '__cleared__' LIMIT 1`).bind(clearUserId).first();
      if (existing) {
        await env.DB.prepare(`UPDATE system_notifications SET created_at = ? WHERE id = ?`).bind(now, existing.id).run();
      } else {
        await env.DB.prepare(`INSERT INTO system_notifications (id, user_id, message, created_at) VALUES (?, ?, '__cleared__', ?)`).bind(crypto.randomUUID(), clearUserId, now).run();
      }
      return json({ success: true, clearedAt: now });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /notifications ────────────────────────────────────────────────────────────

  // One list for both the notifications page and the red bubble, so the bubble only ever counts
  // things you can see (and mark read) in the list. Your own actions never notify you, from any device.
  const buildNotifs = async (browser_id) => {
      const me = authUser.username;
      const mod_user_id = isModerator ? authUser.sub : null;
      const uname = isModerator ? null : authUser.username;

      // Check for cleared watermark — only show notifications after this time
      const notifUserId = authUser?.username || mod_user_id || null;
      let clearedSince = new Date(0).toISOString();
      if (notifUserId) {
        const wm = await env.DB.prepare(`SELECT created_at FROM system_notifications WHERE user_id = ? AND message = '__cleared__' LIMIT 1`).bind(notifUserId).first();
        if (wm) clearedSince = wm.created_at;
      }

      let postIds = [], commentIds = [], postTitleMap = {}, commentPostMap = {};

      if (mod_user_id) {
        const { results: mp } = await env.DB.prepare(`SELECT id, title FROM posts WHERE mod_user_id = ? AND deleted = 0`).bind(mod_user_id).all();
        const { results: mc } = await env.DB.prepare(`SELECT id, post_id FROM comments WHERE mod_user_id = ? AND deleted = 0`).bind(mod_user_id).all();
        postIds = (mp || []).map(p => p.id); (mp || []).forEach(p => postTitleMap[p.id] = p.title);
        commentIds = (mc || []).map(c => c.id); (mc || []).forEach(c => commentPostMap[c.id] = c.post_id);
      } else if (uname) {
        const { results: mp } = await env.DB.prepare(`SELECT id, title FROM posts WHERE username = ? AND is_mod = 0 AND deleted = 0 AND (is_huddle = 0 OR is_huddle IS NULL)`).bind(uname).all();
        const { results: mc } = await env.DB.prepare(`SELECT id, post_id FROM comments WHERE username = ? AND is_mod = 0 AND deleted = 0`).bind(uname).all();
        postIds = (mp || []).map(p => p.id); (mp || []).forEach(p => postTitleMap[p.id] = p.title);
        commentIds = (mc || []).map(c => c.id); (mc || []).forEach(c => commentPostMap[c.id] = c.post_id);
      }

      const results = [];
      if (postIds.length) {
        const ph = ID_LIST;
        const { results: comments } = await env.DB.prepare(
          `SELECT id, content, username, browser_id, post_id, MAX(created_at) as created_at FROM comments WHERE post_id IN (${ph}) AND browser_id != ? AND (username IS NULL OR username != ?) AND deleted = 0 AND parent_comment_id IS NULL AND created_at > ? GROUP BY post_id ORDER BY created_at DESC LIMIT 60`
        ).bind(JSON.stringify(postIds), browser_id, me, clearedSince).all();
        (comments || []).forEach(c => results.push({ id: `c-${c.post_id}`, type: "comment", icon: "💬", text: `${c.username || "Someone"} commented on your post`, subtext: `"${(postTitleMap[c.post_id] || "").slice(0, 50)}"`, preview: (c.content || "").slice(0, 80), time: c.created_at, postId: c.post_id, targetId: c.id }));
        const { results: votes } = await env.DB.prepare(
          `SELECT post_id, value, browser_id, username, created_at FROM post_votes WHERE post_id IN (${ph}) AND browser_id != ? AND (username IS NULL OR username != ?) AND created_at > ? ORDER BY created_at DESC LIMIT 60`
        ).bind(JSON.stringify(postIds), browser_id, me, clearedSince).all();
        (votes || []).forEach((v, i) => { const who = v.username || `Anon`; results.push({ id: `v-${v.post_id}-${v.browser_id}`, type: "vote", icon: "🪽", text: `${who} flapped your post. Flap flap!`, subtext: `"${(postTitleMap[v.post_id] || "").slice(0, 50)}"`, time: v.created_at, postId: v.post_id }); });
      }
      // Worms given to you, on your posts and chirps: one rolling notification per person per post or chirp (it moves
      // to the top and counts as new again when they give more, like chirp notifications)
      if (me) {
        const { results: wg = [] } = await env.DB.prepare(
          `SELECT giver, post_id, comment_id, MAX(created_at) AS created_at, COUNT(*) AS n FROM worms WHERE receiver = ? AND giver != ? AND giver != '__hunt__' AND created_at > ? GROUP BY giver, post_id, comment_id ORDER BY created_at DESC LIMIT 60`
        ).bind(me, me, clearedSince).all();
        if (wg.length) {
          const cids = [...new Set(wg.filter(w => w.comment_id).map(w => w.comment_id))];
          const cm = new Map();
          if (cids.length) {
            const { results: cr = [] } = await env.DB.prepare(`SELECT id, post_id, content FROM comments WHERE id IN (${ID_LIST})`).bind(JSON.stringify(cids)).all();
            for (const r of cr) cm.set(r.id, r);
          }
          const pids = [...new Set(wg.map(w => w.post_id || cm.get(w.comment_id)?.post_id).filter(Boolean))];
          const titles = new Map();
          if (pids.length) {
            const { results: pr = [] } = await env.DB.prepare(`SELECT id, title FROM posts WHERE id IN (${ID_LIST})`).bind(JSON.stringify(pids)).all();
            for (const r of pr) titles.set(r.id, r.title || "");
          }
          for (const w of wg) {
            const c = w.comment_id ? cm.get(w.comment_id) : null;
            if (w.comment_id && !c) continue;
            const postId = w.post_id || c.post_id, many = w.n === 1 ? "a worm" : `${w.n} worms`;
            results.push({ id: `w-${w.giver}-${w.comment_id || w.post_id}`, type: "worm", icon: "🪱",
              text: c ? `${w.giver} fed you ${many} for your chirp. Yummy!` : `${w.giver} fed you ${many}. Yummy!`,
              subtext: `"${(titles.get(postId) || "").slice(0, 50)}"`, preview: c ? (String(c.content || "").split(/\s*\[ATTACH/)[0].trim() || "Photo").slice(0, 80) : undefined,
              time: w.created_at, postId, targetId: w.comment_id || undefined });
          }
        }
      }
      if (commentIds.length) {
        const ph = ID_LIST;
        const { results: replies } = await env.DB.prepare(
          `SELECT id, content, username, browser_id, post_id, parent_comment_id, MAX(created_at) as created_at FROM comments WHERE parent_comment_id IN (${ph}) AND browser_id != ? AND (username IS NULL OR username != ?) AND deleted = 0 AND created_at > ? GROUP BY parent_comment_id ORDER BY created_at DESC LIMIT 60`
        ).bind(JSON.stringify(commentIds), browser_id, me, clearedSince).all();
        (replies || []).forEach(r => results.push({ id: `r-${r.parent_comment_id}`, type: "reply", icon: "↩️", text: `${r.username || "Someone"} replied to your comment`, preview: (r.content || "").slice(0, 80), time: r.created_at, postId: r.post_id, targetId: r.id }));
        const { results: reactions } = await env.DB.prepare(
          `SELECT comment_id, emoji, browser_id, username, created_at FROM comment_reactions WHERE comment_id IN (${ph}) AND browser_id != ? AND (username IS NULL OR username != ?) AND created_at > ? ORDER BY created_at DESC LIMIT 60`
        ).bind(JSON.stringify(commentIds), browser_id, me, clearedSince).all();
        (reactions || []).forEach((r, i) => { const who = r.username || `Anon`; results.push({ id: `rx-${r.comment_id}-${r.browser_id}-${r.emoji}`, type: "reaction", icon: r.emoji, text: `${who} reacted ${r.emoji} to your comment`, time: r.created_at, postId: commentPostMap[r.comment_id], targetId: r.comment_id }); });
      }
      if (mod_user_id) {
        const { results: sysN } = await env.DB.prepare(
          `SELECT id, message, created_at FROM system_notifications WHERE user_id = ? AND message != '__cleared__' AND created_at > ? ORDER BY created_at DESC LIMIT 20`
        ).bind(mod_user_id, clearedSince).all();
        (sysN || []).forEach(n => results.push({ id: `sys-${n.id}`, type: "system", icon: "🔔", text: n.message, time: n.created_at }));
      }
      // Huddle notifications by username (with JSON message parsing for postId)
      const notifUname = uname || authUser?.username || null;
      if (notifUname) {
        const { results: huddleN } = await env.DB.prepare(
          `SELECT id, message, created_at FROM system_notifications WHERE user_id = ? AND message != '__cleared__' AND created_at > ? ORDER BY created_at DESC LIMIT 30`
        ).bind(notifUname, clearedSince).all();
        // Invitations / requests are listed even from before a Clear all (only ones still waiting survive it)
        const { results: reqN = [] } = await env.DB.prepare(
          `SELECT id, message, created_at FROM system_notifications WHERE user_id = ? AND message LIKE '%"req":"%' ORDER BY created_at DESC LIMIT 40`
        ).bind(notifUname).all();
        const seenRows = new Set((huddleN || []).map(n => n.id));
        for (const n of reqN) if (!seenRows.has(n.id)) { n.preClear = n.created_at <= clearedSince; huddleN.push(n); }
        const reqIds = [];
        (huddleN || []).forEach(n => {
          let text = n.message, postId = undefined, req = undefined;
          let preview, icon, targetId, link, alert, an;
          try { const parsed = JSON.parse(n.message); text = parsed.text || text; postId = parsed.postId; req = parsed.req; preview = parsed.preview; icon = parsed.icon; targetId = parsed.targetId; if (parsed.alert) { link = parsed.link; alert = parsed.alert; an = parsed.n; } } catch {}
          if (req) reqIds.push(req);
          results.push({ id: `hsys-${n.id}`, type: "system", icon: icon || (req ? "📨" : "👥"), text, postId, targetId, time: n.created_at, req, preview, link, alert, an, preClear: n.preClear || undefined });
        });
        // Invitations and requests carry their state, and whether this bird is the one who answers them
        if (reqIds.length) {
          const { results: rqs = [] } = await env.DB.prepare(
            `SELECT r.id, r.kind, r.status, r.target, r.created_at, p.username AS owner, p.deleted AS gone FROM huddle_requests r LEFT JOIN posts p ON p.id = r.post_id WHERE r.id IN (${ID_LIST})`
          ).bind(JSON.stringify(reqIds)).all();
          const byId = new Map(rqs.map(r => [r.id, r])), cut = requestCutoff(), lower = me.toLowerCase();
          for (const n of results) {
            if (!n.req) continue;
            const r = byId.get(n.req);
            if (!r) { delete n.req; continue; }
            const status = r.status === "pending" && (r.created_at < cut || r.gone || r.owner == null) ? "expired" : r.status;
            const act = r.kind === "invite" ? r.target.toLowerCase() === lower : (r.owner || "").toLowerCase() === lower;
            n.req = { id: r.id, kind: r.kind, status, act: status === "pending" && act };
            if (n.req.act) n.need = true; // waiting on you: pinned, counted and not clearable until answered
          }
        }
        for (let i = results.length - 1; i >= 0; i--) {
          if (results[i].preClear && !results[i].need) results.splice(i, 1);
          else delete results[i].preClear;
        }
      }
      // A chirp that tags you AND is the newest chirp on your post (or a reply to your chirp) gives one
      // notification, the "tagged you" one, not two
      const taggedIn = new Set(results.filter(n => n.icon === "AT" && n.targetId).map(n => n.targetId));
      if (taggedIn.size) for (let i = results.length - 1; i >= 0; i--) {
        if ((results[i].type === "comment" || results[i].type === "reply") && taggedIn.has(results[i].targetId)) results.splice(i, 1);
      }
      results.sort((a, b) => (a.time && b.time) ? new Date(b.time) - new Date(a.time) : a.time ? -1 : 1);
      const names = await extinctNames();
      const { results: hiddenPosts } = await env.DB.prepare(`SELECT id FROM posts INDEXED BY idx_posts_frozen_list WHERE frozen = 1 AND deleted = 0 AND archived = 1`).all();
      const hidden = new Set(isModerator ? [] : (hiddenPosts || []).map(p => p.id));
      return results.filter(n => !hidden.has(n.postId)).map(n => Object.fromEntries(Object.entries(n).map(([k, v]) => [k, scrubNames(v, names)])));
  };

  if (url.pathname === "/notifications") {
    try {
      const browser_id = url.searchParams.get("browser_id") || "";
      if (!authUser?.username) return signInRequired();
      return json({ notifs: await buildNotifs(browser_id) });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /notif-count ──────────────────────────────────────────────────────────────

  // ── /notif-read, /notif-read-all: notification read state on the account ───────

  // ── /admin-huddle-view: an admin's "see all huddles" switch (mod panel) ──
  if (url.pathname === "/admin-huddle-view") {
    if (!isAdmin) return json({ error: "Unauthorized" }, 403);
    if (request.method === "POST") {
      const on = body.on === true ? 1 : 0;
      await env.DB.prepare(`UPDATE mod_users SET see_all_huddles = ? WHERE id = ?`).bind(on, authUser.sub).run();
      return json({ on: !!on });
    }
    return json({ on: !!authUser.see_all_huddles });
  }

  // ── /huddle-read: how far you've read a huddle, kept on the account so every device agrees ──
  if (url.pathname === "/huddle-read" && request.method === "POST") {
    if (!authUser?.username) return signInRequired();
    const postId = String(body.post_id || "").slice(0, 80), at = String(body.at || "");
    if (!postId || !/^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}/.test(at)) return json({ error: "Bad request" }, 400);
    const post = await env.DB.prepare(`SELECT id, username, huddle_members, is_huddle FROM posts WHERE id = ?`).bind(postId).first();
    if (!post || !post.is_huddle || (!seeAllHuddles && !isHuddleMember(post, authUser.username))) return json({ error: "Not found" }, 404);
    const t = at > now ? now : at.slice(0, 40);
    await env.DB.prepare(`INSERT INTO huddle_reads (username, post_id, read_at) VALUES (?, ?, ?) ON CONFLICT(username, post_id) DO UPDATE SET read_at = MAX(read_at, excluded.read_at)`)
      .bind(authUser.username.toLowerCase(), postId, t).run();
    return json({ success: true });
  }

  if (url.pathname === "/notif-read" && request.method === "POST") {
    if (!authUser?.username) return signInRequired();
    const id = String(body.id || "").slice(0, 200), t = String(body.time || now).slice(0, 40);
    if (!id) return json({ error: "Missing id" }, 400);
    // Upsert: some notifications are reused and bumped when there's new activity (huddle chirps, comments on a
    // post), so the read record keeps the newest time you've seen for that notification
    await env.DB.prepare(`INSERT INTO notif_reads (user_key, notif_id, notif_time) VALUES (?, ?, ?) ON CONFLICT(user_key, notif_id) DO UPDATE SET notif_time = MAX(notif_time, excluded.notif_time)`).bind(authUser.username, id, t).run();
    return json({ success: true });
  }

  if (url.pathname === "/notif-read-all" && request.method === "POST") {
    if (!authUser?.username) return signInRequired();
    await env.DB.prepare(`INSERT INTO notif_state (user_key, seen_at) VALUES (?, ?) ON CONFLICT(user_key) DO UPDATE SET seen_at = excluded.seen_at`).bind(authUser.username, now).run();
    await env.DB.prepare(`DELETE FROM notif_reads WHERE user_key = ?`).bind(authUser.username).run();
    return json({ success: true, seen_at: now });
  }

  if (url.pathname === "/notif-count") {
    try {
      const browser_id = url.searchParams.get("browser_id") || "";
      if (!authUser?.username) return signInRequired();
      const mod_user_id = isModerator ? authUser.sub : null;
      const uname = isModerator ? null : authUser.username;
      // Read state lives on the account (syncs across devices). First time: seed it from this device.
      const nk = authUser.username;
      let since = url.searchParams.get("since") || new Date(0).toISOString();
      const nst = await env.DB.prepare(`SELECT seen_at FROM notif_state WHERE user_key = ?`).bind(nk).first();
      if (nst) since = nst.seen_at;
      else await env.DB.prepare(`INSERT OR IGNORE INTO notif_state (user_key, seen_at) VALUES (?, ?)`).bind(nk, since).run();
      const list = await buildNotifs(browser_id);
      // A notification is read only if you've seen its latest version: a reused notification that got new
      // activity after you tapped it is unread again (glows, counts) until you tap it again
      const { results: rd = [] } = await env.DB.prepare(`SELECT notif_id, notif_time FROM notif_reads WHERE user_key = ? ORDER BY notif_time DESC LIMIT 500`).bind(nk).all();
      const readAt = new Map(rd.map(r => [r.notif_id, new Date(r.notif_time).getTime() || 0])), sinceMs = new Date(since).getTime();
      const isRead = n => readAt.has(n.id) && readAt.get(n.id) >= (new Date(n.time).getTime() || 0);
      // Invitations / requests waiting on you keep the bubble lit until you answer them
      const count = list.filter(n => n.need || (n.time && new Date(n.time).getTime() > sinceMs && !isRead(n))).length;
      return json({ count, seen_at: since, read: list.filter(isRead).map(n => n.id) });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /my-posts ─────────────────────────────────────────────────────────────────

  if (url.pathname === "/my-posts") {
    try {
      const browser_id = url.searchParams.get("browser_id") || "";
      if (!authUser?.username) return signInRequired();
      const mod_user_id = isModerator ? authUser.sub : null;
      const uname = isModerator ? null : authUser.username;
      let posts;
      if (mod_user_id) {
        const { results } = await env.DB.prepare(`SELECT id, title, board, created_at FROM posts WHERE mod_user_id = ? AND deleted = 0 AND (archived = 0 OR archived IS NULL) ORDER BY created_at DESC LIMIT 100`).bind(mod_user_id).all();
        posts = results;
      } else if (uname) {
        const { results } = await env.DB.prepare(`SELECT id, title, board, created_at FROM posts WHERE username = ? AND is_mod = 0 AND deleted = 0 AND (archived = 0 OR archived IS NULL) ORDER BY created_at DESC LIMIT 100`).bind(uname).all();
        posts = results;
      }
      return json({ posts: posts || [] });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /backfill-username ────────────────────────────────────────────────────────

  if (url.pathname === "/backfill-username") {
    try {
      // Old cached pages still call this. Every post and chirp has a username now, so there's nothing to do.
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /delete-my-post ───────────────────────────────────────────────────────────

  if (url.pathname === "/delete-my-post") {
    try {
      if (!username) return signInRequired();
      const { post_id } = body;
      if (!post_id) return json({ error: "Missing post_id" }, 400);
      const result = await env.DB.prepare(`UPDATE posts SET deleted = 1 WHERE id = ? AND username = ? AND is_mod = 0 AND COALESCE(locked, 0) = 0 AND COALESCE(frozen, 0) = 0`).bind(post_id, username).run();
      if (result.meta?.changes === 0) return json({ error: "Not authorized or already deleted" }, 403);
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /delete-my-comment ────────────────────────────────────────────────────────

  if (url.pathname === "/delete-my-comment") {
    try {
      if (!username) return signInRequired();
      const { comment_id } = body;
      if (!comment_id) return json({ error: "Missing fields" }, 400);
      const result = await env.DB.prepare(`UPDATE comments SET deleted = 1 WHERE id = ? AND username = ? AND is_mod = 0 AND post_id NOT IN (SELECT id FROM posts WHERE id = comments.post_id AND (locked = 1 OR frozen = 1))`).bind(comment_id, username).run();
      if (result.meta?.changes === 0) return json({ error: "Not authorized or already deleted" }, 403);
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /bot-seen ─────────────────────────────────────────────────────────────────

  if (url.pathname === "/bot-seen") {
    if (!isBot) return json({ error: "Unauthorized" }, 401);
    if (request.method === "GET") {
      const row = await env.DB.prepare(`SELECT urls, last_run FROM bot_seen WHERE id = 1`).first();
      try {
        return json({ seen: row?.urls ? JSON.parse(row.urls) : [], last_run: row?.last_run || null });
      } catch { return json({ seen: [], last_run: null }); }
    }
    if (request.method === "POST") {
      if (!Array.isArray(body.seen)) return json({ error: "Missing seen array" }, 400);
      const expectedLastRun = body.expected_last_run || null;
      try {
        let result;
        if (expectedLastRun) {
          result = await env.DB.prepare(
            `UPDATE bot_seen SET urls = ?, last_run = ?, updated_at = ? WHERE id = 1 AND last_run = ?`
          ).bind(JSON.stringify(body.seen.slice(-5000)), body.last_run || now, now, expectedLastRun).run();
        } else {
          result = await env.DB.prepare(
            `UPDATE bot_seen SET urls = ?, last_run = ?, updated_at = ? WHERE id = 1 AND last_run IS NULL`
          ).bind(JSON.stringify(body.seen.slice(-5000)), body.last_run || now, now).run();
        }
        if (result.meta.changes === 0) return json({ success: false, reason: "stale" }, 409);
        return json({ success: true });
      } catch (err) {
        return serverError(err);
      }
    }
  }

  // ── /bot-logs ─────────────────────────────────────────────────────────────────

  if (url.pathname === "/bot-logs") {
    if (!isAdmin && !isBot) return json({ error: "Unauthorized" }, 401);
    const { results } = await env.DB.prepare(
      `SELECT * FROM bot_logs ORDER BY started_at DESC`
    ).all();
    const logs = (results || []).map(r => ({
      ...r,
      posted_articles: (() => { try { return JSON.parse(r.posted_articles); } catch { return []; } })(),
      feed_errors:     (() => { try { return JSON.parse(r.feed_errors);     } catch { return []; } })(),
    }));
    return json({ logs });
  }

  // ── /bot-log/:id ──────────────────────────────────────────────────────────────

  if (url.pathname.startsWith("/bot-log/") && !url.pathname.startsWith("/bot-log-")) {
    let authorized = isAdmin || isBot;
    if (!authorized) {
      const qToken = url.searchParams.get("token");
      if (qToken) {
        const u = await verifyJWT(qToken, env.JWT_SECRET);
        if (u?.role === "admin") authorized = true;
      }
    }
    if (!authorized) return new Response("Unauthorized", { status: 401, headers: corsHeaders });
    const id = url.pathname.slice("/bot-log/".length);
    const row = await env.DB.prepare("SELECT * FROM bot_logs WHERE id = ?").bind(id).first();
    if (!row) return new Response("Log not found", { status: 404, headers: { ...corsHeaders, "Content-Type": "text/plain" } });

    let pa = []; try { pa = JSON.parse(row.posted_articles); } catch {}
    let fe = []; try { fe = JSON.parse(row.feed_errors); } catch {}

    const dur = row.finished_at
      ? Math.round((new Date(row.finished_at) - new Date(row.started_at)) / 1000) + "s"
      : "still running";

    const sep = "─".repeat(60);
    let text = `BOT DEPLOYMENT LOG\n${"=".repeat(60)}\n`;
    text += `ID:          ${row.id}\n`;
    text += `Status:      ${row.status}\n`;
    text += `Run type:    ${row.run_type || "manual"}\n`;
    text += `Started:     ${row.started_at}\n`;
    text += `Finished:    ${row.finished_at || "(still running)"}\n`;
    text += `Duration:    ${dur}\n\n`;

    text += `STATS\n${sep}\n`;
    text += `Posted:      ${row.posted}\n`;
    text += `Skipped:     ${row.skipped_seen} (seen before)\n`;
    text += `Bad titles:  ${row.skipped_bad_title}\n`;
    text += `Failed:      ${row.post_failed}\n`;
    text += `Feed errors: ${fe.length}\n\n`;

    if (pa.length > 0) {
      text += `POSTED ARTICLES (${pa.length})\n${sep}\n`;
      pa.forEach((a, i) => {
        const line = typeof a === "string" ? a : (a.url || a.title || a.link || JSON.stringify(a));
        text += `${i + 1}. ${line}\n`;
      });
      text += "\n";
    }

    if (fe.length > 0) {
      text += `FEED ERRORS (${fe.length})\n${sep}\n`;
      fe.forEach((e, i) => {
        text += `${i + 1}. ${typeof e === "string" ? e : JSON.stringify(e)}\n`;
      });
      text += "\n";
    }

    text += `RAW JSON\n${sep}\n`;
    text += JSON.stringify({ ...row, posted_articles: pa, feed_errors: fe }, null, 2);

    return new Response(text, {
      headers: { ...corsHeaders, "Content-Type": "text/plain; charset=utf-8" },
    });
  }

  // ── /bot-log-create ───────────────────────────────────────────────────────────

  if (url.pathname === "/bot-log-create") {
    if (!isBot) return json({ error: "Unauthorized" }, 401);
    try {
      const id = crypto.randomUUID();
      await env.DB.prepare(`
        INSERT INTO bot_logs (id, status, run_type, posted, posted_articles, feed_errors, skipped_seen, skipped_bad_title, post_failed)
        VALUES (?, 'running', ?, 0, '[]', '[]', 0, 0, 0)
      `).bind(id, body.run_type || "subsequent").run();
      return json({ id });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /bot-log-finish ───────────────────────────────────────────────────────────

  if (url.pathname === "/bot-log-finish") {
    if (!isBot) return json({ error: "Unauthorized" }, 401);
    if (!body.id) return json({ error: "Missing id" }, 400);
    try {
      await env.DB.prepare(`
        UPDATE bot_logs SET status = 'done', finished_at = ?, posted = ?, posted_articles = ?,
          skipped_seen = ?, skipped_bad_title = ?, post_failed = ?, feed_errors = ?
        WHERE id = ?
      `).bind(
        now,
        body.posted || 0,
        JSON.stringify(body.posted_articles || []),
        body.skipped_seen || 0,
        body.skipped_bad_title || 0,
        body.post_failed || 0,
        JSON.stringify(body.feed_errors || []),
        body.id
      ).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /bot-log-expire ───────────────────────────────────────────────────────────

  if (url.pathname === "/bot-log-expire") {
    if (!isBot && !isAdmin) return json({ error: "Unauthorized" }, 401);
    try {
      // Mark any "running" logs older than 30 minutes as "error"
      await env.DB.prepare(`
        UPDATE bot_logs SET status = 'error', finished_at = ?
        WHERE status = 'running'
          AND started_at < datetime('now', '-30 minutes')
      `).bind(now).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /bot-log-delete ───────────────────────────────────────────────────────────

  if (url.pathname === "/bot-log-delete") {
    if (!isAdmin) return json({ error: "Unauthorized" }, 401);
    if (!body.id) return json({ error: "Missing id" }, 400);
    try {
      await env.DB.prepare(`DELETE FROM bot_logs WHERE id = ?`).bind(body.id).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }

  // ── /bot-trigger ──────────────────────────────────────────────────────────────

  if (url.pathname === "/bot-trigger") {
    if (!isAdmin) return json({ error: "Unauthorized" }, 401);
    const ghPat = env.GITHUB_PAT;
    if (!ghPat) return json({ error: "GITHUB_PAT not configured" }, 500);
    const ghRepo = env.GITHUB_REPO || "coldbrainarchive/perchposts";
    ctx.waitUntil(
      fetch(`https://api.github.com/repos/${ghRepo}/actions/workflows/news-bot.yml/dispatches`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${ghPat}`,
          "Accept": "application/vnd.github+json",
          "X-GitHub-Api-Version": "2022-11-28",
          "Content-Type": "application/json",
          "User-Agent": "daboysforum-worker",
        },
        body: JSON.stringify({ ref: "main" }),
      }).catch(err => console.error("GitHub dispatch error:", err.message))
    );
    return json({ success: true });
  }

  // ── /link-preview ─────────────────────────────────────────────────────────────
  // Replaces microlink.io: the linked site only sees Cloudflare, nobody outside learns who shared what.
  // Signed-in only, so it can't be used as a free page-fetching service. Same answer shape as microlink.
  if (url.pathname === "/link-preview" && request.method === "GET") {
    if (!username) return signInRequired();
    const target = url.searchParams.get("url") || "";
    if (!target || target.length > 2000) return json({ status: "fail", message: "Missing url" }, 400);
    try {
      const p = await linkPreview(target);
      if (!p) return json({ status: "fail" });
      return json({ status: "success", data: { url: p.url, title: p.title || null, description: p.description || null, image: p.image ? { url: p.image } : null } });
    } catch (err) {
      return json({ status: "fail" });
    }
  }

  // ── /my-username ──────────────────────────────────────────────────────────────

  if (url.pathname === "/my-username") {
    return json({ username });
  }

  // ── /get-ban-lists ────────────────────────────────────────────────────────────

  if (url.pathname === "/get-ban-lists") {
    const [bansRes, jailedRes, staffRes] = await Promise.all([
      env.DB.prepare(`SELECT DISTINCT username FROM bans WHERE username IS NOT NULL`).all(),
      env.DB.prepare(`SELECT DISTINCT username FROM jailed WHERE username IS NOT NULL`).all(),
      // Staff names (already public on their tags), so mod purple / admin white show on every tag, old posts included
      env.DB.prepare(`SELECT username, role FROM mod_users WHERE role IN ('mod','admin') AND deleted_at IS NULL AND username IS NOT NULL`).all()
    ]);
    const staff = staffRes.results || [];
    return json({
      banned: (bansRes.results || []).map(r => r.username),
      jailed: (jailedRes.results || []).map(r => r.username),
      mods: staff.filter(r => r.role === "mod").map(r => r.username),
      admins: staff.filter(r => r.role === "admin").map(r => r.username)
    });
  }

  return new Response("OK", { headers: corsHeaders });
}
