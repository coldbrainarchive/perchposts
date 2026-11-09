#!/usr/bin/env python3
"""Patch v928 -> v929: effects take the colour of the bird who did the thing; site purple stays for the site.
- Your send animation: your name-tag colour (read from your chirp's header), instead of purple.
- Incoming chirps materialize in the sender's colour.
- The jump/reply/find glow (_glow) uses that chirp author's colour (CSS var --gc in the chat-flash
  keyframes). Pinned chirps keep the purple pin glow.
- Notification rows: a 3px accent bar in the colour of the bird who flapped/chirped/invited (the first
  word of the notification), and unread rows are tinted with it (was purple). "You ..." rows get no bar.
Text on the coloured glow stays dark, like the name tags. Admin = white, mods = site purple."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v928.js'
dst = '_deploy/assets/index-DUcNPOLc-v929.js'
c = open(src, encoding='utf-8').read()
errors = []
def patch(old, new, label, s=None):
    global c
    n = c.count(old)
    if n != 1: errors.append(f'FAIL ({label}): {n}')
    else: c = c.replace(old, new); print('OK: ' + label)

# helper: an element's background colour as "r,g,b" (site purple if none)
HELPER = r'''
;window._rgbOf=function(el){try{if(!el)return'192,132,252';const m=(getComputedStyle(el).backgroundColor||'').match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/);if(!m||(m[4]!==undefined&&+m[4]===0))return'192,132,252';return Math.round(m[1])+','+Math.round(m[2])+','+Math.round(m[3])}catch(e){return'192,132,252'}};
'''
# 1. send animation (_chirpFly segment)
a = c.index('window._chirpFly=function'); b = c.index("}catch(e){H.classList.remove('chirp-fly')}};", a)
seg = c[a:b]
seg = seg.replace("  const g=document.createElement('div');", "  const C=window._rgbOf(body.querySelector('.chat-msg-meta'));\n  const g=document.createElement('div');", 1)
n1 = seg.count('rgba(192,132,252,'); n2 = seg.count("'#c084fc'")
seg = seg.replace('rgba(192,132,252,', "rgba('+C+',").replace("'#c084fc'", "'rgb('+C+')'")
c = c[:a] + seg + c[b:]
print(f'send animation: {n1} rgba + {n2} hex -> author colour')
# 2. incoming materialize (mat segment)
a = c.index('const mat=(w,body)=>{'); b = c.index('const pill=', a)
seg = c[a:b]
seg = seg.replace('const mat=(w,body)=>{', "const mat=(w,body)=>{const C=window._rgbOf(body.querySelector('.chat-msg-meta')),G='0 0 0 4px rgba('+C+',0.6),0 0 20px rgba('+C+',0.8)';", 1)
seg = seg.replace('boxShadow:GLOW', 'boxShadow:G').replace('rgba(192,132,252,', "rgba('+C+',").replace('background:#c084fc;', "background:rgb('+C+');")
c = c[:a] + seg + c[b:]
print('incoming materialize -> sender colour')
# 3. jump/reply glow
patch('function _glow(e){e=e.closest(`.chat-msg-body`)||e;',
      'function _glow(e){e=e.closest(`.chat-msg-body`)||e;try{const _gm=e.querySelector(`.chat-msg-meta`);if(_gm&&!e.classList.contains(`chat-pinned`))e.style.setProperty(`--gc`,window._rgbOf(_gm));else e.style.removeProperty(`--gc`)}catch(_){}', 'jump glow sets author colour')
for kf in ['@keyframes chat-flash{', '@keyframes chat-flash-fade{']:
    i = c.index(kf); j = c.index('}}', i) + 2
    body = c[i:j].replace('rgba(192,132,252,', 'rgba(var(--gc,192,132,252),').replace('rgba(216,180,254,', 'rgba(var(--gc,216,180,254),')
    c = c[:i] + body + c[j:]
print('flash keyframes use --gc (purple fallback for pins)')
# 4. notification rows
patch("background:t?`rgba(192,132,252,0.07)`:`transparent`},children:[(0,L.jsx)(`span`,{style:{fontSize:20,lineHeight:1,flexShrink:0},children:e.icon})",
      "background:t?`color-mix(in srgb, ${_ncol(e.text)} 10%, transparent)`:`transparent`,borderLeft:`3px solid ${_ncol(e.text)}`},children:[(0,L.jsx)(`span`,{style:{fontSize:20,lineHeight:1,flexShrink:0},children:e.icon})",
      'notification accent + tint')
patch('function Hn(e,t){', 'function _ncol(x){let _w=String(x||``).split(` `)[0];if(!_w||_w===`You`||_w===`Someone`)return`transparent`;let _l=_w.toLowerCase();return _adminUsers.has(_l)?`#ffffff`:_modUsers.has(_l)?`#c084fc`:Hn(null,_w)}function Hn(e,t){', 'notification colour helper')
if errors: print('\n'.join(errors)); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(c + HELPER); print('Wrote ' + dst)
