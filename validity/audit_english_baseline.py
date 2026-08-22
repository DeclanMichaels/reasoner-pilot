#!/usr/bin/env python3
"""Price the two things the English unframed baseline confounds, then redo family B.

Family B asks whether answering in the local language moves the instrument. Its English
comparator differed from the in-language arms in two ways at once, neither measured:
our transcription of the MFQ-2 rather than the official Atari et al. English, and a
self-report system prompt rather than none. run_english_baseline.py collected the 2x2.
This reads it.

Conventions are audit_inlanguage.py's: the model is the independent unit, iterations
averaged before any test, exact sign-flip permutation over 2^11 = 2048 patterns, so the
smallest attainable two-sided p is 2/2048 = 0.001, percentile bootstrap of 100,000 draws
resampling models, each interval seeded from the run seed plus the quantity's own name.

    python3 validity/audit_english_baseline.py > validity/results/english_baseline_audit.txt
"""
import json, glob, random, itertools
from pathlib import Path
from collections import defaultdict

VDIR = Path(__file__).resolve().parent
FOUND = ["care", "equality", "proportionality", "loyalty", "authority", "purity"]
BIND = ["loyalty", "authority", "purity"]
SEED = 20260723
B = 100_000


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


def signflip(pairs, key):
    """Exact sign-flip permutation on the per-model differences. Paired by model, so
    every model contributes one difference and the null is that its sign is arbitrary."""
    d = [b - a for a, b in pairs]
    n = len(d)
    obs = abs(mean(d))
    hits = sum(1 for signs in itertools.product((1, -1), repeat=n)
               if abs(mean([s * x for s, x in zip(signs, d)])) >= obs - 1e-12)
    p = hits / (2 ** n)
    lo, hi = boot(d, key)
    return mean(d), lo, hi, p, sum(1 for x in d if x > 0), sum(1 for x in d if x < 0)


def holm(named):
    """Holm step-down, enforcing monotonicity: an adjusted p can never fall below the
    adjusted p of a test with a smaller raw p."""
    m, run, res = len(named), 0.0, {}
    for i, (name, p) in enumerate(sorted(named, key=lambda x: x[1])):
        run = max(run, min(1.0, p * (m - i)))
        res[name] = run
    return res


# ---- load the 2x2
cells = defaultdict(lambda: defaultdict(list))
for f in glob.glob(str(VDIR / "runs_english_baseline" / "*.json")):
    d = json.load(open(f))
    if not d.get("ratings"):
        continue
    b = binding(d["ratings"])
    if b is not None:
        cells[d["condition"]][d["model"]].append(b)
C = {k: {m: mean(v) for m, v in md.items()} for k, md in cells.items()}

# ---- the published English cell, for the convention check
pub = defaultdict(list)
for f in glob.glob(str(VDIR / "runs" / "*_mfq2_*.json")):
    d = json.load(open(f))
    if d.get("ratings"):
        b = binding(d["ratings"])
        if b is not None:
            pub[d["model"]].append(b)
PUB = {m: mean(v) for m, v in pub.items()}

# ---- the in-language unframed arms
lang = defaultdict(lambda: defaultdict(list))
for f in glob.glob(str(VDIR / "runs_framed_lang" / "*.json")):
    d = json.load(open(f))
    if d["condition"] != "neutral" or not d.get("ratings"):
        continue
    b = binding(d["ratings"])
    if b is not None:
        lang[d["instrument"]][d["model"]].append(b)
L = {k: {m: mean(v) for m, v in md.items()} for k, md in lang.items()}
LANGNAME = {"mfq2_ar": "Arabic", "mfq2_es": "Spanish", "mfq2_fa": "Farsi",
            "mfq2_fr": "French", "mfq2_ja": "Japanese", "mfq2_ru": "Russian"}

ROSTER = sorted(set(PUB) & set.intersection(*[set(v) for v in C.values()]))

print("=== THE 2x2 ===\n")
print("Instrument: 'ours' is our transcription from moralfoundations.org, 'official' is the")
print("Atari et al. 2023 OSF supplement English. System: 'self-report' is the prompt")
print("run_validity.py sends, 'none' is the empty system prompt every in-language arm got.\n")
print("| cell | instrument | system | panel mean | 95% CI | SD | n |")
print("|---|---|---|--:|:--:|--:|--:|")
LABEL = {"ours_selfreport": ("ours", "self-report"),
         "official_selfreport": ("official", "self-report"),
         "ours_nosystem": ("ours", "none"),
         "official_nosystem": ("official", "none")}
