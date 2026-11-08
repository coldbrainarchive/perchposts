#!/usr/bin/env python3
"""Patch v863 -> v864: country pills use the same name rule as region tabs.
A pill keeps its tagged posts plus posts naming the country as a whole word, exact case, in the headline,
description or typed text (never the link), so every pill adds up to its region tab.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v863.js'
dst = '_deploy/assets/index-DUcNPOLc-v864.js'

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

helper = t(r'''function _rtx(e){let c=e.content||``,x=[e.title||``,c.split(`[ATTACH`)[0]],m=c.match(/\[ATTACH:(\{.*\})\]/s);if(m)try{let a=JSON.parse(m[1]);x.push(a.title||``,a.description||``)}catch{}return x.join(` `)}function _cnHit(e,c){let k=`c:`+c,p=_RWP[k]||(_RWP[k]=new RegExp(`(?<![\\p{L}\\p{N}])(?:${[...new Set([c,...(_NA[c]||[])])].map(n=>n===`Guinea`?`(?<!New )Guinea`:n).join(`|`)})(?![\\p{L}\\p{N}])`,`u`));return p.test(_rtx(e))}''')
patch('function _rgnHit(e,f){', helper + 'function _rgnHit(e,f){', 'country name helper')
patch(t('if(!m||(_cs&&_inHome(e,f)))return!0;'), t('if(!m)return!0;if(_cs)return _inHome(e,f)||_cnHit(e,f);'), 'country pill filter')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
