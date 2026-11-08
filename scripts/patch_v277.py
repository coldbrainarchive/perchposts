#!/usr/bin/env python3
"""Patch v276 -> v277: add empty state + loading indicator for search so users
don't see a blank page when their query returns no results."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v276.js'
dst = '_deploy/assets/index-DUcNPOLc-v277.js'

content = open(src, encoding='utf-8').read()
errors = []

# Replace the posts list end to add an empty state before the sentinel div.
# When m is set, SRLoading is false, SR is not null (fetch done), and both b and UR are empty
# → show "No results found" message.
OLD_END = 'o<b.length&&(0,L.jsx)(`div`,{ref:c,style:{height:1}})'
NEW_END = (
    # Loading indicator while search is in flight
    'm&&SRLoading&&(0,L.jsx)(`div`,{style:{padding:`32px 20px`,textAlign:`center`,color:`#64748b`,fontSize:13},children:`Searching…`}),'
    # Empty state: search done, no posts, no users
    'm&&!SRLoading&&SR!==null&&b.length===0&&UR.length===0&&(0,L.jsxs)(`div`,{style:{padding:`48px 20px`,textAlign:`center`,color:`#64748b`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:32,marginBottom:8},children:`🔍`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600,color:`#94a3b8`},children:`No results for "${m}"`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:12,marginTop:6},children:`Try a different spelling, or check if the user is registered`})]}),'
    'o<b.length&&(0,L.jsx)(`div`,{ref:c,style:{height:1}})'
)
if OLD_END in content:
    content = content.replace(OLD_END, NEW_END, 1)
    print('OK: empty state + loading indicator added')
else:
    errors.append('FAIL: sentinel div not found in home-feed')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
