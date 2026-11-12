#!/usr/bin/env python3
"""Patch v1020 -> v1021: one photo in a chirp looks the same as several.
Before, a single photo used the general attachment preview (up to 240px, shrunk to fit with empty space at the
sides on wider screens) while several photos used the gallery (240px cropped on phones, up to 480px on wider
screens). Now a single photo goes through the gallery too (no count badge), and the gallery is one size
everywhere: full bubble width, 240px tall on phones / 320px on wider screens, cropped to fill. Tap opens the
whole photo. The fixed height also stops chirps jumping when someone else's photo finishes loading."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1020.js'
dst = '_deploy/assets/index-DUcNPOLc-v1021.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch(']}))( Mr(e.content))', ']}))(_cNorm(Mr(e.content)))', 'single photo -> gallery')
patch('src:_mtSrc(_cAtts[0].url),style:{width:`100%`,height:(window.innerWidth>=768?`auto`:240),maxHeight:window.innerWidth>=768?480:void 0,objectFit:window.innerWidth>=768?`contain`:`cover`,borderRadius:8',
      'src:_mtSrc(_cAtts[0].url),alt:``,style:{width:`100%`,height:window.innerWidth>=768?320:240,objectFit:`cover`,borderRadius:8', 'one size')
c += r'''
function _cNorm(r){try{if(r&&!r.attachments&&r.attachment&&r.attachment.type===`image`&&r.attachment.url)return{...r,attachments:[r.attachment],attachment:null}}catch(e){}return r}
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
