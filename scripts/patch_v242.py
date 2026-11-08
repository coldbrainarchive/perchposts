#!/usr/bin/env python3
"""Patch v241 -> v242: properly fix header div closing — keep } for props, add ) for jsx call."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v241.js'
dst = '_deploy/assets/index-DUcNPOLc-v242.js'

content = open(src, encoding='utf-8').read()
errors = []

# v241 has: }  )  ]  )  ,   (missing the } that closes header div props)
# Should be: }  )  ]  }  )  ,
# } = close span props
# ) = close span jsx
# ] = close header children[]
# } = close header div props   ← this is missing in v241
# ) = close header div (0,L.jsxs)(
# , = separator to msgs div
OLD = 'children:_dmThread})]),(0,L.jsx)(`div`,{style:{flex:1'
NEW = 'children:_dmThread})]}),(0,L.jsx)(`div`,{style:{flex:1'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: header div closing fixed — } restored, ) kept')
else:
    errors.append('FAIL: broken header not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

opens_p = content.count('(')
closes_p = content.count(')')
opens_b = content.count('{')
closes_b = content.count('}')
print(f'Parens: {opens_p-closes_p}, Braces: {opens_b-closes_b}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
