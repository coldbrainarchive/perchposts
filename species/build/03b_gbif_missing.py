# second pass for species with no country data: match the name to GBIF's own record first (catches spelling differences
# like habroptila / habroptilus), then ask for countries by that record number. Gentle: 1 request at a time, obeys Retry-After.
import json, time, urllib.request, urllib.parse, urllib.error
OUT = "species/raw/gbif_countries.json"
done = json.load(open(OUT))
recs = json.load(open("species/out/species.json"))
todo = [r["sci"] for r in recs if not r.get("countries")]
print(len(todo), "species to retry", flush=True)
def get(url):
    for tries in range(6):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "species-db-build/1.0"}), timeout=90))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(float(e.headers.get("Retry-After") or 3) + .5); continue
            time.sleep(3 * (tries + 1))
        except Exception: time.sleep(3 * (tries + 1))
    return None
fixed = 0
for i, sci in enumerate(todo):
    m = get("https://api.gbif.org/v1/species/match?" + urllib.parse.urlencode({"name": sci, "class": "Aves", "verbose": "false"}))
    key = m and (m.get("acceptedUsageKey") or m.get("usageKey"))
    if key and m.get("rank") in ("SPECIES", "SUBSPECIES"):
        j = get("https://api.gbif.org/v1/occurrence/search?" + urllib.parse.urlencode({"taxonKey": key, "limit": 0, "facet": "country", "facetLimit": 300, "occurrenceStatus": "PRESENT"}))
        if j and j.get("facets"):
            c = {x["name"]: x["count"] for x in j["facets"][0]["counts"]}
            if c: done[sci] = {"n": j.get("count", 0), "c": c, "via": key}; fixed += 1
    time.sleep(.6)
    if (i + 1) % 50 == 0: json.dump(done, open(OUT, "w")); print(i + 1, "/", len(todo), "fixed", fixed, flush=True)
json.dump(done, open(OUT, "w")); print("done, fixed", fixed, "of", len(todo), flush=True)
