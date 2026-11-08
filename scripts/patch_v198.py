#!/usr/bin/env python3
"""Patch v197 -> v198: reset highlight guard when highlight param changes."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v197.js'
dst = '_deploy/assets/index-DUcNPOLc-v198.js'

content = open(src, encoding='utf-8').read()
errors = []

# The highlight scroll effect checks k.current and bails if true.
# k.current is never reset, so clicking a notification while already on the post
# page does nothing. We inject a tiny effect that resets k.current whenever the
# highlight param (a) changes, so the scroll always fires on a new notification click.
OLD = (
    '(0,_.useEffect)(()=>{if(!a||k.current)return;'
    'let e=D.current,t=e?.querySelector(`[data-comment-id="${a}"]`);'
    'if(!t)return;k.current=!0;'
)
NEW = (
    '(0,_.useEffect)(()=>{k.current=!1;},[a]);'
    '(0,_.useEffect)(()=>{if(!a||k.current)return;'
    'let e=D.current,t=e?.querySelector(`[data-comment-id="${a}"]`);'
    'if(!t)return;k.current=!0;'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: highlight guard reset on param change')
else:
    errors.append('FAIL: highlight effect not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
