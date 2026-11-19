#!/usr/bin/env python3
"""Patch v1239 -> v1240:
- The card for a shared perchposts post no longer says "VIEW POST →" / "VIEW HUDDLE →" (tapping the card opens the
  preview, which has the View Post button).
- The Cage note on the new-post page is two lines ("You're Caged!" / "You can only post and comment in “The Cage”")
  so it doesn't wrap oddly on phones."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1239.js'
dst = '_deploy/assets/index-DUcNPOLc-v1240.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch(",(0,L.jsx)(`div`,{style:{color:`#c084fc`,fontSize:11,fontWeight:700,letterSpacing:`0.03em`,textTransform:`uppercase`},children:_ih?`View Huddle →`:`View Post →`})]})",
      "]})", 'no View Post line on the card')
patch("s&&(0,L.jsx)(`div`,{style:{color:`#64748b`,fontSize:12,marginBottom:8,lineHeight:1.4},children:s})]})",
      "s&&(0,L.jsx)(`div`,{style:{color:`#64748b`,fontSize:12,marginBottom:0,lineHeight:1.4},children:s})]})", 'no gap left under the text')
patch("p&&(0,L.jsx)(`span`,{style:{fontSize:11,color:`#92400e`,fontWeight:500,marginLeft:4},children:`You’re Caged! You can only post and comment in “The Cage”`})",
      "p&&(0,L.jsxs)(`span`,{style:{fontSize:11,color:`#92400e`,fontWeight:500,marginLeft:4,display:`inline-flex`,flexDirection:`column`,lineHeight:1.35},children:[(0,L.jsx)(`span`,{style:{fontWeight:800},children:`You’re Caged!`}),(0,L.jsx)(`span`,{children:`You can only post and comment in “The Cage”`})]})", 'cage note on two lines')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
