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
      return new Response(JSON.stringify({ error: err.message, stack: err.stack }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" }
      });
    }
  },

  // Hourly: make sure the read-saving indexes exist (self-heals if they go missing,
  // and retries automatically if D1 is still over its daily limit).
  async scheduled(event, env, ctx) {
    ctx.waitUntil(ensureIndexes(env, event));
  }
};

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
const BOARD_NAMES = { general: "General", sports: "Sports", "science-nature": "Science", random: "Random", announcements: "Announcements", cage: "The Cage" };
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
// A country pill keeps to that country's home region, so BBC Africa stays out of the UK pill
const inHomeRegion = (p, country) =>
  p.country === country && (!p.continent || !COUNTRY_REGION[country] || p.continent === COUNTRY_REGION[country]);
const regionWhere = region => ({
  sql: `(continent = ? OR (continent IS NULL AND country IN (${ID_LIST})))`,
  params: [region, JSON.stringify(REGION_COUNTRIES[region] || [])]
});
const countryWhere = country => COUNTRY_REGION[country]
  ? { sql: `(country = ? AND (continent IS NULL OR continent = ?))`, params: [country, COUNTRY_REGION[country]] }
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
    (!continent || regionOf(p) === continent) &&
    (!country || inHomeRegion(p, country));
  const page = posts => posts.map(p => boolify(p, POST_BOOL_FIELDS));

  if (activity) {
    // Flock: posts by people, plus bot posts that have comments — both small sets
    const cond = [LIVE_POSTS];
    const params = [];
    if (before) { cond.push("last_activity < ?"); params.push(before); }
    const where = cond.join(" AND ");
    const [commented, human] = await Promise.all([
      env.DB.prepare(
        `SELECT rowid AS _rid, * FROM posts WHERE id IN (SELECT post_id FROM comments WHERE deleted = 0) AND ${where} ORDER BY last_activity DESC LIMIT ?`
      ).bind(...params, limit).all(),
      // INDEXED BY fails fast instead of scanning every post if the index is missing
      env.DB.prepare(
        `SELECT rowid AS _rid, * FROM posts INDEXED BY idx_posts_human_activity WHERE ${HUMAN_POSTS} AND ${where} ORDER BY last_activity DESC LIMIT ?`
      ).bind(...params, limit).all().catch(err => {
        console.error("get-posts activity: human posts unavailable:", err.message);
        return { results: [] };
      })
    ]);
    const c = commented.results || [], h = human.results || [];
    const byId = new Map([...h, ...c].map(p => [p.id, p]));
    const scanned = [...byId.values()]
      .sort((a, b) => String(b.last_activity || "").localeCompare(String(a.last_activity || "")))
      .slice(0, limit);
    const more = c.length === limit || h.length === limit;
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

  const ip = request.headers.get("CF-Connecting-IP") || "0.0.0.0";
  const hashBuffer = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(ip));
  const ip_hash = Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, "0")).join("");

  const body = (request.method !== "GET" && url.pathname !== "/upload") ? await request.json().catch(() => ({})) : {};
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
    return next;
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
      const account = await env.DB.prepare(`SELECT deleted_at FROM mod_users WHERE id = ?`).bind(user.sub).first();
      if (!account || account.deleted_at) return null;
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
    const key = url.pathname.slice("/media/".length);
    if (!key) return new Response("Not found", { status: 404 });
    try {
      const object = await env.MEDIA.get(key);
      if (!object) return new Response("Not found", { status: 404 });
      const headers = new Headers();
      object.writeHttpMetadata(headers);
      headers.set("etag", object.httpEtag);
      headers.set("cache-control", "public, max-age=31536000, immutable");
      headers.set("access-control-allow-origin", "*");
      return new Response(object.body, { headers });
    } catch (err) {
      return new Response("Error", { status: 500 });
    }
  }

  // ── /upload ───────────────────────────────────────────────────────────────────

  if (url.pathname === "/upload" && request.method === "POST") {
    if (!username) return signInRequired();
    try {
      const formData = await request.formData();
      const file = formData.get("file");
      if (!file) return json({ error: "No file provided" }, 400);

      const ALLOWED = /^(image\/(jpeg|png|gif|webp)|video\/(mp4|webm|quicktime))$/;
      if (!ALLOWED.test(file.type)) return json({ error: "Unsupported file type" }, 400);

      const MAX_SIZE = 50 * 1024 * 1024; // 50 MB
      const buffer = await file.arrayBuffer();
      if (buffer.byteLength > MAX_SIZE) return json({ error: "File too large (max 50 MB)" }, 400);

      const ext = (file.name || "file").split(".").pop().toLowerCase().replace(/[^a-z0-9]/g, "") || "bin";
      const key = `${crypto.randomUUID()}.${ext}`;

      await env.MEDIA.put(key, buffer, {
        httpMetadata: { contentType: file.type, cacheControl: "public, max-age=31536000, immutable" }
      });

      return json({ url: `${url.origin}/media/${key}` });
    } catch (err) {
      return json({ error: err.message }, 500);
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
      // Retired names stay taken: the site knows people by name, so a reused one would inherit someone's posts
      const existing = await env.DB.prepare(`SELECT id FROM mod_users WHERE LOWER(username) = LOWER(?)`).bind(uname.trim()).first();
      if (existing) return json({ error: "Username already taken" }, 409);
      const id = crypto.randomUUID();
      const hash = await hashPassword(password);
      await env.DB.prepare(
        `INSERT INTO mod_users (id, email, password_hash, username, role, created_at) VALUES (?, ?, ?, ?, 'user', ?)`
      ).bind(id, `${uname.trim().toLowerCase()}@users.local`, hash, uname.trim(), now).run();
      if (bid) {
        await env.DB.prepare(`UPDATE posts SET username = ? WHERE browser_id = ? AND is_mod = 0 AND username IS NULL`).bind(uname.trim(), bid).run();
        await env.DB.prepare(`UPDATE comments SET username = ? WHERE browser_id = ? AND is_mod = 0 AND username IS NULL`).bind(uname.trim(), bid).run();
      }
      const token = await signJWT(
        { sub: id, role: "user", username: uname.trim(), exp: Math.floor(Date.now() / 1000) + 86400 * 90 },
        env.JWT_SECRET
      );
      return json({ token, user: { id, role: "user", username: uname.trim() } });
    } catch (err) {
      return json({ error: err.message }, 500);
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
      const ok = await verifyPassword(password, user.password_hash);
      if (!ok) return json({ error: "Invalid credentials" }, 401);
      const token = await signJWT(
        { sub: user.id, role: user.role, username: user.username, exp: Math.floor(Date.now() / 1000) + 86400 * 90 },
        env.JWT_SECRET
      );
      return json({ token, user: { id: user.id, role: user.role, username: user.username } });
    } catch (err) {
      return json({ error: err.message }, 500);
    }
  }

  // ── /update-password ──────────────────────────────────────────────────────────

  if (url.pathname === "/update-password" && request.method === "POST") {
    if (!authUser) return json({ error: "Unauthorized" }, 401);
    const { newPassword } = body;
    if (!newPassword) return json({ error: "Missing newPassword" }, 400);
    try {
      const hash = await hashPassword(newPassword);
      await env.DB.prepare(`UPDATE mod_users SET password_hash = ? WHERE id = ?`)
        .bind(hash, authUser.sub).run();
      return json({ success: true });
    } catch (err) {
      return json({ error: err.message }, 500);
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
      if (caged) {
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
      // Bots can't post an article twice
      let botClaim = null;
      if (isBot) {
        botClaim = await claimBotPost(env, botPostKeys(body.content), now);
        if (botClaim.duplicate) return json({ success: false, duplicate: true }, 409);
      }
      const huddleMembers = isHuddle ? JSON.stringify(Array.isArray(body.huddle_members) ? body.huddle_members : []) : null;
      const id = crypto.randomUUID();
      await env.DB.prepare(`
        INSERT INTO posts (id, title, content, username, ip_hash, browser_id, last_activity,
          is_mod, is_admin, moderator, mod_user_id, continent, country, board, community_id,
          is_huddle, huddle_members, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        now
      ).run().catch(async err => {
        // The post didn't save, so the article can be tried again next run
        for (const key of botClaim?.claimed || []) {
          await env.DB.prepare(`DELETE FROM bot_links WHERE url = ?`).bind(key).run().catch(() => {});
        }
        throw err;
      });
      // Notify huddle members
      if (isHuddle && huddleMembers) {
        const members = JSON.parse(huddleMembers);
        const huddleTitle = body.title || "Huddle";
        for (const memberUsername of members.map(normMember)) {
          if (memberUsername === username) continue;
          const notifMsg = JSON.stringify({ text: `${username} added you to a huddle: "${huddleTitle}"`, postId: id });
          await upsertNotif(memberUsername, notifMsg, id);
        }
      }
      const post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ?`).bind(id).first();
      return json({ success: true, post: boolify(post, POST_BOOL_FIELDS) });
    } catch (err) {
      return json({ error: err.message }, 500);
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
        if (!isModerator && !isHuddleMember(post, username)) {
          return json({ error: "not_member", huddle: true }, 403);
        }
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
      // Top chirps of the whole conversation (1+ reactions while the site is small; most reacted first, newest wins ties) for the post page
      // preview; they may be older than the loaded page, so their reactions ride along below
      const { results: topRows } = await env.DB.prepare(
        `SELECT c.*, COUNT(r.id) AS rx_count FROM comments c JOIN comment_reactions r ON r.comment_id = c.id WHERE c.post_id = ? AND c.deleted = 0 GROUP BY c.id HAVING COUNT(r.id) >= 1 ORDER BY rx_count DESC, c.created_at DESC LIMIT 6`
      ).bind(id).all();
      const top = topRows || [];
      // Most replied chirps (1+ replies while the site is small), for the preview's "Most replied" section
      const { results: repRows } = await env.DB.prepare(
        `SELECT c.*, COUNT(r.id) AS reply_count FROM comments c JOIN comments r ON r.parent_comment_id = c.id AND r.deleted = 0 WHERE c.post_id = ? AND c.deleted = 0 GROUP BY c.id HAVING COUNT(r.id) >= 1 ORDER BY reply_count DESC, c.created_at DESC LIMIT 9`
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
      return json({ error: err.message }, 500);
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
      const rankSort = url.searchParams.get("sort");
      if (rankSort === "flaps" || rankSort === "chirps") {
        const range = url.searchParams.get("range");
        const since = range === "all" ? "" : new Date(Date.now() - (range === "day" ? 1 : 7) * 86400000).toISOString();
        // Count the flaps / chirps made in the range (on posts of any age): "Most chirps today" = the posts
        // that got the most chirps today. Before, it only looked at posts created in the range.
        const { results: top = [] } = await env.DB.prepare(rankSort === "flaps"
          ? `SELECT post_id, SUM(value) AS n FROM post_votes WHERE created_at >= ? GROUP BY post_id HAVING n > 0 ORDER BY n DESC LIMIT 500`
          : `SELECT post_id, COUNT(*) AS n FROM comments WHERE deleted = 0 AND (username IS NULL OR username != '__system__') AND created_at >= ? GROUP BY post_id ORDER BY n DESC LIMIT 500`
        ).bind(since).all();
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
        q += ` AND (username NOT IN (${placeholders}) OR id IN (SELECT DISTINCT post_id FROM comments WHERE deleted = 0))`;
        params.push(...BOTS);
      }
      if (isHuddleBoard) {
        // Huddles board: only is_huddle posts, filtered by JWT-authenticated username only (no spoofable query param)
        q += ` AND is_huddle = 1`;
        const huddleUsername = authUser?.username || null;
        if (!isModerator) {
          if (huddleUsername) {
            q += ` AND (LOWER(username) = LOWER(?) OR (huddle_members IS NOT NULL AND LOWER(huddle_members) LIKE LOWER(?)))`;
            params.push(huddleUsername, `%"${huddleUsername}"%`);
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
      if (username)  { q += ` AND LOWER(username) = ?`;  params.push(username.toLowerCase()); }
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
      return json({
        posts: await publicRows(await addCommentCounts(env, rows.map(p => boolify(p, POST_BOOL_FIELDS)))),
        next_before: nextBefore
      });
    } catch (err) {
      return json({ error: err.message }, 500);
    }
  }

  // ── /get-comments-index ───────────────────────────────────────────────────────

  if (url.pathname === "/get-comments-index") {
    try {
      const { results } = await env.DB.prepare(
        `SELECT id, post_id, parent_comment_id FROM comments WHERE deleted = 0 AND (username IS NULL OR username != '__system__')`
      ).all();
      return json(results || []);
    } catch (err) {
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
    }
  }

  // ── /purge-deleted ────────────────────────────────────────────────────────────

  if (url.pathname === "/purge-deleted") {
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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
      if (target?.is_huddle && !isModerator && !isHuddleMember(target, username)) return json({ error: "Not a member of this huddle" }, 403);
      if (!isModerator && await isJailed()) {
        const post = await env.DB.prepare(`SELECT board, community_id FROM posts WHERE id = ?`).bind(body.post_id).first();
        const postBoard = (post?.board || post?.community_id || "").toLowerCase();
        if (!post || (postBoard !== "cage" && postBoard !== "the cage")) return json({ error: "Caged" }, 403);
      }
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
      return json({ error: err.message }, 500);
    }
  }

  // ── /invite-to-huddle ─────────────────────────────────────────────────────────

  if (url.pathname === "/invite-to-huddle") {
    try {
      if (!username) return signInRequired();
      const { post_id, invite_username } = body;
      if (!post_id || !invite_username) return json({ error: "Missing fields" }, 400);
      const post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ? AND deleted = 0`).bind(post_id).first();
      if (!post || !post.is_huddle) return json({ error: "Not found" }, 404);
      if (post.frozen) return json({ error: "This huddle is archived" }, 403);
      const members = JSON.parse(post.huddle_members || "[]");
      if (!isModerator && !isHuddleMember(post, username)) return json({ error: "Unauthorized" }, 403);
      const normInvUser = normMember(invite_username);
      if ((await extinctNames()).has(normInvUser)) return json({ error: "That bird is extinct" }, 404);
      if (members.map(normMember).includes(normInvUser)) return json({ error: "Already a member" }, 400);
      members.push(invite_username); // store with role suffix for frontend display
      await env.DB.prepare(`UPDATE posts SET huddle_members = ?, last_activity = ? WHERE id = ?`)
        .bind(JSON.stringify(members), now, post_id).run();
      const sysCommentId = crypto.randomUUID();
      const sysContent = `👥 ${normInvUser} was added to the huddle`;
      await env.DB.prepare(`INSERT INTO comments (id, content, post_id, parent_comment_id, username, ip_hash, browser_id, is_mod, is_admin, moderator, mod_user_id, created_at) VALUES (?, ?, ?, NULL, '__system__', NULL, NULL, 0, 0, 0, NULL, ?)`)
        .bind(sysCommentId, sysContent, post_id, now).run().catch(() => {});
      const huddleTitle = post.title || "Huddle";
      // Notify the invited person
      const inviteMsg = JSON.stringify({ text: `${username} invited you to "${huddleTitle}"`, postId: post_id });
      await upsertNotif(normInvUser, inviteMsg, post_id);
      // Notify all existing members that someone was invited
      const existingMembers = [...members.map(normMember), post.username].filter(Boolean);
      for (const mu of existingMembers) {
        if (!mu || mu === username || mu === normInvUser) continue;
        const broadcastMsg = JSON.stringify({ text: `${username} invited ${normInvUser} to "${huddleTitle}"`, postId: post_id });
        await upsertNotif(mu, broadcastMsg, post_id);
      }
      // Notify the actor (inviter) so they see it in their own panel
      if (username) {
        await upsertNotif(username, JSON.stringify({ text: `You invited ${normInvUser} to "${huddleTitle}"`, postId: post_id }), post_id);
      }
      // Construct updated post from known data — avoids D1 read-after-write stale reads
      const updatedPost = { ...post, huddle_members: JSON.stringify(members), last_activity: now };
      return json({ success: true, post: boolify(updatedPost, POST_BOOL_FIELDS), systemComment: { id: sysCommentId, content: sysContent, username: '__system__', created_at: now, parent_comment_id: null, browser_id: null, is_mod: 0 } });
    } catch (err) {
      return json({ error: err.message }, 500);
    }
  }

  // ── /edit-huddle-title ────────────────────────────────────────────────────────

  if (url.pathname === "/edit-huddle-title") {
    try {
      if (!username) return signInRequired();
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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
      if (!isCreator && !isModerator) return json({ error: "Unauthorized" }, 403);
      const members = JSON.parse(post.huddle_members || "[]");
      const targetMember = members.find(m => normMember(m).toLowerCase() === remove_username.toLowerCase());
      if (!targetMember) return json({ error: "Not a member" }, 404);
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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
    }
  }

  // ── /vote-post ────────────────────────────────────────────────────────────────

  if (url.pathname === "/vote-post") {
    if (!username) return signInRequired();
    try {
      if (!body.post_id || !body.browser_id || ![1, 0].includes(body.value))
        return json({ error: "Missing or invalid fields" }, 400);
      if (await isBanned()) return json({ error: "Banned" }, 403);
      const votedPost = await env.DB.prepare(`SELECT frozen FROM posts WHERE id = ?`).bind(body.post_id).first();
      if (votedPost?.frozen) return json({ error: "This post is archived" }, 403);

      // Read current state BEFORE write to avoid D1 eventual-consistency race
      const [existing, preSummary] = await Promise.all([
        env.DB.prepare(`SELECT id, value FROM post_votes WHERE post_id = ? AND browser_id = ?`).bind(body.post_id, body.browser_id).first(),
        getPostVoteSummary(body.post_id, body.browser_id),
      ]);
      const prevValue = existing?.value || 0;
      const prevScore = preSummary.score;
      const prevCount = preSummary.voteCount;

      if (body.value === 0) {
        if (existing?.id) {
          await env.DB.prepare(`DELETE FROM post_votes WHERE id = ?`).bind(existing.id).run();
        }
        const newScore = prevScore - prevValue;
        const newCount = existing?.id ? prevCount - 1 : prevCount;
        return json({ success: true, score: newScore, myVote: 0, voteCount: newCount });
      }

      if (existing?.id) {
        await env.DB.prepare(`UPDATE post_votes SET value = ?, username = ?, ip_hash = ?, is_mod = ?, mod_user_id = ? WHERE id = ?`)
          .bind(body.value, username, ip_hash, isModerator ? 1 : 0, isModerator ? authUser.sub : null, existing.id).run();
      } else {
        await env.DB.prepare(`
          INSERT INTO post_votes (id, post_id, browser_id, value, username, ip_hash, is_mod, mod_user_id, created_at)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        `).bind(crypto.randomUUID(), body.post_id, body.browser_id, body.value, username, ip_hash,
            isModerator ? 1 : 0, isModerator ? authUser.sub : null, now).run();
      }
      await bumpPost(body.post_id);
      const newScore = prevScore - prevValue + body.value;
      const newCount = existing?.id ? prevCount : prevCount + 1;
      return json({ success: true, score: newScore, myVote: body.value, voteCount: newCount });
    } catch (err) {
      return json({ error: err.message }, 500);
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
      return json({ votes: results || [] });
    } catch (err) {
      return json({ error: err.message }, 500);
    }
  }

  // ── /get-reactions ────────────────────────────────────────────────────────────

  if (url.pathname === "/get-reactions") {
    try {
      const commentIds = (url.searchParams.get("comment_ids") || "").split(",").filter(Boolean);
      if (!commentIds.length) return json({ reactions: [] });
      const placeholders = ID_LIST;
      const { results } = await env.DB.prepare(
        `SELECT comment_id, browser_id, emoji, username, created_at FROM comment_reactions WHERE comment_id IN (${placeholders})`
      ).bind(JSON.stringify(commentIds)).all();
      return json({ reactions: results || [] });
    } catch (err) {
      return json({ error: err.message }, 500);
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
      const reactedPost = await env.DB.prepare(`SELECT p.frozen FROM comments c JOIN posts p ON p.id = c.post_id WHERE c.id = ?`).bind(body.comment_id).first();
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
        }
      }
      return json({ success: true });
    } catch (err) {
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
    }
  }

  // ── /get-members ──────────────────────────────────────────────────────────────

  if (url.pathname === "/get-members") {
    if (!isModerator) return json({ error: "Unauthorized" }, 401);
    try {
      const { results } = await env.DB.prepare(`
        SELECT m.id, m.email, m.username, m.role, m.created_at, m.last_active, m.deleted_at,
          (SELECT p.ip_hash FROM posts p WHERE p.username = m.username AND p.ip_hash IS NOT NULL ORDER BY p.created_at DESC LIMIT 1) as ip_hash,
          (SELECT p.browser_id FROM posts p WHERE p.username = m.username AND p.browser_id IS NOT NULL ORDER BY p.created_at DESC LIMIT 1) as browser_id,
          COALESCE((SELECT COUNT(*) FROM post_votes pv JOIN posts p ON pv.post_id = p.id WHERE p.username = m.username AND pv.value > 0 AND p.deleted = 0 AND (p.archived = 0 OR p.archived IS NULL)), 0)
          + COALESCE((SELECT COUNT(*) FROM comment_reactions cr JOIN comments c ON cr.comment_id = c.id WHERE c.username = m.username AND c.deleted = 0), 0) as worm_count
        FROM mod_users m WHERE m.deleted_at IS NULL ORDER BY m.last_active DESC, m.created_at DESC`).all();
      const members = (results || []).map(u => ({
        id: u.id,
        email: u.email,
        created_at: u.created_at,
        last_active: u.last_active || null,
        worm_count: u.worm_count || 0,
        user_metadata: { username: u.username, role: u.role, ip_hash: u.ip_hash || null, browser_id: u.browser_id || null }
      }));
      return json({ members });
    } catch (err) {
      return json({ error: err.message }, 500);
    }
  }

  // ── /update-member ────────────────────────────────────────────────────────────

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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
        await env.DB.prepare(`DELETE FROM post_votes WHERE post_id = ?`).bind(body.post_id).run();
        await env.DB.prepare(`DELETE FROM comments WHERE post_id = ?`).bind(body.post_id).run();
        await env.DB.prepare(`DELETE FROM posts WHERE id = ?`).bind(body.post_id).run();
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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
    }
  }

  // ── /search-users ─────────────────────────────────────────────────────────────

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

      // Worm count: positive votes on user's posts + reactions on user's comments
      let worm_count = 0;
      let postIds = [], commentIds = [];
      if (mod_user_id) {
        const { results: mp } = await env.DB.prepare(`SELECT id FROM posts WHERE mod_user_id = ? AND deleted = 0 AND (archived = 0 OR archived IS NULL)`).bind(mod_user_id).all();
        const { results: mc } = await env.DB.prepare(`SELECT id FROM comments WHERE mod_user_id = ? AND deleted = 0`).bind(mod_user_id).all();
        postIds = (mp || []).map(p => p.id); commentIds = (mc || []).map(c => c.id);
      } else if (uname) {
        const { results: mp } = await env.DB.prepare(`SELECT id FROM posts WHERE username = ? AND deleted = 0 AND (archived = 0 OR archived IS NULL)`).bind(uname).all();
        const { results: mc } = await env.DB.prepare(`SELECT id FROM comments WHERE username = ? AND deleted = 0`).bind(uname).all();
        postIds = (mp || []).map(p => p.id); commentIds = (mc || []).map(c => c.id);
      } else if (browser_id) {
        const { results: mp } = await env.DB.prepare(`SELECT id FROM posts WHERE browser_id = ? AND deleted = 0 AND (archived = 0 OR archived IS NULL)`).bind(browser_id).all();
        const { results: mc } = await env.DB.prepare(`SELECT id FROM comments WHERE browser_id = ? AND deleted = 0`).bind(browser_id).all();
        postIds = (mp || []).map(p => p.id); commentIds = (mc || []).map(c => c.id);
      }
      if (postIds.length) {
        const ph = ID_LIST;
        const r = await env.DB.prepare(`SELECT COUNT(*) as c FROM post_votes WHERE post_id IN (${ph}) AND value > 0`).bind(JSON.stringify(postIds)).first();
        worm_count += (r?.c || 0);
      }
      if (commentIds.length) {
        const ph = ID_LIST;
        const r = await env.DB.prepare(`SELECT COUNT(*) as c FROM comment_reactions WHERE comment_id IN (${ph})`).bind(JSON.stringify(commentIds)).first();
        worm_count += (r?.c || 0);
      }
      const modRow = uname ? await env.DB.prepare(`SELECT role FROM mod_users WHERE username = ?`).bind(uname).first() : null;
      const role = modRow?.role || null;
      return json({ joined_at, worm_count, role });
    } catch (err) {
      return json({ error: err.message }, 500);
    }
  }

  // ── /send-dm ──────────────────────────────────────────────────────────────────

  if (url.pathname === "/send-dm") {
    if (!authUser?.username) return json({ error: "Unauthorized" }, 401);
    const { to_username, content: dmContent, reply_to_id: dmReplyId } = body;
    if (!to_username || !dmContent?.trim()) return json({ error: "Missing fields" }, 400);
    if (to_username === authUser.username) return json({ error: "Cannot message yourself" }, 400);
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
      return json({ error: err.message }, 500);
    }
  }

  // ── /clear-notifications ─────────────────────────────────────────────────────

  if (url.pathname === "/clear-notifications") {
    try {
      const clearUserId = authUser?.username || null;
      if (!clearUserId) return signInRequired();
      // Delete all non-watermark notifications for this user
      await env.DB.prepare(`DELETE FROM system_notifications WHERE user_id = ? AND message != '__cleared__'`).bind(clearUserId).run();
      // Upsert a cleared watermark so future fetches know the cutoff time
      const existing = await env.DB.prepare(`SELECT id FROM system_notifications WHERE user_id = ? AND message = '__cleared__' LIMIT 1`).bind(clearUserId).first();
      if (existing) {
        await env.DB.prepare(`UPDATE system_notifications SET created_at = ? WHERE id = ?`).bind(now, existing.id).run();
      } else {
        await env.DB.prepare(`INSERT INTO system_notifications (id, user_id, message, created_at) VALUES (?, ?, '__cleared__', ?)`).bind(crypto.randomUUID(), clearUserId, now).run();
      }
      return json({ success: true, clearedAt: now });
    } catch (err) {
      return json({ error: err.message }, 500);
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
        (votes || []).forEach((v, i) => { const who = v.username || `Anon`; results.push({ id: `v-${v.post_id}-${v.browser_id}`, type: "vote", icon: "🪽", text: `${who} gave your post a flap`, subtext: `"${(postTitleMap[v.post_id] || "").slice(0, 50)}"`, time: v.created_at, postId: v.post_id }); });
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
        (huddleN || []).forEach(n => {
          let text = n.message, postId = undefined;
          try { const parsed = JSON.parse(n.message); text = parsed.text || text; postId = parsed.postId; } catch {}
          results.push({ id: `hsys-${n.id}`, type: "system", icon: "👥", text, postId, time: n.created_at });
        });
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
      return json({ error: err.message }, 500);
    }
  }

  // ── /notif-count ──────────────────────────────────────────────────────────────

  // ── /notif-read, /notif-read-all: notification read state on the account ───────

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
      const count = list.filter(n => n.time && new Date(n.time).getTime() > sinceMs && !isRead(n)).length;
      return json({ count, seen_at: since, read: list.filter(isRead).map(n => n.id) });
    } catch (err) {
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
    }
  }

  // ── /backfill-username ────────────────────────────────────────────────────────

  if (url.pathname === "/backfill-username") {
    try {
      // Old cached pages still call this. Every post and chirp has a username now, so there's nothing to do.
      return json({ success: true });
    } catch (err) {
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
        return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
      return json({ error: err.message }, 500);
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
