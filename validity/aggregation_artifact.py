#!/usr/bin/env python3
"""
Aggregation-artifact check on the pilot's compression ratio.

QUESTION
    The reported compression ratio is human_sd / model_sd, where each model's position is
    the MEAN of k iterations and each human's position is a SINGLE response. Dispersion of
    means is mechanically smaller than dispersion of singletons, so some of the reported
    tightness could be an averaging artifact rather than a property of the models.

METHOD
    For a model position that is the mean of k iterations:
        Var(observed model positions) = Var_between_models + Var_within_model / k
    so the variance those positions would have had as SINGLE draws is
        Var_single = Var_observed + Var_within_model * (1 - 1/k)
    Recompute the ratio against that inflated model SD. This puts models and humans on the
    same footing: one draw each, both carrying their own within-unit noise.

    The mirror correction (removing within-PERSON noise from the human side) is NOT
    computable here: the pilot has no human test-retest. Instead we report the sensitivity,
    i.e. how much of the observed human variance would have to be within-person noise
    before the corrected ratio falls to a given level.

INPUTS   results/appendix_stats.json  (compression + reliability blocks, already computed)
         runs/*.json                  (used only to verify k, the iteration count)
OUTPUT   validity/results/aggregation_artifact.json  and stdout
"""
import json, glob, os, statistics, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS = os.path.join(ROOT, "results", "appendix_stats.json")
OUTDIR = os.path.join(ROOT, "validity", "results")
NAME = {"moral_agent": "Moral Agent", "authority": "Authority",
        "domain_boundary": "Moral Domain", "scope": "Obligation Scope"}


def observed_k():
    """Verify the iteration count from the raw runs rather than assuming it."""
    counts = collections.Counter()
    for p in glob.glob(os.path.join(ROOT, "runs", "*.json")):
        try:
            d = json.load(open(p))
        except Exception:
            continue
        iters = {r.get("iteration", 0) for r in d.get("responses", [])}
        if iters:
            counts[len(iters)] += 1
    return counts


def main():
    d = json.load(open(STATS))
    comp, rel = d["compression"], d["reliability"]
    kc = observed_k()
    k = max(kc, key=kc.get) if kc else None
    print(f"n_human={d.get('n_human')}  n_models={d.get('n_models')}")
    print(f"iteration counts per run file: {dict(kc)}  ->  k = {k}\n")
    if not k or k < 2:
        raise SystemExit("could not verify k; aborting rather than assuming")

    infl = 1.0 - 1.0 / k
    out, rows = {}, []
    for ax in comp:
        h = comp[ax]["human_sd"]
        m = comp[ax]["model_sd"]
        w = rel[ax]["within_run_sd_median"]
        m_single = (m ** 2 + (w ** 2) * infl) ** 0.5
        r_rep, r_cor = h / m, h / m_single
        # share of the OBSERVED between-model variance attributable to un-averaged noise
        share = ((w ** 2) / k) / (m ** 2)
        # sensitivity: within-person SD that would drag the corrected ratio down to 3.0
        h_need = 3.0 * m_single
        var_noise = max(h ** 2 - h_need ** 2, 0.0)
        noise_share = var_noise / (h ** 2)
        out[ax] = {"human_sd": h, "model_sd_reported": m, "within_run_sd": w,
                   "model_sd_as_single_draw": round(m_single, 5),
                   "ratio_reported": round(r_rep, 2), "ratio_corrected": round(r_cor, 2),
                   "pct_change": round(100 * (r_cor - r_rep) / r_rep, 1),
                   "noise_share_of_model_var": round(share, 4),
                   "human_noise_share_needed_for_ratio_3": round(noise_share, 3)}
        rows.append((NAME.get(ax, ax), r_rep, r_cor, out[ax]["pct_change"], noise_share))

    print(f"{'axis':18}{'reported':>10}{'corrected':>11}{'change':>9}"
          f"{'human noise share for ratio 3':>32}")
    for n, a, b, c, ns in rows:
        print(f"{n:18}{a:>10.2f}{b:>11.2f}{c:>8.1f}%{ns:>31.0%}")
    lo, hi = min(r[2] for r in rows), max(r[2] for r in rows)
    print(f"\nreported range  {min(r[1] for r in rows):.2f} to {max(r[1] for r in rows):.2f}")
    print(f"corrected range {lo:.2f} to {hi:.2f}")

    # Independent cross-check: reconstruct model_sd directly from model_scores.csv
    # (neutral frame, b12 subset) and confirm it matches the stats file.
    import csv
    per = collections.defaultdict(dict)
    with open(os.path.join(ROOT, "results", "csv", "model_scores.csv")) as f:
        for r in csv.DictReader(f):
            if r["frame"] == "neutral" and r["subset"] == "b12":
                per[r["axis_id"]][r["model"]] = float(r["score"])
    print("\ncross-check, model_sd recomputed from model_scores.csv:")
    ok = True
    for ax in comp:
        if ax in per and len(per[ax]) > 1:
            v = statistics.pstdev(list(per[ax].values()))
            match = abs(v - comp[ax]["model_sd"]) < 5e-3
            ok &= match
            print(f"  {NAME.get(ax,ax):18} csv {v:.4f}  stats {comp[ax]['model_sd']:.4f}"
                  f"  {'match' if match else 'MISMATCH'}")
    print("  cross-check:", "passed" if ok else "FAILED")

    os.makedirs(OUTDIR, exist_ok=True)
    payload = {"_provenance": {"script": "validity/aggregation_artifact.py",
                               "source": "results/appendix_stats.json",
                               "k_iterations_verified": k,
                               "cross_check_passed": bool(ok)},
               "per_axis": out}
    with open(os.path.join(OUTDIR, "aggregation_artifact.json"), "w") as f:
        json.dump(payload, f, indent=1)
    print(f"\nwrote {os.path.join(OUTDIR,'aggregation_artifact.json')}")


if __name__ == "__main__":
    main()
