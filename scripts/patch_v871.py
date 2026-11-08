#!/usr/bin/env python3
"""Patch v870 -> v871: remove the 🤖 badge from bot posts, in the feed and on the post page, as asked.
The badge row now only shows for pinned, locked or archived posts. The bots' own 🤖 profile icon and the
"🤖 Bots" filter chip are unchanged.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v870.js'
dst = '_deploy/assets/index-DUcNPOLc-v871.js'

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

for v in ('e', 'c'):
    patch(t('(' + v + '.pinned||' + v + '.locked||' + v + '.frozen||' + v + '.browser_id&&String(' + v + '.browser_id).startsWith(`bot-`))&&(0,L.jsxs)(`div`,{className:`post-badges`'),
          t('(' + v + '.pinned||' + v + '.locked||' + v + '.frozen)&&(0,L.jsxs)(`div`,{className:`post-badges`'), 'badge row only when needed (' + v + ')')
patch(t(',e.browser_id&&String(e.browser_id).startsWith(`bot-`)&&(0,L.jsx)(`button`,{type:`button`,onClick:_e=>m(`bot`,`1`,_e),className:`post-badge bot`,children:(0,L.jsx)(`span`,{className:`post-badge-i`,children:`🤖`})})]'),
      ']', 'feed bot badge')
patch(t(',c.browser_id&&String(c.browser_id).startsWith(`bot-`)&&(0,L.jsx)(`span`,{className:`post-badge bot`,children:(0,L.jsx)(`span`,{className:`post-badge-i`,children:`🤖`})})]'),
      ']', 'post page bot badge')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
