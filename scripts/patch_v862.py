#!/usr/bin/env python3
"""Patch v861 -> v862: region filters also keep posts whose headline names the region.
Matches the server: the region's own name only ("Africa", "Europe", "Latin America"...), whole words,
exact case, in the headline, description or typed text, never the link.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v861.js'
dst = '_deploy/assets/index-DUcNPOLc-v862.js'

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

helper = t(r'''var _RW={Africa:[`Africa`],Europe:[`Europe`],Asia:[`Asia`],"Middle East":[`Middle East`],"North America":[`North America`],"South America":[`South America`,`Latin America`],"Australia/Oceania":[`Oceania`]},_RWP={};function _rgnHit(e,f){if(_rgn(e)===f)return!0;let w=_RW[f];if(!w)return!1;let p=_RWP[f]||(_RWP[f]=new RegExp(`(?<![\\p{L}\\p{N}])(?:${w.join(`|`)})(?![\\p{L}\\p{N}])`,`u`)),c=e.content||``,x=[e.title||``,c.split(`[ATTACH`)[0]],m=c.match(/\[ATTACH:(\{.*\})\]/s);if(m)try{let a=JSON.parse(m[1]);x.push(a.title||``,a.description||``)}catch{}return p.test(x.join(` `))}''')
patch('function _rgn(e){', helper + 'function _rgn(e){', 'region name helper')
patch(t('.filter(e=>!d||(!m&&TagR!==null)||_rgn(e)===d)'), t('.filter(e=>!d||(!m&&TagR!==null)||_rgnHit(e,d))'), 'feed region filter')
patch(t('.filter(e=>!f||_rgn(e)===f).filter(e=>!p||_inHome(e,p))'), t('.filter(e=>!f||_rgnHit(e,f)).filter(e=>!p||_inHome(e,p))'), 'board region filter')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
