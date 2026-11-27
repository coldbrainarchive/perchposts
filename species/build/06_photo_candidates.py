# Photo pipeline, step 1: candidate photos for every species (links only, nothing downloaded yet).
# Source: iNaturalist research-grade observations whose photo licence lets us reuse it (CC0 / CC BY / CC BY-SA).
# For each species: the most-faved observations (any age), plus juvenile-tagged ones and female-tagged ones where they exist.
# Each candidate keeps: photo link, licence, the photographer's credit line, observation id, and its life-stage / sex tags.
# Resumable (progress in species/raw/photo_candidates.json). Gentle: one request at a time, about 1 a second.
import json, os, time, urllib.request, urllib.parse, urllib.error

OUT = "species/raw/photo_candidates.json"
done = json.load(open(OUT)) if os.path.exists(OUT) else {}
cov = json.load(open("species/raw/inat_coverage.json"))
OK_LIC = {"cc0", "cc-by", "cc-by-sa"}
STAGE = {2: "adult", 8: "juvenile", 7: "egg"}; SEX = {10: "female", 11: "male"}

def get(params):
    url = "https://api.inaturalist.org/v1/observations?" + urllib.parse.urlencode(params)
    for tries in range(6):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "species-db-build/1.0"}), timeout=90))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(float(e.headers.get("Retry-After") or 10) + 1); continue
            time.sleep(4 * (tries + 1))
        except Exception: time.sleep(4 * (tries + 1))
    return None

def pull(taxon, extra, n):
    j = get({"taxon_id": taxon, "quality_grade": "research", "photos": "true", "photo_license": "cc0,cc-by,cc-by-sa",
             "order_by": "votes", "per_page": n, **extra})
    out = []
    for o in (j or {}).get("results", []):
        tags = {}
        for a in o.get("annotations") or []:
            if a.get("controlled_attribute_id") == 1 and a.get("controlled_value_id") in STAGE: tags["stage"] = STAGE[a["controlled_value_id"]]
            if a.get("controlled_attribute_id") == 9 and a.get("controlled_value_id") in SEX: tags["sex"] = SEX[a["controlled_value_id"]]
        for ph in (o.get("photos") or [])[:3]:
            if (ph.get("license_code") or "").lower() not in OK_LIC: continue
            out.append({"photo": ph["id"], "url": (ph.get("url") or "").replace("/square.", "/large."), "license": ph.get("license_code"),
                        "credit": ph.get("attribution"), "obs": o.get("id"), "faves": o.get("faves_count", 0), **tags})
    return out

names = sorted(cov, key=lambda n: -cov[n].get("any", 0))
todo = [n for n in names if n not in done and cov[n].get("any")]
print(len(cov), "species with photos,", len(todo), "to fetch", flush=True)
for i, sci in enumerate(todo):
    c = cov[sci]; t = c["inat"]; rec = {"inat": t, "all": pull(t, {}, 30)}
    time.sleep(1.1)
    if c.get("juv"): rec["juvenile"] = pull(t, {"term_id": 1, "term_value_id": 8}, 20); time.sleep(1.1)
    if c.get("female"): rec["female"] = pull(t, {"term_id": 9, "term_value_id": 10}, 15); time.sleep(1.1)
    done[sci] = rec
    if (i + 1) % 100 == 0: json.dump(done, open(OUT, "w")); print(i + 1, "/", len(todo), flush=True)
json.dump(done, open(OUT, "w")); print("done", len(done), flush=True)
