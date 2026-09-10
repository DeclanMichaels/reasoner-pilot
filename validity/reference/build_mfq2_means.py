#!/usr/bin/env python3
"""Build the MFQ-2 country-means reference from Atari et al. (2023) Study 2 raw data.

This does NOT ship Atari's microdata (its OSF licence governs the raw file; download it
yourself, free). It reads the Study-2 raw CSV and computes per-country MFQ-2 foundation
means, replicating the scoring in the authors' own Code_Study2.R EXACTLY:

  source project : osf.io/srtxn  ("Morality Beyond the WEIRD", Atari et al. 2023, JPSP)
  raw data       : Data/Study 2/Study_2_raw_dat.csv   (download: osf.io/9dwzt)
  authors' code  : Code/Study 2/Code_Study2.R         (download: osf.io/vwrpn)

Final MFQ-2 composites (6 items each, mean; from Code_Study2.R lines ~374-380):
  care            = mean(care1, care3, care11, care12, care13, care14)
  equality        = mean(equalFairness6, equalFairness10, equality2, equality4, equality6, equality10)
  proportionality = mean(propFairness1, propFairness3, proportionality5, proportionality9,
                         proportionality12, proportionality17)
  loyalty         = mean(loyalty5, loyalty6, loyalty12, loyalty13, loyalty14, loyalty16)
  authority       = mean(authority6, authority8, authority11, authority14, authority18, authority20)
  purity          = mean(purity2, purity3, purity6, purity9, purity13, purity17)

Scale 1-5 (higher = describes me better). The published Study-2 file is already the final
analytic sample (attention1==3 & attention2==5 & attention3==2 for all rows; 19 countries,
~205 each, N=3902). The attention guard is kept for parity. Country names are as coded by
the authors (note: 'Columbia' is their spelling of Colombia).

    python3 build_mfq2_means.py [_raw/Study_2_raw_dat.csv] > mfq2_country_means.csv
"""
import csv, statistics, math, sys
COMP = {
 "care": ["care1","care3","care11","care12","care13","care14"],
 "equality": ["equalFairness6","equalFairness10","equality2","equality4","equality6","equality10"],
 "proportionality": ["propFairness1","propFairness3","proportionality5","proportionality9","proportionality12","proportionality17"],
 "loyalty": ["loyalty5","loyalty6","loyalty12","loyalty13","loyalty14","loyalty16"],
 "authority": ["authority6","authority8","authority11","authority14","authority18","authority20"],
 "purity": ["purity2","purity3","purity6","purity9","purity13","purity17"],
}
FOUND=list(COMP)
def item(v):
    try: f=float(v)
    except: return None
    return f if 1<=f<=5 else None
def se(xs): return (statistics.stdev(xs)/math.sqrt(len(xs))) if len(xs)>1 else 0.0
def main(path):
    rows=list(csv.DictReader(open(path)))
    kept=[r for r in rows if r.get("attention1")=="3" and r.get("attention2")=="5" and r.get("attention3")=="2"]
    acc={}; ncomplete={}
    for r in kept:
        c=r["country"].strip()
        acc.setdefault(c,{f:[] for f in FOUND}); ncomplete.setdefault(c,0)
        comps={}; ok=True
        for f,its in COMP.items():
            vals=[item(r.get(k)) for k in its]
            if all(v is not None for v in vals): comps[f]=sum(vals)/6.0
            else: ok=False
        if ok: ncomplete[c]+=1
        for f,v in comps.items(): acc[c][f].append(v)
    w=csv.writer(sys.stdout)
    w.writerow(["country","n"]+FOUND+[f+"_se" for f in FOUND])
    for c in sorted(acc):
        means=[round(statistics.fmean(acc[c][f]),4) for f in FOUND]
        ses=[round(se(acc[c][f]),4) for f in FOUND]
        w.writerow([c,ncomplete[c]]+means+ses)
    sys.stderr.write("kept %d rows, %d countries\n"%(len(kept),len(acc)))
if __name__=="__main__":
    from pathlib import Path
    main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parent / "_raw" / "Study_2_raw_dat.csv")
