#!/usr/bin/env python3
"""Post-hoc statistical audit of the in-language MFQ-2 study. Stdlib only.

Independent unit: MODEL (11 clusters). All tests aggregate per model first.
- Bootstrap CIs (resample models, 100k, seed 20260723) on each condition's panel mean.
- Exact sign-flip permutation tests (2^11 = 2048 enumerations) on paired per-model
  differences and one-sample-vs-anchor differences.
- Leave-one-model-out sweeps on the two headline quantities.
- Holm correction within each family.

TWO FAMILIES, one per headline claim.
  Family A (T1-T10): the framing claim. Declared and reported in appendix B4; the
    values here are unchanged from the version that produced that table.
  Family B (T5, T6, T11): the language claim. One test per language, asking whether
    the local-language unframed condition departs from the English default. Added
    2026-08-21, after the results were seen, because the declared family omitted the
    Japanese case and so contained no complete test of the claim the title makes.
    T5 and T6 belong to both families; that double membership is disclosed rather
    than resolved by re-partitioning A, since re-cutting a declared family after
    seeing results is the larger sin and every conclusion holds under both cuts.

Verification pass: raw per-model descriptives printed first; panel means must
reconcile with analyze_lang.py's reported values before anything else is trusted.
    python3 validity/audit_inlanguage.py
"""
import json, glob, random, itertools
from pathlib import Path
from collections import defaultdict

VDIR = Path(__file__).resolve().parent
FOUND = ["care","equality","proportionality","loyalty","authority","purity"]
BIND = ["loyalty","authority","purity"]
# Anchors carried at the precision of their sources. Egypt and Japan from Atari et al.
# (2023) Study 2 via the reasoner-study reference build; Iran from Hazrati et al. (2025)
# sample 2, per anchors_iran.json. The appendix previously rounded these to two decimals
# here and used three elsewhere, so two of its own tables disagreed by a thousandth.
ANCH = {"Egypt": 4.267, "Japan": 2.652, "Iran": 3.333}
SEED = 20260723
B = 100_000

def fmeans(ratings):
    by = defaultdict(list)
    for iid,v in ratings.items(): by[iid.rsplit("_",1)[0]].append(v)
    return {g: sum(v)/len(v) for g,v in by.items()}

def binding(ratings):
    fm = fmeans(ratings)
    if any(g not in fm for g in FOUND): return None
    return sum(fm[g] for g in BIND)/3

def permodel(pattern, keyfn):
    acc = defaultdict(lambda: defaultdict(list))
    for f in glob.glob(pattern):
        d = json.load(open(f))
        if not d.get("ratings"): continue
        k = keyfn(d)
        if k is None: continue
        b = binding(d["ratings"])
        if b is None: continue
        acc[k][d["model"]].append(b)
    return {k: {m: sum(v)/len(v) for m,v in md.items()} for k,md in acc.items()}

# ---- load all three sources
# Framed in-language cells are keyed BY COUNTRY. Without the country every Arabic
# framed country pools into a single "ar_framed" bucket and silently moves the published
# Egypt number; that happened for real on 2026-08-21 with three test cells.
lang = permodel(str(VDIR/"runs_framed_lang"/"*.json"),
                lambda d: (d["instrument"].split("_")[1],
                           d["condition"] if d["condition"] != "framed"
                           else "framed_" + d["country"]))
# Every English-framed country, since 2026-09-08. Until then this loaded only Egypt, Japan
# and Iran, the three the first collection needed, so condition_means.json carried 27 of the
# 47 conditions and the contrast set could not be built on the full grid (decision 15).
enfr = permodel(str(VDIR/"runs_framed"/"*_mfq2_*.json"),
                lambda d: d.get("country") if d.get("country") else None)
# ENGLISH UNFRAMED, changed 2026-08-22. This used to be our own transcription of the
# MFQ-2 administered with run_validity.py's self-report system prompt, while every
# in-language unframed arm used the official Atari et al. translation with NO system
# prompt: the comparator differed from what it was compared against in two ways at once.
# Both were measured (results/english_baseline_audit.txt): instrument -0.038 p=.47,
# system prompt +0.026 p=.49, neither distinguishable from zero. The official no-system
# cell is the baseline now because it is the matched one. The old cell is kept under
# en_neutral_ours so the errata can cite what was published before.
ennu = permodel(str(VDIR/"runs_english_baseline"/"*.json"),
                lambda d: "en_neutral" if d.get("condition")=="official_nosystem" else None)
enold = permodel(str(VDIR/"runs"/"*mfq2*.json"),
                 lambda d: "en_neutral_ours" if d.get("instrument")=="mfq2" else None)

CONDS = {**{f"{c[0]}_{c[1]}": v for c,v in lang.items()},
         **{f"EN_framed_{k}": v for k,v in enfr.items()},
         **({"en_neutral": ennu["en_neutral"]} if "en_neutral" in ennu else {}),
         **({"en_neutral_ours": enold["en_neutral_ours"]}
            if "en_neutral_ours" in enold else {})}

