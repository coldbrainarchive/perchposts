#!/usr/bin/env python3
"""Patch v788 -> v789:
A country pill on its own runs only its search. It also fetched a 4,000-row country window whose
results the search replaced straight away. While the search loads, the home list shows matches.
Pills combined with a board, region, user or a different typed word still fetch as before.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v788.js'
dst = '_deploy/assets/index-DUcNPOLc-v789.js'

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

patch('(0,_.useEffect)(()=>{if(!u&&!d&&!f&&!p){setTagR(null);return}',
      '(0,_.useEffect)(()=>{if(!u&&!d&&!p&&(!f||_cs)){setTagR(null);return}',
      'skip window fetch for a lone country pill')
patch('return()=>{_c=!0}},[u,d,f,p])',
      'return()=>{_c=!0}},[u,d,f,p,_cs])',
      'rerun when pill and word stop matching')

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
