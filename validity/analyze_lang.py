#!/usr/bin/env python3
"""In-language MFQ-2 analysis: per-condition foundation/binding profiles vs the
English-framed run (runs_framed/) and human anchors. Stdlib only.
    python3 validity/analyze_lang.py
"""
import json, glob
from pathlib import Path
from collections import defaultdict

VDIR = Path(__file__).resolve().parent
FOUND = ["care", "equality", "proportionality", "loyalty", "authority", "purity"]
BIND = ["loyalty", "authority", "purity"]

ANCHOR = {
    "Egypt": {"binding": 4.27, "note": "Atari Table 7"},
    "Japan": {"binding": 2.65, "note": "Atari Table 7 (approx)"},
    "Iran": {"binding": 3.33, "note": "Hazrati 2025 S2 (N=989), rescaled 0-4 -> 1-5"},
}


def foundation_means(ratings):
    by = defaultdict(list)
    for iid, v in ratings.items():
        by[iid.rsplit("_", 1)[0]].append(v)
    return {g: sum(v) / len(v) for g, v in by.items()}


def collect(pattern, keyfn):
    """-> {key: {model: [per-iter binding]}} and foundation profiles."""
    bind = defaultdict(lambda: defaultdict(list))
    prof = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for f in glob.glob(pattern):
        d = json.load(open(f))
        if not d.get("ratings"):
            continue
        k = keyfn(d)
        if k is None:
            continue
        fm = foundation_means(d["ratings"])
        if any(g not in fm for g in FOUND):
            continue
        b = sum(fm[g] for g in BIND) / 3
        bind[k][d["model"]].append(b)
        for g in FOUND:
            prof[k][d["model"]][g].append(fm[g])
    return bind, prof


def panel_stats(permodel):
    means = [sum(v) / len(v) for v in permodel.values()]
    n = len(means)
    if n == 0:
        return None, None, 0
    mu = sum(means) / n
    sd = (sum((x - mu) ** 2 for x in means) / n) ** 0.5
    return mu, sd, n


def report(bind, prof, title):
    print(f"\n=== {title} ===")
    print(f"{'condition':<28} {'panel_binding':>13} {'between-mSD':>11} {'models':>7}")
    for k in sorted(bind):
        mu, sd, n = panel_stats(bind[k])
        print(f"{str(k):<28} {mu:13.2f} {sd:11.2f} {n:7d}")
    return {k: panel_stats(bind[k]) for k in bind}


# in-language runs
bl, pl = collect(str(VDIR / "runs_framed_lang" / "*.json"),
                 lambda d: (d["instrument"].split("_")[1],
                            d["condition"] if d["condition"] != "framed"
                            else "framed_" + d["country"]))
rl = report(bl, pl, "IN-LANGUAGE (official translations)")

# English framed runs, restrict to countries of interest
be, pe = collect(str(VDIR / "runs_framed" / "*_mfq2_*.json"),
                 lambda d: d.get("country") if d.get("country") in ("Egypt", "Japan", "Iran") else None)
re_ = report(be, pe, "ENGLISH framed (07-20 run)")

LANG_COUNTRY = {"ar": "Egypt", "ja": "Japan", "fa": "Iran"}
print("\n=== verdicts (binding composite, 1-5) ===")
print(f"{'country':<8} {'human':>6} {'EN-framed':>10} {'LANG-framed':>12} {'LANG-neutral':>13} "
      f"{'EN-overshoot':>13} {'LANG-overshoot':>15}")
for code, country in LANG_COUNTRY.items():
    hf = ANCHOR.get(country, {}).get("binding")
    en = re_.get(country, (None,))[0] if re_.get(country) else None
    lf = rl.get((code, "framed_" + country), (None,))[0] if rl.get((code, "framed_" + country)) else None
    ln = rl.get((code, "neutral"), (None,))[0] if rl.get((code, "neutral")) else None
    if lf is None:
        continue
    eno = f"{en-hf:+.2f}" if (en is not None and hf) else "-"
    lno = f"{lf-hf:+.2f}" if hf else "-"
    print(f"{country:<8} {hf if hf else '-':>6} {en if en is not None else float('nan'):10.2f} "
          f"{lf:12.2f} {ln:13.2f} {eno:>13} {lno:>15}")
print("\nEnglish NEUTRAL panel binding (07-20 write-up): 2.71 (between-model SD 0.34)")
print("\nper-foundation panel means, in-language conditions:")
for k in sorted(pl):
    agg = {g: [] for g in FOUND}
    for m, gd in pl[k].items():
        for g in FOUND:
            agg[g].append(sum(gd[g]) / len(gd[g]))
    line = " ".join(f"{g[:4]}={sum(v)/len(v):.2f}" for g, v in agg.items())
    print(f"  {str(k):<22} {line}")
