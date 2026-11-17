#!/usr/bin/env python3
"""Patch v1120 -> v1121: the 🪱 is sized to match the bird icon next to it (it looked too big): in post buttons, the
reactions tabs and rows, chirp pills and the post page pill."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1120.js'
dst = '_deploy/assets/index-DUcNPOLc-v1121.js'
c = open(src, encoding='utf-8').read()
old = "body .pp-pick-worm:first-child{"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
css = ("body .feed-post-action-pill .ri.wemo,body .pr-line .ri.wemo{font-size:11px}"
       "body .pr-tab .ri.wemo{font-size:11.5px}body .pr-did .ri.wemo{font-size:12.5px}"
       "body .chat-reaction-pill .ri.wemo{font-size:11.5px}body .pp-pick-worm .ri.wemo{font-size:16px}")
c = c.replace(old, css + old); print('OK: worm sized to the bird')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