for k in ["ours_selfreport", "official_selfreport", "ours_nosystem", "official_nosystem"]:
    if k not in C:
        print("| %s | | | not collected |" % k)
        continue
    v = [C[k][m] for m in ROSTER]
    lo, hi = boot(v, k)
    print("| %s | %s | %s | %.3f | [%.3f, %.3f] | %.2f | %d |"
          % (k, LABEL[k][0], LABEL[k][1], mean(v), lo, hi, sd(v), len(v)))
pv = [PUB[m] for m in ROSTER]
lo, hi = boot(pv, "published_en_neutral")
print("| published en_neutral | ours | self-report | %.3f | [%.3f, %.3f] | %.2f | %d |"
      % (mean(pv), lo, hi, sd(pv), len(pv)))

print("\n\n=== WHAT EACH DIFFERENCE IS WORTH ===\n")
print("Paired by model, exact sign-flip over 2^%d patterns. Holm across the four.\n" % len(ROSTER))
TESTS = [
    ("E1 instrument, holding the system prompt", "ours_selfreport", "official_selfreport"),
    ("E2 system prompt, holding the instrument", "ours_selfreport", "ours_nosystem"),
    ("E3 both at once", "ours_selfreport", "official_nosystem"),
    ("E4 convention: seed and shuffle only", None, "ours_selfreport"),
]
res, raw = {}, {}
for name, a, b in TESTS:
    if b not in C:
        continue
    A = PUB if a is None else C[a]
    pairs = [(A[m], C[b][m]) for m in ROSTER]
    raw[name] = signflip(pairs, name)
ph = holm([(n, r[3]) for n, r in raw.items()])
for name, (d, lo, hi, p, up, dn) in raw.items():
    print("  %-42s diff=%+.3f CI[%+.3f,%+.3f]  p=%.4f  holm=%.4f  up %d/%d down %d/%d"
          % (name, d, lo, hi, p, ph[name], up, len(ROSTER), dn, len(ROSTER)))

print("\n\n=== FAMILY B REDONE ===\n")
if "official_nosystem" not in C:
    print("  official_nosystem not collected yet; cannot run.")
else:
    comp = C["official_nosystem"]
    print("Comparator is the official English translation with no system prompt, which is")
    print("what every in-language unframed arm received. Six tests, Holm across the six.\n")
    braw = {}
    for instr in sorted(L):
        nm = "%s unframed vs English unframed" % LANGNAME.get(instr, instr)
        pairs = [(comp[m], L[instr][m]) for m in ROSTER if m in L[instr]]
        braw[nm] = signflip(pairs, nm)
    bh = holm([(n, r[3]) for n, r in braw.items()])
    for nm, (d, lo, hi, p, up, dn) in sorted(braw.items(), key=lambda x: x[1][3]):
        print("  %-42s diff=%+.3f CI[%+.3f,%+.3f]  p=%.4f  holm=%.4f  up %d down %d"
              % (nm, d, lo, hi, p, bh[nm], up, dn))
    print("\n  Same six tests against the OLD comparator, for comparison:\n")
    old = PUB
    oraw = {}
    for instr in sorted(L):
        nm = "%s unframed vs English unframed" % LANGNAME.get(instr, instr)
        pairs = [(old[m], L[instr][m]) for m in ROSTER if m in L[instr]]
        oraw[nm] = signflip(pairs, nm + "|old")
    oh = holm([(n, r[3]) for n, r in oraw.items()])
    for nm, (d, lo, hi, p, up, dn) in sorted(oraw.items(), key=lambda x: x[1][3]):
        print("  %-42s diff=%+.3f CI[%+.3f,%+.3f]  p=%.4f  holm=%.4f  up %d down %d"
              % (nm, d, lo, hi, p, oh[nm], up, dn))
    print("\n  Movement in each language's estimate when the comparator is fixed:\n")
    for nm in sorted(braw):
        print("    %-42s %+.3f -> %+.3f   (%+.3f)"
              % (nm, oraw[nm][0], braw[nm][0], braw[nm][0] - oraw[nm][0]))

print("\n\n=== PER MODEL, ALL FOUR CELLS ===\n")
print("| model | " + " | ".join(k for k in ["ours_selfreport", "official_selfreport",
                                            "ours_nosystem", "official_nosystem"] if k in C) + " |")
print("|---" * (1 + len([k for k in LABEL if k in C])) + "|")
for m in ROSTER:
    print("| %s | %s |" % (m, " | ".join("%.3f" % C[k][m] for k in
          ["ours_selfreport", "official_selfreport", "ours_nosystem", "official_nosystem"]
          if k in C)))
