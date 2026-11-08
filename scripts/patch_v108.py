#!/usr/bin/env python3
"""Patch v107 -> v108: caged users can post AND comment in Cage tag only.
- Replace alert() cage warnings with _showBlock modal
- Update all cage messages to clarify Cage-tag restriction
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v107.js'
dst = '_deploy/assets/index-DUcNPOLc-v108.js'

content = open(src, encoding='utf-8').read()
errors = []

MSG = "You’re caged — you can only post and comment in the \U0001fab9 Cage tag."

# 1. Post creation client-side cage check (alert -> _showBlock)
OLD_POST_ALERT = 'if(p&&h!==`cage`)return alert(`\U0001fab9 You are caged — you can only post in the Cage board`)'
NEW_POST_ALERT = f'if(p&&h!==`cage`){{_showBlock("{MSG}","caged");return}}'
if OLD_POST_ALERT in content:
    content = content.replace(OLD_POST_ALERT, NEW_POST_ALERT, 1)
    print('OK: post creation cage alert -> _showBlock')
else:
    errors.append('FAIL: post creation cage alert not found')

# 2. Post server error message for Caged
OLD_POST_ERR = '_showBlock("You are caged — posting is restricted.","caged")'
NEW_POST_ERR = f'_showBlock("{MSG}","caged")'
if OLD_POST_ERR in content:
    content = content.replace(OLD_POST_ERR, NEW_POST_ERR, 1)
    print('OK: post server Caged message updated')
else:
    errors.append('FAIL: post server Caged message not found')

# 3. Comment handler client-side cage check (alert -> _showBlock)
OLD_CMT_ALERT = 'if(oe&&cr(c)!==`Cage`){alert(`\U0001fab9 You are caged — you can only post in the Cage board`);return}'
NEW_CMT_ALERT = f'if(oe&&cr(c)!==`Cage`){{_showBlock("{MSG}","caged");return}}'
if OLD_CMT_ALERT in content:
    content = content.replace(OLD_CMT_ALERT, NEW_CMT_ALERT, 1)
    print('OK: comment cage alert -> _showBlock')
else:
    errors.append('FAIL: comment cage alert not found')

# 4. Comment server error message for Caged
OLD_CMT_ERR = '_showBlock("You are caged — commenting is restricted.","caged")'
NEW_CMT_ERR = f'_showBlock("{MSG}","caged")'
if OLD_CMT_ERR in content:
    content = content.replace(OLD_CMT_ERR, NEW_CMT_ERR, 1)
    print('OK: comment server Caged message updated')
else:
    errors.append('FAIL: comment server Caged message not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
