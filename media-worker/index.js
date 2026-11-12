// perchposts-media: serves /media/<key> from R2 for the main worker, through Workers Cache.
// The main worker forwards GET/HEAD /media/* here over a service binding (this worker has no public address).
// Responses are full 200s marked cacheable; Cloudflare stores them and slices byte ranges itself, so repeat
// views and video seeking are answered from a nearby copy without touching R2.
//   ?thumb=1         → the small copy (thumbs/<key>.jpg) of an older photo if there is one, else the photo
//   POST /__purge    → { keys: [...] } removes those files' cached copies everywhere (used by Delete forever)

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === "/__purge" && request.method === "POST") {
      const { keys = [] } = await request.json().catch(() => ({}));
      const tags = keys.filter(k => typeof k === "string" && /^[\x21-\x7e]{1,1000}$/.test(k)).map(k => "m:" + k);
      if (!tags.length) return Response.json({ success: true, purged: 0 });
      const result = await ctx.cache.purge({ tags });
      return Response.json({ ...result, purged: tags.length });
    }

    if (request.method !== "GET" && request.method !== "HEAD") return new Response("Method not allowed", { status: 405 });
    if (!url.pathname.startsWith("/media/")) return new Response("Not found", { status: 404 });

    const name = url.pathname.slice("/media/".length);
    if (!/^(thumbs\/)?[A-Za-z0-9][A-Za-z0-9._-]*$/.test(name)) return new Response("Not found", { status: 404 });
    let key = name;
    if (url.searchParams.get("thumb") === "1" && !name.startsWith("thumbs/")) {
      if (await env.MEDIA.head(`thumbs/${name}.jpg`)) key = `thumbs/${name}.jpg`;
    }

    const base = name.startsWith("thumbs/") ? name.slice(7).replace(/\.jpg$/, "") : name;

    // Normally Cloudflare strips Range and slices the cached copy itself. If a Range header still reaches us
    // (cache skipped for this request), answer the piece directly so video seeking keeps working.
    const rm = /^bytes=(\d*)-(\d*)$/.exec((request.headers.get("range") || "").trim());
    if (rm && (rm[1] !== "" || rm[2] !== "")) {
      const head = await env.MEDIA.head(key);
      if (!head) return new Response("Not found", { status: 404, headers: { "access-control-allow-origin": "*" } });
      const size = head.size;
      let start, end;
      if (rm[1] === "") { start = Math.max(0, size - Number(rm[2])); end = size - 1; }
      else { start = Number(rm[1]); end = rm[2] === "" ? size - 1 : Math.min(size - 1, Number(rm[2])); }
      const h = new Headers();
      head.writeHttpMetadata(h);
      h.set("etag", head.httpEtag);
      h.set("accept-ranges", "bytes");
      h.set("access-control-allow-origin", "*");
      h.set("access-control-expose-headers", "content-range, content-length, accept-ranges");
      h.set("x-content-type-options", "nosniff");
      h.set("content-security-policy", "default-src 'none'; sandbox");
      h.set("cache-control", "public, max-age=31536000, immutable");
      if (start >= size || end < start) { h.set("content-range", `bytes */${size}`); return new Response(null, { status: 416, headers: h }); }
      h.set("content-range", `bytes ${start}-${end}/${size}`);
      h.set("content-length", String(end - start + 1));
      if (request.method === "HEAD") return new Response(null, { status: 206, headers: h });
      const part = await env.MEDIA.get(key, { range: { offset: start, length: end - start + 1 } });
      return new Response(part.body, { status: 206, headers: h });
    }

    const obj = await env.MEDIA.get(key);
    if (!obj) {
      return new Response("Not found", { status: 404, headers: { "cache-control": "public, max-age=60", "cache-tag": `m:${base}`, "access-control-allow-origin": "*" } });
    }
    const headers = new Headers();
    obj.writeHttpMetadata(headers);
    headers.set("etag", obj.httpEtag);
    headers.set("content-length", String(obj.size));
    headers.set("cache-control", "public, max-age=31536000, immutable");
    headers.set("cache-tag", `m:${base}`);
    headers.set("accept-ranges", "bytes");
    headers.set("access-control-allow-origin", "*");
    headers.set("access-control-expose-headers", "content-range, content-length, accept-ranges");
    headers.set("x-content-type-options", "nosniff");
    headers.set("content-security-policy", "default-src 'none'; sandbox");
    return new Response(request.method === "HEAD" ? null : obj.body, { headers });
  },
};
