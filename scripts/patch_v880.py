#!/usr/bin/env python3
"""Patch v879 -> v880: stop Safari offering contact AutoFill ("AutoFill Contact", home / Ireland) on the main
search bar. Safari ignores autocomplete="off" there and treats it as an address field because the placeholder
mentions "country". Marking it type="search" tells Safari it's a search box, so the wording can stay.
enterKeyHint="search" makes the iPhone return key read "Search". Safari's own search-field styling and grey
clear button are turned off, since the bar already has its own clear button.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v879.js'
dst = '_deploy/assets/index-DUcNPOLc-v880.js'

content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n != 1:
        errors.append('FAIL (' + label + '): found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

patch('country…`,autoComplete:`off`', 'country…`,autoComplete:`off`,type:`search`,enterKeyHint:`search`', 'search type')
patch('.search-input::placeholder { color: #4b5563; }',
      '.search-input::placeholder { color: #4b5563; }\n'
      '      .search-input { -webkit-appearance: none; appearance: none; border-radius: 0; }\n'
      '      .search-input::-webkit-search-cancel-button, .search-input::-webkit-search-decoration,'
      ' .search-input::-webkit-search-results-button, .search-input::-webkit-search-results-decoration'
      ' { -webkit-appearance: none; appearance: none; display: none; }',
      'hide native search styling')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
