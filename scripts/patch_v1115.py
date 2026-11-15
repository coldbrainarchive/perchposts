#!/usr/bin/env python3
"""Patch v1114 -> v1115: signed out, the flap in the full-screen preview closes it like tapping out (back to the same
spot in the feed) AND flashes the Sign In button, as other signed-out taps do."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1114.js'
dst = '_deploy/assets/index-DUcNPOLc-v1115.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("const flap=(s,id)=>{if(!localStorage.getItem(`auth_token`)){close();return}",
      "const flap=(s,id)=>{if(!localStorage.getItem(`auth_token`)){pendingNoAuth=!0;close();return}", 'flap marks signed-out')
# the flash no longer replaces putting you back at your spot: it happens as well
patch("if(pendingNoAuth){window.dispatchEvent(new CustomEvent(`like-no-auth`))}else if(pendingChat){",
      "if(pendingNoAuth)setTimeout(()=>window.dispatchEvent(new CustomEvent(`like-no-auth`)),60);if(pendingChat){", 'spot kept + sign-in flash')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
