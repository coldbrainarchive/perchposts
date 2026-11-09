#!/usr/bin/env python3
"""Patch v890 -> v892: on phones, keyword search no longer filters the feed while you type.
The typed text used to go into the URL (?q=) 300ms after each pause, which re-ran the keyword search and
re-rendered the feed under the search box; iOS misdrew the cursor every time that happened (only for keyword
searches, since tag suggestions don't touch the feed). Now, on touch devices, the URL is only updated once the
search box loses focus: pressing Search on the keyboard (Enter) blurs it, and so does closing the keyboard.
Tag and user suggestions in the dropdown still update live. Desktop keeps live filtering.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v890.js'
dst = '_deploy/assets/index-DUcNPOLc-v892.js'
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n != 1:
        errors.append('FAIL (' + label + '): found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

TOUCH = "window.matchMedia&&matchMedia(`(pointer:coarse)`).matches"

# 1. While the search box is focused on a phone, don't push the typed text into the URL.
patch("let e=new URLSearchParams(u.current);if((e.get(`q`)||``)!==n.trim()){n.trim()?e.set(`q`,n.trim()):e.delete(`q`),t(e,{replace:!0})}n.trim()?fetch(",
      "let e=new URLSearchParams(u.current);if(!(" + TOUCH + "&&document.activeElement===c.current)&&(e.get(`q`)||``)!==n.trim()){n.trim()?e.set(`q`,n.trim()):e.delete(`q`),t(e,{replace:!0})}n.trim()?fetch(",
      'defer URL update while focused')

# 2. Apply it when the box loses focus; Enter (keyboard Search) blurs the box.
patch("onFocus:()=>a(!0),onKeyDown:e=>{e.key===`Escape`&&(a(!1),s(null)),",
      "onFocus:()=>a(!0),onBlur:()=>{if(!(" + TOUCH + "))return;setTimeout(()=>{if(!c.current||document.activeElement===c.current)return;"
      "const v=c.current.value.trim();let e=new URLSearchParams(u.current);if((e.get(`q`)||``)!==v){v?e.set(`q`,v):e.delete(`q`),t(e,{replace:!0})}},0)},"
      "onKeyDown:e=>{e.key===`Enter`&&" + TOUCH + "&&c.current&&c.current.blur(),e.key===`Escape`&&(a(!1),s(null)),",
      'commit on blur / Enter')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
