#!/usr/bin/env python3
"""Patch v158 -> v159: lock body scroll when link preview modal is open."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v158.js'
dst = '_deploy/assets/index-DUcNPOLc-v159.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'function c(){window.history.pushState({linkPreview:!0},``),a(!0)}'
    'function l(){a(!1)}'
)
NEW = (
    'function c(){window.history.pushState({linkPreview:!0},``),a(!0),'
    'document.body.style.overflow=`hidden`}'
    'function l(){a(!1),document.body.style.overflow=``}'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: body scroll locked on open, restored on close')
else:
    errors.append('FAIL: open/close functions not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
