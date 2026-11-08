#!/usr/bin/env python3
"""Patch v465 -> v466: Bump Safari bird badge fontSize from 11 to 12."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v465.js'
dst = '_deploy/assets/index-DUcNPOLc-v466.js'

content = open(src, encoding='utf-8').read()

OLD = 'var _bsz=/Chrome\\//.test(navigator.userAgent)&&!/Edg\\//.test(navigator.userAgent)?15:11;'
NEW = 'var _bsz=/Chrome\\//.test(navigator.userAgent)&&!/Edg\\//.test(navigator.userAgent)?15:12;'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Safari fontSize 11 → 12')
else:
    print('FAIL: constant not found'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
