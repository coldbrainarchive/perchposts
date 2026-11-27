# Merge everything into one record per species -> species/out/species.json
# Sources: eBird/Clements taxonomy (species list, order, family) · AVONET (Tobias et al. 2022, CC BY 4.0: body traits, habitat,
# diet, migration, range) · Avian wingspan database (Fox et al. 2026, CC BY 4.0) · Wikidata (CC0: IUCN status) ·
# iNaturalist (photo coverage, reusable licences only) · GBIF (sightings per country)
import csv, json, math, os, statistics, collections
import openpyxl

R = "species/raw/"
tax = [r for r in csv.DictReader(open(R + "ebird_taxonomy.csv")) if r["CATEGORY"] == "species" and not r["EXTINCT"]]

def sheet(name, key):
    ws = openpyxl.load_workbook(R + "avonet.xlsx", read_only=True)[name]
    rows = ws.iter_rows(values_only=True); hdr = next(rows)
    na = lambda v: None if v in ("NA", "") else v   # AVONET writes missing values as "NA"
    return {r[hdr.index(key)]: {h: na(v) for h, v in zip(hdr, r)} for r in rows if r[hdr.index(key)]}
av2 = sheet("AVONET2_eBird", "Species2")          # traits, eBird names (2021)
av1 = sheet("AVONET1_BirdLife", "Species1")       # range size + centroid, BirdLife names
cw = openpyxl.load_workbook(R + "avonet.xlsx", read_only=True)["BirdLife-eBird crosswalk"]
bl_of = collections.defaultdict(list)             # eBird name -> BirdLife names
it = cw.iter_rows(values_only=True); next(it)
for r in it:
    if r[0] and r[1]: bl_of[r[1]].append(r[0])
ws = openpyxl.load_workbook(R + "wingspan.xlsx", read_only=True)["wingspan data"]
it = ws.iter_rows(values_only=True); hdr = next(it)
wing = {}
for r in it:
    d = dict(zip(hdr, r))
    fv = lambda x: float(x) if x not in (None, "", "NA") else None
    rep = fv(d.get("wingspan_reported_mid_all")); v = rep or fv(d.get("wingspan_predicted_order")) or fv(d.get("wingspan_predicted_global"))
    if d.get("Species1") and v: wing[d["Species1"]] = (v, rep is None)
wd = json.load(open(R + "wikidata.json"))
inat = json.load(open(R + "inat_coverage.json"))
gb = json.load(open(R + "gbif_countries.json")) if os.path.exists(R + "gbif_countries.json") else {}
effort = {c["name"]: c["count"] for c in json.load(open(R + "gbif_effort.json"))["facets"][0]["counts"]}
area = json.load(open(R + "country_area.json"))   # World Bank land area, km2

# groups: one per order, with a plain name (abilities come later)
GROUPS = {"Passeriformes": "Songbirds", "Apodiformes": "Swifts & Hummingbirds", "Piciformes": "Woodpeckers & Toucans", "Psittaciformes": "Parrots",
  "Charadriiformes": "Shorebirds & Gulls", "Columbiformes": "Pigeons & Doves", "Galliformes": "Gamebirds", "Accipitriformes": "Hawks & Eagles",
  "Strigiformes": "Owls", "Coraciiformes": "Kingfishers & Rollers", "Anseriformes": "Waterfowl", "Gruiformes": "Cranes & Rails",
  "Cuculiformes": "Cuckoos", "Procellariiformes": "Albatrosses & Petrels", "Pelecaniformes": "Pelicans, Herons & Ibises", "Caprimulgiformes": "Nightjars",
  "Bucerotiformes": "Hornbills & Hoopoes", "Falconiformes": "Falcons", "Suliformes": "Cormorants & Gannets", "Tinamiformes": "Tinamous",
  "Trogoniformes": "Trogons", "Otidiformes": "Bustards", "Musophagiformes": "Turacos", "Ciconiiformes": "Storks", "Podicipediformes": "Grebes",
  "Sphenisciformes": "Penguins", "Pterocliformes": "Sandgrouse", "Podargiformes": "Frogmouths", "Aegotheliformes": "Owlet-nightjars",
  "Nyctibiiformes": "Potoos", "Cathartiformes": "New World Vultures", "Phoenicopteriformes": "Flamingos", "Coliiformes": "Mousebirds",
  "Apterygiformes": "Kiwis", "Gaviiformes": "Loons", "Casuariiformes": "Cassowaries & Emus", "Mesitornithiformes": "Mesites",
  "Phaethontiformes": "Tropicbirds", "Struthioniformes": "Ostriches", "Rheiformes": "Rheas", "Eurypygiformes": "Kagu & Sunbittern",
  "Cariamiformes": "Seriemas", "Steatornithiformes": "Oilbird", "Opisthocomiformes": "Hoatzin", "Leptosomiformes": "Cuckoo-roller"}
