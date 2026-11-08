#!/usr/bin/env python3
"""Patch v597 -> v598:
- Default comment sort: 'oldest' -> 'newest' so newest comments show at top immediately
- isAtBottomRef init: true -> false so the auto-scroll-to-bottom doesn't fight newest-first layout
- Also flip the sort toggle label order so Newest appears active by default
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v597.js'
dst = '_deploy/assets/index-DUcNPOLc-v598.js'

content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append(f'FAIL ({label}): not found')
    elif n > 1:
        errors.append(f'FAIL ({label}): {n} matches (not unique)')
    else:
        content = content.replace(old, new)
        print(f'OK: {label}')

# ── 1. Default sort: oldest -> newest ──
patch(
    '[y]=(0,_.useState)(`oldest`)',
    '[y]=(0,_.useState)(`newest`)',
    'default sort newest'
)

# ── 2. isAtBottomRef init: true -> false (don't auto-scroll to bottom in newest mode) ──
# Only patch the one in PostPage (Wr) — the ref is O
# Pattern: O=(0,_.useRef)(!0) immediately followed by other refs in Wr
patch(
    ',O=(0,_.useRef)(!0),k=(0,_.useRef)(!1),A=(0,_.useRef)(!1),te=(0,_.useRef)(!!s.state?.scrollToComments)',
    ',O=(0,_.useRef)(!1),k=(0,_.useRef)(!1),A=(0,_.useRef)(!1),te=(0,_.useRef)(!!s.state?.scrollToComments)',
    'isAtBottomRef init false for newest-first'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print(f'Paren delta: {p_delta}, Brace delta: {b_delta}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
