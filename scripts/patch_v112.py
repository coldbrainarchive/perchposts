#!/usr/bin/env python3
"""Patch v111 -> v112: add debug logging to cage post submit."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v111.js'
dst = '_deploy/assets/index-DUcNPOLc-v112.js'

content = open(src, encoding='utf-8').read()
errors = []

# Add console.log before cage check in ae()
OLD_CAGE = 'if(p&&h!==`cage`){_showBlock('
NEW_CAGE = 'console.log("[CAGE]",{p,h,board:(sr(h)||nr[0]).name,ls:localStorage.getItem("_caged")});if(p&&h!==`cage`){_showBlock('
if OLD_CAGE in content:
    # Only replace first occurrence (in ae, not in comment handler Wr)
    content = content.replace(OLD_CAGE, NEW_CAGE, 1)
    print('OK: debug log added before cage check in ae()')
else:
    errors.append('FAIL: cage check not found')

# Also log server error response
OLD_ERR = 'if(!m.ok){u(!1),g.error===`Banned`?_showBlock("You are banned from postchats.")'
NEW_ERR = 'if(!m.ok){console.log("[POST-ERR]",g);u(!1),g.error===`Banned`?_showBlock("You are banned from postchats.")'
if OLD_ERR in content:
    content = content.replace(OLD_ERR, NEW_ERR, 1)
    print('OK: server error log added')
else:
    errors.append('FAIL: server error pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
