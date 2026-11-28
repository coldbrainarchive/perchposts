# Passport photos for every species: one hero shot of the adult (main, usually the male) and one of the female where
# Wikipedia has one, plus the bird's colours sampled from each photo.
#   main   = the species' Wikidata image (P18) or the article's lead image; if it shows a female, it becomes the female
#            photo and the next photo captioned male/adult becomes the main one
#   female = an article photo whose caption or file name says female (not juvenile / nest / pair)
#   check  = Apple Vision (species/bin/birdmask) counts the subjects; a photo with two big birds is swapped for the next one
#   colours= k-means on the cut-out bird only (main + female)
# One ~960px copy of each chosen photo is kept in species/raw/hero/, with author + licence for the credit line.
# Resumable: progress in species/raw/hero/results.json. Run from the repo root.
import json, os, re, sys, time, subprocess, urllib.request, urllib.parse, urllib.error
import numpy as np
from PIL import Image, ImageFilter

UA = {"User-Agent": "species-db-build/1.0 (bird species database; one request at a time)"}
DIR = "species/raw/hero"; os.makedirs(DIR, exist_ok=True); OUT = f"{DIR}/results.json"
done = json.load(open(OUT)) if os.path.exists(OUT) else {}
SP = json.load(open("species/out/species.json"))
SP.sort(key=lambda s: -(s.get("sightings") or 0))          # common birds first, so the useful part lands early
todo = [s for s in SP if s["sci"] not in done]
if len(sys.argv) > 1: todo = todo[:int(sys.argv[1])]
print(len(SP), "species,", len(todo), "to do", flush=True)
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def fetch(url, binary=False):
    tries, wait = 0, 2
    while True:
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read() if binary else json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (400, 403, 404, 410): return None
            if e.code == 429:
                # too fast: wait at least as long as asked, doubling up to 5 minutes, and never give up (so a refusal
                # is never saved as "no photo")
                print("429", url.split("/")[2], time.strftime("%H:%M:%S"), "waiting", wait, flush=True)
                time.sleep(max(wait, float(e.headers.get("Retry-After") or 1))); wait = min(wait * 2, 300); continue
            tries += 1
        except Exception: tries += 1
        if tries >= 5: return None
        time.sleep(4 * tries)

def api(host, **p):
    return fetch(f"https://{host}/w/api.php?" + urllib.parse.urlencode({"format": "json", "formatversion": 2, "maxlag": 5, **p})) or {}

BAD = re.compile(r"juv|fledg|immature|chick|nestling|hatchl|egg|nest|map|range|distribution|skelet|skull|specimen|museum|stamp|"
                 r"illustrat|drawing|painting|plate|feeding|young|baby|pair|couple|mating|\bmale and female\b|\bmales? & females?\b|"
                 r"\.(svg|ogg|oga|wav|mp3|webm|ogv|gif|tiff?|pdf)$", re.I)
FEM = re.compile(r"\bfemales?\b|femelle|weibchen|hembra|♀|\bhen\b", re.I)
MALE = re.compile(r"(?<!fe)\bmales?\b|♂|\bcock\b|\bdrake\b", re.I)

# Wikidata: image + English article for every species still to do, from the query service, 2,000 birds per query
ents = {}
qids = [s["wikidata"] for s in todo if s.get("wikidata")]
for i in range(0, len(qids), 2000):
    q = ("SELECT ?item ?img ?article WHERE { VALUES ?item { " + " ".join("wd:" + x for x in qids[i:i + 2000]) + " } "
         "OPTIONAL { ?item wdt:P18 ?img } OPTIONAL { ?article schema:about ?item ; schema:isPartOf <https://en.wikipedia.org/> } }")
    body = urllib.parse.urlencode({"query": q, "format": "json"}).encode()
    for t in range(6):
        try:
            j = json.load(urllib.request.urlopen(urllib.request.Request("https://query.wikidata.org/sparql", data=body, headers={**UA, "Accept": "application/sparql-results+json"}), timeout=120)); break
        except Exception as ex: print("wikidata query retry", ex, flush=True); time.sleep(10 * (t + 1)); j = {}
    for b in j.get("results", {}).get("bindings", []):
        e = ents.setdefault(b["item"]["value"].rsplit("/", 1)[1], {"p18": [], "title": None})
        if "img" in b:
            f = urllib.parse.unquote(b["img"]["value"].rsplit("/", 1)[1]).replace("_", " ")
            if f not in e["p18"]: e["p18"].append(f)
        if "article" in b: e["title"] = urllib.parse.unquote(b["article"]["value"].rsplit("/", 1)[1]).replace("_", " ")
    time.sleep(2)
