#!/usr/bin/env python3
"""Score the administered instruments per official keys.

Reads validity/runs/*.json, averages each item's rating across iterations per model,
then computes foundation/value scores:
  - MFQ (mean): foundation = mean of its items; composites = mean of member foundations;
    catch items excluded from scoring but reported as a validity flag.
  - PVQ (ipsative_mean): MRAT = mean of all 40 items per model; value = mean(value items) - MRAT;
    higher-order = mean of member centered values (Schwartz centering for scale-use bias).
Writes validity/results/instrument_scores.json.

  python3 validity/score_validity.py
"""
import glob, json, statistics, sys
from pathlib import Path

VDIR = Path(__file__).resolve().parent
INSTR_DIR = VDIR / "instruments"
RUNS = VDIR / "runs"
OUT = VDIR / "results"
OUT.mkdir(parents=True, exist_ok=True)


def instrument(name):
    filled = INSTR_DIR / f"{name}.filled.json"
    path = filled if filled.exists() else INSTR_DIR / f"{name}.json"
    return json.load(open(path))


def per_item_means(name):
    """{model: {item_id: mean_rating}} averaged over iterations; plus catch flags."""
    acc, catchacc = {}, {}
    for f in sorted(glob.glob(str(RUNS / f"*_{name}_*.json"))):
        d = json.load(open(f))
        if d.get("parse_error") or not d.get("ratings"):
            continue
        m = d["model"]
        for iid, val in d["ratings"].items():
            acc.setdefault(m, {}).setdefault(iid, []).append(val)
    means = {m: {iid: statistics.mean(vs) for iid, vs in items.items()} for m, items in acc.items()}
    return means


def score_mfq(name):
    instr = instrument(name)
    by_group = {}
    for it in instr["items"]:
        by_group.setdefault(it["group"], []).append(it["id"])
    means = per_item_means(name)
    out = {}
    for m, im in means.items():
        founds = {}
        for f in instr["score"]["foundations"]:
            vals = [im[i] for i in by_group.get(f, []) if i in im]
            if vals:
                founds[f] = statistics.mean(vals)
        row = dict(founds)
        for comp, members in instr["score"].get("composites", {}).items():
            ms = [founds[f] for f in members if f in founds]
            if ms:
                row[comp] = statistics.mean(ms)
        # catch validity flag (mean of catch items, if any)
        catch_ids = by_group.get("_catch", [])
        cvals = [im[i] for i in catch_ids if i in im]
        if cvals:
            row["_catch_mean"] = statistics.mean(cvals)
        out[m] = row
    return out


def score_pvq(name):
    instr = instrument(name)
    by_group = {}
    for it in instr["items"]:
        by_group.setdefault(it["group"], []).append(it["id"])
    means = per_item_means(name)
    out = {}
    for m, im in means.items():
        allvals = list(im.values())
        if not allvals:
            continue
        mrat = statistics.mean(allvals)  # Schwartz centering baseline
        vals = {}
        for v in instr["score"]["values"]:
            vs = [im[i] for i in by_group.get(v, []) if i in im]
            if vs:
                vals[v] = statistics.mean(vs) - mrat
        row = dict(vals)
        for hi, members in instr["score"].get("higher_order", {}).items():
            ms = [vals[v] for v in members if v in vals]
            if ms:
                row[hi] = statistics.mean(ms)
        row["_mrat"] = mrat
        out[m] = row
    return out


def main():
    scores = {"mfq30": score_mfq("mfq30"), "mfq2": score_mfq("mfq2"), "pvq40": score_pvq("pvq40")}
    # reshape to {model: {instrument: {...}}}
    models = sorted({m for inst in scores.values() for m in inst})
    by_model = {m: {inst: scores[inst].get(m, {}) for inst in scores} for m in models}
    (OUT / "instrument_scores.json").write_text(json.dumps(by_model, indent=2))
    n_by = {inst: len(d) for inst, d in scores.items()}
    print("scored models per instrument:", n_by)
    print("wrote", OUT / "instrument_scores.json")
    if any(v == 0 for v in n_by.values()):
        print("NOTE: an instrument has 0 scored models — run validity/run_validity.py first (or check parse errors).")


if __name__ == "__main__":
    main()
