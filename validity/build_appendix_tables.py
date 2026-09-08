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
import csv, json, glob, random
from pathlib import Path
from collections import defaultdict

VDIR = Path(__file__).resolve().parent
FOUND = ["care", "equality", "proportionality", "loyalty", "authority", "purity"]
BIND = ["loyalty", "authority", "purity"]
SEED = 20260723
B = 100_000

# Human anchors, computed rather than transcribed. The nineteen-nation set comes from
# Atari et al. (2023) Study 2 via reference/mfq2_country_means.csv; Iran is not in that set
# and comes from anchors_iran.json. Binding is the mean of loyalty, authority and purity.
# Rounded to three decimals, the precision the appendix has always carried them at: the
# unrounded means would move published overshoots in the third decimal for no gain.
REF_NAME = {"Columbia": "Colombia", "UAE": "United Arab Emirates"}


ANCH_N = {}


def anchors():
    a, src = {}, {}
    with open(VDIR / "reference" / "mfq2_country_means.csv") as fh:
        for r in csv.DictReader(fh):
            c = REF_NAME.get(r["country"], r["country"])
            a[c] = round(sum(float(r[g]) for g in BIND) / 3, 3)
            src[c] = "Atari 2023 Study 2"
            ANCH_N[c] = int(r["n"])
    ir = json.load(open(VDIR / "anchors_iran.json"))
    a["Iran"] = ir["binding_1to5"]["s2"]
    src["Iran"] = "Hazrati 2025 sample 2"
    return a, src


ANCH, ANCH_SRC = anchors()

LANG_NAME = {"ar": "Arabic", "es": "Spanish", "fr": "French",
             "ja": "Japanese", "fa": "Farsi", "ru": "Russian"}
LANG_ORDER = ["ar", "es", "fr", "ja", "fa", "ru", None]

# Decision 12. Morocco was administered in Spanish by Atari et al. though its majority
# language is Arabic, so the anchor comparison uses the Spanish arm while the country stays
# in the Arabic group for the ordering and foundation-shift views. Both runs are carried.
# A country appearing in two in-language arms and listed in neither map is an error, not a
# default: raise rather than silently pick one.
GROUP_ARM = {"Morocco": "ar"}
ANCHOR_ARM = {"Morocco": "es"}
MARK = {"Morocco": " [d12]", "Iran": " [*]"}


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
    # ENGLISH UNFRAMED, changed 2026-08-22. This used to be our own transcription of the
    # MFQ-2 administered with run_validity.py's self-report system prompt, while every
    # in-language unframed arm used the official Atari et al. translation with NO system
    # prompt: the comparator differed from what it was compared against in two ways at once.
    # Both were measured (results/english_baseline_audit.txt): instrument -0.038 p=.47,
    # system prompt +0.026 p=.49, neither distinguishable from zero. The official no-system
    # cell is the baseline now because it is the matched one. The old cell is kept under
    # en_neutral_ours so the errata can cite what was published before.
    src = [(VDIR / "runs_framed_lang" / "*.json",
            lambda d: "%s_%s" % (d["instrument"].split("_")[1],
                                 d["condition"] if d["condition"] != "framed"
                                 else "framed_" + d["country"])),
           (VDIR / "runs_framed" / "*_mfq2_*.json",
            lambda d: ("EN_framed_" + d["country"]) if d.get("country") else None),
           (VDIR / "runs_english_baseline" / "*.json",
            lambda d: "en_neutral" if d["condition"] == "official_nosystem"
            else "en_baseline_" + d["condition"]),
           (VDIR / "runs" / "*_mfq2_*.json", lambda d: "en_neutral_ours")]
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


def build_rows():
    """country, language name, instrument code - derived from the conditions present."""
    out = []
    for c in sorted(k[len("EN_framed_"):] for k in C if k.startswith("EN_framed_")):
        arms = [code for code in LANG_ORDER[:-1] if (code + "_framed_" + c) in C]
        if len(arms) > 1:
            code = GROUP_ARM.get(c)
            if code not in arms:
                raise SystemExit("%s has arms %s and no GROUP_ARM entry" % (c, arms))
        else:
            code = arms[0] if arms else None
        out.append((c, LANG_NAME.get(code), code))
    return sorted(out, key=lambda r: (LANG_ORDER.index(r[2]), r[0]))


