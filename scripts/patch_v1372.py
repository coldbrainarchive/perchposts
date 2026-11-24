#!/usr/bin/env python3
"""Patch v1371 -> v1372: no pause when tapping chirps in the post scroller (user's recording: the scroller sat still
~1.5s while the post loaded). The scroller now fetches the post + chirps in the background once you've stayed on a
slide ~0.8s, and again the moment a finger touches the chirps button; the chat page uses that answer (same request,
under 30s old) instead of asking again."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1371.js'
dst = '_deploy/assets/index-DUcNPOLc-v1372.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("let _rq=++_rid.current,e=await fetch(_gpUrl,{headers:er()});",
      "let _rq=++_rid.current,e=await _ppGP(_gpUrl);", 'post page uses prefetch')
patch("setTimeout(()=>_fs(items[i]&&items[i].post),350)",
      "setTimeout(()=>_fs(items[i]&&items[i].post),350);setTimeout(()=>{const _p=items[i]&&items[i].post;_p&&_ppPre(_p)},800)", 'prefetch on dwell')
c += r"""
// Post scroller -> chirps without a pause: fetch the same get-post request the chat page makes on first load
const _ppPreM=new Map();
function _ppGPUrl(id){const u=localStorage.getItem(`_myUsername`)||null;return `${R}/get-post?id=${id}&req_browser_id=${encodeURIComponent(Gn())}&limit=100`+(u?`&req_username=${encodeURIComponent(u)}`:``)}
function _ppPre(id){try{if(!id)return;const url=_ppGPUrl(id),o=_ppPreM.get(url);if(o&&Date.now()-o.t<25e3)return;
 const p=fetch(url,{headers:er()}).then(r=>r.ok?r:Promise.reject(r)).catch(()=>{_ppPreM.delete(url);return null});_ppPreM.set(url,{t:Date.now(),p})}catch(e){}}
async function _ppGP(url){const o=_ppPreM.get(url);if(o&&Date.now()-o.t<3e4){_ppPreM.delete(url);try{const r=await o.p;if(r)return r}catch(e){}}return fetch(url,{headers:er()})}
document.addEventListener(`pointerdown`,e=>{try{const b=e.target.closest&&e.target.closest(`.reel-chat`);if(!b)return;const s=b.closest(`[data-post]`);s&&_ppPre(s.dataset.post)}catch(x){}},!0);
"""
patch("label();loadNear();\n history.pushState({...(history.state||{}),reel:1},``);",
      "label();loadNear();setTimeout(()=>{const _p=items[i]&&items[i].post;_p&&_ppPre(_p)},800);\n history.pushState({...(history.state||{}),reel:1},``);", 'prefetch first slide')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
