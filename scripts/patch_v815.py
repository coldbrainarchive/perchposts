#!/usr/bin/env python3
"""Patch v814 -> v815: the notifications/Nest panel uses the main header's colour (#16171d, was #0b0f12)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v814.js'
dst = '_deploy/assets/index-DUcNPOLc-v815.js'

q = chr(0x60)
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

def t(s):
    return s.replace('`', q)

patch(t('width:`min(420px, 100vw)`,background:`#0b0f12`,borderLeft:'),
      t('width:`min(420px, 100vw)`,background:`#16171d`,borderLeft:'),
      'panel')
patch(t('borderBottom:e?`1px solid #2e303a`:`none`,position:`relative`,background:`#0b0f12`}'),
      t('borderBottom:e?`1px solid #2e303a`:`none`,position:`relative`,background:`#16171d`}'),
      'panel top')

# The old row line nearly vanishes on the lighter panel
patch(t('borderBottom:`1px solid #1a1c23`,background:t?`rgba(192,132,252,0.07)`'),
      t('borderBottom:`1px solid #2e303a`,background:t?`rgba(192,132,252,0.07)`'),
      'row lines')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
