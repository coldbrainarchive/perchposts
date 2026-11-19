#!/usr/bin/env python3
"""Patch v1234 -> v1235: Perch News pill matches the other space pills: solid site purple, dark text, no outline or
glow. Its icon is the site's tab icon (the dark globe with purple grid lines), shown at emoji size."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1234.js'
dst = '_deploy/assets/index-DUcNPOLc-v1235.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('border:n.slug===`botnews`?`1px solid #c084fc`:`1px solid rgba(0,0,0,0.15)`,background:n.slug===`botnews`?`#14151b`:_bc,color:n.slug===`botnews`?`#c084fc`:`#0a0a0a`,textShadow:n.slug===`botnews`?`0 0 4px rgba(192,132,252,.7)`:void 0,boxShadow:n.slug===`botnews`?`0 0 6px rgba(192,132,252,.35)`:void 0,',
      'border:`1px solid rgba(0,0,0,0.15)`,background:_bc,color:`#0a0a0a`,', 'same pill look as the other spaces')
patch('dangerouslySetInnerHTML:{__html:_ppLogo(`mono`,`#c084fc`)}',
      'dangerouslySetInnerHTML:{__html:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="15 9 82 82"><defs><clipPath id="pnf"><circle cx="56" cy="50" r="38"/></clipPath></defs><circle cx="56" cy="50" r="38" fill="#14151b"/><g fill="none" stroke="#c084fc" stroke-width="3.2" clip-path="url(#pnf)"><line x1="18" y1="50" x2="94" y2="50"/><path d="M 16 30 Q 56 37 96 30"/><path d="M 16 70 Q 56 63 96 70"/><path d="M 56 12 A 11.49 38 0 0 1 56 88"/><path d="M 56 12 A 24.98 38 0 0 1 56 88"/><path d="M 56 12 A 11.49 38 0 0 0 56 88"/><path d="M 56 12 A 24.98 38 0 0 0 56 88"/></g><g clip-path="url(#pnf)"></g><circle cx="56" cy="50" r="38" fill="none" stroke="#c084fc" stroke-width="4.6"/></svg>`}', 'tab icon as the symbol')
patch('body .pp-pn-ic{display:inline-flex;width:13px;height:13px;flex-shrink:0;filter:drop-shadow(0 0 2px rgba(192,132,252,.6))}',
      'body .pp-pn-ic{display:inline-flex;width:14px;height:14px;flex-shrink:0}', 'emoji-size icon, no glow')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
