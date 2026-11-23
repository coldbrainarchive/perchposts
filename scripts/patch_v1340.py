#!/usr/bin/env python3
"""Patch v1339 -> v1340: the starred default search fills the bar on every page load / refresh of the home page
(with no filters in the address). Within the same page load (moving around the site) it's applied only once, so
clearing it sticks until the next refresh. Was: once per 30 minutes, which skipped refreshes."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1339.js'
dst = '_deploy/assets/index-DUcNPOLc-v1340.js'
c = open(src, encoding='utf-8').read()
old = "const now=Date.now(),last=+(sessionStorage.getItem(`pp_ss_at`)||0);sessionStorage.setItem(`pp_ss_at`,String(now));\n if(last&&now-last<30*60e3)return;"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, "if(window._ppSsTried)return;window._ppSsTried=!0;")
open(dst, 'w', encoding='utf-8').write(c); print('OK, wrote', dst)
