#!/usr/bin/env python3
"""Patch v1165 -> v1166: the profile's Flaps tab shows the posts the person flapped. The page kept only posts written
by that person (fine for Posts), which threw away every flapped post (other people's). Flaps are sorted by when they
were flapped, newest first."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1165.js'
dst = '_deploy/assets/index-DUcNPOLc-v1166.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch(".filter(e=>!p||(e.username||``).toLowerCase()===p||(e.is_huddle&&_hxIn(e,p)))",
      ".filter(e=>!p||!!l.get(`flaps`)||(e.username||``).toLowerCase()===p||(e.is_huddle&&_hxIn(e,p)))", 'Flaps tab keeps flapped posts')
patch(".sort((e,t)=>{let n=(t.pinned_global?1:0)-(e.pinned_global?1:0);return n===0?(_srt===`flaps`||_srt===`chirps`)?",
      ".sort((e,t)=>{if(p&&l.get(`flaps`))return String(t.flapped_at||``).localeCompare(String(e.flapped_at||``));let n=(t.pinned_global?1:0)-(e.pinned_global?1:0);return n===0?(_srt===`flaps`||_srt===`chirps`)?", 'newest flap first')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
