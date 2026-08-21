#!/usr/bin/env python3
"""Language x framing grid for the in-language MFQ-2 study, and a claim audit. Stdlib only.

Extends validity/audit_inlanguage.py, which produced appendix B3/B4/B5. Same conventions:
independent unit is the MODEL (11 clusters), iterations averaged first, bootstrap 100,000
draws resampling models, exact sign-flip permutation over all 2^11 = 2048 sign patterns,
seed 20260723. Reconciles against audit_inlanguage.py's published panel means before any
new number is reported.

Adds:
  1. The full 2 x 2 of language (English / local) x framing (unframed / framed), per country.
  2. The tests the declared T1-T10 family omits, T11 first: JA-neutral vs EN-neutral, the
     comparison that bears on the title.
  3. Per-foundation panel means for the ENGLISH conditions, absent from appendix B6.
  4. Direct checks of the claims in the write-up that no current artifact supports.

    python3 validity/audit_inlanguage_grid.py
"""
import json, glob, random, itertools
from pathlib import Path
from collections import defaultdict

VDIR = Path(__file__).resolve().parent
FOUND = ["care", "equality", "proportionality", "loyalty", "authority", "purity"]
BIND = ["loyalty", "authority", "purity"]
SEED = 20260723
B = 100_000

# Anchors. Egypt/Japan/Nigeria from Atari et al. (2023) Study 2 via the reasoner-study
# reference build (mfq2_country_means.csv); Iran from Hazrati et al. (2025) sample 2,
# per validity/anchors_iran.json.
ANCH = {"Egypt": 4.267, "Japan": 2.652, "Nigeria": 4.038, "Iran": 3.333}
ANCH_FOUND = {
    "Japan": {"care": 3.03, "equality": 2.27, "proportionality": 3.14,
              "loyalty": 2.66, "authority": 2.67, "purity": 2.63},
    "Iran": {"care": 3.948, "equality": 2.672, "proportionality": 4.147,
             "loyalty": 3.630, "authority": 3.050, "purity": 3.318},
}


def fmeans(ratings):
    by = defaultdict(list)
    for iid, v in ratings.items():
        by[iid.rsplit("_", 1)[0]].append(v)
    return {g: sum(v) / len(v) for g, v in by.items()}


def binding(ratings):
    fm = fmeans(ratings)
    if any(g not in fm for g in FOUND):
        return None
    return sum(fm[g] for g in BIND) / 3


def permodel(pattern, keyfn, what):
    acc = defaultdict(lambda: defaultdict(list))
    for f in glob.glob(pattern):
        d = json.load(open(f))
        if not d.get("ratings"):
            continue
        k = keyfn(d)
        if k is None:
            continue
        if what == "binding":
            b = binding(d["ratings"])
            if b is None:
                continue
            acc[k][d["model"]].append(b)
        else:
            fm = fmeans(d["ratings"])
            if any(g not in fm for g in FOUND):
                continue
            acc[k][d["model"]].append(fm)
    if what == "binding":
        return {k: {m: sum(v) / len(v) for m, v in md.items()} for k, md in acc.items()}
    return {k: {m: {g: sum(x[g] for x in v) / len(v) for g in FOUND} for m, v in md.items()}
            for k, md in acc.items()}


def load_all(what):
    # Framed in-language cells are keyed BY COUNTRY; see audit_inlanguage.py.
    lang = permodel(str(VDIR / "runs_framed_lang" / "*.json"),
                    lambda d: "%s_%s" % (d["instrument"].split("_")[1],
                                         d["condition"] if d["condition"] != "framed"
                                         else "framed_" + d["country"]), what)
    enfr = permodel(str(VDIR / "runs_framed" / "*_mfq2_*.json"),
                    lambda d: ("EN_framed_" + d["country"]) if d.get("country") else None, what)
    ennu = permodel(str(VDIR / "runs" / "*mfq2*.json"),
                    lambda d: "en_neutral" if d.get("instrument") == "mfq2" else None, what)
    return dict(list(lang.items()) + list(enfr.items()) + list(ennu.items()))


