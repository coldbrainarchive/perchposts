#!/usr/bin/env python3
"""Patch v1308 -> v1309: scroller videos freezing when flipping with sound on.
v1308 tagged scroller videos so any mute change saved the sound setting; the scroller mutes a video itself when the
phone blocks starting it with sound, which flipped the setting mid-swipe. Scroller videos are untagged again (its
speaker button already saves the choice); only post-page / chirp videos (native controls) save via volumechange."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1308.js'
dst = '_deploy/assets/index-DUcNPOLc-v1309.js'
c = open(src, encoding='utf-8').read()
old = "if(v.muted)v.setAttribute(`muted`,``);v.dataset.snd=``;"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "if(v.muted)v.setAttribute(`muted`,``);"); print('OK: untag scroller videos')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
