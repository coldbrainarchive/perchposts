#!/usr/bin/env python3
"""Patch v849 -> v850: the 🤖 badge uses the same circle and emoji size as 📌 🔒 📦, with the same centring.
It keeps a grey ring, because amber marks things mods switch on.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v849.js'
dst = '_deploy/assets/index-DUcNPOLc-v850.js'

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

BASE = 'display:`inline-flex`,alignItems:`center`,justifyContent:`center`,height:20,width:20,borderRadius:999,border:`1px solid #323b48`,background:`#20262f`,fontSize:13,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`'
patch(t('onClick:_e=>m(`bot`,`1`,_e),style:{' + BASE + ',cursor:`pointer`},children:`🤖`'), t('onClick:_e=>m(`bot`,`1`,_e),className:`post-badge bot`,children:`🤖`'), 'feed')
patch(t('(0,L.jsx)(`span`,{style:{' + BASE + '},children:`🤖`'), t('(0,L.jsx)(`span`,{className:`post-badge bot`,children:`🤖`'), 'post page')
old = '.chat-section-title{display:flex;'
patch(old, '.post-badge.bot{border-color:#323b48;background:#20262f}button.post-badge{cursor:pointer}' + old, 'style')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
