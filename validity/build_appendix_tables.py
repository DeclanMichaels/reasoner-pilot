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
ANCH_SE = {}   # reference-sample standard error of the binding mean, SD / sqrt(n)


def anchors():
    a, src = {}, {}
    with open(VDIR / "reference" / "mfq2_country_dispersion.csv") as fh:
        for r in csv.DictReader(fh):
            c = REF_NAME.get(r["country"], r["country"])
            ANCH_SE[c] = float(r["binding_sd"]) / int(r["n"]) ** 0.5
    with open(VDIR / "reference" / "mfq2_country_means.csv") as fh:
        for r in csv.DictReader(fh):
            c = REF_NAME.get(r["country"], r["country"])
            a[c] = sum(float(r[g]) for g in BIND) / 3   # full precision; rounded for display only
            src[c] = "Atari 2023 Study 2"
            ANCH_N[c] = int(r["n"])
    ir = json.load(open(VDIR / "anchors_iran.json"))
    a["Iran"] = ir["binding_1to5"]["s2"]
    src["Iran"] = "Hazrati 2025 sample 2"
    ANCH_SE["Iran"] = ir["person_level_sd"]["binding"]["s2"] / ir["person_level_sd"]["n_binding"]["s2"] ** 0.5
    return a, src


ANCH, ANCH_SRC = anchors()

LANG_NAME = {"ar": "Arabic", "es": "Spanish", "fr": "French",
             "ja": "Japanese", "fa": "Farsi", "ru": "Russian"}
LANG_ORDER = ["ar", "es", "fr", "ja", "fa", "ru", None]

# Decision 18, superseding 12's grouping clause. Atari et al. administered Morocco's sample in
# Spanish, so Morocco is reported under Spanish in every view and compared on the Spanish arm.
# The Arabic-framed cells stay in the data (B3a, B6, B4's within-Arabic block) and enter no
# comparison against the human mean. A country appearing in two in-language arms and listed in
# neither map is an error, not a default: raise rather than silently pick one.
GROUP_ARM = {"Morocco": "es"}
ANCHOR_ARM = {"Morocco": "es"}
MARK = {"Morocco": " [d18]", "Iran": " [*]"}


def fmeans(r):
    by = defaultdict(list)
    for iid, v in r.items():
        by[iid.rsplit("_", 1)[0]].append(v)
    return {g: sum(v) / len(v) for g, v in by.items()}


def binding(r):
    f = fmeans(r)
    return None if any(g not in f for g in FOUND) else sum(f[g] for g in BIND) / 3


import sys as _sys
_sys.path.insert(0, str(VDIR))
from ratings_dataset import load_cells
# The published ratings dataset (decision 19) is the only ratings source (#71). The September
# wave's three conditions are B4a's and stay out of the grid tables.
_SEPT = {"en_neutral_template", "en_neutral_sept", "EN_framed_Egypt_sept"}
CELLS = {k: v for k, v in load_cells().items() if k not in _SEPT}


def _cells():
    for k, md in CELLS.items():
        for m, cells in md.items():
            for c in cells:
                yield k, m, c["ratings"]


def load_items():
    """Per condition, per model: mean endpoint share (ratings at 1 or 5) and per-item means.
    B6a reads these; nothing else does."""
    end = defaultdict(lambda: defaultdict(list))
    items = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    runsd = defaultdict(lambda: defaultdict(list))   # per condition, per model: binding per run
    for k, m, r in _cells():
            b = binding(r)
            if b is not None:
                runsd[k][m].append(b)
            end[k][m].append(sum(1 for v in r.values() if v in (1, 5)) / len(r))
            for iid, v in r.items():
                items[k][m][iid].append(v)
    return ({k: {m: mean(v) for m, v in md.items()} for k, md in end.items()},
            {k: {m: {i: mean(v) for i, v in mi.items()} for m, mi in md.items()} for k, md in items.items()},
            {k: {m: v for m, v in md.items()} for k, md in runsd.items()})


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
    for k, m, r in _cells():
            if what == "binding":
                b = binding(r)
                if b is not None:
                    acc[k][m].append(b)
            else:
                fm = fmeans(r)
                if not any(g not in fm for g in FOUND):
                    acc[k][m].append(fm)
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

