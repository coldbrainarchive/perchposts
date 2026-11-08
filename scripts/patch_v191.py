#!/usr/bin/env python3
"""Patch v190 -> v191: globe SVG in comment header uses black stroke (visible on all header colours)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v190.js'
dst = '_deploy/assets/index-DUcNPOLc-v191.js'

content = open(src, encoding='utf-8').read()
errors = []

# The comment-card globe uses id="bcc" to distinguish it from the nav globe.
# Replace all #c084fc strokes only within that SVG block.
# The block spans from the opening svg tag to the closing clipPath.
OLD_GLOBE = (
    '(0,L.jsxs)(`svg`,{width:`14`,height:`14`,viewBox:`0 0 100 100`,'
    'xmlns:`http://www.w3.org/2000/svg`,style:{flexShrink:0},'
    'children:['
    '(0,L.jsx)(`circle`,{cx:`50`,cy:`50`,r:`44`,fill:`none`,stroke:`#c084fc`,strokeWidth:`7`}),'
    '(0,L.jsx)(`line`,{x1:`6`,y1:`50`,x2:`94`,y2:`50`,stroke:`#c084fc`,strokeWidth:`6`}),'
    '(0,L.jsx)(`path`,{d:`M 14 28 Q 50 38 86 28`,fill:`none`,stroke:`#c084fc`,strokeWidth:`6`}),'
    '(0,L.jsx)(`path`,{d:`M 14 72 Q 50 62 86 72`,fill:`none`,stroke:`#c084fc`,strokeWidth:`6`}),'
    '(0,L.jsx)(`ellipse`,{cx:`50`,cy:`50`,rx:`16`,ry:`44`,fill:`none`,stroke:`#c084fc`,strokeWidth:`6`,clipPath:`url(#bcc)`}),'
    '(0,L.jsx)(`ellipse`,{cx:`50`,cy:`50`,rx:`32`,ry:`44`,fill:`none`,stroke:`#c084fc`,strokeWidth:`6`,clipPath:`url(#bcc)`}),'
    '(0,L.jsx)(`clipPath`,{id:`bcc`,children:(0,L.jsx)(`circle`,{cx:`50`,cy:`50`,r:`44`})})'
    ']})'
)
NEW_GLOBE = (
    '(0,L.jsxs)(`svg`,{width:`14`,height:`14`,viewBox:`0 0 100 100`,'
    'xmlns:`http://www.w3.org/2000/svg`,style:{flexShrink:0},'
    'children:['
    '(0,L.jsx)(`circle`,{cx:`50`,cy:`50`,r:`44`,fill:`none`,stroke:`#0a0a0a`,strokeWidth:`7`}),'
    '(0,L.jsx)(`line`,{x1:`6`,y1:`50`,x2:`94`,y2:`50`,stroke:`#0a0a0a`,strokeWidth:`6`}),'
    '(0,L.jsx)(`path`,{d:`M 14 28 Q 50 38 86 28`,fill:`none`,stroke:`#0a0a0a`,strokeWidth:`6`}),'
    '(0,L.jsx)(`path`,{d:`M 14 72 Q 50 62 86 72`,fill:`none`,stroke:`#0a0a0a`,strokeWidth:`6`}),'
    '(0,L.jsx)(`ellipse`,{cx:`50`,cy:`50`,rx:`16`,ry:`44`,fill:`none`,stroke:`#0a0a0a`,strokeWidth:`6`,clipPath:`url(#bcc)`}),'
    '(0,L.jsx)(`ellipse`,{cx:`50`,cy:`50`,rx:`32`,ry:`44`,fill:`none`,stroke:`#0a0a0a`,strokeWidth:`6`,clipPath:`url(#bcc)`}),'
    '(0,L.jsx)(`clipPath`,{id:`bcc`,children:(0,L.jsx)(`circle`,{cx:`50`,cy:`50`,r:`44`})})'
    ']})'
)
if OLD_GLOBE in content:
    content = content.replace(OLD_GLOBE, NEW_GLOBE, 1)
    print('OK: comment globe stroke → black')
else:
    errors.append('FAIL: comment globe SVG not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
