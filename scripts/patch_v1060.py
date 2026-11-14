#!/usr/bin/env python3
"""Patch v1059 -> v1060:
- Admin/mod badges next to names (chirp name pills and profile cards) go back to the original plain globe;
  the bird-globe stays only as the site logo.
- Softer glow on the "perchposts" name.
- New Post / notification buttons moved down ~3px to line up with the body of the lowercase letters
  (the text box is centred, but the letters' visual middle sits lower)."""
import sys
old_src = open('_deploy/assets/index-DUcNPOLc-v1058.js', encoding='utf-8').read()
src = '_deploy/assets/index-DUcNPOLc-v1059.js'
dst = '_deploy/assets/index-DUcNPOLc-v1060.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
def seg(s, pat):
    i = s.find(pat); assert i >= 0, pat
    j = s.find('(', i + len('(0,L.jsxs)')); d = 0; k = j
    while True:
        if s[k] == '(': d += 1
        elif s[k] == ')':
            d -= 1
            if d == 0: return s[i:k+1]
        k += 1
patch('(0,L.jsx)(`span`,{className:`pp-badge`,"aria-hidden":!0,dangerouslySetInnerHTML:{__html:_ppLogo(`mono`,`#0a0a0a`)}})',
      seg(old_src, '(0,L.jsxs)(`svg`,{width:`14`'), 'name pill globe back')
patch('(0,L.jsx)(`span`,{className:`pp-badge`,"aria-hidden":!0,dangerouslySetInnerHTML:{__html:_ppLogo(`mono`,k)}})',
      seg(old_src, '(0,L.jsxs)(`svg`,{width:14,height:14'), 'profile card globe back')
c += r''';(()=>{try{const s=document.createElement(`style`);s.textContent=`
.app-brand{text-shadow:0 0 3px rgba(192,132,252,.55),0 0 10px rgba(192,132,252,.28)}
.app-actions{position:relative;top:3px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
