#!/usr/bin/env python3
"""Rebuild the condition means from the published ratings dataset and compare them to the committed
condition_means.json (decision 19). Needs only this clone: no run files, no keys, no network.

    python3 validity/check_ratings_dataset.py

Exit 0 when every condition in condition_means.json is reproduced to 1e-9 and the dataset has the
expected shape; nonzero otherwise. analysis/test_reproduce.py runs this.
"""
import csv, json, sys
from collections import defaultdict
from pathlib import Path

VDIR = Path(__file__).resolve().parent
BIND = ("loyalty", "authority", "purity")

runs = defaultdict(list)            # (condition, model, iteration) -> ratings
with open(VDIR / "results" / "mfq2_ratings.csv") as fh:
    for r in csv.DictReader(fh):
        runs[(r["condition"], r["model"], int(r["iteration"]))].append((r["item_id"], int(r["rating"])))

SEPT = {"en_neutral_template", "en_neutral_sept", "EN_framed_Egypt_sept"}   # ten models, decision 21
bad = []
if len(runs) != 2750 + 150: bad.append("expected 2900 cells, found %d" % len(runs))
conds = sorted({k[0] for k in runs})
if len(conds) != 53: bad.append("expected 53 conditions, found %d" % len(conds))
for cond in conds:
    ms = {k[1] for k in runs if k[0] == cond}
    want = 10 if cond in SEPT else 11
    if len(ms) != want: bad.append("%s has %d models, expected %d" % (cond, len(ms), want))
for k, items in runs.items():
    if len(items) != 36: bad.append("%s has %d items" % (k, len(items)))

def binding(items):
    v = [x for iid, x in items if iid.split("_")[0] in BIND]
    assert len(v) == 18, k
    return sum(v) / 18

permodel = defaultdict(lambda: defaultdict(list))
for (cond, model, it), items in runs.items():
    permodel[cond][model].append(binding(items))
means = {cond: sum(sum(v) / len(v) for v in md.values()) / len(md) for cond, md in permodel.items()}

pinned = json.load(open(VDIR / "results" / "condition_means.json"))
for cond, exp in sorted(pinned.items()):
    got = means.get(cond)
    if got is None: bad.append("%s missing from the dataset" % cond)
    elif abs(got - exp) > 1e-9: bad.append("%s: dataset %.6f, pinned %.6f" % (cond, got, exp))

n_ok = len(pinned) - sum(1 for b in bad if ":" in b or "missing" in b)
print("  ratings dataset: %d conditions rebuilt, %d of %d pinned condition means reproduced" % (len(means), n_ok, len(pinned)))
for b in bad: print("  FAIL", b)
sys.exit(1 if bad else 0)
