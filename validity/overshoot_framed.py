import json, glob, statistics, collections
from pathlib import Path
V = Path(__file__).resolve().parent
instr = json.load(open(V / "instruments/mfq2.filled.json"))
grp = {it["id"]: it["group"] for it in instr["items"]}
FOUND = ["care","equality","proportionality","loyalty","authority","purity"]
BIND = ["loyalty","authority","purity"]

# Real human MFQ-2 means (M, SD) — Atari, Haidt & Graham (2023) "Morality Beyond the WEIRD", Table 7.
REAL = {
 "Egypt":  {"care":(4.38,0.60),"equality":(3.56,0.94),"proportionality":(4.37,0.58),"loyalty":(4.42,0.62),"authority":(4.18,0.68),"purity":(4.19,0.63)},
 "Japan":  {"care":(3.03,0.77),"equality":(2.27,0.78),"proportionality":(3.14,0.73),"loyalty":(2.66,0.82),"authority":(2.67,0.66),"purity":(2.63,0.69)},
 "Nigeria":{"care":(4.32,0.64),"equality":(2.90,1.03),"proportionality":(4.14,0.67),"loyalty":(4.11,0.74),"authority":(4.21,0.61),"purity":(3.80,0.77)},
}

def fmeans(r):
    acc=collections.defaultdict(list)
    for iid,v in r.items(): acc[grp[iid]].append(v)
    return {f:statistics.mean(acc[f]) for f in FOUND if acc[f]}

rows=collections.defaultdict(lambda: collections.defaultdict(list))
for f in glob.glob(str(V/"runs_framed/*_mfq2_*.json")):
    d=json.load(open(f))
    if not d.get("ratings"): continue
    if d.get("country") not in REAL: continue
    for fnd,v in fmeans(d["ratings"]).items():
        rows[d["country"]][fnd].append((d["model"], v))

for c in ["Japan","Nigeria","Egypt"]:
    print(f"\n=== {c}  (model panel mean vs real human M[SD]; z = (model-real)/SD) ===")
    print(f"  {'foundation':16s} {'model':>6} {'real':>6} {'SD':>5} {'resid':>7} {'z':>6}")
    zs=[]
    for f in FOUND:
        mv=[v for _,v in rows[c][f]]
        model=statistics.mean(mv)
        real,sd=REAL[c][f]
        resid=model-real; z=resid/sd
        zs.append((f,z))
        print(f"  {f:16s} {model:6.2f} {real:6.2f} {sd:5.2f} {resid:+7.2f} {z:+6.2f}")
    mb=statistics.mean([statistics.mean([v for _,v in rows[c][f]]) for f in BIND])
    rb=statistics.mean([REAL[c][f][0] for f in BIND])
    print(f"  BINDING composite: model {mb:.2f}  real {rb:.2f}  overshoot {mb-rb:+.2f}")
