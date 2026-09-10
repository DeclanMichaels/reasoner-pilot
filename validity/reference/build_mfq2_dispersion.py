#!/usr/bin/env python3
"""Per-country DISPERSION for the MFQ-2 reference: foundation SDs, the binding composite, and
the Loyalty-Authority composite (mean of the two; the binding three less Purity).

Companion to build_mfq2_means.py, same source, same scoring, same attention filter. It exists
because one quantity the published means cannot give is the person-level SD of the BINDING
composite: Var(mean of loyalty, authority, purity) depends on the three covariances among them,
and a table of foundation means and SEs carries only the variances. Computing it needs one pass
over the respondents.

Bounds, for reference: assuming independence understates the binding SD by roughly a third
(Arabic 0.449 against the true 0.705); assuming perfect correlation overstates it (0.777). The
true value is nearer the upper bound because the binding three correlate strongly.

  source project : osf.io/srtxn  ("Morality Beyond the WEIRD", Atari et al. 2023, JPSP)
  raw data       : Data/Study 2/Study_2_raw_dat.csv   (download: osf.io/9dwzt)
  authors' code  : Code/Study 2/Code_Study2.R         (download: osf.io/vwrpn)

Microdata is NOT committed (licence parity with build_mfq2_means.py and the ESS builder). Put it
in _raw/ , which is gitignored, or pass a path. The OUTPUT is aggregate and is committed.

    python3 build_mfq2_dispersion.py [_raw/Study_2_raw_dat.csv] > mfq2_country_dispersion.csv
"""
import csv, statistics as st, sys
from pathlib import Path

COMP = {
 "care": ["care1","care3","care11","care12","care13","care14"],
 "equality": ["equalFairness6","equalFairness10","equality2","equality4","equality6","equality10"],
 "proportionality": ["propFairness1","propFairness3","proportionality5","proportionality9","proportionality12","proportionality17"],
 "loyalty": ["loyalty5","loyalty6","loyalty12","loyalty13","loyalty14","loyalty16"],
 "authority": ["authority6","authority8","authority11","authority14","authority18","authority20"],
 "purity": ["purity2","purity3","purity6","purity9","purity13","purity17"],
}
FOUND = list(COMP)
BIND = ["loyalty", "authority", "purity"]


def item(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if 1 <= f <= 5 else None


def main(path):
    rows = [r for r in csv.DictReader(open(path))
            if r.get("attention1") == "3" and r.get("attention2") == "5" and r.get("attention3") == "2"]
    per = {}
    for r in rows:
        comps = {}
        for f, its in COMP.items():
            vals = [item(r.get(k)) for k in its]
            if not all(v is not None for v in vals):
                break
            comps[f] = sum(vals) / 6.0
        else:
            comps["binding"] = sum(comps[b] for b in BIND) / 3.0
            comps["loyalty_authority"] = (comps["loyalty"] + comps["authority"]) / 2.0
            per.setdefault(r["country"].strip(), []).append(comps)

    w = csv.writer(sys.stdout)
    w.writerow(["country", "n", "binding_mean", "binding_sd"] + [f + "_sd" for f in FOUND]
               + ["loyalty_authority_mean", "loyalty_authority_sd"])
    for c in sorted(per):
        v = per[c]
        w.writerow([c, len(v), round(st.fmean(x["binding"] for x in v), 4),
                    round(st.stdev(x["binding"] for x in v), 4)] +
                   [round(st.stdev(x[f] for x in v), 4) for f in FOUND] +
                   [round(st.fmean(x["loyalty_authority"] for x in v), 4),
                    round(st.stdev(x["loyalty_authority"] for x in v), 4)])
    sys.stderr.write("kept %d rows, %d countries\n" % (len(rows), len(per)))


if __name__ == "__main__":
    d = Path(__file__).resolve().parent
    main(sys.argv[1] if len(sys.argv) > 1 else d / "_raw" / "Study_2_raw_dat.csv")
