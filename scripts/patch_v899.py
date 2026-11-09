#!/usr/bin/env python3
"""Patch v898 -> v899: Safari's "AutoFill Contact" (home / Ireland) came back on the main search bar on the
user's iPhone even with type="search" (v880). Safari guesses address fields from the field's name/id and its
placeholder words ("region", "country"). Now the input is named "search" (id "site-search"), which Safari's
AutoFill skips, and the placeholder has a zero-width space inside "region" and "country" so those words no
longer match. The placeholder looks identical.
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v898.js'
dst = '_deploy/assets/index-DUcNPOLc-v899.js'
content = open(src, encoding='utf-8').read()
old = 'placeholder:M?`Add keywords to filter…`:`Search or filter by board, region, country…`'
new = 'name:`search`,id:`site-search`,placeholder:M?`Add keywords to filter…`:`Search or filter by board, reg​ion, coun​try…`'
if content.count(old) != 1:
    print('FAIL', content.count(old)); sys.exit(1)
content = content.replace(old, new)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