CONDS = load_all("binding")
FCONDS = load_all("found")


def mean(v):
    return sum(v) / len(v)


print("=== STEP 1. PLAIN DESCRIPTIVES, computed directly from the raw cells ===")
print("    (no resampling, no correction; every later estimate reconciles against these)")
for k in sorted(CONDS):
    v = CONDS[k]
    mu = mean(list(v.values()))
    sd = (sum((x - mu) ** 2 for x in v.values()) / len(v)) ** 0.5
    print("  %-20s n_models=%-3d mean=%.3f  between-model SD=%.3f" % (k, len(v), mu, sd))

ROSTER = sorted(set(m for v in CONDS.values() for m in v))
print("\n  roster (%d): %s" % (len(ROSTER), ", ".join(ROSTER)))
bad = dict((k, sorted(set(ROSTER) - set(v))) for k, v in CONDS.items() if sorted(v) != ROSTER)
print("  conditions missing a model: %s" % (bad if bad else "none"))

EXPECT = {"ar_framed_Egypt": 4.613, "ar_neutral": 3.033, "ja_framed_Japan": 3.459, "ja_neutral": 2.662,
          "fa_framed_Iran": 4.358, "fa_neutral": 2.720, "EN_framed_Egypt": 4.607,
          "EN_framed_Japan": 3.668, "EN_framed_Iran": 4.587, "en_neutral": 2.705}
print("\n  reconcile against appendix B3 (audit_inlanguage.py):")
ok = True
for k in sorted(EXPECT):
    got = mean(list(CONDS[k].values()))
    m = abs(got - EXPECT[k]) < 0.0015
    ok = ok and m
    print("    %-20s B3 %.3f  recomputed %.3f  %s" % (k, EXPECT[k], got, "OK" if m else "MISMATCH"))
print("  RECONCILED" if ok else "  *** RECONCILIATION FAILED, STOP ***")
if not ok:
    raise SystemExit(1)

def boot_ci(vals, key):
    """Seeded from (SEED, key) so an interval never depends on what else was computed
    first. See the same note in audit_inlanguage.py."""
    rng = random.Random("%d|%s" % (SEED, key))
    n = len(vals)
    s = []
    for _ in range(B):
        s.append(sum(vals[rng.randrange(n)] for _ in range(n)) / n)
    s.sort()
    return s[int(0.025 * B)], s[int(0.975 * B)]


def signflip_exact(diffs):
    n = len(diffs)
    obs = abs(mean(diffs))
    cnt = 0
    for signs in itertools.product((1, -1), repeat=n):
        if abs(sum(d * sg for d, sg in zip(diffs, signs)) / n) >= obs - 1e-12:
            cnt += 1
    return cnt / 2 ** n


def paired(a, b):
    ms = sorted(set(a) & set(b))
    return [a[m] - b[m] for m in ms]


print("\n=== STEP 2. THE GRID: binding composite, panel mean [95% CI] ===")
GRID = [("Egypt", "Arabic", "ar"), ("Japan", "Japanese", "ja"), ("Iran", "Farsi", "fa")]
cache = {}


def ci(k):
    if k not in cache:
        cache[k] = boot_ci(list(CONDS[k].values()), k)
    return cache[k]


hdr = "  %-18s%8s%22s%22s%22s%22s" % ("country/lang", "human", "EN unframed",
                                      "LOCAL unframed", "EN framed", "LOCAL framed")
print(hdr)
for country, langname, code in GRID:
    cells = []
    for k in ["en_neutral", code + "_neutral", "EN_framed_" + country, code + "_framed_" + country]:
        mu = mean(list(CONDS[k].values()))
        lo, hi = ci(k)
        cells.append(("%.3f [%.2f,%.2f]" % (mu, lo, hi)).rjust(22))
    print("  %-18s%8.3f%s" % (country + "/" + langname, ANCH[country], "".join(cells)))