print("=== VERIFICATION: per-model binding by condition (n models, panel mean) ===")
ROSTER = sorted(set(m for v in CONDS.values() for m in v))
for k in sorted(CONDS):
    v = CONDS[k]
    mu = sum(v.values())/len(v)
    print(f"  {k:<18} n={len(v):<3} mean={mu:.3f}  models={sorted(v)==ROSTER or sorted(v)}")
# INDEPENDENT RECOMPUTATION, the reconciliation gate. The old gate compared against
# panel means hardcoded from the July collection, which cannot survive a re-collection
# and would have to be edited by hand every time the data changes, defeating its purpose.
# This route reaches the same quantity by different code: it takes the plain mean of the
# eighteen binding ITEMS in a cell rather than averaging three foundation means. The two
# agree only if each binding foundation carries the same number of items, so the check
# also verifies the item counts it depends on.
def direct_binding(ratings):
    vals = [v for iid, v in ratings.items() if iid.rsplit("_", 1)[0] in BIND]
    return (sum(vals) / len(vals)) if vals else None

alt = defaultdict(lambda: defaultdict(list))
for pattern, keyfn in ((str(VDIR/"runs_framed_lang"/"*.json"),
                        lambda d: "%s_%s" % (d["instrument"].split("_")[1],
                                             d["condition"] if d["condition"] != "framed"
                                             else "framed_" + d["country"])),
                       (str(VDIR/"runs_framed"/"*_mfq2_*.json"),
                        lambda d: ("EN_framed_" + d["country"]) if d.get("country") else None),
                       (str(VDIR/"runs_english_baseline"/"*.json"),
                        lambda d: "en_neutral" if d.get("condition") == "official_nosystem"
                        else None),
                       (str(VDIR/"runs"/"*mfq2*.json"),
                        lambda d: "en_neutral_ours" if d.get("instrument") == "mfq2" else None)):
    import glob as _g
    for f in _g.glob(pattern):
        d = json.load(open(f))
        if not d.get("ratings"): continue
        k = keyfn(d)
        if k is None: continue
        b = direct_binding(d["ratings"])
        if b is None: continue
        alt[k][d["model"]].append(b)
ALT = {k: sum(sum(v)/len(v) for v in md.values())/len(md) for k, md in alt.items()}

print("  reconcile against an independent recomputation from the raw cells:")
ok = True
for k in sorted(CONDS):
    got = sum(CONDS[k].values())/len(CONDS[k])
    exp = ALT.get(k)
    match = exp is not None and abs(got-exp) < 1e-9
    ok &= match
    print(f"    {k:<30} foundation-route {got:.4f}  item-route {exp if exp is None else '%.4f'%exp}  {'OK' if match else 'MISMATCH'}")
print("  RECONCILED" if ok else "  *** RECONCILIATION FAILED - STOP ***")
if not ok: raise SystemExit(1)

# hand the condition means to audit_inlanguage_grid.py so it reconciles against this
# run rather than against numbers frozen from an earlier collection
(VDIR/"results"/"condition_means.json").write_text(json.dumps(
    {k: sum(v.values())/len(v) for k, v in CONDS.items()}, indent=2, sort_keys=True) + "\n")

def boot_ci(vals, key):
    """Percentile bootstrap over models. The RNG is seeded from (SEED, key), so each
    interval is independent of how many other quantities were computed first. Seeding
    one shared stream made every interval depend on the order and NUMBER of conditions
    present, so adding a condition silently moved the third decimal of unrelated
    intervals. Changed 2026-08-21; that change moved four published bounds by 0.001
    once, and no addition can move them again."""
    rng = random.Random("%d|%s" % (SEED, key))
    n = len(vals); stats = []
    for _ in range(B):
        s = [vals[rng.randrange(n)] for _ in range(n)]
        stats.append(sum(s)/n)
    stats.sort()
    return stats[int(0.025*B)], stats[int(0.975*B)]

def signflip_exact(diffs):
    """Exact sign-flip permutation p (two-sided) for mean(diffs) != 0."""
    n = len(diffs); obs = abs(sum(diffs)/n); cnt = 0; tot = 2**n
    for signs in itertools.product((1,-1), repeat=n):
        s = sum(d*sg for d,sg in zip(diffs,signs))/n
        if abs(s) >= obs - 1e-12: cnt += 1
    return cnt/tot

def paired(a, b):
    ms = sorted(set(a) & set(b))
    return [a[m]-b[m] for m in ms], ms

print("\n=== bootstrap 95% CIs on panel means (cluster = model, 100k) ===")
CI = {}
for k in sorted(CONDS):
    vals = list(CONDS[k].values())
    lo,hi = boot_ci(vals, k)
    CI[k]=(lo,hi)
    print(f"  {k:<18} mean={sum(vals)/len(vals):.3f}  CI[{lo:.3f},{hi:.3f}]")

