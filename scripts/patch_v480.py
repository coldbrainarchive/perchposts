#!/usr/bin/env python3
"""Patch v479 -> v480:
Make ptr-strip gray only when notification panel is open, using a CSS custom
property (--ptr-bg). The open handler sets it to #1a1d27; close (backdrop
onClick:l) resets it to #0b0f12.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v479.js'
dst = '_deploy/assets/index-DUcNPOLc-v480.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. ptr-strip: use CSS custom property ─────────────────────────────────────
OLD_PTR = 'zIndex:9999,background:`#1a1d27`,pointerEvents:`none`'
NEW_PTR = 'zIndex:9999,background:`var(--ptr-bg,#0b0f12)`,pointerEvents:`none`'
if OLD_PTR in content:
    content = content.replace(OLD_PTR, NEW_PTR, 1)
    print('OK: ptr-strip uses --ptr-bg CSS var')
else:
    errors.append('FAIL: ptr-strip background')

# ── 2. Open handler: set --ptr-bg to gray ─────────────────────────────────────
OLD_OPEN = 'onClick:()=>{p(0),d(!0)}'
NEW_OPEN = 'onClick:()=>{p(0),d(!0),document.documentElement.style.setProperty(`--ptr-bg`,`#1a1d27`)}'
if OLD_OPEN in content:
    content = content.replace(OLD_OPEN, NEW_OPEN, 1)
    print('OK: open handler sets --ptr-bg')
else:
    errors.append('FAIL: open handler')

# ── 3. Backdrop close (onClick:l) → wrap to also reset --ptr-bg ───────────────
OLD_CLOSE = 'position:`fixed`,inset:0,zIndex:10000,display:`flex`,flexDirection:`column`,justifyContent:`flex-end`},onClick:l,'
NEW_CLOSE = 'position:`fixed`,inset:0,zIndex:10000,display:`flex`,flexDirection:`column`,justifyContent:`flex-end`},onClick:()=>{l();document.documentElement.style.setProperty(`--ptr-bg`,`#0b0f12`)},'
if OLD_CLOSE in content:
    content = content.replace(OLD_CLOSE, NEW_CLOSE, 1)
    print('OK: backdrop close resets --ptr-bg')
else:
    errors.append('FAIL: backdrop close')

# ── 4. Inner close (onClick:e=>{...l()}) → also reset --ptr-bg ────────────────
OLD_INNER = "onClick:e=>{if(e.target.tagName!==`A`&&e.target.tagName!==`BUTTON`&&e.target.tagName!==`IMG`)l()}"
NEW_INNER = "onClick:e=>{if(e.target.tagName!==`A`&&e.target.tagName!==`BUTTON`&&e.target.tagName!==`IMG`){l();document.documentElement.style.setProperty(`--ptr-bg`,`#0b0f12`);}}"
if OLD_INNER in content:
    content = content.replace(OLD_INNER, NEW_INNER, 1)
    print('OK: inner panel close resets --ptr-bg')
else:
    errors.append('FAIL: inner close')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
