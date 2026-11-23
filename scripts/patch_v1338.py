#!/usr/bin/env python3
"""Patch v1337 -> v1338: share counts. A signed-in bird's share (huddle send, Copy link, or the phone's share menu via
More…) calls /share; it counts once per bird per post. The number shows beside Share on feed cards, the post page and
the post scroller (dock) once it's above 0, and updates straight away after you share."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1337.js'
dst = '_deploy/assets/index-DUcNPOLc-v1338.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

# share sheet: record each kind of share
patch("const copy=async()=>{try{await navigator.clipboard.writeText(url);setCopied(!0);",
      "const copy=async()=>{try{await navigator.clipboard.writeText(url);setCopied(!0);_ppShared(id,`copy`);", 'copy')
patch("const more=async()=>{try{if(navigator.share){await navigator.share({url});bye()}else{await navigator.clipboard.writeText(url);setCopied(!0);",
      "const more=async()=>{try{if(navigator.share){await navigator.share({url});_ppShared(id,`more`);bye()}else{await navigator.clipboard.writeText(url);setCopied(!0);_ppShared(id,`copy`);", 'more')
patch("setBusy(!1);if(ok){const one=sel.length===1",
      "setBusy(!1);if(ok){_ppShared(id,`huddle`);const one=sel.length===1", 'huddle send')

# feed card: number beside the share icon, re-render on updates
patch("(0,_.useEffect)(()=>_ppResp.sub(e.id,()=>_rv(x=>x+1)),[e.id]);",
      "(0,_.useEffect)(()=>_ppResp.sub(e.id,()=>_rv(x=>x+1)),[e.id]);(0,_.useEffect)(()=>_ppShSub(e.id,()=>_rv(x=>x+1)),[e.id]);", 'card sub')
patch("dangerouslySetInnerHTML:{__html:_ppIco(`SHARE`)}}),o!==`Share`?(0,L.jsx)(`span`,{children:o}):null]",
      "dangerouslySetInnerHTML:{__html:_ppIco(`SHARE`)}}),o!==`Share`?(0,L.jsx)(`span`,{children:o}):_ppShN(e.id,e.share_count)>0?(0,L.jsx)(`span`,{children:_ppShN(e.id,e.share_count)}):null]", 'card number')

# post page
patch("[j,M]=(0,_.useState)(`Share`),",
      "[j,M]=(0,_.useState)(`Share`),[,_shv]=(0,_.useState)(0),_shE=(0,_.useEffect)(()=>{const h=()=>_shv(x=>x+1);addEventListener(`pp-sharen`,h);return()=>removeEventListener(`pp-sharen`,h)},[]),", 'post page sub')
patch("dangerouslySetInnerHTML:{__html:_ppIco(`SHARE`)}}),(0,L.jsx)(`span`,{children:j})]}",
      "dangerouslySetInnerHTML:{__html:_ppIco(`SHARE`)}}),(0,L.jsx)(`span`,{children:j===`Share`&&_ppShN(c.id,c.share_count)>0?_ppShN(c.id,c.share_count):j})]}", 'post page number')

# post scroller
patch("sh.setAttribute(`aria-label`,`Share`);sh.innerHTML=_ppIco(`SHARE`)+`<span>Share</span>`;",
      "sh.setAttribute(`aria-label`,`Share`);sh.dataset.sid=d.post;sh.innerHTML=_ppIco(`SHARE`)+`<span>${_ppShN(d.post)||`Share`}</span>`;", 'reel label')
patch("setTimeout(()=>{sh.innerHTML=_ppIco(`SHARE`)+`<span>Share</span>`;sh.classList.remove(`done`)},1800)",
      "setTimeout(()=>{sh.innerHTML=_ppIco(`SHARE`)+`<span>${_ppShN(d.post)||`Share`}</span>`;sh.classList.remove(`done`)},1800)", 'reel reset')

c += r"""
function _ppShN(id,n){const s=window._ppShareN||(window._ppShareN={});if(n!=null&&(s[id]==null||+n>s[id]))s[id]=+n||0;return s[id]||0}
function _ppShSub(id,f){const h=e=>{if(e.detail&&e.detail.id===id)f()};addEventListener(`pp-sharen`,h);return()=>removeEventListener(`pp-sharen`,h)}
function _ppShared(id,via){try{if(!id||!localStorage.getItem(`auth_token`))return;fetch(`${R}/share`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({post_id:id,via})}).then(r=>r.ok?r.json():null).then(j=>{if(!j||j.share_count==null)return;(window._ppShareN||(window._ppShareN={}))[id]=j.share_count;dispatchEvent(new CustomEvent(`pp-sharen`,{detail:{id,n:j.share_count}}))}).catch(()=>{})}catch(e){}}
;addEventListener(`pp-sharen`,e=>{try{const{id,n}=e.detail||{};document.querySelectorAll(`.reel-share[data-sid="${CSS.escape(id)}"]`).forEach(b=>{if(b.classList.contains(`done`))return;b.innerHTML=_ppIco(`SHARE`)+`<span>${n>0?n:`Share`}</span>`})}catch(er){}});
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
