#!/usr/bin/env python3
"""Patch v1022 -> v1023: older photos show their new small copy too.
Photos uploaded before v1022 have no "thumb" in the post/chirp; the server now keeps a small copy for them
(made by the 2026-11-12 media clean-up) and serves it at the photo's address + "?thumb=1" (falling back to the
photo itself if there isn't one). Chirps, postcards, the post page and notifications use that."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1022.js'
dst = '_deploy/assets/index-DUcNPOLc-v1023.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('return l!==a.url?l:(a.thumb||a.url)}', 'return l!==a.url?l:_mtThumbOf(a)}', 'chirps / postcards / post page')
patch('image:p?.type===`image`?(p.thumb||p.url):', 'image:p?.type===`image`?_mtThumbOf(p):', 'preview card')
patch('img:(_s?.[0]?(_s[0].thumb||_s[0].url):null)||(_a?.type===`image`?(_a.thumb||_a.url):', 'img:(_s?.[0]?_mtThumbOf(_s[0]):null)||(_a?.type===`image`?_mtThumbOf(_a):', 'notifications')
c += r'''
function _mtThumbOf(a){try{if(!a)return``;if(a.thumb)return a.thumb;const u=a.url||``;return/^https:\/\/daboysforumip\.coldbrainarchive\.workers\.dev\/media\/[A-Za-z0-9][A-Za-z0-9._-]*$/.test(u)?u+`?thumb=1`:u}catch(e){return a&&a.url||``}}
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
