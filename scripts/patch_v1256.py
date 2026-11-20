#!/usr/bin/env python3
"""Patch v1255 -> v1256: a more minimal Perch News globe drawn like the other space icons (24 grid, same stroke):
outer circle, one line across the middle, one meridian. Uses the shared _SPK icon path, so it's the same weight."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1255.js'
dst = '_deploy/assets/index-DUcNPOLc-v1256.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
HEAD = '<svg class="ri" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
G = HEAD + '<circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19"/><path d="M12 2.5c-2.7 2.7-4 5.9-4 9.5s1.3 6.8 4 9.5c2.7-2.7 4-5.9 4-9.5s-1.3-6.8-4-9.5z"/></svg>'
patch('function _ppIco(k){return ({', 'function _ppIco(k){return ({"PNGLOBE": "%s", ' % G.replace('"', '\\"'), 'minimal globe icon')
patch('const _SPK={activity:`BIRDHEAD`,', 'const _SPK={botnews:`PNGLOBE`,activity:`BIRDHEAD`,', 'Perch News uses it')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
