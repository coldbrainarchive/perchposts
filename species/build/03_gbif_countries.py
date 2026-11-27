# sightings per country for every species (GBIF occurrence facets). Resumable: progress saved to species/raw/gbif_countries.json
import csv, json, os, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
OUT = "species/raw/gbif_countries.json"
done = json.load(open(OUT)) if os.path.exists(OUT) else {}
names = [r["SCIENTIFIC_NAME"] for r in csv.DictReader(open("species/raw/ebird_taxonomy.csv")) if r["CATEGORY"] == "species" and not r["EXTINCT"]]
todo = [n for n in names if n not in done]
print(len(names), "species,", len(todo), "to fetch", flush=True)
def fetch(name):
    p = {"scientificName": name, "limit": 0, "facet": "country", "facetLimit": 300, "occurrenceStatus": "PRESENT", "basisOfRecord": "HUMAN_OBSERVATION"}
    for tries in range(6):
        try:
            req = urllib.request.Request("https://api.gbif.org/v1/occurrence/search?" + urllib.parse.urlencode(p), headers={"User-Agent": "species-db-build/1.0"})
            j = json.load(urllib.request.urlopen(req, timeout=90))
            f = (j.get("facets") or [{}])[0].get("counts", []) if j.get("facets") else []
            time.sleep(0.3)   # be gentle: GBIF refused connections at 14 parallel requests
            return name, {"n": j.get("count", 0), "c": {x["name"]: x["count"] for x in f}}
        except Exception as e:
            time.sleep(4 * (tries + 1))
    return name, None
n = 0
with ThreadPoolExecutor(4) as ex:
    for fut in as_completed([ex.submit(fetch, t) for t in todo]):
        name, res = fut.result()
        if res is not None: done[name] = res
        n += 1
        if n % 100 == 0:
            json.dump(done, open(OUT, "w")); print(n, "/", len(todo), flush=True)
json.dump(done, open(OUT, "w")); print("done", len(done), flush=True)
