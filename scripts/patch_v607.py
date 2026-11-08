#!/usr/bin/env python3
"""Patch v606 -> v607:
Fix iOS scroll glitch by switching to flex-direction:column-reverse so the browser
natively starts at the bottom — no JS scrollTop manipulation needed.
- CSS: column -> column-reverse on .chat-window
- Render comments in reversed DOM order ([...de].reverse()) so newest=first in DOM,
  which column-reverse places at visual bottom (oldest top, newest bottom) ✓
- isAtBottom: scrollTop<60 (column-reverse: scrollTop=0 means at bottom/newest)
- Scroll effect: no initial scroll needed; after-send uses scrollTop=0
- scrollToComments effect: scrollTop=0 (bottom)
- Sort toggle buttons: swap scroll targets to match column-reverse coordinate system
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v606.js'
dst = '_deploy/assets/index-DUcNPOLc-v607.js'

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

# ── 1. CSS: column -> column-reverse ──
patch(
    'flex-direction: column;\n        gap: 6px;\n        position: relative;\n        padding: 14px 12px 45px;',
    'flex-direction: column-reverse;\n        gap: 6px;\n        position: relative;\n        padding: 14px 12px 45px;',
    'css column-reverse'
)

# ── 2. Reverse rendered array so newest is first in DOM ──
patch(
    '...de.map(e=>(0,L.jsx)(Rr,',
    '...[...de].reverse().map(e=>(0,L.jsx)(Rr,',
    'reverse rendered comments'
)

# ── 3. isAtBottom: scrollTop<60 (0=bottom in column-reverse) ──
patch(
    'O.current=e.scrollHeight-e.scrollTop-e.clientHeight<60',
    'O.current=e.scrollTop<60',
    'isAtBottom for column-reverse'
)

# ── 4. Scroll effect: skip initial (column-reverse handles it); after-send use scrollTop=0 ──
patch(
    'if(!_isd.current){_isd.current=!0;setTimeout(()=>{const _e=D.current;_e&&(_e.scrollTop=_e.scrollHeight)},200);return;}if(O.current){e.scrollTop=e.scrollHeight;}',
    'if(!_isd.current){_isd.current=!0;return;}if(O.current){e.scrollTop=0;}',
    'scroll effect uses scrollTop=0'
)

# ── 5. scrollToComments effect: scrollTop=0 (bottom) ──
patch(
    'let e=D.current;if(e)e.scrollTop=e.scrollHeight;window.scrollTo(0,document.body.scrollHeight);setTimeout(()=>{if(e)e.scrollTop=e.scrollHeight;},100)',
    'let e=D.current;if(e)e.scrollTop=0;window.scrollTo(0,document.body.scrollHeight);setTimeout(()=>{if(e)e.scrollTop=0;},100)',
    'scrollToComments uses scrollTop=0'
)

# ── 6. Sort toggle: swap scroll targets for column-reverse ──
patch(
    'e&&e.scrollTo({top:0,behavior:`smooth`});x(!1);',
    'e&&e.scrollTo({top:e.scrollHeight,behavior:`smooth`});x(!1);',
    'oldest btn scrollTo bottom (column-reverse)'
)
patch(
    'e&&e.scrollTo({top:e.scrollHeight,behavior:`smooth`});x(!0);',
    'e&&e.scrollTo({top:0,behavior:`smooth`});x(!0);',
    'newest btn scrollTo top (column-reverse)'
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