print("## B2a. Measurement invariance across the nineteen\n")
print("Comparing raw composite means across countries needs the instrument to behave the same "
      "way in each. Atari et al. checked this with Muthen-Asparouhov alignment on their Study 2 "
      "data and report the result in their Table 6: a loadings R-squared and an intercepts "
      "R-squared per foundation, and the percentage of item parameters the alignment left "
      "non-invariant, against the 25 percent that Muthen and Asparouhov (2014) treat as "
      "acceptable. We recomputed the R-squared values on the same raw data in `reasoner-study` "
      "(`compute_alignment_r2.R`: sirt 3.13-228, `invariance.alignment`, align.scale c(.2, .4), "
      "align.pow c(.25, .25), lavaan) and show them beside the published ones; the percentages are Atari et al.'s, transcribed and not recomputed. Loadings R-squared concerns loading "
      "(metric) invariance, intercepts R-squared concerns intercept (scalar) invariance, the one "
      "that bears on comparing means. Neither establishes exact invariance. "
      "This is a property of the nineteen human samples. It says nothing about whether a model's "
      "score and a person's score measure the same thing, and nothing in this appendix claims "
      "they do.\n")
print("| foundation | loadings R-squared, published / recomputed | intercepts R-squared, published / recomputed | non-invariant loadings | non-invariant intercepts |")
print("|---|:--:|:--:|--:|--:|")
with open(VDIR / "reference" / "mfq2_alignment_r2.csv") as fh:
    _al = {r["foundation"]: r for r in csv.DictReader(fh)}
with open(VDIR / "reference" / "mfq2_alignment_table6_published.csv") as fh:
    _pub = list(csv.DictReader(fh))
_maxdiff = 0.0
for r in _pub:
    a = _al[r["foundation"]]
    _maxdiff = max(_maxdiff, abs(float(a["R2_loadings"]) - float(r["published_R2_loadings"])),
                   abs(float(a["R2_intercepts"]) - float(r["published_R2_intercepts"])))
    print("| %s | %.3f / %.4f | %.3f / %.4f | %.1f%% | %.1f%% |" % (
        r["foundation"].capitalize(), float(r["published_R2_loadings"]), float(a["R2_loadings"]),
        float(r["published_R2_intercepts"]), float(a["R2_intercepts"]),
        float(r["pct_noninvariant_loadings"]), float(r["pct_noninvariant_intercepts"])))
_over = [r for r in _pub if float(r["pct_noninvariant_intercepts"]) > 25 or float(r["pct_noninvariant_loadings"]) > 25]
assert [r["foundation"] for r in _over] == ["purity"], _over
print("\nEvery recomputed R-squared is within %.4f of the published one; the recomputation used Atari et al.'s shared data and the pinned sirt 3.13-228, and the residual is not traced. Purity is the one "
      "foundation over the 25 percent line, at %.1f percent of intercept parameters, and Atari et al. write that caution should be practiced when comparing Purity group-level means; they trace "
      "most of it to unique intercepts in Argentina and Chile and to one item. Purity is one third "
      "of the binding composite and carries its largest framing shift, so every composite comparison "
      "in this appendix inherits that caution. B6 gives each foundation separately, and the report "
      "gives the Loyalty and Authority shifts on their own.\n" % (_maxdiff, float(_over[0]["pct_noninvariant_intercepts"])))
print("## B3. Where the panel lands, by country\n")
print("Binding composite, panel mean over eleven models, each model's five iterations "
      "averaged first. The English unframed column is one condition and repeats down the "
      "table; the unframed in-language column is one condition per language and repeats "
      "across the countries that share a language, because neither condition names a "
      "country. Dashes mark arms not run. Morocco's local cells are the Spanish arm in both tables, "
      "decision 18; its Arabic-framed cells appear in B3a, B6 and B4.\n")
print("| country | language | human | human SE | EN unframed | local unframed | EN framed | local framed |")
print("|---|---|--:|--:|--:|--:|--:|--:|")


def arm(country, code, value):
    """Label the local-arm cell where a country has two arms (decision 18)."""
    if value is None:
        return "-"
    return "%.3f%s" % (value, " (%s arm)" % LANG_NAME[code] if country in ANCHOR_ARM else "")