tests = {}
d,_ = paired(CONDS["EN_framed_Egypt"], CONDS["ar_framed_Egypt"])
tests["T1 Egypt: EN-framed vs AR-framed"] = (sum(d)/len(d), signflip_exact(d), d)
d,_ = paired(CONDS["EN_framed_Japan"], CONDS["ja_framed_Japan"])
tests["T2 Japan: EN-framed vs JA-framed"] = (sum(d)/len(d), signflip_exact(d), d)
d = [v-ANCH["Japan"] for v in CONDS["ja_neutral"].values()]
tests["T3 JA-neutral vs Japan anchor"] = (sum(d)/len(d), signflip_exact(d), d)
d = [v-ANCH["Iran"] for v in CONDS["fa_framed_Iran"].values()]
tests["T4 FA-framed vs Iran anchor"] = (sum(d)/len(d), signflip_exact(d), d)
if "en_neutral" in CONDS:
    d,_ = paired(CONDS["fa_neutral"], CONDS["en_neutral"])
    tests["T5 FA-neutral vs EN-neutral"] = (sum(d)/len(d), signflip_exact(d), d)
    d,_ = paired(CONDS["ar_neutral"], CONDS["en_neutral"])
    tests["T6 AR-neutral vs EN-neutral"] = (sum(d)/len(d), signflip_exact(d), d)
d = [v-ANCH["Egypt"] for v in CONDS["ar_framed_Egypt"].values()]
tests["T7 AR-framed vs Egypt anchor"] = (sum(d)/len(d), signflip_exact(d), d)
d,_ = paired(CONDS["ja_framed_Japan"], CONDS["ja_neutral"])
tests["T8 Japan: framed vs neutral (in-lang)"] = (sum(d)/len(d), signflip_exact(d), d)
if "EN_framed_Iran" in CONDS:
    d = [v-ANCH["Iran"] for v in CONDS["EN_framed_Iran"].values()]
    tests["T9 EN-framed Iran vs Iran anchor"] = (sum(d)/len(d), signflip_exact(d), d)
    d,_ = paired(CONDS["EN_framed_Iran"], CONDS["fa_framed_Iran"])
    tests["T10 Iran: EN-framed vs FA-framed"] = (sum(d)/len(d), signflip_exact(d), d)

FAMILY_A = list(tests)

# T11 completes the language family: one test per language against the English default.
d,_ = paired(CONDS["ja_neutral"], CONDS["en_neutral"])
tests["T11 JA-neutral vs EN-neutral"] = (sum(d)/len(d), signflip_exact(d), d)

FAMILY_B = ["T5 FA-neutral vs EN-neutral",
            "T6 AR-neutral vs EN-neutral",
            "T11 JA-neutral vs EN-neutral"]

def holm(names):
    ps = sorted((tests[k][1], k) for k in names)
    m = len(ps); out = {}; running = 0.0
    for i,(p,k) in enumerate(ps):
        running = max(running, p*(m-i))
        out[k] = min(1.0, running)
    return out

hA = holm(FAMILY_A)
hB = holm(FAMILY_B)

# One interval per test, drawn once, in family-A order and then T11. A test that
# belongs to both families therefore reports the same interval in both, and the
# family-A draws sit at the same position in the RNG stream as before T11 existed,
# so appendix B4 still reproduces line for line.
CIT = {}
for k in FAMILY_A + ["T11 JA-neutral vs EN-neutral"]:
    CIT[k] = boot_ci(tests[k][2], k)

print("\n=== FAMILY A, the framing claim (post hoc, exploratory): exact sign-flip tests ===")
print("    Ten tests, Holm across the ten. Unchanged from appendix B4.")
for k in FAMILY_A:
    eff,p,d = tests[k]
    lo,hi = CIT[k]
    print(f"  {k:<40} diff={eff:+.3f} CI[{lo:+.3f},{hi:+.3f}]  p={p:.4f}  holm={hA[k]:.4f}  n={len(d)}")

print("\n=== FAMILY B, the language claim (post hoc, exploratory): one test per language ===")
print("    Does the local-language unframed condition depart from the English default?")
print("    Holm across the three. T5 and T6 also appear in family A; see the module docstring.")
for k in FAMILY_B:
    eff,p,d = tests[k]
    lo,hi = CIT[k]
    print(f"  {k:<40} diff={eff:+.3f} CI[{lo:+.3f},{hi:+.3f}]  p={p:.4f}  holm={hB[k]:.4f}  n={len(d)}")
print("  Nulls are bounds, not demonstrated absence. Largest effect each rules out:")
for k in FAMILY_B:
    lo,hi = CIT[k]
    print(f"    {k:<40} |effect| <= {max(abs(lo),abs(hi)):.3f}")
print("  Per-model sign counts (a real shift moves models together):")
for k in FAMILY_B:
    d = tests[k][2]
    print(f"    {k:<40} up {sum(1 for x in d if x>0)}/{len(d)}, down {sum(1 for x in d if x<0)}/{len(d)}")

print("\n=== leave-one-model-out sweeps ===")
def loo(vals_by_model):
    out=[]
    for m in vals_by_model:
        rest=[v for k,v in vals_by_model.items() if k!=m]
        out.append((m, sum(rest)/len(rest)))
    return out
