#!/usr/bin/env python3
"""Patch v219 -> v220: Flock board shows all posts — remove bot engagement gate."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v219.js'
dst = '_deploy/assets/index-DUcNPOLc-v220.js'

content = open(src, encoding='utf-8').read()
errors = []

# The activity board filter currently hides bot posts with no engagement.
# Replace: y ? fr.includes(e.username) ? (has comments or votes) : !0
# With:    y ? !0   (show everything on the Flock board)
OLD = (
    'b=_bl.filter(e=>u?y?fr.includes(e.username)?'
    '(n[e.id]||0)>0||(i[e.id]?.voteCount??0)>0:!0:'
    'cr(e)===(sr(u)?.name||u):!0)'
)
NEW = (
    'b=_bl.filter(e=>u?y?!0:'
    'cr(e)===(sr(u)?.name||u):!0)'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Flock board now shows all posts')
else:
    errors.append('FAIL: activity filter not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
