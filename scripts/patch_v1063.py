#!/usr/bin/env python3
"""Patch v1062 -> v1063: the admin/mod globe on profile cards uses the same design as the one on chirps (globe with
two curved latitude lines and two meridians), in the card's role colour."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1062.js'
dst = '_deploy/assets/index-DUcNPOLc-v1063.js'
c = open(src, encoding='utf-8').read()
def seg(s, pat):
    i = s.find(pat); assert i >= 0 and s.count(pat) == 1, pat
    j = s.find('(', i + len('(0,L.jsxs)')); d = 0; k = j
    while True:
        if s[k] == '(': d += 1
        elif s[k] == ')':
            d -= 1
            if d == 0: return s[i:k+1]
        k += 1
card = seg(c, '(0,L.jsxs)(`svg`,{width:14,height:14')
chirp = seg(c, '(0,L.jsxs)(`svg`,{width:`14`')
new = chirp.replace('stroke:`#0a0a0a`', 'stroke:k').replace('url(#bcc)', 'url(#bcg)').replace('id:`bcc`', 'id:`bcg`')
assert new.count('stroke:k') == 6, new.count('stroke:k')
c = c.replace(card, new); print('OK: card globe matches chirp globe')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
