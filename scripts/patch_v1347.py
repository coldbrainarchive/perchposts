#!/usr/bin/env python3
"""Patch v1346 -> v1347: keyword search in Huddles. With the Huddles tag + keywords, the list comes from /huddle-search
(your huddles whose title, opening message or any chirp has the word). Opening one jumps to the FIRST chirp that said
it (?highlight= via window._ppHxHit), while that search is active."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1346.js'
dst = '_deploy/assets/index-DUcNPOLc-v1347.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch("if(!m){setSR(null);setSRLoading(!1);return}setSRLoading(!0);fetch(`${R}/get-posts?search=",
      "if(!m){window._ppHxHit={};setSR(null);setSRLoading(!1);return}setSRLoading(!0);"
      "if(u===`feedback`||u===`huddles`){let _hc=!1;fetch(`${R}/huddle-search?q=${encodeURIComponent(m)}`,{headers:er()}).then(r2=>r2.ok?r2.json():{posts:[]}).then(d2=>{if(_hc)return;const hit={};const ps=(d2.posts||[]).map(x=>{if(x.hit_comment)hit[x.id]=x.hit_comment;return{...x,_kwHit:1}});window._ppHxHit=hit;setSR(Sr(ps));setSRLoading(!1)}).catch(()=>{if(!_hc){setSR([]);setSRLoading(!1)}});return()=>{_hc=!0}}"
      "fetch(`${R}/get-posts?search=", 'SR huddles')
patch("},[m,f]),", "},[m,f,u]),", 'SR deps')
patch(".filter(e=>{if(!m)return!0;if(_cs)return _inHome(e,f)||_cnHit(e,f);",
      ".filter(e=>{if(!m)return!0;if(e._kwHit)return!0;if(_cs)return _inHome(e,f)||_cnHit(e,f);", 'keyword filter')
patch("[i]=kn(),a=i.get(`highlight`),_nc=i.get(`nc`)",
      "[i]=kn(),a=i.get(`highlight`)||(window._ppHxHit||{})[(location.pathname.match(/^\\/post\\/([^/?#]+)/)||[])[1]]||null,_nc=i.get(`nc`)", 'post page highlight')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
