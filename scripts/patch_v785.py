#!/usr/bin/env python3
"""Patch v784 -> v785:
Choosing a chip replaces what was being typed.
The search box registers keystrokes 250ms late, so clicking a chip while typing let the late
keystrokes overwrite it: "Russi" became the search (0 results), and "Europ" came back after a
continent chip. Choosing a chip now cancels the pending keystrokes and drops the typed search.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v784.js'
dst = '_deploy/assets/index-DUcNPOLc-v785.js'

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

patch(t('function ee(n){let i=new URLSearchParams(e);i.set(`board`,n),t(i),'),
      t('function ee(n){clearTimeout(c.current?._dbt);let i=new URLSearchParams(e);i.set(`board`,n),i.delete(`q`),t(i),'),
      'board chip replaces typing')
patch(t('function D(n){let i=new URLSearchParams(e);i.set(`continent`,n),i.delete(`country`),t(i),'),
      t('function D(n){clearTimeout(c.current?._dbt);let i=new URLSearchParams(e);i.set(`continent`,n),i.delete(`country`),i.delete(`q`),t(i),'),
      'continent chip replaces typing')
patch(t('function O(e){s(e),r(``);'),
      t('function O(e){clearTimeout(c.current?._dbt);s(e),r(``);'),
      'continent list replaces typing')
patch(t('function k(n){let i=new URLSearchParams(e);i.set(`country`,n),i.delete(`continent`),t(i),'),
      t('function k(n){clearTimeout(c.current?._dbt);let i=new URLSearchParams(e);i.set(`country`,n),i.delete(`continent`),i.delete(`q`),t(i),'),
      'country chip replaces typing')

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
