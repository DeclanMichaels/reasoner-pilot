import json, glob, statistics, collections
from pathlib import Path
V = Path(__file__).resolve().parent
instr = json.load(open(V / "instruments/mfq2.filled.json"))
grp = {it["id"]: it["group"] for it in instr["items"]}
FOUND = ["care","equality","proportionality","loyalty","authority","purity"]
BIND = ["loyalty","authority","purity"]

def fmeans(ratings):
    acc = collections.defaultdict(list)
    for iid, v in ratings.items():
        acc[grp[iid]].append(v)
    return {f: statistics.mean(acc[f]) for f in FOUND if acc[f]}

def load(dirpath):
    rows = collections.defaultdict(lambda: collections.defaultdict(list))
    for f in glob.glob(str(dirpath / "*_mfq2_*.json")):
        d = json.load(open(f))
        if not d.get("ratings"): continue
        fm = fmeans(d["ratings"])
        key = (d["model"], d.get("country", "NEUTRAL"))
        for fnd, v in fm.items():
            rows[key][fnd].append(v)
    return {k: {fnd: statistics.mean(vs) for fnd, vs in fd.items()} for k, fd in rows.items()}

neutral = load(V / "runs")
framed = load(V / "runs_framed")
countries = sorted({c for (m, c) in framed})
models = sorted({m for (m, c) in framed})
binding = lambda p: statistics.mean([p[f] for f in BIND])

print(f"models={len(models)} countries={countries}")
nb = [binding(neutral[(m,"NEUTRAL")]) for m in models if (m,"NEUTRAL") in neutral]
print(f"\nNEUTRAL binding: mean={statistics.mean(nb):.2f}  between-model sd={statistics.pstdev(nb):.2f}")
print("\n=== per-country panel means (6 foundations) + binding composite ===")
hdr = "country".ljust(15) + "".join(f.ljust(7)[:7] for f in FOUND) + "  BIND"
print(hdr)
for c in countries:
    prof = {f: statistics.mean([framed[(m,c)][f] for m in models if (m,c) in framed and f in framed[(m,c)]]) for f in FOUND}
    print(c.ljust(15) + "".join(f"{prof[f]:.2f}".ljust(7) for f in FOUND) + f"  {binding(prof):.2f}")
print("\n=== de-compression: within-model spread of binding across countries ===")
wm = []
for m in models:
    vals = [binding(framed[(m,c)]) for c in countries if (m,c) in framed]
    if len(vals) >= 2:
        wm.append(statistics.pstdev(vals))
        print(f"  {m:14s} {min(vals):.2f}..{max(vals):.2f}  (sd {statistics.pstdev(vals):.2f})")
if wm:
    print(f"mean within-model across-country binding SD = {statistics.mean(wm):.2f}")
    print(f"(neutral between-model binding SD was {statistics.pstdev(nb):.2f} — compression baseline)")
print("\n=== between-model agreement per country (stereotype: low sd = shared caricature) ===")
for c in countries:
    vals = [binding(framed[(m,c)]) for m in models if (m,c) in framed]
    print(f"  {c:15s} binding {statistics.mean(vals):.2f} between-model sd {statistics.pstdev(vals):.2f}")
