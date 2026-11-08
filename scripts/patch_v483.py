#!/usr/bin/env python3
"""Patch v474 -> v483: Replace 'Tap to close' text with a proper iOS-style
drag handle bar. Adds a subtle handle + keeps the panel top aesthetic clean."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v474.js'
dst = '_deploy/assets/index-DUcNPOLc-v483.js'

content = open(src, encoding='utf-8').read()

OLD = ('display:`flex`,alignItems:`center`,justifyContent:`center`,'
       'padding:`14px 20px 8px`,flexShrink:0},children:(0,L.jsx)(`span`,{'
       'style:{fontSize:11,color:`#64748b`,letterSpacing:`0.04em`,fontWeight:500},'
       'children:`Tap to close`})})')
NEW = ('display:`flex`,alignItems:`center`,justifyContent:`center`,'
       'padding:`12px 20px 6px`,flexShrink:0},children:(0,L.jsx)(`div`,{'
       'style:{width:36,height:4,borderRadius:2,background:`#3a3f52`}})})')

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: drag handle added')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
