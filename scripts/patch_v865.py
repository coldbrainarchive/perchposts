#!/usr/bin/env python3
"""Patch v864 -> v865: only the admin and mods can post in Announcements.
The board picker hides Announcements for everyone else, and a /new?board=announcements link falls back
to Random for them. The server refuses it too.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v864.js'
dst = '_deploy/assets/index-DUcNPOLc-v865.js'

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

patch(t('g]=(0,_.useState)(localStorage.getItem(`_caged`)===`1`?`cage`:sr(i.get(`board`))?.slug||`random`)'),
      t('g]=(0,_.useState)(localStorage.getItem(`_caged`)===`1`?`cage`:(_b=>_b===`announcements`&&![`mod`,`admin`].includes(Qn()?.role)?`random`:_b)(sr(i.get(`board`))?.slug)||`random`)'),
      'non-mods cannot start in Announcements')
patch(t('nr.filter(e=>!e.virtual&&e.slug!==`feedback`).map(e=>(0,L.jsx)(`button`,{className:`search-suggestion`'),
      t('nr.filter(e=>!e.virtual&&e.slug!==`feedback`&&(e.slug!==`announcements`||[`mod`,`admin`].includes(Qn()?.role))).map(e=>(0,L.jsx)(`button`,{className:`search-suggestion`'),
      'hide Announcements from non-mods')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
