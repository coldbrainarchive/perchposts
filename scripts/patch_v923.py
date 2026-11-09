#!/usr/bin/env python3
"""NOT DEPLOYED (folded into v924). Patch v922 -> v923: the chirp send animation uses the site's purple #c084fc (logo, name, toggle sliders)
instead of the send button's #7c3aed, with dark text (#14081d) on it like the site's other purple pills."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v922.js'
dst = '_deploy/assets/index-DUcNPOLc-v923.js'
content = open(src, encoding='utf-8').read()
k = content.index('window._chirpFly=function')
head, tail = content[:k], content[k:]
n1 = tail.count("'#7c3aed'"); n2 = tail.count('rgba(124,58,237,')
tail = tail.replace("'#7c3aed'", "'#c084fc'").replace('rgba(124,58,237,', 'rgba(192,132,252,')
# dark text while purple: flight keyframes get color #14081d; landing fades it out
tail = tail.replace("borderRadius:'28px',background:'#c084fc',borderColor:'#c084fc',boxShadow", "borderRadius:'28px',background:'#c084fc',borderColor:'#c084fc',color:'#14081d',boxShadow", 1)
tail = tail.replace("color:'rgba(248,250,252,1)'", "color:'rgba(20,8,29,1)'").replace("color:'rgba(248,250,252,0)'", "color:'rgba(20,8,29,0)'")
tail = tail.replace("background:'#c084fc',fontSize:cs.fontSize,padding:cs.padding,borderColor:'#c084fc',boxShadow", "background:'#c084fc',fontSize:cs.fontSize,padding:cs.padding,borderColor:'#c084fc',color:'#14081d',boxShadow")
print('replaced', n1, 'hex and', n2, 'rgba')
content = head + tail
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
