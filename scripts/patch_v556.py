#!/usr/bin/env python3
"""Patch v555 -> v556:
After selecting a board, continent, or country from the search dropdown, clear
the visible input text (c.current.value) in addition to the React state r('').
This lets the user immediately type a keyword on top of the selected filter.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v555.js'
dst = '_deploy/assets/index-DUcNPOLc-v556.js'

content = open(src, encoding='utf-8').read()
errors = []

patches = [
    # Board select
    (
        'function ee(n){let i=new URLSearchParams(e);i.set(`board`,n),t(i),r(``),s(null),a(!1)}',
        'function ee(n){let i=new URLSearchParams(e);i.set(`board`,n),t(i),r(``),s(null),a(!1);if(c.current){c.current.value=``;c.current.focus();}}',
        'ee (board select)'
    ),
    # Continent select
    (
        'function D(n){let i=new URLSearchParams(e);i.set(`continent`,n),i.delete(`country`),t(i),r(``)}',
        'function D(n){let i=new URLSearchParams(e);i.set(`continent`,n),i.delete(`country`),t(i),r(``);if(c.current){c.current.value=``;c.current.focus();}}',
        'D (continent select)'
    ),
    # Continent drill-down (O sets the sub-state, keeps dropdown open)
    (
        'function O(e){s(e),r(``)}',
        'function O(e){s(e),r(``);if(c.current)c.current.value=``;}',
        'O (continent drill-down)'
    ),
    # Country select
    (
        'function k(n){let i=new URLSearchParams(e);i.set(`country`,n),i.delete(`continent`),t(i),r(``),s(null),c.current?.focus()}',
        'function k(n){let i=new URLSearchParams(e);i.set(`country`,n),i.delete(`continent`),t(i),r(``),s(null);if(c.current){c.current.value=``;c.current.focus();}}',
        'k (country select)'
    ),
]

for old, new, label in patches:
    if old in content:
        content = content.replace(old, new, 1)
        print(f'OK: {label}')
    else:
        errors.append(f'FAIL: {label} not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
