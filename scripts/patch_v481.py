#!/usr/bin/invoke python3
"""Patch v480 -> v481: Wrap the remaining bare onClick:l in the notification
panel (the 'View Post' link) so it also resets --ptr-bg when closing."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v480.js'
dst = '_deploy/assets/index-DUcNPOLc-v481.js'

content = open(src, encoding='utf-8').read()

OLD = 'to:`/post/${p}`,onClick:l,style:'
NEW = 'to:`/post/${p}`,onClick:()=>{l();document.documentElement.style.setProperty(`--ptr-bg`,`#0b0f12`)},style:'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: view-post link close resets --ptr-bg')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
