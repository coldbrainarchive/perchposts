#!/usr/bin/env python3
"""Patch v106 -> v107: fix TDZ in send-button onClick handler.

The onClick declares 'let e=f' (comment text) in the same arrow scope that
first reads 'e' as the outer user prop. Safari/JSC strictly enforces TDZ;
Chrome is lenient. Fix: rename inner 'e' to '_txt' throughout the handler.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v106.js'
dst = '_deploy/assets/index-DUcNPOLc-v107.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'onClick:()=>{if(!e||!f.trim())return;let e=f,t=S?.id||null;p(``),C(null),O.current=!0,F(e,t)}'
NEW = 'onClick:()=>{if(!e||!f.trim())return;let _txt=f,t=S?.id||null;p(``),C(null),O.current=!0,F(_txt,t)}'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: renamed let e=f -> let _txt=f in send onClick')
else:
    errors.append('FAIL: onClick TDZ pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
