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

# Iran is the only anchor not from Atari Study 2. It is read from anchors_iran.json rather
# than retyped, on the same principle as the reference file below: a number that appears in
# two places drifts in one of them. The viewer renders its caveats and sensitivity from here.
IRAN = json.load(open(VDIR / "anchors_iran.json"))
ANCH = {"Iran": IRAN["binding_1to5"]["s2"]}
ANCH_SRC = {"Iran": "Hazrati et al. 2025, sample 2"}

# Per-foundation human profiles. Every Atari country has one in the published reference; they
# are read from a committed copy of mfq2_country_means.csv rather than retyped, so a country
# gains its profile by existing in that file. Iran is not in Atari and is carried separately.
# Repo boundary: reasoner-study owns the reference, this is a documented copy (4_toolbox Paths).
ANCH_FOUND = {"Iran": {g: IRAN["means_1to5"][g]["s2"] for g in FOUND}}
ANCH_N = {"Iran": IRAN["samples"]["s2"]["n"]}
_CSV_NAME = {"UAE": "United Arab Emirates", "Columbia": "Colombia"}
_ref = VDIR / "reference" / "mfq2_country_means.csv"
if _ref.exists():
    import csv as _csv
    for _r in _csv.DictReader(open(_ref)):
        _c = _CSV_NAME.get(_r["country"].strip(), _r["country"].strip())
        ANCH_FOUND.setdefault(_c, {f: round(float(_r[f]), 4) for f in FOUND})
        ANCH_N.setdefault(_c, int(_r["n"]))
        ANCH.setdefault(_c, sum(float(_r[b]) for b in BIND) / 3)   # full precision; rounded for display only
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


# ---- load: per condition, per model, the binding value and the six foundations, from the
# published ratings dataset and the collection record (decision 19, #92); no run file is read.
sys.path.insert(0, str(VDIR))
from ratings_dataset import load_cells, load_record
CELLS_ALL = load_cells()
RECORD = load_record()
SEPT = ["en_neutral_sept", "en_neutral_template", "EN_framed_Egypt_sept"]   # the September wave, B4a
CELLS = {k: v for k, v in CELLS_ALL.items() if k not in SEPT}
bind_acc = defaultdict(lambda: defaultdict(list))
found_acc = defaultdict(lambda: defaultdict(list))
cells = 0
for k, md in CELLS.items():
    for m, runs in md.items():
        for c in runs:
            fm = fmeans(c["ratings"])
            if any(g not in fm for g in FOUND):
                continue
            cells += 1
            bind_acc[k][m].append(sum(fm[g] for g in BIND) / 3)
            found_acc[k][m].append(fm)
usage = {m: dict(u) for m, u in RECORD["token_usage"]["grid"].items()}

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
# Decision 18. Atari et al. administered Morocco's human sample in Spanish (their Table 3), so
# Morocco is reported under Spanish in every view and compared on the Spanish arm. Its
# Arabic-framed arm is carried as data beside it and enters no comparison. A country with two
# in-language arms and no entry here is an error, not a default.
GROUP_CODE = {"Morocco": "es"}
ANCHOR_CODE = {"Morocco": "es"}

pairs = {}
for k in C:
    if "_framed_" in k and not k.startswith("EN_"):
        code, country = k.split("_framed_", 1)
        if country in pairs and pairs[country] != code:
            if country not in GROUP_CODE:
                raise SystemExit("%s has two in-language arms and no GROUP_CODE entry" % country)
            code = GROUP_CODE[country]
        pairs[country] = code

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
    # a second in-language arm is carried beside the reported one so the page can say it
    # exists, without comparing it to anything
    other = [c for c in LANGS if c != code and (c + "_framed_" + country) in C]
    if other:
        row["other_arm_lang"] = LANGS[other[0]]
        row["other_arm_framed"] = cond(other[0] + "_framed_" + country)
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
# foundation separately, with a model-resampling interval; no test (decision 15).
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
                        "up": sum(1 for x in d if x > 0), "down": sum(1 for x in d if x < 0),
            "unframed": round(mean([F[nk][m][fo] for m in ms]), 4),
            "framed": round(mean([mean([F[code + "_framed_" + c][m][fo] for c in cs])
                                  for m in ms]), 4)}
    shifts.append(row)

# ---- language against framing, on the binding composite: the document's lead contrast.
# Unframed: the translation minus English unframed, per model. Framing: in-language framed
# minus in-language unframed, per model, averaged over the language's countries with Morocco
# under Spanish (decision 18), the same country sets as the foundation shifts above. Model-
# resampling intervals, seeded per quantity; no test (decision 15).
def _signed(d, key):
    lo, hi = boot(d, key)
    return {"shift": round(mean(d), 4), "ci": [round(lo, 4), round(hi, 4)],
            "up": sum(1 for x in d if x > 0), "down": sum(1 for x in d if x < 0)}
contrasts = []
for row in shifts:
    code, cs = row["lang_code"], row["countries"]
    nk = code + "_neutral"
    ms = sorted(set(C[nk]) & set(C["en_neutral"])
                & set.intersection(*[set(C[code + "_framed_" + c]) for c in cs]))
    contrasts.append({
        "lang_code": code, "language": row["language"], "countries": len(cs), "n_models": len(ms),
        "unframed_mean": round(mean([C[nk][m] for m in ms]), 4),
        "unframed_vs_english": _signed([C[nk][m] - C["en_neutral"][m] for m in ms],
                                       "lang_unframed|%s" % code),
        "framing": _signed([mean([C[code + "_framed_" + c][m] for c in cs]) - C[nk][m] for m in ms],
                           "lang_framing|%s" % code)})
