#!/usr/bin/env python3
"""Emit everything the in-language viewer needs as one JSON. Stdlib only.

The viewer reads this file and nothing else, so a country added to the collection
appears in the viewer without touching the HTML. Same conventions as
validity/audit_inlanguage.py: the model is the independent unit, iterations averaged
first, bootstrap 100,000 draws resampling models, each interval seeded from the run
seed plus the quantity's own name.

    python3 validity/build_viewer_data.py > validity/results/viewer_data.json
"""
import json, glob, itertools, random, sys, time
from pathlib import Path
from collections import defaultdict

VDIR = Path(__file__).resolve().parent
FOUND = ["care", "equality", "proportionality", "loyalty", "authority", "purity"]
BIND = ["loyalty", "authority", "purity"]
SEED = 20260723
B = 100_000

# Iran is the only anchor not from Atari Study 2 and is the only one stated by hand.
# Everything else is derived below from the committed reference, so a country gets its
# anchor by being in that file rather than by someone retyping a number.
ANCH = {"Iran": 3.333}
ANCH_SRC = {"Iran": "Hazrati et al. 2025, sample 2"}

# Per-foundation human profiles. Every Atari country has one in the published reference; they
# are read from a committed copy of mfq2_country_means.csv rather than retyped, so a country
# gains its profile by existing in that file. Iran is not in Atari and is carried separately.
# Repo boundary: reasoner-study owns the reference, this is a documented copy (4_toolbox Paths).
ANCH_FOUND = {
    "Iran": {"care": 3.948, "equality": 2.672, "proportionality": 4.147,
             "loyalty": 3.630, "authority": 3.050, "purity": 3.318},
}
ANCH_N = {"Iran": 989}   # Hazrati sample 2
_CSV_NAME = {"UAE": "United Arab Emirates", "Columbia": "Colombia"}
_ref = VDIR / "reference" / "mfq2_country_means.csv"
if _ref.exists():
    import csv as _csv
    for _r in _csv.DictReader(open(_ref)):
        _c = _CSV_NAME.get(_r["country"].strip(), _r["country"].strip())
        ANCH_FOUND.setdefault(_c, {f: round(float(_r[f]), 4) for f in FOUND})
        ANCH_N.setdefault(_c, int(_r["n"]))
        ANCH.setdefault(_c, round(sum(float(_r[b]) for b in BIND) / 3, 3))
        ANCH_SRC.setdefault(_c, "Atari et al. 2023, Study 2")
else:
    sys.exit(f"missing {_ref}; copy it from reasoner-study/instruments/MFQ-PVQ/mfq/reference/")

# The composites above must equal (loyalty + authority + purity) / 3 of the profile just loaded.
# A silent disagreement would put a country's caret and its dot on different scales.
for _c, _v in ANCH.items():
    _f = ANCH_FOUND.get(_c)
    if _f and abs(sum(_f[b] for b in BIND) / 3 - _v) > 0.001:
        sys.exit(f"{_c}: composite {_v} disagrees with its foundation profile "
                 f"{sum(_f[b] for b in BIND) / 3:.4f}")

LANGS = {"ar": "Arabic", "ja": "Japanese", "fa": "Farsi",
         "es": "Spanish", "fr": "French", "ru": "Russian"}


def fmeans(r):
    by = defaultdict(list)
    for iid, v in r.items():
        by[iid.rsplit("_", 1)[0]].append(v)
    return {g: sum(v) / len(v) for g, v in by.items()}


def binding(r):
    f = fmeans(r)
    return None if any(g not in f for g in FOUND) else sum(f[g] for g in BIND) / 3


def mean(v):
    return sum(v) / len(v)


