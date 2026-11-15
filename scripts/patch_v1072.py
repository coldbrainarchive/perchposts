#!/usr/bin/env python3
"""Patch v1071 -> v1072: no circle behind the bird on profile cards or behind the level emoji in Your Nest;
the icon is centred in its space."""
src = '_deploy/assets/index-DUcNPOLc-v1071.js'
dst = '_deploy/assets/index-DUcNPOLc-v1072.js'
c = open(src, encoding='utf-8').read()
c += r''';(()=>{try{const s=document.createElement(`style`);s.textContent=`
.bc-card .bc-av,.bc-card .bc-rbox .bc-av{background:transparent!important;border:0!important;box-shadow:none!important}
.bc-av{display:flex;align-items:center;justify-content:center;line-height:1}
.bc-av>span,.bc-av>img{display:flex;align-items:center;justify-content:center;line-height:1;margin:0}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
