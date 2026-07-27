#!/usr/bin/env python3
"""Foundation-level extension of the in-language audit. Same conventions:
unit = model (11 clusters), aggregate-then-estimate, 100k bootstrap over models
(seed 20260723), exact sign-flip where a test is made. Covers the paper's new
foundation-level claims:
  F1  JA-neutral per-foundation deltas vs Japan Table 7 anchors (CIs)
  F2  the offsetting-misses decomposition of the JA-neutral binding match
  F3  the Care ceiling: per-condition Care panel means + CIs, and the minimum
      panel Care across all 10 conditions vs the Japan anchor 3.03
    python3 validity/audit_foundations_ext.py
"""
import json, glob, random, itertools
from pathlib import Path
from collections import defaultdict

VDIR = Path(__file__).resolve().parent
FOUND = ["care","equality","proportionality","loyalty","authority","purity"]
JP = {"care":3.03,"equality":2.27,"proportionality":3.14,"loyalty":2.66,"authority":2.67,"purity":2.63}
SEED, B = 20260723, 100_000

def fmeans(r):
    by = defaultdict(list)
    for iid,v in r.items(): by[iid.rsplit("_",1)[0]].append(v)
    return {g: sum(v)/len(v) for g,v in by.items()}

def permodel(pat, keyf):
    acc = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for f in glob.glob(pat):
        d = json.load(open(f))
        if not d.get("ratings"): continue
        k = keyf(d)
        if k is None: continue
        fm = fmeans(d["ratings"])
        if any(g not in fm for g in FOUND): continue
        for g in FOUND: acc[k][d["model"]][g].append(fm[g])
    return {k: {m: {g: sum(v[g])/len(v[g]) for g in FOUND} for m,v in md.items()} for k,md in acc.items()}

L = permodel(str(VDIR/"runs_framed_lang"/"*.json"), lambda d:(d["instrument"].split("_")[1],d["condition"]))
E = permodel(str(VDIR/"runs_framed"/"*_mfq2_*.json"), lambda d:d.get("country"))
N = permodel(str(VDIR/"runs"/"*mfq2*.json"), lambda d:"en_neutral" if d.get("instrument")=="mfq2" else None)

rng = random.Random(SEED)
def ci(vals):
    n=len(vals); s=[]
    for _ in range(B):
        t=[vals[rng.randrange(n)] for _ in range(n)]; s.append(sum(t)/n)
    s.sort(); return sum(vals)/n, s[int(.025*B)], s[int(.975*B)]

def sf(diffs):
    n=len(diffs); obs=abs(sum(diffs)/n); c=0
    for signs in itertools.product((1,-1),repeat=n):
        if abs(sum(x*g for x,g in zip(diffs,signs))/n)>=obs-1e-12: c+=1
    return c/2**n

print("=== F1: JA-neutral per-foundation delta vs Japan anchor ===")
jn = L[("ja","neutral")]
for g in FOUND:
    d=[jn[m][g]-JP[g] for m in jn]
    mu,lo,hi=ci(d)
    print(f"  {g:<16} delta={mu:+.3f} CI[{lo:+.3f},{hi:+.3f}] p={sf(d):.4f}")

print("\n=== F2: offsetting-misses decomposition (binding composite) ===")
comp=[ (jn[m]["loyalty"]-JP["loyalty"] + jn[m]["authority"]-JP["authority"] + jn[m]["purity"]-JP["purity"])/3 for m in jn]
mu,lo,hi=ci(comp)
print(f"  net binding delta = {mu:+.3f} CI[{lo:+.3f},{hi:+.3f}]  (composite of +L +A -P misses)")

print("\n=== F3: the Care ceiling ===")
CONDS = {**{f"{k[0]}_{k[1]}":v for k,v in L.items()},
         **{f"EN_framed_{k}":v for k,v in E.items()}, "en_neutral":N["en_neutral"]}
lows=[]
for k in sorted(CONDS):
    vals=[CONDS[k][m]["care"] for m in CONDS[k]]
    mu,lo,hi=ci(vals); lows.append((mu,k))
    print(f"  {k:<18} care={mu:.3f} CI[{lo:.3f},{hi:.3f}]")
mn=min(lows)
d=[CONDS[mn[1]][m]["care"]-JP["care"] for m in CONDS[mn[1]]]
mu,lo,hi=ci(d)
print(f"  lowest-Care condition is {mn[1]} ({mn[0]:.3f}); its delta vs Japan anchor 3.03 = {mu:+.3f} CI[{lo:+.3f},{hi:+.3f}] p={sf(d):.4f}")
