# conservation status (IUCN) + Wikidata id for every bird with an eBird species code (Wikidata is CC0)
import json, urllib.request, urllib.parse, sys
Q = """SELECT ?code ?item ?status WHERE { ?item wdt:P3444 ?code . OPTIONAL { ?item wdt:P141 ?status } }"""
url = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": Q, "format": "json"})
req = urllib.request.Request(url, headers={"User-Agent": "species-db-build/1.0 (bird species reference build)", "Accept": "application/sparql-results+json"})
rows = json.load(urllib.request.urlopen(req, timeout=300))["results"]["bindings"]
IUCN = {"Q211005": "LC", "Q719675": "NT", "Q278113": "VU", "Q11394": "EN", "Q219127": "CR", "Q239509": "EW", "Q237350": "EX", "Q3245245": "DD"}
out = {}
for r in rows:
    code = r["code"]["value"]; st = r.get("status", {}).get("value", "").rsplit("/", 1)[-1]
    o = out.setdefault(code, {"wd": r["item"]["value"].rsplit("/", 1)[-1], "iucn": None})
    if IUCN.get(st): o["iucn"] = IUCN[st]
json.dump(out, open("species/raw/wikidata.json", "w"))
print(len(out), "codes;", sum(1 for v in out.values() if v["iucn"]), "with IUCN status")
