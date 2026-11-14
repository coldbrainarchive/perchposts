#!/usr/bin/env python3
"""Patch v1066 -> v1067: header logo a bit smaller on phones (48px -> 44px); desktop stays 48px. The header keeps its height."""
src = '_deploy/assets/index-DUcNPOLc-v1066.js'
dst = '_deploy/assets/index-DUcNPOLc-v1067.js'
c = open(src, encoding='utf-8').read()
c += r''';(()=>{try{const s=document.createElement(`style`);s.textContent=`
@media (max-width:900px){.pp-logo{width:44px;height:44px;margin:-2px 0}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