print("  JA-neutral panel mean without each model (anchor 2.652):")
for m,mu in sorted(loo(CONDS["ja_neutral"]), key=lambda x:x[1]):
    print(f"    -{m:<14} {mu:.3f}")
print("  FA-framed overshoot vs the Iran anchor without each model:")
for m,mu in sorted(loo(CONDS["fa_framed_Iran"]), key=lambda x:x[1]):
    print(f"    -{m:<14} {mu-ANCH["Iran"]:+.3f}")
print("  EN-framed Iran overshoot vs the Iran anchor without each model:")
for m,mu in sorted(loo(CONDS["EN_framed_Iran"]), key=lambda x:x[1]):
    print(f"    -{m:<14} {mu-ANCH['Iran']:+.3f}")
print("  T11 (JA-neutral minus EN-neutral) without each model:")
ms = sorted(set(CONDS["ja_neutral"]) & set(CONDS["en_neutral"]))
for drop in ms:
    rest = [CONDS["ja_neutral"][m]-CONDS["en_neutral"][m] for m in ms if m != drop]
    print(f"    -{drop:<14} {sum(rest)/len(rest):+.4f}")


# ------------------------------------------------------------------ appendix B4/B5
# Emitted as markdown so the appendix document splices these sections rather than
# transcribing them. The stdout above stays the verification trail; the exact sign-flip
# enumeration lives there and nowhere else (decision 15). Nothing is recomputed here:
# every value comes from CONDS, boot_ci and loo as already built.
#
# The contrast set covers every (language, country) pair with both languages, per
# decision 15: four contrasts and their interaction, each reported as the difference,
# the 95% model-resampling interval, the per-model sign count and the leave-one-out
# range. Seven contrasts are the same quantity as a test the declared family reported
# (some with the sign reversed); their bootstraps keep the old key so the interval
# carries over to the digit. New contrasts get their own stream.

LANG_NAME = {"ar": "Arabic", "es": "Spanish", "fr": "French",
             "ja": "Japanese", "fa": "Farsi", "ru": "Russian"}
LANG_ORDER = ["ar", "es", "fr", "ja", "fa", "ru"]
PAIRS = [(code, k[len(code) + 8:]) for code in LANG_ORDER
         for k in sorted(CONDS) if k.startswith(code + "_framed_")]

# (kind, code, country) -> (old test key, sign of old relative to new)
OLD_KEY = {("lang_framed", "ar", "Egypt"):  ("T1 Egypt: EN-framed vs AR-framed", -1),
           ("lang_framed", "ja", "Japan"):  ("T2 Japan: EN-framed vs JA-framed", -1),
           ("lang_framed", "fa", "Iran"):   ("T10 Iran: EN-framed vs FA-framed", -1),
           ("framing_local", "ja", "Japan"): ("T8 Japan: framed vs neutral (in-lang)", +1),
           ("lang_unframed", "fa", None):   ("T5 FA-neutral vs EN-neutral", +1),
           ("lang_unframed", "ar", None):   ("T6 AR-neutral vs EN-neutral", +1),
           ("lang_unframed", "ja", None):   ("T11 JA-neutral vs EN-neutral", +1)}


def per_model(kind, code, country):
    en_n, lo_n = CONDS["en_neutral"], CONDS[code + "_neutral"]
    if kind == "lang_unframed":
        ms = sorted(set(lo_n) & set(en_n)); return {m: lo_n[m] - en_n[m] for m in ms}
    en_f, lo_f = CONDS["EN_framed_" + country], CONDS[code + "_framed_" + country]
    ms = sorted(set(en_n) & set(lo_n) & set(en_f) & set(lo_f))
    if kind == "framing_en":    return {m: en_f[m] - en_n[m] for m in ms}
    if kind == "framing_local": return {m: lo_f[m] - lo_n[m] for m in ms}
    if kind == "lang_framed":   return {m: lo_f[m] - en_f[m] for m in ms}
    if kind == "interaction":   return {m: (lo_f[m] - lo_n[m]) - (en_f[m] - en_n[m]) for m in ms}
    raise KeyError(kind)


def contrast(kind, code, country):
    d = per_model(kind, code, country); vals = list(d.values())
    old = OLD_KEY.get((kind, code, country))
    if old:
        key, sgn = old
        lo, hi = boot_ci([sgn * v for v in vals], key)
        lo, hi = (lo, hi) if sgn == 1 else (-hi, -lo)
    else:
        lo, hi = boot_ci(vals, "C|%s|%s|%s" % (kind, code, country))
    up = sum(1 for v in vals if v > 0); dn = sum(1 for v in vals if v < 0)
    loo_v = [mu for _, mu in loo(d)]
    return {"diff": sum(vals) / len(vals), "lo": lo, "hi": hi, "up": up, "dn": dn,
            "n": len(vals), "loo_lo": min(loo_v), "loo_hi": max(loo_v), "vals": vals}


