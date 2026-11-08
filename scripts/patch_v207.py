#!/usr/bin/env python3
"""Patch v206 -> v207: board chips get unique colours; country/continent chips get one warm colour."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v206.js'
dst = '_deploy/assets/index-DUcNPOLc-v207.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Board chip (Ar) — each board gets its own colour ──────────────────────
OLD_AR = (
    'function Ar({boardName:e,small:t}){'
    'let n=nr.find(t=>t.name===e);'
    'return n?(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'gap:t?4:6,height:t?22:26,padding:t?`0 7px`:`0 8px`,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,color:`#dbe4ee`,'
    'fontSize:t?10:11,fontWeight:800,letterSpacing:`0.03em`,textTransform:`uppercase`,'
    'whiteSpace:`nowrap`,lineHeight:1,overflow:`hidden`,flexShrink:0,boxSizing:`border-box`},'
    'children:[(0,L.jsx)(`span`,{children:n.icon}),(0,L.jsx)(`span`,{children:n.name})]}):null}'
)
NEW_AR = (
    'function Ar({boardName:e,small:t}){'
    'let n=nr.find(t=>t.name===e);'
    'if(!n)return null;'
    'let _bc={'
    'activity:`#a5f3fc`,'   # Flock - light cyan
    'general:`#93c5fd`,'    # General - light blue
    'sports:`#86efac`,'     # Sports - light green
    '"science-nature":`#f9a8d4`,'  # Science - light pink
    'random:`#fda4af`,'     # Random - light rose
    'announcements:`#fde68a`,'  # Announcements - amber
    'feedback:`#6ee7b7`,'   # Feedback - emerald
    'cage:`#fb923c`'        # The Cage - orange
    '}[n.slug]||`#e2e8f0`;'
    'return(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'gap:t?4:6,height:t?22:26,padding:t?`0 7px`:`0 8px`,borderRadius:999,'
    'border:`1px solid rgba(0,0,0,0.15)`,background:_bc,color:`#0a0a0a`,'
    'fontSize:t?10:11,fontWeight:800,letterSpacing:`0.03em`,textTransform:`uppercase`,'
    'whiteSpace:`nowrap`,lineHeight:1,overflow:`hidden`,flexShrink:0,boxSizing:`border-box`},'
    'children:[(0,L.jsx)(`span`,{children:n.icon}),(0,L.jsx)(`span`,{children:n.name})]})'
    '}'
)
if OLD_AR in content:
    content = content.replace(OLD_AR, NEW_AR, 1)
    print('OK: board chips coloured')
else:
    errors.append('FAIL: Ar component not found')

# ── 2. Country/continent chip (kr) — one warm sandy colour ───────────────────
OLD_KR = (
    'return(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'gap:n?4:6,height:n?22:26,padding:n?`0 7px`:`0 8px`,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#20262f`,color:`#dbe4ee`,'
    'fontSize:n?10:11,fontWeight:800,letterSpacing:`0.03em`,textTransform:`uppercase`,'
    'whiteSpace:`nowrap`,lineHeight:1,overflow:`hidden`,flexShrink:0,boxSizing:`border-box`},'
    'children:[(0,L.jsx)(`span`,{children:r}),(0,L.jsx)(`span`,{children:a})]'
)
NEW_KR = (
    'return(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'gap:n?4:6,height:n?22:26,padding:n?`0 7px`:`0 8px`,borderRadius:999,'
    'border:`1px solid rgba(0,0,0,0.15)`,background:`#fde68a`,color:`#0a0a0a`,'
    'fontSize:n?10:11,fontWeight:800,letterSpacing:`0.03em`,textTransform:`uppercase`,'
    'whiteSpace:`nowrap`,lineHeight:1,overflow:`hidden`,flexShrink:0,boxSizing:`border-box`},'
    'children:[(0,L.jsx)(`span`,{children:r}),(0,L.jsx)(`span`,{children:a})]'
)
if OLD_KR in content:
    content = content.replace(OLD_KR, NEW_KR, 1)
    print('OK: country/continent chips amber')
else:
    errors.append('FAIL: kr component not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
