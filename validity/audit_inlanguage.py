#!/usr/bin/env python3
"""Post-hoc statistical audit of the in-language MFQ-2 study. Stdlib only.

Independent unit: MODEL (11 clusters). All tests aggregate per model first.
- Bootstrap CIs (resample models, 100k, seed 20260723) on each condition's panel mean.
- Exact sign-flip permutation tests (2^11 = 2048 enumerations) on paired per-model
  differences and one-sample-vs-anchor differences.
- Leave-one-model-out sweeps on the two headline quantities.
- Holm correction across the declared (post hoc, therefore exploratory) family.

Verification pass: raw per-model descriptives printed first; panel means must
reconcile with analyze_lang.py's reported values before anything else is trusted.
    python3 validity/audit_inlanguage.py
"""
import json, glob, random, itertools
from pathlib import Path
from collections import defaultdict

VDIR = Path(__file__).resolve().parent
FOUND = ["care","equality","proportionality","loyalty","authority","purity"]
BIND = ["loyalty","authority","purity"]
ANCH = {"Egypt":4.27, "Japan":2.65, "Iran":3.33}
SEED = 20260723
B = 100_000

def fmeans(ratings):
    by = defaultdict(list)
    for iid,v in ratings.items(): by[iid.rsplit("_",1)[0]].append(v)
    return {g: sum(v)/len(v) for g,v in by.items()}

def binding(ratings):
    fm = fmeans(ratings)
    if any(g not in fm for g in FOUND): return None
    return sum(fm[g] for g in BIND)/3

def permodel(pattern, keyfn):
    acc = defaultdict(lambda: defaultdict(list))
    for f in glob.glob(pattern):
        d = json.load(open(f))
        if not d.get("ratings"): continue
        k = keyfn(d)
        if k is None: continue
        b = binding(d["ratings"])
        if b is None: continue
        acc[k][d["model"]].append(b)
    return {k: {m: sum(v)/len(v) for m,v in md.items()} for k,md in acc.items()}

# ---- load all three sources
lang = permodel(str(VDIR/"runs_framed_lang"/"*.json"),
                lambda d: (d["instrument"].split("_")[1], d["condition"]))
enfr = permodel(str(VDIR/"runs_framed"/"*_mfq2_*.json"),
                lambda d: d.get("country") if d.get("country") in ("Egypt","Japan") else None)
ennu = permodel(str(VDIR/"runs"/"*mfq2*.json"),
                lambda d: "en_neutral" if d.get("instrument")=="mfq2" else None)

CONDS = {**{f"{c[0]}_{c[1]}": v for c,v in lang.items()},
         **{f"EN_framed_{k}": v for k,v in enfr.items()},
         **({"en_neutral": ennu["en_neutral"]} if "en_neutral" in ennu else {})}

print("=== VERIFICATION: per-model binding by condition (n models, panel mean) ===")
ROSTER = sorted(set(m for v in CONDS.values() for m in v))
for k in sorted(CONDS):
    v = CONDS[k]
    mu = sum(v.values())/len(v)
    print(f"  {k:<18} n={len(v):<3} mean={mu:.3f}  models={sorted(v)==ROSTER or sorted(v)}")
EXPECT = {"ar_framed":4.61,"ar_neutral":3.03,"ja_framed":3.46,"ja_neutral":2.66,
          "fa_framed":4.36,"fa_neutral":2.72,"EN_framed_Egypt":4.61,"EN_framed_Japan":3.67}
print("  reconcile vs analyze_lang.py:")
ok = True
for k,e in EXPECT.items():
    got = sum(CONDS[k].values())/len(CONDS[k])
    match = abs(got-e) < 0.006
    ok &= match
    print(f"    {k:<18} expected {e:.2f} got {got:.3f} {'OK' if match else 'MISMATCH'}")
print("  RECONCILED" if ok else "  *** RECONCILIATION FAILED — STOP ***")

rng = random.Random(SEED)
def boot_ci(vals):
    n = len(vals); stats = []
    for _ in range(B):
        s = [vals[rng.randrange(n)] for _ in range(n)]
        stats.append(sum(s)/n)
    stats.sort()
    return stats[int(0.025*B)], stats[int(0.975*B)]