print("\n  same grid as deviation from that country's measured human mean:")
print("  %-18s%16s%16s%16s%16s" % ("country/lang", "EN unframed", "LOCAL unframed",
                                   "EN framed", "LOCAL framed"))
for country, langname, code in GRID:
    cells = []
    for k in ["en_neutral", code + "_neutral", "EN_framed_" + country, code + "_framed_" + country]:
        cells.append("%+16.3f" % (mean(list(CONDS[k].values())) - ANCH[country]))
    print("  %-18s%s" % (country + "/" + langname, "".join(cells)))

print("\n=== STEP 3. TEST FAMILY. T1-T10 are the declared family (appendix B4).")
print("    T11+ are added here; each is fixed by the grid's structure, not chosen by its values.")
tests = {}
order = []


def add(name, diffs):
    tests[name] = (mean(diffs), signflip_exact(diffs), diffs)
    order.append(name)


add("T1  Egypt: EN-framed vs AR-framed", paired(CONDS["EN_framed_Egypt"], CONDS["ar_framed_Egypt"]))
add("T2  Japan: EN-framed vs JA-framed", paired(CONDS["EN_framed_Japan"], CONDS["ja_framed_Japan"]))
add("T3  JA-neutral vs Japan anchor", [v - ANCH["Japan"] for v in CONDS["ja_neutral"].values()])
add("T4  FA-framed vs Iran anchor", [v - ANCH["Iran"] for v in CONDS["fa_framed_Iran"].values()])
add("T5  FA-neutral vs EN-neutral", paired(CONDS["fa_neutral"], CONDS["en_neutral"]))
add("T6  AR-neutral vs EN-neutral", paired(CONDS["ar_neutral"], CONDS["en_neutral"]))
add("T7  AR-framed vs Egypt anchor", [v - ANCH["Egypt"] for v in CONDS["ar_framed_Egypt"].values()])
add("T8  Japan: framed vs neutral in-lang", paired(CONDS["ja_framed_Japan"], CONDS["ja_neutral"]))
add("T9  EN-framed Iran vs Iran anchor", [v - ANCH["Iran"] for v in CONDS["EN_framed_Iran"].values()])
add("T10 Iran: EN-framed vs FA-framed", paired(CONDS["EN_framed_Iran"], CONDS["fa_framed_Iran"]))
DECLARED = list(order)
add("T11 JA-neutral vs EN-neutral", paired(CONDS["ja_neutral"], CONDS["en_neutral"]))
add("T12 EN-neutral vs Japan anchor", [v - ANCH["Japan"] for v in CONDS["en_neutral"].values()])
add("T13 Egypt: AR-framed vs AR-neutral", paired(CONDS["ar_framed_Egypt"], CONDS["ar_neutral"]))
add("T14 Iran: FA-framed vs FA-neutral", paired(CONDS["fa_framed_Iran"], CONDS["fa_neutral"]))
add("T15 Egypt: EN-framed vs EN-neutral", paired(CONDS["EN_framed_Egypt"], CONDS["en_neutral"]))
add("T16 Japan: EN-framed vs EN-neutral", paired(CONDS["EN_framed_Japan"], CONDS["en_neutral"]))
add("T17 Iran: EN-framed vs EN-neutral", paired(CONDS["EN_framed_Iran"], CONDS["en_neutral"]))
add("T18 EN-framed Egypt vs Egypt anchor", [v - ANCH["Egypt"] for v in CONDS["EN_framed_Egypt"].values()])
add("T19 EN-framed Japan vs Japan anchor", [v - ANCH["Japan"] for v in CONDS["EN_framed_Japan"].values()])
add("T20 AR-neutral vs Egypt anchor", [v - ANCH["Egypt"] for v in CONDS["ar_neutral"].values()])
add("T21 FA-neutral vs Iran anchor", [v - ANCH["Iran"] for v in CONDS["fa_neutral"].values()])
add("T22 EN-framed Nigeria vs Nga anchor", [v - ANCH["Nigeria"] for v in CONDS["EN_framed_Nigeria"].values()])


