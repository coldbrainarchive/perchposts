#!/usr/bin/env python3
"""Patch v854 -> v855: desktop Safari gets no emoji nudge. A real screenshot showed all badges 1.3-1.5px right
there, which is the nudge desktop Chrome needs, so Safari draws these emojis centred already.
-apple-system-body is only understood by Apple's browsers, and touch-callout only on iPhones and iPads, so
this rule reaches Mac Safari alone. iPhone and Chrome are untouched.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v854.js'
dst = '_deploy/assets/index-DUcNPOLc-v855.js'

content = open(src, encoding='utf-8').read()
old = '.post-badge-i{transform:translate(.08px,-1.11px)}}'
new = old + '@supports (font:-apple-system-body) and (not (-webkit-touch-callout:none)){.post-badge,.post-badge.bot{padding:0}.post-badge-i{transform:none}}'
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old)))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
