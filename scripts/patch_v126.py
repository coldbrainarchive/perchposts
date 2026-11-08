#!/usr/bin/env python3
"""Patch v125 -> v126: notification pill shows just count in red, no bird/name."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v125.js'
dst = '_deploy/assets/index-DUcNPOLc-v126.js'

content = open(src, encoding='utf-8').read()
errors = []

# When f>0: render a simple red pill showing just the count
# When f===0: render normal Xn pill
OLD = (
    'className:`nav-user-pill`,style:{background:`none`,border:`none`,padding:0,cursor:`pointer`,display:`flex`},'
    'children:(()=>{let e=n===`admin`,t=n===`mod`,r=e||t?i:o||`Me`;'
    'return(0,L.jsx)(Xn,{record:{is_admin:e,is_mod:t&&!e,username:r,browser_id:Gn()},name:r,color:f>0?`#ef4444`:Hn(Gn(),r)})})()})]'
)
NEW = (
    'className:`nav-user-pill`,style:{background:`none`,border:`none`,padding:0,cursor:`pointer`,display:`flex`},'
    'children:(()=>{'
    'if(f>0)return(0,L.jsx)(`span`,{className:`user-pill`,style:{'
    'background:`#ef4444`,borderColor:`#ef4444`,color:`#ffffff`,'
    'fontWeight:800,fontSize:14,minWidth:28,justifyContent:`center`},'
    'children:f>99?`99+`:f});'
    'let e=n===`admin`,t=n===`mod`,r=e||t?i:o||`Me`;'
    'return(0,L.jsx)(Xn,{record:{is_admin:e,is_mod:t&&!e,username:r,browser_id:Gn()},name:r,color:Hn(Gn(),r)})})()})]'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: notification pill shows count only in red')
else:
    errors.append('FAIL: nav pill pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
