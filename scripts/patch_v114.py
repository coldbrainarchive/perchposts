#!/usr/bin/env python3
"""Patch v113 -> v114: remove client-side cage block from post submit.

The server already auto-redirects jailed posts to the cage board, so the
client doesn't need to block the submit. The modal was firing because of a
slug/case mismatch in the h check, blocking the request before it reached
the server.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v113.js'
dst = '_deploy/assets/index-DUcNPOLc-v114.js'

content = open(src, encoding='utf-8').read()
errors = []

# Remove the client-side cage check in ae() — server handles it
OLD = 'if(p&&h!==`cage`){_showBlock("You’re caged — you can only post and comment in the \U0001fab9 Cage tag.","caged");return};'
if OLD in content:
    content = content.replace(OLD, '', 1)
    print('OK: removed client cage block from post submit')
else:
    errors.append('FAIL: client cage block not found')
    # Try to find it
    idx = content.find('if(p&&h!==`cage`)')
    if idx >= 0:
        print(f'  Found at {idx}: {repr(content[idx:idx+120])}')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
