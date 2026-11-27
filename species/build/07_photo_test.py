# Photo pipeline test on 30 species: download candidates, cut the bird out (Apple Vision, species/bin/birdmask),
# score each photo, pick the best adult / juvenile / female, crop the head, sample colours.
# Writes species/raw/photos_test/results.json (+ the downloaded photos and masks in the same folder).
import json, os, re, subprocess, urllib.request
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image, ImageFilter

TEST = ["Mallard", "Canada Goose", "Bald Eagle", "American Flamingo", "King Penguin", "Common Ostrich", "House Sparrow",
        "Anna's Hummingbird", "Great Blue Heron", "Great Horned Owl", "Northern Cardinal", "Rainbow Lorikeet",
        "Belted Kingfisher", "Ring-necked Pheasant", "Peregrine Falcon", "Common Loon", "Double-crested Cormorant",
        "Pied-billed Grebe", "Mourning Dove", "Downy Woodpecker", "Killdeer", "Laughing Kookaburra", "Common Hoopoe",
        "Emu", "Turkey Vulture", "Tawny Frogmouth", "White Stork", "Black-headed Gull", "Common Swift", "Hoatzin"]
DIR = "species/raw/photos_test"; os.makedirs(DIR, exist_ok=True)
sp = {s["name"]: s for s in json.load(open("species/out/species.json"))}
pc = json.load(open("species/raw/photo_candidates.json"))
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# candidates: top 12 general (by faves, one photo per observation first, then extras) + top 4 juvenile-tagged
jobs, picks = [], {}
for name in TEST:
    s = sp[name]; rec = pc.get(s["sci"])
    if not rec: print("not fetched yet:", name); continue
    seen, gen = set(), []
    for c in sorted(rec["all"], key=lambda c: -c["faves"]):
        if c["photo"] in seen: continue
        seen.add(c["photo"]); gen.append(c)
    first = {}; [first.setdefault(c["obs"], c) for c in gen]
    gen = (list(first.values()) + [c for c in gen if first[c["obs"]] is not c])[:12]
    juv = [dict(c, stage="juvenile") for c in rec.get("juvenile", []) if c["photo"] not in seen][:4]
    picks[name] = gen + juv
    os.makedirs(f"{DIR}/{slug(name)}", exist_ok=True)
    for c in picks[name]: jobs.append((c["url"], f"{DIR}/{slug(name)}/{c['photo']}.jpg"))

def dl(job):
    url, path = job
    if os.path.exists(path): return
    try:
        data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "species-db-build/1.0"}), timeout=60).read()
        open(path, "wb").write(data)
    except Exception as e: print("download failed", url, e)
with ThreadPoolExecutor(4) as ex: list(ex.map(dl, jobs))
print("downloaded", sum(os.path.exists(p) for _, p in jobs), "/", len(jobs), flush=True)

# masks: one call per species folder
vis = {}
for name in picks:
    d = f"{DIR}/{slug(name)}"; files = [f"{d}/{c['photo']}.jpg" for c in picks[name] if os.path.exists(f"{d}/{c['photo']}.jpg")]
    out = subprocess.run(["species/bin/birdmask", d, *files], capture_output=True, text=True).stdout
    for line in out.splitlines():
        try: j = json.loads(line); vis[(name, j["file"])] = j
        except Exception: pass

def lap_var(gray, m):
    g = gray.astype(np.float32)
    l = -4 * g[1:-1, 1:-1] + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:]
    mm = m[1:-1, 1:-1]
    return float(l[mm].var()) if mm.sum() > 50 else 0.0

def kmeans(px, k=6, it=12):
    rng = np.random.default_rng(1); c = px[rng.choice(len(px), k, replace=False)].astype(np.float32)
    for _ in range(it):
        lab = ((px[:, None, :] - c[None]) ** 2).sum(-1).argmin(1)
        for i in range(k):
            if (lab == i).any(): c[i] = px[lab == i].mean(0)
    share = np.bincount(lab, minlength=k) / len(px)
    return [("#%02x%02x%02x" % tuple(int(v) for v in c[i]), round(float(share[i]), 3)) for i in np.argsort(-share) if share[i] > .02]

