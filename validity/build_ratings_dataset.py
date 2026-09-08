#!/usr/bin/env python3
"""Write every scored rating in the in-language MFQ-2 grid as one tidy CSV (decision 19).

    python3 validity/build_ratings_dataset.py > validity/results/mfq2_ratings.csv

One row per (condition, model, iteration, item): the integer rating, the item's position in that
run's shuffled presentation order, the instrument file the run used and the request seed. No item
wording, no system prompt, no model reply: the run files carrying those stay gitignored (decision 7).
Condition keys are the ones condition_means.json and appendix B3a use. Standard library only.
"""
import csv, glob, json, sys
from pathlib import Path

VDIR = Path(__file__).resolve().parent

# (glob, key function) - the same four sources and keys as audit_inlanguage.py
def _lang(d):
    return "%s_%s" % (d["instrument"].split("_")[1],
                      "framed_" + d["country"] if d["condition"] == "framed" else "neutral")
def _enfr(d):
    return "EN_framed_" + d["country"]
def _base(d):
    return "en_neutral" if d["condition"] == "official_nosystem" else "en_baseline_" + d["condition"]
def _old(d):
    return "en_neutral_ours"
SOURCES = [("runs_framed_lang/*.json", _lang), ("runs_framed/*_mfq2_*.json", _enfr),
           ("runs_english_baseline/*.json", _base), ("runs/*mfq2*.json", _old)]

rows = []
for pat, keyf in SOURCES:
    for f in sorted(glob.glob(str(VDIR / pat))):
        d = json.load(open(f))
        if not d.get("ratings"):
            continue                       # unparsed reply, retried; enters no number
        cond = keyf(d)
        order = d["presentation_order"]
        assert len(order) == 36 and set(order) == set(d["ratings"]), f
        pos = {iid: i + 1 for i, iid in enumerate(order)}
        for iid, v in d["ratings"].items():
            rows.append((cond, d["model"], int(d["iter"]), d["instrument"], d.get("seed"), iid, pos[iid], int(v)))

rows.sort(key=lambda r: (r[0], r[1], r[2], r[6]))
cells = {(r[0], r[1], r[2]) for r in rows}
conds = {r[0] for r in rows}
assert len(conds) == 50, len(conds)
assert len(cells) == 2750, len(cells)
assert all(sum(1 for c in cells if c[0] == k) == 55 for k in conds), "a condition without 11 x 5 cells"
assert len(rows) == 99000, len(rows)

w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(["condition", "model", "iteration", "instrument", "seed", "item_id", "position", "rating"])
w.writerows(rows)
print("wrote %d rows, %d cells, %d conditions" % (len(rows), len(cells), len(conds)), file=sys.stderr)
