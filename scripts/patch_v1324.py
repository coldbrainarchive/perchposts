#!/usr/bin/env python3
"""Patch v1323 -> v1324: New Post dropdown: tapping the picked perch tag or country again unpicks it (lists and search
results); the picked country's region gets the purple outline like a picked perch tag."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1323.js'
dst = '_deploy/assets/index-DUcNPOLc-v1324.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("onClick:()=>g(e.slug),style:{outline:`none`,boxShadow:e.slug===h?`0 0 0 2px #c084fc`:`none`,borderRadius:999}",
      "onClick:()=>g(e.slug===h?``:e.slug),style:{outline:`none`,boxShadow:e.slug===h?`0 0 0 2px #c084fc`:`none`,borderRadius:999}", 'perch tag toggles')
patch("onClick:()=>{y(e.name);C(null);},style:{outline:`none`,boxShadow:e.name===v?",
      "onClick:()=>{y(e.name===v?``:e.name);C(null);},style:{outline:`none`,boxShadow:e.name===v?", 'country toggles')
patch("onClick:()=>C(e),style:{outline:`none`,borderRadius:999,width:`100%`,justifyContent:`flex-start`}",
      "onClick:()=>C(e),style:{outline:`none`,boxShadow:v&&ar[v]===e?`0 0 0 2px #c084fc`:`none`,borderRadius:999,width:`100%`,justifyContent:`flex-start`}", 'region outline')
# search results
patch("onClick:()=>{pickBoard(e.slug);setQ(``)}", "onClick:()=>{pickBoard(e.slug===cur?``:e.slug);setQ(``)}", 'search: perch toggles')
patch("onClick:()=>{pickCountry(e.name);setQ(``);close()}", "onClick:()=>{pickCountry(e.name===curC?``:e.name);setQ(``);close()}", 'search: country toggles')
patch("onClick:()=>{pickRegion(e);setQ(``)},style:{outline:`none`,borderRadius:999}", "onClick:()=>{pickRegion(e);setQ(``)},style:{outline:`none`,boxShadow:curC&&ar[curC]===e?`0 0 0 2px #c084fc`:`none`,borderRadius:999}", 'search: region outline')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
