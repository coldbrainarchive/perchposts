# Photo pipeline, step 1: candidate photos for every species (links only, nothing downloaded yet).
# Source: iNaturalist research-grade observations whose photo licence lets us reuse it (CC0 / CC BY / CC BY-SA).
# For each species: the most-faved observations (any age), plus juvenile-tagged ones and female-tagged ones where they exist.
# Each candidate keeps: photo link, licence, the photographer's credit line, observation id, and its life-stage / sex tags.
# Resumable (progress in species/raw/photo_candidates.json). Gentle: one request at a time, about 1 a second.
import json, os, time, threading, urllib.request, urllib.parse, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT = "species/raw/photo_candidates.json"
done = json.load(open(OUT)) if os.path.exists(OUT) else {}
cov = json.load(open("species/raw/inat_coverage.json"))
OK_LIC = {"cc0", "cc-by", "cc-by-sa"}
STAGE = {2: "adult", 8: "juvenile", 7: "egg"}; SEX = {10: "female", 11: "male"}

# one request per second in total across all threads (iNaturalist's guideline), 3 in flight because each takes ~1.7 s
_lock, _next = threading.Lock(), [0.0]
def _slot():
    with _lock:
        now = time.time(); wait = max(0, _next[0] - now); _next[0] = max(now, _next[0]) + 1.0
    if wait: time.sleep(wait)
def _pause(secs):
    # everyone waits: pushes the shared clock forward so no thread sends anything until the pause is over
    with _lock: _next[0] = max(_next[0], time.time() + secs)
def get(params):
    url = "https://api.inaturalist.org/v1/observations?" + urllib.parse.urlencode(params)
    tries = 0
    while True:
        _slot()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "species-db-build/1.0"}), timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                # over the limit (likely the daily one): pause everything 5 minutes, then try again; never give up,
                # so a refusal is never saved as "no photos"
                print("429, pausing 5 min", time.strftime("%H:%M"), flush=True); _pause(300); continue
            tries += 1
        except Exception: tries += 1
        if tries >= 6: raise RuntimeError("failed: " + url)
        time.sleep(4 * tries)

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
# females: the general results include tagged females; a targeted pass for species that look different comes later
def one(sci):
    c = cov[sci]; t = c["inat"]; rec = {"inat": t, "all": pull(t, {}, 30)}
    if c.get("juv", 0) >= 2: rec["juvenile"] = pull(t, {"term_id": 1, "term_value_id": 8}, 20)
    return sci, rec
n = 0
with ThreadPoolExecutor(3) as ex:
    for fut in as_completed([ex.submit(one, s_) for s_ in todo]):
        try: sci, rec = fut.result()
        except Exception as e: print("skipped (will retry next run):", e, flush=True); continue
        done[sci] = rec; n += 1
        if n % 100 == 0: json.dump(done, open(OUT, "w")); print(n, "/", len(todo), time.strftime("%H:%M"), flush=True)
json.dump(done, open(OUT, "w")); print("done", len(done), flush=True)
