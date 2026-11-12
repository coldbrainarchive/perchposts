// Removes personal metadata (GPS location, camera/phone make & model, dates, software, comments) from
// uploaded media, keeping only what's needed to display it correctly.
// Used by the worker on every /upload and by the one-off clean-up of existing files.
//
//   JPEG  — drops EXIF/XMP/IPTC/comments; keeps JFIF, the colour profile (ICC) and Adobe colour info.
//           If the photo relied on an EXIF "rotate me" flag, a tiny EXIF block with only that flag is kept.
//   PNG   — keeps only image chunks (plus colour/transparency info); drops text, EXIF, timestamps.
//   WebP  — drops EXIF and XMP chunks.
//   MP4/MOV — blanks every metadata box (udta, meta, uuid) inside the movie header: it is renamed to
//           "free" and zero-filled. Sizes and offsets don't change, so playback is untouched.
//
// stripMedia(bytes: Uint8Array, contentType: string) -> { bytes: Uint8Array, changed: boolean }

export function stripMedia(bytes, contentType = "") {
  try {
    const t = String(contentType).toLowerCase();
    if (t === "image/jpeg" || isJpeg(bytes)) return stripJpeg(bytes);
    if (t === "image/png" || isPng(bytes)) return stripPng(bytes);
    if (t === "image/webp" || isWebp(bytes)) return stripWebp(bytes);
    if (t.startsWith("video/") || isIsoBmff(bytes)) return stripIsoBmff(bytes);
  } catch (e) {
    // fall through: unchanged
  }
  return { bytes, changed: false };
}

const isJpeg = b => b.length > 3 && b[0] === 0xff && b[1] === 0xd8;
const isPng = b => b.length > 8 && b[0] === 0x89 && b[1] === 0x50 && b[2] === 0x4e && b[3] === 0x47;
const isWebp = b => b.length > 12 && str(b, 0, 4) === "RIFF" && str(b, 8, 4) === "WEBP";
const isIsoBmff = b => b.length > 12 && ["ftyp", "moov", "mdat", "wide", "free"].includes(str(b, 4, 4));
const str = (b, o, n) => String.fromCharCode(...b.subarray(o, o + n));

// ── JPEG ────────────────────────────────────────────────────────────────────
function stripJpeg(b) {
  const keep = [b.subarray(0, 2)];
  let i = 2, changed = false, orientation = 1;
  while (i + 4 <= b.length) {
    if (b[i] !== 0xff) return { bytes: b, changed: false }; // not a clean marker stream: leave it alone
    const m = b[i + 1];
    if (m === 0xff) { i++; continue; }                       // fill byte
    if (m === 0xd8 || m === 0x01 || (m >= 0xd0 && m <= 0xd7)) { keep.push(b.subarray(i, i + 2)); i += 2; continue; }
    if (m === 0xda || m === 0xd9) { keep.push(b.subarray(i)); i = b.length; break; } // image data: copy the rest as is
    const len = (b[i + 2] << 8) | b[i + 3];
    const seg = b.subarray(i, i + 2 + len);
    const isApp = m >= 0xe0 && m <= 0xef;
    let drop = false;
    if (m === 0xfe) drop = true;                                         // comment
    else if (isApp && m !== 0xe0 && m !== 0xee) {
      if (m === 0xe2 && str(seg, 4, 11) === "ICC_PROFILE") drop = false;  // colour profile: keep
      else {
        if (m === 0xe1 && str(seg, 4, 4) === "Exif") orientation = readOrientation(seg.subarray(10)) || orientation;
        drop = true;                                                     // EXIF / XMP / IPTC / maker data
      }
    }
    if (drop) changed = true; else keep.push(seg);
    i += 2 + len;
  }
  if (!changed) return { bytes: b, changed: false };
  if (orientation >= 2 && orientation <= 8) keep.splice(keep[1] && keep[1][1] === 0xe0 ? 2 : 1, 0, orientationExif(orientation));
  return { bytes: concat(keep), changed: true };
}
function readOrientation(t) {
  if (t.length < 8) return 0;
  const le = t[0] === 0x49;
  const u16 = o => le ? t[o] | (t[o + 1] << 8) : (t[o] << 8) | t[o + 1];
  const u32 = o => le ? (t[o] | (t[o + 1] << 8) | (t[o + 2] << 16) | (t[o + 3] << 24)) >>> 0 : ((t[o] << 24) | (t[o + 1] << 16) | (t[o + 2] << 8) | t[o + 3]) >>> 0;
  const ifd = u32(4);
  if (ifd + 2 > t.length) return 0;
  const n = u16(ifd);
  for (let k = 0; k < n; k++) {
    const e = ifd + 2 + k * 12;
    if (e + 12 > t.length) break;
    if (u16(e) === 0x0112) return u16(e + 8);
  }
  return 0;
}
function orientationExif(o) {
  // APP1 "Exif\0\0" + little-endian TIFF with one IFD entry: Orientation (0x0112, SHORT, 1, o)
  const tiff = [0x49, 0x49, 0x2a, 0x00, 0x08, 0x00, 0x00, 0x00, 0x01, 0x00, 0x12, 0x01, 0x03, 0x00, 0x01, 0x00, 0x00, 0x00, o, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00];
  const body = [0x45, 0x78, 0x69, 0x66, 0x00, 0x00, ...tiff];
  const len = body.length + 2;
  return new Uint8Array([0xff, 0xe1, len >> 8, len & 0xff, ...body]);
}