def holm(names):
    ps = sorted((tests[k][1], k) for k in names)
    m = len(ps)
    out = {}
    run = 0.0
    for i, (p, k) in enumerate(ps):
        run = max(run, p * (m - i))
        out[k] = min(1.0, run)
    return out


h_dec = holm(DECLARED)
h_all = holm(order)

print("\n  %-38s%8s  %-19s%9s%10s%10s" % ("test", "diff", "  95% CI", "exact p", "Holm(10)", "Holm(22)"))
for k in order:
    eff, p, d = tests[k]
    lo, hi = boot_ci(d, k)
    hd = ("%.4f" % h_dec[k]) if k in h_dec else "-"
    print("  %-38s%+8.3f  [%+.3f,%+.3f]%9.4f%10s%10.4f" % (k, eff, lo, hi, p, hd, h_all[k]))

print("\n  Nulls stated as bounds (the CI is what can be ruled out, not evidence of zero):")
for k in ["T1  Egypt: EN-framed vs AR-framed", "T3  JA-neutral vs Japan anchor",
          "T5  FA-neutral vs EN-neutral", "T11 JA-neutral vs EN-neutral",
          "T12 EN-neutral vs Japan anchor"]:
    eff, p, d = tests[k]
    lo, hi = boot_ci(d, k)
    print("    %-38s |effect| <= %.3f" % (k, max(abs(lo), abs(hi))))

print("\n=== STEP 4. PER-FOUNDATION PANEL MEANS, English conditions (absent from appendix B6) ===")
print("  %-22s%s" % ("condition", "".join("%16s" % g[:14] for g in FOUND)))
for k in ["en_neutral", "EN_framed_Egypt", "EN_framed_Japan", "EN_framed_Iran", "EN_framed_Nigeria"]:
    if k not in FCONDS:
        continue
    row = dict((g, mean([FCONDS[k][m][g] for m in FCONDS[k]])) for g in FOUND)
    print("  %-22s%s" % (k, "".join("%16.3f" % row[g] for g in FOUND)))
print("  in-language cells, recomputed for cross-check against B6:")
for k in ["ar_framed_Egypt", "ar_neutral", "ja_framed_Japan", "ja_neutral", "fa_framed_Iran", "fa_neutral"]:
    row = dict((g, mean([FCONDS[k][m][g] for m in FCONDS[k]])) for g in FOUND)
    print("  %-22s%s" % (k, "".join("%16.3f" % row[g] for g in FOUND)))
print("  measured anchors:")
for c in ANCH_FOUND:
    print("  %-22s%s" % (c + ", measured", "".join("%16.3f" % ANCH_FOUND[c][g] for g in FOUND)))

print("\n  EN-framed Iran per-foundation error vs the measured Iranian sample:")
for g in FOUND:
    d = [FCONDS["EN_framed_Iran"][m][g] - ANCH_FOUND["Iran"][g] for m in FCONDS["EN_framed_Iran"]]
    lo, hi = boot_ci(d, "EN_framed_Iran_vs_anchor::" + g)
    print("    %-18s%+8.3f  [%+.3f,%+.3f]  p=%.4f" % (g, mean(d), lo, hi, signflip_exact(d)))

print("\n=== STEP 5. CLAIM CHECKS ===")

print('\n  C1. "an overshoot of +1.26, the largest we have measured on any country"')
print("      Overshoot is computable only where a published human mean exists.")
for c in ["Egypt", "Japan", "Nigeria", "Iran"]:
    k = "EN_framed_" + c
    if k in CONDS:
        mu = mean(list(CONDS[k].values()))
        print("      EN-framed %-8s %.3f vs anchor %.3f  overshoot %+.3f" % (c, mu, ANCH[c], mu - ANCH[c]))
noanch = [c for c in ["India", "Sweden", "United States"] if "EN_framed_" + c in CONDS]
print("      No anchor in the MFQ-2 19-nation set, so not comparable: %s" % ", ".join(noanch))