print("wikidata", len(ents), flush=True)

def media(title):
    j = fetch("https://en.wikipedia.org/api/rest_v1/page/media-list/" + urllib.parse.quote(title.replace(" ", "_"), safe="") + "?redirect=true")
    out = []
    for it in (j or {}).get("items", []):
        if it.get("type") != "image" or not it.get("title", "").startswith("File:"): continue
        out.append({"file": it["title"][5:].replace("_", " "), "cap": ((it.get("caption") or {}).get("text") or "")[:300], "lead": bool(it.get("leadImage"))})
    return out

def info(files):
    # licence + author for up to 50 files per request; the resized copy's link is built from the file's own address
    # (Wikimedia's standard thumb path), so Commons doesn't have to render anything for us (that part is rate-limited)
    out = {}
    for i in range(0, len(files), 50):
        r = api("commons.wikimedia.org", action="query", titles="|".join("File:" + f for f in files[i:i + 50]), prop="imageinfo", iiprop="url|extmetadata|size")
        norm = {x["to"]: x["from"] for x in r.get("query", {}).get("normalized", [])}
        for pg in r.get("query", {}).get("pages", []):
            ii = (pg.get("imageinfo") or [{}])[0]; md = ii.get("extmetadata", {}); u = (ii.get("url") or "").split("?")[0]
            g = lambda k: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", (md.get(k) or {}).get("value", ""))).strip()
            if (ii.get("width") or 0) > 960 and "/wikipedia/commons/" in u:
                a, b = u.split("/wikipedia/commons/", 1); fn = b.rsplit("/", 1)[1]
                u = f"{a}/wikipedia/commons/thumb/{b}/960px-{fn}" + (".jpg" if fn.lower().endswith((".tif", ".tiff")) else "")
            t = norm.get(pg["title"], pg["title"])[5:]
            out[t] = {"url": u, "page": ii.get("descriptionurl"), "license": g("LicenseShortName"),
                      "license_url": g("LicenseUrl"), "author": g("Artist")[:200], "w": ii.get("width"), "h": ii.get("height")}
        time.sleep(.3)
    return out

FREE = re.compile(r"^(cc0|public domain|pd|cc by(-sa)? [0-9.]+|cc by(-sa)?|attribution|no restrictions)", re.I)
def check(path):
    # Vision: biggest subject's share of the photo, and whether a second subject is nearly as big
    o = subprocess.run(["species/bin/birdmask", DIR, path], capture_output=True, text=True).stdout.strip()
    try: j = json.loads(o.splitlines()[-1])
    except Exception: return None
    a = [float(x) for x in j.get("areas", [])]
    return {"area": a[0] if a else 0, "others": sum(1 for x in a[1:] if a and x > a[0] * .35)}

def kmeans(px, k=6, it=12):
    rng = np.random.default_rng(1); c = px[rng.choice(len(px), k, replace=False)].astype(np.float32)
    for _ in range(it):
        lab = ((px[:, None, :] - c[None]) ** 2).sum(-1).argmin(1)
        for i in range(k):
            if (lab == i).any(): c[i] = px[lab == i].mean(0)
    share = np.bincount(lab, minlength=k) / len(px)
    return [["#%02x%02x%02x" % tuple(int(v) for v in c[i]), round(float(share[i]), 3)] for i in np.argsort(-share) if share[i] > .02]
