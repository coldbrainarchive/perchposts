#!/usr/bin/env python3
"""Patch v799 -> v800:
Desktop chat header shows the chirp count again, next to the huddle name or headline.
It sits outside the title so a long headline can't cut it off. Phones don't show it: the
preview's "View all" button and the post's chirp button already carry the number.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v799.js'
dst = '_deploy/assets/index-DUcNPOLc-v800.js'

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

patch(t('(0,L.jsxs)(`span`,{className:`comments-panel-title`,onClick:_cf?_closeC:void 0,children:[_ct]})]}),'),
      t('(0,L.jsxs)(`span`,{className:`comments-panel-title`,onClick:_cf?_closeC:void 0,children:[_ct]}),(0,L.jsx)(`span`,{className:`chat-count`,children:`${_cn} Chirp${_cn===1?``:`s`}`})]}),'),
      'chirp count beside the title')
patch('.chat-full .comments-panel-title{cursor:pointer}',
      '.chat-full .comments-panel-title{cursor:pointer}.chat-count{display:none}@media(min-width:768px){.chat-count{display:inline;flex:none;color:#94a3b8;font-size:13px;font-weight:600;white-space:nowrap;margin-right:10px}}',
      'count style: desktop only')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print('Paren delta: ' + str(p_delta) + ', Brace delta: ' + str(b_delta))
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
