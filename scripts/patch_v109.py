#!/usr/bin/env python3
"""Patch v108 -> v109: remove _showBlock auto-dismiss timeout."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v108.js'
dst = '_deploy/assets/index-DUcNPOLc-v109.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'o.onclick=function(){o.remove()};document.body.appendChild(o);setTimeout(function(){if(o.parentNode)o.remove()},5000)'
NEW = 'o.onclick=function(){o.remove()};document.body.appendChild(o)'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: removed _showBlock auto-dismiss timeout')
else:
    errors.append('FAIL: _showBlock setTimeout not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