def sd(v):
    m = mean(v)
    return (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5


def boot(vals, key):
    rng = random.Random("%d|%s" % (SEED, key))
    n = len(vals)
    s = sorted(sum(vals[rng.randrange(n)] for _ in range(n)) / n for _ in range(B))
    return s[int(0.025 * B)], s[int(0.975 * B)]


# ---- load: per condition, per model, the binding value and the six foundations
bind_acc = defaultdict(lambda: defaultdict(list))
found_acc = defaultdict(lambda: defaultdict(list))
usage = defaultdict(lambda: {"reasoning": 0, "output": 0, "input": 0, "n": 0})
cells = 0

# ENGLISH UNFRAMED, changed 2026-08-22. This used to be our own transcription of the
# MFQ-2 administered with run_validity.py's self-report system prompt, while every
# in-language unframed arm used the official Atari et al. translation with NO system
# prompt: the comparator differed from what it was compared against in two ways at once.
# Both were measured (results/english_baseline_audit.txt): instrument -0.038 p=.47,
# system prompt +0.026 p=.49, neither distinguishable from zero. The official no-system
# cell is the baseline now because it is the matched one. The old cell is kept under
# en_neutral_ours so the errata can cite what was published before.
SRC = [(VDIR / "runs_framed_lang" / "*.json",
        lambda d: "%s_%s" % (d["instrument"].split("_")[1],
                             d["condition"] if d["condition"] != "framed"
                             else "framed_" + d["country"])),
       (VDIR / "runs_framed" / "*_mfq2_*.json",
        lambda d: ("EN_framed_" + d["country"]) if d.get("country") else None),
       (VDIR / "runs_english_baseline" / "*.json",
        lambda d: "en_neutral" if d["condition"] == "official_nosystem"
        else "en_baseline_" + d["condition"]),
       (VDIR / "runs" / "*_mfq2_*.json", lambda d: "en_neutral_ours")]

for pat, keyf in SRC:
    for f in glob.glob(str(pat)):
        d = json.load(open(f))
        if not d.get("ratings"):
            continue
        k = keyf(d)
        if k is None:
            continue
        fm = fmeans(d["ratings"])
        if any(g not in fm for g in FOUND):
            continue
        cells += 1
        m = d["model"]
        bind_acc[k][m].append(sum(fm[g] for g in BIND) / 3)
        found_acc[k][m].append(fm)
        u = d.get("usage") or {}
        for fld in ("reasoning", "output", "input"):
            usage[m][fld] += int(u.get(fld) or 0)
        usage[m]["n"] += 1

C = {k: {m: mean(v) for m, v in md.items()} for k, md in bind_acc.items()}
F = {k: {m: {g: mean([x[g] for x in v]) for g in FOUND} for m, v in md.items()}
     for k, md in found_acc.items()}
ROSTER = sorted({m for v in C.values() for m in v})


def cond(k):
    if k not in C:
        return None
    vals = list(C[k].values())
    lo, hi = boot(vals, k)
    return {"mean": round(mean(vals), 4), "ci": [round(lo, 4), round(hi, 4)],
            "sd": round(sd(vals), 4), "n_models": len(vals),
            "per_model": {m: round(v, 4) for m, v in sorted(C[k].items())},
            "foundations": {g: round(mean([F[k][m][g] for m in F[k]]), 4) for g in FOUND}}


# ---- which country goes with which language, discovered from the data
pairs = {}
for k in C:
    if "_framed_" in k and not k.startswith("EN_"):
        code, country = k.split("_framed_", 1)
        pairs[country] = code

# Morocco was administered to HUMANS in Spanish (Atari et al. 2023, Table 3) while its own
# majority language is Arabic. The two analyses want different arms. Comparing the panel to
# Morocco's human anchor wants the Spanish arm, because that is the like-for-like match. The
# ordering and foundation-shift analyses ask what administering in ARABIC does, and
# Morocco-in-Arabic is a real observation of that, so the language group keeps the Arabic run.
# Both arms are carried; neither is discarded.
ANCHOR_CODE = {"Morocco": "es"}

countries = []
for country in sorted(set(list(pairs) + [c.split("EN_framed_", 1)[1]
                                         for c in C if c.startswith("EN_framed_")])):
    code = pairs.get(country)
    row = {
        "country": country,
        "language": LANGS.get(code) if code else None,
        "lang_code": code,
        "human": ANCH.get(country),
        "human_source": ANCH_SRC.get(country),
        "human_foundations": ANCH_FOUND.get(country),
        "human_n": ANCH_N.get(country),
        "conditions": {
            "en_unframed": cond("en_neutral"),
            "local_unframed": cond(code + "_neutral") if code else None,
            "en_framed": cond("EN_framed_" + country),
            "local_framed": cond((ANCHOR_CODE.get(country) or code) + "_framed_" + country)
                            if code else None,
        },
    }
    # where the two differ, carry the group's own arm beside the anchor-matched one so the
    # page can show both rather than implying only one run exists
    ac = ANCHOR_CODE.get(country)
    if ac and code and ac != code:
        row["anchor_lang"] = LANGS.get(ac)
        row["group_lang"] = LANGS.get(code)
        row["group_framed"] = cond(code + "_framed_" + country)
    h = row["human"]
    row["deviation"] = {kk: (round(v["mean"] - h, 4) if (v and h is not None) else None)
                        for kk, v in row["conditions"].items()}
    countries.append(row)

# ---- language groups: the within-language ordering comparison
groups = []
for code, name in LANGS.items():
    members = [r for r in countries if r["lang_code"] == code and r["human"] is not None]
    if len(members) < 2:
        continue
    g = {"lang_code": code, "language": name, "countries": [r["country"] for r in members]}
    for cname, ckey in (("local_framed", "local_framed"), ("en_framed", "en_framed")):
        got = [(r["country"], r["conditions"][ckey]["mean"]) for r in members
               if r["conditions"][ckey]]
        if len(got) != len(members):
            continue
        hum = sorted(members, key=lambda r: -r["human"])
        pan = sorted(got, key=lambda x: -x[1])
        rh = {r["country"]: i for i, r in enumerate(hum)}
        rp = {c: i for i, (c, _) in enumerate(pan)}
        n = len(members)
        dsq = sum((rh[c] - rp[c]) ** 2 for c in rh)
        g[cname] = {
            "human_order": [r["country"] for r in hum],
            "panel_order": [c for c, _ in pan],
            "spearman": round(1 - 6 * dsq / (n * (n * n - 1)), 3),
            "panel_spread": round(max(v for _, v in got) - min(v for _, v in got), 4),
            "human_spread": round(max(r["human"] for r in members)
                                  - min(r["human"] for r in members), 4),
        }
    groups.append(g)

# ---- what framing moves, foundation by foundation
# The binding composite is three of the six foundations averaged, so a shift in it says
# nothing about whether the other three moved. This computes, per model, the mean over a
# language's countries of (in-language framed minus in-language unframed) for each
# foundation separately, and tests each with the same exact sign-flip used elsewhere.
def signflip(d):
    n = len(d)
    obs = abs(mean(d))
    hits = sum(1 for s in itertools.product((1, -1), repeat=n)
               if abs(mean([a * b for a, b in zip(s, d)])) >= obs - 1e-12)
    return hits / 2 ** n


shifts = []
for g in groups + [{"lang_code": c, "language": LANGS[c],
                    "countries": [r["country"] for r in countries if r["lang_code"] == c]}
                   for c in LANGS if not any(x["lang_code"] == c for x in groups)]:
    code = g["lang_code"]
    nk = code + "_neutral"
    cs = [c for c in g["countries"] if code + "_framed_" + c in F]
    if nk not in F or not cs:
        continue
    ms = sorted(set(F[nk]) & set.intersection(*[set(F[code + "_framed_" + c]) for c in cs]))
    row = {"lang_code": code, "language": g["language"], "countries": cs,
           "n_models": len(ms), "foundations": {}}
    for fo in FOUND:
        d = [mean([F[code + "_framed_" + c][m][fo] for c in cs]) - F[nk][m][fo] for m in ms]
        lo, hi = boot(d, "shift|%s|%s" % (code, fo))
        row["foundations"][fo] = {
            "shift": round(mean(d), 4), "ci": [round(lo, 4), round(hi, 4)],
            "p": round(signflip(d), 4),
            "up": sum(1 for x in d if x > 0), "down": sum(1 for x in d if x < 0),
            "unframed": round(mean([F[nk][m][fo] for m in ms]), 4),
            "framed": round(mean([mean([F[code + "_framed_" + c][m][fo] for c in cs])
                                  for m in ms]), 4)}
    shifts.append(row)

# ---- reasoning cost, per model
gap = defaultdict(list)
for k in C:
    present = C[k]
    if len(present) < 3:
        continue
    for m, v in present.items():
        others = [x for mm, x in present.items() if mm != m]
        gap[m].append(abs(v - mean(others)))
spread = defaultdict(list)
for k, md in bind_acc.items():
    for m, v in md.items():
        if len(v) > 1:
            spread[m].append(sd(v))
models = []
for m in ROSTER:
    u = usage[m]
    n = max(u["n"], 1)
    models.append({
        "model": m, "cells": u["n"],
        "reasoning_per_call": round(u["reasoning"] / n, 1),
        "output_per_call": round(u["output"] / n, 1),
        "reasoning_share": round(u["reasoning"] / (u["reasoning"] + u["output"]), 4)
        if (u["reasoning"] + u["output"]) else 0,
        "total_reasoning": u["reasoning"],
        "gap_to_panel": round(mean(gap[m]), 4) if gap.get(m) else None,
        "own_spread": round(mean(spread[m]), 4) if spread.get(m) else None,
    })

out = {
    "meta": {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "produced_by": "validity/build_viewer_data.py",
        "reads": "validity/runs_framed_lang, validity/runs_framed, validity/runs",
        "scored_cells": cells,
        "conditions": len(C),
        "models": len(ROSTER),
        "roster": ROSTER,
        "unit_of_analysis": "model; each model's iterations averaged before any test",
        "intervals": "percentile bootstrap, 100,000 draws resampling models, "
                     "seeded per quantity from seed %d" % SEED,
        "scale": [1, 5],
        "measure": "binding composite, the mean of Loyalty, Authority and Purity",
    },
    "countries": countries,
    "language_groups": groups,
    "models": models,
    "foundation_shifts": shifts,
    "conditions_raw": {k: cond(k) for k in sorted(C)},
}
json.dump(out, sys.stdout, indent=1, sort_keys=False)
sys.stdout.write("\n")
