// Shared post links: give /post/<id> its own link-preview tags (title, description, card image) so iMessage,
// WhatsApp, Discord etc. show the post instead of a bare "perchposts". The data comes from the perchposts-og worker,
// which only answers for public posts (never huddles, deleted or archived ones). Everything else is the normal page.
const esc = s => String(s || "");

export async function onRequestGet(ctx) {
  const res = await ctx.next();
  if (!(res.headers.get("content-type") || "").includes("text/html")) return res;
  let meta = null;
  try {
    const r = await fetch(`https://perchposts-og.coldbrainarchive.workers.dev/meta/${encodeURIComponent(ctx.params.id)}`, { signal: AbortSignal.timeout(2500) });
    if (r.ok) meta = await r.json();
  } catch {}
  if (!meta || !meta.title) return res;
  const url = `https://perchposts.com/post/${encodeURIComponent(ctx.params.id)}`;
  const desc = meta.description || (meta.site ? `Shared from ${meta.site}` : "On perchposts");
  const set = (v) => ({ element(el) { el.setAttribute("content", esc(v)); } });
  let added = false;
  return new HTMLRewriter()
    .on('meta[property="og:title"]', set(meta.title))
    .on('meta[name="twitter:title"]', set(meta.title))
    .on('meta[property="og:description"]', set(desc))
    .on('meta[name="twitter:description"]', set(desc))
    .on('meta[property="og:image"]', set(meta.img))
    .on('meta[name="twitter:image"]', set(meta.img))
    .on('meta[property="og:type"]', set("article"))
    .on("title", { element(el) { el.setInnerContent(meta.title); } })
    .on("head", { element(el) {
      if (added) return; added = true;
      const q = s => esc(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
      el.append(`<meta property="og:url" content="${q(url)}" /><meta property="og:site_name" content="perchposts" />` +
        `<meta property="og:image:width" content="1200" /><meta property="og:image:height" content="630" />` +
        `<meta property="og:image:type" content="image/png" /><link rel="canonical" href="${q(url)}" />`, { html: true });
    } })
    .transform(res);
}
