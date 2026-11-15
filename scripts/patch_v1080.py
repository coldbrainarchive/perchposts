#!/usr/bin/env python3
"""Patch v1079 -> v1080: the new birds in the last three places still drawing the old filter-coloured emoji:
huddle faces (_hxFace), reaction rows (_rxFace) and notifications (_nPillKids). Same tag-style bird (cropped, 1px outline);
the admin bird there gets the drawn outline too."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1079.js'
dst = '_deploy/assets/index-DUcNPOLc-v1080.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
def admin(style, z, label):
    old = "(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{" + style + "}})"
    patch(old, "(0,L.jsx)(_PB,{n:`admin`,c:`A`,z:" + z + ",k:`t`,fb:" + old + "})", label)

# huddle faces
patch("children:b&&b.e||`🐦`}),...(b&&b.s?_spEls(b.s,sz):[])]})}",
      "children:b&&b.e?_ppB(b,sz,`t`):`🐦`}),...(b&&b.s?_spEls(b.s,sz):[])]})}", 'huddle bird')
admin("width:sz+2,height:sz+2,objectFit:`contain`", "sz+2", 'huddle admin')
# reaction rows
patch("children:b.e||`🐦`}),...(b.s?_spEls(b.s,sz):[])]});",
      "children:b.e?_ppB(b,sz,`t`):`🐦`}),...(b.s?_spEls(b.s,sz):[])]});", 'reaction bird')
admin("width:sz+3,height:sz+3,objectFit:`contain`", "sz+3", 'reaction admin')
# notifications
patch("children:b.e||`🐦`}),...(b.s?_spEls(b.s,20):[])]})",
      "children:b.e?_ppB(b,21,`t`):`🐦`}),...(b.s?_spEls(b.s,20):[])]})", 'notification bird')
admin("width:24,height:24,objectFit:`contain`", "24", 'notification admin')

open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
