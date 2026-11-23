#!/usr/bin/env python3
"""Patch v1345 -> v1346: Announcements and The Cage move from the Spaces tab to the Tags tab (after Random). They're
real tags shown on posts, so they now combine with other filters like any perch tag. Spaces = Flock, Perch News, Huddles."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1345.js'
dst = '_deploy/assets/index-DUcNPOLc-v1346.js'
c = open(src, encoding='utf-8').read()
old = "_SPACES=[`activity`,`botnews`,`announcements`,`feedback`,`cage`]"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, "_SPACES=[`activity`,`botnews`,`feedback`]")
open(dst, 'w', encoding='utf-8').write(c); print('OK, wrote', dst)
