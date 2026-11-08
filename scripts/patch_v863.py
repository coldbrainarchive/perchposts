#!/usr/bin/env python3
"""Patch v862 -> v863: region filters also match the region's country names, like the server.
A BBC story about Kenya shows under Africa. Georgia, Jordan, Chad and Turkey go by tags only (they mostly
mean a US state, people or Thanksgiving); Türkiye is searched; Guinea skips "Papua New Guinea".
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v862.js'
dst = '_deploy/assets/index-DUcNPOLc-v863.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n != 1:
        errors.append('FAIL (' + label + '): found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

def t(s):
    return s.replace('`', q)

patch(t('_RWP={};function _rgnHit'), t('_RWP={},_NS=new Set([`Georgia`,`Jordan`,`Chad`,`Turkey`]),_NA={"Bosnia & Herzegovina":[`Bosnia`],"Trinidad & Tobago":[`Trinidad`],Turkey:[`Türkiye`]};function _rgnHit'), 'name rules')
patch(t('${w.join(`|`)}'), t('${w.concat(Object.keys(ar).filter(c=>ar[c]===f).flatMap(c=>_NA[c]||(_NS.has(c)?[]:[c]))).map(n=>n===`Guinea`?`(?<!New )Guinea`:n).join(`|`)}'), 'country names in region pattern')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
