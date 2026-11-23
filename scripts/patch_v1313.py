#!/usr/bin/env python3
"""Patch v1312 -> v1313: visitor counter ignores automated browsers: no ping when navigator.webdriver is set
(headless crawlers, test browsers); the ping also sends wd so the worker can drop it. The worker also drops known
bot user agents."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1312.js'
dst = '_deploy/assets/index-DUcNPOLc-v1313.js'
c = open(src, encoding='utf-8').read()
old = "const ping=()=>{try{if(document.visibilityState!==`visible`)return;"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, "const ping=()=>{try{if(document.visibilityState!==`visible`||navigator.webdriver)return;"); print('OK: skip automated browsers')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
