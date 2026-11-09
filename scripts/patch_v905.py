#!/usr/bin/env python3
"""Patch v904 -> v905: shorter Filters tab. Each section's label sits to the left of its pills (a centred
two-column grid) instead of above them, the pills are 22px like the board pills, and labels are shorter
(🪽 Flaps, 💬 Chirps, 🤖 Bots, 🕐 Time; "Any time" -> "Any")."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v904.js'
dst = '_deploy/assets/index-DUcNPOLc-v905.js'
content = open(src, encoding='utf-8').read()
reps = [
 ('.srch-filters { display: flex; flex-direction: column; gap: 6px; padding: 10px 14px 8px; }',
  '.srch-filters { display: grid; grid-template-columns: auto auto; justify-content: center; align-items: center; column-gap: 10px; row-gap: 8px; padding: 10px 10px 8px; }\n'
  '      .srch-filters .search-section-label { flex-basis: auto; padding: 0; text-align: right; white-space: nowrap; }\n'
  '      .srch-filters .srch-row { margin: 0; flex-wrap: nowrap; justify-content: flex-start; }'),
 ('.srch-opt { height: 26px; padding: 0 10px;', '.srch-opt { height: 22px; padding: 0 9px;'),
 ('color: #cbd5e1; font-size: 12px; font-weight: 700; cursor: pointer; white-space: nowrap; }',
  'color: #cbd5e1; font-size: 11px; font-weight: 700; cursor: pointer; white-space: nowrap; }'),
 ('.srch-time { height: 26px;', '.srch-time { height: 22px; max-width: 120px;'),
 ('color: #cbd5e1; font-size: 12px; font-weight: 700; padding: 0 10px; color-scheme: dark;',
  'color: #cbd5e1; font-size: 11px; font-weight: 700; padding: 0 9px; color-scheme: dark;'),
 ('children:`🪽 Most flaps`}),', 'children:`🪽 Flaps`}),'),
 ('children:`💬 Most chirps`}),', 'children:`💬 Chirps`}),'),
 ('(0,L.jsx)(`div`,{className:`search-section-label`,children:`Bots`}),', '(0,L.jsx)(`div`,{className:`search-section-label`,children:`🤖 Bots`}),'),
 ('(0,L.jsx)(`div`,{className:`search-section-label`,children:`Time`}),', '(0,L.jsx)(`div`,{className:`search-section-label`,children:`🕐 Time`}),'),
 ('_pill(!q2,`Any time`,()=>ae()),', '_pill(!q2,`Any`,()=>ae()),'),
]
for o, n in reps:
    if content.count(o) != 1: print('FAIL', content.count(o), o); sys.exit(1)
    content = content.replace(o, n)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
