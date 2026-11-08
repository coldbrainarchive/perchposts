#!/usr/bin/env python3
"""Patch v785 -> v786:
A country pill takes the place of the typed word: the box shows only the pill. The feed still
searches for the country's name behind it (Vr derives the search from ?country= when ?q= is empty).
Links saved with both ?country=X&q=X also drop the duplicate text.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v785.js'
dst = '_deploy/assets/index-DUcNPOLc-v786.js'

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

patch(t('[qM,setQM]=(0,_.useState)(!1),_pc=(0,_.useRef)(``);'
        '(0,_.useEffect)(()=>{let _was=_pc.current;_pc.current=p;if(p===_was)return;'
        'let _v=(c.current?.value||``).trim().toLowerCase(),_same=!_v||_v===_was.toLowerCase();'
        'if(_same){r(p);if(c.current)c.current.value=p}},[p]);'),
      t('[qM,setQM]=(0,_.useState)(!1);'
        '(0,_.useEffect)(()=>{if(p&&(c.current?.value||``).trim().toLowerCase()===p.toLowerCase()){r(``);c.current.value=``}},[p]);'),
      'pill replaces the typed country')

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
