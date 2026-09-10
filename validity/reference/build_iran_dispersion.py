#!/usr/bin/env python3
"""Per-sample person-level SDs for the Iranian MFQ-2 anchor, from Hazrati, Nejat and Daneshi
(2025), computed the way reasoner-study's build_mfq2_dispersion.py computes the Atari set.

NOT on the reproduce path: needs pyreadstat, and reads respondent microdata that stays out of
git (validity/reference/_raw/, view-only OSF project zt3u2, the authors' data-availability
link). Its aggregate output, mfq2_iran_dispersion.csv, is committed and read with stdlib.

Scoring: six items per foundation in the files' canonical order, mean per respondent, binding
the mean of loyalty, authority and purity, and the Loyalty-Authority composite the mean of those
two; the SDs are taken over the authors' own composite
columns, so their inclusion rule applies: a respondent with any missing item has no composite. Administered 0-4; +1 is applied so means match the
1-5 figures in anchors_iran.json. SD is the sample SD (n-1), as in the Atari file.

Gate: the shifted means of item means must reproduce anchors_iran.json's means_1to5 (the
published Table 2 means) to 0.005 for both samples, and the authors' own foundation columns to
0.001, or nothing is written.

    venv/bin/python validity/reference/build_iran_dispersion.py   (a scratch venv with pyreadstat; venv/ is gitignored)
"""
import csv, json, statistics as st, sys
from pathlib import Path
import pyreadstat

HERE = Path(__file__).resolve().parent
FOUND = ["care", "equality", "proportionality", "loyalty", "authority", "purity"]
BIND = FOUND[3:]
FILES = {"s1": ("MFQ2_Sample1.sav", "MFQ2_", "Filter_2"),
         "s2": ("MFQ2_Sample2.sav", "", "Filter")}
pub = json.load(open(HERE.parent / "anchors_iran.json"))

rows = []
for s, (fname, prefix, filt) in FILES.items():
    data, meta = pyreadstat.read_sav(str(HERE / "_raw" / fname), output_format="dict")
    cols = list(data.keys()); items = cols[:36]
    assert all(c.startswith(prefix) for c in items), items[:3]
    n_all = len(data[items[0]])
    keep = [i for i in range(n_all) if data[filt][i] in (1, 1.0)] if filt in data else list(range(n_all))
    per = []   # per respondent: foundation means (0-4) and binding
    for i in keep:
        f = {}
        for gi, g in enumerate(FOUND):
            vals = [data[c][i] for c in items[gi * 6:(gi + 1) * 6]]
            vals = [v for v in vals if v is not None]
            f[g] = sum(vals) / len(vals) if vals else None
        per.append(f)
    # gate 1: the published Table 2 means are means of item means, each item over its own
    # available responses; anchors_iran.json carries them. Sample 1 has 445 missing item values
    # across 16 respondents, so this differs from the mean of per-respondent means by ~0.01.
    for gi, g in enumerate(FOUND):
        got = st.mean(st.mean(v for v in data[c] if v is not None) for c in items[gi * 6:(gi + 1) * 6]) + 1
        exp = pub["means_1to5"][g][s]
        flag = "OK" if abs(got - exp) < 0.005 else "MISMATCH"
        print("  %s %-16s ours %.3f  published %.3f  %s" % (s, g, got, exp, flag), file=sys.stderr)
        if flag != "OK":
            sys.exit("gate failed: %s %s" % (s, g))
    # gate 2: the authors' own foundation columns, where present
    for g in FOUND:
        col = prefix + g.capitalize()
        if col in data:
            theirs = [data[col][i] for i in keep]
            pairs = [(a, b) for a, b in zip((x[g] for x in per), theirs) if a is not None and b is not None]
            mx = max(abs(a - b) for a, b in pairs)
            if mx > 0.001:
                sys.exit("gate failed: %s %s differs from the authors' column by %.4f" % (s, g, mx))
    # The SDs use the authors' OWN composite columns, so their inclusion rule is theirs: a
    # respondent with any missing item has no composite in their file and is not in the SD.
    # (A mean over available items would keep 8 more respondents in sample 1; the authors
    # did not, and this is their statistic.) The recomputation above is the gate, not the source.
    theirs = {g: [data[prefix + g.capitalize()][i] for i in keep] for g in FOUND}
    full = [i for i in range(len(keep)) if all(theirs[g][i] is not None for g in BIND)]
    binding = [sum(theirs[g][i] for g in BIND) / 3 for i in full]
    full_la = [i for i in range(len(keep)) if all(theirs[g][i] is not None for g in ("loyalty", "authority"))]
    la = [(theirs["loyalty"][i] + theirs["authority"][i]) / 2 for i in full_la]
    row = {"sample": s, "n_file": n_all, "n_kept": len(keep), "n_binding": len(full),
           "binding_mean_1to5": round(st.mean(binding) + 1, 4), "binding_sd": round(st.stdev(binding), 4)}
    for g in FOUND:
        row[g + "_sd"] = round(st.stdev([v for v in theirs[g] if v is not None]), 4)
    row["n_loyalty_authority"] = len(full_la)
    row["loyalty_authority_mean_1to5"] = round(st.mean(la) + 1, 4)
    row["loyalty_authority_sd"] = round(st.stdev(la), 4)
    rows.append(row)
    print("  %s kept %d of %d, binding on %d; binding mean %.3f (published %.3f), SD %.4f" % (
        s, len(keep), n_all, len(full), row["binding_mean_1to5"], pub["binding_1to5"][s], row["binding_sd"]), file=sys.stderr)

with open(HERE / "mfq2_iran_dispersion.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("wrote", HERE / "mfq2_iran_dispersion.csv", file=sys.stderr)
