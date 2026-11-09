#!/usr/bin/env python3
"""Patch v907 -> v908: The Cage is no longer offered in the New Post board picker unless you're caged
(localStorage _caged, set by the page's check-jailed call) or a mod/admin. The worker refuses Cage posts
from everyone else ("Only caged birds can post in The Cage"); anyone can still chirp on Cage posts."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v907.js'
dst = '_deploy/assets/index-DUcNPOLc-v908.js'
content = open(src, encoding='utf-8').read()
old = "nr.filter(e=>!e.virtual&&e.slug!==`feedback`&&(e.slug!==`announcements`||[`mod`,`admin`].includes(Qn()?.role))).map("
new = ("nr.filter(e=>!e.virtual&&e.slug!==`feedback`&&(e.slug!==`announcements`||[`mod`,`admin`].includes(Qn()?.role))"
       "&&(e.slug!==`cage`||[`mod`,`admin`].includes(Qn()?.role)||localStorage.getItem(`_caged`)===`1`)).map(")
if content.count(old) != 1: print('FAIL', content.count(old)); sys.exit(1)
content = content.replace(old, new)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
