#!/usr/bin/env python3
"""Patch v90 -> v91: massively expanded bird username pools."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v90.js'
dst = '_deploy/assets/index-DUcNPOLc-v91.js'

# ── Pool A: adjective/region/color (first word) ──────────────────────────────
# 100 words
POOL_A = [
    "african","alpine","amazonian","american","andean","arabian","arctic","ashy","asian",
    "australasian","azure","banded","barred","black","blue","bornean","brown","buff",
    "burmese","cape","chestnut","chinese","cinnamon","collared","common","copper",
    "crested","crimson","dark","dusky","eastern","elegant","emerald","eurasian",
    "european","fiery","flame","giant","golden","greater","green","grey","himalayan",
    "hooded","indian","indigo","island","javan","lesser","lilac","little","long",
    "magenta","maroon","melodious","mongolian","mountain","northern","olive","orange",
    "oriental","pacific","painted","pale","papuan","philippine","pink","purple",
    "pygmy","red","royal","rufous","rusty","sacred","scarlet","short","siberian",
    "silvery","slaty","sooty","southern","speckled","spotted","streaked","striped",
    "sumatran","tibetan","tropical","turquoise","varied","velvet","violet","western",
    "white","yellow","cinnamon","coral","dusky","ferruginous","fulvous","garnet",
    "glossy","iridescent","malachite","oceanic","ringed","tawny",
]

# ── Pool B: body-part descriptor (middle word) ────────────────────────────────
# 42 words
POOL_B = [
    "backed","banded","bellied","billed","breasted","browed","capped","cheeked",
    "chested","chinned","collared","crowned","eared","eyed","faced","flanked",
    "fronted","gorgeted","headed","hooded","legged","lored","mantled","masked",
    "naped","necked","plumed","ringed","rumped","shouldered","sided","spotted",
    "streaked","striped","tailed","throated","tipped","vented","winged","crested",
    "bibbed","footed",
]

# ── Pool C: bird type (last word) ─────────────────────────────────────────────
# 115 words
POOL_C = [
    "albatross","antbird","antpitta","antshrike","aracari","avocet","babbler",
    "barbet","bee-eater","bittern","blackbird","booby","broadbill","bulbul",
    "bunting","bustard","buzzard","canary","cisticola","cockatoo","conebill",
    "cormorant","cotinga","coucal","crane","creeper","cuckoo","dacnis","dove",
    "drongo","duck","eagle","egret","elaenia","falcon","fantail","finch",
    "flamingo","flowerpecker","flycatcher","francolin","gerygone","goshawk",
    "grebe","grosbeak","gull","harrier","hawk","heron","honeyeater","hornbill",
    "hummingbird","ibis","jacamar","jay","kestrel","kingfisher","kite","lark",
    "lorikeet","magpie","manakin","martin","merganser","mockingbird","monarch",
    "nightjar","nuthatch","oriole","owl","parakeet","parrot","pelican","penguin",
    "petrel","pheasant","pigeon","pipit","plover","puffbird","rail","raven",
    "robin","sandpiper","shrike","skua","snipe","sparrow","starling","stork",
    "sunbird","swallow","swift","tanager","teal","tern","thrush","tit","toucan",
    "trogon","tyrannulet","vireo","vulture","warbler","waxbill","waxwing",
    "weaver","whistler","woodpecker","wren","flycatcher","jacana","lapwing",
    "lorikeet","myzomela","parrotbill","pitta","tailorbird","treecreeper",
]

# deduplicate while preserving order
def dedup(lst):
    seen = set()
    out = []
    for x in lst:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

POOL_A = dedup(POOL_A)
POOL_B = dedup(POOL_B)
POOL_C = dedup(POOL_C)

combos = len(POOL_A) * len(POOL_B) * len(POOL_C)
print(f'Pool A: {len(POOL_A)} words')
print(f'Pool B: {len(POOL_B)} words')
print(f'Pool C: {len(POOL_C)} words')
print(f'Total unique combinations: {combos:,}')

def js_array(lst):
    quoted = ','.join(f'"{w}"' for w in lst)
    return f'[{quoted}]'

BIRD_GEN = (
    '(function(){'
    f'var _a={js_array(POOL_A)},'
    f'_b={js_array(POOL_B)},'
    f'_c={js_array(POOL_C)};'
    'return _a[Math.floor(Math.random()*_a.length)]+"-"+'
    '_b[Math.floor(Math.random()*_b.length)]+"-"+'
    '_c[Math.floor(Math.random()*_c.length)];'
    '})()'
)

content = open(src, encoding='utf-8').read()

# Find and replace both BIRD_GEN IIFEs
OLD_IIFE_START = '(function(){var _a=['
count = content.count(OLD_IIFE_START)
print(f'Found {count} IIFE(s) to replace')

if count != 2:
    print('ERROR: expected exactly 2 IIFEs')
    sys.exit(1)

# Replace each one by finding start -> end
result = content
replaced = 0
search_from = 0
while True:
    idx = result.find(OLD_IIFE_START, search_from)
    if idx == -1:
        break
    end = result.find('})()', idx)
    if end == -1:
        print('ERROR: could not find IIFE end')
        sys.exit(1)
    old_iife = result[idx:end+4]
    result = result[:idx] + BIRD_GEN + result[end+4:]
    search_from = idx + len(BIRD_GEN)
    replaced += 1
    print(f'Replaced IIFE #{replaced} (was {len(old_iife)} chars -> now {len(BIRD_GEN)} chars)')

if replaced != 2:
    print(f'ERROR: replaced {replaced}, expected 2')
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(result)
print(f'\nWrote {dst}')
print(f'With {combos:,} unique username combinations possible')
