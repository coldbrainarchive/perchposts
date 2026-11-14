#!/usr/bin/env python3
"""Patch v1061 -> v1062: header logo 40px -> 48px. Negative vertical margin keeps the header the same height."""
src = '_deploy/assets/index-DUcNPOLc-v1061.js'
dst = '_deploy/assets/index-DUcNPOLc-v1062.js'
c = open(src, encoding='utf-8').read()
c += r''';(()=>{try{const s=document.createElement(`style`);s.textContent=`
.pp-logo{width:48px;height:48px;margin:-4px 0}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
