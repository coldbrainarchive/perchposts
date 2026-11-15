#!/usr/bin/env python3
"""Patch v1113 -> v1114: in the full-screen link preview (reel), tapping the flap while signed out just closes the preview
and returns to the post, the same as tapping out of it (it used to close and then open the sign-in prompt)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1113.js'
dst = '_deploy/assets/index-DUcNPOLc-v1114.js'
c = open(src, encoding='utf-8').read()
old = "const flap=(s,id)=>{const b=_reelFlapBtn(id);if(!b)return;"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "const flap=(s,id)=>{if(!localStorage.getItem(`auth_token`)){close();return}const b=_reelFlapBtn(id);if(!b)return;"); print('OK: signed-out flap closes the preview')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
