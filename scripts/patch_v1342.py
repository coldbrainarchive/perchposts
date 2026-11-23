#!/usr/bin/env python3
"""Patch v1341 -> v1342: saved searches find your username from the signed-in account (auth_user) when _myUsername
isn't stored — without it the list read as empty, so the Saved row and the starred default didn't show."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1341.js'
dst = '_deploy/assets/index-DUcNPOLc-v1342.js'
c = open(src, encoding='utf-8').read()
old = "function _ssMe(){return(localStorage.getItem(`_myUsername`)||``).toLowerCase()}"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "function _ssMe(){return(localStorage.getItem(`_myUsername`)||Qn()?.username||``).toLowerCase()}")
open(dst, 'w', encoding='utf-8').write(c); print('OK, wrote', dst)
