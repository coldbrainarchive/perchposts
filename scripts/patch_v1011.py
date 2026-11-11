#!/usr/bin/env python3
"""Patch v1010 -> v1011: stop Safari's "AutoFill Contact" on the New Post boxes.
Safari ignores autocomplete="off" and offers contact AutoFill on pages it reads as a form (several boxes together).
It never offers it on search fields (the site search box never gets AutoFill), so the New Post boxes are set up the
same way in their own props (React resets name/type on every redraw, so they can't be changed from outside):
- title, Add Birds and link boxes: type="search", a search_… name, autocomplete off (styled exactly as before: no
  clear button, normal Enter key)
- the body / opening message box: a search_… name, autocomplete off."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1010.js'
dst = '_deploy/assets/index-DUcNPOLc-v1011.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('(0,L.jsx)(`input`,{value:a,onChange:e=>o(e.target.value),placeholder:_isHuddle?',
      '(0,L.jsx)(`input`,{type:`search`,name:`search_np_title`,autoComplete:`off`,enterKeyHint:`next`,value:a,onChange:e=>o(e.target.value),placeholder:_isHuddle?', 'title')
patch('(0,L.jsx)(`input`,{className:`search-input`,value:_hmTagQ,',
      '(0,L.jsx)(`input`,{className:`search-input`,type:`search`,name:`search_np_birds`,autoComplete:`off`,autoCorrect:`off`,autoCapitalize:`off`,spellCheck:!1,enterKeyHint:`search`,value:_hmTagQ,', 'add birds')
patch('(0,L.jsx)(`input`,{value:O,onChange:e=>k(e.target.value),onKeyDown:e=>e.key===`Enter`&&N(),placeholder:`Paste a URL...`',
      '(0,L.jsx)(`input`,{type:`search`,name:`search_np_link`,autoComplete:`off`,autoCorrect:`off`,autoCapitalize:`off`,spellCheck:!1,enterKeyHint:`go`,value:O,onChange:e=>k(e.target.value),onKeyDown:e=>e.key===`Enter`&&N(),placeholder:`Paste a URL...`', 'link')
patch('(0,L.jsx)(`textarea`,{value:s,onChange:e=>c(e.target.value),',
      '(0,L.jsx)(`textarea`,{name:`search_np_body`,autoComplete:`off`,value:s,onChange:e=>c(e.target.value),', 'body')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`.nh-card input[type=search]{-webkit-appearance:none;appearance:none}.nh-card input[type=search]::-webkit-search-cancel-button,.nh-card input[type=search]::-webkit-search-decoration,.nh-card input[type=search]::-webkit-search-results-button{-webkit-appearance:none;display:none}`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