def judge(name, c):
    pid = str(c["photo"]); d = f"{DIR}/{slug(name)}"; v = vis.get((name, pid))
    r = {"photo": c["photo"], "faves": c["faves"], "stage": c.get("stage"), "sex": c.get("sex"), "credit": c["credit"],
         "license": c["license"], "obs": c["obs"], "problems": []}
    if not v or not v.get("subjects") or not os.path.exists(f"{d}/{pid}.mask.png"):
        r["problems"].append("no bird found"); r["score"] = -9; return r
    img = Image.open(f"{d}/{pid}.jpg").convert("RGB"); W, H = img.size
    m = np.asarray(Image.open(f"{d}/{pid}.mask.png").convert("L").resize((W, H))) > 127
    if m.sum() < 100: r["problems"].append("no bird found"); r["score"] = -9; return r
    area = m.mean(); ys, xs = np.nonzero(m); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    bw, bh = x1 - x0 + 1, y1 - y0 + 1
    edges = {"left": m[:, :3].any(1).mean(), "right": m[:, -3:].any(1).mean(), "top": m[:3].any(0).mean(), "bottom": m[-3:].any(0).mean()}
    cut = [k for k, f in edges.items() if f > .12]
    areas = [float(a) for a in v["areas"]]; others = [a for a in areas[1:] if a > areas[0] * .3]
    # sharpness: measured on the bird alone, scaled to 400px across so big and small photos compare fairly
    sc = 400 / max(bw, bh); crop = img.crop((x0, y0, x1 + 1, y1 + 1)).resize((max(8, int(bw * sc)), max(8, int(bh * sc))))
    cm = np.asarray(Image.fromarray(m[y0:y1 + 1, x0:x1 + 1].astype(np.uint8) * 255).resize(crop.size).filter(ImageFilter.MinFilter(5))) > 127
    sharp = lap_var(np.asarray(crop.convert("L")), cm)
    r.update(area=round(float(area), 3), sharp=round(sharp, 1), box=[int(x0), int(y0), int(bw), int(bh)], size=[W, H], subjects=len(areas))
    if area < .03: r["problems"].append("bird too small / far away")
    if area > .7: r["problems"].append("too close, bird fills the frame")
    if cut: r["problems"].append("cut off at the " + " & ".join(cut))
    if others: r["problems"].append(f"{len(others) + 1} subjects in the photo")
    if bw / bh > 2.3: r["problems"].append("wide shape, likely wings spread / flying")
    if sharp < 60: r["problems"].append("blurry")
    # score: sharpness (log), size near 25% of the frame, faves as a light tiebreak, minus problems
    s = np.log1p(sharp) - 3 * abs(np.log(max(area, .005) / .25)) * .35 + .12 * np.log1p(c["faves"])
    s -= 1.5 * len(cut) + 1.2 * bool(others) + .8 * (bw / bh > 2.3) + 1.5 * (area < .03) + 1.0 * (area > .7)
    r["score"] = round(float(s), 2)
    return r

def head_crop(name, r):
    # head = the top of the bird: mask pixels in the top 30% of the bird's height, centred on them, square
    d = f"{DIR}/{slug(name)}"; pid = str(r["photo"])
    img = Image.open(f"{d}/{pid}.jpg").convert("RGB"); W, H = img.size
    m = np.asarray(Image.open(f"{d}/{pid}.mask.png").convert("L").resize((W, H))) > 127
    x0, y0, bw, bh = r["box"]; band = m[y0:y0 + max(2, int(bh * .3))]
    ys, xs = np.nonzero(band); cx, cy = xs.mean(), y0 + ys.mean()
    side = max(24, int(min(bw, bh) * .55)); L, T = int(cx - side / 2), int(cy - side / 2)
    return [max(0, L), max(0, T), side]

def palette(name, r):
    d = f"{DIR}/{slug(name)}"; pid = str(r["photo"])
    img = Image.open(f"{d}/{pid}.jpg").convert("RGB"); img.thumbnail((300, 300))
    m = np.asarray(Image.open(f"{d}/{pid}.mask.png").convert("L").resize(img.size).filter(ImageFilter.MinFilter(3))) > 127
    px = np.asarray(img)[m].reshape(-1, 3)
    return kmeans(px[:: max(1, len(px) // 4000)]) if len(px) > 50 else []

results = {}
for name in picks:
    rs = sorted((judge(name, c) for c in picks[name]), key=lambda r: -r["score"])
    ok = lambda r: r["score"] > -9 and not r["problems"]
    best = lambda pred: next((r for r in rs if pred(r) and ok(r)), None) or next((r for r in rs if pred(r) and r["score"] > -9), None)
    out = {"sci": sp[name]["sci"], "order": sp[name]["order"], "candidates": rs,
           "main": best(lambda r: r["stage"] not in ("juvenile", "egg") and r["sex"] != "female"),
           "juvenile": best(lambda r: r["stage"] == "juvenile"),
           "female": best(lambda r: r["sex"] == "female" and r["stage"] != "juvenile")}
    if out["main"]:
        out["head"] = head_crop(name, out["main"]); out["palette"] = palette(name, out["main"])
    results[name] = out
    print(name, "main", out["main"] and out["main"]["photo"], "juv", out["juvenile"] and out["juvenile"]["photo"],
          "fem", out["female"] and out["female"]["photo"], flush=True)
json.dump(results, open(f"{DIR}/results.json", "w"))
