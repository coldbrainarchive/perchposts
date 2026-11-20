#!/usr/bin/env python3
"""Patch v1258 -> v1259: every copy of the globe logo gets the evenly spaced lines the animated header globe
has used since v1258 (12 lines, one every 30°: front lines at ±15/±45 instead of ±17.6/±41.1; the ±75 pair sits under the outer ring, so the static copies leave it out).
Updates the bundle's _ppLogo (header before the animation draws), the tab icon (favicon.svg, ?v bump),
brand/globe*.svg and the share-card worker's GLOBE (og-worker, IMG_VER bump; deployed separately)."""
import sys, re
OLD = ['<path d="M 56 12 A 11.49 38 0 0 1 56 88"/>', '<path d="M 56 12 A 24.98 38 0 0 1 56 88"/>',
       '<path d="M 56 12 A 11.49 38 0 0 0 56 88"/>', '<path d="M 56 12 A 24.98 38 0 0 0 56 88"/>']
NEW = ''.join(f'<path d="M 56 12 A {rx} 38 0 0 {s} 56 88"/>' for rx in ('9.84', '26.87') for s in (1, 0))
OLDS = ''.join(OLD)
def fix(path, esc=False, expect=None):
    t = open(path, encoding='utf-8').read()
    o, n = (OLDS, NEW) if not esc else (OLDS.replace('"', '\\"'), NEW.replace('"', '\\"'))
    k = t.count(o)
    if k == 0 or (expect and k != expect): print('FAIL', path, k); sys.exit(1)
    return t.replace(o, n), k
src = '_deploy/assets/index-DUcNPOLc-v1258.js'; dst = '_deploy/assets/index-DUcNPOLc-v1259.js'
c, k = fix(src, esc=True); open(dst, 'w', encoding='utf-8').write(c); print('OK: bundle _ppLogo copies', k)
for p in ['_deploy/favicon.svg', 'brand/globe.svg', 'brand/globe-glow.svg', 'brand/globe-thinlines.svg', 'og-worker/index.js']:
    t, k = fix(p); open(p, 'w', encoding='utf-8').write(t); print('OK:', p, k)
h = open('_deploy/index.html', encoding='utf-8').read()
assert 'favicon.svg?v=12' in h; open('_deploy/index.html', 'w', encoding='utf-8').write(h.replace('favicon.svg?v=12', 'favicon.svg?v=13')); print('OK: favicon ?v=13')
w = open('og-worker/index.js', encoding='utf-8').read()
assert 'const IMG_VER = "21";' in w; open('og-worker/index.js', 'w', encoding='utf-8').write(w.replace('const IMG_VER = "21";', 'const IMG_VER = "22";')); print('OK: IMG_VER 22')
print('Wrote', dst)