def row(label, c):
    return "| %s | %+.3f | [%+.3f, %+.3f] | %d up, %d down | %+.3f to %+.3f |" % (
        label, c["diff"], c["lo"], c["hi"], c["up"], c["dn"], c["loo_lo"], c["loo_hi"])


HEAD = "| contrast | difference | 95%% model-resampling interval | models (of %d) | leave-one-out range |"
SEP = "|---|--:|:--:|--:|:--:|"

C = {}
for code, country in PAIRS:
    for kind in ["framing_en", "framing_local", "lang_framed", "interaction"]:
        C[(kind, code, country)] = contrast(kind, code, country)
U = {code: contrast("lang_unframed", code, None) for code in LANG_ORDER}
N = next(iter(C.values()))["n"]

# verification trail: the same numbers, plainly
print("\n=== CONTRASTS on the full grid (decision 15): diff, model-resampling 95%, signs, LOO ===")
for code in LANG_ORDER:
    c = U[code]
    print("  %-34s %+.3f [%+.3f,%+.3f] up %d/%d dn %d  LOO %+.3f..%+.3f" % (
        LANG_NAME[code] + " unframed vs English", c["diff"], c["lo"], c["hi"], c["up"], c["n"], c["dn"], c["loo_lo"], c["loo_hi"]))
for code, country in PAIRS:
    for kind in ["framing_en", "framing_local", "lang_framed", "interaction"]:
        c = C[(kind, code, country)]
        print("  %-34s %+.3f [%+.3f,%+.3f] up %d/%d dn %d  LOO %+.3f..%+.3f" % (
            "%s/%s %s" % (LANG_NAME[code], country, kind), c["diff"], c["lo"], c["hi"], c["up"], c["n"], c["dn"], c["loo_lo"], c["loo_hi"]))

L = []
L.append("## B4. The contrasts\n")
L.append("Every country with both languages, and every language with both framings. Each contrast "
         "is computed within a model first and then averaged across the %d, so the interval, the "
         "sign count and the leave-one-out range all describe the same per-model differences. The "
         "interval is a percentile bootstrap resampling the %d models, 100,000 draws, seeded per "
         "quantity: it shows how far the difference moves when models like these are resampled, and "
         "it bounds nothing. An interval that includes both positive and negative values is reported "
         "as such; it does not establish equivalence. The sign count and the leave-one-out range "
         "describe the same eleven per-model differences and carry no test; across the %d contrasts "
         "reported here no family-wise claim is made, and none should be read in. Language under "
         "framing changes the questionnaire and the instruction together, since the in-language "
         "framing instruction is a translation; the unframed rows change the questionnaire alone. "
         "No p-values are reported; decision 15 
         "says why; the exact sign-flip enumeration remains in the audit's verification output.\n" % (N, N))
L.append("**Language without framing.** The translated questionnaire against the English one, "
         "neither naming a country. One row per language.\n")
L.append(HEAD % N); L.append(SEP)
for code in LANG_ORDER:
    L.append(row(LANG_NAME[code] + " unframed minus English unframed", U[code]))
_ex = [LANG_NAME[c] for c in LANG_ORDER if U[c]["lo"] > 0 or U[c]["hi"] < 0]
L.append("\n%s\n" % ("The interval excludes zero for %s only." % ", ".join(_ex) if len(_ex) == 1
                     else "The interval excludes zero for %s." % ", ".join(_ex) if _ex
                     else "No language's interval excludes zero."))
L.append("**Framing, and language under framing, per country.** Framing in English is the "
         "English-framed condition minus the English unframed one. Framing in the local language "
         "is the local-framed condition minus the local unframed one. Language under framing is the "
         "local-framed condition minus the English-framed one. The interaction is the local framing "
         "effect minus the English framing effect: positive where naming the country moves the panel "
         "further in the local language than in English.\n")
for code in LANG_ORDER:
    for cc, country in PAIRS:
        if cc != code: continue
        L.append("*%s, framed as %s%s*\n" % (LANG_NAME[code], country,
                 " (the Spanish arm, decision 12)" if (code, country) == ("es", "Morocco") else ""))
        L.append(HEAD % N); L.append(SEP)
        L.append(row("framing in English", C[("framing_en", code, country)]))
        L.append(row("framing in " + LANG_NAME[code], C[("framing_local", code, country)]))
        L.append(row("language under framing", C[("lang_framed", code, country)]))
        L.append(row("interaction", C[("interaction", code, country)]))
        L.append("")