for country, lang, code in ROWS:
    h = "%.3f" % ANCH[country] if country in ANCH else "n/a"
    se = "%.3f" % ANCH_SE[country] if country in ANCH_SE else "n/a"
    ln = cell(code + "_neutral") if code else None
    lf = cell(code + "_framed_" + country) if code else None
    ef = cell("EN_framed_" + country)
    print("| %s | %s | %s | %s | %.3f | %s | %s | %s |" % (
        country + MARK.get(country, ""), lang or "n/a", h, se, EN,
        arm(country, code, ln),
        "%.3f" % ef if ef is not None else "-",
        arm(country, code, lf)))

print("\nThe same table as distance from that country's reference-sample mean. Positive is "
      "above it.\n")
print("| country | EN unframed | local unframed | EN framed | local framed |")
print("|---|--:|--:|--:|--:|")
for country, lang, code in ROWS:
    if country not in ANCH:
        continue
    a = ANCH[country]
    code = ANCHOR_ARM.get(country, code)   # decision 18
    ln = cell(code + "_neutral") if code else None
    lf = cell(code + "_framed_" + country) if code else None
    ef = cell("EN_framed_" + country)
    def darm(v):
        if v is None:
            return "-"
        return "%+.3f%s" % (v - a, " (%s arm)" % LANG_NAME[code] if country in ANCHOR_ARM else "")
    print("| %s | %+.3f | %s | %s | %s |" % (
        country + MARK.get(country, ""), EN - a, darm(ln),
        "%+.3f" % (ef - a) if ef is not None else "-", darm(lf)))

ARTICLE = {"United States": "the United States"}
UNANCHORED = [ARTICLE.get(c, c) for c, _, _ in ROWS if c not in ANCH]
_ns = sorted(ANCH_N.values())
print("\nEach of those nineteen means rests on %d to %d respondents for its country, %s in all, "
      "collected by Atari et al. in May 2021 through Qualtrics Panels and stratified within "
      "each nation on age, gender and political orientation. Education was not a "
      "stratification variable, and Atari et al. state their results rest on \"a subset of "
      "these populations who were educated enough to complete the surveys online\", noting "
      "that people from traditional, small-scale communities are absent. Every overshoot in "
      "this appendix is a distance from those samples' means.\n"
      % (_ns[0], _ns[-1], format(sum(_ns), ",")))
_ses = sorted(v for c, v in ANCH_SE.items() if c != "Iran")
print("The human SE column is SD over root n from the per-country dispersion file, %.3f to %.3f "
      "across the nineteen: a standard error under an independent-respondent approximation. The "
      "stratified recruitment does not by itself justify a design-based population SE. It is a "
      "different quantity from the model-resampling interval in B3a, which "
      "describes panel composition, and neither one removes selection in who was sampled. Iran's "
      "comes from Hazrati et al.'s shared respondent-level files, sample 2, %d respondents, over "
      "their own composite scores, binding SD %.3f.\n" % (_ses[0], _ses[-1],
      json.load(open(VDIR / "anchors_iran.json"))["person_level_sd"]["n_binding"]["s2"],
      json.load(open(VDIR / "anchors_iran.json"))["person_level_sd"]["binding"]["s2"]))
print("[*] Iran's anchor is the only one not drawn from Atari et al. (2023) Study 2. B4 "
      "carries the source, the sample's own caveats and the sensitivity across every anchor "
      "that source offers.\n")
print("[d18] Morocco: reported under Spanish, the language Atari et al. administered its sample "
      "in, and compared on the Spanish arm. We also ran an Arabic-framed arm; its cells are in "
      "B3a, B6 and B4 and enter no comparison against the human mean.\n")
print("Human anchors, treated as constants, binding as the mean of loyalty, authority and "
      "purity: %s. %s %s not in the MFQ-2 nineteen-nation set, so no overshoot is "
      "computable for %s. Hazrati et al. administered Iran's sample on a 0-4 scale and we shift it linearly by +1 for comparability with the 1-5 runs; anchors_iran.json carries the "
      "detail and the caveats.\n"
      % (", ".join("%s %.3f (%s)" % (c, ANCH[c], ANCH_SRC[c])
                   for c, _, _ in ROWS if c in ANCH),
         ", ".join(UNANCHORED[:-1]) + " and " + UNANCHORED[-1],
         "is" if len(UNANCHORED) == 1 else "are",
         "it" if len(UNANCHORED) == 1 else "them"))


