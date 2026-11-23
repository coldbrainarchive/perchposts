#!/usr/bin/env python3
"""Patch v1340 -> v1341: the Tags tab shows the "Saved searches" section only when you have at least one saved
(no empty hint). The bookmark in the search bar stays, since that's how you save one."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1340.js'
dst = '_deploy/assets/index-DUcNPOLc-v1341.js'
c = open(src, encoding='utf-8').read()
old = "function _SavedSearches({go}){const list=_ssUse(),[ed,setEd]=(0,_.useState)(!1);if(!localStorage.getItem(`auth_token`))return null;"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "function _SavedSearches({go}){const list=_ssUse(),[ed,setEd]=(0,_.useState)(!1);if(!localStorage.getItem(`auth_token`)||!list.length)return null;")
open(dst, 'w', encoding='utf-8').write(c); print('OK, wrote', dst)
