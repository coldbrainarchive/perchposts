#!/usr/bin/env python3
"""Patch v1019 -> v1020: logging in (or signing up) refreshes the notification bubble straight away.
The bubble only checked on page load and every 30 seconds, so after logging in it could take up to 30s
(or a refresh) to show. Every place that saves a login now pings the bubble right after (and once more a
moment later, once the account details have settled)."""
import re, sys
src = '_deploy/assets/index-DUcNPOLc-v1019.js'
dst = '_deploy/assets/index-DUcNPOLc-v1020.js'
c = open(src, encoding='utf-8').read()
c, n = re.subn(r'localStorage\.setItem\(`auth_token`,(\w+)\.token\)', r'localStorage.setItem(`auth_token`,\1.token),_authPing()', c)
if n != 3: print('FAIL login sites', n); sys.exit(1)
print('OK: login sites', n)
c += r'''
function _authPing(){try{const go=()=>window.dispatchEvent(new Event(`notif-read`));setTimeout(go,60);setTimeout(go,1500)}catch(e){}}
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
