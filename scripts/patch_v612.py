#!/usr/bin/env python3
"""Patch v611 -> v612:
New post page: replace separate Photo and Video buttons with a single 📎 Attach button,
identical in style to the Link button. Merge the two file inputs into one that accepts
both image/* and video/*, detecting type from the file's MIME type on change.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v611.js'
dst = '_deploy/assets/index-DUcNPOLc-v612.js'

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

# ── 1. Replace Photo + Video buttons with single Attach button ──
patch(
    '!_isHuddle&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>ie.current?.click(),disabled:ne,className:`feed-post-action-pill`,children:ne?`…`:`🖼 Photo`}),!_isHuddle&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>j.current?.click(),disabled:ne,className:`feed-post-action-pill`,children:ne?`…`:`🎥 Video`})',
    '!_isHuddle&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>ie.current?.click(),className:`feed-post-action-pill`,children:ne?`…`:`📎 Attach`})',
    'replace Photo+Video with single Attach button'
)

# ── 2. Merge image + video file inputs into one combined input ──
patch(
    '(0,L.jsx)(`input`,{ref:ie,type:`file`,accept:`image/*`,style:{display:`none`},onChange:e=>e.target.files[0]&&M(e.target.files[0],`image`)}),(0,L.jsx)(`input`,{ref:j,type:`file`,accept:`video/*`,style:{display:`none`},onChange:e=>e.target.files[0]&&M(e.target.files[0],`video`)})',
    '(0,L.jsx)(`input`,{ref:ie,type:`file`,accept:`image/*,video/*`,style:{display:`none`},onChange:e=>e.target.files[0]&&M(e.target.files[0],e.target.files[0].type.startsWith(`video`)?`video`:`image`)})',
    'merge image+video inputs into one'
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
