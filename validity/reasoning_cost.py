#!/usr/bin/env python3
"""What the reasoning tokens buy, per model. Stdlib only.

Every cell records usage {input, output, reasoning}. This asks three questions of
that field, for each model in the panel, across every scored cell of this collection:

  COST         how many reasoning tokens per call, and what share of everything the
               model generated was reasoning rather than answer.
  DISTINCTNESS how far the model's answer sits from where the rest of the panel landed,
               measured per condition as the gap to the leave-one-out mean of the other
               models. A model that deliberates at length and lands exactly where the
               non-deliberating models land bought no different answer.
  STABILITY    the model's own spread across its five iterations of the same condition.
               Deliberation that does not move the answer might still buy reproducibility;
               if the spread matches the non-reasoning models', it bought neither.

Prints a cost-per-effect column last: reasoning tokens spent per 0.01 of binding-scale
deviation from the panel. That is the waste question in the units of the study.

    python3 validity/reasoning_cost.py
"""
import json, glob
from pathlib import Path
from collections import defaultdict

VDIR = Path(__file__).resolve().parent
FOUND = ["care", "equality", "proportionality", "loyalty", "authority", "purity"]
BIND = ["loyalty", "authority", "purity"]

SOURCES = [
    (VDIR / "runs_framed_lang" / "*.json",
     lambda d: "%s_%s" % (d["instrument"].split("_")[1],
                          d["condition"] if d["condition"] != "framed"
                          else "framed_" + d["country"])),
    (VDIR / "runs_framed" / "*_mfq2_*.json",
     lambda d: ("EN_framed_" + d["country"]) if d.get("country") else None),
    (VDIR / "runs" / "*_mfq2_*.json", lambda d: "en_neutral"),
]


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


def mean(v):
    return sum(v) / len(v)


def sd(v):
    if len(v) < 2:
        return None
    m = mean(v)
    return (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5


# cell[(cond, model)] = list of per-iteration binding values
cells = defaultdict(list)
usage = defaultdict(lambda: {"input": 0, "output": 0, "reasoning": 0, "n": 0})
missing_usage = defaultdict(int)

for pattern, keyfn in SOURCES:
    for f in glob.glob(str(pattern)):
        d = json.load(open(f))
        if not d.get("ratings"):
            continue
        k = keyfn(d)
        if k is None:
            continue
        b = binding(d["ratings"])
        if b is None:
            continue
        m = d["model"]
        cells[(k, m)].append(b)
        u = d.get("usage") or {}
        if not u:
            missing_usage[m] += 1
            continue
        for f2 in ("input", "output", "reasoning"):
            usage[m][f2] += int(u.get(f2) or 0)
        usage[m]["n"] += 1

MODELS = sorted(usage)
CONDS = sorted({k for k, _ in cells})
print("=== SCOPE ===")
print("  models %d, conditions %d, scored cells %d"
      % (len(MODELS), len(CONDS), sum(u["n"] for u in usage.values())))
if missing_usage:
    print("  cells with no usage field: %s" % dict(missing_usage))

# distinctness: per condition, gap to the mean of the OTHER models
gap = defaultdict(list)
for c in CONDS:
    present = {m: mean(cells[(c, m)]) for m in MODELS if (c, m) in cells}
    if len(present) < 3:
        continue
    for m, v in present.items():
        others = [x for mm, x in present.items() if mm != m]
        gap[m].append(abs(v - mean(others)))

# stability: within model, within condition, across iterations
spread = defaultdict(list)
for (c, m), vals in cells.items():
    s = sd(vals)
    if s is not None:
        spread[m].append(s)

rows = []
for m in MODELS:
    u = usage[m]
    n = max(u["n"], 1)
    r_per_call = u["reasoning"] / n
    gen = u["reasoning"] + u["output"]
    share = (u["reasoning"] / gen) if gen else 0.0
    g = mean(gap[m]) if gap.get(m) else float("nan")
    sp = mean(spread[m]) if spread.get(m) else float("nan")
    cost = (u["reasoning"] / (g * 100)) if (g and g == g and g > 0) else float("nan")
    rows.append((m, n, r_per_call, u["output"] / n, share, g, sp, u["reasoning"], cost))

rows.sort(key=lambda r: -r[2])

print("\n=== COST AND WHAT IT BUYS, per model ===")
print("  %-15s %5s %10s %9s %8s %10s %9s %12s %12s"
      % ("model", "cells", "reason/call", "out/call", "reason%", "gap-to-", "own", "total",
         "reason tok"))
print("  %-15s %5s %10s %9s %8s %10s %9s %12s %12s"
      % ("", "", "", "", "of gen", "panel", "spread", "reasoning", "per 0.01 gap"))
for m, n, rpc, opc, share, g, sp, tot, cost in rows:
    gs = "%.3f" % g if g == g else "  -  "
    ss = "%.3f" % sp if sp == sp else "  -  "
    cs = "%,.0f".replace(",", "") % cost if cost == cost else "   -"
    print("  %-15s %5d %10.0f %9.0f %7.0f%% %10s %9s %12d %12s"
          % (m, n, rpc, opc, share * 100, gs, ss, tot, cs))

think = [r for r in rows if r[2] >= 1]
nothink = [r for r in rows if r[2] < 1]
print("\n=== REASONING MODELS VS THE REST ===")
for label, grp in (("reasoning (>0 tok/call)", think), ("no reasoning tokens", nothink)):
    if not grp:
        continue
    print("  %-24s n=%d  mean gap-to-panel %.3f  mean own spread %.3f  mean reason/call %.0f"
          % (label, len(grp), mean([r[5] for r in grp if r[5] == r[5]]),
             mean([r[6] for r in grp if r[6] == r[6]]), mean([r[2] for r in grp])))

# Spearman between reasoning per call and gap to panel
def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    mx, my = mean(rx), mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else float("nan")

valid = [r for r in rows if r[5] == r[5]]
if len(valid) >= 4:
    print("\n=== DOES SPENDING MORE MOVE THE ANSWER? (descriptive, n=%d models) ===" % len(valid))
    print("  Spearman, reasoning per call vs gap to panel:   %+.3f"
          % spearman([r[2] for r in valid], [r[5] for r in valid]))
    print("  Spearman, reasoning per call vs own spread:     %+.3f"
          % spearman([r[2] for r in valid], [r[6] for r in valid]))
    print("  A correlation near zero means the tokens are not buying a different answer")
    print("  or a steadier one. With eleven models this is descriptive, not a test.")