# the 1.04 and its weighting
_grp = {c: [k for cc, k in PAIRS if cc == c and not (c == "es" and k == "Morocco")] for c in LANG_ORDER}
_per_lang = {c: sum(C[("framing_local", c, k)]["diff"] for k in _grp[c]) / len(_grp[c]) for c in LANG_ORDER}
_eq_lang = sum(_per_lang.values()) / len(_per_lang)
_all_pairs = sum(C[("framing_local", c, k)]["diff"] for c, k in PAIRS) / len(PAIRS)
_no_esmor = [(c, k) for c, k in PAIRS if not (c == "es" and k == "Morocco")]
_eq_pair = sum(C[("framing_local", c, k)]["diff"] for c, k in _no_esmor) / len(_no_esmor)
L.append("**The average framing shift, and how it is weighted.** The paper's %.2f is the local "
         "framing effect averaged within each language over its countries, with Morocco counted "
         "under Arabic and not Spanish, and then averaged across the six languages with equal "
         "weight: %s. Weighting every (language, country) pair equally instead gives %.3f over the "
         "same %d pairs, and %.3f over all %d including Spanish Morocco.\n" % (
         _eq_lang, ", ".join("%s %+.3f" % (LANG_NAME[c], _per_lang[c]) for c in LANG_ORDER),
         _eq_pair, len(_no_esmor), _all_pairs, len(PAIRS)))

# ---- Iran anchor: caveat and sensitivity, unchanged in substance
_IR = json.load(open(VDIR / "anchors_iran.json"))
_s1, _s2 = _IR["samples"]["s1"]["n"], _IR["samples"]["s2"]["n"]
_b1, _b2 = _IR["binding_1to5"]["s1"], _IR["binding_1to5"]["s2"]
_pool = (_b1 * _s1 + _b2 * _s2) / (_s1 + _s2)
_en_ir_mean = sum(CONDS["EN_framed_Iran"].values()) / len(CONDS["EN_framed_Iran"])
_fa_ir_mean = sum(CONDS["fa_framed_Iran"].values()) / len(CONDS["fa_framed_Iran"])
L.append("**[*] The Iran anchor, and what it costs.** Nineteen of the twenty anchors are "
         "Atari et al. (2023) Study 2. Iran is not in that set; its anchor is Hazrati, Nejat "
         "and Daneshi (2025), a different paper with different collection conditions, using "
         "Atari's Persian translation with minor linguistic edits, administered 0 to 4 with the "
         "same anchor words as the 1-to-5 scale, from does not describe me at all to describes me "
         "extremely well, so the +1 shift maps label to label. That sample is a Telegram "
         "and snowball convenience sample, n=%d, 68 to 71 percent female, mean age 26 to 28, "
         "57 to 59 percent educated to bachelor's or above, and we read it as "
         "likely less binding-endorsing than the general Iranian population, our inference and not the "
         "authors' statement - which would bias this overshoot upward. Collection began a year after the Woman, Life, Freedom movement "
         "and the authors note possible period effects. Iran is the only Farsi country, so it "
         "carries that group throughout. Respondent-level data for both samples are shared by the "
         "authors on OSF.\n" % _s2)
_alts = [_b2, _b1, _pool]
_rank = ("largest" if _b2 == max(_alts) else "smallest" if _b2 == min(_alts) else "middle")
_conseq = ("smallest" if _b2 == max(_alts) else "largest" if _b2 == min(_alts) else "middle")
L.append("Every anchor the source offers is shown. The one in use is the %s of the three, "
         "so the overshoot reported throughout is the %s of the three:\n" % (_rank, _conseq))
L.append("| Iran anchor | binding | EN-framed overshoot | FA-framed overshoot |")
L.append("|---|--:|--:|--:|")
for lab, a in [("sample 2, n=%d (in use)" % _s2, _b2), ("sample 1, n=%d" % _s1, _b1),
               ("n-weighted pool of both", _pool)]:
    L.append("| %s | %.3f | %+.3f | %+.3f |" % (lab, a, _en_ir_mean - a, _fa_ir_mean - a))
L.append("\nThe sign and the ordering of the Iran result do not depend on the choice. Its "
         "magnitude does, by up to %.3f.\n" % (max(_alts) - min(_alts)))

# ---- B5
_ja = [mu for _, mu in loo(CONDS["ja_neutral"])]
_en_ir = [mu - ANCH["Iran"] for _, mu in loo(CONDS["EN_framed_Iran"])]
_fa_ir = [mu - ANCH["Iran"] for _, mu in loo(CONDS["fa_framed_Iran"])]
_all_over = all(v > ANCH["Iran"] for v in CONDS["EN_framed_Iran"].values()) and \
            all(v > ANCH["Iran"] for v in CONDS["fa_framed_Iran"].values())
L.append("## B5. Robustness: leave-one-model-out\n")
L.append("Every contrast in B4 carries its own leave-one-out range. The anchor comparisons, which "
         "are distances from a constant, are swept here. Japanese neutral panel mean with each "
         "model removed spans %.3f to %.3f around an anchor of %.3f. English-framed Iran overshoot "
         "spans %+.3f to %+.3f; Farsi-framed Iran overshoot spans %+.3f to %+.3f. %s\n"
         % (min(_ja), max(_ja), ANCH["Japan"], min(_en_ir), max(_en_ir), min(_fa_ir), max(_fa_ir),
            "Every individual model overshoots both Iran conditions."
            if _all_over else "Not every model overshoots both Iran conditions."))