def colours(path):
    mp = path[:-4] + ".mask.png"
    if not os.path.exists(mp): return []
    img = Image.open(path).convert("RGB"); img.thumbnail((320, 320))
    m = np.asarray(Image.open(mp).convert("L").resize(img.size).filter(ImageFilter.MinFilter(3))) > 127
    px = np.asarray(img)[m].reshape(-1, 3)
    return kmeans(px[:: max(1, len(px) // 4000)]) if len(px) > 60 else []

def take(name, kind, cands, meta):
    # try up to 3 candidates; first one with a single clear bird wins, otherwise the first one that downloaded
    first = None
    for f in cands[:3]:
        m = meta.get(f)
        if not m or not m["url"] or not FREE.match(m["license"] or ""): continue
        path = f"{DIR}/{slug(name)}.{kind}.jpg"
        data = fetch(m["url"], binary=True); time.sleep(3.0)   # one photo every ~3 s
        if not data: continue
        open(path, "wb").write(data)
        c = check(path); lbl = path[:-4] + ".labels.png"
        if os.path.exists(lbl): os.remove(lbl)
        rec = dict(m, file=f, area=c and round(c["area"], 3), others=c and c["others"])
        if c and c["area"] >= .015 and not c["others"]: return rec
        if first is None: first = (rec, data)
    if first:
        rec, data = first; open(f"{DIR}/{slug(name)}.{kind}.jpg", "wb").write(data); check(f"{DIR}/{slug(name)}.{kind}.jpg")
        lbl = f"{DIR}/{slug(name)}.{kind}.labels.png"
        if os.path.exists(lbl): os.remove(lbl)
        rec["flag"] = "several birds or no clear bird"; return rec
    return None

n = 0
def plan(s):
    name, sci = s["name"], s["sci"]
    e = ents.get(s.get("wikidata") or "", {})
    p18 = e.get("p18", [])
    title = e.get("title") or sci
    items = media(title); time.sleep(.15)
    ok = [i for i in items if not BAD.search(i["file"] + " " + i["cap"])]
    caps = {i["file"]: i["cap"] for i in items}
    is_f = lambda f: bool(FEM.search(f + " " + caps.get(f, ""))) and not MALE.search(f + " " + caps.get(f, ""))
    lead = [i["file"] for i in ok if i["lead"]]
    main_c, fem_c = [], [i["file"] for i in ok if is_f(i["file"])]
    for f in p18 + lead + [i["file"] for i in ok if MALE.search(i["file"] + " " + i["cap"]) or re.search(r"adult|breeding", i["cap"], re.I)] + [i["file"] for i in ok]:
        if BAD.search(f) or f in main_c: continue
        if is_f(f):
            if f not in fem_c: fem_c.insert(0, f)
            continue
        main_c.append(f)
    # the Wikipedia link saved with the bird (only when there is an article), so it can be looked up from the profile
    rec = {"name": name, "inat": s.get("inat"), "wiki": title if items else None,
           "wiki_url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")) if items else None}
    return s, rec, main_c, fem_c

for b in range(0, len(todo), 40):
    batch = [plan(s) for s in todo[b:b + 40]]
    meta = info(list(dict.fromkeys(f for _, _, m, fc in batch for f in m[:3] + fc[:3])))
    for s, rec, main_c, fem_c in batch:
        name = s["name"]
        rec["main"] = take(name, "main", main_c, meta) if main_c else None
        rec["female"] = take(name, "female", fem_c, meta) if fem_c else None
        for k in ("main", "female"):
            if rec[k]: rec[k]["colours"] = colours(f"{DIR}/{slug(name)}.{k}.jpg")
        done[s["sci"]] = rec; n += 1
    json.dump(done, open(OUT, "w"))
    got = sum(1 for r in done.values() if r["main"]); fem = sum(1 for r in done.values() if r["female"])
    print(n, "/", len(todo), time.strftime("%H:%M"), "| main", got, "female", fem, flush=True)
json.dump(done, open(OUT, "w")); print("done", len(done), flush=True)