def signflip_exact(diffs):
    """Exact sign-flip permutation p (two-sided) for mean(diffs) != 0."""
    n = len(diffs); obs = abs(sum(diffs)/n); cnt = 0; tot = 2**n
    for signs in itertools.product((1,-1), repeat=n):
        s = sum(d*sg for d,sg in zip(diffs,signs))/n
        if abs(s) >= obs - 1e-12: cnt += 1
    return cnt/tot

def paired(a, b):
    ms = sorted(set(a) & set(b))
    return [a[m]-b[m] for m in ms], ms

print("\n=== bootstrap 95% CIs on panel means (cluster = model, 100k) ===")
CI = {}
for k in sorted(CONDS):
    vals = list(CONDS[k].values())
    lo,hi = boot_ci(vals)
    CI[k]=(lo,hi)
    print(f"  {k:<18} mean={sum(vals)/len(vals):.3f}  CI[{lo:.3f},{hi:.3f}]")

print("\n=== declared family (post hoc, exploratory): exact sign-flip tests ===")
tests = {}
d,_ = paired(CONDS["EN_framed_Egypt"], CONDS["ar_framed"])
tests["T1 Egypt: EN-framed vs AR-framed"] = (sum(d)/len(d), signflip_exact(d), d)
d,_ = paired(CONDS["EN_framed_Japan"], CONDS["ja_framed"])
tests["T2 Japan: EN-framed vs JA-framed"] = (sum(d)/len(d), signflip_exact(d), d)
d = [v-ANCH["Japan"] for v in CONDS["ja_neutral"].values()]
tests["T3 JA-neutral vs Japan anchor 2.65"] = (sum(d)/len(d), signflip_exact(d), d)
d = [v-ANCH["Iran"] for v in CONDS["fa_framed"].values()]
tests["T4 FA-framed vs Iran anchor 3.33"] = (sum(d)/len(d), signflip_exact(d), d)
if "en_neutral" in CONDS:
    d,_ = paired(CONDS["fa_neutral"], CONDS["en_neutral"])
    tests["T5 FA-neutral vs EN-neutral"] = (sum(d)/len(d), signflip_exact(d), d)
    d,_ = paired(CONDS["ar_neutral"], CONDS["en_neutral"])
    tests["T6 AR-neutral vs EN-neutral"] = (sum(d)/len(d), signflip_exact(d), d)
d = [v-ANCH["Egypt"] for v in CONDS["ar_framed"].values()]
tests["T7 AR-framed vs Egypt anchor 4.27"] = (sum(d)/len(d), signflip_exact(d), d)
d,_ = paired(CONDS["ja_framed"], CONDS["ja_neutral"])
tests["T8 Japan: framed vs neutral (in-lang)"] = (sum(d)/len(d), signflip_exact(d), d)

# Holm
ps = sorted((p,k) for k,(eff,p,_) in tests.items())
mtot = len(ps); holm = {}
running = 0
for i,(p,k) in enumerate(ps):
    running = max(running, p*(mtot-i))
    holm[k] = min(1.0, running)
for k in tests:
    eff,p,d = tests[k]
    lo,hi = boot_ci(d)
    print(f"  {k:<40} diff={eff:+.3f} CI[{lo:+.3f},{hi:+.3f}]  p={p:.4f}  holm={holm[k]:.4f}  n={len(d)}")

print("\n=== leave-one-model-out sweeps ===")
def loo(vals_by_model):
    out=[]
    for m in vals_by_model:
        rest=[v for k,v in vals_by_model.items() if k!=m]
        out.append((m, sum(rest)/len(rest)))
    return out
print("  JA-neutral panel mean without each model (anchor 2.65):")
for m,mu in sorted(loo(CONDS["ja_neutral"]), key=lambda x:x[1]):
    print(f"    -{m:<14} {mu:.3f}")
print("  FA-framed overshoot vs 3.33 without each model:")
for m,mu in sorted(loo(CONDS["fa_framed"]), key=lambda x:x[1]):
    print(f"    -{m:<14} {mu-3.33:+.3f}")