# ---- B7: failed calls, counted from the files rather than typed
_fail = defaultdict(int); _nfail = 0; _scored = 0
for _d in ("runs_framed", "runs_framed_lang", "runs_english_baseline"):
    for _f in glob.glob(str(VDIR / _d / "*.json")):
        _r = json.load(open(_f))
        if _r.get("ratings"):
            _scored += 1
        else:
            _fail[_r["model"]] += 1; _nfail += 1
# the fiftieth condition, en_neutral_ours, lives in runs/ and had no failures
_scored += sum(1 for _f in glob.glob(str(VDIR / "runs" / "*mfq2*.json"))
               if json.load(open(_f)).get("instrument") == "mfq2" and json.load(open(_f)).get("ratings"))
_by = sorted(_fail.items(), key=lambda x: (-x[1], x[0]))
L.append("## B7. Failed calls\n")
L.append("%s of %s attempted calls returned no ratings object, from provider rate limits on the "
         "Together-hosted models and from replies that carried no parseable object. All were "
         "retried to success within the same collection window, so every one of the %s scored "
         "cells is present and no condition rests on fewer than five iterations. By model: %s. "
         "Retrying to a parseable reply conditions the scored sample on compliance; the %s "
         "unparsed replies are kept as collected and are not scored. This collection contains "
         "no refusal.\n" % (
         "{:,}".format(_nfail), "{:,}".format(_scored + _nfail), "{:,}".format(_scored),
         ", ".join("%s %d" % (m, n) for m, n in _by), _nfail))

# ---- B1a: roster and protocol, generated so the manifest cannot drift from the code
import ast, re
_reg = json.load(open(VDIR.parent / "models.json"))["models"]
_present = set(ROSTER)
_rv = (VDIR / "run_validity.py").read_text()
_m = re.search(r"^SYSTEM = \((.*?)\)\n", _rv, re.S | re.M)
_unframed_system = ast.literal_eval("(" + _m.group(1) + ")") if _m else None
assert _unframed_system, "run_validity.SYSTEM not found"
_rf = (VDIR / "run_framed.py").read_text()


def _frame_template():
    """The framing instruction exactly as run_framed.frame_system builds it, with {country}
    left in place: read from the function's AST, so the appendix cannot drift from the runner."""
    tree = ast.parse(_rf)
    fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "frame_system")
    ret = next(n for n in ast.walk(fn) if isinstance(n, ast.Return)).value
    parts = ret.values if isinstance(ret, ast.JoinedStr) else [ret]
    out = []
    for p in parts:
        if isinstance(p, ast.Constant):
            out.append(str(p.value))
        elif isinstance(p, ast.FormattedValue) and isinstance(p.value, ast.Name):
            out.append("{" + p.value.id + "}")
        else:
            raise SystemExit("frame_system has a part the appendix emitter cannot render")
    return "".join(out)


_FRAME = _frame_template()
# parser rounding audit: how many accepted ratings were non-integers in the raw reply
_nrat = _nround = 0
for _d in ("runs_framed", "runs_framed_lang", "runs_english_baseline", "runs"):
    for _f in glob.glob(str(VDIR / _d / "*.json")):
        _r = json.load(open(_f))
        if not _r.get("ratings") or (_d == "runs" and _r.get("instrument") != "mfq2"):
            continue
        _m = re.search(r'"ratings"\s*:\s*\{[^}]*\}', _r.get("raw_text") or "")
        if not _m:
            continue
        for _k, _v in re.findall(r'"(\d+)"\s*:\s*([-\d.]+)', _m.group(0)):
            _nrat += 1
            if "." in _v and float(_v) != int(float(_v)):
                _nround += 1
assert "{country}" in _FRAME and "questionnaire" in _FRAME, "frame_system template not recovered"
M = []
M.append("## B1a. Roster and protocol\n")
M.append("**The panel.** `models.json` registers %d models. %d answered every cell; %d are absent "
         "from every cell for the infrastructural reasons B1 gives. Roster keys are the names used "
         "throughout; a swapped model gets its own key (decision 10).\n" % (len(_reg), len(_present), len(_reg) - len(_present)))
M.append("| roster key | provider | model string | in the grid |")
M.append("|---|---|---|---|")
for k in sorted(_reg, key=lambda x: (x not in _present, x)):
    M.append("| %s | %s | `%s` | %s |" % (k, _reg[k]["provider"], _reg[k]["model_id"], "yes" if k in _present else "no"))
M.append("\n**Request.** One user message carrying the questionnaire; the framing instruction, where "
         "there is one, as the system prompt; nothing else. Anthropic receives it in the `system` "
         "field, OpenAI, xAI, Together and Mistral as a `role: system` message, Google as "
         "`systemInstruction`. A request seed is sent where the provider accepts one (OpenAI, xAI, "
         "Together as `seed`, Mistral as `random_seed`); the English framed runner uses 20260721 "
         "plus the iteration, the in-language runner 20260722 plus the iteration. Token ceilings are "
         "per provider: Anthropic 3072, OpenAI and xAI 4096, Together 6144, Mistral 2048, Google "
         "6144, Cohere 2048. No temperature is sent, so each model ran at its provider's default, "
         "which the run records do not capture; a pinned value would have documented the setting "
         "and would not have made stochasticity equivalent across models. The defaults are not "
         "reconstructed from provider documentation, which is not dated to the collection window "
         "and changes.\n")
