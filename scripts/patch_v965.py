#!/usr/bin/env python3
"""Patch v964 -> v965: Safari draws its toolbar / keyboard bar (address pill, arrows + ✓) over the page's base
colour and darkens it ~1-2 shades with its glass, leaving a band just below the message box. In the open
chat, the base colour (html/body, only visible under Safari's own strips) is a touch lighter (#15181d), so
after Safari's tint it lands on the chat's #14161b."""
src = '_deploy/assets/index-DUcNPOLc-v964.js'
dst = '_deploy/assets/index-DUcNPOLc-v965.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`html.chat-open,html.chat-open body{background:#15181d!important}`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