# ---- Loyalty and Authority alone, against the reference samples (#109)
def _la_anchor():
    """Reference-sample mean and respondent-level SD of the Loyalty-Authority composite, from the
    same sources as ANCH: the means file and the dispersion file for the nineteen, Hazrati et al.'s
    sample 2 via mfq2_iran_dispersion.csv for Iran (#113)."""
    a, s = {}, {}
    with open(VDIR / "reference" / "mfq2_country_means.csv") as fh:
        for r in csv.DictReader(fh):
            a[REF_NAME.get(r["country"], r["country"])] = (float(r["loyalty"]) + float(r["authority"])) / 2
    with open(VDIR / "reference" / "mfq2_country_dispersion.csv") as fh:
        for r in csv.DictReader(fh):
            s[REF_NAME.get(r["country"], r["country"])] = float(r["loyalty_authority_sd"])
    ir = json.load(open(VDIR / "anchors_iran.json"))["means_1to5"]
    a["Iran"] = (ir["loyalty"]["s2"] + ir["authority"]["s2"]) / 2
    with open(VDIR / "reference" / "mfq2_iran_dispersion.csv") as fh:
        s["Iran"] = [float(r["loyalty_authority_sd"]) for r in csv.DictReader(fh) if r["sample"] == "s2"][0]
    assert set(a) == set(s), sorted(set(a) ^ set(s))
    return a, s


def _la_cell(k):
    return mean([(F[k][m]["loyalty"] + F[k][m]["authority"]) / 2 for m in sorted(F[k])])


_LA, _LA_SD = _la_anchor()
_la_rows = sorted(((c, _LA[c], _la_cell("EN_framed_" + c)) for c, _, _ in ROWS if c in ANCH),
                  key=lambda r: r[2] - r[1])
_la_above = [c for c, h, pm in _la_rows if pm - h > 0]
_bd_above = [c for c, _, _ in ROWS if c in ANCH and cell("EN_framed_" + c) - ANCH[c] > 0]
_la_flip = sorted(set(_la_above) ^ set(_bd_above))
print("**Loyalty and Authority alone.** The English-framed comparison again, leaving out Purity, "
      "the foundation Atari et al. flag (B2a): the panel's mean of Loyalty and Authority against "
      "each reference sample's, the human figure the mean of the two published foundation means, "
      "Iran's from Hazrati et al. The last column divides the difference by that country's "
      "respondent-level standard deviation of the same two-foundation composite, computed over "
      "respondents the way the binding SD is (B9). Ordered by difference.\n")
print("| country | human | human SD | panel, EN framed | difference | d |")
print("|---|--:|--:|--:|--:|--:|")
for c, h, pm in _la_rows:
    print("| %s | %.3f | %.3f | %.3f | %+.3f | %+.2f |" % (c + MARK.get(c, ""), h, _LA_SD[c], pm, pm - h, (pm - h) / _LA_SD[c]))


def _rho(a, b):
    ra = {k: i for i, k in enumerate(sorted(a, key=a.get))}
    rb = {k: i for i, k in enumerate(sorted(b, key=b.get))}
    n = len(a)
    return 1 - 6 * sum((ra[k] - rb[k]) ** 2 for k in a) / (n * (n * n - 1))


