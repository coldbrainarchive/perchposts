#!/usr/bin/env python3
"""Patch v809 -> v810: the loading bird is all purple, including its beak and eye."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v809.js'
dst = '_deploy/assets/index-DUcNPOLc-v810.js'

content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label, count=1):
    global content
    n = content.count(old)
    if n != count:
        errors.append('FAIL (' + label + '): expected ' + str(count) + ' matches, found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

patch('<path fill="#fbbf24" d="m51 20 7 3-7 3z"/>', '<path fill="#9d5fe0" d="m51 20 7 3-7 3z"/>', 'beak')
patch('<circle fill="#14161c" cx="46" cy="21.5" r="1.4"/>', '<circle fill="#4c1d95" cx="46" cy="21.5" r="1.4"/>', 'eye')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