language_contrasts = {
    "english_unframed": round(mean([C["en_neutral"][m] for m in ROSTER]), 4),
    "languages": contrasts,
    "framing_equal_weight": round(mean([e["framing"]["shift"] for e in contrasts]), 4),
    "countries_total": sum(e["countries"] for e in contrasts)}

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

def iran_anchor():
    """Everything the page needs to caveat Iran, computed rather than typed into the HTML."""
    n1, n2 = IRAN["samples"]["s1"]["n"], IRAN["samples"]["s2"]["n"]
    b1, b2 = IRAN["binding_1to5"]["s1"], IRAN["binding_1to5"]["s2"]
    pool = (b1 * n1 + b2 * n2) / (n1 + n2)
    en = mean(list(C["EN_framed_Iran"].values())) if "EN_framed_Iran" in C else None
    fa = mean(list(C["fa_framed_Iran"].values())) if "fa_framed_Iran" in C else None
    def row(label, n, a):
        r = {"label": label, "n": n, "binding": round(a, 3)}
        if en is not None:
            r["en_framed_overshoot"] = round(en - a, 3)
        if fa is not None:
            r["fa_framed_overshoot"] = round(fa - a, 3)
        return r
    alts = [row("sample 2", n2, b2), row("sample 1", n1, b1),
            row("n-weighted pool", n1 + n2, pool)]
    return {
        "source": IRAN["source"],
        "instrument": IRAN["instrument"],
        "scale_note": IRAN["scale_note"],
        "caveats": IRAN["caveats"],
        "in_use": "sample 2",
        "alternatives": alts,
        "in_use_is": ("largest" if b2 == max(b1, b2, pool)
                      else "smallest" if b2 == min(b1, b2, pool) else "middle"),
    }


def _ten_stats(md, models, key):
    vals = [mean(md[m]) if isinstance(md[m], list) else md[m] for m in models]
    lo, hi = boot(vals, key)
    return {"mean": round(mean(vals), 4), "ci": [round(lo, 4), round(hi, 4)], "sd": round(sd(vals), 4), "n_models": len(vals)}
_sept_models = sorted(set.intersection(*[set(CELLS_ALL[k]) for k in SEPT]))
_sept_bind = {k: {m: mean([sum(fmeans(c["ratings"])[g] for g in BIND) / 3 for c in CELLS_ALL[k][m]]) for m in _sept_models} for k in SEPT}
september = {
    "models": _sept_models,
    "collected": (lambda d: d["first"][:4] + "-" + d["first"][4:6] + "-" + d["first"][6:] if d and d["first"] == d["last"]
                  else None)(RECORD["collected"].get("september_wave")),
    "conditions": {**{k: _ten_stats(_sept_bind[k], _sept_models, "sept|" + k) for k in SEPT},
                   "en_neutral_august_ten": _ten_stats(C["en_neutral"], _sept_models, "sept|en_neutral_august_ten"),
                   "EN_framed_Egypt_august_ten": _ten_stats(C["EN_framed_Egypt"], _sept_models, "sept|EN_framed_Egypt_august_ten")},
    "increments": {"template_minus_unframed": round(mean([_sept_bind["en_neutral_template"][m] - _sept_bind["en_neutral_sept"][m] for m in _sept_models]), 4),
                   "egypt_minus_template": round(mean([_sept_bind["EN_framed_Egypt_sept"][m] - _sept_bind["en_neutral_template"][m] for m in _sept_models]), 4),
                   "drift_unframed": round(mean([_sept_bind["en_neutral_sept"][m] - C["en_neutral"][m] for m in _sept_models]), 4),
                   "drift_framed_egypt": round(mean([_sept_bind["EN_framed_Egypt_sept"][m] - C["EN_framed_Egypt"][m] for m in _sept_models]), 4)},
}

out = {
    "september": september,
    "meta": {
        "collected": {g: "%s to %s" % (d["first"][:4] + "-" + d["first"][4:6] + "-" + d["first"][6:], d["last"][:4] + "-" + d["last"][4:6] + "-" + d["last"][6:])
                      if d["first"] != d["last"] else d["first"][:4] + "-" + d["first"][4:6] + "-" + d["first"][6:]
                      for g, d in RECORD["collected"].items()},
        "produced_by": "validity/build_viewer_data.py",
        "reads": "validity/results/mfq2_ratings.csv, validity/results/collection_record.json",
        "scored_cells": cells,
        "conditions": len(C),
        "models": len(ROSTER),
        "roster": ROSTER,
        "unit_of_analysis": "model; each model's iterations averaged before any test",
        "intervals": "percentile bootstrap, 100,000 draws resampling models, "
                     "seeded per quantity from seed %d" % SEED,
        "scale": [1, 5],
        "measure": "binding composite, the mean of Loyalty, Authority and Purity",
        "iran_anchor": iran_anchor(),
    },
    "countries": countries,
    "language_groups": groups,
    "models": models,
    "foundation_shifts": shifts,
    "language_contrasts": language_contrasts,
    "conditions_raw": {k: cond(k) for k in sorted(C)},
}
json.dump(out, sys.stdout, indent=1, sort_keys=False)
sys.stdout.write("\n")
