#!/usr/bin/env python3
"""Patch v1058 -> v1059: new logo, a globe shaped like a bird's head (crest, eye, beak) replacing the plain globe.
- Header: 40px glowing version (neon + halo), nudged up 1px; the "perchposts" name gets a matching purple glow.
- Small role badges next to admin/mod names (post cards, profile cards): one-colour version of the bird.
Logo artwork lives in brand/ (logo_strings.json). To go back to the globe: point _deploy/index.html at v1058 and
copy brand/old-globe-favicon.svg over _deploy/favicon.svg."""
import sys, json
src = '_deploy/assets/index-DUcNPOLc-v1058.js'
dst = '_deploy/assets/index-DUcNPOLc-v1059.js'
c = open(src, encoding='utf-8').read()
S = json.load(open('brand/logo_strings.json'))
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
def seg(pat):
    i = c.find(pat); assert i >= 0, pat
    j = c.find('(', i + len('(0,L.jsxs)')); d = 0; k = j
    while True:
        if c[k] == '(': d += 1
        elif c[k] == ')':
            d -= 1
            if d == 0: return c[i:k+1]
        k += 1
header = seg('(0,L.jsxs)(`svg`,{width:`32`,height:`32`')
pill = seg('(0,L.jsxs)(`svg`,{width:`14`')
bc = seg('(0,L.jsxs)(`svg`,{width:14,height:14')
patch(header, '(0,L.jsx)(`span`,{className:`pp-logo`,"aria-hidden":!0,dangerouslySetInnerHTML:{__html:_ppLogo(`glow`)}})', 'header logo')
patch(pill, '(0,L.jsx)(`span`,{className:`pp-badge`,"aria-hidden":!0,dangerouslySetInnerHTML:{__html:_ppLogo(`mono`,`#0a0a0a`)}})', 'name pill badge')
patch(bc, '(0,L.jsx)(`span`,{className:`pp-badge`,"aria-hidden":!0,dangerouslySetInnerHTML:{__html:_ppLogo(`mono`,k)}})', 'profile card badge')
c += '\nfunction _ppLogo(kind,col){const S=' + json.dumps({k: S[k] for k in ('glow', 'mono')}) + ';'
c += 'if(kind===`mono`){_ppLogo.n=(_ppLogo.n||0)+1;return S.mono.split(`COLOR`).join(col||`#c084fc`).split(`mbID`).join(`mb`+_ppLogo.n)}return S.glow}\n'
c += r''';(()=>{try{const s=document.createElement(`style`);s.textContent=`
.pp-logo{display:inline-flex;width:40px;height:40px;flex-shrink:0;position:relative;top:-1px}
.pp-logo svg{width:100%;height:100%;overflow:visible}
.app-brand{text-shadow:0 0 4px rgba(192,132,252,.8),0 0 12px rgba(192,132,252,.5),0 0 24px rgba(192,132,252,.3)}
.pp-badge{display:inline-flex;width:14px;height:14px;flex-shrink:0}
.pp-badge svg{width:100%;height:100%}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
