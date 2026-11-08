#!/usr/bin/env python3
"""Patch v114 -> v115: replace _showBlock modals with plain alert() for ban/cage."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v114.js'
dst = '_deploy/assets/index-DUcNPOLc-v115.js'

content = open(src, encoding='utf-8').read()
errors = []

CAGE_ALERT = 'alert("You\'re caged — you can only post and comment in the Cage")'
BAN_ALERT  = 'alert("You are banned from postchats.")'

CAGE_BLOCK = '_showBlock("You’re caged — you can only post and comment in the \U0001fab9 Cage tag.","caged")'
BAN_BLOCK  = '_showBlock("You are banned from postchats.")'

replaced = 0
while CAGE_BLOCK in content:
    content = content.replace(CAGE_BLOCK, CAGE_ALERT, 1)
    replaced += 1
print(f'OK: replaced {replaced} cage _showBlock -> alert')

replaced = 0
while BAN_BLOCK in content:
    content = content.replace(BAN_BLOCK, BAN_ALERT, 1)
    replaced += 1
print(f'OK: replaced {replaced} ban _showBlock -> alert')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
