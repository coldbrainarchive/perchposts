#!/usr/bin/env python3
"""Patch v432 -> v433:
1. Huddle member search input: backspace on empty input removes last tagged user
2. Huddle title: required (not optional) — update placeholder + validation
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v432.js'
dst = '_deploy/assets/index-DUcNPOLc-v433.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add onKeyDown backspace handler to the Add Birds search input ──────────
OLD_INPUT = 'className:`search-input`,value:_hmTagQ,onChange:e=>{_setHmTagQ(e.target.value);clearTimeout(_hmTimer.current);_hmTimer.current=setTimeout(()=>{if(e.target.value.trim()){fetch(`${R}/search-users?q=${encodeURIComponent(e.target.value.trim())}`).then(_r=>_r.ok?_r.json():{users:[]}).then(_d=>_setHmTagR(_d.users||[])).catch(()=>_setHmTagR([]));}else{_setHmTagR([]);}},300);},placeholder:`Add Birds`'
NEW_INPUT = 'className:`search-input`,value:_hmTagQ,onChange:e=>{_setHmTagQ(e.target.value);clearTimeout(_hmTimer.current);_hmTimer.current=setTimeout(()=>{if(e.target.value.trim()){fetch(`${R}/search-users?q=${encodeURIComponent(e.target.value.trim())}`).then(_r=>_r.ok?_r.json():{users:[]}).then(_d=>_setHmTagR(_d.users||[])).catch(()=>_setHmTagR([]));}else{_setHmTagR([]);}},300);},onKeyDown:e=>{if(e.key===`Backspace`&&!_hmTagQ&&_hmTagged.length>0){_setHmTagged(_hmTagged.slice(0,-1));}},placeholder:`Add Birds`'
if OLD_INPUT in content:
    content = content.replace(OLD_INPUT, NEW_INPUT, 1)
    print('OK: backspace removes last tagged user when input is empty')
else:
    errors.append('FAIL: Add Birds input not found')

# ── 2. Title placeholder: remove "(optional)" ─────────────────────────────────
OLD_PH = 'placeholder:_isHuddle?`Give this huddle a title (optional)`:`Give the thread a title…`'
NEW_PH = 'placeholder:_isHuddle?`Give this huddle a title…`:`Give the thread a title…`'
if OLD_PH in content:
    content = content.replace(OLD_PH, NEW_PH, 1)
    print('OK: huddle title placeholder updated')
else:
    errors.append('FAIL: title placeholder not found')

# ── 3. Validation: require title for huddles too ──────────────────────────────
OLD_VAL = 'if(!_isHuddle&&!a.trim())return alert(`Give your post a title`);if(!_isHuddle&&!s.trim()&&!T)return alert(`Add a body, or attach a link, photo, or video`);if(_isHuddle&&_hmTagged.length===0)return alert(`Add at least one user to your huddle`)'
NEW_VAL = 'if(!a.trim())return alert(`Give your huddle a title`);if(!_isHuddle&&!s.trim()&&!T)return alert(`Add a body, or attach a link, photo, or video`);if(_isHuddle&&_hmTagged.length===0)return alert(`Add at least one user to your huddle`)'
if OLD_VAL in content:
    content = content.replace(OLD_VAL, NEW_VAL, 1)
    print('OK: title required for all posts including huddles')
else:
    errors.append('FAIL: validation block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