// ── PNG ─────────────────────────────────────────────────────────────────────
const PNG_KEEP = new Set(["IHDR", "PLTE", "IDAT", "IEND", "tRNS", "gAMA", "cHRM", "sRGB", "iCCP", "sBIT", "pHYs", "acTL", "fcTL", "fdAT"]);
function stripPng(b) {
  const keep = [b.subarray(0, 8)];
  let i = 8, changed = false;
  while (i + 12 <= b.length) {
    const len = ((b[i] << 24) | (b[i + 1] << 16) | (b[i + 2] << 8) | b[i + 3]) >>> 0;
    const type = str(b, i + 4, 4);
    const end = i + 12 + len;
    if (end > b.length) return { bytes: b, changed: false };
    if (PNG_KEEP.has(type)) keep.push(b.subarray(i, end)); else changed = true;
    i = end;
    if (type === "IEND") break;
  }
  return changed ? { bytes: concat(keep), changed: true } : { bytes: b, changed: false };
}

// ── WebP ────────────────────────────────────────────────────────────────────
function stripWebp(b) {
  const keep = [];
  let i = 12, changed = false;
  while (i + 8 <= b.length) {
    const type = str(b, i, 4);
    const len = (b[i + 4] | (b[i + 5] << 8) | (b[i + 6] << 16) | (b[i + 7] << 24)) >>> 0;
    const end = i + 8 + len + (len & 1);
    if (end > b.length + 1) return { bytes: b, changed: false };
    if (type === "EXIF" || type === "XMP ") changed = true;
    else {
      const c = b.slice(i, Math.min(end, b.length));
      if (type === "VP8X") c[8] &= ~(0x08 | 0x04);   // clear "has EXIF" / "has XMP" flags
      keep.push(c);
    }
    i = end;
  }
  if (!changed) return { bytes: b, changed: false };
  const body = concat(keep);
  const out = new Uint8Array(12 + body.length);
  out.set(b.subarray(0, 12));
  const size = 4 + body.length;
  out[4] = size & 0xff; out[5] = (size >> 8) & 0xff; out[6] = (size >> 16) & 0xff; out[7] = (size >>> 24) & 0xff;
  out.set(body, 12);
  return { bytes: out, changed: true };
}