FLIGHTLESS_ORDERS = {"Sphenisciformes", "Struthioniformes", "Rheiformes", "Casuariiformes", "Apterygiformes"}
# flightless birds outside the ratite/penguin orders (hand-checked)
FLIGHTLESS_GENERA = {"Strigops", "Apteryx", "Gallirallus", "Hypotaenidia", "Habroptila", "Megacrex", "Atlantisia", "Aptenodytes"}
FLIGHTLESS_SPECIES = {"Porphyrio hochstetteri", "Tachyeres pteneres", "Tachyeres brachypterus", "Tachyeres leucocephalus", "Nannopterum harrisi",
  "Anas aucklandica", "Anas nesiotis", "Rollandia microptera", "Podiceps taczanowskii", "Rhynochetos jubatus", "Laterallus rogersi",
  "Gallinula comeri", "Porzana atra", "Zapornia atra", "Gallirallus australis", "Hypotaenidia sylvestris", "Cabalus modestus", "Dryolimnas aldabranus",
  "Dryolimnas cuvieri aldabranus", "Lewinia muelleri", "Gallicolumba stairi", "Pezophaps solitaria", "Mergus australis"}
IUCN_W = {"LC": 1, "NT": .45, "VU": .2, "EN": .08, "CR": .025, "DD": .3, None: .6}

def num(v):
    try: return float(v)
    except (TypeError, ValueError): return None

recs = []
genus_traits = collections.defaultdict(list)
for t in tax:
    sci = t["SCIENTIFIC_NAME"]; a = av2.get(sci); bls = bl_of.get(sci, []) if a else []
    if not a:   # name spelled differently (e.g. habroptila / habroptilus): same genus, same start of the species name
        g, e = sci.split()[0], sci.split()[1]
        hit = next((k for k in av1 if k.split()[0] == g and k.split()[1][:5] == e[:5]), None) or next((k for k in av2 if k.split()[0] == g and k.split()[1][:5] == e[:5]), None)
        if hit in av1: a, bls = av1[hit], [hit]
        elif hit: a, bls = av2[hit], bl_of.get(hit, [])
    r = {"code": t["SPECIES_CODE"], "name": t["COMMON_NAME"], "sci": sci, "order": t["ORDER"], "family": t["FAMILY_SCI_NAME"],
         "familyName": t["FAMILY_COM_NAME"], "group": GROUPS.get(t["ORDER"], t["ORDER"]), "traitsFrom": "measured" if a else None}
    if a:
        r.update(mass=num(a["Mass"]), wingLen=num(a["Wing.Length"]), hwi=num(a["Hand-Wing.Index"]), habitat=a["Habitat"],
                 migration=int(a["Migration"]) if a["Migration"] else None, diet=a["Trophic.Niche"], lifestyle=a["Primary.Lifestyle"])
        genus_traits[sci.split()[0]].append(r)
    rng = [num(av1[b]["Range.Size"]) for b in bls if b in av1 and num(av1[b]["Range.Size"])]
    r["rangeKm2"] = sum(rng) if rng else None
    ws_ = [wing[b] for b in bls if b in wing]
    r["wingspanCm"] = round(statistics.mean(w[0] for w in ws_), 1) if ws_ else None
    r["flightless"] = t["ORDER"] in FLIGHTLESS_ORDERS or sci in FLIGHTLESS_SPECIES or sci.split()[0] in FLIGHTLESS_GENERA
    w = wd.get(t["SPECIES_CODE"], {}); r["iucn"] = w.get("iucn"); r["wikidata"] = w.get("wd")
    i = inat.get(sci, {}); r["photos"] = {k: i.get(k, 0) for k in ("any", "adult", "juv", "female", "male")}; r["inat"] = i.get("inat")
    recs.append(r)

