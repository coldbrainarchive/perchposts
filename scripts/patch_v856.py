#!/usr/bin/env python3
"""Patch v855 -> v856: tapping the photo closes the photo viewer, on cards, the post page and chirps.
Several photos: on touch screens swiping already changes photo, so the tap zones go and any tap on the photo
closes it. With a mouse there's no swipe, so the side zones stay and a click on the middle closes it.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v855.js'
dst = '_deploy/assets/index-DUcNPOLc-v856.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []
for v in ('_pAtts', '_cAtts', '_tAtts'):
    old = ('_ov.appendChild(_im);_ov.appendChild(_hdr);if(' + v + '.length>1){_ov.appendChild(_dots);_ov.appendChild(_lz);_ov.appendChild(_rz);}')
    new = ('_im.style.cursor=`zoom-out`;_im.onclick=_e=>{_e.stopPropagation();_close()};_ov.appendChild(_im);_ov.appendChild(_hdr);if(' + v + '.length>1){_ov.appendChild(_dots);if(!matchMedia(`(hover:none)`).matches){_ov.appendChild(_lz);_ov.appendChild(_rz);}}').replace('`', q)
    if content.count(old) != 1:
        errors.append('FAIL ' + v + ': found ' + str(content.count(old)))
    content = content.replace(old, new)
if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
