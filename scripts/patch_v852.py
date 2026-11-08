#!/usr/bin/env python3
"""Patch v851 -> v852: the 🤖 moves with a transform on an inner span, because tiny padding changes did almost
nothing on iPhone (text snaps to whole pixels there, a transform doesn't). It centres on the head, not the
antenna. iPhone values come from a real screenshot: head 0.23px right and 0.3px low.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v851.js'
dst = '_deploy/assets/index-DUcNPOLc-v852.js'

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

def t(s):
    return s.replace('`', q)

patch(t('className:`post-badge bot`,children:`🤖`'), t('className:`post-badge bot`,children:(0,L.jsx)(`span`,{className:`post-badge-i`,children:`🤖`})'), 'inner span', 2)
patch('.post-badge.bot{padding:1px 0 0 3px}@supports (-webkit-touch-callout:none){.post-badge{padding:0 0 .7px 1.4px}.post-badge.bot{padding:1px 0 0 .7px}}',
      '.post-badge.bot{padding:0 0 0 3px}.post-badge-i{display:block;transform:translateY(-.1px)}'
      '@supports (-webkit-touch-callout:none){.post-badge{padding:0 0 .7px 1.4px}.post-badge.bot{padding:1px 0 0 .7px}.post-badge-i{transform:translate(-.25px,-.3px)}}', 'nudge')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
