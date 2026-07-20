#!/usr/bin/env python3
"""Convergent validity: correlate the Reasoner's four neutral axes against MFQ/PVQ
scores across the model panel, testing a PRE-SPECIFIED expected sign pattern.

Reasoner axes (neutral, b12) are read from ../results/viewer_data.json:
  higher value = autonomous (moral_agent), skeptical (authority), narrow (domain_boundary),
  universal (scope).

n = number of models (~11), so correlations are SUGGESTIVE, not confirmatory. The point
is whether the axes move with established frameworks in the pre-registered directions.

  python3 validity/convergent_validity.py            # -> results/convergent_validity.{md,json}
"""
import json, math, sys
from pathlib import Path

VDIR = Path(__file__).resolve().parent
ROOT = VDIR.parent
RES = VDIR / "results"
AXES = ["moral_agent", "authority", "domain_boundary", "scope"]

# Pre-specified expectations (committed before running). Axis in native polarity:
# higher = autonomous / skeptical / narrow / universal.
EXPECTED = [
    ("moral_agent",     "pvq40.self_direction",      "+", "autonomous self <-> self-direction value"),
    ("moral_agent",     "pvq40.openness_to_change",  "+", "autonomous <-> openness to change"),
    ("moral_agent",     "mfq30.binding",             "-", "autonomous <-> weaker binding foundations"),
    ("moral_agent",     "mfq2.loyalty",              "-", "autonomous <-> weaker loyalty"),
    ("authority",       "mfq30.authority",           "-", "skeptical-of-authority <-> lower Authority foundation"),
    ("authority",       "mfq2.authority",            "-", "skeptical <-> lower Authority foundation (MFQ-2)"),
    ("authority",       "pvq40.conservation",        "-", "skeptical <-> lower conservation values"),
    ("authority",       "pvq40.openness_to_change",  "+", "skeptical <-> higher openness"),
    ("domain_boundary", "mfq30.binding",             "-", "narrow domain <-> weaker binding"),
    ("domain_boundary", "mfq30.sanctity",            "-", "narrow <-> lower Sanctity"),
    ("domain_boundary", "mfq30.individualizing",     "+", "narrow <-> individualizing-only morality"),
    ("domain_boundary", "mfq2.purity",               "-", "narrow <-> lower Purity (MFQ-2)"),
    ("scope",           "pvq40.universalism",        "+", "universal obligation <-> universalism value"),
    ("scope",           "pvq40.self_transcendence",  "+", "universal <-> self-transcendence"),
    ("scope",           "mfq30.fairness",            "+", "universal <-> Fairness (individualizing)"),
    ("scope",           "mfq30.loyalty",             "-", "universal <-> lower Loyalty (parochial)"),
    ("scope",           "mfq2.equality",             "+", "universal <-> Equality (MFQ-2)"),
]


def pearson(xs, ys):
    pts = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    n = len(pts)
    if n < 3:
        return None, n
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sx = math.sqrt(sum((p[0] - mx) ** 2 for p in pts))
    sy = math.sqrt(sum((p[1] - my) ** 2 for p in pts))
    if sx == 0 or sy == 0:
        return None, n
    cov = sum((p[0] - mx) * (p[1] - my) for p in pts)
    return cov / (sx * sy), n


def load_axes():
    vd = json.load(open(ROOT / "results" / "viewer_data.json"))
    out = {}
    for m, frames in vd["scores"].items():
        b12 = (frames.get("neutral") or {}).get("b12")
        if b12:
            out[m] = {a: b12.get(a) for a in AXES}
    return out


def metric(scores, model, ref):
    inst, met = ref.split(".", 1)
    return scores.get(model, {}).get(inst, {}).get(met)


def main():
    sp = RES / "instrument_scores.json"
    if not sp.exists():
        sys.exit("results/instrument_scores.json missing — run score_validity.py first.")
    scores = json.load(open(sp))
    axes = load_axes()
    models = sorted(set(scores) & set(axes))
    if len(models) < 3:
        sys.exit(f"only {len(models)} models have both Reasoner axes and instrument scores; run the panel first.")

    # pre-specified pattern. Predictions whose metric was not administered (e.g. MFQ-2 when
    # skipped) yield r=None; they are marked "untested" and excluded from the confirmed ratio
    # rather than counted as failures.
    rows, hits, testable = [], 0, 0
    for axis, ref, sign, why in EXPECTED:
        xs = [axes[m][axis] for m in models]
        ys = [metric(scores, m, ref) for m in models]
        r, n = pearson(xs, ys)
        if r is None:
            ok = None
        else:
            testable += 1
            ok = (r > 0) == (sign == "+")
            hits += 1 if ok else 0
        rows.append({"axis": axis, "metric": ref, "expected": sign, "r": r, "n": n, "match": ok, "rationale": why})
    untested = len(EXPECTED) - testable

    # full exploratory matrix (all axes x all metrics present)
    all_refs = sorted({f"{inst}.{met}" for m in models for inst, d in scores[m].items()
                       for met in d if not met.startswith("_")})
    matrix = {}
    for axis in AXES:
        matrix[axis] = {}
        for ref in all_refs:
            r, n = pearson([axes[m][axis] for m in models], [metric(scores, m, ref) for m in models])
            matrix[axis][ref] = r

    report = {"n_models": len(models), "models": models, "expected": rows, "matrix": matrix,
              "predicted_directions_confirmed": f"{hits}/{testable}",
              "n_testable": testable, "n_untested": untested}
    (RES / "convergent_validity.json").write_text(json.dumps(report, indent=2))

    # markdown
    L = [f"# Convergent validity (model panel, n = {len(models)})", "",
         "Correlations of the four Reasoner axes (neutral, b12) with MFQ-30, MFQ-2, and PVQ-40 "
         "scores across the model panel. Axis polarity: higher = autonomous / skeptical / narrow / "
         f"universal. **n = {len(models)} — suggestive, not confirmatory.**", "",
         (f"**Pre-specified directions confirmed: {hits}/{testable}"
          + (f" — {untested} prediction(s) not administered this run.**" if untested else ".**")), "",
         "## Pre-registered predictions", "",
         "| Reasoner axis | Instrument metric | Predicted | r | n | Direction holds |",
         "|---|---|:--:|--:|:--:|:--:|"]
    for row in rows:
        rr = "n/a" if row["r"] is None else f"{row['r']:+.2f}"
        hold = {None: "untested", True: "yes", False: "no"}[row["match"]]
        L.append(f"| {row['axis']} | {row['metric']} | {row['expected']} | {rr} | {row['n']} | "
                 f"{hold} |")
    L += ["", "## Full correlation matrix (exploratory)", "",
          "| Axis | " + " | ".join(all_refs) + " |",
          "|---|" + "|".join(["--:"] * len(all_refs)) + "|"]
    for axis in AXES:
        cells = ["" if matrix[axis][ref] is None else f"{matrix[axis][ref]:+.2f}" for ref in all_refs]
        L.append(f"| {axis} | " + " | ".join(cells) + " |")
    L += ["", "_Model-panel convergent validity is exploratory (small n; LLM questionnaire responses "
          "have their own validity limits). Human convergent validity requires co-administration in the "
          "confirmatory sample._"]
    (RES / "convergent_validity.md").write_text("\n".join(L))
    print(f"n={len(models)} models | predicted directions confirmed {hits}/{testable}"
          f" ({untested} untested)")
    print("wrote", RES / "convergent_validity.md", "and .json")


if __name__ == "__main__":
    main()
