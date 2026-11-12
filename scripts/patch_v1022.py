#!/usr/bin/env python3
"""Patch v1021 -> v1022: lighter photos.
- Photos are shrunk on the phone before uploading: a full copy (longest side 2048px, sharp full screen) and a
  small copy (960px) used in chirps, postcards, the post page and notifications; the full one only loads in the
  photo viewer. Older photos without a small copy work as before. Re-saving also drops hidden location (GPS) data.
  Small screenshots/PNGs (<= 1.5 MB, not oversized) and GIFs (animation) are left alone. If shrinking fails,
  the original uploads as before.
- The photo viewer only loads the photo you're on and its neighbours.
- Images wait until they're about to scroll into view (feed photos, post photos, chirp photos, link-preview
  pictures, notification thumbnails) and decode off the main thread. A photo you just sent still shows at once
  (it comes from your phone's own copy)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1021.js'
dst = '_deploy/assets/index-DUcNPOLc-v1022.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch('const u=await _mtXhr(it,it.file,p=>{it.p=Math.min(.98,p);_mtEmit(S)});',
      'const [up,th]=it.type===`image`?await Promise.all([_mtShrink(it.file,2048,.82),_mtShrink(it.file,960,.78)]):[it.file,null];if(g!==S.gen||it.gone)return;'
      'const u=await _mtXhr(it,up,p=>{it.p=Math.min(.92,p);_mtEmit(S)});if(g!==S.gen||it.gone)return;'
      'if(th&&th!==it.file){try{const tu=await _mtXhr(it,th,()=>{});(window._mtTh||(window._mtTh={}))[u]=tu}catch(e){if(g!==S.gen||it.gone)return}}', 'full + small copy upload')
patch('it.length===1&&S.fmt===`chat`?{type:`image`,url:it[0].url}:', 'it.length===1&&S.fmt===`chat`?_mtAtt(it[0].url):', 'single chat photo keeps small copy')
patch('_u=>({type:`image`,url:_u})', '_u=>_mtAtt(_u)', 'photo lists keep small copy', n=3)
for v in ['_pAtts', '_cAtts', '_tAtts']:
    patch('src:_mtSrc(' + v + '[0].url),', 'src:_mtPrev(' + v + '[0]),', v + ' shows small copy')
patch('src:_mtSrc(n),alt:``,', 'src:_mtPrev(e),alt:``,', 'attachment photo shows small copy')
patch('image:p?.type===`image`?p.url:', 'image:p?.type===`image`?(p.thumb||p.url):', 'preview card small copy')
patch('img:_s?.[0]?.url||(_a?.type===`image`?_a.url:_a?.image||_a?.poster)', 'img:(_s?.[0]?(_s[0].thumb||_s[0].url):null)||(_a?.type===`image`?(_a.thumb||_a.url):_a?.image||_a?.poster)', 'notification thumbnail small copy')
# viewer: only load the photo you're on and its neighbours
patch('im.alt=``;im.draggable=!1;im.src=u;return im', 'im.alt=``;im.draggable=!1;im.dataset.src=u;return im', 'viewer: hold photos')
patch('const label=()=>{if(!many)return;', 'const label=()=>{[i-1,i,i+1].forEach(k=>{const m=imgs[k];if(m&&!m.src)m.src=m.dataset.src});if(!many)return;', 'viewer: load current + neighbours')
LZ = 'loading:`lazy`,decoding:`async`,'
patch('(0,L.jsx)(`img`,{src:r,alt:``,style:{', '(0,L.jsx)(`img`,{src:r,alt:``,' + LZ + 'style:{', 'link preview pictures', n=4)
patch('(0,L.jsx)(`img`,{src:_pvw(e).img,alt:``,', '(0,L.jsx)(`img`,{src:_pvw(e).img,alt:``,' + LZ, 'notification thumbnails', n=2)
patch('src:_mtPrev(e),alt:``,style:{width:`100%`,maxWidth:`100%`', 'src:_mtPrev(e),alt:``,loading:_mtLz(n),decoding:`async`,style:{width:`100%`,maxWidth:`100%`', 'attachment photo lazy')
for v, rest in [('_pAtts', 'style:'), ('_cAtts', 'alt:``,style:'), ('_tAtts', 'style:')]:
    patch('src:_mtPrev(' + v + '[0]),' + rest, 'src:_mtPrev(' + v + '[0]),loading:_mtLz(' + v + '[0].url),decoding:`async`,' + rest, v + ' photo lazy')

c += r'''
function _mtAtt(u){const t=window._mtTh&&window._mtTh[u];return t?{type:`image`,url:u,thumb:t}:{type:`image`,url:u}}
function _mtPrev(a){try{if(!a)return``;const l=_mtSrc(a.url);return l!==a.url?l:(a.thumb||a.url)}catch(e){return a&&a.url||``}}
function _mtLz(u){try{return _mtSrc(u)!==u?`eager`:`lazy`}catch(e){return`lazy`}}
async function _mtShrink(file,MAX=2048,Q=.85){try{
 const t=(file.type||``).toLowerCase();if(t===`image/gif`)return file;
 let src,w,h,close=()=>{};
 try{src=await createImageBitmap(file,{imageOrientation:`from-image`});w=src.width;h=src.height;close=()=>{try{src.close()}catch(e){}}}
 catch(e){const u=URL.createObjectURL(file);src=await new Promise((res,rej)=>{const i=new Image();i.onload=()=>res(i);i.onerror=rej;i.src=u});w=src.naturalWidth;h=src.naturalHeight;close=()=>URL.revokeObjectURL(u)}
 if(!w||!h){close();return file}
 const k=Math.min(1,MAX/Math.max(w,h));
 if(MAX<2048&&k===1){close();return file}
 if(t===`image/png`&&k===1&&file.size<=1.5e6){close();return file}
 const cw=Math.max(1,Math.round(w*k)),ch=Math.max(1,Math.round(h*k)),cv=document.createElement(`canvas`);cv.width=cw;cv.height=ch;
 const x=cv.getContext(`2d`);x.fillStyle=`#14161c`;x.fillRect(0,0,cw,ch);x.imageSmoothingQuality=`high`;x.drawImage(src,0,0,cw,ch);close();
 const blob=await new Promise(r=>cv.toBlob(r,`image/jpeg`,Q));cv.width=cv.height=0;
 if(!blob||!blob.size)return file;
 if(t===`image/png`&&blob.size>=file.size&&k===1)return file;
 const base=(file.name||`photo`).replace(/\.[^.]+$/,``)||`photo`;
 return new File([blob],base+`.jpg`,{type:`image/jpeg`})
}catch(e){return file}}
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