_es = {c for c, _, code in ROWS if ANCHOR_ARM.get(c, code) == "es" and c in ANCH}
_es_p = {c: _la_cell("es_framed_" + c) for c in sorted(_es)}
_es_h = {c: _LA[c] for c in sorted(_es)}
_ar = ["Egypt", "Saudi Arabia", "United Arab Emirates"]
_ar_p = sorted(_ar, key=lambda c: -_la_cell("ar_framed_" + c))
_ar_h = sorted(_ar, key=lambda c: -_LA[c])
_fr = ["Belgium", "France", "Switzerland"]
_fr_p = sorted(_fr, key=lambda c: -_la_cell("fr_framed_" + c))
_fr_h = sorted(_fr, key=lambda c: -_LA[c])
print("\nOn Loyalty and Authority the panel sits above the reference sample in %d countries and at "
      "or below it in %d; against the composite, the sign changes for %s and for no other country. "
      "Framed in the local language, the Spanish six rank with rho %+.2f against the reference "
      "order, %+.2f on the composite; the Arabic panel order is %s against a reference order of "
      "%s, and the French %s against %s.\n"
      % (len(_la_above), len(_la_rows) - len(_la_above),
         " and ".join(_la_flip) if _la_flip else "no country",
         _rho(_es_p, _es_h), _rho({c: cell("es_framed_" + c) for c in _es}, {c: ANCH[c] for c in _es}),
         ", ".join(_ar_p), ", ".join(_ar_h), ", ".join(_fr_p), ", ".join(_fr_h)))

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
      "countries, in the country order of B3. The measured rows are reference samples, not "
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


# ---- B6a: the dispersion finding taken apart, by foundation and against the ceiling
END, ITEMS, RUNS = load_items()
UNF = ["en_neutral"] + [c + "_neutral" for c in ["ar", "es", "fr", "ja", "fa", "ru"]]
FRM = sorted(k for k in C if "_framed_" in k)


def psd(vals):
    m = mean(vals)
    return (sum((x - m) ** 2 for x in vals) / len(vals)) ** 0.5


def fsd(k, g):
    return psd([F[k][m][g] for m in F[k]])


def median(v):
    v = sorted(v); n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


print("\n## B6a. The dispersion finding, by foundation and against the ceiling\n")
print("The between-model spread in B3a is on the binding composite. This section takes it apart. "
      "Spread is the population standard deviation of the %d model means, the median over the %d "
      "unframed conditions against the median over the %d framed ones, per foundation; the last "
      "column counts framed conditions whose spread is below every unframed condition's.\n"
      % (len(C["en_neutral"]), len(UNF), len(FRM)))
print("| foundation | unframed | framed | framed / unframed | framed tighter than every unframed |")
print("|---|--:|--:|--:|--:|")
for g in FOUND:
    u = median([fsd(k, g) for k in UNF]); f = median([fsd(k, g) for k in FRM]); mu = min(fsd(k, g) for k in UNF)
    print("| %s | %.3f | %.3f | %.2f | %d of %d |" % (g.capitalize(), u, f, f / u, sum(fsd(k, g) < mu for k in FRM), len(FRM)))
_eu = median([mean(END[k].values()) for k in UNF]); _ef = median([mean(END[k].values()) for k in FRM])
_isd = lambda k: median([psd([ITEMS[k][m][i] for m in ITEMS[k]]) for i in next(iter(ITEMS[k].values()))])
_iu = median([_isd(k) for k in UNF]); _if = median([_isd(k) for k in FRM])
print("\nEndpoint use, the share of item ratings at 1 or 5, panel mean and then the median over "
      "conditions: %.3f unframed, %.3f framed. Item-level between-model spread, the same statistic "
      "on each of the 36 items and then the median: %.3f unframed, %.3f framed.\n" % (_eu, _ef, _iu, _if))
_wu = median([psd(v) for k in UNF for v in RUNS[k].values() if len(v) > 1])
_wf = median([psd(v) for k in FRM for v in RUNS[k].values() if len(v) > 1])
assert set(C) <= set(RUNS), sorted(set(C) - set(RUNS))
_wa = median([psd(v) for k in C for v in RUNS[k].values() if len(v) > 1])
_na = sum(len(RUNS[k]) for k in C)
_ba = median([sd(k) for k in C])
def _svar(v):
    m = mean(v)
    return sum((x - m) ** 2 for x in v) / (len(v) - 1)
def _decomp(k):
    """between-model variance of the five-run means, the run-noise share of it (mean within-model
    variance over five, assuming independent runs), and the noise-corrected between-model SD."""
    vb = sd(k) ** 2
    n = len(RUNS[k])
    vw = (n - 1) / n * mean([_svar(v) for v in RUNS[k].values() if len(v) > 1]) / 5   # noise share of a population variance over n means
    return vb, vw, max(vb - vw, 0.0) ** 0.5
