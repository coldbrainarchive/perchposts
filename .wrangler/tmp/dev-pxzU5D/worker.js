var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// .wrangler/tmp/bundle-QFQGBq/checked-fetch.js
var urls = /* @__PURE__ */ new Set();
function checkURL(request, init) {
  const url = request instanceof URL ? request : new URL(
    (typeof request === "string" ? new Request(request, init) : request).url
  );
  if (url.port && url.port !== "443" && url.protocol === "https:") {
    if (!urls.has(url.toString())) {
      urls.add(url.toString());
      console.warn(
        `WARNING: known issue with \`fetch()\` requests to custom HTTPS ports in published Workers:
 - ${url.toString()} - the custom port will be ignored when the Worker is published using the \`wrangler deploy\` command.
`
      );
    }
  }
}
__name(checkURL, "checkURL");
globalThis.fetch = new Proxy(globalThis.fetch, {
  apply(target, thisArg, argArray) {
    const [request, init] = argArray;
    checkURL(request, init);
    return Reflect.apply(target, thisArg, argArray);
  }
});

// media-strip.js
function stripMedia(bytes, contentType = "") {
  try {
    const t = String(contentType).toLowerCase();
    if (t === "image/jpeg" || isJpeg(bytes)) return stripJpeg(bytes);
    if (t === "image/png" || isPng(bytes)) return stripPng(bytes);
    if (t === "image/webp" || isWebp(bytes)) return stripWebp(bytes);
    if (t.startsWith("video/") || isIsoBmff(bytes)) return stripIsoBmff(bytes);
  } catch (e) {
  }
  return { bytes, changed: false };
}
__name(stripMedia, "stripMedia");
var isJpeg = /* @__PURE__ */ __name((b) => b.length > 3 && b[0] === 255 && b[1] === 216, "isJpeg");
var isPng = /* @__PURE__ */ __name((b) => b.length > 8 && b[0] === 137 && b[1] === 80 && b[2] === 78 && b[3] === 71, "isPng");
var isWebp = /* @__PURE__ */ __name((b) => b.length > 12 && str(b, 0, 4) === "RIFF" && str(b, 8, 4) === "WEBP", "isWebp");
var isIsoBmff = /* @__PURE__ */ __name((b) => b.length > 12 && ["ftyp", "moov", "mdat", "wide", "free"].includes(str(b, 4, 4)), "isIsoBmff");
var str = /* @__PURE__ */ __name((b, o, n) => String.fromCharCode(...b.subarray(o, o + n)), "str");
function stripJpeg(b) {
  const keep = [b.subarray(0, 2)];
  let i = 2, changed = false, orientation = 1;
  while (i + 4 <= b.length) {
    if (b[i] !== 255) return { bytes: b, changed: false };
    const m = b[i + 1];
    if (m === 255) {
      i++;
      continue;
    }
    if (m === 216 || m === 1 || m >= 208 && m <= 215) {
      keep.push(b.subarray(i, i + 2));
      i += 2;
      continue;
    }
    if (m === 218 || m === 217) {
      keep.push(b.subarray(i));
      i = b.length;
      break;
    }
    const len = b[i + 2] << 8 | b[i + 3];
    const seg = b.subarray(i, i + 2 + len);
    const isApp = m >= 224 && m <= 239;
    let drop = false;
    if (m === 254) drop = true;
    else if (isApp && m !== 224 && m !== 238) {
      if (m === 226 && str(seg, 4, 11) === "ICC_PROFILE") drop = false;
      else {
        if (m === 225 && str(seg, 4, 4) === "Exif") orientation = readOrientation(seg.subarray(10)) || orientation;
        drop = true;
      }
    }
    if (drop) changed = true;
    else keep.push(seg);
    i += 2 + len;
  }
  if (!changed) return { bytes: b, changed: false };
  if (orientation >= 2 && orientation <= 8) keep.splice(keep[1] && keep[1][1] === 224 ? 2 : 1, 0, orientationExif(orientation));
  return { bytes: concat(keep), changed: true };
}
__name(stripJpeg, "stripJpeg");
function readOrientation(t) {
  if (t.length < 8) return 0;
  const le = t[0] === 73;
  const u16 = /* @__PURE__ */ __name((o) => le ? t[o] | t[o + 1] << 8 : t[o] << 8 | t[o + 1], "u16");
  const u32 = /* @__PURE__ */ __name((o) => le ? (t[o] | t[o + 1] << 8 | t[o + 2] << 16 | t[o + 3] << 24) >>> 0 : (t[o] << 24 | t[o + 1] << 16 | t[o + 2] << 8 | t[o + 3]) >>> 0, "u32");
  const ifd = u32(4);
  if (ifd + 2 > t.length) return 0;
  const n = u16(ifd);
  for (let k = 0; k < n; k++) {
    const e = ifd + 2 + k * 12;
    if (e + 12 > t.length) break;
    if (u16(e) === 274) return u16(e + 8);
  }
  return 0;
}
__name(readOrientation, "readOrientation");
function orientationExif(o) {
  const tiff = [73, 73, 42, 0, 8, 0, 0, 0, 1, 0, 18, 1, 3, 0, 1, 0, 0, 0, o, 0, 0, 0, 0, 0, 0, 0];
  const body = [69, 120, 105, 102, 0, 0, ...tiff];
  const len = body.length + 2;
  return new Uint8Array([255, 225, len >> 8, len & 255, ...body]);
}
__name(orientationExif, "orientationExif");
var PNG_KEEP = /* @__PURE__ */ new Set(["IHDR", "PLTE", "IDAT", "IEND", "tRNS", "gAMA", "cHRM", "sRGB", "iCCP", "sBIT", "pHYs", "acTL", "fcTL", "fdAT"]);
function stripPng(b) {
  const keep = [b.subarray(0, 8)];
  let i = 8, changed = false;
  while (i + 12 <= b.length) {
    const len = (b[i] << 24 | b[i + 1] << 16 | b[i + 2] << 8 | b[i + 3]) >>> 0;
    const type = str(b, i + 4, 4);
    const end = i + 12 + len;
    if (end > b.length) return { bytes: b, changed: false };
    if (PNG_KEEP.has(type)) keep.push(b.subarray(i, end));
    else changed = true;
    i = end;
    if (type === "IEND") break;
  }
  return changed ? { bytes: concat(keep), changed: true } : { bytes: b, changed: false };
}
__name(stripPng, "stripPng");
function stripWebp(b) {
  const keep = [];
  let i = 12, changed = false;
  while (i + 8 <= b.length) {
    const type = str(b, i, 4);
    const len = (b[i + 4] | b[i + 5] << 8 | b[i + 6] << 16 | b[i + 7] << 24) >>> 0;
    const end = i + 8 + len + (len & 1);
    if (end > b.length + 1) return { bytes: b, changed: false };
    if (type === "EXIF" || type === "XMP ") changed = true;
    else {
      const c = b.slice(i, Math.min(end, b.length));
      if (type === "VP8X") c[8] &= ~(8 | 4);
      keep.push(c);
    }
    i = end;
  }
  if (!changed) return { bytes: b, changed: false };
  const body = concat(keep);
  const out = new Uint8Array(12 + body.length);
  out.set(b.subarray(0, 12));
  const size = 4 + body.length;
  out[4] = size & 255;
  out[5] = size >> 8 & 255;
  out[6] = size >> 16 & 255;
  out[7] = size >>> 24 & 255;
  out.set(body, 12);
  return { bytes: out, changed: true };
}
__name(stripWebp, "stripWebp");
var CONTAINERS = /* @__PURE__ */ new Set(["moov", "trak", "mdia", "minf", "edts"]);
var WIPE = /* @__PURE__ */ new Set(["udta", "meta", "uuid"]);
function stripIsoBmff(b) {
  let changed = false;
  const dv = new DataView(b.buffer, b.byteOffset, b.byteLength);
  const walk = /* @__PURE__ */ __name((start, end, depth, inMoov) => {
    let i = start;
    while (i + 8 <= end) {
      let size = dv.getUint32(i), hdr = 8;
      const type = str(b, i + 4, 4);
      if (size === 1) {
        if (i + 16 > end) return;
        size = Number(dv.getBigUint64(i + 8));
        hdr = 16;
      } else if (size === 0) size = end - i;
      if (size < hdr || i + size > end) return;
      if (inMoov && WIPE.has(type)) {
        b[i + 4] = 102;
        b[i + 5] = 114;
        b[i + 6] = 101;
        b[i + 7] = 101;
        b.fill(0, i + hdr, i + size);
        changed = true;
      } else if (CONTAINERS.has(type) && depth < 6) {
        walk(i + hdr, i + size, depth + 1, inMoov || type === "moov");
      } else if (depth === 0 && (type === "udta" || type === "meta")) {
        b[i + 4] = 102;
        b[i + 5] = 114;
        b[i + 6] = 101;
        b[i + 7] = 101;
        b.fill(0, i + hdr, i + size);
        changed = true;
      }
      i += size;
    }
  }, "walk");
  walk(0, b.length, 0, false);
  return { bytes: b, changed };
}
__name(stripIsoBmff, "stripIsoBmff");
function stripIsoBmffStream() {
  const HOLD = /* @__PURE__ */ new Set(["moov", "udta", "meta"]), MAX_HOLD = 64 * 1024 * 1024;
  let hdr = new Uint8Array(0), mode = "header", left = 0, held = null, heldLen = 0, heldNeed = 0;
  const join = /* @__PURE__ */ __name((a, b) => {
    const o = new Uint8Array(a.length + b.length);
    o.set(a);
    o.set(b, a.length);
    return o;
  }, "join");
  return new TransformStream({
    transform(chunk, ctl) {
      let c = chunk instanceof Uint8Array ? chunk : new Uint8Array(chunk);
      while (c.length) {
        if (mode === "rest") {
          ctl.enqueue(c);
          return;
        }
        if (mode === "pass") {
          const n2 = Math.min(left, c.length);
          ctl.enqueue(c.subarray(0, n2));
          left -= n2;
          c = c.subarray(n2);
          if (!left) mode = "header";
          continue;
        }
        if (mode === "hold") {
          const n2 = Math.min(heldNeed - heldLen, c.length);
          held.set(c.subarray(0, n2), heldLen);
          heldLen += n2;
          c = c.subarray(n2);
          if (heldLen === heldNeed) {
            ctl.enqueue(stripIsoBmff(held).bytes);
            held = null;
            mode = "header";
          }
          continue;
        }
        const want = hdr.length >= 8 && new DataView(hdr.buffer, hdr.byteOffset).getUint32(0) === 1 ? 16 : 8;
        const n = Math.min(want - hdr.length, c.length);
        hdr = join(hdr, c.subarray(0, n));
        c = c.subarray(n);
        if (hdr.length < want) continue;
        if (want === 8 && new DataView(hdr.buffer, hdr.byteOffset).getUint32(0) === 1) continue;
        const dv = new DataView(hdr.buffer, hdr.byteOffset);
        let size = dv.getUint32(0);
        if (size === 1) size = Number(dv.getBigUint64(8));
        const type = str(hdr, 4, 4), h = hdr;
        hdr = new Uint8Array(0);
        if (size === 0 || size < h.length) {
          ctl.enqueue(h);
          mode = "rest";
          continue;
        }
        if (HOLD.has(type) && size <= MAX_HOLD) {
          held = new Uint8Array(size);
          held.set(h);
          heldLen = h.length;
          heldNeed = size;
          mode = "hold";
          continue;
        }
        ctl.enqueue(h);
        left = size - h.length;
        mode = left ? "pass" : "header";
      }
    },
    flush(ctl) {
      if (hdr.length) ctl.enqueue(hdr);
      if (held) ctl.enqueue(held.subarray(0, heldLen));
    }
  });
}
__name(stripIsoBmffStream, "stripIsoBmffStream");
function concat(parts) {
  const n = parts.reduce((s, p) => s + p.length, 0), out = new Uint8Array(n);
  let o = 0;
  for (const p of parts) {
    out.set(p, o);
    o += p.length;
  }
  return out;
}
__name(concat, "concat");

