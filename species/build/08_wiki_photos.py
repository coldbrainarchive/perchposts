# Hero photos from Wikipedia / Wikimedia Commons.
# Main photo: the species' Wikidata image (P18), the photo editors chose to represent it (usually the male / adult).
# Female photo: an image in the English Wikipedia article whose file name says female.
# Keeps the licence and author for each, downloads one ~1280px copy of each chosen photo.
# Usage: 08_wiki_photos.py [names file]   (default: the 30 test species) -> species/raw/wiki_photos/results.json
import json, os, re, sys, time, urllib.request, urllib.parse, urllib.error
sys.path.insert(0, os.path.dirname(__file__))
UA = {"User-Agent": "species-db-build/1.0 (bird species database; one request at a time)"}
DIR = "species/raw/wiki_photos"; os.makedirs(DIR, exist_ok=True)
sp = {s["name"]: s for s in json.load(open("species/out/species.json"))}
TEST = ["Mallard", "Canada Goose", "Bald Eagle", "American Flamingo", "King Penguin", "Common Ostrich", "House Sparrow",
        "Anna's Hummingbird", "Great Blue Heron", "Great Horned Owl", "Northern Cardinal", "Rainbow Lorikeet",
        "Belted Kingfisher", "Ring-necked Pheasant", "Peregrine Falcon", "Common Loon", "Double-crested Cormorant",
        "Pied-billed Grebe", "Mourning Dove", "Downy Woodpecker", "Killdeer", "Laughing Kookaburra", "Common Hoopoe",
        "Emu", "Turkey Vulture", "Tawny Frogmouth", "White Stork", "Black-headed Gull", "Common Swift", "Hoatzin"]
names = [l.strip() for l in open(sys.argv[1])] if len(sys.argv) > 1 else TEST
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def api(host, **p):
    url = f"https://{host}/w/api.php?" + urllib.parse.urlencode({"format": "json", "formatversion": 2, "maxlag": 5, **p})
    for t in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception: time.sleep(3 * (t + 1))
    return {}

ids = {n: sp[n]["wikidata"] for n in names if sp[n].get("wikidata")}
ents = {}
L = list(ids.values())
for i in range(0, len(L), 50):
    ents.update(api("www.wikidata.org", action="wbgetentities", ids="|".join(L[i:i + 50]), props="claims|sitelinks").get("entities", {}))

def info(files):
    # licence, author, a 1280px link for each Commons file
    out = {}
    for i in range(0, len(files), 40):
        r = api("commons.wikimedia.org", action="query", titles="|".join("File:" + f for f in files[i:i + 40]), prop="imageinfo",
                iiprop="url|extmetadata|size", iiurlwidth=1280)
        for pg in r.get("query", {}).get("pages", []):
            ii = (pg.get("imageinfo") or [{}])[0]; md = ii.get("extmetadata", {})
            strip = lambda v: re.sub(r"<[^>]+>", "", (md.get(v) or {}).get("value", "")).strip()
            out[pg["title"][5:]] = {"url": ii.get("thumburl") or ii.get("url"), "page": ii.get("descriptionurl"),
                                    "license": strip("LicenseShortName"), "author": strip("Artist"), "w": ii.get("width"), "h": ii.get("height")}
    return out

res = {}
for n in names:
    e = ents.get(ids.get(n), {}); cl = e.get("claims", {})
    p18 = [c["mainsnak"]["datavalue"]["value"] for c in cl.get("P18", []) if c["mainsnak"].get("datavalue")]
    # no Wikidata link in our database: try the scientific name as the article title (Wikipedia redirects it)
    title = (e.get("sitelinks", {}).get("enwiki") or {}).get("title") or sp[n]["sci"]
    fem = []
    if title:
        imgs = api("en.wikipedia.org", action="query", titles=title, redirects=1, prop="images", imlimit=200).get("query", {}).get("pages", [{}])[0].get("images", [])
        fem = [i["title"].split(":", 1)[1] for i in imgs if re.search(r"female|femelle|weibchen|hembra|\bhen\b|♀", i["title"], re.I)
               and not re.search(r"\.(svg|ogg|oga|wav|mp3|webm|ogv|gif|tiff?)$", i["title"], re.I) and not re.search(r"juv|fledg|immature|egg|chick|map|range|nest|feed|young|baby|\bmales?\b|pair|couple", i["title"], re.I)]
    if not p18 and title:   # no Wikidata photo: use the lead photo of the English Wikipedia article
        pg = api("en.wikipedia.org", action="query", titles=title, redirects=1, prop="pageimages", piprop="name").get("query", {}).get("pages", [{}])[0]
        if pg.get("pageimage"): p18 = [pg["pageimage"].replace("_", " ")]
    res[n] = {"sci": sp[n]["sci"], "wiki": title, "main": p18[0] if p18 else None, "female": fem[0] if fem else None, "female_all": fem}
    time.sleep(.3)

meta = info([f for r in res.values() for f in (r["main"], r["female"]) if f])
for n, r in res.items():
    for k in ("main", "female"):
        f = r[k]
        if not f or f not in meta: r[k] = None; continue
        m = meta[f]; m["file"] = f; path = f"{DIR}/{slug(n)}.{k}.jpg"
        if not os.path.exists(path) and m["url"]:
            for t in range(6):
                try: open(path, "wb").write(urllib.request.urlopen(urllib.request.Request(m["url"], headers=UA), timeout=60).read()); break
                except urllib.error.HTTPError as ex:
                    if ex.code != 429: print("download failed", n, k, ex); break
                    time.sleep(float(ex.headers.get("Retry-After") or 0) + 10 * (t + 1))
                except Exception as ex: print("download failed", n, k, ex); time.sleep(5)
            time.sleep(2)
        m["path"] = path if os.path.exists(path) else None; r[k] = m
    print(n, "| main:", r["main"] and r["main"]["file"], r["main"] and r["main"]["license"], "| female:", r["female"] and r["female"]["file"], flush=True)
json.dump(res, open(f"{DIR}/results.json", "w"), indent=1)
