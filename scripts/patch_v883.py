#!/usr/bin/env python3
"""Patch v880 -> v883: the search-bar cursor fix from v882, without v881's typing recorder.
Only restore the saved cursor when the text is unchanged since it was saved and the cursor actually moved, so a
letter typed while the tag suggestions update no longer sends the cursor backwards. Verified on the user's iPhone
via iPhone Mirroring: "united kingdom" typed with pauses came out intact (v881 gave "uited kingdomn").
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v880.js'
dst = '_deploy/assets/index-DUcNPOLc-v883.js'
content = open(src, encoding='utf-8').read()

old = 'requestAnimationFrame(()=>{if(c.current&&document.activeElement===c.current)c.current.setSelectionRange(_sc,_sc);'
new = 'requestAnimationFrame(()=>{if(c.current&&document.activeElement===c.current&&c.current.value===_sv&&c.current.selectionStart!==_sc)c.current.setSelectionRange(_sc,_sc);'
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old))); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
