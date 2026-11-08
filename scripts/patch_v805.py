#!/usr/bin/env python3
"""Patch v804 -> v805:
Remove the temporary ?vvdebug sizes readout. The Chrome fix from v804 stays.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v804.js'
dst = '_deploy/assets/index-DUcNPOLc-v805.js'

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

start_mark = t('_ts=[],_bi=`inner ')
end_mark = '_f=()=>{cancelAnimationFrame(_r);'
if content.count(start_mark) != 1 or content.count(end_mark) != 1:
    errors.append('FAIL: readout block not found exactly once')
else:
    a = content.index(start_mark) + len('_ts=[],')
    b = content.index(end_mark)
    block = content[a:b]
    if not (block.startswith('_bi=') and block.endswith('},') and 'vvdebug' in block and len(block) < 2500):
        errors.append('FAIL: readout block looks wrong (' + str(len(block)) + ' chars)')
    else:
        content = content[:a] + content[b:]
        print('OK: remove readout (' + str(len(block)) + ' chars)')

patch(t('.test(document.activeElement?.tagName||``));_dg()})}'),
      t('.test(document.activeElement?.tagName||``))})}'),
      'stop calling the readout')
patch(t('document.getElementById(`vvd`)?.remove();'), '', 'no readout to clean up')

for gone in ('vvdebug', '_dg(', 'vvd'):
    if gone in content:
        errors.append('FAIL: still contains ' + gone)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