// ── MP4 / MOV (ISO base media) ──────────────────────────────────────────────
const CONTAINERS = new Set(["moov", "trak", "mdia", "minf", "edts"]);
const WIPE = new Set(["udta", "meta", "uuid"]);
function stripIsoBmff(b) {
  let changed = false;
  const dv = new DataView(b.buffer, b.byteOffset, b.byteLength);
  const walk = (start, end, depth, inMoov) => {
    let i = start;
    while (i + 8 <= end) {
      let size = dv.getUint32(i), hdr = 8;
      const type = str(b, i + 4, 4);
      if (size === 1) { if (i + 16 > end) return; size = Number(dv.getBigUint64(i + 8)); hdr = 16; }
      else if (size === 0) size = end - i;
      if (size < hdr || i + size > end) return;
      if (inMoov && WIPE.has(type)) {
        b[i + 4] = 0x66; b[i + 5] = 0x72; b[i + 6] = 0x65; b[i + 7] = 0x65;   // "free"
        b.fill(0, i + hdr, i + size);
        changed = true;
      } else if (CONTAINERS.has(type) && depth < 6) {
        walk(i + hdr, i + size, depth + 1, inMoov || type === "moov");
      } else if (depth === 0 && (type === "udta" || type === "meta")) {
        b[i + 4] = 0x66; b[i + 5] = 0x72; b[i + 6] = 0x65; b[i + 7] = 0x65;
        b.fill(0, i + hdr, i + size);
        changed = true;
      }
      i += size;
    }
  };
  walk(0, b.length, 0, false);
  return { bytes: b, changed };
}

// Streaming version for MP4/MOV, so big videos never sit in memory: top-level boxes flow through as they arrive;
// only the movie header ("moov", normally well under a few MB) and any top-level udta/meta are held, cleaned
// with stripIsoBmff, then passed on. Output length always equals input length.
export function stripIsoBmffStream() {
  const HOLD = new Set(["moov", "udta", "meta"]), MAX_HOLD = 64 * 1024 * 1024;
  let hdr = new Uint8Array(0), mode = "header", left = 0, held = null, heldLen = 0, heldNeed = 0;
  const join = (a, b) => { const o = new Uint8Array(a.length + b.length); o.set(a); o.set(b, a.length); return o; };
  return new TransformStream({
    transform(chunk, ctl) {
      let c = chunk instanceof Uint8Array ? chunk : new Uint8Array(chunk);
      while (c.length) {
        if (mode === "rest") { ctl.enqueue(c); return; }
        if (mode === "pass") {
          const n = Math.min(left, c.length);
          ctl.enqueue(c.subarray(0, n)); left -= n; c = c.subarray(n);
          if (!left) mode = "header";
          continue;
        }
        if (mode === "hold") {
          const n = Math.min(heldNeed - heldLen, c.length);
          held.set(c.subarray(0, n), heldLen); heldLen += n; c = c.subarray(n);
          if (heldLen === heldNeed) { ctl.enqueue(stripIsoBmff(held).bytes); held = null; mode = "header"; }
          continue;
        }
        // header: need 8 bytes (16 for a 64-bit size)
        const want = hdr.length >= 8 && new DataView(hdr.buffer, hdr.byteOffset).getUint32(0) === 1 ? 16 : 8;
        const n = Math.min(want - hdr.length, c.length);
        hdr = join(hdr, c.subarray(0, n)); c = c.subarray(n);
        if (hdr.length < want) continue;
        if (want === 8 && new DataView(hdr.buffer, hdr.byteOffset).getUint32(0) === 1) continue; // read the 64-bit size next
        const dv = new DataView(hdr.buffer, hdr.byteOffset);
        let size = dv.getUint32(0);
        if (size === 1) size = Number(dv.getBigUint64(8));
        const type = str(hdr, 4, 4), h = hdr; hdr = new Uint8Array(0);
        if (size === 0 || size < h.length) { ctl.enqueue(h); mode = "rest"; continue; }       // runs to the end / not a box
        if (HOLD.has(type) && size <= MAX_HOLD) { held = new Uint8Array(size); held.set(h); heldLen = h.length; heldNeed = size; mode = "hold"; continue; }
        ctl.enqueue(h); left = size - h.length; mode = left ? "pass" : "header";
      }
    },
    flush(ctl) {
      if (hdr.length) ctl.enqueue(hdr);
      if (held) ctl.enqueue(held.subarray(0, heldLen));
    }
  });
}

function concat(parts) {
  const n = parts.reduce((s, p) => s + p.length, 0), out = new Uint8Array(n);
  let o = 0;
  for (const p of parts) { out.set(p, o); o += p.length; }
  return out;
}
