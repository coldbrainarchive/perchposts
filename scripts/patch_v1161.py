#!/usr/bin/env python3
"""Patch v1160 -> v1161: the nest hint is only the countdown ("New nest in m:ss"). Earlier (v1160): the sign-up nest times out after 15 minutes (birds/nest.js): the countdown always shows,
and at 0:00 the nest fetches new eggs by itself and clears the pick, so names aren't held in limbo. The worker hands
out new eggs once a nest is 15 minutes old and refuses sign-ups with a name from a timed-out nest."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1160.js'
dst = '_deploy/assets/index-DUcNPOLc-v1161.js'
c = open(src, encoding='utf-8').read()
H = '/*ppnest*/'
a = c.index(H) + len(H); w = c.index('function _PNest(', a)
c = c[:a] + open('birds/nest.js', encoding='utf-8').read() + '\n' + c[w:]; print('OK: nest code updated')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
