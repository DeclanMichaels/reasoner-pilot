"""Read the published ratings dataset (decision 19) for the appendix emitters (#71).

    from ratings_dataset import load_cells, load_record

load_cells() returns {condition: {model: [cell, cell, ...]}} with cells in iteration order; each
cell is {"iteration", "instrument", "seed", "ratings"} and ratings is a dict keyed by item id in
the run's presentation order, which is the order the run file recorded. load_record() returns
results/collection_record.json: the facts the emitters need that are not ratings (failed calls,
the parser's rounding audit, the translated instructions as sent), written by
build_ratings_dataset.py from the run files so that a clone needs neither the runs nor the runners.
"""
import csv, json
from collections import defaultdict
from pathlib import Path

VDIR = Path(__file__).resolve().parent
DATASET = VDIR / "results" / "mfq2_ratings.csv"
RECORD = VDIR / "results" / "collection_record.json"


def load_cells(path=DATASET):
    rows = defaultdict(list)
    with open(path) as fh:
        for r in csv.DictReader(fh):
            rows[(r["condition"], r["model"], int(r["iteration"]))].append(
                (int(r["position"]), r["item_id"], int(r["rating"]), r["instrument"], r["seed"]))
    out = defaultdict(lambda: defaultdict(list))
    for (cond, model, it), items in sorted(rows.items()):
        items.sort()
        out[cond][model].append({"iteration": it, "instrument": items[0][3],
                                 "seed": int(items[0][4]) if items[0][4] else None,
                                 "ratings": {iid: v for _, iid, v, _, _ in items}})
    return {c: dict(md) for c, md in out.items()}


def load_record(path=RECORD):
    return json.load(open(path))
