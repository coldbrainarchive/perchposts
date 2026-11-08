#!/usr/bin/env python3
"""Patch v363 -> v364: navigate to new post page after successful submit (post or huddle)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v363.js'
dst = '_deploy/assets/index-DUcNPOLc-v364.js'

content = open(src, encoding='utf-8').read()
errors = []

# After successful post, currently navigates to r('/') — change to r('/post/'+id)
OLD = 'o(``),c(``),u(!1),r(`/`)'
NEW = 'o(``),c(``),_setHmTagged([]),_setIsHuddle(!1),u(!1),r(`/post/${g.post?.id}`)'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: navigate to new post page after submission')
else:
    errors.append('FAIL: post success handler not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
