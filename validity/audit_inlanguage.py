#!/usr/bin/env python3
"""Post-hoc statistical audit of the in-language MFQ-2 study. Stdlib only.

Independent unit: MODEL (11 clusters). All tests aggregate per model first.
- Bootstrap CIs (resample models, 100k, seed 20260723) on each condition's panel mean.
- Exact sign-flip permutation tests (2^11 = 2048 enumerations) on paired per-model
  differences and one-sample-vs-anchor differences.
- Leave-one-model-out sweeps on the two headline quantities.
- Holm correction within each family.

TWO FAMILIES, one per headline claim.
  Family A (T1-T10): the framing claim. Declared and reported in appendix B4; the
    values here are unchanged from the version that produced that table.
  Family B (T5, T6, T11): the language claim. One test per language, asking whether
    the local-language unframed condition departs from the English default. Added
    2026-08-21, after the results were seen, because the declared family omitted the
    Japanese case and so contained no complete test of the claim the title makes.
    T5 and T6 belong to both families; that double membership is disclosed rather
    than resolved by re-partitioning A, since re-cutting a declared family after
    seeing results is the larger sin and every conclusion holds under both cuts.

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
# Framed in-language cells are keyed BY COUNTRY. Without the country every Arabic
# framed country pools into a single "ar_framed" bucket and silently moves the published
# Egypt number; that happened for real on 2026-08-21 with three test cells.
lang = permodel(str(VDIR/"runs_framed_lang"/"*.json"),
                lambda d: (d["instrument"].split("_")[1],
                           d["condition"] if d["condition"] != "framed"
                           else "framed_" + d["country"]))
enfr = permodel(str(VDIR/"runs_framed"/"*_mfq2_*.json"),
                lambda d: d.get("country") if d.get("country") in ("Egypt","Japan","Iran") else None)
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
EXPECT = {"ar_framed_Egypt":4.61,"ar_neutral":3.03,"ja_framed_Japan":3.46,"ja_neutral":2.66,
          "fa_framed_Iran":4.36,"fa_neutral":2.72,"EN_framed_Egypt":4.61,"EN_framed_Japan":3.67}
print("  reconcile vs analyze_lang.py:")
ok = True
for k,e in EXPECT.items():
    got = sum(CONDS[k].values())/len(CONDS[k])
    match = abs(got-e) < 0.006
    ok &= match
    print(f"    {k:<18} expected {e:.2f} got {got:.3f} {'OK' if match else 'MISMATCH'}")
print("  RECONCILED" if ok else "  *** RECONCILIATION FAILED — STOP ***")

def boot_ci(vals, key):
    """Percentile bootstrap over models. The RNG is seeded from (SEED, key), so each
    interval is independent of how many other quantities were computed first. Seeding
    one shared stream made every interval depend on the order and NUMBER of conditions
    present, so adding a condition silently moved the third decimal of unrelated
    intervals. Changed 2026-08-21; that change moved four published bounds by 0.001
    once, and no addition can move them again."""
    rng = random.Random("%d|%s" % (SEED, key))
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
    lo,hi = boot_ci(vals, k)
    CI[k]=(lo,hi)
    print(f"  {k:<18} mean={sum(vals)/len(vals):.3f}  CI[{lo:.3f},{hi:.3f}]")

tests = {}
d,_ = paired(CONDS["EN_framed_Egypt"], CONDS["ar_framed_Egypt"])
tests["T1 Egypt: EN-framed vs AR-framed"] = (sum(d)/len(d), signflip_exact(d), d)
d,_ = paired(CONDS["EN_framed_Japan"], CONDS["ja_framed_Japan"])
tests["T2 Japan: EN-framed vs JA-framed"] = (sum(d)/len(d), signflip_exact(d), d)
d = [v-ANCH["Japan"] for v in CONDS["ja_neutral"].values()]
tests["T3 JA-neutral vs Japan anchor 2.65"] = (sum(d)/len(d), signflip_exact(d), d)
d = [v-ANCH["Iran"] for v in CONDS["fa_framed_Iran"].values()]
tests["T4 FA-framed vs Iran anchor 3.33"] = (sum(d)/len(d), signflip_exact(d), d)
if "en_neutral" in CONDS:
    d,_ = paired(CONDS["fa_neutral"], CONDS["en_neutral"])
    tests["T5 FA-neutral vs EN-neutral"] = (sum(d)/len(d), signflip_exact(d), d)
    d,_ = paired(CONDS["ar_neutral"], CONDS["en_neutral"])
    tests["T6 AR-neutral vs EN-neutral"] = (sum(d)/len(d), signflip_exact(d), d)
d = [v-ANCH["Egypt"] for v in CONDS["ar_framed_Egypt"].values()]
tests["T7 AR-framed vs Egypt anchor 4.27"] = (sum(d)/len(d), signflip_exact(d), d)
d,_ = paired(CONDS["ja_framed_Japan"], CONDS["ja_neutral"])
tests["T8 Japan: framed vs neutral (in-lang)"] = (sum(d)/len(d), signflip_exact(d), d)
if "EN_framed_Iran" in CONDS:
    d = [v-ANCH["Iran"] for v in CONDS["EN_framed_Iran"].values()]
    tests["T9 EN-framed Iran vs anchor 3.33"] = (sum(d)/len(d), signflip_exact(d), d)
    d,_ = paired(CONDS["EN_framed_Iran"], CONDS["fa_framed_Iran"])
    tests["T10 Iran: EN-framed vs FA-framed"] = (sum(d)/len(d), signflip_exact(d), d)

FAMILY_A = list(tests)

# T11 completes the language family: one test per language against the English default.
d,_ = paired(CONDS["ja_neutral"], CONDS["en_neutral"])
tests["T11 JA-neutral vs EN-neutral"] = (sum(d)/len(d), signflip_exact(d), d)

FAMILY_B = ["T5 FA-neutral vs EN-neutral",
            "T6 AR-neutral vs EN-neutral",
            "T11 JA-neutral vs EN-neutral"]

def holm(names):
    ps = sorted((tests[k][1], k) for k in names)
    m = len(ps); out = {}; running = 0.0
    for i,(p,k) in enumerate(ps):
        running = max(running, p*(m-i))
        out[k] = min(1.0, running)
    return out

hA = holm(FAMILY_A)
hB = holm(FAMILY_B)

# One interval per test, drawn once, in family-A order and then T11. A test that
# belongs to both families therefore reports the same interval in both, and the
# family-A draws sit at the same position in the RNG stream as before T11 existed,
# so appendix B4 still reproduces line for line.
CIT = {}
for k in FAMILY_A + ["T11 JA-neutral vs EN-neutral"]:
    CIT[k] = boot_ci(tests[k][2], k)

print("\n=== FAMILY A, the framing claim (post hoc, exploratory): exact sign-flip tests ===")
print("    Ten tests, Holm across the ten. Unchanged from appendix B4.")
for k in FAMILY_A:
    eff,p,d = tests[k]
    lo,hi = CIT[k]
    print(f"  {k:<40} diff={eff:+.3f} CI[{lo:+.3f},{hi:+.3f}]  p={p:.4f}  holm={hA[k]:.4f}  n={len(d)}")

print("\n=== FAMILY B, the language claim (post hoc, exploratory): one test per language ===")
print("    Does the local-language unframed condition depart from the English default?")
print("    Holm across the three. T5 and T6 also appear in family A; see the module docstring.")
for k in FAMILY_B:
    eff,p,d = tests[k]
    lo,hi = CIT[k]
    print(f"  {k:<40} diff={eff:+.3f} CI[{lo:+.3f},{hi:+.3f}]  p={p:.4f}  holm={hB[k]:.4f}  n={len(d)}")
print("  Nulls are bounds, not demonstrated absence. Largest effect each rules out:")
for k in FAMILY_B:
    lo,hi = CIT[k]
    print(f"    {k:<40} |effect| <= {max(abs(lo),abs(hi)):.3f}")
print("  Per-model sign counts (a real shift moves models together):")
for k in FAMILY_B:
    d = tests[k][2]
    print(f"    {k:<40} up {sum(1 for x in d if x>0)}/{len(d)}, down {sum(1 for x in d if x<0)}/{len(d)}")

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
for m,mu in sorted(loo(CONDS["fa_framed_Iran"]), key=lambda x:x[1]):
    print(f"    -{m:<14} {mu-3.33:+.3f}")
print("  T11 (JA-neutral minus EN-neutral) without each model:")
ms = sorted(set(CONDS["ja_neutral"]) & set(CONDS["en_neutral"]))
for drop in ms:
    rest = [CONDS["ja_neutral"][m]-CONDS["en_neutral"][m] for m in ms if m != drop]
    print(f"    -{drop:<14} {sum(rest)/len(rest):+.4f}")
