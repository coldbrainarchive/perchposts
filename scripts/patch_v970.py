#!/usr/bin/env python3
"""Patch v969 -> v970: desktop, clicking the message box always brings the chat into view, not just when it
first gets focus (it stays focused after you scroll back up, so a second click did nothing before)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v969.js'
dst = '_deploy/assets/index-DUcNPOLc-v970.js'
c = open(src, encoding='utf-8').read()
old = " document.addEventListener(`focusin`,e=>{const t=e.target;if(!H.classList.contains(`dc-on`)||!t.closest||!t.closest(`.chat-compose`))return;"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, " const _dcGo=e=>{const t=e.target;if(!H.classList.contains(`dc-on`)||!t.closest||!t.closest(`.chat-compose`))return;")
old2 = "if(d>4)scrollTo({top:scrollY+d,behavior:matchMedia(`(prefers-reduced-motion: reduce)`).matches?`auto`:`smooth`})});"
if c.count(old2) != 1: print('FAIL2', c.count(old2)); sys.exit(1)
c = c.replace(old2, "if(d>4)scrollTo({top:scrollY+d,behavior:matchMedia(`(prefers-reduced-motion: reduce)`).matches?`auto`:`smooth`})};document.addEventListener(`focusin`,_dcGo);document.addEventListener(`pointerdown`,_dcGo);")
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
