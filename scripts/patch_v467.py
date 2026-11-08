#!/usr/bin/env python3
"""Patch v466 -> v467: Apply browser-detected fontSize to comment bubble bird.
Chrome gets _bsz+2=17, Safari gets _bsz+2=14 (inflates to ~17px visually)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v466.js'
dst = '_deploy/assets/index-DUcNPOLc-v467.js'

content = open(src, encoding='utf-8').read()

OLD = 'display:`inline-flex`,alignItems:`center`,justifyContent:`center`,fontSize:17,lineHeight:1,flexShrink:0,width:`17px`,height:`17px`'
NEW = 'display:`inline-flex`,alignItems:`center`,justifyContent:`center`,fontSize:_bsz+2,lineHeight:1,flexShrink:0,width:`17px`,height:`17px`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: comment bubble fontSize:17 → _bsz+2')
else:
    print('FAIL: comment bubble bird not found'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
