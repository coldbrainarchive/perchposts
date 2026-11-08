#!/usr/bin/env python3
"""Patch v99 -> v100: fix cage/ban in members panel to use IP + show for all members."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v99.js'
dst = '_deploy/assets/index-DUcNPOLc-v100.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Se (jailed check): also match ip_hash and username, not just browser_id ─
OLD_SE = 'Se=e=>s.some(t=>t.browser_id===e.browser_id)'
NEW_SE = 'Se=e=>s.some(t=>t.browser_id===e.browser_id||t.ip_hash===e.ip_hash||t.username===e.username)'
if OLD_SE in content:
    content = content.replace(OLD_SE, NEW_SE, 1)
    print('OK: Se now checks browser_id + ip_hash + username')
else:
    errors.append('FAIL: Se definition not found')

# ── 2. Member card: always create o with ip_hash, never null ─────────────────
OLD_O = 'a=ae[i]||null,o=a?{browser_id:a,username:i}:null,s=o?be(o):!1,c=o?Se(o):!1'
NEW_O = (
    'a=ae[i]||null,'
    'o={browser_id:a||n.user_metadata?.browser_id||null,username:i,ip_hash:n.user_metadata?.ip_hash||null},'
    's=be(o),c=Se(o)'
)
if OLD_O in content:
    content = content.replace(OLD_O, NEW_O, 1)
    print('OK: member o now always includes ip_hash from member data')
else:
    errors.append('FAIL: member o construction not found')

# ── 3. Button condition: show when not admin AND have something to act on ─────
OLD_COND = 'o&&!d&&(0,L.jsxs)(L.Fragment,{children:['
NEW_COND = '!d&&(o.browser_id||o.ip_hash)&&(0,L.jsxs)(L.Fragment,{children:['
if OLD_COND in content:
    content = content.replace(OLD_COND, NEW_COND, 1)
    print('OK: button condition uses ip_hash/browser_id check instead of o null check')
else:
    errors.append('FAIL: button condition not found')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
