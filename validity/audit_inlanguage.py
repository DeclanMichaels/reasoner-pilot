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
enfr = permodel(str(VDIR/"runs_framed"/"*_mfq2_*.json"),
                lambda d: d.get("country") if d.get("country") in ("Egypt","Japan","Iran") else None)
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
# transcribing them. The stdout above stays the verification trail; this is the same
# numbers in the document's shape. Nothing is recomputed here: every value comes from
# tests, CIT, hA, hB and CONDS as already built.

def _t11_loo():
    ms = sorted(set(CONDS["ja_neutral"]) & set(CONDS["en_neutral"]))
    return [(d, sum(CONDS["ja_neutral"][m] - CONDS["en_neutral"][m]
                    for m in ms if m != d) / (len(ms) - 1)) for d in ms]


def _span(pairs):
    v = [x[1] for x in pairs]
    return min(v), max(v)


def _bound(k):
    lo, hi = CIT[k]
    return max(abs(lo), abs(hi))


def _up(k):
    d = tests[k][2]
    return sum(1 for x in d if x > 0), sum(1 for x in d if x < 0), len(d)


TEST_MARK = {"T4 FA-framed vs Iran anchor": " [*]",
             "T9 EN-framed Iran vs Iran anchor": " [*]"}


def _row(k, fam_holm, with_signs=False):
    eff, p, d = tests[k]
    lo, hi = CIT[k]
    cells = ["%s%s" % (k, TEST_MARK.get(k, "")), "%+.3f" % eff, "[%+.3f, %+.3f]" % (lo, hi),
             "%.4f" % p, "%.4f" % fam_holm[k]]
    if with_signs:
        u, dn, n = _up(k)
        cells.append("%d of %d%s" % (u, n, ", none down" if dn == 0 else ""))
    return "| " + " | ".join(cells) + " |"


L = []
L.append("## B4. The test families\n")
L.append("Two families, one per headline claim, both post hoc and both exploratory. Paired "
         "tests use per-model differences; anchor tests subtract the constant from each "
         "model's mean. Exact sign-flip permutation: with eleven models the minimum "
         "attainable two-sided p is 2/2048, reported as 0.001. Nothing was pre-registered.\n")
