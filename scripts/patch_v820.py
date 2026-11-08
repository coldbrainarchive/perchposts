#!/usr/bin/env python3
"""Patch v819 -> v820:
Pinned chirps lose the purple tint and left bar, so the glow alone marks them.
The phone preview shows pinned chirps at the top, then the latest 5 other chirps. The list is drawn
bottom up (column-reverse), so the pinned ones go last in _rev to land on top.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v819.js'
dst = '_deploy/assets/index-DUcNPOLc-v820.js'

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

patch(t('onClick:()=>!p&&y(e=>!e),style:e.pinned?{background:`rgba(192,132,252,0.12)`,borderLeft:`3px solid #c084fc`,paddingLeft:8}:void 0,children:['),
      t('onClick:()=>!p&&y(e=>!e),children:['),
      'remove pinned tint')
patch(t('if(_pv)_rev=_rev.slice(0,5);'),
      t('if(_pv)_rev=[..._rev.filter(_x=>!_x.pinned).slice(0,5),..._rev.filter(_x=>_x.pinned)];'),
      'pinned at top of preview')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
