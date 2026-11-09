#!/usr/bin/env python3
"""Patch v913 -> v914: picking a country (or board/region) from the dropdown after typing its name lost the
filter on phones. Tapping the pill set ?country=Kenya and cleared the box; the keyboard-close handler
(v894) then saved the empty box onto the *old* search params it had cached (u.current, still ?q=kenya), which
wiped the country. It now reads the live URL, and leaves the URL alone if the box was cleared by a pick."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v913.js'
dst = '_deploy/assets/index-DUcNPOLc-v914.js'
content = open(src, encoding='utf-8').read()
old = 'const v=c.current.value.trim();let e=new URLSearchParams(u.current);'
new = 'const v=c.current.value.trim();let e=new URLSearchParams(window.location.search);'
if content.count(old) != 1: print('FAIL', content.count(old)); sys.exit(1)
content = content.replace(old, new)
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
