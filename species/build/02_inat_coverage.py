# which bird species have research-grade iNaturalist photos we may reuse (CC0 / CC BY / CC BY-SA), by life stage and sex
import json, time, urllib.request, urllib.parse
BASE = "https://api.inaturalist.org/v1/observations/species_counts"
SETS = {"any": {}, "adult": {"term_id": 1, "term_value_id": 2}, "juv": {"term_id": 1, "term_value_id": 8},
        "female": {"term_id": 9, "term_value_id": 10}, "male": {"term_id": 9, "term_value_id": 11}}
def get(params):
    for tries in range(5):
        try:
            req = urllib.request.Request(BASE + "?" + urllib.parse.urlencode(params), headers={"User-Agent": "species-db-build/1.0"})
            return json.load(urllib.request.urlopen(req, timeout=120))
        except Exception as e:
            time.sleep(5 * (tries + 1))
    raise SystemExit("failed " + str(params))
out = {}
for key, extra in SETS.items():
    page = 1
    while True:
        p = {"taxon_id": 3, "quality_grade": "research", "photos": "true", "photo_license": "cc0,cc-by,cc-by-sa", "per_page": 500, "page": page, **extra}
        j = get(p); res = j["results"]
        for r in res:
            t = r["taxon"]
            if t.get("rank") != "species": continue
            o = out.setdefault(t["name"], {"inat": t["id"], "common": t.get("preferred_common_name")})
            o[key] = r["count"]
        print(key, "page", page, len(res), "of", j["total_results"], flush=True)
        if page * 500 >= j["total_results"] or not res: break
        page += 1; time.sleep(1.1)
    time.sleep(1.1)
json.dump(out, open("species/raw/inat_coverage.json", "w"))
print(len(out), "species")
