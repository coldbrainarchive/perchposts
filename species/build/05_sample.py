# print a readable sample of the species database
import json, sys
recs = {r["name"]: r for r in json.load(open("species/out/species.json"))}
NAMES = sys.argv[1:] or ["Mallard", "Canada Goose", "Peregrine Falcon", "Ruby-throated Hummingbird", "Snowy Owl", "Emperor Penguin",
    "Common Ostrich", "Kakapo", "Atlantic Puffin", "American Robin", "Keel-billed Toucan", "Scarlet Macaw", "Arctic Tern", "Bald Eagle",
    "Greater Flamingo", "Southern Brown Kiwi", "Laughing Kookaburra", "Resplendent Quetzal", "Shoebill", "House Sparrow"]
IUCN = {"LC": "Least Concern", "NT": "Near Threatened", "VU": "Vulnerable", "EN": "Endangered", "CR": "Critically Endangered", "DD": "Data Deficient", None: "?"}
MIG = {1: "stays put", 2: "partly migratory", 3: "migratory", None: "?"}
def start(r):
    p = r["photos"]
    if not p["any"]: return "left out (no usable photo)"
    return "juvenile/hatchling photos" if p["juv"] >= 3 else "starts as adult"
for n in NAMES:
    r = recs.get(n)
    if not r: print("?? not found:", n); continue
    top = ", ".join(f"{c} {round(v * 100)}%" for c, v in list((r.get("countries") or {}).items())[:4]) or "?"
    move = "flightless" + (", swims" if r["swims"] else ", runs") if r["flightless"] else f"speed {r.get('speed')}/10 · stamina {r.get('stamina')}/10" + (" · swims" if r["swims"] else "")
    p = r["photos"]
    print(f"{r['name']} ({r['sci']}) — {r['group']} · {r['familyName']}")
    print(f"   {move} · {r.get('diet') or '?'} · {r.get('mass') or '?'} g · wingspan {r.get('wingspanCm') or '?'} cm · {MIG[r.get('migration')]}")
    print(f"   {IUCN[r['iucn']]} · egg rarity: {r['rarity']} · countries: {top}")
    print(f"   photos: {p['any']} (adult {p['adult']}, juvenile {p['juv']}, female {p['female']}, male {p['male']}) → {start(r)}")
