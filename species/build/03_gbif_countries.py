# sightings per country for every species (GBIF occurrence facets). Resumable: progress saved to species/raw/gbif_countries.json
import csv, json, os, time, urllib.request, urllib.parse, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
OUT = "species/raw/gbif_countries.json"
done = json.load(open(OUT)) if os.path.exists(OUT) else {}
names = [r["SCIENTIFIC_NAME"] for r in csv.DictReader(open("species/raw/ebird_taxonomy.csv")) if r["CATEGORY"] == "species" and not r["EXTINCT"]]
todo = [n for n in names if n not in done]
print(len(names), "species,", len(todo), "to fetch", flush=True)
def fetch(name):
    p = {"scientificName": name, "limit": 0, "facet": "country", "facetLimit": 300, "occurrenceStatus": "PRESENT", "basisOfRecord": "HUMAN_OBSERVATION"}
    tries = 0
    while tries < 6:
        try:
            req = urllib.request.Request("https://api.gbif.org/v1/occurrence/search?" + urllib.parse.urlencode(p), headers={"User-Agent": "species-db-build/1.0"})
            j = json.load(urllib.request.urlopen(req, timeout=90))
            f = (j.get("facets") or [{}])[0].get("counts", []) if j.get("facets") else []
            time.sleep(0.3)   # be gentle: GBIF refused connections at 14 parallel requests
            return name, {"n": j.get("count", 0), "c": {x["name"]: x["count"] for x in f}}
        except urllib.error.HTTPError as e:
            if e.code == 429:   # GBIF says how long to wait; do exactly that (doesn't count as a failed try)
                time.sleep(float(e.headers.get("Retry-After") or 3) + .5); continue
            tries += 1; time.sleep(4 * tries)
        except Exception as e:
            tries += 1; time.sleep(4 * tries)
    return name, None
n = 0
with ThreadPoolExecutor(2) as ex:
    for fut in as_completed([ex.submit(fetch, t) for t in todo]):
        name, res = fut.result()
        if res is not None: done[name] = res
        n += 1
        if n % 100 == 0:
            json.dump(done, open(OUT, "w")); print(n, "/", len(todo), flush=True)
json.dump(done, open(OUT, "w")); print("done", len(done), flush=True)