WORDS = {3: "Three", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve"}
L.append("**Family A, the framing claim.** %s comparisons, Holm across the %s.\n"
         % (WORDS.get(len(FAMILY_A), len(FAMILY_A)),
            WORDS.get(len(FAMILY_A), len(FAMILY_A)).lower()
            if len(FAMILY_A) in WORDS else len(FAMILY_A)))
L.append("| test | difference | 95% CI | exact p | Holm |")
L.append("|---|--:|:--:|--:|--:|")
L += [_row(k, hA) for k in FAMILY_A]
L.append("\nNulls are reported as bounds, not as demonstrated absence: any Egypt language "
         "effect is within %.3f, and any Japanese-neutral displacement from the Japanese "
         "mean is within %.3f.\n"
         % (_bound("T1 Egypt: EN-framed vs AR-framed"),
            _bound("T3 JA-neutral vs Japan anchor")))
L.append("**Family B, the language claim.** One comparison per language, asking whether "
         "that language's unframed condition departs from the panel's English default. "
         "Holm across the three. T5 and T6 sit in both families; the double membership is "
         "disclosed rather than removed by re-cutting family A, and every conclusion holds "
         "under either cut.\n")
L.append("| test | difference | 95% CI | exact p | Holm | models moving up |")
L.append("|---|--:|:--:|--:|--:|--:|")
L += [_row(k, hB, with_signs=True) for k in FAMILY_B]
_t5u, _t5d, _n = _up("T5 FA-neutral vs EN-neutral")
_t11u, _t11d, _ = _up("T11 JA-neutral vs EN-neutral")
L.append("\nArabic is the only language whose interval excludes zero, and no model moves "
         "against it. Farsi splits %d up to %d down and Japanese %d up to %d down. As "
         "bounds: any Farsi departure from the English default is within %.3f, and any "
         "Japanese departure is within %.3f.\n"
         % (_t5u, _t5d, _t11u, _t11d,
            _bound("T5 FA-neutral vs EN-neutral"),
            _bound("T11 JA-neutral vs EN-neutral")))
L.append("One further comparison is reported outside both families as a single "
         "descriptive: the English default sits %+.3f from the Japanese human mean.\n"
         % (sum(CONDS["en_neutral"].values()) / len(CONDS["en_neutral"]) - ANCH["Japan"]))

_ja = _span(loo(CONDS["ja_neutral"]))
_en_ir = _span([(m, v - ANCH["Iran"]) for m, v in loo(CONDS["EN_framed_Iran"])])
_fa_ir = _span([(m, v - ANCH["Iran"]) for m, v in loo(CONDS["fa_framed_Iran"])])
_t11 = _span(_t11_loo())
_all_over = all(v > ANCH["Iran"] for v in CONDS["EN_framed_Iran"].values()) and \
            all(v > ANCH["Iran"] for v in CONDS["fa_framed_Iran"].values())
_IR = json.load(open(VDIR / "anchors_iran.json"))
_s1, _s2 = _IR["samples"]["s1"]["n"], _IR["samples"]["s2"]["n"]
_b1, _b2 = _IR["binding_1to5"]["s1"], _IR["binding_1to5"]["s2"]
_pool = (_b1 * _s1 + _b2 * _s2) / (_s1 + _s2)
_en_ir_mean = sum(CONDS["EN_framed_Iran"].values()) / len(CONDS["EN_framed_Iran"])
_fa_ir_mean = sum(CONDS["fa_framed_Iran"].values()) / len(CONDS["fa_framed_Iran"])
L.append("**[*] The Iran anchor, and what it costs.** Nineteen of the twenty anchors are "
         "Atari et al. (2023) Study 2. Iran is not in that set; its anchor is Hazrati, Nejat "
         "and Daneshi (2025), a different paper with different collection conditions. That "
         "sample is a Telegram and snowball convenience sample, n=%d, 68 to 71 percent "
         "female, mean age 26 to 28, 57 to 59 percent educated to bachelor's or above, and "
         "the anchor file records it as likely less binding-endorsing than the general "
         "Iranian population - which would bias this overshoot upward. Collection began a "
         "year after the Woman, Life, Freedom movement and the authors note possible period "
         "effects. Iran is the only Farsi country, so it carries that group throughout.\n"
         % _s2)
_alts = [_b2, _b1, _pool]
_rank = ("largest" if _b2 == max(_alts) else
         "smallest" if _b2 == min(_alts) else "middle")
_conseq = ("smallest" if _b2 == max(_alts) else
           "largest" if _b2 == min(_alts) else "middle")
L.append("Every anchor the source offers is shown. The one in use is the %s of the three, "
         "so the overshoot reported throughout is the %s of the three:\n"
         % (_rank, _conseq))
L.append("| Iran anchor | binding | EN-framed overshoot | FA-framed overshoot |")
L.append("|---|--:|--:|--:|")
for lab, a in [("sample 2, n=%d (in use)" % _s2, _b2),
               ("sample 1, n=%d" % _s1, _b1),
               ("n-weighted pool of both", _pool)]:
    L.append("| %s | %.3f | %+.3f | %+.3f |"
             % (lab, a, _en_ir_mean - a, _fa_ir_mean - a))
L.append("\nThe sign and the ordering of the Iran result do not depend on the choice. Its "
         "magnitude does, by up to %.3f.\n" % (max(_b2, _b1, _pool) - min(_b2, _b1, _pool)))
L.append("## B5. Robustness: leave-one-model-out\n")
L.append("Japanese neutral panel mean with each model removed spans %.3f to %.3f around an "
         "anchor of %.3f. English-framed Iran overshoot spans %+.3f to %+.3f; Farsi-framed "
         "Iran overshoot spans %+.3f to %+.3f. %s T11, the Japanese language effect, spans "
         "%+.3f to %+.3f under the same sweep.\n"
         % (_ja[0], _ja[1], ANCH["Japan"], _en_ir[0], _en_ir[1], _fa_ir[0], _fa_ir[1],
            "Every individual model overshoots both Iran conditions."
            if _all_over else "Not every model overshoots both Iran conditions.",
            _t11[0], _t11[1]))

(VDIR / "results" / "appendix_b4_b5.md").write_text("\n".join(L) + "\n")
print("\nwrote results/appendix_b4_b5.md")
