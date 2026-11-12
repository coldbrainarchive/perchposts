#!/usr/bin/env python3
"""Patch v1023 -> v1024: iPhone HEIC photos in browsers that can't open them (e.g. desktop Chrome).
Before: the upload was refused by the server and the tile offered "↻ Retry", which could never work.
Now: the tile says "HEIC — not supported here" (no Retry) and a message explains to use Safari or save the
photo as JPEG. Safari (phone and Mac) converts HEIC to a cleaned JPEG as before."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1023.js'
dst = '_deploy/assets/index-DUcNPOLc-v1024.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('if(g!==S.gen||it.gone)return;const u=await _mtXhr(it,up,',
      'if(g!==S.gen||it.gone)return;if(it.type===`image`&&up===it.file&&/hei[cf]/i.test((it.file.type||``)+` `+(it.file.name||``))){it.err=`heic`;it.xhr=null;_mtSync(S);_hxToast(`This browser can’t open iPhone HEIC photos. Use Safari, or save the photo as JPEG first.`);return}const u=await _mtXhr(it,up,',
      'spot HEIC the browser cannot open')
patch('x.err?(0,L.jsx)(`button`,{type:`button`,className:`mt-err`,onClick:e=>{e.stopPropagation();_mtUpload(S,x)},children:`↻ Retry`}):null',
      'x.err===`heic`?(0,L.jsxs)(`div`,{className:`mt-err mt-heic`,children:[`HEIC`,(0,L.jsx)(`small`,{children:`not supported here`})]}):x.err?(0,L.jsx)(`button`,{type:`button`,className:`mt-err`,onClick:e=>{e.stopPropagation();_mtUpload(S,x)},children:`↻ Retry`}):null',
      'HEIC tile')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.mt-heic{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;cursor:default;line-height:1.1;text-align:center}
.mt-heic small{font-size:10px;font-weight:700;opacity:.85}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
