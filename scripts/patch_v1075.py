#!/usr/bin/env python3
"""Patch v1074 -> v1075: bigger bird on profile cards (emoji 38px -> 48px, admin bird picture 44px -> 54px)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1074.js'
dst = '_deploy/assets/index-DUcNPOLc-v1075.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("face:_bd&&_bd.hat?(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{width:44,height:44,objectFit:`contain`}}):(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-flex`,fontSize:38,lineHeight:1},children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``},children:_bd&&_bd.e?_bd.e:`🐤`}),...(_bd&&_bd.s?_spEls(_bd.s,38):[])]}),rc:_resolvedCol",
      "face:_bd&&_bd.hat?(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{width:54,height:54,objectFit:`contain`}}):(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-flex`,fontSize:48,lineHeight:1},children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``},children:_bd&&_bd.e?_bd.e:`🐤`}),...(_bd&&_bd.s?_spEls(_bd.s,48):[])]}),rc:_resolvedCol", 'bigger bird')
c += r''';(()=>{try{const s=document.createElement(`style`);s.textContent=`
.bc-card:not(.bc-nest) .bc-rbox .bc-av{width:64px;height:64px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
