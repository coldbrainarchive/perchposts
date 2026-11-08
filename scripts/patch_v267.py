#!/usr/bin/env python3
"""Patch v266 -> v267: fix DM thread height — remove comments-panel class, fill full panel."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v266.js'
dst = '_deploy/assets/index-DUcNPOLc-v267.js'

content = open(src, encoding='utf-8').read()
errors = []

# Remove the comments-panel class (it forces height:min(600px,80dvh))
# and use inline flex styles that fill the available panel space
OLD = (
    'className:`content-card comments-panel`,'
    'style:{padding:0,overflow:`clip`,display:`flex`,flexDirection:`column`,'
    'height:`min(600px, 80dvh)`},'
)
NEW = (
    'style:{display:`flex`,flexDirection:`column`,flex:1,minHeight:0,'
    'overflow:`hidden`,background:`#161920`,borderRadius:0},'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: comments-panel class removed, thread fills full panel height')
else:
    # Try alternate form
    OLD2 = 'className:`content-card comments-panel`,style:{padding:0,overflow:`clip`,display:`flex`,flexDirection:`column`,flex:1,height:0},'
    if OLD2 in content:
        content = content.replace(OLD2, NEW, 1)
        print('OK: comments-panel class removed (alt form)')
    else:
        # Just patch whatever is there
        idx = content.find('className:`content-card comments-panel`')
        if idx != -1:
            end = content.find(',children:[', idx)
            old_frag = content[idx:end]
            content = content[:idx] + 'style:{display:`flex`,flexDirection:`column`,flex:1,minHeight:0,overflow:`hidden`}' + content[end:]
            print('OK: comments-panel replaced via index')
        else:
            errors.append('FAIL: comments-panel not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
