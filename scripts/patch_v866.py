#!/usr/bin/env python3
"""Patch v865 -> v866: the page's own edge swipe only runs in the home-screen app.
Safari and Chrome already go back on an edge swipe, so the page's handler could add a second step back:
from a post past its board feed to the main feed at the top. The home-screen app has no browser swipe,
so it keeps the handler.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v865.js'
dst = '_deploy/assets/index-DUcNPOLc-v866.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label, count=1):
    global content
    n = content.count(old)
    if n != count:
        errors.append('FAIL (' + label + '): found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

swipe = 'if(_sx<50&&_dx>60&&Math.abs(_dx)>Math.abs(_dy)*1.5)'
app = 'if((navigator.standalone||matchMedia(`(display-mode: standalone)`).matches)&&_sx<50&&_dx>60&&Math.abs(_dx)>Math.abs(_dy)*1.5)'.replace('`', q)
patch(swipe + 'r(-1);', app + 'r(-1);', 'new post page swipe')
patch(swipe + 'o(-1);', app + 'o(-1);', 'post page swipe')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
