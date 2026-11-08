#!/usr/bin/env python3
"""Patch v811 -> v812:
Times read "just now" under a minute (this also covers phones whose clock runs behind, which gave
"-2s ago"), then 5m, 3h, 12d as before, then months from day 30 and years from day 365.
A month is counted as 30 days, so days 360-364 read "12mo ago" before day 365 reads "1y ago".
"active ..." on profiles uses the same wording once it's a day or more.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v811.js'
dst = '_deploy/assets/index-DUcNPOLc-v812.js'

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

patch(t('return n<60?`${n}s ago`:n<3600?`${Math.floor(n/60)}m ago`:n<86400?`${Math.floor(n/3600)}h ago`:`${Math.floor(n/86400)}d ago`}'),
      t('return n<60?`just now`:n<3600?`${Math.floor(n/60)}m ago`:n<86400?`${Math.floor(n/3600)}h ago`:n<2592e3?`${Math.floor(n/86400)}d ago`:n<31536e3?`${Math.floor(n/2592e3)}mo ago`:`${Math.floor(n/31536e3)}y ago`}'),
      'time wording')
patch(t('` · active ${Math.round(d/1440)}d ago`'),
      t('` · active ${Un(n.last_active)}`'),
      'profile active wording')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