M.append("**The self-report system prompt** of the two `selfreport` baseline variants, English, verbatim from `run_validity.py`:\n")
M.append("> " + _unframed_system + "\n")
M.append("**The framing instruction**, English, verbatim from `run_framed.py` with the country "
         "substituted:\n")
M.append("> " + _FRAME + "\n")
M.append("The in-language framing instructions are our translations of that template, one per "
         "language, AI-assisted and disclosed as such, varying only the country name and the "
         "demonym. Each cell records the instruction it was sent verbatim in its `system_prompt` "
         "field, and the runner asserts at start-up that the Arabic template still reproduces the "
         "Egypt prompt byte for byte as first collected.\n")
M.append("**The unframed conditions send no system prompt.** The matched English baseline and all six "
         "translated unframed conditions were run with `NEUTRAL_SYSTEM = \"\"`; every one of their "
         "saved runs records an empty system prompt. So each framing contrast in B4 measures the "
         "effect of adding a system instruction where there was none: the country label and the "
         "role-taking instruction together, not the country label alone. The nearest measurement of "
         "the instruction on its own is the English baseline pair in `results/english_baseline_audit.txt`, "
         "where a self-report system prompt naming no country lowered the composite by 0.026 against "
         "none, model-resampling interval [-0.090, +0.042], eight of eleven models lower with the "
         "prompt. That prompt is not the framing template, so it brackets the role-taking component "
         "rather than isolating it; a country-neutral arm with the framing template itself would, "
         "and was not run.\n")
M.append("**The user message.** Items are shuffled per run, then grouped by response scale in the "
         "instrument's fixed scale order and numbered 1 to 36 in shuffled order within each group. "
         "Each group opens with its scale prompt and a legend of the anchor labels. The message "
         "closes by asking for exactly one JSON object, `{\"ratings\": {\"1\": <int>, ..., \"36\": "
         "<int>}}`, and nothing else.\n")
M.append("**The parser.** Every top-level balanced `{...}` in the reply is parsed. The last one "
         "carrying a `ratings` dictionary is taken; failing that, the last bare map keyed by item "
         "number. Every item must be present; each value is coerced by `int(round(float(v)))` and "
         "must fall inside its scale's bounds. Any failure returns no ratings object, and the reply "
         "is kept as collected with the parser's reason. No reply is edited or re-parsed by hand. Of "
         "the %s ratings accepted across the fifty conditions, %d arrived as a non-integer and were "
         "rounded.\n" % ("{:,}".format(_nrat), _nround))
M.append("**Retries.** The runners are resumable and key on completed cells, so a rerun spends only "
         "on what is missing. `fill.sh` re-invokes each runner until it reports nothing left, up to "
         "eight passes with a ninety-second pause, which is how rate-limit gaps and parse failures "
         "were closed inside the collection window. B7 counts them. Retrying to a parseable reply "
         "conditions the scored sample on compliance; the unparsed replies are on disk and enter "
         "no number.\n")
M.append("**Instruments.** Item wording is the official MFQ-2 and its six official translations from "
         "the Atari et al. (2023) supplement, extracted verbatim; ids, groups and scoring are cloned "
         "from the English scaffold so every language scores identically. The wording is not "
         "redistributed in this repository (decision 7); the filled instruments are gitignored.\n")
M.append("**Dated design history**, from the commit log. 2026-07-20: the MFQ-2 administered "
         "unframed and framed as six countries in English, the collection now archived unchanged "
         "under `validity/archive-2026-07/`; its interim result is what led to the in-language "
         "design, and none of its cells enters any number here. 2026-07-23: the in-language "
         "machinery, per-language instruments and runner. 2026-08-21: three Arabic framed cells "
         "keyed on country; Kimi-K2.6 withdrawn by its host mid-collection and replaced by Kimi-K3 "
         "under its own key (decision 10); Spanish, French and Russian added, nine more countries. "
         "2026-08-21 to 2026-08-23: the collection reported here, in one window. 2026-08-22: the "
         "English comparator changed to the matched cell, the old one kept as errata (decision 11); "
         "Spanish Morocco added. 2026-08-24: Morocco compared on the Spanish arm and grouped with "
         "Arabic (decision 12); the fifteen-above shape left uninterpreted (decision 13). "
         "2026-09-07: the appendix regenerated on the completed grid. 2026-09-08: the contrast set "
         "rebuilt on the full grid without p-values (decision 15). Binding became the focal "
         "quantity on 2026-07-20, before any in-language cell existed; every choice after that "
         "was made with results in view.\n")
(VDIR / "results" / "appendix_b4_b5.md").write_text("\n".join(M + L) + "\n")
print("\nwrote results/appendix_b4_b5.md")
