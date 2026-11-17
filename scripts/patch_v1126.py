#!/usr/bin/env python3
"""Patch v1125 -> v1126: the worm count in who-reacted rows is a small pink chip (🪱 N), sized to sit with the emoji."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1125.js'
dst = '_deploy/assets/index-DUcNPOLc-v1126.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("body .rx-qs .rx-w{display:inline-flex;align-items:center;gap:3px;margin-left:6px;vertical-align:middle}body .rx-qs .rx-w .ri.wemo{font-size:14px}",
      "body .rx-qs{display:inline-flex;align-items:center}"
      "body .rx-qs .rx-w{display:inline-flex;align-items:center;gap:4px;margin-left:8px;padding:0 8px 0 6px;height:1.6em;border-radius:999px;background:rgba(251,113,133,.12);border:1px solid rgba(251,113,133,.38);letter-spacing:0;font-size:inherit;vertical-align:middle}"
      "body .rx-qs .rx-w .pp-ic{display:inline-flex}body .rx-qs .rx-w .ri.wemo{font-size:1.1em}"
      "body .rx-qs .rx-w{font-size:.82em;font-weight:800;color:#fda4af}",
      'worm chip')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
