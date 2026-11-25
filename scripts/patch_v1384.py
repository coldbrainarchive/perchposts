#!/usr/bin/env python3
"""Patch v1383 -> v1384: the emoji picker / worm wallet sheet and the photo viewer use the site's colours.
- Sheet #1f1f21 (iPhone grey) -> #161920 (the Share sheet's colour), search box like the Share message box,
  category / emoji highlights and greys in the site's slate tones, worm wallet steppers like the Share buttons.
- Photo viewer backdrop black -> the main page colour (#16171d).
One shared sheet (.ri-sheet) + one shared viewer (.pv), so this applies everywhere they open."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1383.js'
dst = '_deploy/assets/index-DUcNPOLc-v1384.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
CSS = (
 "body .ri-sheet{background:#161920!important}"
 "body .ww-ov .ri-sheet,body .ri-ov .ri-sheet{box-shadow:0 -10px 40px rgba(0,0,0,.45),0 300px 0 0 #161920!important}"
 "body .ri-search{background:#0d0f14!important;border:1px solid rgba(255,255,255,.07);color:#64748b!important}"
 "body .ri-search input{color:#e2e8f0!important}body .ri-search input::placeholder{color:#64748b!important}"
 "body .ri-lb{color:#64748b!important}body .ri-msg{color:#94a3b8!important}"
 "body .ri-cat{color:#94a3b8!important}body .ri-cat.on{background:#23262e!important;color:#f1f5f9!important}"
 "body .ri-e:hover{background:#1f222b!important}body .ri-e:active{background:#23262e!important}"
 "body .ww-in{background:#0d0f14!important;border-color:rgba(255,255,255,.07)!important}"
 "body .ww-st{background:#1d242d!important;border-color:#323b48!important}"
 "body .ww-st:disabled{background:#16191f!important;border-color:#23262e!important}"
 "body .pv{background:rgba(22,23,29,.98)!important}"
 "body .lb-ic{")
patch("body .lb-ic{", CSS, 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