// link-preview.js
var BOT_UA = "Mozilla/5.0 (compatible; PerchpostsBot/1.0; +https://perchposts.com) facebookexternalhit/1.1";
var BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15";
var MAX_BYTES = 15e5;
var TIMEOUT_MS = 6e3;
var MAX_REDIRECTS = 5;
async function linkPreview(raw, fetchImpl = fetch, opts = {}) {
  const addressFallback = opts.addressFallback !== false;
  const timeout = opts.timeoutMs || TIMEOUT_MS;
  let u = normalize(raw);
  if (!u) return null;
  try {
    const special = await viaOEmbed(u, fetchImpl, timeout);
    if (special) return special;
  } catch (e) {
  }
  if (/(^|\.)bbc\.(co\.uk|com)$/.test(u.hostname)) {
    return await bbcFromFeeds(u, fetchImpl).catch(() => null) || (addressFallback ? fromAddress(u) : null);
  }
  const score = /* @__PURE__ */ __name((p) => p ? (p.title && !generic(p) ? 2 : p.title ? 1 : 0) + (p.description ? 1 : 0) + (p.image ? 2 : 0) : -1, "score");
  const results = await new Promise((resolve) => {
    const got = [null, null];
    let left = 2;
    [BOT_UA, BROWSER_UA].forEach((ua, i) => fromPage(u, ua, fetchImpl, timeout).catch(() => null).then((p) => {
      got[i] = p;
      left--;
      if (score(p) >= 5 || !left) resolve(got.slice());
    }));
  });
  const [a, b] = results;
  let best = score(b) > score(a) ? mergePreview(b, a) : mergePreview(a, b);
  if (!best || !best.title) {
    if (/(^|\.)bbc\.(co\.uk|com)$/.test(u.hostname)) {
      const f = await bbcFromFeeds(u, fetchImpl).catch(() => null);
      if (f) return f;
    }
    const s = addressFallback ? fromAddress(u) : null;
    if (s) return s;
  }
  if (best && /(^|\.)tiktok\.com$/.test(u.hostname) && generic(best)) {
    const who = /^\/@([^/]+)/.exec(u.pathname);
    best = { ...best, title: who ? `@${who[1]} on TikTok` : "TikTok video", description: "TikTok" };
  }
  return best && (best.title || best.image) ? best : null;
}
__name(linkPreview, "linkPreview");
function normalize(raw) {
  let s = String(raw || "").trim();
  if (!s) return null;
  if (!/^https?:\/\//i.test(s)) s = "https://" + s;
  let u;
  try {
    u = new URL(s);
  } catch {
    return null;
  }
  if (!safeUrl(u)) return null;
  u.hash = "";
  return u;
}
__name(normalize, "normalize");
function safeUrl(u) {
  if (u.protocol !== "https:" && u.protocol !== "http:") return false;
  if (u.username || u.password) return false;
  if (u.port && u.port !== "80" && u.port !== "443") return false;
  const h = u.hostname.toLowerCase().replace(/\.$/, "");
  if (!h.includes(".") || h === "localhost" || /\.(local|internal|localhost|lan|home|arpa)$/.test(h)) return false;
  if (/(^|\.)workers\.dev$/.test(h) && h.startsWith("daboysforumip")) return false;
  if (/^\d+\.\d+\.\d+\.\d+$/.test(h)) {
    const [a, b] = h.split(".").map(Number);
    if (a === 10 || a === 127 || a === 0 || a === 169 && b === 254 || a === 172 && b >= 16 && b <= 31 || a === 192 && b === 168 || a === 100 && b >= 64 && b <= 127 || a >= 224) return false;
  }
  if (h.includes(":") || h.startsWith("[")) return false;
  return true;
}
__name(safeUrl, "safeUrl");
async function viaOEmbed(u, fetchImpl, timeout = TIMEOUT_MS) {
  const h = u.hostname.replace(/^www\.|^m\./, "");
  const getJson = /* @__PURE__ */ __name(async (endpoint) => {
    const r = await fetchImpl(endpoint, { headers: { "User-Agent": BOT_UA, Accept: "application/json" }, signal: AbortSignal.timeout(timeout) });
    return r.ok ? r.json() : null;
  }, "getJson");
  if (h === "youtube.com" || h === "youtu.be" || h === "music.youtube.com") {
    const id = youtubeId(u);
    if (!id) return null;
    const j = await getJson(`https://www.youtube.com/oembed?format=json&url=${encodeURIComponent(`https://www.youtube.com/watch?v=${id}`)}`);
    if (!j?.title) return null;
    return { url: `https://www.youtube.com/watch?v=${id}`, title: j.title, description: j.author_name ? `${j.author_name} \xB7 YouTube` : "YouTube", image: `https://i.ytimg.com/vi/${id}/hqdefault.jpg` };
  }
  if (h === "x.com" || h === "twitter.com" || h === "mobile.twitter.com" || h === "fxtwitter.com" || h === "vxtwitter.com") {
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
    return { url: u.href, title: j.title || (j.author_name ? `${j.author_name} on TikTok` : "TikTok"), description: j.author_name ? `${j.author_name} \xB7 TikTok` : "TikTok", image: j.thumbnail_url || null };
  }
  if (h === "open.spotify.com") {
    const j = await getJson(`https://open.spotify.com/oembed?url=${encodeURIComponent(u.href)}`);
    if (!j?.title) return null;
    return { url: u.href, title: j.title, description: "Spotify", image: j.thumbnail_url || null };
  }
  return null;
}
__name(viaOEmbed, "viaOEmbed");
function youtubeId(u) {
  const h = u.hostname.replace(/^www\.|^m\./, "");
  if (h === "youtu.be") return u.pathname.slice(1).split("/")[0] || null;
  if (u.searchParams.get("v")) return u.searchParams.get("v");
  const m = /^\/(shorts|embed|live|v)\/([A-Za-z0-9_-]{6,})/.exec(u.pathname);
  return m ? m[2] : null;
}
__name(youtubeId, "youtubeId");
async function fromPage(start, ua, fetchImpl, timeout = TIMEOUT_MS) {
  let u = start, res;
  for (let hop = 0; hop <= MAX_REDIRECTS; hop++) {
    res = await fetchImpl(u.href, {
      redirect: "manual",
      headers: { "User-Agent": ua, Accept: "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5", "Accept-Language": "en-IE,en;q=0.9" },
      signal: AbortSignal.timeout(timeout)
    });
    if (res.status >= 300 && res.status < 400 && res.headers.get("location")) {
      const next = new URL(res.headers.get("location"), u);
      if (!safeUrl(next)) return null;
      try {
        res.body?.cancel();
      } catch {
      }
      u = next;
      continue;
    }
    break;
  }
  if (!res || !res.ok) {
    try {
      res?.body?.cancel();
    } catch {
    }
    return null;
  }
  const type = (res.headers.get("content-type") || "").toLowerCase();
  if (type.startsWith("image/")) {
    try {
      res.body?.cancel();
    } catch {
    }
    return { url: u.href, title: null, description: null, image: u.href };
  }
  if (!type.includes("html")) {
    try {
      res.body?.cancel();
    } catch {
    }
    return null;
  }
  const html = await readHead(res);
  return parse(html, u);
}
__name(fromPage, "fromPage");
async function readHead(res) {
  const reader = res.body.getReader(), dec = new TextDecoder();
  let html = "", n = 0;
  for (; ; ) {
    const { done, value } = await reader.read();
    if (done) break;
    n += value.length;
    html += dec.decode(value, { stream: true });
    if (/<\/head\s*>/i.test(html) || n > MAX_BYTES) {
      try {
        await reader.cancel();
      } catch {
      }
      break;
    }
  }
  return html;
}
__name(readHead, "readHead");
function parse(html, base) {
  const metas = {};
  for (const tag of html.match(/<meta\b[^>]*>/gi) || []) {
    const attr = /* @__PURE__ */ __name((name) => {
      const m = new RegExp(`\\b${name}\\s*=\\s*("([^"]*)"|'([^']*)'|([^\\s"'>]+))`, "i").exec(tag);
      return m ? m[2] ?? m[3] ?? m[4] ?? "" : null;
    }, "attr");
    const key = (attr("property") || attr("name") || attr("itemprop") || "").toLowerCase().trim();
    const val = attr("content");
    if (key && val != null && !(key in metas)) metas[key] = decode(val).trim();
  }
  const pick = /* @__PURE__ */ __name((...ks) => {
    for (const k of ks) if (metas[k]) return metas[k];
    return null;
  }, "pick");
  const titleTag = (() => {
    const m = /<title[^>]*>([\s\S]*?)<\/title>/i.exec(html);
    return m ? decode(m[1]).replace(/\s+/g, " ").trim() : null;
  })();
  const title = pick("og:title", "twitter:title", "title") || titleTag || null;
  const description = pick("og:description", "twitter:description", "description") || null;
  let image = pick("og:image:secure_url", "og:image", "og:image:url", "twitter:image", "twitter:image:src", "image", "thumbnailurl");
  if (!image) {
    const m = /<link\b[^>]*rel=["']image_src["'][^>]*>/i.exec(html);
    const h = m && /href=["']([^"']+)["']/i.exec(m[0]);
    if (h) image = decode(h[1]);
  }
  let url = pick("og:url") || base.href;
  try {
    if (image) image = new URL(image, base).href;
  } catch {
    image = null;
  }
  try {
    url = new URL(url, base).href;
  } catch {
    url = base.href;
  }
  if (image && !/^https?:/i.test(image)) image = null;
  return { url, title: clip(title, 300), description: clip(description, 600), image };
}
__name(parse, "parse");
var BBC_FEEDS = [
  "news",
  "news/world",
  "news/uk",
  "news/england",
  "news/northern_ireland",
  "news/scotland",
  "news/wales",
  "news/business",
  "news/politics",
  "news/health",
  "news/education",
  "news/science_and_environment",
  "news/technology",
  "news/entertainment_and_arts",
  "news/world/europe",
  "news/world/us_and_canada",
  "sport",
  "sport/football"
].map((p) => `https://feeds.bbci.co.uk/${p}/rss.xml`);
var bbcCache = { at: 0, items: [] };
async function bbcFromFeeds(u, fetchImpl) {
  const id = (u.pathname.match(/([a-z0-9]{8,}|\d{6,})\/?$/i) || [])[1];
  if (!id) return null;
  if (Date.now() - bbcCache.at > 5 * 60 * 1e3) {
    const texts = await Promise.all(BBC_FEEDS.map((f) => fetchImpl(f, { headers: { "User-Agent": BOT_UA }, signal: AbortSignal.timeout(TIMEOUT_MS) }).then((r) => r.ok ? r.text() : "").catch(() => "")));
    const items = [];
    for (const xml of texts) for (const it of xml.match(/<item>[\s\S]*?<\/item>/g) || []) {
      const tag = /* @__PURE__ */ __name((n) => {
        const m = new RegExp(`<${n}[^>]*>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?</${n}>`).exec(it);
        return m ? decode(m[1]).trim() : null;
      }, "tag");
      const thumb = /<media:thumbnail[^>]*url="([^"]+)"/.exec(it);
      items.push({ link: tag("link") || "", title: tag("title"), description: tag("description"), image: thumb ? thumb[1].replace(/\/standard\/\d+\//, "/standard/976/").replace(/\/ace\/standard\/\d+\//, "/ace/standard/976/") : null });
    }
    if (items.length) bbcCache = { at: Date.now(), items };
  }
  const hit = bbcCache.items.find((i) => i.link.split("?")[0].replace(/\/$/, "").endsWith(id));
  return hit && hit.title ? { url: u.href, title: hit.title, description: hit.description, image: hit.image } : null;
}
__name(bbcFromFeeds, "bbcFromFeeds");
function fromAddress(u) {
  const segs = u.pathname.split("/").filter(Boolean).map((s) => decodeURIComponent(s).replace(/\.(html?|php|aspx?|ece)$/i, ""));
  const slug = segs.reverse().find((s) => /[a-z]-[a-z]/i.test(s) && (s.match(/[a-z]+/gi) || []).length >= 3 && !/^[0-9a-f-]{20,}$/i.test(s));
  if (!slug) return null;
  const words = slug.replace(/[-_+]+/g, " ").replace(/\b\d{5,}\b/g, "").replace(/\s+/g, " ").trim();
  if (words.length < 12) return null;
  const site = u.hostname.replace(/^www\./, "");
  return { url: u.href, title: words.charAt(0).toUpperCase() + words.slice(1), description: site, image: null };
}
__name(fromAddress, "fromAddress");
function generic(p) {
  return !p.title || /^(instagram|tiktok|reddit|amazon(\.com)?|x|twitter)$/i.test(p.title.trim()) || /^visit tiktok/i.test(p.title);
}
__name(generic, "generic");
function mergePreview(a, b) {
  if (!a) return b;
  if (!b) return a;
  return { url: a.url || b.url, title: a.title || b.title, description: a.description || b.description, image: a.image || b.image };
}
__name(mergePreview, "mergePreview");
var clip = /* @__PURE__ */ __name((s, n) => s && s.length > n ? s.slice(0, n - 1).trimEnd() + "\u2026" : s, "clip");
var NAMED = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", ndash: "\u2013", mdash: "\u2014", hellip: "\u2026", lsquo: "\u2018", rsquo: "\u2019", ldquo: "\u201C", rdquo: "\u201D", eacute: "\xE9", egrave: "\xE8", aacute: "\xE1", agrave: "\xE0", ouml: "\xF6", uuml: "\xFC", auml: "\xE4", ccedil: "\xE7", ntilde: "\xF1", oacute: "\xF3", iacute: "\xED", uacute: "\xFA", pound: "\xA3", euro: "\u20AC", copy: "\xA9", reg: "\xAE", trade: "\u2122", middot: "\xB7", bull: "\u2022" };
function decode(s) {
  return String(s).replace(/&#(\d+);/g, (_, d) => {
    try {
      return String.fromCodePoint(Number(d));
    } catch {
      return "";
    }
  }).replace(/&#x([0-9a-f]+);/gi, (_, h) => {
    try {
      return String.fromCodePoint(parseInt(h, 16));
    } catch {
      return "";
    }
  }).replace(/&([a-z]+);/gi, (m, n) => NAMED[n.toLowerCase()] ?? m);
}
__name(decode, "decode");

// worker.js
var worker_default = {
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
  }
};
var LOGIN_TRIES = 10;
var LOCK_MINUTES = 15;
var HUMAN_POSTS = `username NOT IN ('NewsBot','ScienceBot','NatureBot','SportsBot')`;
var INDEX_STATEMENTS = [
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
  `CREATE INDEX IF NOT EXISTS idx_comments_pinned      ON comments(post_id) WHERE pinned = 1`
];
var REQUIRED_INDEXES = [
  "idx_posts_feed_created",
  "idx_posts_feed_activity",
  "idx_posts_username",
  "idx_comments_username",
  "idx_posts_human_activity",
  "idx_bot_logs_status",
  "idx_posts_deleted_list",
  "idx_posts_archived_list",
  "idx_posts_huddles",
  "idx_comments_post_created",
  "idx_comments_pinned",
  "idx_posts_frozen_list"
];
var TRACKING_PARAMS = /^(utm_|at_|cmp|ns_|fbclid|gclid|ref$|ocid|traffic_source|smid|ito|sr_share|mc_)/i;
var REPEAT_TITLE_DAYS = 6;
function articleKey(link) {
  if (!link || link.includes("undefined")) return null;
  let u;
  try {
    u = new URL(link);
  } catch {
    return null;
  }
  const path = u.pathname.replace(/\/+$/, "");
  if (path.length < 12) return null;
  let host = u.hostname.toLowerCase().replace(/^www\./, "");
  if (host === "bbc.com") host = "bbc.co.uk";
  const query = [...u.searchParams].filter(([k]) => !TRACKING_PARAMS.test(k)).map(([k, v]) => `${k}=${v}`).sort().join("&");
  return `l:${host}${path}${query ? `?${query}` : ""}`;
}
__name(articleKey, "articleKey");
function headlineKey(title) {
  const t = String(title || "").toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
  return t.length >= 20 ? `t:${t}` : null;
}
__name(headlineKey, "headlineKey");
function botPostKeys(content) {
  const at = (content || "").indexOf("[ATTACH:");
  if (at < 0) return { link: null, title: null };
  try {
    const a = JSON.parse(content.slice(at + 8, content.lastIndexOf("]")));
    return { link: articleKey(a.url), title: headlineKey(a.title) };
  } catch {
    return { link: null, title: null };
  }
}
__name(botPostKeys, "botPostKeys");
async function claimBotPost(env, keys, now) {
  const claimed = [];
  try {
    if (keys.link) {
      const r = await env.DB.prepare(`INSERT OR IGNORE INTO bot_links (url, created_at) VALUES (?, ?)`).bind(keys.link, now).run();
      if (r.meta.changes === 0) return { duplicate: true, claimed };
      claimed.push(keys.link);
    }
    if (keys.title) {
      const cutoff = new Date(Date.now() - REPEAT_TITLE_DAYS * 864e5).toISOString();
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
__name(claimBotPost, "claimBotPost");
async function passesBotCheck(env, token, ip, action) {
  const hostnames = (env.TURNSTILE_HOSTNAMES || "").split(",").map((h) => h.trim()).filter(Boolean);
  if (typeof token !== "string" || !token || token.length > 2048 || !hostnames.length || !env.TURNSTILE_SECRET) return false;
  try {
    const form = new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: token });
    if (ip) form.set("remoteip", ip);
    const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form,
      signal: AbortSignal.timeout(1e4)
    });
    if (!res.ok) return false;
    const result = await res.json();
    return result.success === true && result.action === action && hostnames.includes(result.hostname);
  } catch (err) {
    console.error("passesBotCheck:", err.message);
    return false;
  }
}
__name(passesBotCheck, "passesBotCheck");
async function addHuddleInbox(env, rows, name) {
  if (!rows.length || !name) return rows;
  const me = name.toLowerCase(), ids = rows.map((p) => p.id);
  try {
    const { results: rd = [] } = await env.DB.prepare(
      `SELECT post_id, read_at FROM huddle_reads WHERE username = ? AND post_id IN (${ids.map(() => "?").join(",")})`
    ).bind(me, ...ids).all();
    const readAt = new Map(rd.map((r) => [r.post_id, r.read_at]));
    const first = await env.DB.batch(ids.flatMap((id) => [
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
      const last = first[2 * i].results?.[0] || null, fr = (fresh[i].results || []).sort((a, b) => a.t < b.t ? 1 : -1);
      p.hx = {
        unread: fr.reduce((a, r) => a + r.n, 0),
        fresh: fr.map((r) => r.username),
        nt: fr.length ? fr[0].t : null,
        // newest unread chirp, so a device that already read past it can clear the badge
        last: last ? { u: last.username, c: String(last.content || "").slice(0, 400), t: last.created_at } : null
      };
    });
  } catch (err) {
    console.error("huddle inbox unavailable:", err.message);
  }
  return rows;
}
__name(addHuddleInbox, "addHuddleInbox");
async function addCommentCounts(env, posts) {
  if (!posts.length) return posts;
  try {
    const { results } = await env.DB.prepare(
      `SELECT post_id, COUNT(*) AS n FROM comments WHERE post_id IN (${ID_LIST}) AND deleted = 0 AND (username IS NULL OR username != '__system__') GROUP BY post_id`
    ).bind(JSON.stringify(posts.map((p) => p.id))).all();
    const counts = Object.fromEntries((results || []).map((r) => [r.post_id, r.n]));
    return posts.map((p) => ({ ...p, comment_count: counts[p.id] || 0 }));
  } catch (err) {
    console.error("addCommentCounts:", err.message);
    return posts;
  }
}
__name(addCommentCounts, "addCommentCounts");
async function ensureIndexes(env, event) {
  try {
    const { results } = await env.DB.prepare(
      `SELECT name FROM sqlite_master WHERE type = 'index'`
    ).all();
    const have = new Set((results || []).map((r) => r.name));
    if (REQUIRED_INDEXES.every((n) => have.has(n)) && !have.has("idx_posts_deleted")) return;
    if (new Date(event.scheduledTime).getUTCHours() !== 0) {
      console.log("ensureIndexes: indexes missing, will build in the 00:05 UTC run");
      return;
    }
    await env.DB.batch(INDEX_STATEMENTS.map((s) => env.DB.prepare(s)));
    await env.DB.prepare(`PRAGMA optimize`).run();
    console.log("ensureIndexes: indexes applied");
  } catch (err) {
    console.error("ensureIndexes failed (will retry next hour):", err.message);
  }
}
__name(ensureIndexes, "ensureIndexes");
async function signJWT(payload, secret) {
  const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const body = btoa(JSON.stringify(payload));
  const data = `${header}.${body}`;
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(data));
  const sigB64 = btoa(String.fromCharCode(...new Uint8Array(sig))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
  return `${data}.${sigB64}`;
}
__name(signJWT, "signJWT");
async function verifyJWT(token, secret) {
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  try {
    const key = await crypto.subtle.importKey(
      "raw",
      new TextEncoder().encode(secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["verify"]
    );
    const pad = /* @__PURE__ */ __name((s) => s + "=".repeat((4 - s.length % 4) % 4), "pad");
    const sigBytes = Uint8Array.from(
      atob(pad(parts[2].replace(/-/g, "+").replace(/_/g, "/"))),
      (c) => c.charCodeAt(0)
    );
    const valid = await crypto.subtle.verify(
      "HMAC",
      key,
      sigBytes,
      new TextEncoder().encode(`${parts[0]}.${parts[1]}`)
    );
    if (!valid) return null;
    const payload = JSON.parse(atob(pad(parts[1])));
    if (payload.exp && payload.exp < Math.floor(Date.now() / 1e3)) return null;
    return payload;
  } catch {
    return null;
  }
}
__name(verifyJWT, "verifyJWT");
async function hashPassword(password) {
  const enc = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveBits"]);
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const bits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", hash: "SHA-256", salt, iterations: 1e5 },
    keyMaterial,
    256
  );
  const toHex = /* @__PURE__ */ __name((b) => Array.from(b).map((x) => x.toString(16).padStart(2, "0")).join(""), "toHex");
  return toHex(salt) + ":" + toHex(new Uint8Array(bits));
}
__name(hashPassword, "hashPassword");
async function verifyPassword(password, stored) {
  const [saltHex, hashHex] = stored.split(":");
  const salt = new Uint8Array(saltHex.match(/.{2}/g).map((b) => parseInt(b, 16)));
  const enc = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", hash: "SHA-256", salt, iterations: 1e5 },
    keyMaterial,
    256
  );
  const toHex = /* @__PURE__ */ __name((b) => Array.from(b).map((x) => x.toString(16).padStart(2, "0")).join(""), "toHex");
  return toHex(new Uint8Array(bits)) === hashHex;
}
__name(verifyPassword, "verifyPassword");
var POST_BOOL_FIELDS = ["is_mod", "is_admin", "moderator", "deleted", "archived", "frozen", "pinned", "pinned_global", "locked", "is_huddle"];
var COMMENT_BOOL_FIELDS = ["is_mod", "is_admin", "moderator", "deleted", "pinned"];
var EXTINCT_NAME = "Extinct Bird";
var RESERVED_NAMES = /* @__PURE__ */ new Set(["extinct bird", "__system__", "newsbot", "sciencebot", "naturebot", "sportsbot"]);
function boolify(row, fields) {
  if (!row) return row;
  const out = { ...row };
  for (const f of fields) if (f in out) out[f] = out[f] === 1 || out[f] === true;
  return out;
}
__name(boolify, "boolify");
var ID_LIST = `SELECT value FROM json_each(?)`;
var LIVE_POSTS = `deleted = 0 AND (archived = 0 OR archived IS NULL) AND (is_huddle = 0 OR is_huddle IS NULL)`;
var BOARD_NAMES = { general: "General", sports: "Sports", "science-nature": "Science", random: "Random", announcements: "Announcements", cage: "The Cage" };
var REGION_WINDOW = 4e3;
var REGION_COUNTRIES = {
  "Europe": [
    "Albania",
    "Andorra",
    "Austria",
    "Belarus",
    "Belgium",
    "Bosnia & Herzegovina",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Georgia",
    "Germany",
    "Greece",
    "Hungary",
    "Iceland",
    "Ireland",
    "Italy",
    "Kosovo",
    "Latvia",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Moldova",
    "Monaco",
    "Montenegro",
    "Netherlands",
    "North Macedonia",
    "Norway",
    "Poland",
    "Portugal",
    "Romania",
    "Russia",
    "Serbia",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
    "Switzerland",
    "Ukraine",
    "United Kingdom"
  ],
  "Africa": [
    "Algeria",
    "Angola",
    "Benin",
    "Botswana",
    "Burkina Faso",
    "Burundi",
    "Cameroon",
    "Chad",
    "Congo",
    "DR Congo",
    "Egypt",
    "Eritrea",
    "Eswatini",
    "Ethiopia",
    "Gabon",
    "Gambia",
    "Ghana",
    "Guinea",
    "Kenya",
    "Liberia",
    "Libya",
    "Madagascar",
    "Malawi",
    "Mali",
    "Mauritania",
    "Mauritius",
    "Morocco",
    "Mozambique",
    "Namibia",
    "Niger",
    "Nigeria",
    "Rwanda",
    "Senegal",
    "Sierra Leone",
    "Somalia",
    "South Africa",
    "South Sudan",
    "Sudan",
    "Tanzania",
    "Togo",
    "Tunisia",
    "Uganda",
    "Zambia",
    "Zimbabwe"
  ],
  "Asia": [
    "Afghanistan",
    "Armenia",
    "Azerbaijan",
    "Bangladesh",
    "Bhutan",
    "Brunei",
    "Cambodia",
    "China",
    "Hong Kong",
    "India",
    "Indonesia",
    "Japan",
    "Kazakhstan",
    "Kyrgyzstan",
    "Laos",
    "Malaysia",
    "Maldives",
    "Mongolia",
    "Myanmar",
    "Nepal",
    "North Korea",
    "Pakistan",
    "Philippines",
    "Singapore",
    "South Korea",
    "Sri Lanka",
    "Taiwan",
    "Tajikistan",
    "Thailand",
    "Turkmenistan",
    "Uzbekistan",
    "Vietnam"
  ],
  "North America": [
    "Bahamas",
    "Belize",
    "Canada",
    "Costa Rica",
    "Cuba",
    "Dominican Republic",
    "El Salvador",
    "Guatemala",
    "Haiti",
    "Honduras",
    "Jamaica",
    "Mexico",
    "Nicaragua",
    "Panama",
    "Trinidad & Tobago",
    "United States"
  ],
  "Middle East": [
    "Bahrain",
    "Iran",
    "Iraq",
    "Israel",
    "Jordan",
    "Kuwait",
    "Lebanon",
    "Oman",
    "Palestine",
    "Qatar",
    "Saudi Arabia",
    "Syria",
    "Turkey",
    "United Arab Emirates",
    "Yemen"
  ],
  "South America": [
    "Argentina",
    "Bolivia",
    "Brazil",
    "Chile",
    "Colombia",
    "Ecuador",
    "Paraguay",
    "Peru",
    "Uruguay",
    "Venezuela"
  ],
  "Australia/Oceania": [
    "Australia",
    "Fiji",
    "New Zealand",
    "Papua New Guinea"
  ]
};
var COUNTRY_REGION = Object.fromEntries(
  Object.entries(REGION_COUNTRIES).flatMap(([region, list]) => list.map((c) => [c, region]))
);
var regionOf = /* @__PURE__ */ __name((p) => p.continent || COUNTRY_REGION[p.country] || null, "regionOf");
var REGION_WORDS = {
  "Africa": ["Africa"],
  "Europe": ["Europe"],
  "Asia": ["Asia"],
  "Middle East": ["Middle East"],
  "North America": ["North America"],
  "South America": ["South America", "Latin America"],
  "Australia/Oceania": ["Oceania"]
};
var NAME_SKIP = /* @__PURE__ */ new Set(["Georgia", "Jordan", "Chad", "Turkey"]);
var NAME_AS = { "Bosnia & Herzegovina": ["Bosnia"], "Trinidad & Tobago": ["Trinidad"], "Turkey": ["T\xFCrkiye"] };
var namePiece = /* @__PURE__ */ __name((n) => n === "Guinea" ? "(?<!New )Guinea" : n.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "namePiece");
var regionTerms = /* @__PURE__ */ __name((region) => [
  ...REGION_WORDS[region] || [],
  ...(REGION_COUNTRIES[region] || []).flatMap((c) => NAME_AS[c] || (NAME_SKIP.has(c) ? [] : [c]))
], "regionTerms");
var countryTerms = /* @__PURE__ */ __name((country) => [.../* @__PURE__ */ new Set([country, ...NAME_AS[country] || []])], "countryTerms");
var namePatterns = /* @__PURE__ */ new Map();
function namesPattern(key, terms) {
  if (!namePatterns.has(key)) {
    namePatterns.set(key, new RegExp(`(?<![\\p{L}\\p{N}])(?:${terms.map(namePiece).join("|")})(?![\\p{L}\\p{N}])`, "u"));
  }
  return namePatterns.get(key);
}
__name(namesPattern, "namesPattern");
var regionWordPattern = /* @__PURE__ */ __name((region) => namesPattern(`r:${region}`, regionTerms(region)), "regionWordPattern");
var countryNamePattern = /* @__PURE__ */ __name((country) => namesPattern(`c:${country}`, countryTerms(country)), "countryNamePattern");
var MAYBE_NAMES = `EXISTS (SELECT 1 FROM json_each(?) WHERE (COALESCE(title, '') || ' ' || COALESCE(content, '')) LIKE '%' || value || '%')`;
function readableText(post) {
  const content = post.content || "";
  const parts = [post.title || "", content.split("[ATTACH")[0]];
  const attach = content.match(/\[ATTACH:(\{.*\})\]/s);
  if (attach) {
    try {
      const { title, description } = JSON.parse(attach[1]);
      parts.push(title || "", description || "");
    } catch {
    }
  }
  return parts.join(" ");
}
__name(readableText, "readableText");
var inHomeRegion = /* @__PURE__ */ __name((p, country) => p.country === country && (!p.continent || !COUNTRY_REGION[country] || p.continent === COUNTRY_REGION[country]), "inHomeRegion");
var regionWhere = /* @__PURE__ */ __name((region) => ({
  sql: `(continent = ? OR (continent IS NULL AND country IN (${ID_LIST})))`,
  params: [region, JSON.stringify(REGION_COUNTRIES[region] || [])]
}), "regionWhere");
var countryWhere = /* @__PURE__ */ __name((country) => COUNTRY_REGION[country] ? { sql: `(country = ? AND (continent IS NULL OR continent = ?))`, params: [country, COUNTRY_REGION[country]] } : { sql: `country = ?`, params: [country] }, "countryWhere");
function boardVariants(board) {
  const lower = board.trim().toLowerCase();
  const slug = Object.keys(BOARD_NAMES).find((k) => k === lower || BOARD_NAMES[k].toLowerCase() === lower);
  return [.../* @__PURE__ */ new Set([board.trim(), lower, ...slug ? [slug, BOARD_NAMES[slug]] : []])];
}
__name(boardVariants, "boardVariants");
function usernameVariants(username) {
  const lower = username.trim().toLowerCase();
  return [.../* @__PURE__ */ new Set([username.trim(), lower, lower.charAt(0).toUpperCase() + lower.slice(1)])];
}
__name(usernameVariants, "usernameVariants");
async function getPostsPage(env, { activity, board, continent, country, username, before, limit }) {
  const boards = board ? boardVariants(board) : null;
  const users = username ? usernameVariants(username) : null;
  const boardSet = boards && new Set(boards.map((b) => b.toLowerCase()));
  const userSet = users && new Set(users.map((u) => u.toLowerCase()));
  const matchesBoardAndUser = /* @__PURE__ */ __name((p) => (!boardSet || boardSet.has((p.board || "").toLowerCase())) && (!userSet || userSet.has((p.username || "").toLowerCase())), "matchesBoardAndUser");
  const matches = /* @__PURE__ */ __name((p) => matchesBoardAndUser(p) && (!continent || regionOf(p) === continent) && (!country || inHomeRegion(p, country)), "matches");
  const page = /* @__PURE__ */ __name((posts) => posts.map((p) => boolify(p, POST_BOOL_FIELDS)), "page");
  if (activity) {
    const cond = [LIVE_POSTS];
    const params = [];
    if (before) {
      cond.push("last_activity < ?");
      params.push(before);
    }
    const where = cond.join(" AND ");
    const [commented, human] = await Promise.all([
      env.DB.prepare(
        `SELECT rowid AS _rid, * FROM posts WHERE id IN (SELECT post_id FROM comments WHERE deleted = 0) AND ${where} ORDER BY last_activity DESC LIMIT ?`
      ).bind(...params, limit).all(),
      // INDEXED BY fails fast instead of scanning every post if the index is missing
      env.DB.prepare(
        `SELECT rowid AS _rid, * FROM posts INDEXED BY idx_posts_human_activity WHERE ${HUMAN_POSTS} AND ${where} ORDER BY last_activity DESC LIMIT ?`
      ).bind(...params, limit).all().catch((err) => {
        console.error("get-posts activity: human posts unavailable:", err.message);
        return { results: [] };
      })
    ]);
    const c = commented.results || [], h = human.results || [];
    const byId2 = new Map([...h, ...c].map((p) => [p.id, p]));
    const scanned2 = [...byId2.values()].sort((a, b) => String(b.last_activity || "").localeCompare(String(a.last_activity || ""))).slice(0, limit);
    const more2 = c.length === limit || h.length === limit;
    return { posts: page(scanned2.filter(matches)), next_before: more2 && scanned2.length ? scanned2[scanned2.length - 1].last_activity : null };
  }
  const cursor = before ? parseInt(before, 10) : null;
  if (before && !Number.isFinite(cursor)) return { posts: [], next_before: null };
  const below = cursor ? " AND rowid < ?" : "";
  const belowParams = cursor ? [cursor] : [];
  if ((continent || country) && !users) {
    const words = continent && !country ? regionTerms(continent) : [];
    const maybe = words.length ? `, ${MAYBE_NAMES} AS _m` : "";
    const { results: win = [] } = await env.DB.prepare(
      `SELECT rowid AS _rid, board, username, continent, country${maybe} FROM posts WHERE ${LIVE_POSTS}${below} ORDER BY rowid DESC LIMIT ?`
    ).bind(...words.length ? [JSON.stringify(words)] : [], ...belowParams, REGION_WINDOW).all();
    const hits = win.filter((p) => matches(p) || p._m && matchesBoardAndUser(p)).slice(0, limit);
    let posts = [];
    if (hits.length) {
      const { results = [] } = await env.DB.prepare(
        `SELECT rowid AS _rid, * FROM posts WHERE rowid IN (${hits.map(() => "?").join(",")}) ORDER BY rowid DESC`
      ).bind(...hits.map((p) => p._rid)).all();
      posts = words.length ? results.filter((p) => matches(p) || regionWordPattern(continent).test(readableText(p))) : results;
    }
    const next_before = hits.length === limit ? hits[hits.length - 1]._rid : win.length === REGION_WINDOW ? win[win.length - 1]._rid : null;
    return { posts: page(posts), next_before };
  }
  const [col, values] = users ? ["username", users] : boards ? ["board", boards] : [null, [null]];
  const lists = await Promise.all(values.map(
    (v) => env.DB.prepare(
      `SELECT rowid AS _rid, * FROM posts WHERE ${col ? `${col} = ? AND ` : ""}${LIVE_POSTS}${below} ORDER BY rowid DESC LIMIT ?`
    ).bind(...col ? [v] : [], ...belowParams, limit).all().then((r) => r.results || [])
  ));
  const byId = new Map(lists.flat().map((p) => [p.id, p]));
  const scanned = [...byId.values()].sort((a, b) => b._rid - a._rid).slice(0, limit);
  const more = lists.some((l) => l.length === limit);
  return { posts: page(scanned.filter(matches)), next_before: more && scanned.length ? scanned[scanned.length - 1]._rid : null };
}
__name(getPostsPage, "getPostsPage");
async function handleRequest(request, env, ctx, corsHeaders) {
  const url = new URL(request.url);
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: corsHeaders });
  }
  const ip = request.headers.get("CF-Connecting-IP") || "0.0.0.0";
  let ip_hash = null;
  if (env.IP_HASH_KEY) {
    const hk = await crypto.subtle.importKey("raw", new TextEncoder().encode(env.IP_HASH_KEY), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
    const sig = await crypto.subtle.sign("HMAC", hk, new TextEncoder().encode(ip));
    ip_hash = Array.from(new Uint8Array(sig)).map((b) => b.toString(16).padStart(2, "0")).join("");
  }
  const body = request.method !== "GET" && request.method !== "HEAD" && url.pathname !== "/upload" ? await request.json().catch(() => ({})) : {};
  const now = (/* @__PURE__ */ new Date()).toISOString();
  const normMember = /* @__PURE__ */ __name((m) => {
    const ci = (m || "").lastIndexOf(":");
    if (ci > 0) {
      const r = m.slice(ci + 1);
      if (r === "admin" || r === "mod") return m.slice(0, ci);
    }
    return m || "";
  }, "normMember");
  const isHuddleMember = /* @__PURE__ */ __name((post, name) => {
    if (!name) return false;
    const lower = name.toLowerCase();
    if (lower === (post.username || post.owner || "").toLowerCase()) return true;
    return JSON.parse(post.huddle_members || "[]").some((m) => normMember(m).toLowerCase() === lower);
  }, "isHuddleMember");
  const huddleLine = /* @__PURE__ */ __name((post_id, text, when) => env.DB.prepare(
    `INSERT INTO comments (id, content, post_id, parent_comment_id, username, ip_hash, browser_id, is_mod, is_admin, moderator, mod_user_id, created_at) VALUES (?, ?, ?, NULL, '__system__', NULL, NULL, 0, 0, 0, NULL, ?)`
  ).bind(crypto.randomUUID(), text, post_id, when).run().catch(() => {
  }), "huddleLine");
  const passHuddleOn = /* @__PURE__ */ __name(async (post, when) => {
    const members = JSON.parse(post.huddle_members || "[]");
    if (!members.length) {
      await env.DB.prepare(`UPDATE posts SET deleted = 1 WHERE id = ?`).bind(post.id).run();
      return null;
    }
    const next = normMember(members[0]);
    await env.DB.prepare(`UPDATE posts SET username = ?, browser_id = NULL, mod_user_id = NULL, is_mod = 0, is_admin = 0, moderator = 0, huddle_members = ? WHERE id = ?`).bind(next, JSON.stringify(members.slice(1)), post.id).run();
    await huddleLine(post.id, `\u{1F451} ${next} now runs the huddle`, when);
    await upsertNotif(next, JSON.stringify({ text: `You now run "${post.title || "Huddle"}"`, postId: post.id }), post.id);
    const { results: waiting = [] } = await env.DB.prepare(
      `SELECT * FROM huddle_requests WHERE post_id = ? AND status = 'pending' AND kind IN ('add', 'remove') AND created_at > ?`
    ).bind(post.id, requestCutoff()).all().catch(() => ({ results: [] }));
    for (const rq of waiting) await upsertNotif(next, requestMessage(rq, post), post.id);
    return next;
  }, "passHuddleOn");
  const REQUEST_DAYS = 7;
  const waitingOn = /* @__PURE__ */ __name(async (name) => {
    const { results: rows = [] } = await env.DB.prepare(`SELECT id, message FROM system_notifications WHERE user_id = ? AND message LIKE '%"req":"%'`).bind(name).all();
    const byReq = /* @__PURE__ */ new Map();
    for (const r of rows) {
      try {
        const q = JSON.parse(r.message).req;
        if (q) byReq.set(r.id, q);
      } catch {
      }
    }
    if (!byReq.size) return [];
    const { results: rqs = [] } = await env.DB.prepare(
      `SELECT r.id, r.kind, r.target, p.username AS owner FROM huddle_requests r JOIN posts p ON p.id = r.post_id AND p.deleted = 0 WHERE r.id IN (${ID_LIST}) AND r.status = 'pending' AND r.created_at > ?`
    ).bind(JSON.stringify([...new Set(byReq.values())]), requestCutoff()).all();
    const lower = name.toLowerCase();
    const live = new Set(rqs.filter((r) => (r.kind === "invite" ? r.target : r.owner || "").toLowerCase() === lower).map((r) => r.id));
    return [...byReq].filter(([, q]) => live.has(q)).map(([id]) => id);
  }, "waitingOn");
  function requestCutoff() {
    return new Date(Date.now() - REQUEST_DAYS * 864e5).toISOString();
  }
  __name(requestCutoff, "requestCutoff");
  function requestMessage(rq, post) {
    const title = post.title || "Huddle";
    const text = rq.kind === "invite" ? `${rq.from_user} invited you to "${title}"` : rq.kind === "add" ? `${rq.from_user} wants to invite ${rq.target} to "${title}"` : `${rq.from_user} wants to remove ${rq.target} from "${title}"`;
    return JSON.stringify({ text, postId: post.id, req: rq.id, ...rq.preview ? { preview: rq.preview } : {} });
  }
  __name(requestMessage, "requestMessage");
  const huddlePreview = /* @__PURE__ */ __name(async (postId) => {
    const row = await env.DB.prepare(`SELECT content FROM comments WHERE post_id = ? AND pinned = 1 AND deleted = 0 AND username != '__system__' ORDER BY created_at LIMIT 1`).bind(postId).first().catch(() => null);
    if (!row) return null;
    const raw = String(row.content || ""), cut = raw.search(/\n\n\[ATTACH/);
    let text = (cut >= 0 ? raw.slice(0, cut) : raw).replace(/\s+/g, " ").trim();
    if (!text && cut >= 0) {
      const tail = raw.slice(cut);
      if (/"type":"video"/.test(tail)) text = "\u{1F3AC} Video";
      else if (/"type":"image"/.test(tail)) text = "\u{1F4F7} Photo";
      else {
        let label = "";
        try {
          const att = JSON.parse(tail.slice(tail.indexOf(":") + 1, tail.lastIndexOf("]")));
          label = String(att.title || "").trim() || new URL(att.url).hostname.replace(/^www\./, "");
        } catch {
        }
        text = "\u{1F517} " + (label || "Link");
      }
    }
    return text ? text.length > 80 ? text.slice(0, 79).trimEnd() + "\u2026" : text : null;
  }, "huddlePreview");
  const accountRole = /* @__PURE__ */ __name(async (name) => {
    const row = await env.DB.prepare(`SELECT role FROM mod_users WHERE LOWER(username) = ? AND deleted_at IS NULL LIMIT 1`).bind(String(name).toLowerCase()).first();
    return row && (row.role === "admin" || row.role === "mod") ? row.role : null;
  }, "accountRole");
  const pendingRequest = /* @__PURE__ */ __name((postId, kind, target) => env.DB.prepare(
    `SELECT * FROM huddle_requests WHERE post_id = ? AND kind = ? AND LOWER(target) = ? AND status = 'pending' AND created_at > ? LIMIT 1`
  ).bind(postId, kind, String(target).toLowerCase(), requestCutoff()).first(), "pendingRequest");
  const newRequest = /* @__PURE__ */ __name(async (post, kind, from, target, role) => {
    const rq = { id: crypto.randomUUID(), post_id: post.id, kind, from_user: from, target, target_role: role || null, status: "pending", created_at: now };
    if (kind === "invite") rq.preview = await huddlePreview(post.id);
    await env.DB.prepare(`INSERT INTO huddle_requests (id, post_id, kind, from_user, target, target_role, status, created_at) VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)`).bind(rq.id, post.id, kind, from, target, rq.target_role, now).run();
    await upsertNotif(kind === "invite" ? target : post.username, requestMessage(rq, post), post.id);
    return rq;
  }, "newRequest");
  const sendInvite = /* @__PURE__ */ __name(async (post, from, target) => {
    if (isHuddleMember(post, target) || await pendingRequest(post.id, "invite", target)) return null;
    return newRequest(post, "invite", from, target, await accountRole(target));
  }, "sendInvite");
  const retireAccount = /* @__PURE__ */ __name(async (account, when, by) => {
    const name = account.username;
    const left = [];
    if (name) {
      const { results } = await env.DB.prepare(
        `SELECT * FROM posts INDEXED BY idx_posts_huddles WHERE is_huddle = 1 AND deleted = 0 AND (username = ? OR huddle_members LIKE ?)`
      ).bind(name, `%"${name}%`).all();
      for (const huddle of results || []) {
        if ((huddle.username || "").toLowerCase() === name.toLowerCase()) {
          await huddleLine(huddle.id, `\u{1F44B} ${name} left the huddle`, when);
          left.push({ id: huddle.id, ended: !await passHuddleOn(huddle, when) });
        } else {
          const members = JSON.parse(huddle.huddle_members || "[]");
          const rest = members.filter((m) => normMember(m).toLowerCase() !== name.toLowerCase());
          if (rest.length === members.length) continue;
          await env.DB.prepare(`UPDATE posts SET huddle_members = ? WHERE id = ?`).bind(JSON.stringify(rest), huddle.id).run();
          await huddleLine(huddle.id, `\u{1F44B} ${name} left the huddle`, when);
          left.push({ id: huddle.id });
        }
      }
    }
    await env.DB.prepare(`UPDATE mod_users SET deleted_at = ?, deleted_by = ?, left_huddles = ? WHERE id = ?`).bind(when, by, JSON.stringify(left), account.id).run();
  }, "retireAccount");
  const restoreAccount = /* @__PURE__ */ __name(async (account, when) => {
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
      await huddleLine(spot.id, `\u{1F44B} ${name} is back in the huddle`, when);
    }
    await env.DB.prepare(`UPDATE mod_users SET deleted_at = NULL, deleted_by = NULL, left_huddles = NULL WHERE id = ?`).bind(account.id).run();
  }, "restoreAccount");
  async function upsertNotif(userId, message, postId) {
    const isComment = message.includes('"dk":"comment"');
    if (postId && isComment) {
      const existing = await env.DB.prepare(
        `SELECT id FROM system_notifications WHERE user_id = ? AND message LIKE ? AND message LIKE ? LIMIT 1`
      ).bind(userId, `%"postId":"${postId}"%`, '%"dk":"comment"%').first();
      if (existing) {
        await env.DB.prepare(`UPDATE system_notifications SET message = ?, created_at = ? WHERE id = ?`).bind(message, now, existing.id).run().catch(() => {
        });
        return;
      }
    }
    await env.DB.prepare(`INSERT INTO system_notifications (id, user_id, message) VALUES (?, ?, ?)`).bind(crypto.randomUUID(), userId, message).run();
  }
  __name(upsertNotif, "upsertNotif");
  async function maskBid(id, mine) {
    if (!id) return id;
    if (mine && id === mine) return id;
    const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(env.IP_HASH_KEY || env.JWT_SECRET || "pp"), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
    const s = new Uint8Array(await crypto.subtle.sign("HMAC", k, new TextEncoder().encode("bid:" + id)));
    return "x" + Array.from(s.slice(0, 12)).map((b) => b.toString(16).padStart(2, "0")).join("");
  }
  __name(maskBid, "maskBid");
  function serverError(err) {
    console.error("server error:", err && (err.stack || err.message));
    return json({ error: "Something went wrong. Please try again." }, 500);
  }
  __name(serverError, "serverError");
  function json(data, status = 200) {
    return new Response(JSON.stringify(data), {
      status,
      headers: { ...corsHeaders, "Content-Type": "application/json" }
    });
  }
  __name(json, "json");
  async function getAuthUser() {
    const authHeader = request.headers.get("Authorization");
    if (!authHeader?.startsWith("Bearer ")) return null;
    const token = authHeader.slice(7);
    const user = await verifyJWT(token, env.JWT_SECRET);
    if (user?.sub) {
      const account = await env.DB.prepare(`SELECT deleted_at, see_all_huddles, role, password_changed_at FROM mod_users WHERE id = ?`).bind(user.sub).first();
      if (!account || account.deleted_at) return null;
      if (account.password_changed_at && (!user.iat || user.iat * 1e3 < Date.parse(account.password_changed_at))) return null;
      user.role = account.role || "user";
      user.see_all_huddles = !!account.see_all_huddles;
      const now2 = (/* @__PURE__ */ new Date()).toISOString();
      ctx.waitUntil(
        env.DB.prepare("UPDATE mod_users SET last_active = ? WHERE id = ?").bind(now2, user.sub).run()
      );
    }
    return user;
  }
  __name(getAuthUser, "getAuthUser");
  const botKey = request.headers.get("x-bot-key");
  const isBot = !!(botKey && env.BOT_KEY && botKey === env.BOT_KEY);
  const authUser = await getAuthUser();
  const isAdmin = authUser?.role === "admin";
  const isModerator = authUser?.role === "mod" || authUser?.role === "admin";
  const seeAllHuddles = isAdmin && !!authUser?.see_all_huddles;
  const isMember = false;
  let username = null;
  if (isBot) {
    username = typeof body.username === "string" && body.username.trim() || "NewsBot";
  } else if (isModerator) {
    username = authUser.username || "Mod";
  } else if (authUser) {
    username = authUser.username || null;
  }
  const signInRequired = /* @__PURE__ */ __name(() => json({ error: "Sign in required" }, 401), "signInRequired");
  let extinct = null;
  const extinctNames = /* @__PURE__ */ __name(async () => {
    if (!extinct) {
      const { results } = await env.DB.prepare(`SELECT username FROM mod_users WHERE deleted_at IS NOT NULL`).all();
      extinct = new Set((results || []).map((r) => r.username));
    }
    return extinct;
  }, "extinctNames");
  const scrubNames = /* @__PURE__ */ __name((text, names) => {
    if (typeof text !== "string") return text;
    for (const name of names) {
      if (text.includes(name)) text = text.replace(new RegExp(`(?<![\\w-])${name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?![\\w-])`, "g"), EXTINCT_NAME);
    }
    return text;
  }, "scrubNames");
  const publicRows = /* @__PURE__ */ __name(async (rows) => {
    const names = await extinctNames();
    return rows.map(({ ip_hash: ip_hash2, ...visible }) => {
      const row = isModerator ? { ...visible, ip_hash: ip_hash2 } : visible;
      if (row.username === "__system__") return { ...row, content: scrubNames(row.content, names) };
      return names.has(row.username) ? { ...row, username: EXTINCT_NAME, browser_id: null, is_mod: false, moderator: false, mod_user_id: null } : row;
    });
  }, "publicRows");
  async function isBanned() {
    if (isAdmin) return false;
    const bid = (body.browser_id || "").trim();
    const conditions = isModerator ? ["username = ?"] : ["ip_hash = ?", "username = ?"];
    const params = isModerator ? [username] : [ip_hash, username];
    if (bid) {
      conditions.push("browser_id = ?");
      params.push(bid);
    }
    const row = await env.DB.prepare(
      `SELECT 1 FROM bans WHERE ${conditions.join(" OR ")} LIMIT 1`
    ).bind(...params).first();
    return !!row;
  }
  __name(isBanned, "isBanned");
  async function isJailed() {
    if (isAdmin) return false;
    const bid = (body.browser_id || "").trim();
    const uname = (username || "").trim();
    if (!bid && !uname) return false;
    const conditions = [];
    const params = [];
    if (bid) {
      conditions.push("browser_id = ?");
      params.push(bid);
    }
    if (uname) {
      conditions.push("username = ?");
      params.push(uname);
    }
    const row = await env.DB.prepare(
      `SELECT 1 FROM jailed WHERE ${conditions.join(" OR ")} LIMIT 1`
    ).bind(...params).first();
    return !!row;
  }
  __name(isJailed, "isJailed");
  async function bumpPost(post_id) {
    await env.DB.prepare(`UPDATE posts SET last_activity = ? WHERE id = ?`).bind(now, post_id).run();
  }
  __name(bumpPost, "bumpPost");
  async function getPostVoteSummary(postId, browserId) {
    const { results } = await env.DB.prepare(
      `SELECT value, browser_id FROM post_votes WHERE post_id = ?`
    ).bind(postId).all();
    const score = (results || []).reduce((s, v) => s + (v.value || 0), 0);
    const myVote = (results || []).find((v) => v.browser_id === browserId)?.value || 0;
    return { score, myVote, voteCount: (results || []).length };
  }
  __name(getPostVoteSummary, "getPostVoteSummary");
  if (url.pathname.startsWith("/media/")) {
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
    if (url.searchParams.get("thumb") === "1" && !key.startsWith("thumbs/")) {
      const small = await env.MEDIA.head(`thumbs/${key}.jpg`).catch(() => null);
      if (small) key = `thumbs/${key}.jpg`;
    }
    try {
      const want = (request.headers.get("range") || "").trim();
      const rm = /^bytes=(\d*)-(\d*)$/.exec(want);
      let range = null;
      if (rm && (rm[1] !== "" || rm[2] !== "")) {
        if (rm[1] === "") range = { suffix: Number(rm[2]) };
        else range = rm[2] === "" ? { offset: Number(rm[1]) } : { offset: Number(rm[1]), length: Number(rm[2]) - Number(rm[1]) + 1 };
        if (range.length !== void 0 && range.length <= 0 || range.suffix === 0) range = null;
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
      const inm = request.headers.get("if-none-match");
      if (inm && !range && inm.split(",").some((t) => t.trim().replace(/^W\//, "") === head.httpEtag)) {
        return new Response(null, { status: 304, headers });
      }
      if (range) {
        const start = range.suffix !== void 0 ? Math.max(0, size - range.suffix) : range.offset;
        if (start >= size) {
          headers.set("content-range", `bytes */${size}`);
          return new Response(null, { status: 416, headers });
        }
        const end = range.length !== void 0 ? Math.min(size - 1, start + range.length - 1) : size - 1;
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
  if (url.pathname === "/upload" && request.method === "POST") {
    if (!username) return signInRequired();
    const ALLOWED = /^(image\/(jpeg|png|gif|webp)|video\/(mp4|webm|quicktime))$/;
    const MAX_VIDEO = 1e8, MAX_IMAGE = 5e7;
    const reqType = (request.headers.get("content-type") || "").split(";")[0].trim().toLowerCase();
    if (reqType && reqType !== "multipart/form-data") {
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
      if (!ALLOWED.test(file.type)) return json({ error: "Unsupported file type" }, 400);
      const MAX_SIZE = 50 * 1024 * 1024;
      if (file.size > MAX_SIZE) return json({ error: "File too large (max 50 MB)" }, 400);
      const buffer = await file.arrayBuffer();
      const ext = (file.name || "file").split(".").pop().toLowerCase().replace(/[^a-z0-9]/g, "") || "bin";
      const key = `${crypto.randomUUID()}.${ext}`;
      const clean = stripMedia(new Uint8Array(buffer), file.type).bytes;
      await env.MEDIA.put(key, clean, {
        httpMetadata: { contentType: file.type, cacheControl: "public, max-age=31536000, immutable" }
      });
      return json({ url: `${url.origin}/media/${key}` });
    } catch (err) {
      return serverError(err);
    }
  }
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
        { sub: id, role: "user", username: uname.trim(), iat: Math.floor(Date.now() / 1e3), exp: Math.floor(Date.now() / 1e3) + 86400 * 90 },
        env.JWT_SECRET
      );
      return json({ token, user: { id, role: "user", username: uname.trim() } });
    } catch (err) {
      return serverError(err);
    }
  }
  if (url.pathname === "/login" && request.method === "POST") {
    const { username: uname, password } = body;
    if (!uname || !password) return json({ error: "Missing fields" }, 400);
    try {
      const user = await env.DB.prepare(
        `SELECT * FROM mod_users WHERE username = ? AND deleted_at IS NULL`
      ).bind(uname.trim()).first();
      if (!user) return json({ error: "Invalid credentials" }, 401);
      const lockedMsg = /* @__PURE__ */ __name((until) => {
        const mins = Math.max(1, Math.ceil((new Date(until) - Date.now()) / 6e4));
        return `Too many wrong passwords. This account is locked for ${mins} more minute${mins === 1 ? "" : "s"}. Try again later, or ask an admin to unlock it.`;
      }, "lockedMsg");
      if (user.locked_until && user.locked_until > now) return json({ error: lockedMsg(user.locked_until), locked: true }, 423);
      const ok = await verifyPassword(password, user.password_hash).catch(() => false);
      if (!ok) {
        const row = await env.DB.prepare(`UPDATE mod_users SET failed_logins = failed_logins + 1 WHERE id = ? RETURNING failed_logins`).bind(user.id).first();
        if ((row?.failed_logins || 0) >= LOGIN_TRIES) {
          const until = new Date(Date.now() + LOCK_MINUTES * 6e4).toISOString();
          await env.DB.prepare(`UPDATE mod_users SET failed_logins = 0, locked_until = ? WHERE id = ?`).bind(until, user.id).run();
          const { results: admins = [] } = await env.DB.prepare(`SELECT username FROM mod_users WHERE role = 'admin' AND deleted_at IS NULL AND username IS NOT NULL`).all();
          const msg = JSON.stringify({ text: `${user.username}'s account was locked for ${LOCK_MINUTES} minutes after ${LOGIN_TRIES} wrong passwords. You can unlock it in the mod panel.`, icon: "\u{1F512}" });
          await Promise.all(admins.map((a) => upsertNotif(a.username, msg))).catch((err) => console.error("lock notify failed", err.message));
          return json({ error: lockedMsg(until), locked: true }, 423);
        }
        return json({ error: "Invalid credentials" }, 401);
      }
      if (user.failed_logins || user.locked_until) await env.DB.prepare(`UPDATE mod_users SET failed_logins = 0, locked_until = NULL WHERE id = ?`).bind(user.id).run();
      const token = await signJWT(
        { sub: user.id, role: user.role, username: user.username, iat: Math.floor(Date.now() / 1e3), exp: Math.floor(Date.now() / 1e3) + 86400 * 90 },
        env.JWT_SECRET
      );
      return json({ token, user: { id: user.id, role: user.role, username: user.username } });
    } catch (err) {
      return serverError(err);
    }
  }
  if (url.pathname === "/update-password" && request.method === "POST") {
    if (!authUser) return json({ error: "Unauthorized" }, 401);
    const { newPassword, currentPassword } = body;
    if (!newPassword) return json({ error: "Missing newPassword" }, 400);
    if (!currentPassword) return json({ error: "Enter your current password" }, 400);
    if (String(newPassword).length < 6) return json({ error: "Password must be at least 6 characters" }, 400);
    try {
      const acct = await env.DB.prepare(`SELECT id, username, role, password_hash FROM mod_users WHERE id = ? AND deleted_at IS NULL`).bind(authUser.sub).first();
      if (!acct) return json({ error: "Unauthorized" }, 401);
      if (!await verifyPassword(currentPassword, acct.password_hash).catch(() => false)) return json({ error: "Your current password isn't right" }, 403);
      const hash = await hashPassword(newPassword);
      const changedAt = new Date(Math.floor(Date.now() / 1e3) * 1e3).toISOString();
      await env.DB.prepare(`UPDATE mod_users SET password_hash = ?, password_changed_at = ?, failed_logins = 0, locked_until = NULL WHERE id = ?`).bind(hash, changedAt, acct.id).run();
      const t = Math.floor(Date.now() / 1e3) + 3;
      const token = await signJWT({ sub: acct.id, role: acct.role, username: acct.username, iat: t, exp: t + 86400 * 90 }, env.JWT_SECRET);
      return json({ success: true, token });
    } catch (err) {
      return serverError(err);
    }
  }
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
        return json({ error: "Banned", _debug: { username, browser_id: (body.browser_id || "").trim() } }, 403);
      }
      if (isHuddle) {
        body.board = "Huddles";
        body.community_id = "feedback";
        body.content = body.content || "";
      }
      if (!body.board) body.board = "General";
      if (!isModerator && !isBot && [body.board, body.category, body.community_id].some((v) => String(v || "").trim().toLowerCase() === "announcements")) {
        return json({ error: "Only mods can post in Announcements" }, 403);
      }
      if (!caged && !isModerator && !isBot && [body.board, body.category, body.community_id].some((v) => ["cage", "the cage"].includes(String(v || "").trim().toLowerCase()))) {
        return json({ error: "Only caged birds can post in The Cage" }, 403);
      }
      let botClaim = null;
      if (isBot) {
        botClaim = await claimBotPost(env, botPostKeys(body.content), now);
        if (botClaim.duplicate) return json({ success: false, duplicate: true }, 409);
      }
      const invitees = isHuddle ? [...new Set((Array.isArray(body.huddle_members) ? body.huddle_members : []).map(normMember).filter((n) => n && n.toLowerCase() !== username.toLowerCase()))] : [];
      const huddleMembers = isHuddle ? "[]" : null;
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
        isModerator ? authUser.sub ?? null : null,
        body.continent || null,
        body.country || null,
        body.board,
        body.community_id || null,
        isHuddle ? 1 : 0,
        huddleMembers,
        now
      ).run().catch(async (err) => {
        for (const key of botClaim?.claimed || []) {
          await env.DB.prepare(`DELETE FROM bot_links WHERE url = ?`).bind(key).run().catch(() => {
          });
        }
        throw err;
      });
      const first = isHuddle && typeof body.first_chirp === "string" && body.first_chirp.trim() ? body.first_chirp.slice(0, 8e3) : null;
      if (first) {
        await env.DB.prepare(`INSERT INTO comments (id, content, post_id, parent_comment_id, username, ip_hash, browser_id, is_mod, is_admin, moderator, mod_user_id, created_at, pinned) VALUES (?, ?, ?, NULL, ?, ?, ?, ?, ?, ?, ?, ?, 1)`).bind(crypto.randomUUID(), first, id, username, ip_hash, body.browser_id || null, isModerator ? 1 : 0, isAdmin ? 1 : 0, isModerator ? 1 : 0, isModerator ? authUser.sub ?? null : null, now).run();
      }
      if (isHuddle && invitees.length) {
        const extinct2 = await extinctNames();
        const newPost = { id, title: body.title || null, username, huddle_members: "[]" };
        for (const name of invitees) if (!extinct2.has(name)) await sendInvite(newPost, username, name);
      }
      const post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ?`).bind(id).first();
      return json({ success: true, post: boolify(post, POST_BOOL_FIELDS) });
    } catch (err) {
      return serverError(err);
    }
  }
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
        const chirpAt = /* @__PURE__ */ __name(async (older2, skip) => (await env.DB.prepare(
          `SELECT created_at FROM comments WHERE post_id = ? AND deleted = 0${older2 ? " AND created_at < ?" : ""} ORDER BY created_at DESC LIMIT 1 OFFSET ?`
        ).bind(...older2 ? [id, older2, skip] : [id, skip]).first())?.created_at || "", "chirpAt");
        const reachBack = /* @__PURE__ */ __name(async (at) => {
          if (at && (from === "" ? false : at < from)) from = await chirpAt(at, 19);
        }, "reachBack");
        from = sp.has("from") ? sp.get("from") : null;
        if (sp.get("all") === "1") from = "";
        else {
          if (from === null) from = await chirpAt(null, pageSize - 1);
          if (sp.get("older") === "1" && from) from = await chirpAt(from, pageSize - 1);
          const to = sp.get("to"), toUser = sp.get("to_user");
          if (to) {
            const row = await env.DB.prepare(`SELECT created_at, pinned FROM comments WHERE id = ? AND post_id = ? AND deleted = 0`).bind(to, id).first();
            if (row && !row.pinned) await reachBack(row.created_at);
          }
          if (toUser) {
            const row = await env.DB.prepare(`SELECT created_at FROM comments WHERE post_id = ? AND username = ? AND deleted = 0 ORDER BY created_at DESC LIMIT 1`).bind(id, toUser).first();
            if (row) await reachBack(row.created_at);
            else from = "";
          }
        }
        const [{ results: page }, { results: pins }] = await Promise.all([
          env.DB.prepare(`SELECT * FROM comments WHERE post_id = ? AND deleted = 0 AND created_at >= ? ORDER BY created_at ASC`).bind(id, from).all(),
          env.DB.prepare(`SELECT * FROM comments WHERE post_id = ? AND pinned = 1 AND deleted = 0`).bind(id).all()
        ]);
        const inPage = new Set((page || []).map((c) => c.id));
        comments = [...(pins || []).filter((c) => !inPage.has(c.id)), ...page || []];
      } else {
        comments = (await env.DB.prepare(`SELECT * FROM comments WHERE post_id = ? AND deleted = 0 ORDER BY created_at ASC`).bind(id).all()).results || [];
      }
      const { results: topRows } = await env.DB.prepare(
        `SELECT c.*, COUNT(r.id) AS rx_count FROM comments c JOIN comment_reactions r ON r.comment_id = c.id WHERE c.post_id = ? AND c.deleted = 0 GROUP BY c.id HAVING COUNT(r.id) >= 1 ORDER BY rx_count DESC, c.created_at DESC LIMIT 6`
      ).bind(id).all();
      const top = topRows || [];
      const { results: repRows } = await env.DB.prepare(
        `SELECT c.*, COUNT(r.id) AS reply_count FROM comments c JOIN comments r ON r.parent_comment_id = c.id AND r.deleted = 0 WHERE c.post_id = ? AND c.deleted = 0 GROUP BY c.id HAVING COUNT(r.id) >= 1 ORDER BY reply_count DESC, c.created_at DESC LIMIT 9`
      ).bind(id).all();
      const replied = repRows || [];
      const rxIds = [.../* @__PURE__ */ new Set([...comments.map((c) => c.id), ...top.map((c) => c.id), ...replied.map((c) => c.id)])];
      const { results: reactions } = await env.DB.prepare(
        `SELECT comment_id, browser_id, emoji, username FROM comment_reactions WHERE comment_id IN (${ID_LIST})`
      ).bind(JSON.stringify(rxIds)).all();
      const payload = {
        post: (await publicRows([boolify(post, POST_BOOL_FIELDS)]))[0],
        comments: await publicRows(comments.map((c) => boolify(c, COMMENT_BOOL_FIELDS))),
        reactions: reactions || [],
        top: await publicRows(top.map((c) => boolify(c, COMMENT_BOOL_FIELDS))),
        replied: await publicRows(replied.map((c) => boolify(c, COMMENT_BOOL_FIELDS)))
      };
      const digest = await crypto.subtle.digest("SHA-1", new TextEncoder().encode(JSON.stringify(payload)));
      const version = [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
      if (sp.get("v") === version) return json({ unchanged: true });
      if (!paged) return json({ ...payload, version });
      const have = new Set(comments.map((c) => c.id));
      const parents = [...new Set(comments.map((c) => c.parent_comment_id).filter((p) => p && !have.has(p)))];
      const [total, older, quoted] = await Promise.all([
        env.DB.prepare(`SELECT COUNT(*) AS n FROM comments WHERE post_id = ? AND deleted = 0 AND (username IS NULL OR username != '__system__')`).bind(id).first(),
        from ? env.DB.prepare(`SELECT 1 FROM comments WHERE post_id = ? AND deleted = 0 AND created_at < ? LIMIT 1`).bind(id, from).first() : null,
        parents.length ? env.DB.prepare(`SELECT * FROM comments WHERE id IN (${ID_LIST}) AND deleted = 0`).bind(JSON.stringify(parents)).all() : { results: [] }
      ]);
      return json({
        ...payload,
        version,
        from,
        has_more: !!older,
        comment_total: total?.n || 0,
        // Chirps quoted by replies on this page but older than it, for the quote and nothing else
        quoted: await publicRows((quoted.results || []).map((c) => boolify(c, COMMENT_BOOL_FIELDS)))
      });
    } catch (err) {
      return serverError(err);
    }
  }
  if (url.pathname === "/get-posts") {
    try {
      const board = url.searchParams.get("board") || null;
      const continent = url.searchParams.get("continent") || null;
      const country = url.searchParams.get("country") || null;
      const username2 = url.searchParams.get("username") || null;
      const activityFilter = url.searchParams.get("activity") === "1";
      const limit = activityFilter ? 1e4 : Math.min(parseInt(url.searchParams.get("limit") || "50"), 1e4);
      const offset = parseInt(url.searchParams.get("offset") || "0");
      const search = url.searchParams.get("search") || null;
      const sortBy = url.searchParams.get("sort") === "activity" ? "last_activity" : "created_at";
      const BOTS = ["NewsBot", "ScienceBot", "NatureBot", "SportsBot"];
      const isHuddleBoard = board && (board.toLowerCase() === "feedback" || board.toLowerCase() === "huddles");
      const since = url.searchParams.get("since") || null;
      const until = url.searchParams.get("until") || null;
      const before = url.searchParams.get("before") || null;
      const rankSort = url.searchParams.get("sort");
      if (rankSort === "flaps" || rankSort === "chirps") {
        const range = url.searchParams.get("range");
        const since2 = range === "all" ? "" : new Date(Date.now() - (range === "day" ? 1 : 7) * 864e5).toISOString();
        const { results: top = [] } = await env.DB.prepare(
          rankSort === "flaps" ? `SELECT post_id, SUM(value) AS n FROM post_votes WHERE created_at >= ? GROUP BY post_id HAVING n > 0 ORDER BY n DESC LIMIT 500` : `SELECT post_id, COUNT(*) AS n FROM comments WHERE deleted = 0 AND (username IS NULL OR username != '__system__') AND created_at >= ? GROUP BY post_id ORDER BY n DESC LIMIT 500`
        ).bind(since2).all();
        const countOf = new Map(top.map((r) => [r.post_id, r.n]));
        const ids = [...countOf.keys()];
        const rows2 = [];
        for (let i = 0; i < ids.length; i += 90) {
          const chunk = ids.slice(i, i + 90);
          const { results: results2 = [] } = await env.DB.prepare(
            `SELECT rowid AS _rid, * FROM posts WHERE id IN (${chunk.map(() => "?").join(",")}) AND ${LIVE_POSTS}`
          ).bind(...chunk).all();
          rows2.push(...results2);
        }
        rows2.sort((a, b) => (countOf.get(b.id) || 0) - (countOf.get(a.id) || 0));
        const posts = await publicRows(await addCommentCounts(env, rows2.map((p) => ({ ...boolify(p, POST_BOOL_FIELDS), rank: countOf.get(p.id) || 0 }))));
        return json({ posts, next_before: null });
      }
      if (url.searchParams.get("people") === "1") {
        const { results: results2 = [] } = await env.DB.prepare(
          `SELECT rowid AS _rid, * FROM posts INDEXED BY idx_posts_human_activity WHERE ${HUMAN_POSTS} AND ${LIVE_POSTS} ORDER BY last_activity DESC LIMIT 500`
        ).all();
        return json({ posts: await publicRows(await addCommentCounts(env, results2.map((p) => boolify(p, POST_BOOL_FIELDS)))), next_before: null });
      }
      if (!search && !since && !until && !isHuddleBoard && (activityFilter || board || continent || country || username2 || before)) {
        const pageLimit = Math.min(parseInt(url.searchParams.get("limit") || "50") || 50, 100);
        const page = await getPostsPage(env, { activity: activityFilter, board, continent, country, username: username2, before, limit: pageLimit });
        return json({ ...page, posts: await publicRows(await addCommentCounts(env, page.posts)) });
      }
      let q = `SELECT rowid AS _rid, * FROM posts${isHuddleBoard ? " INDEXED BY idx_posts_huddles" : ""} WHERE deleted = 0 AND (archived = 0 OR archived IS NULL)`;
      const params = [];
      if (activityFilter) {
        const placeholders = BOTS.map(() => "?").join(",");
        q += ` AND (username NOT IN (${placeholders}) OR id IN (SELECT DISTINCT post_id FROM comments WHERE deleted = 0))`;
        params.push(...BOTS);
      }
      if (isHuddleBoard) {
        q += ` AND is_huddle = 1`;
        const huddleUsername = authUser?.username || null;
        if (!seeAllHuddles) {
          if (huddleUsername) {
            q += ` AND (LOWER(username) = LOWER(?) OR (huddle_members IS NOT NULL AND (LOWER(huddle_members) LIKE LOWER(?) OR LOWER(huddle_members) LIKE LOWER(?))))`;
            params.push(huddleUsername, `%"${huddleUsername}"%`, `%"${huddleUsername}:%`);
          } else {
            q += ` AND 1 = 0`;
          }
        }
      } else {
        q += ` AND (is_huddle = 0 OR is_huddle IS NULL)`;
        if (board) {
          q += ` AND (LOWER(community_id) = LOWER(?) OR LOWER(board) = LOWER(?))`;
          params.push(board, board);
        }
      }
      if (!isHuddleBoard && continent) {
        const w = regionWhere(continent);
        q += ` AND ${w.sql}`;
        params.push(...w.params);
      }
      const chipSearch = !!search && !!country && search.toLowerCase() === country.toLowerCase();
      const cw = country && countryWhere(country);
      if (!isHuddleBoard && country && !chipSearch) {
        q += ` AND ${cw.sql}`;
        params.push(...cw.params);
      }
      if (username2 && isHuddleBoard) {
        const un = username2.toLowerCase();
        q += ` AND (LOWER(username) = ? OR (huddle_members IS NOT NULL AND (LOWER(huddle_members) LIKE ? OR LOWER(huddle_members) LIKE ?)))`;
        params.push(un, `%"${un}"%`, `%"${un}:%`);
      } else if (username2) {
        q += ` AND LOWER(username) = ?`;
        params.push(username2.toLowerCase());
      }
      if (chipSearch) {
        q += ` AND (${MAYBE_NAMES} OR ${cw.sql})`;
        params.push(JSON.stringify(countryTerms(country)), ...cw.params);
      } else if (search) {
        q += ` AND (title LIKE ? OR content LIKE ?)`;
        params.push(`%${search}%`, `%${search}%`);
      }
      if (since) {
        q += ` AND created_at >= ?`;
        params.push(since);
      }
      if (until) {
        q += ` AND created_at < ?`;
        params.push(until);
      }
      q += ` ORDER BY pinned_global DESC, pinned DESC, ${sortBy} DESC, created_at DESC LIMIT ? OFFSET ?`;
      params.push(limit, offset);
      const { results } = await env.DB.prepare(q).bind(...params).all();
      const nextBefore = (results || []).length >= limit ? results[results.length - 1]._rid : null;
      const rows = chipSearch ? (results || []).filter((p) => inHomeRegion(p, country) || countryNamePattern(country).test(readableText(p))) : results || [];
      if (chipSearch && !offset) {
        const [human, commented] = await Promise.all([
          env.DB.prepare(`SELECT rowid AS _rid, * FROM posts INDEXED BY idx_posts_human_activity WHERE ${HUMAN_POSTS} AND ${cw.sql} AND ${LIVE_POSTS}`).bind(...cw.params).all(),
          env.DB.prepare(`SELECT rowid AS _rid, * FROM posts WHERE ${cw.sql} AND id IN (SELECT post_id FROM comments WHERE deleted = 0) AND ${LIVE_POSTS}`).bind(...cw.params).all()
        ]).catch((err) => {
          console.error("get-posts country pill: flock posts unavailable:", err.message);
          return [{ results: [] }, { results: [] }];
        });
        const have = new Set(rows.map((p) => p.id));
        for (const p of [...human.results || [], ...commented.results || []]) {
          if (!have.has(p.id)) {
            have.add(p.id);
            rows.push(p);
          }
        }
      }
      if (isHuddleBoard && authUser?.username) await addHuddleInbox(env, rows, authUser.username);
      return json({
        posts: await publicRows(await addCommentCounts(env, rows.map((p) => boolify(p, POST_BOOL_FIELDS)))),
        next_before: nextBefore
      });
    } catch (err) {
      return serverError(err);
    }
  }
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
  if (url.pathname === "/bot-config") {
    if (!isAdmin && !isBot) return json({ error: "Unauthorized" }, 401);
    if (request.method === "GET") {
      const row = await env.DB.prepare(`SELECT config FROM bot_config WHERE id = 1`).first();
      try {
        return json({ config: row?.config ? JSON.parse(row.config) : null });
      } catch {
        return json({ config: null });
      }
    }
    if (!isAdmin) return json({ error: "Unauthorized" }, 401);
    if (!body.config) return json({ error: "Missing config" }, 400);
    try {
      await env.DB.prepare(`UPDATE bot_config SET config = ?, updated_at = ? WHERE id = 1`).bind(JSON.stringify(body.config), now).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }
  if (url.pathname === "/update-post") {
    if (!isBot) return json({ error: "Unauthorized" }, 401);
    if (!body.post_id || !body.content) return json({ error: "Missing fields" }, 400);
    try {
      await env.DB.prepare(`UPDATE posts SET content = ? WHERE id = ?`).bind(body.content, body.post_id).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }
  if (url.pathname === "/purge-deleted") {
    return json({ error: "Disabled: deleted posts are kept. Use Delete forever in the admin controls." }, 410);
    if (!isBot) return json({ error: "Unauthorized" }, 401);
    try {
      const { results } = await env.DB.prepare(
        `SELECT id FROM posts WHERE deleted = 1 LIMIT 100`
      ).all();
      if (!results || results.length === 0) return json({ success: true, purged: 0 });
      const ids = results.map((p) => p.id);
      const placeholders = ids.map(() => "?").join(",");
      await env.DB.prepare(`DELETE FROM post_votes WHERE post_id IN (${placeholders})`).bind(...ids).run();
      await env.DB.prepare(`DELETE FROM comments WHERE post_id IN (${placeholders})`).bind(...ids).run();
      await env.DB.prepare(`DELETE FROM posts WHERE id IN (${placeholders})`).bind(...ids).run();
      return json({ success: true, purged: ids.length });
    } catch (err) {
      return serverError(err);
    }
  }
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
        if (!post || postBoard !== "cage" && postBoard !== "the cage") return json({ error: "Caged" }, 403);
      }
      const parentCommentId = typeof body.parent_comment_id === "string" && body.parent_comment_id.trim() ? body.parent_comment_id.trim() : null;
      const id = crypto.randomUUID();
      await env.DB.prepare(`
        INSERT INTO comments (id, content, post_id, parent_comment_id, username, ip_hash, browser_id,
          is_mod, is_admin, moderator, mod_user_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `).bind(
        id,
        body.content,
        body.post_id,
        parentCommentId,
        username,
        ip_hash,
        body.browser_id || null,
        isModerator ? 1 : 0,
        isAdmin ? 1 : 0,
        isModerator ? 1 : 0,
        isModerator ? authUser.sub ?? null : null,
        now
      ).run();
      await bumpPost(body.post_id);
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
  if (url.pathname === "/invite-to-huddle") {
    try {
      if (!username) return signInRequired();
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
      const settle = /* @__PURE__ */ __name((st) => env.DB.prepare(`UPDATE huddle_requests SET status = ?, decided_at = ? WHERE id = ?`).bind(st, now, rq.id).run(), "settle");
      if (!post || !post.is_huddle) {
        await settle("expired");
        return json({ error: "This huddle doesn't exist anymore", status: "expired" }, 410);
      }
      if (post.frozen) return json({ error: "This huddle is archived" }, 403);
      if (rq.created_at < requestCutoff()) {
        await settle("expired");
        return json({ error: "This request expired", status: "expired" }, 410);
      }
      const yes = body.accept === true, title = post.title || "Huddle";
      const tell = /* @__PURE__ */ __name((who, text) => who && who.toLowerCase() !== me ? upsertNotif(who, JSON.stringify({ text, postId: post.id }), post.id) : null, "tell");
      let status;
      if (rq.kind === "invite") {
        if (yes) {
          if (!isHuddleMember(post, rq.target)) {
            const members = JSON.parse(post.huddle_members || "[]");
            members.push(rq.target_role ? `${rq.target}:${rq.target_role}` : rq.target);
            await env.DB.prepare(`UPDATE posts SET huddle_members = ?, last_activity = ? WHERE id = ?`).bind(JSON.stringify(members), now, post.id).run();
          }
          await huddleLine(post.id, `\u{1F44B} ${rq.target} joined the huddle`, now);
          await tell(rq.from_user, `${rq.target} accepted your invite to "${title}"`);
          if (owner !== rq.from_user.toLowerCase()) await tell(post.username, `${rq.target} joined "${title}"`);
          status = "accepted";
        } else {
          await huddleLine(post.id, `\u{1F6AB} ${rq.target} declined the invite`, now);
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
          const rest = members.filter((m) => normMember(m).toLowerCase() !== rq.target.toLowerCase());
          if (rest.length !== members.length) {
            await env.DB.prepare(`UPDATE posts SET huddle_members = ? WHERE id = ?`).bind(JSON.stringify(rest), post.id).run();
            await huddleLine(post.id, `\u{1F4A8} ${rq.target} was removed from the huddle`, now);
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
      return serverError(err);
    }
  }
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
        await huddleLine(post_id, `\u{1F44B} ${leavingUser} left the huddle`, now);
        const next = await passHuddleOn(post, now);
        return json({ success: true, deleted: !next });
      }
      const members = JSON.parse(post.huddle_members || "[]");
      const newMembers = members.filter((m) => normMember(m).toLowerCase() !== leavingUser.toLowerCase());
      if (newMembers.length === members.length) {
        return json({ error: "Not a member of this huddle" }, 403);
      }
      await env.DB.prepare(`UPDATE posts SET huddle_members = ? WHERE id = ?`).bind(JSON.stringify(newMembers), post_id).run();
      await env.DB.prepare(`INSERT INTO comments (id, content, post_id, parent_comment_id, username, ip_hash, browser_id, is_mod, is_admin, moderator, mod_user_id, created_at) VALUES (?, ?, ?, NULL, '__system__', NULL, NULL, 0, 0, 0, NULL, ?)`).bind(crypto.randomUUID(), `\u{1F44B} ${leavingUser} left the huddle`, post_id, now).run().catch(() => {
      });
      const leaveTitle = post.title || "Huddle";
      const remaining = [...newMembers.map(normMember), post.username].filter(Boolean);
      for (const mu of remaining) {
        if (!mu || mu === leavingUser) continue;
        const leaveMsg = JSON.stringify({ text: `${leavingUser} left "${leaveTitle}"`, postId: post_id });
        await upsertNotif(mu, leaveMsg, post_id);
      }
      await upsertNotif(leavingUser, JSON.stringify({ text: `You left "${leaveTitle}"`, postId: post_id }), post_id);
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }
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
      const targetMember = members.find((m) => normMember(m).toLowerCase() === remove_username.toLowerCase());
      if (!targetMember) return json({ error: "Not a member" }, 404);
      if (!isCreator && !isModerator) {
        if (!isHuddleMember(post, effectiveUsername)) return json({ error: "Unauthorized" }, 403);
        const target = normMember(targetMember);
        if (target.toLowerCase() === effectiveUsername.toLowerCase()) return json({ error: "Use Leave to leave the huddle" }, 400);
        const r = targetMember.slice(targetMember.lastIndexOf(":") + 1);
        if (targetMember.includes(":") && (r === "admin" || r === "mod")) return json({ error: "Cannot remove mods or admins" }, 403);
        if (await pendingRequest(post_id, "remove", target)) return json({ error: `Someone already asked to remove ${target}` }, 400);
        await newRequest(post, "remove", effectiveUsername, target, null);
        return json({ success: true, pending: true, kind: "remove", message: `Asked ${post.username} to remove ${target}` });
      }
      if (isCreator && !isModerator) {
        const lastColon = targetMember.lastIndexOf(":");
        const targetRole = lastColon > 0 ? targetMember.slice(lastColon + 1) : null;
        if (targetRole === "admin" || targetRole === "mod") return json({ error: "Cannot remove mods or admins" }, 403);
      }
      const newMembers = members.filter((m) => normMember(m).toLowerCase() !== remove_username.toLowerCase());
      await env.DB.prepare(`UPDATE posts SET huddle_members = ? WHERE id = ?`).bind(JSON.stringify(newMembers), post_id).run();
      const sysContent = `\u{1F4A8} ${remove_username} was removed from the huddle`;
      const sysId = crypto.randomUUID();
      await env.DB.prepare(`INSERT INTO comments (id, content, post_id, parent_comment_id, username, ip_hash, browser_id, is_mod, is_admin, moderator, mod_user_id, created_at) VALUES (?, ?, ?, NULL, '__system__', NULL, NULL, 0, 0, 0, NULL, ?)`).bind(sysId, sysContent, post_id, now).run().catch(() => {
      });
      const huddleTitle = post.title || "Huddle";
      await upsertNotif(remove_username, JSON.stringify({ text: `You were removed from "${huddleTitle}"`, postId: post_id }), post_id);
      const remaining = [...newMembers.map(normMember), post.username].filter(Boolean);
      for (const mu of remaining) {
        if (!mu || mu === effectiveUsername || mu === remove_username) continue;
        await upsertNotif(mu, JSON.stringify({ text: `${effectiveUsername} removed ${remove_username} from "${huddleTitle}"`, postId: post_id }), post_id);
      }
      await upsertNotif(effectiveUsername, JSON.stringify({ text: `You removed ${remove_username} from "${huddleTitle}"`, postId: post_id }), post_id);
      const updatedPost = { ...post, huddle_members: JSON.stringify(newMembers) };
      return json({ success: true, post: boolify(updatedPost, POST_BOOL_FIELDS), systemComment: { id: sysId, content: sysContent, username: "__system__", created_at: now, parent_comment_id: null, browser_id: null, is_mod: 0 } });
    } catch (err) {
      return serverError(err);
    }
  }
  if (url.pathname === "/pin-huddle-comment") {
    try {
      if (!username) return signInRequired();
      const { post_id, comment_id, pinned } = body;
      if (!post_id || !comment_id || pinned === void 0) return json({ error: "Missing fields" }, 400);
      const effectiveUsername = username;
      const post = await env.DB.prepare(`SELECT * FROM posts WHERE id = ? AND deleted = 0`).bind(post_id).first();
      if (!post) return json({ error: "Post not found" }, 404);
      if (post.frozen) return json({ error: "This post is archived" }, 403);
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
  if (url.pathname === "/vote-post") {
    if (!username) return signInRequired();
    try {
      if (!body.post_id || !body.browser_id || ![1, 0].includes(body.value))
        return json({ error: "Missing or invalid fields" }, 400);
      if (await isBanned()) return json({ error: "Banned" }, 403);
      const votedPost = await env.DB.prepare(`SELECT frozen FROM posts WHERE id = ?`).bind(body.post_id).first();
      if (votedPost?.frozen) return json({ error: "This post is archived" }, 403);
      const [existing, preSummary] = await Promise.all([
        // Your vote is found by your account, never by a device id the request sends (those are visible on posts)
        env.DB.prepare(`SELECT id, value FROM post_votes WHERE post_id = ? AND username = ?`).bind(body.post_id, username).first(),
        getPostVoteSummary(body.post_id, body.browser_id)
      ]);
      const prevValue = existing?.value || 0;
      const prevScore = preSummary.score;
      const prevCount = preSummary.voteCount;
      if (body.value === 0) {
        if (existing?.id) {
          await env.DB.prepare(`DELETE FROM post_votes WHERE id = ?`).bind(existing.id).run();
        }
        const newScore2 = prevScore - prevValue;
        const newCount2 = existing?.id ? prevCount - 1 : prevCount;
        return json({ success: true, score: newScore2, myVote: 0, voteCount: newCount2 });
      }
      if (existing?.id) {
        await env.DB.prepare(`UPDATE post_votes SET value = ?, username = ?, ip_hash = NULL, is_mod = ?, mod_user_id = ? WHERE id = ?`).bind(body.value, username, isModerator ? 1 : 0, isModerator ? authUser.sub : null, existing.id).run();
      } else {
        await env.DB.prepare(`
          INSERT INTO post_votes (id, post_id, browser_id, value, username, ip_hash, is_mod, mod_user_id, created_at)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        `).bind(
          crypto.randomUUID(),
          body.post_id,
          body.browser_id,
          body.value,
          username,
          null,
          isModerator ? 1 : 0,
          isModerator ? authUser.sub : null,
          now
        ).run();
      }
      await bumpPost(body.post_id);
      const newScore = prevScore - prevValue + body.value;
      const newCount = existing?.id ? prevCount : prevCount + 1;
      return json({ success: true, score: newScore, myVote: body.value, voteCount: newCount });
    } catch (err) {
      return serverError(err);
    }
  }
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
  if (url.pathname === "/react-comment") {
    try {
      if (!username) return signInRequired();
      if (!body.comment_id || !body.browser_id || !body.emoji) return json({ error: "Missing fields" }, 400);
      const em = String(body.emoji);
      if (em.length > 32 || !/\p{Extended_Pictographic}|\p{Regional_Indicator}|⃣/u.test(em) || /[\p{L}\s<>]/u.test(em) || /\p{N}/u.test(em.replace(/[0-9#*]️?⃣/gu, ""))) {
        return json({ error: "Not an emoji" }, 400);
      }
      if (await isBanned()) return json({ error: "Banned" }, 403);
      const reactedPost = await env.DB.prepare(`SELECT p.frozen FROM comments c JOIN posts p ON p.id = c.post_id WHERE c.id = ?`).bind(body.comment_id).first();
      if (reactedPost?.frozen) return json({ error: "This post is archived" }, 403);
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
      return serverError(err);
    }
  }
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
  if (url.pathname === "/purge-member" && request.method === "POST") {
    if (!isAdmin) return json({ error: "Unauthorized" }, 401);
    try {
      const account = await env.DB.prepare(`SELECT id, username FROM mod_users WHERE id = ? AND deleted_at IS NOT NULL AND purged_at IS NULL`).bind(body.user_id || "").first();
      if (!account) return json({ error: "Not in the Trash" }, 404);
      await env.DB.prepare(`UPDATE mod_users SET purged_at = ?, password_hash = '', email = ?, left_huddles = NULL WHERE id = ?`).bind(now, `retired-${account.id}@users.local`, account.id).run();
      if (account.username) await env.DB.prepare(`DELETE FROM system_notifications WHERE user_id = ?`).bind(account.username).run();
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }
  if (url.pathname === "/get-members") {
    if (!isModerator) return json({ error: "Unauthorized" }, 401);
    try {
      const { results } = await env.DB.prepare(`
        SELECT m.id, m.email, m.username, m.role, m.created_at, m.last_active, m.deleted_at, m.failed_logins, m.locked_until,
          (SELECT p.ip_hash FROM posts p WHERE p.username = m.username AND p.ip_hash IS NOT NULL ORDER BY p.created_at DESC LIMIT 1) as ip_hash,
          (SELECT p.browser_id FROM posts p WHERE p.username = m.username AND p.browser_id IS NOT NULL ORDER BY p.created_at DESC LIMIT 1) as browser_id,
          COALESCE((SELECT COUNT(*) FROM post_votes pv JOIN posts p ON pv.post_id = p.id WHERE p.username = m.username AND pv.value > 0 AND p.deleted = 0 AND (p.archived = 0 OR p.archived IS NULL)), 0)
          + COALESCE((SELECT COUNT(*) FROM comment_reactions cr JOIN comments c ON cr.comment_id = c.id WHERE c.username = m.username AND c.deleted = 0), 0) as worm_count
        FROM mod_users m WHERE m.deleted_at IS NULL ORDER BY m.last_active DESC, m.created_at DESC`).all();
      const members = (results || []).map((u) => ({
        id: u.id,
        email: u.email,
        created_at: u.created_at,
        last_active: u.last_active || null,
        worm_count: u.worm_count || 0,
        failed_logins: u.failed_logins || 0,
        locked_until: u.locked_until && u.locked_until > now ? u.locked_until : null,
        user_metadata: { username: u.username, role: u.role, ip_hash: u.ip_hash || null, browser_id: u.browser_id || null }
      }));
      return json({ members });
    } catch (err) {
      return serverError(err);
    }
  }
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
          await env.DB.prepare(`INSERT INTO system_notifications (id, user_id, message) VALUES (?, ?, ?)`).bind(notifId, user_id, notifMsg).run();
        }
      }
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }
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
  if (url.pathname === "/mod-action") {
    try {
      if (!isModerator) return json({ error: "Unauthorized" }, 401);
      if (!body.type) return json({ error: "Missing type" }, 400);
      const t = body.type;
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
        if (body.username) await env.DB.prepare(`DELETE FROM jailed WHERE username = ?`).bind(body.username).run();
        if (body.browser_id) await env.DB.prepare(`DELETE FROM jailed WHERE browser_id = ?`).bind(body.browser_id).run();
        if (body.ip_hash) await env.DB.prepare(`DELETE FROM jailed WHERE ip_hash = ?`).bind(body.ip_hash).run();
        await env.DB.prepare(`INSERT INTO bans (id, username, browser_id, ip_hash, created_at) VALUES (?, ?, ?, ?, ?)`).bind(crypto.randomUUID(), body.username || null, body.browser_id || null, body.ban_ip === true ? body.ip_hash || null : null, now).run();
      }
      if (t === "unban") {
        if (body.username) await env.DB.prepare(`DELETE FROM bans WHERE username = ?`).bind(body.username).run();
        if (body.browser_id) await env.DB.prepare(`DELETE FROM bans WHERE browser_id = ?`).bind(body.browser_id).run();
        if (body.ip_hash) await env.DB.prepare(`DELETE FROM bans WHERE ip_hash = ?`).bind(body.ip_hash).run();
      }
      if (t === "jail") {
        if (body.username) await env.DB.prepare(`DELETE FROM bans WHERE username = ?`).bind(body.username).run();
        if (body.browser_id) await env.DB.prepare(`DELETE FROM bans WHERE browser_id = ?`).bind(body.browser_id).run();
        if (body.ip_hash) await env.DB.prepare(`DELETE FROM bans WHERE ip_hash = ?`).bind(body.ip_hash).run();
        await env.DB.prepare(`INSERT OR IGNORE INTO jailed (id, browser_id, username, ip_hash, created_at) VALUES (?, ?, ?, ?, ?)`).bind(crypto.randomUUID(), body.browser_id || null, body.username || null, body.ip_hash || null, now).run();
      }
      if (t === "unjail") {
        if (body.username) await env.DB.prepare(`DELETE FROM jailed WHERE username = ?`).bind(body.username).run();
        if (body.browser_id) await env.DB.prepare(`DELETE FROM jailed WHERE browser_id = ?`).bind(body.browser_id).run();
        if (body.ip_hash) await env.DB.prepare(`DELETE FROM jailed WHERE ip_hash = ?`).bind(body.ip_hash).run();
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
        const _pdcIds = (_pdc.results || []).map((c) => c.id);
        if (_pdcIds.length) {
          await env.DB.prepare(`DELETE FROM comment_reactions WHERE comment_id IN (${ID_LIST})`).bind(JSON.stringify(_pdcIds)).run();
        }
        const _pdp = await env.DB.prepare(`SELECT content FROM posts WHERE id = ?`).bind(body.post_id).first();
        const _pdcc = await env.DB.prepare(`SELECT content FROM comments WHERE post_id = ?`).bind(body.post_id).all();
        const _mediaKeys = /* @__PURE__ */ new Set();
        for (const txt of [_pdp?.content, ...(_pdcc.results || []).map((r) => r.content)]) {
          for (const m of String(txt || "").matchAll(/\/media\/([A-Za-z0-9][A-Za-z0-9._-]*)/g)) {
            _mediaKeys.add(m[1]);
            _mediaKeys.add(`thumbs/${m[1]}.jpg`);
          }
        }
        await env.DB.prepare(`DELETE FROM post_votes WHERE post_id = ?`).bind(body.post_id).run();
        await env.DB.prepare(`DELETE FROM comments WHERE post_id = ?`).bind(body.post_id).run();
        await env.DB.prepare(`DELETE FROM posts WHERE id = ?`).bind(body.post_id).run();
        if (_mediaKeys.size) {
          await env.MEDIA.delete([..._mediaKeys]).catch((err) => console.error("media delete failed", err.message));
          if (env.MEDIA_SVC) await env.MEDIA_SVC.fetch("https://media/__purge", { method: "POST", body: JSON.stringify({ keys: [..._mediaKeys].filter((k) => !k.startsWith("thumbs/")) }) }).catch((err) => console.error("media cache purge failed", err.message));
        }
      }
      if (t === "delete_comment") {
        const _dc = await env.DB.prepare(`SELECT is_admin FROM comments WHERE id = ?`).bind(body.comment_id).first();
        if (_dc?.is_admin && !isAdmin) return json({ error: "Cannot delete an admin comment" }, 403);
        await env.DB.prepare(`UPDATE comments SET deleted = 1 WHERE id = ?`).bind(body.comment_id).run();
      }
      if (t === "pin_post") {
        await env.DB.prepare(`UPDATE posts SET pinned = ?, pinned_global = ? WHERE id = ?`).bind(body.pinned ? 1 : 0, body.pinned_global ? 1 : 0, body.post_id).run();
      }
      if (t === "pin_comment") {
        await env.DB.prepare(`UPDATE comments SET pinned = ? WHERE id = ?`).bind(body.pinned ? 1 : 0, body.comment_id).run();
      }
      if (t === "lock_post") {
        await env.DB.prepare(`UPDATE posts SET locked = ? WHERE id = ?`).bind(body.locked ? 1 : 0, body.post_id).run();
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
  if (url.pathname === "/get-mod-data") {
    if (!isModerator) return json({ error: "Unauthorized" }, 401);
    try {
      const [postsRes, commentsRes, bansRes, jailedRes, deletedRes, archivedRes] = await Promise.all([
        env.DB.prepare(`SELECT * FROM posts WHERE deleted = 0 AND (archived = 0 OR archived IS NULL) ORDER BY created_at DESC LIMIT 500`).all(),
        env.DB.prepare(`SELECT * FROM comments WHERE deleted = 0 ORDER BY created_at DESC LIMIT 1000`).all(),
        env.DB.prepare(`SELECT * FROM bans ORDER BY created_at DESC`).all(),
        env.DB.prepare(`SELECT * FROM jailed ORDER BY created_at DESC`).all(),
        env.DB.prepare(`SELECT id, title, board, username, browser_id, created_at, content, is_admin FROM posts WHERE deleted = 1 ORDER BY created_at DESC LIMIT 100`).all(),
        env.DB.prepare(`SELECT id, title, board, username, browser_id, created_at, content, archived, frozen, is_admin FROM posts WHERE frozen = 1 AND deleted = 0 ORDER BY created_at DESC LIMIT 100`).all()
      ]);
      return json({
        posts: (postsRes.results || []).map((p) => boolify(p, POST_BOOL_FIELDS)),
        comments: (commentsRes.results || []).map((c) => boolify(c, COMMENT_BOOL_FIELDS)),
        bans: bansRes.results || [],
        jailed: jailedRes.results || [],
        deletedPosts: deletedRes.results || [],
        archivedPosts: archivedRes.results || []
      });
    } catch (err) {
      return serverError(err);
    }
  }
  if (url.pathname === "/check-jailed") {
    try {
      const bid = (url.searchParams.get("browser_id") || body.browser_id || "").trim();
      const uname = (url.searchParams.get("username") || "").trim();
      if (!bid && !uname) return json({ jailed: false });
      const conditions = [];
      const params = [];
      if (bid) {
        conditions.push("browser_id = ?");
        params.push(bid);
      }
      if (uname) {
        conditions.push("username = ?");
        params.push(uname);
      }
      const row = await env.DB.prepare(
        `SELECT 1 FROM jailed WHERE ${conditions.join(" OR ")} LIMIT 1`
      ).bind(...params).first();
      return json({ jailed: !!row });
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
  if (url.pathname === "/user-stats") {
    try {
      const browser_id = url.searchParams.get("browser_id") || "";
      const mod_user_id = url.searchParams.get("mod_user_id") || null;
      const uname = url.searchParams.get("username") || null;
      if (uname && (uname === EXTINCT_NAME || (await extinctNames()).has(uname))) return json({ joined_at: null, worm_count: 0, extinct: true });
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
      let worm_count = 0;
      let postIds = [], commentIds = [];
      if (mod_user_id) {
        const { results: mp } = await env.DB.prepare(`SELECT id FROM posts WHERE mod_user_id = ? AND deleted = 0 AND (archived = 0 OR archived IS NULL)`).bind(mod_user_id).all();
        const { results: mc } = await env.DB.prepare(`SELECT id FROM comments WHERE mod_user_id = ? AND deleted = 0`).bind(mod_user_id).all();
        postIds = (mp || []).map((p) => p.id);
        commentIds = (mc || []).map((c) => c.id);
      } else if (uname) {
        const { results: mp } = await env.DB.prepare(`SELECT id FROM posts WHERE username = ? AND deleted = 0 AND (archived = 0 OR archived IS NULL)`).bind(uname).all();
        const { results: mc } = await env.DB.prepare(`SELECT id FROM comments WHERE username = ? AND deleted = 0`).bind(uname).all();
        postIds = (mp || []).map((p) => p.id);
        commentIds = (mc || []).map((c) => c.id);
      } else if (browser_id) {
        const { results: mp } = await env.DB.prepare(`SELECT id FROM posts WHERE browser_id = ? AND deleted = 0 AND (archived = 0 OR archived IS NULL)`).bind(browser_id).all();
        const { results: mc } = await env.DB.prepare(`SELECT id FROM comments WHERE browser_id = ? AND deleted = 0`).bind(browser_id).all();
        postIds = (mp || []).map((p) => p.id);
        commentIds = (mc || []).map((c) => c.id);
      }
      if (postIds.length) {
        const ph = ID_LIST;
        const r = await env.DB.prepare(`SELECT COUNT(*) as c FROM post_votes WHERE post_id IN (${ph}) AND value > 0`).bind(JSON.stringify(postIds)).first();
        worm_count += r?.c || 0;
      }
      if (commentIds.length) {
        const ph = ID_LIST;
        const r = await env.DB.prepare(`SELECT COUNT(*) as c FROM comment_reactions WHERE comment_id IN (${ph})`).bind(JSON.stringify(commentIds)).first();
        worm_count += r?.c || 0;
      }
      const modRow = uname ? await env.DB.prepare(`SELECT role FROM mod_users WHERE username = ?`).bind(uname).first() : null;
      const role = modRow?.role || null;
      return json({ joined_at, worm_count, role });
    } catch (err) {
      return serverError(err);
    }
  }
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
      const placeholders = convs.map(() => "?").join(",");
      const { results: roles } = await env.DB.prepare(
        `SELECT username, role FROM mod_users WHERE username IN (${placeholders})`
      ).bind(...convs.map((c) => c.contact)).all();
      const roleMap = Object.fromEntries((roles || []).map((r) => [r.username, r.role]));
      convs.forEach((c) => {
        c.is_admin = roleMap[c.contact] === "admin";
        c.is_mod = roleMap[c.contact] === "mod";
      });
    }
    return json({ conversations: convs });
  }
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
      const senders = [...new Set(msgs.map((m) => m.from_username))];
      if (senders.length) {
        const sph = senders.map(() => "?").join(",");
        const { results: roles } = await env.DB.prepare(
          `SELECT username, role FROM mod_users WHERE username IN (${sph})`
        ).bind(...senders).all();
        const roleMap = Object.fromEntries((roles || []).map((r) => [r.username, r.role]));
        msgs.forEach((m) => {
          m.is_admin = roleMap[m.from_username] === "admin";
          m.is_mod = roleMap[m.from_username] === "mod";
        });
      }
      const msgIds = msgs.map((m) => m.id);
      const ph = msgIds.map(() => "?").join(",");
      const { results: rxs } = await env.DB.prepare(
        `SELECT message_id, from_username, emoji FROM dm_reactions WHERE message_id IN (${ph})`
      ).bind(...msgIds).all();
      const rxMap = {};
      (rxs || []).forEach((r) => {
        if (!rxMap[r.message_id]) rxMap[r.message_id] = [];
        rxMap[r.message_id].push({ from_username: r.from_username, emoji: r.emoji });
      });
      msgs.forEach((m) => {
        m.reactions = rxMap[m.id] || [];
      });
      const replyIds = msgs.filter((m) => m.reply_to_id).map((m) => m.reply_to_id);
      if (replyIds.length) {
        const rph = replyIds.map(() => "?").join(",");
        const { results: rmsgs } = await env.DB.prepare(
          `SELECT id, from_username, content FROM private_messages WHERE id IN (${rph})`
        ).bind(...replyIds).all();
        const replyMap = Object.fromEntries((rmsgs || []).map((r) => [r.id, r]));
        msgs.forEach((m) => {
          if (m.reply_to_id) m.reply_to = replyMap[m.reply_to_id] || null;
        });
      }
    }
    await env.DB.prepare(`UPDATE private_messages SET read_at=? WHERE to_username=? AND from_username=? AND read_at IS NULL`).bind(now, me, withUser).run();
    return json({ messages: msgs });
  }
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
  if (url.pathname === "/delete-dm") {
    if (!authUser?.username) return json({ error: "Unauthorized" }, 401);
    const { message_id } = body;
    if (!message_id) return json({ error: "Missing message_id" }, 400);
    await env.DB.prepare(
      `DELETE FROM private_messages WHERE id=? AND from_username=?`
    ).bind(message_id, authUser.username).run();
    return json({ success: true });
  }
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
  if (url.pathname === "/clear-notifications") {
    try {
      const clearUserId = authUser?.username || null;
      if (!clearUserId) return signInRequired();
      const keep = await waitingOn(clearUserId);
      await env.DB.prepare(`DELETE FROM system_notifications WHERE user_id = ? AND message != '__cleared__' AND id NOT IN (${ID_LIST})`).bind(clearUserId, JSON.stringify(keep)).run();
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
  const buildNotifs = /* @__PURE__ */ __name(async (browser_id) => {
    const me = authUser.username;
    const mod_user_id = isModerator ? authUser.sub : null;
    const uname = isModerator ? null : authUser.username;
    const notifUserId = authUser?.username || mod_user_id || null;
    let clearedSince = (/* @__PURE__ */ new Date(0)).toISOString();
    if (notifUserId) {
      const wm = await env.DB.prepare(`SELECT created_at FROM system_notifications WHERE user_id = ? AND message = '__cleared__' LIMIT 1`).bind(notifUserId).first();
      if (wm) clearedSince = wm.created_at;
    }
    let postIds = [], commentIds = [], postTitleMap = {}, commentPostMap = {};
    if (mod_user_id) {
      const { results: mp } = await env.DB.prepare(`SELECT id, title FROM posts WHERE mod_user_id = ? AND deleted = 0`).bind(mod_user_id).all();
      const { results: mc } = await env.DB.prepare(`SELECT id, post_id FROM comments WHERE mod_user_id = ? AND deleted = 0`).bind(mod_user_id).all();
      postIds = (mp || []).map((p) => p.id);
      (mp || []).forEach((p) => postTitleMap[p.id] = p.title);
      commentIds = (mc || []).map((c) => c.id);
      (mc || []).forEach((c) => commentPostMap[c.id] = c.post_id);
    } else if (uname) {
      const { results: mp } = await env.DB.prepare(`SELECT id, title FROM posts WHERE username = ? AND is_mod = 0 AND deleted = 0 AND (is_huddle = 0 OR is_huddle IS NULL)`).bind(uname).all();
      const { results: mc } = await env.DB.prepare(`SELECT id, post_id FROM comments WHERE username = ? AND is_mod = 0 AND deleted = 0`).bind(uname).all();
      postIds = (mp || []).map((p) => p.id);
      (mp || []).forEach((p) => postTitleMap[p.id] = p.title);
      commentIds = (mc || []).map((c) => c.id);
      (mc || []).forEach((c) => commentPostMap[c.id] = c.post_id);
    }
    const results = [];
    if (postIds.length) {
      const ph = ID_LIST;
      const { results: comments } = await env.DB.prepare(
        `SELECT id, content, username, browser_id, post_id, MAX(created_at) as created_at FROM comments WHERE post_id IN (${ph}) AND browser_id != ? AND (username IS NULL OR username != ?) AND deleted = 0 AND parent_comment_id IS NULL AND created_at > ? GROUP BY post_id ORDER BY created_at DESC LIMIT 60`
      ).bind(JSON.stringify(postIds), browser_id, me, clearedSince).all();
      (comments || []).forEach((c) => results.push({ id: `c-${c.post_id}`, type: "comment", icon: "\u{1F4AC}", text: `${c.username || "Someone"} commented on your post`, subtext: `"${(postTitleMap[c.post_id] || "").slice(0, 50)}"`, preview: (c.content || "").slice(0, 80), time: c.created_at, postId: c.post_id, targetId: c.id }));
      const { results: votes } = await env.DB.prepare(
        `SELECT post_id, value, browser_id, username, created_at FROM post_votes WHERE post_id IN (${ph}) AND browser_id != ? AND (username IS NULL OR username != ?) AND created_at > ? ORDER BY created_at DESC LIMIT 60`
      ).bind(JSON.stringify(postIds), browser_id, me, clearedSince).all();
      (votes || []).forEach((v, i) => {
        const who = v.username || `Anon`;
        results.push({ id: `v-${v.post_id}-${v.browser_id}`, type: "vote", icon: "\u{1FABD}", text: `${who} gave your post a flap`, subtext: `"${(postTitleMap[v.post_id] || "").slice(0, 50)}"`, time: v.created_at, postId: v.post_id });
      });
    }
    if (commentIds.length) {
      const ph = ID_LIST;
      const { results: replies } = await env.DB.prepare(
        `SELECT id, content, username, browser_id, post_id, parent_comment_id, MAX(created_at) as created_at FROM comments WHERE parent_comment_id IN (${ph}) AND browser_id != ? AND (username IS NULL OR username != ?) AND deleted = 0 AND created_at > ? GROUP BY parent_comment_id ORDER BY created_at DESC LIMIT 60`
      ).bind(JSON.stringify(commentIds), browser_id, me, clearedSince).all();
      (replies || []).forEach((r) => results.push({ id: `r-${r.parent_comment_id}`, type: "reply", icon: "\u21A9\uFE0F", text: `${r.username || "Someone"} replied to your comment`, preview: (r.content || "").slice(0, 80), time: r.created_at, postId: r.post_id, targetId: r.id }));
      const { results: reactions } = await env.DB.prepare(
        `SELECT comment_id, emoji, browser_id, username, created_at FROM comment_reactions WHERE comment_id IN (${ph}) AND browser_id != ? AND (username IS NULL OR username != ?) AND created_at > ? ORDER BY created_at DESC LIMIT 60`
      ).bind(JSON.stringify(commentIds), browser_id, me, clearedSince).all();
      (reactions || []).forEach((r, i) => {
        const who = r.username || `Anon`;
        results.push({ id: `rx-${r.comment_id}-${r.browser_id}-${r.emoji}`, type: "reaction", icon: r.emoji, text: `${who} reacted ${r.emoji} to your comment`, time: r.created_at, postId: commentPostMap[r.comment_id], targetId: r.comment_id });
      });
    }
    if (mod_user_id) {
      const { results: sysN } = await env.DB.prepare(
        `SELECT id, message, created_at FROM system_notifications WHERE user_id = ? AND message != '__cleared__' AND created_at > ? ORDER BY created_at DESC LIMIT 20`
      ).bind(mod_user_id, clearedSince).all();
      (sysN || []).forEach((n) => results.push({ id: `sys-${n.id}`, type: "system", icon: "\u{1F514}", text: n.message, time: n.created_at }));
    }
    const notifUname = uname || authUser?.username || null;
    if (notifUname) {
      const { results: huddleN } = await env.DB.prepare(
        `SELECT id, message, created_at FROM system_notifications WHERE user_id = ? AND message != '__cleared__' AND created_at > ? ORDER BY created_at DESC LIMIT 30`
      ).bind(notifUname, clearedSince).all();
      const { results: reqN = [] } = await env.DB.prepare(
        `SELECT id, message, created_at FROM system_notifications WHERE user_id = ? AND message LIKE '%"req":"%' ORDER BY created_at DESC LIMIT 40`
      ).bind(notifUname).all();
      const seenRows = new Set((huddleN || []).map((n) => n.id));
      for (const n of reqN) if (!seenRows.has(n.id)) {
        n.preClear = n.created_at <= clearedSince;
        huddleN.push(n);
      }
      const reqIds = [];
      (huddleN || []).forEach((n) => {
        let text = n.message, postId = void 0, req = void 0;
        let preview, icon;
        try {
          const parsed = JSON.parse(n.message);
          text = parsed.text || text;
          postId = parsed.postId;
          req = parsed.req;
          preview = parsed.preview;
          icon = parsed.icon;
        } catch {
        }
        if (req) reqIds.push(req);
        results.push({ id: `hsys-${n.id}`, type: "system", icon: icon || (req ? "\u{1F4E8}" : "\u{1F465}"), text, postId, time: n.created_at, req, preview, preClear: n.preClear || void 0 });
      });
      if (reqIds.length) {
        const { results: rqs = [] } = await env.DB.prepare(
          `SELECT r.id, r.kind, r.status, r.target, r.created_at, p.username AS owner, p.deleted AS gone FROM huddle_requests r LEFT JOIN posts p ON p.id = r.post_id WHERE r.id IN (${ID_LIST})`
        ).bind(JSON.stringify(reqIds)).all();
        const byId = new Map(rqs.map((r) => [r.id, r])), cut = requestCutoff(), lower = me.toLowerCase();
        for (const n of results) {
          if (!n.req) continue;
          const r = byId.get(n.req);
          if (!r) {
            delete n.req;
            continue;
          }
          const status = r.status === "pending" && (r.created_at < cut || r.gone || r.owner == null) ? "expired" : r.status;
          const act = r.kind === "invite" ? r.target.toLowerCase() === lower : (r.owner || "").toLowerCase() === lower;
          n.req = { id: r.id, kind: r.kind, status, act: status === "pending" && act };
          if (n.req.act) n.need = true;
        }
      }
      for (let i = results.length - 1; i >= 0; i--) {
        if (results[i].preClear && !results[i].need) results.splice(i, 1);
        else delete results[i].preClear;
      }
    }
    results.sort((a, b) => a.time && b.time ? new Date(b.time) - new Date(a.time) : a.time ? -1 : 1);
    const names = await extinctNames();
    const { results: hiddenPosts } = await env.DB.prepare(`SELECT id FROM posts INDEXED BY idx_posts_frozen_list WHERE frozen = 1 AND deleted = 0 AND archived = 1`).all();
    const hidden = new Set(isModerator ? [] : (hiddenPosts || []).map((p) => p.id));
    return results.filter((n) => !hidden.has(n.postId)).map((n) => Object.fromEntries(Object.entries(n).map(([k, v]) => [k, scrubNames(v, names)])));
  }, "buildNotifs");
  if (url.pathname === "/notifications") {
    try {
      const browser_id = url.searchParams.get("browser_id") || "";
      if (!authUser?.username) return signInRequired();
      return json({ notifs: await buildNotifs(browser_id) });
    } catch (err) {
      return serverError(err);
    }
  }
  if (url.pathname === "/admin-huddle-view") {
    if (!isAdmin) return json({ error: "Unauthorized" }, 403);
    if (request.method === "POST") {
      const on = body.on === true ? 1 : 0;
      await env.DB.prepare(`UPDATE mod_users SET see_all_huddles = ? WHERE id = ?`).bind(on, authUser.sub).run();
      return json({ on: !!on });
    }
    return json({ on: !!authUser.see_all_huddles });
  }
  if (url.pathname === "/huddle-read" && request.method === "POST") {
    if (!authUser?.username) return signInRequired();
    const postId = String(body.post_id || "").slice(0, 80), at = String(body.at || "");
    if (!postId || !/^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}/.test(at)) return json({ error: "Bad request" }, 400);
    const post = await env.DB.prepare(`SELECT id, username, huddle_members, is_huddle FROM posts WHERE id = ?`).bind(postId).first();
    if (!post || !post.is_huddle || !seeAllHuddles && !isHuddleMember(post, authUser.username)) return json({ error: "Not found" }, 404);
    const t = at > now ? now : at.slice(0, 40);
    await env.DB.prepare(`INSERT INTO huddle_reads (username, post_id, read_at) VALUES (?, ?, ?) ON CONFLICT(username, post_id) DO UPDATE SET read_at = MAX(read_at, excluded.read_at)`).bind(authUser.username.toLowerCase(), postId, t).run();
    return json({ success: true });
  }
  if (url.pathname === "/notif-read" && request.method === "POST") {
    if (!authUser?.username) return signInRequired();
    const id = String(body.id || "").slice(0, 200), t = String(body.time || now).slice(0, 40);
    if (!id) return json({ error: "Missing id" }, 400);
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
      const nk = authUser.username;
      let since = url.searchParams.get("since") || (/* @__PURE__ */ new Date(0)).toISOString();
      const nst = await env.DB.prepare(`SELECT seen_at FROM notif_state WHERE user_key = ?`).bind(nk).first();
      if (nst) since = nst.seen_at;
      else await env.DB.prepare(`INSERT OR IGNORE INTO notif_state (user_key, seen_at) VALUES (?, ?)`).bind(nk, since).run();
      const list = await buildNotifs(browser_id);
      const { results: rd = [] } = await env.DB.prepare(`SELECT notif_id, notif_time FROM notif_reads WHERE user_key = ? ORDER BY notif_time DESC LIMIT 500`).bind(nk).all();
      const readAt = new Map(rd.map((r) => [r.notif_id, new Date(r.notif_time).getTime() || 0])), sinceMs = new Date(since).getTime();
      const isRead = /* @__PURE__ */ __name((n) => readAt.has(n.id) && readAt.get(n.id) >= (new Date(n.time).getTime() || 0), "isRead");
      const count = list.filter((n) => n.need || n.time && new Date(n.time).getTime() > sinceMs && !isRead(n)).length;
      return json({ count, seen_at: since, read: list.filter(isRead).map((n) => n.id) });
    } catch (err) {
      return serverError(err);
    }
  }
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
  if (url.pathname === "/backfill-username") {
    try {
      return json({ success: true });
    } catch (err) {
      return serverError(err);
    }
  }
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
  if (url.pathname === "/bot-seen") {
    if (!isBot) return json({ error: "Unauthorized" }, 401);
    if (request.method === "GET") {
      const row = await env.DB.prepare(`SELECT urls, last_run FROM bot_seen WHERE id = 1`).first();
      try {
        return json({ seen: row?.urls ? JSON.parse(row.urls) : [], last_run: row?.last_run || null });
      } catch {
        return json({ seen: [], last_run: null });
      }
    }
    if (request.method === "POST") {
      if (!Array.isArray(body.seen)) return json({ error: "Missing seen array" }, 400);
      const expectedLastRun = body.expected_last_run || null;
      try {
        let result;
        if (expectedLastRun) {
          result = await env.DB.prepare(
            `UPDATE bot_seen SET urls = ?, last_run = ?, updated_at = ? WHERE id = 1 AND last_run = ?`
          ).bind(JSON.stringify(body.seen.slice(-5e3)), body.last_run || now, now, expectedLastRun).run();
        } else {
          result = await env.DB.prepare(
            `UPDATE bot_seen SET urls = ?, last_run = ?, updated_at = ? WHERE id = 1 AND last_run IS NULL`
          ).bind(JSON.stringify(body.seen.slice(-5e3)), body.last_run || now, now).run();
        }
        if (result.meta.changes === 0) return json({ success: false, reason: "stale" }, 409);
        return json({ success: true });
      } catch (err) {
        return serverError(err);
      }
    }
  }
  if (url.pathname === "/bot-logs") {
    if (!isAdmin && !isBot) return json({ error: "Unauthorized" }, 401);
    const { results } = await env.DB.prepare(
      `SELECT * FROM bot_logs ORDER BY started_at DESC`
    ).all();
    const logs = (results || []).map((r) => ({
      ...r,
      posted_articles: (() => {
        try {
          return JSON.parse(r.posted_articles);
        } catch {
          return [];
        }
      })(),
      feed_errors: (() => {
        try {
          return JSON.parse(r.feed_errors);
        } catch {
          return [];
        }
      })()
    }));
    return json({ logs });
  }
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
    let pa = [];
    try {
      pa = JSON.parse(row.posted_articles);
    } catch {
    }
    let fe = [];
    try {
      fe = JSON.parse(row.feed_errors);
    } catch {
    }
    const dur = row.finished_at ? Math.round((new Date(row.finished_at) - new Date(row.started_at)) / 1e3) + "s" : "still running";
    const sep = "\u2500".repeat(60);
    let text = `BOT DEPLOYMENT LOG
${"=".repeat(60)}
`;
    text += `ID:          ${row.id}
`;
    text += `Status:      ${row.status}
`;
    text += `Run type:    ${row.run_type || "manual"}
`;
    text += `Started:     ${row.started_at}
`;
    text += `Finished:    ${row.finished_at || "(still running)"}
`;
    text += `Duration:    ${dur}

`;
    text += `STATS
${sep}
`;
    text += `Posted:      ${row.posted}
`;
    text += `Skipped:     ${row.skipped_seen} (seen before)
`;
    text += `Bad titles:  ${row.skipped_bad_title}
`;
    text += `Failed:      ${row.post_failed}
`;
    text += `Feed errors: ${fe.length}

`;
    if (pa.length > 0) {
      text += `POSTED ARTICLES (${pa.length})
${sep}
`;
      pa.forEach((a, i) => {
        const line = typeof a === "string" ? a : a.url || a.title || a.link || JSON.stringify(a);
        text += `${i + 1}. ${line}
`;
      });
      text += "\n";
    }
    if (fe.length > 0) {
      text += `FEED ERRORS (${fe.length})
${sep}
`;
      fe.forEach((e, i) => {
        text += `${i + 1}. ${typeof e === "string" ? e : JSON.stringify(e)}
`;
      });
      text += "\n";
    }
    text += `RAW JSON
${sep}
`;
    text += JSON.stringify({ ...row, posted_articles: pa, feed_errors: fe }, null, 2);
    return new Response(text, {
      headers: { ...corsHeaders, "Content-Type": "text/plain; charset=utf-8" }
    });
  }
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
  if (url.pathname === "/bot-log-expire") {
    if (!isBot && !isAdmin) return json({ error: "Unauthorized" }, 401);
    try {
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
          "User-Agent": "daboysforum-worker"
        },
        body: JSON.stringify({ ref: "main" })
      }).catch((err) => console.error("GitHub dispatch error:", err.message))
    );
    return json({ success: true });
  }
  if (url.pathname === "/link-preview" && request.method === "GET") {
    if (!username) return signInRequired();
    const target = url.searchParams.get("url") || "";
    if (!target || target.length > 2e3) return json({ status: "fail", message: "Missing url" }, 400);
    try {
      const p = await linkPreview(target);
      if (!p) return json({ status: "fail" });
      return json({ status: "success", data: { url: p.url, title: p.title || null, description: p.description || null, image: p.image ? { url: p.image } : null } });
    } catch (err) {
      return json({ status: "fail" });
    }
  }
  if (url.pathname === "/my-username") {
    return json({ username });
  }
  if (url.pathname === "/get-ban-lists") {
    const [bansRes, jailedRes, staffRes] = await Promise.all([
      env.DB.prepare(`SELECT DISTINCT username FROM bans WHERE username IS NOT NULL`).all(),
      env.DB.prepare(`SELECT DISTINCT username FROM jailed WHERE username IS NOT NULL`).all(),
      // Staff names (already public on their tags), so mod purple / admin white show on every tag, old posts included
      env.DB.prepare(`SELECT username, role FROM mod_users WHERE role IN ('mod','admin') AND deleted_at IS NULL AND username IS NOT NULL`).all()
    ]);
    const staff = staffRes.results || [];
    return json({
      banned: (bansRes.results || []).map((r) => r.username),
      jailed: (jailedRes.results || []).map((r) => r.username),
      mods: staff.filter((r) => r.role === "mod").map((r) => r.username),
      admins: staff.filter((r) => r.role === "admin").map((r) => r.username)
    });
  }
  return new Response("OK", { headers: corsHeaders });
}
__name(handleRequest, "handleRequest");