# species newer than AVONET (taxonomy splits since 2021): borrow the genus average, marked as estimated
for r in recs:
    if r["traitsFrom"]: continue
    g = genus_traits.get(r["sci"].split()[0])
    if not g: continue
    r["traitsFrom"] = "genus estimate"
    for k in ("mass", "wingLen", "hwi"):
        vals = [x[k] for x in g if x.get(k)]; r[k] = round(statistics.mean(vals), 2) if vals else None
    for k in ("habitat", "migration", "diet", "lifestyle"):
        vals = [x[k] for x in g if x.get(k) is not None]; r[k] = collections.Counter(vals).most_common(1)[0][0] if vals else None

# game stats 1-10 from real traits, on fixed scales (not ranks: most species are small tropical songbirds, which pushed every
# well-known bird to 10). Speed: estimated cruising km/h - grows with weight^(1/6) (Pennycuick) and pointier wings (hand-wing index).
# Stamina: how far it can go - wing pointiness x how migratory x a little for size (fuel reserves).
def scale(v, lo, hi): return max(1, min(10, 1 + round(9 * (v - lo) / (hi - lo))))
for r in recs:
    if r.get("mass") and r.get("hwi"):
        r["kmh"] = round(15 * r["mass"] ** (1 / 6) * (max(r["hwi"], 5) / 30) ** .3)
        r["speed"] = scale(math.log(r["kmh"]), math.log(19), math.log(75))
        st = r["hwi"] * (1, 1.5, 2.2)[(r["migration"] or 1) - 1] * r["mass"] ** .08
        r["staminaRaw"] = round(st, 1); r["stamina"] = scale(math.log(st), math.log(11), math.log(260))
for r in recs:
    r["swims"] = r.get("lifestyle") == "Aquatic" or r["order"] in ("Sphenisciformes", "Anseriformes", "Gaviiformes", "Podicipediformes")
    if r["flightless"]: r["speed"] = r["stamina"] = None   # they run or swim instead (game mechanics later)

# how often it hatches: range size x conservation status (rare and endangered birds are rare finds)
for r in recs:
    r["eggWeight"] = round(math.sqrt(r["rangeKm2"] or 2e4) * IUCN_W.get(r["iucn"], .6), 2)
ws_sorted = sorted(r["eggWeight"] for r in recs)
def tier(w):
    p = sum(1 for x in ws_sorted if x <= w) / len(ws_sorted)
    return "common" if p > .6 else "uncommon" if p > .3 else "rare" if p > .1 else "very rare" if p > .02 else "legendary"
for r in recs: r["rarity"] = tier(r["eggWeight"])

# home countries, weighted like a population: how big a share of a country's bird sightings this species is (evens out countries
# full of birdwatchers, like the US), times the square root of the country's size (so a bird common across Canada outweighs one
# common across Belgium; size counts a little less than a square root, so huge countries don't win on size alone).
# Countries with few sightings are smoothed (+100k), stray visitors (vagrants) dropped.
for r in recs:
    g = gb.get(r["sci"])
    if not g: r["countries"] = None; continue
    c = g["c"]; tot = sum(c.values()) or 1
    # ZZ / XZ = GBIF's "unknown country" and "high seas" codes: not a home
    w = {k: v / (effort.get(k, 0) + 1e5) * area.get(k, 2e3) ** .35 for k, v in c.items() if v >= max(3, .002 * tot) and k not in ("ZZ", "XZ", "QO")}
    s = sum(w.values()) or 1
    r["countries"] = {k: round(v / s, 4) for k, v in sorted(w.items(), key=lambda x: -x[1]) if v / s >= .002}
    r["sightings"] = g["n"]

os.makedirs("species/out", exist_ok=True)
json.dump(recs, open("species/out/species.json", "w"))
have = lambda f: sum(1 for r in recs if r.get(f))
print(len(recs), "species | traits:", have("traitsFrom"), "| wingspan:", have("wingspanCm"), "| IUCN:", have("iucn"),
      "| photos:", sum(1 for r in recs if r["photos"]["any"]), "| countries:", have("countries"))
print(collections.Counter(r["traitsFrom"] for r in recs), collections.Counter(r["rarity"] for r in recs))
