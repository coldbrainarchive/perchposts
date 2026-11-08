#!/usr/bin/env python3
"""Patch v881 -> v882: fix the search-bar cursor jumping while typing.

Recorded on the user's iPhone (v881's typing recorder, real keyboard through iPhone Mirroring): 250ms after a
keystroke the search box saves the cursor position, applies the search, and when the tag suggestions re-render it
moves the cursor back to the saved spot. If another letter is typed in that gap, the saved spot is stale:
"u" -> save 1 -> type "n" ("un", cursor 2) -> tags update -> cursor forced to 1 -> every later letter lands before
the "n" ("uited kingdomn").

Fix: only restore when the text is still exactly what it was when the position was saved, and only if the cursor
actually moved. Keeps v881's recorder for verification; v883 drops it.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v881.js'
dst = '_deploy/assets/index-DUcNPOLc-v882.js'
content = open(src, encoding='utf-8').read()

old = 'requestAnimationFrame(()=>{if(c.current&&document.activeElement===c.current)c.current.setSelectionRange(_sc,_sc);'
new = 'requestAnimationFrame(()=>{if(c.current&&document.activeElement===c.current&&c.current.value===_sv&&c.current.selectionStart!==_sc)c.current.setSelectionRange(_sc,_sc);'
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old))); sys.exit(1)
content = content.replace(old, new)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