_du = [_decomp(k) for k in UNF]; _df = [_decomp(k) for k in FRM]
_minc = min(x[2] for x in _du)
print("Within a model, the five-run spread of the binding composite has a median of %.3f in the "
      "unframed conditions and %.3f in the framed ones, and %.3f over all %d model-by-condition cells; "
      "the between-model spread has a median of %.3f over all %d conditions. Taking run noise out "
      "condition by condition, under independence of a model's runs, by subtracting the mean within-model variance over five, scaled by (n-1)/n for a population variance over n model means, from the between-model variance of the five-run means: the estimated noise-adjusted between-model SD, truncated at zero, has a median of %.3f in the unframed conditions and %.3f in the framed ones, run noise is a median %.0f and %.0f percent of the between-model variance, and %d of %d framed conditions sit below every unframed one on the adjusted SD as well. Whatever default sampling "
      "temperature each provider applied, we assume the same default applied to a model's framed and unframed conditions, collected in one window.\n" % (
      _wu, _wf, _wa, _na, _ba, len(C), median([x[2] for x in _du]), median([x[2] for x in _df]),
      100 * median([x[1] / x[0] for x in _du]), 100 * median([x[1] / x[0] for x in _df]),
      sum(1 for x in _df if x[2] < _minc), len(FRM)))
print("Restricting the framed set by its distance from the top of the scale, against the same "
      "%d unframed conditions, whose binding means run %.2f to %.2f:\n"
      % (len(UNF), min(cell(k) for k in UNF), max(cell(k) for k in UNF)))
print("| framed conditions with binding mean below | conditions | tighter than every unframed | median spread |")
print("|---|--:|--:|--:|")
_minu = min(sd(k) for k in UNF)
for thr in [5.0, 4.5, 4.0, 3.5]:
    sub_ = [k for k in FRM if cell(k) < thr]
    print("| %.1f | %d | %d | %.3f |" % (thr, len(sub_), sum(sd(k) < _minu for k in sub_), median([sd(k) for k in sub_])))

print("\n**The unframed language contrasts by foundation.** Each translated unframed condition minus "
      "the English unframed one, panel means, so the composite rows of B4 can be read in their parts. "
      "The last column is the mean over models of the absolute within-model change in the binding "
      "composite, the movement a panel-level shift near zero can hide.\n")
print("| language | Care | Equality | Proportionality | Loyalty | Authority | Purity | binding | mean abs. within-model binding change |")
print("|---|--:|--:|--:|--:|--:|--:|--:|--:|")
for code in ["ar", "es", "fr", "ja", "fa", "ru"]:
    k = code + "_neutral"
    d = {g: mean([F[k][m][g] for m in F[k]]) - mean([F["en_neutral"][m][g] for m in F["en_neutral"]]) for g in FOUND}
    _wabs = mean([abs(mean(RUNS[k][m]) - mean(RUNS["en_neutral"][m])) for m in RUNS[k]])
    print("| %s | %s | %+.2f | %.2f |" % (LANG_NAME[code], " | ".join("%+.2f" % d[g] for g in FOUND),
                                          sum(d[g] for g in BIND) / 3, _wabs))

# ---- a system prompt without a country, and the spread (#73)
_sp = {k: sd(k) for k in ("en_neutral", "en_baseline_official_selfreport",
                          "en_baseline_ours_nosystem", "en_baseline_ours_selfreport")}
_fmed = median([sd(k) for k in FRM]); _umed = median([sd(k) for k in UNF])
_spdrop = max(_sp["en_neutral"] - _sp["en_baseline_official_selfreport"],
              _sp["en_baseline_ours_nosystem"] - _sp["en_baseline_ours_selfreport"])
print("\n**A self-report system prompt without a country.** The four English unframed variants, none of which names a country, separate the presence of a self-report system prompt from its absence, across the two questionnaire files. Between-model SD is %.2f with no system prompt and %.2f with the self-report prompt on the official file, %.2f and %.2f on our transcription, against a median of %.3f across the 39 framed conditions. The self-report prompt moves the spread by at most %.2f, while the framing conditions sit %.2f below the unframed median; the country-free framing template in B4a moves it by about 0.17 in the September check, so the content of a country-free instruction, not the presence of one, is what separates the two.\n" % (
      _sp["en_neutral"], _sp["en_baseline_official_selfreport"], _sp["en_baseline_ours_nosystem"],
      _sp["en_baseline_ours_selfreport"], _fmed, _spdrop, _umed - _fmed))

