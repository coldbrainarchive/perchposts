#!/usr/bin/env python3
"""Patch v123 -> v124: swap 🐤 to 🪹/❌ for jailed/banned users site-wide."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v123.js'
dst = '_deploy/assets/index-DUcNPOLc-v124.js'

content = open(src, encoding='utf-8').read()
errors = []

API = 'https://daboysforumip.coldbrainarchive.workers.dev'

# 1. Inject ban-list Sets + fetch right after _showBlock (at file start)
INJECT_AFTER = '};var e=Object.create'
INJECT_CODE = (
    'var _jailed=new Set(),_banned=new Set();'
    f'fetch("{API}/get-ban-lists")'
    '.then(function(r){{return r.json()}})'
    '.then(function(d){{'
    '(d.jailed||[]).forEach(function(u){{_jailed.add(u)}});'
    '(d.banned||[]).forEach(function(u){{_banned.add(u)}})'
    '}}).catch(function(){{}});'
)
if INJECT_AFTER in content:
    content = content.replace(INJECT_AFTER, '};' + INJECT_CODE + 'var e=Object.create', 1)
    print('OK: injected ban-list fetch')
else:
    errors.append('FAIL: injection point not found')

# 2. Modify Jn to check sets before returning normal emoji
OLD_JN = (
    'function Jn(e){return e?e.browser_id&&String(e.browser_id).startsWith(`bot-`)'
    '?`🤖`:e.is_admin?`🐧`:e.is_mod?`🐦`:e.username?`🐤`:null:null}'
)
NEW_JN = (
    'function Jn(e){'
    'if(!e)return null;'
    'if(e.username&&_jailed.has(e.username))return`\U0001fab9`;'
    'if(e.username&&_banned.has(e.username))return`❌`;'
    'return e.browser_id&&String(e.browser_id).startsWith(`bot-`)'
    '?`🤖`:e.is_admin?`🐧`:e.is_mod?`🐦`:e.username?`🐤`:null}'
)
if OLD_JN in content:
    content = content.replace(OLD_JN, NEW_JN, 1)
    print('OK: Jn updated — 🪹 for jailed, ❌ for banned')
else:
    errors.append('FAIL: Jn function not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