// node_modules/wrangler/templates/middleware/middleware-ensure-req-body-drained.ts
var drainBody = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } finally {
    try {
      if (request.body !== null && !request.bodyUsed) {
        const reader = request.body.getReader();
        while (!(await reader.read()).done) {
        }
      }
    } catch (e) {
      console.error("Failed to drain the unused request body.", e);
    }
  }
}, "drainBody");
var middleware_ensure_req_body_drained_default = drainBody;

// node_modules/wrangler/templates/middleware/middleware-miniflare3-json-error.ts
function reduceError(e) {
  return {
    name: e?.name,
    message: e?.message ?? String(e),
    stack: e?.stack,
    cause: e?.cause === void 0 ? void 0 : reduceError(e.cause)
  };
}
__name(reduceError, "reduceError");
var jsonError = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } catch (e) {
    const error = reduceError(e);
    return Response.json(error, {
      status: 500,
      headers: { "MF-Experimental-Error-Stack": "true" }
    });
  }
}, "jsonError");
var middleware_miniflare3_json_error_default = jsonError;

// .wrangler/tmp/bundle-QFQGBq/middleware-insertion-facade.js
var __INTERNAL_WRANGLER_MIDDLEWARE__ = [
  middleware_ensure_req_body_drained_default,
  middleware_miniflare3_json_error_default
];
var middleware_insertion_facade_default = worker_default;

