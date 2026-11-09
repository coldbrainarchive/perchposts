#!/usr/bin/env python3
"""Patch v922 -> v924 (v923 folded in): one purple. Everything that used the darker #7c3aed now uses the
site's purple #c084fc (logo, names, toggles): the chirp send button, DM send button and your own DM bubbles,
your reactions, and the chirp send animation. Text/arrows on that purple are dark (#14081d), like the
site's other purple pills."""
import re, sys
src = '_deploy/assets/index-DUcNPOLc-v922.js'
dst = '_deploy/assets/index-DUcNPOLc-v924.js'
content = open(src, encoding='utf-8').read()
# 1. dark text wherever the old purple was a background with white text (CSS)
content, n = re.subn(r'background: #7c3aed;(\s*)color: #fff(?:fff)?;', r'background: #c084fc;\1color: #14081d;', content)
print('css purple+white -> purple+dark:', n)
# 2. chirp send button (inline): dark arrow when active
old = 'background:_cA?`#7c3aed`:`rgba(255,255,255,0.08)`,color:`#fff`'
if content.count(old) != 1: print('FAIL send btn', content.count(old)); sys.exit(1)
content = content.replace(old, 'background:_cA?`#c084fc`:`rgba(255,255,255,0.08)`,color:_cA?`#14081d`:`#fff`')
# 3. animation: dark text through the purple phase
k = content.index('window._chirpFly=function'); head, tail = content[:k], content[k:]
tail = tail.replace("borderRadius:'28px',background:'#7c3aed',borderColor:'#7c3aed',boxShadow", "borderRadius:'28px',background:'#7c3aed',borderColor:'#7c3aed',color:'#14081d',boxShadow", 1)
tail = tail.replace("background:'#7c3aed',fontSize:cs.fontSize,padding:cs.padding,borderColor:'#7c3aed',boxShadow", "background:'#7c3aed',fontSize:cs.fontSize,padding:cs.padding,borderColor:'#7c3aed',color:'#14081d',boxShadow")
tail = tail.replace("color:'rgba(248,250,252,1)'", "color:'rgba(20,8,29,1)'").replace("color:'rgba(248,250,252,0)'", "color:'rgba(20,8,29,0)'")
content = head + tail
# 4. every remaining old purple -> site purple
a, b = content.count('#7c3aed'), content.count('rgba(124,58,237,')
content = content.replace('#7c3aed', '#c084fc').replace('rgba(124,58,237,', 'rgba(192,132,252,')
print('remaining hex', a, 'rgba', b, '-> replaced')
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
