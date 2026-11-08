#!/usr/bin/env python3
"""Patch v860 -> v861: region tabs go by tags only.
Every bot post now has a country (the outlet's home) and a region (what it covers), so BBC Africa is
United Kingdom + Africa. A post's region is its own tag, else its country's region. A country keeps to its
home region, so BBC Africa stays out of the UK filter. Adds Hong Kong (SCMP) under Asia.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v860.js'
dst = '_deploy/assets/index-DUcNPOLc-v861.js'

q = chr(0x60)
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

def t(s):
    return s.replace('`', q)

patch(t('Taiwan:`Asia`'), t('Taiwan:`Asia`,"Hong Kong":`Asia`'), 'Hong Kong region')
patch(t('{name:`Honduras`,flag:`🇭🇳`},'), t('{name:`Honduras`,flag:`🇭🇳`},{name:`Hong Kong`,flag:`🇭🇰`},'), 'Hong Kong flag')
patch('var ar={', 'function _rgn(e){return e.continent||ar[e.country]||null}function _inHome(e,c){return e.country===c&&(!e.continent||!ar[c]||e.continent===ar[c])}var ar={', 'region helpers')
patch(t('.filter(e=>!d||(!m&&TagR!==null)||e.continent===d)'), t('.filter(e=>!d||(!m&&TagR!==null)||_rgn(e)===d)'), 'feed region filter')
patch(t('if(!m||(_cs&&e.country===f))return!0'), t('if(!m||(_cs&&_inHome(e,f)))return!0'), 'feed country filter')
patch(t('.filter(e=>!f||e.continent===f).filter(e=>!p||e.country===p)'), t('.filter(e=>!f||_rgn(e)===f).filter(e=>!p||_inHome(e,p))'), 'board region and country filters')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
