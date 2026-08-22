#!/usr/bin/env python3
"""Emit the appendix's data sections as markdown, straight from the raw cells.

The appendix used to carry numbers transcribed by hand, which is how it ended up
holding July's values after an August re-collection and how a prose figure came to
disagree with the table beside it. Everything here regenerates, so the document and
the artifact cannot drift apart.

Same conventions as validity/audit_inlanguage.py: the model is the independent unit,
iterations averaged first, bootstrap 100,000 draws resampling models with each interval
seeded from the run seed plus the quantity's own name.

    python3 validity/build_appendix_tables.py > validity/results/appendix_tables.md
"""
import json, glob, random
from pathlib import Path
from collections import defaultdict

VDIR = Path(__file__).resolve().parent
FOUND = ["care", "equality", "proportionality", "loyalty", "authority", "purity"]
BIND = ["loyalty", "authority", "purity"]
SEED = 20260723
B = 100_000

ANCH = {"Egypt": 4.267, "Saudi Arabia": 4.083, "Morocco": 4.014,
        "United Arab Emirates": 3.892, "Nigeria": 4.038, "Japan": 2.652, "Iran": 3.333}
ANCH_SRC = {c: "Atari 2023 Study 2" for c in ANCH}
ANCH_SRC["Iran"] = "Hazrati 2025 sample 2"

# country, language name, instrument code (None where no in-language arm was run)
ROWS = [("Egypt", "Arabic", "ar"), ("Morocco", "Arabic", "ar"),
        ("Saudi Arabia", "Arabic", "ar"), ("United Arab Emirates", "Arabic", "ar"),
        ("Japan", "Japanese", "ja"), ("Iran", "Farsi", "fa"),
        ("Nigeria", None, None), ("India", None, None),
        ("Sweden", None, None), ("United States", None, None)]


def fmeans(r):
    by = defaultdict(list)
    for iid, v in r.items():
        by[iid.rsplit("_", 1)[0]].append(v)
    return {g: sum(v) / len(v) for g, v in by.items()}


def binding(r):
    f = fmeans(r)
    return None if any(g not in f for g in FOUND) else sum(f[g] for g in BIND) / 3


def load(what):
    acc = defaultdict(lambda: defaultdict(list))
    src = [(VDIR / "runs_framed_lang" / "*.json",
            lambda d: "%s_%s" % (d["instrument"].split("_")[1],
                                 d["condition"] if d["condition"] != "framed"
                                 else "framed_" + d["country"])),
           (VDIR / "runs_framed" / "*_mfq2_*.json",
            lambda d: ("EN_framed_" + d["country"]) if d.get("country") else None),
           (VDIR / "runs" / "*_mfq2_*.json", lambda d: "en_neutral")]
    for pat, keyf in src:
        for f in glob.glob(str(pat)):
            d = json.load(open(f))
            if not d.get("ratings"):
                continue
            k = keyf(d)
            if k is None:
                continue
            if what == "binding":
                b = binding(d["ratings"])
                if b is not None:
                    acc[k][d["model"]].append(b)
            else:
                fm = fmeans(d["ratings"])
                if not any(g not in fm for g in FOUND):
                    acc[k][d["model"]].append(fm)
    if what == "binding":
        return {k: {m: sum(v) / len(v) for m, v in md.items()} for k, md in acc.items()}
    return {k: {m: {g: sum(x[g] for x in v) / len(v) for g in FOUND} for m, v in md.items()}
            for k, md in acc.items()}


C = load("binding")
F = load("found")


def mean(v):
    return sum(v) / len(v)


def boot(vals, key):
    rng = random.Random("%d|%s" % (SEED, key))
    n = len(vals)
    s = sorted(sum(vals[rng.randrange(n)] for _ in range(n)) / n for _ in range(B))
    return s[int(0.025 * B)], s[int(0.975 * B)]


def cell(k):
    if k not in C:
        return None
    return mean(list(C[k].values()))


def sd(k):
    v = list(C[k].values())
    m = mean(v)
    return (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5


EN = cell("en_neutral")

print("## B3. Where the panel lands, by country\n")
print("Binding composite, panel mean over eleven models, each model's five iterations "
      "averaged first. The English unframed column is one condition and repeats down the "
      "table; the unframed in-language column is one condition per language and repeats "
      "across the countries that share a language, because neither condition names a "
      "country. Dashes mark arms not run.\n")
print("| country | language | human | EN unframed | local unframed | EN framed | local framed |")
print("|---|---|--:|--:|--:|--:|--:|")
for country, lang, code in ROWS:
    h = "%.3f" % ANCH[country] if country in ANCH else "n/a"
    ln = cell(code + "_neutral") if code else None
    lf = cell(code + "_framed_" + country) if code else None
    ef = cell("EN_framed_" + country)
    print("| %s | %s | %s | %.3f | %s | %s | %s |" % (
        country, lang or "n/a", h, EN,
        "%.3f" % ln if ln is not None else "-",
        "%.3f" % ef if ef is not None else "-",
        "%.3f" % lf if lf is not None else "-"))

print("\nThe same table as distance from that country's measured human mean. Positive is "
      "above the population.\n")
print("| country | EN unframed | local unframed | EN framed | local framed |")
print("|---|--:|--:|--:|--:|")
for country, lang, code in ROWS:
    if country not in ANCH:
        continue
    a = ANCH[country]
    ln = cell(code + "_neutral") if code else None
    lf = cell(code + "_framed_" + country) if code else None
    ef = cell("EN_framed_" + country)
    print("| %s | %+.3f | %s | %s | %s |" % (
        country, EN - a,
        "%+.3f" % (ln - a) if ln is not None else "-",
        "%+.3f" % (ef - a) if ef is not None else "-",
        "%+.3f" % (lf - a) if lf is not None else "-"))

print("\nHuman anchors: %s. India, Sweden and the United States are not in the MFQ-2 "
      "nineteen-nation set, so no overshoot is computable for them.\n"
      % ", ".join("%s %.3f (%s)" % (c, ANCH[c], ANCH_SRC[c]) for c in
                  ["Egypt", "Saudi Arabia", "Morocco", "United Arab Emirates",
                   "Nigeria", "Japan", "Iran"]))

print("\n## B3a. Every condition, with intervals\n")
print("| condition | panel mean | 95% CI | between-model SD |")
print("|---|--:|:--:|--:|")
for k in sorted(C):
    lo, hi = boot(list(C[k].values()), k)
    print("| %s | %.3f | [%.3f, %.3f] | %.2f |" % (k, cell(k), lo, hi, sd(k)))

print("\n## B6. Per-foundation panel means\n")
print("| condition | Care | Equality | Proportionality | Loyalty | Authority | Purity |")
print("|---|--:|--:|--:|--:|--:|--:|")
for k in sorted(F):
    row = {g: mean([F[k][m][g] for m in F[k]]) for g in FOUND}
    print("| %s | %s |" % (k, " | ".join("%.2f" % row[g] for g in FOUND)))
