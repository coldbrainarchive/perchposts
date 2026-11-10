#!/usr/bin/env python3
"""Patch v943 -> v944: no circle behind the bird in the reactions lists (menu + long-press sheet)."""
src = '_deploy/assets/index-DUcNPOLc-v943.js'
dst = '_deploy/assets/index-DUcNPOLc-v944.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.rx-av{background:none!important;border:none!important}
.rx-who .rx-row{padding-left:6px}
.rx-who .rx-av{width:16px}
.rx-list .rx-row{padding-left:10px}
.rx-list .rx-av{width:24px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
