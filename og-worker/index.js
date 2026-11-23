// perchposts-og: link-preview data for shared post links (iMessage, WhatsApp, Discord...).
//   GET /meta/<postId>      -> { title, description, site } for the page's og: tags (public posts only)
//   GET /img/<postId>.png   -> 1200x630 card in the site's style (tags, photo, wordmark)
// Huddles, deleted and archived posts get 404, so a shared link never reveals private content.
import { ImageResponse, GoogleFont, cache } from "@cf-wasm/og/workerd";
import FLAGS from "./flags.json";
import ICONS from "./icons.json";

// Tag pills match the site: our line icons (icons.json, from the site's _ppIco) in each tag's colour
const BOARDS = {
  general: ["General", "#60a5fa"], sports: ["Sports", "#facc15"], "science-nature": ["Science", "#2dd4bf"], nature: ["Nature", "#4ade80"],
  entertainment: ["Entertainment", "#fb7185"], random: ["Random", "#c084fc"], announcements: ["Announcements", "#f472b6"], cage: ["The Cage", "#f43f5e"],
  botnews: ["Perch News", "#c084fc"], activity: ["Flock", "#22d3ee"],
};
const boardIcon = (key, color) => ICONS[key] ? "data:image/svg+xml;base64," + btoa(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">${ICONS[key]}</svg>`) : null;
const SHORT = { "United States": "USA", "United Kingdom": "UK", "United Arab Emirates": "UAE" };
const IMG_VER = "25"; // bump to redraw every cached card
const MEDIA_RE = /^https:\/\/daboysforumip\.coldbrainarchive\.workers\.dev\/media\/[A-Za-z0-9][A-Za-z0-9._-]*$/;

function parse(content) {
  const c = content || "";
  let text = c, link = null, media = null;
  const ai = c.indexOf("[ATTACHMENTS:");
  if (ai !== -1) { text = c.slice(0, ai); try { media = JSON.parse(c.slice(ai + 13, c.lastIndexOf("]"))); } catch {} }
  else {
    const li = c.indexOf("[ATTACH:");
    if (li !== -1) { text = c.slice(0, li); try { link = JSON.parse(c.slice(li + 8, c.lastIndexOf("]"))); } catch {} }
  }
  return { text: text.trim(), link, media };
}

const clip = (s, n) => { s = (s || "").replace(/\s+/g, " ").trim(); return s.length > n ? s.slice(0, n - 1).trimEnd() + "…" : s; };

async function getPost(env, id) {
  if (!/^[A-Za-z0-9-]{1,64}$/.test(id)) return null;
  const p = await env.DB.prepare(
    "SELECT id, title, content, board, country, utag, board_auto, is_huddle, deleted, archived FROM posts WHERE id = ?"
  ).bind(id).first();
  if (!p || p.deleted || p.archived || p.is_huddle) return null;
  let { text, link, media } = parse(p.content);
  // A single photo/video is stored like a link ({type:"image"|"video", url, poster}); treat it as media, not a website
  if (link && (link.type === "image" || link.type === "video")) { media = [link]; link = null; }
  const title = clip(p.title || link?.title || text || "A post on perchposts", 140);
  const description = clip(link?.description || (p.title ? text : "") || "", 200);
  let site = "";
  if (link?.url) { try { site = new URL(link.url).hostname.replace(/^www\./, ""); } catch {} }
  let image = link?.image || "";
  let video = false;
  if (!image && Array.isArray(media)) {
    for (const a of media) {
      if (!a) continue;
      const still = a.type === "video" ? a.poster : (a.thumb || a.url);
      if (still && MEDIA_RE.test(still)) { image = still + "?thumb=1"; video = a.type === "video"; break; }
      if (still && /^https:\/\//.test(still)) { image = still; video = a.type === "video"; break; }
    }
  }
  return { id: p.id, title, description, site, image, video, ref: link?.url ? new URL(link.url).origin + "/" : "", board: p.board_auto ? null : p.board, country: p.country, utag: p.utag || null };
}

// Fetch the post's photo ourselves so a slow or blocked image site can't break the card; only JPEG/PNG are drawn.
// Some news image servers (CBC's Akamai Image Manager) send AVIF/WebP whatever we ask for; `imformat=jpeg` gets a JPEG.
const UA = "perchposts-preview/1.0 (+https://perchposts.com) facebookexternalhit/1.1";
const BROWSER = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1";
async function grab(url, ua = UA, ref = "") {
  try {
    const r = await fetch(url, {
      headers: ua === UA ? { Accept: "image/jpeg,image/png;q=0.9,*/*;q=0.5", "User-Agent": ua }
        : { Accept: "image/avif,image/webp,image/png,image/jpeg,*/*;q=0.8", "Accept-Language": "en;q=0.9", "User-Agent": ua, ...(ref ? { Referer: ref } : {}) },
      signal: AbortSignal.timeout(5000), cf: { cacheTtl: 86400 },
    });
    const type = (r.headers.get("content-type") || "").split(";")[0].trim();
    if (!r.ok) return { fail: true };
    if (!/^image\/(jpeg|png)$/.test(type)) { r.body?.cancel(); return { wrong: true }; }
    const buf = await r.arrayBuffer();
    if (buf.byteLength > 6_000_000) return { fail: true };
    let bin = ""; const u = new Uint8Array(buf);
    for (let i = 0; i < u.length; i += 0x8000) bin += String.fromCharCode(...u.subarray(i, i + 0x8000));
    return { data: `data:${type};base64,${btoa(bin)}` };
  } catch { return { fail: true }; }
}
function sized(url) {
  if (/[?&]im=/.test(url) && !/Resize/i.test(url)) return url.replace(/([?&]im=[^&]*)/, (m) => m + (/%3B$/i.test(m) ? "" : "%3B") + "Resize%3D1200");
  return url;
}
async function photo(url, ref = "") {
  if (!/^https:\/\//.test(url || "")) return null;
  // Akamai Image Manager URLs with no resize step serve the full original (can be 5000px+): ask for 1200 wide
  const u = sized(url);
  // Our honest name first; some image servers refuse unknown clients, so then a browser identity (as link-preview.js does)
  let ua = UA, g = await grab(u, ua);
  if (g.fail) { ua = BROWSER; g = await grab(u, ua, ref); }
  if (g.wrong) g = await grab(u + (u.includes("?") ? "&" : "?") + "imformat=jpeg", ua, ref);
  return g.data || null;
}

const h = (type, style, children) => ({ type, props: { style, children } });
// Bird-globe logo (brand/bird-globe.svg). The old plain globe is brand/old-globe-favicon.svg.
const GLOBE = "data:image/svg+xml;base64," + btoa(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="15 9 82 82"><defs><clipPath id="cf"><circle cx="56" cy="50" r="38"/></clipPath></defs><circle cx="56" cy="50" r="38" fill="#14151b"/><g fill="none" stroke="#c084fc" stroke-width="3.2" clip-path="url(#cf)"><line x1="18" y1="50" x2="94" y2="50"/><path d="M 16 30 Q 56 37 96 30"/><path d="M 16 70 Q 56 63 96 70"/><path d="M 56 12 A 9.84 38 0 0 1 56 88"/><path d="M 56 12 A 9.84 38 0 0 0 56 88"/><path d="M 56 12 A 26.87 38 0 0 1 56 88"/><path d="M 56 12 A 26.87 38 0 0 0 56 88"/></g><g clip-path="url(#cf)"></g><circle cx="56" cy="50" r="38" fill="none" stroke="#c084fc" stroke-width="4.6"/></svg>`);

function pill(text, color, emoji, icon) {
  return h("div", {
    display: "flex", alignItems: "center", gap: 10, height: 50, padding: "0 20px", borderRadius: 999,
    border: `3px solid ${color}`, color, fontSize: 24, fontWeight: 800, letterSpacing: 1.5, textTransform: "uppercase",
  }, [icon ? { type: "img", props: { src: icon, width: 26, height: 26 } } : emoji ? h("span", { display: "flex" }, emoji) : null, h("span", { display: "flex" }, text)].filter(Boolean));
}

function card(post, img) {
  const bk = BOARDS[post.board] ? post.board : Object.keys(BOARDS).find(k => BOARDS[k][0].toLowerCase() === String(post.board || "").toLowerCase());
  const b = bk && BOARDS[bk];
  const pills = [];
  if (b) pills.push(pill(b[0], b[1], null, boardIcon(bk, b[1])));
  if (post.country) pills.push(pill(SHORT[post.country] || post.country, "#e2e8f0", FLAGS[post.country] || null));
  // the bird's own #tag: grey like the site's pill, with the # line icon
  if (post.utag) pills.push(pill(post.utag, "#e2e8f0", null, "data:image/svg+xml;base64," + btoa(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#e2e8f0" stroke-width="2.4" stroke-linecap="round"><path d="M5 9h15M4 15h15M10 3.5 8 20.5M16 3.5l-2 17"/></svg>`)));
  const top = h("div", { display: "flex", alignItems: "center", justifyContent: "space-between", width: "100%" }, [
    h("div", { display: "flex", gap: 14 }, pills.length ? pills : [h("span", { display: "flex" }, "")]),
    h("div", { display: "flex", alignItems: "center", gap: 14 }, [
      { type: "img", props: { src: GLOBE, width: 50, height: 50 } },
      h("span", { display: "flex", color: "#c084fc", fontSize: 40, fontWeight: 800, letterSpacing: -1 }, "perchposts"),
    ]),
  ]);
  let body;
  if (img) {
    const play = post.video ? h("div", {
      position: "absolute", left: 0, top: 0, right: 0, bottom: 0, display: "flex", alignItems: "center", justifyContent: "center",
    }, [h("div", {
      display: "flex", alignItems: "center", justifyContent: "center", width: 112, height: 112, borderRadius: 999,
      background: "rgba(11,12,16,.62)", border: "3px solid rgba(255,255,255,.85)",
    }, [{ type: "svg", props: { width: 44, height: 44, viewBox: "0 0 24 24", children: [{ type: "path", props: { d: "M7 4.5v15l13-7.5z", fill: "#ffffff" } }] } }])]) : null;
    body = h("div", { display: "flex", position: "relative", flex: 1, width: "100%", marginTop: 30, borderRadius: 28, overflow: "hidden" }, [
      { type: "img", props: { src: img, style: { width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 25%" } } },
      play,
    ].filter(Boolean));
  } else {
    body = h("div", { display: "flex", flexDirection: "column", justifyContent: "center", flex: 1, width: "100%", marginTop: 20 }, [
      h("div", { display: "flex", color: "#f8fafc", fontSize: post.title.length > 90 ? 52 : 64, fontWeight: 800, lineHeight: 1.15, letterSpacing: -1 }, post.title),
      post.site ? h("div", { display: "flex", marginTop: 28, color: "#c084fc", fontSize: 28, fontWeight: 800, letterSpacing: 2, textTransform: "uppercase" }, post.site + " ↗") : null,
    ].filter(Boolean));
  }
  return h("div", {
    display: "flex", flexDirection: "column", width: "100%", height: "100%", padding: "40px 44px 44px",
    background: "#0b0c10", fontFamily: "Inter",
  }, [top, body]);
}

// Draws the card once and keeps it a day. Metadata says whether the post's photo made it in.
async function renderCard(env, ctx, post) {
  const key = `card:${post.id}:${IMG_VER}`;
  const hit = await env.CARDS.getWithMetadata(key, "arrayBuffer");
  if (hit.value) return { png: hit.value, photo: !!hit.metadata?.photo };
  const img = await photo(post.image, post.ref);
  const res = await ImageResponse.async(card(post, img), {
    width: 1200, height: 630, emoji: "twemoji",
    fonts: [new GoogleFont("Inter", { weight: 800 })],
  });
  const png = await res.arrayBuffer();
  ctx.waitUntil(env.CARDS.put(key, png, { expirationTtl: 86400, metadata: { photo: !!img } }));
  return { png, photo: !!img };
}

export default {
  async fetch(request, env, ctx) {
    cache.setExecutionContext(ctx);
    const url = new URL(request.url);
    if (request.method !== "GET" && request.method !== "HEAD") return new Response("Method not allowed", { status: 405 });
    let m;
    const path = url.pathname.replace(/^\/og(?=\/)/, "");
    if ((m = path.match(/^\/meta\/([^/]+)$/))) {
      const post = await getPost(env, m[1]);
      if (!post) return Response.json({ error: "not_found" }, { status: 404 });
      const img = `${url.origin}/img/${post.id}.png?v=${IMG_VER}`;
      return Response.json({ title: post.title, description: post.description, site: post.site, img },
        { headers: { "Cache-Control": "no-store" } });
    }
    if ((m = path.match(/^\/img\/([^/]+)\.png$/))) {
      // Checked on every request, cached or not, so a card stops showing as soon as its post is deleted
      const post = await getPost(env, m[1]);
      if (!post) return new Response("Not found", { status: 404 });
      const { png } = await renderCard(env, ctx, post);
      return new Response(png, { headers: { "Content-Type": "image/png", "Cache-Control": "public, max-age=86400" } });
    }
    return new Response("Not found", { status: 404 });
  },
};