# ---- floor (#78)
_pur_en = mean([F["en_neutral"][m]["purity"] for m in F["en_neutral"]])
_pur_usd = median([fsd(k, "purity") for k in UNF])
print("A floor would work the other way. Unframed English Purity sits at %.2f on a scale that starts at 1 "
      "and Purity has the largest unframed between-model spread of any foundation, a median of %.3f, so "
      "a floor compressing it would shrink the unframed spread, which is the larger one, not the framed.\n"
      % (_pur_en, _pur_usd))

# ---- framing by language, binding and Loyalty-Authority (#79)
_groups = {}
for _country, _lang, _code in ROWS:
    if _code and (_code + "_framed_" + _country) in C:
        _groups.setdefault(_code, []).append(_country)
def _pf(k, gs):
    return mean([mean([F[k][m][g] for g in gs]) for m in F[k]])
print("**Framing by language, on the binding composite and on Loyalty and Authority alone.** "
      "In-language framed minus in-language unframed, panel means, averaged over the language's "
      "countries with Morocco under Spanish (decision 18); the last row averages the six languages "
      "with equal weight. The Loyalty-Authority column leaves out Purity, the foundation whose "
      "intercepts Atari et al. flag (B2a).\n")
print("| language | countries | binding | Loyalty-Authority |")
print("|---|--:|--:|--:|")
_rb, _rla = [], []
for code in ["ar", "es", "fr", "ja", "fa", "ru"]:
    cs = _groups[code]; nk = code + "_neutral"
    b = mean([cell(code + "_framed_" + c) - cell(nk) for c in cs])
    la = mean([_pf(code + "_framed_" + c, ["loyalty", "authority"]) - _pf(nk, ["loyalty", "authority"]) for c in cs])
    _rb.append(b); _rla.append(la)
    print("| %s | %d | %+.3f | %+.3f |" % (LANG_NAME[code], len(cs), b, la))
print("| six languages, equal weight | %d | %+.3f | %+.3f |" % (sum(len(_groups[c]) for c in _groups), mean(_rb), mean(_rla)))

# ---- the Arabic unframed shift, item by item (#80)
_ia, _ie = ITEMS["ar_neutral"], ITEMS["en_neutral"]
_ms = sorted(set(_ia) & set(_ie))
_iids = sorted(next(iter(_ia.values())), key=lambda i: (FOUND.index(i.rsplit("_", 1)[0]), int(i.rsplit("_", 1)[1])))
_shift = {i: mean([_ia[m][i] for m in _ms]) - mean([_ie[m][i] for m in _ms]) for i in _iids}
_up = {i: sum(1 for m in _ms if _ia[m][i] > _ie[m][i]) for i in _iids}
print("\n**The Arabic unframed shift, item by item.** Arabic unframed minus English unframed, panel mean "
      "per item, with the number of the eleven models whose own mean moved up. Item names give foundation and position in the official key; we do not reproduce wording (decision 7).\n")
print("| item | shift | models up (of %d) |" % len(_ms))
print("|---|--:|--:|")
for i in _iids:
    print("| %s | %+.2f | %d |" % (i, _shift[i], _up[i]))
_n25 = sum(1 for v in _shift.values() if abs(v) > 0.25); _n50 = [i for i, v in _shift.items() if abs(v) > 0.5]
_bind_up = sum(1 for i in _iids if i.rsplit("_", 1)[0] in BIND and _shift[i] > 0)
_eq = [_shift[i] for i in _iids if i.startswith("equality_")]; _care = max(abs(_shift[i]) for i in _iids if i.startswith("care_"))
print("\n%d of 36 items move by more than 0.25 and %d by more than 0.5 (%s); %d of the 18 binding items "
      "move up, and so do all six Equality items, by %+.2f to %+.2f; the six Care items sit within %.2f "
      "of their English values.\n" % (_n25, len(_n50), ", ".join(_n50), _bind_up, min(_eq), max(_eq), _care))