// node_modules/wrangler/templates/middleware/common.ts
var __facade_middleware__ = [];
function __facade_register__(...args) {
  __facade_middleware__.push(...args.flat());
}
__name(__facade_register__, "__facade_register__");
function __facade_invokeChain__(request, env, ctx, dispatch, middlewareChain) {
  const [head, ...tail] = middlewareChain;
  const middlewareCtx = {
    dispatch,
    next(newRequest, newEnv) {
      return __facade_invokeChain__(newRequest, newEnv, ctx, dispatch, tail);
    }
  };
  return head(request, env, ctx, middlewareCtx);
}
__name(__facade_invokeChain__, "__facade_invokeChain__");
function __facade_invoke__(request, env, ctx, dispatch, finalMiddleware) {
  return __facade_invokeChain__(request, env, ctx, dispatch, [
    ...__facade_middleware__,
    finalMiddleware
  ]);
}
__name(__facade_invoke__, "__facade_invoke__");

// .wrangler/tmp/bundle-QFQGBq/middleware-loader.entry.ts
var __Facade_ScheduledController__ = class ___Facade_ScheduledController__ {
  constructor(scheduledTime, cron, noRetry) {
    this.scheduledTime = scheduledTime;
    this.cron = cron;
    this.#noRetry = noRetry;
  }
  static {
    __name(this, "__Facade_ScheduledController__");
  }
  #noRetry;
  noRetry() {
    if (!(this instanceof ___Facade_ScheduledController__)) {
      throw new TypeError("Illegal invocation");
    }
    this.#noRetry();
  }
};
function wrapExportedHandler(worker) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return worker;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  const fetchDispatcher = /* @__PURE__ */ __name(function(request, env, ctx) {
    if (worker.fetch === void 0) {
      throw new Error("Handler does not export a fetch() function.");
    }
    return worker.fetch(request, env, ctx);
  }, "fetchDispatcher");
  return {
    ...worker,
    fetch(request, env, ctx) {
      const dispatcher = /* @__PURE__ */ __name(function(type, init) {
        if (type === "scheduled" && worker.scheduled !== void 0) {
          const controller = new __Facade_ScheduledController__(
            Date.now(),
            init.cron ?? "",
            () => {
            }
          );
          return worker.scheduled(controller, env, ctx);
        }
      }, "dispatcher");
      return __facade_invoke__(request, env, ctx, dispatcher, fetchDispatcher);
    }
  };
}
__name(wrapExportedHandler, "wrapExportedHandler");
function wrapWorkerEntrypoint(klass) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return klass;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  return class extends klass {
    #fetchDispatcher = /* @__PURE__ */ __name((request, env, ctx) => {
      this.env = env;
      this.ctx = ctx;
      if (super.fetch === void 0) {
        throw new Error("Entrypoint class does not define a fetch() function.");
      }
      return super.fetch(request);
    }, "#fetchDispatcher");
    #dispatcher = /* @__PURE__ */ __name((type, init) => {
      if (type === "scheduled" && super.scheduled !== void 0) {
        const controller = new __Facade_ScheduledController__(
          Date.now(),
          init.cron ?? "",
          () => {
          }
        );
        return super.scheduled(controller);
      }
    }, "#dispatcher");
    fetch(request) {
      return __facade_invoke__(
        request,
        this.env,
        this.ctx,
        this.#dispatcher,
        this.#fetchDispatcher
      );
    }
  };
}
__name(wrapWorkerEntrypoint, "wrapWorkerEntrypoint");
var WRAPPED_ENTRY;
if (typeof middleware_insertion_facade_default === "object") {
  WRAPPED_ENTRY = wrapExportedHandler(middleware_insertion_facade_default);
} else if (typeof middleware_insertion_facade_default === "function") {
  WRAPPED_ENTRY = wrapWorkerEntrypoint(middleware_insertion_facade_default);
}
var middleware_loader_entry_default = WRAPPED_ENTRY;
export {
  __INTERNAL_WRANGLER_MIDDLEWARE__,
  middleware_loader_entry_default as default
};
//# sourceMappingURL=worker.js.map
