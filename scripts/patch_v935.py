#!/usr/bin/env python3
"""Patch v934 -> v935:
1. No thin line between the quoted chirp and the reply text (.chat-quote-bar border-bottom removed).
2. The "replying to" bar above the compose box looks like the posted quote: tinted in the replied-to bird's
   colour (no left stripe), same padding, coloured name, message up to 2 lines.
3. Send animation: the text no longer goes wonky in flight. Its font size and padding were animating while
   the bubble changed width, so the words kept reflowing. The flying text now sits at the chirp's final
   size on one line (ellipsis if long) the whole way.
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v934.js'
dst = '_deploy/assets/index-DUcNPOLc-v935.js'
c = open(src, encoding='utf-8').read()
errors = []
def patch(old, new, label, count=1):
    global c
    n = c.count(old)
    if n != count: errors.append(f'FAIL ({label}): {n}')
    else: c = c.replace(old, new); print('OK: ' + label)
patch('border-bottom: 1px solid rgba(var(--rc,192,132,252),0.18);', 'border-bottom: none;', 'no line under quote')
patch('padding: 6px 10px;\n        background: rgba(148, 163, 184, 0.07);\n        border-radius: 10px;\n        border-left: 3px solid rgb(var(--rc,192,132,252));',
      'padding: 8px 12px;\n        background: rgba(var(--rc,192,132,252),0.22);\n        border-radius: 14px;\n        border-left: none;', 'reply preview like quote')
patch('.chat-reply-preview-text {\n        margin: 0;\n        font-size: 12px;\n        color: #8fa0b6;\n        overflow: hidden;\n        white-space: nowrap;\n        text-overflow: ellipsis;',
      '.chat-reply-preview-text {\n        margin: 0;\n        font-size: 12px;\n        color: #8fa0b6;\n        overflow: hidden;\n        display: -webkit-box;\n        -webkit-line-clamp: 2;\n        -webkit-box-orient: vertical;', 'reply preview text 2 lines')
# send ghost text: fixed final size, single line
patch("  g.textContent=(text||'').slice(0,400);\n  g.style.cssText='position:fixed;z-index:2147483000;pointer-events:none;box-sizing:border-box;overflow:hidden;white-space:pre-wrap;word-break:break-word;display:flex;flex-direction:column;justify-content:flex-end;'+",
      "  const _gt=document.createElement('span');_gt.textContent=(text||'').replace(/\\s+/g,' ').slice(0,400);_gt.style.cssText='display:block;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;';g.appendChild(_gt);\n"
      "  g.style.cssText='position:fixed;z-index:2147483000;pointer-events:none;box-sizing:border-box;overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;font-size:'+cs.fontSize+';padding:'+cs.padding+';'+", 'flying text fixed size, one line')
patch(",fontSize:'16px',padding:'12px 16px',", ",", 'no font/padding animation (start)')
patch(",fontSize:cs.fontSize,padding:cs.padding,borderColor:'rgb('+C+')'", ",borderColor:'rgb('+C+')'", 'no font/padding animation (flight)', count=2)
if errors: print('\n'.join(errors)); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(c); print('Wrote ' + dst)