print('\n  C2. B6 prose vs table: JA-framed panel Care')
vals = [FCONDS["ja_framed_Japan"][m]["care"] for m in FCONDS["ja_framed_Japan"]]
lo, hi = boot_ci(vals, "C2:ja_framed_care")
print("      JA-framed Care = %.4f  CI[%.3f,%.3f]   (table says 4.28, prose says 4.29)" % (mean(vals), lo, hi))
d = [v - ANCH_FOUND["Japan"]["care"] for v in vals]
lo, hi = boot_ci(d, "C2:ja_framed_care_vs_anchor")
print("      above measured Japanese Care 3.03 by %+.3f [%+.3f,%+.3f]  (prose says +1.26 [+1.09,+1.45])"
      % (mean(d), lo, hi))

print('\n  C3. Care span across all conditions run')
allc = {}
for k in sorted(FCONDS):
    vals = [FCONDS[k][m]["care"] for m in FCONDS[k]]
    allc[k] = (mean(vals), boot_ci(vals, "C3:" + k)[0])
lowk = min(allc, key=lambda k: allc[k][0])
hik = max(allc, key=lambda k: allc[k][0])
print("      %d conditions; Care spans %.3f (%s) to %.3f (%s)" % (len(allc), allc[lowk][0], lowk, allc[hik][0], hik))
print("      lowest CI floor across conditions: %.3f  (prose says every floor >= 4.11)"
      % min(v[1] for v in allc.values()))

print('\n  C4. "disagreeing less about what an Egyptian is than about what they themselves are"')
for k in ["EN_framed_Egypt", "ar_framed_Egypt", "en_neutral"]:
    v = list(CONDS[k].values())
    mu = mean(v)
    print("      %-20s between-model SD %.3f" % (k, (sum((x - mu) ** 2 for x in v) / len(v)) ** 0.5))

print('\n  C5. Iran anchor sensitivity (anchors_iran.json gives two samples)')
for lab, a in [("s2, n=989 (used)", 3.333), ("s1, n=392", 3.231),
               ("n-weighted pool", (392 * 3.231 + 989 * 3.333) / 1381)]:
    print("      anchor %.3f (%s): EN-framed overshoot %+.3f, FA-framed %+.3f"
          % (a, lab, mean(list(CONDS["EN_framed_Iran"].values())) - a,
             mean(list(CONDS["fa_framed_Iran"].values())) - a))

print('\n  C6. Leave-one-model-out on the headline quantities')
for k, a in [("ja_neutral", ANCH["Japan"]), ("EN_framed_Iran", ANCH["Iran"])]:
    v = CONDS[k]
    s = [mean([x for mm, x in v.items() if mm != m]) for m in v]
    print("      %-18s panel mean spans %.3f to %.3f  (vs anchor %.3f: %+.3f to %+.3f)"
          % (k, min(s), max(s), a, min(s) - a, max(s) - a))
ms = sorted(set(CONDS["ja_neutral"]) & set(CONDS["en_neutral"]))
s = [mean([CONDS["ja_neutral"][m] - CONDS["en_neutral"][m] for m in ms if m != drop]) for drop in ms]
print("      T11 (JA-neutral vs EN-neutral) leave-one-model-out spans %+.4f to %+.4f" % (min(s), max(s)))

print("\n  C7. Per-model sign counts on the three claims that rest on direction")
for lab, k in [("T11 JA-neutral - EN-neutral", None)]:
    d = [CONDS["ja_neutral"][m] - CONDS["en_neutral"][m] for m in ms]
    print("      %-30s positive %d/%d, negative %d/%d"
          % (lab, sum(1 for x in d if x > 0), len(d), sum(1 for x in d if x < 0), len(d)))
for lab, a, b in [("T6 AR-neutral - EN-neutral", "ar_neutral", "en_neutral"),
                  ("T5 FA-neutral - EN-neutral", "fa_neutral", "en_neutral")]:
    d = paired(CONDS[a], CONDS[b])
    print("      %-30s positive %d/%d, negative %d/%d"
          % (lab, sum(1 for x in d if x > 0), len(d), sum(1 for x in d if x < 0), len(d)))
