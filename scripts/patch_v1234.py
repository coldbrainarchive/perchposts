#!/usr/bin/env python3
"""Patch v1233 -> v1234: the "Bot News" space is now "Perch News". Its pill uses the site logo (the purple globe,
mono version) instead of the robot emoji, and the site's own look: dark pill, purple outline, purple glowing text
(plain purple is already Random's colour). The slug stays botnews, so links and filters keep working."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1233.js'
dst = '_deploy/assets/index-DUcNPOLc-v1234.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("{name:`Bot News`,slug:`botnews`,icon:`🤖`,virtual:!0}", "{name:`Perch News`,slug:`botnews`,icon:``,virtual:!0}", 'rename')
patch("botnews:`#a5b4fc`,", "botnews:`#c084fc`,", 'site purple')
P = "n.slug===`botnews`"
patch("border:`1px solid rgba(0,0,0,0.15)`,background:_bc,color:`#0a0a0a`,",
      f"border:{P}?`1px solid #c084fc`:`1px solid rgba(0,0,0,0.15)`,background:{P}?`#14151b`:_bc,color:{P}?`#c084fc`:`#0a0a0a`,textShadow:{P}?`0 0 4px rgba(192,132,252,.7)`:void 0,boxShadow:{P}?`0 0 6px rgba(192,132,252,.35)`:void 0,",
      'dark pill, purple outline and glow')
patch("children:[(0,L.jsx)(`span`,{style:{display:`flex`,alignItems:`center`,lineHeight:1},children:n.icon}),(0,L.jsx)(`span`,{children:n.name})]})}",
      f"children:[{P}?(0,L.jsx)(`span`,{{className:`pp-pn-ic`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{{__html:_ppLogo(`mono`,`#c084fc`)}}}}):(0,L.jsx)(`span`,{{style:{{display:`flex`,alignItems:`center`,lineHeight:1}},children:n.icon}}),(0,L.jsx)(`span`,{{children:n.name}})]}})}}",
      'globe logo as the icon')
patch("body .lb-ic{", "body .pp-pn-ic{display:inline-flex;width:13px;height:13px;flex-shrink:0;filter:drop-shadow(0 0 2px rgba(192,132,252,.6))}body .pp-pn-ic svg{width:100%;height:100%;overflow:visible}body .lb-ic{", 'icon size')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
