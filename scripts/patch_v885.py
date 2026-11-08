#!/usr/bin/env python3
"""Patch v884 -> v885: stop the search box's cursor being drawn in the wrong place for a moment while typing.

Filmed on the user's iPhone (screen recording + iPhone Mirroring): about 250ms after a keystroke, when the search
is applied, the cursor is drawn up to ~2 characters too far right (typing) or left (deleting), then snaps back.
The recorder shows the real cursor position is always correct, so it's a drawing glitch.

At that moment the only thing that touches the search box is React rewriting its defaultValue (the value
attribute) to the newly applied search text. That has no visible effect once the user has typed, but makes
Safari recompute the box's text, and iOS draws the cursor from stale layout. Fix: while the box is focused, keep
passing the box's current defaultValue so React doesn't rewrite it. When it isn't focused the old behaviour
stays (the site clears or sets the box through .value anyway). Keeps v884's recorder for testing.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v884.js'
dst = '_deploy/assets/index-DUcNPOLc-v885.js'
content = open(src, encoding='utf-8').read()
old = 'key:`si`,ref:c,className:`search-input`,defaultValue:n,'
new = 'key:`si`,ref:c,className:`search-input`,defaultValue:(c.current&&document.activeElement===c.current)?c.current.defaultValue:n,'
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old))); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
