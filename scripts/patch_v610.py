#!/usr/bin/env python3
"""Patch v609 -> v610:
Revert flex-direction:column-reverse (cross-browser scrollTop inconsistencies break buttons).
Fix iOS bounce/glitch with overscroll-behavior-y:contain instead.
- CSS: column-reverse -> column, add overscroll-behavior-y:contain
- Render: remove [...de].reverse() — back to normal oldest-first order
- isAtBottom: back to scrollHeight-scrollTop-clientHeight<60
- Scroll effect: single 300ms scroll to bottom (scrollTop=scrollHeight)
- scrollToComments: scrollTop=scrollHeight
- Oldest btn: scrollTop=0 (top), Newest btn: scrollTop=scrollHeight (bottom)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v609.js'
dst = '_deploy/assets/index-DUcNPOLc-v610.js'

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

# ── 1. CSS: revert column-reverse, add overscroll-behavior ──
patch(
    'flex-direction: column-reverse;',
    'flex-direction: column;\n        overscroll-behavior-y: contain;',
    'css revert + overscroll-behavior'
)

# ── 2. Render: remove [...de].reverse() ──
patch(
    '...[...de].reverse().map(e=>(0,L.jsx)(Rr,',
    '...de.map(e=>(0,L.jsx)(Rr,',
    'remove reversed render'
)

# ── 3. isAtBottom: standard check ──
patch(
    'O.current=e.scrollTop<60',
    'O.current=e.scrollHeight-e.scrollTop-e.clientHeight<60',
    'isAtBottom standard check'
)

# ── 4. Scroll effect: 300ms single scroll to bottom ──
patch(
    'if(!_isd.current){_isd.current=!0;return;}if(O.current){e.scrollTop=0;}',
    'if(!_isd.current){_isd.current=!0;setTimeout(()=>{const _e=D.current;_e&&(_e.scrollTop=_e.scrollHeight)},300);return;}if(O.current){e.scrollTop=e.scrollHeight;}',
    'scroll effect 300ms to bottom'
)

# ── 5. scrollToComments: scrollTop=scrollHeight ──
patch(
    'let e=D.current;if(e)e.scrollTop=0;window.scrollTo(0,document.body.scrollHeight);setTimeout(()=>{if(e)e.scrollTop=0;},100)',
    'let e=D.current;if(e)e.scrollTop=e.scrollHeight;window.scrollTo(0,document.body.scrollHeight);setTimeout(()=>{if(e)e.scrollTop=e.scrollHeight;},100)',
    'scrollToComments to bottom'
)

# ── 6. Oldest button: scroll to top (0) — use children label as anchor ──
patch(
    'onClick:()=>{let e=D.current;if(e)e.scrollTop=e.scrollHeight;},children:`Oldest`',
    'onClick:()=>{let e=D.current;if(e)e.scrollTop=0;},children:`Oldest`',
    'oldest btn scroll to top'
)

# ── 7. Newest button: scroll to bottom (scrollHeight) — use children label as anchor ──
patch(
    'onClick:()=>{let e=D.current;if(e)e.scrollTop=0;},children:`Newest`',
    'onClick:()=>{let e=D.current;if(e)e.scrollTop=e.scrollHeight;},children:`Newest`',
    'newest btn scroll to bottom'
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