ROWS = build_rows()


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
        country + MARK.get(country, ""), lang or "n/a", h, EN,
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
    code = ANCHOR_ARM.get(country, code)   # decision 12
    ln = cell(code + "_neutral") if code else None
    lf = cell(code + "_framed_" + country) if code else None
    ef = cell("EN_framed_" + country)
    print("| %s | %+.3f | %s | %s | %s |" % (
        country + MARK.get(country, ""), EN - a,
        "%+.3f" % (ln - a) if ln is not None else "-",
        "%+.3f" % (ef - a) if ef is not None else "-",
        "%+.3f" % (lf - a) if lf is not None else "-"))

ARTICLE = {"United States": "the United States"}
UNANCHORED = [ARTICLE.get(c, c) for c, _, _ in ROWS if c not in ANCH]
_ns = sorted(ANCH_N.values())
print("Each of those nineteen means rests on %d to %d respondents for its country, %s in all, "
      "collected by Atari et al. in May 2021 through Qualtrics Panels and stratified within "
      "each nation on age, gender and political orientation. Education was not a "
      "stratification variable, and the authors state their results rest on \"a subset of "
      "these populations who were educated enough to complete the surveys online\", noting "
      "that people from traditional, small-scale communities are absent. Every overshoot in "
      "this appendix is a distance from those samples' means.\n"
      % (_ns[0], _ns[-1], format(sum(_ns), ",")))
print("[*] Iran's anchor is the only one not drawn from Atari et al. (2023) Study 2. B4 "
      "carries the source, the sample's own caveats and the sensitivity across every anchor "
      "that source offers.\n")
print("[d12] Morocco: grouped with Arabic above, compared against its human mean on the "
      "Spanish arm, because Atari et al. administered Morocco's sample in Spanish. Both "
      "runs are carried in the data.\n")
print("Human anchors, treated as constants, binding as the mean of loyalty, authority and "
      "purity: %s. %s %s not in the MFQ-2 nineteen-nation set, so no overshoot is "
      "computable for %s. Iran's sample was administered on a 0-4 scale and shifted "
      "linearly by +1 for comparability with the 1-5 runs; anchors_iran.json carries the "
      "detail and the caveats.\n"
      % (", ".join("%s %.3f (%s)" % (c, ANCH[c], ANCH_SRC[c])
                   for c, _, _ in ROWS if c in ANCH),
         ", ".join(UNANCHORED[:-1]) + " and " + UNANCHORED[-1],
         "is" if len(UNANCHORED) == 1 else "are",
         "it" if len(UNANCHORED) == 1 else "them"))

print("\n## B3a. Every condition, with intervals\n")
print("| condition | panel mean | 95% model-resampling interval | between-model SD |")
print("|---|--:|:--:|--:|")
for k in sorted(C):
    lo, hi = boot(list(C[k].values()), k)
    print("| %s | %.3f | [%.3f, %.3f] | %.2f |" % (k, cell(k), lo, hi, sd(k)))

def measured():
    """Per-foundation human means for the twenty anchored countries, same sources as ANCH."""
    ref = {}
    with open(VDIR / "reference" / "mfq2_country_means.csv") as fh:
        for r in csv.DictReader(fh):
            ref[REF_NAME.get(r["country"], r["country"])] = {g: float(r[g]) for g in FOUND}
    ir = json.load(open(VDIR / "anchors_iran.json"))["means_1to5"]
    ref["Iran"] = {g: ir[g]["s2"] for g in FOUND}
    return ref


print("\n## B6. Per-foundation panel means\n")
print("All fifty conditions, then the measured human mean for each of the twenty anchored "
      "countries, in the country order of B3. The measured rows are populations, not "
      "conditions; they are here to be read against the panel rows above.\n")
print("| condition | Care | Equality | Proportionality | Loyalty | Authority | Purity |")
print("|---|--:|--:|--:|--:|--:|--:|")
for k in sorted(F):
    row = {g: mean([F[k][m][g] for m in F[k]]) for g in FOUND}
    print("| %s | %s |" % (k, " | ".join("%.2f" % row[g] for g in FOUND)))
REF = measured()
for country, _, _ in ROWS:
    if country not in REF:
        continue
    print("| **%s, measured**%s | %s |" % (
        country, MARK.get(country, ""),
        " | ".join("%.2f" % REF[country][g] for g in FOUND)))
