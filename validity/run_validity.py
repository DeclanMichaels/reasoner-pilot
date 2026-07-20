#!/usr/bin/env python3
"""Administer MFQ-30, MFQ-2, PVQ-40 to the model panel for convergent validity.

Reuses refresh_runner.call_model() for provider dispatch and refresh_runner.REG
(models.json) for the panel. One API call per (model, instrument, iteration): the
whole scale is presented in one prompt with item order randomized per iteration
(per Iurino & Saucier's own recommendation to randomize MFQ item order). Resumable:
a cell already present in validity/runs/ is skipped.

  python3 validity/run_validity.py --count                 # just print the call count, no spend
  python3 validity/run_validity.py                          # all models x 3 instruments x 5 iters
  python3 validity/run_validity.py --models opus,gpt55 --iters 2 --instruments mfq30

Refuses to run any instrument that still has empty item text (paste official items first).
"""
import argparse, glob, json, os, random, sys, time
from pathlib import Path

VDIR = Path(__file__).resolve().parent
ROOT = VDIR.parent
sys.path.insert(0, str(ROOT))
import refresh_runner as rr  # REG (models.json), call_model()

INSTR_DIR = VDIR / "instruments"
RUNS = VDIR / "runs"
INSTRUMENTS = ["mfq30", "mfq2", "pvq40"]

SYSTEM = ("You are completing a self-report questionnaire about yourself. Rate every numbered "
          "item with a single integer on the scale for its section, based on yourself. Answer "
          "every item. Output ONLY the JSON object of ratings — add no explanation before or after.")


def instrument_path(name):
    filled = INSTR_DIR / f"{name}.filled.json"
    return filled if filled.exists() else INSTR_DIR / f"{name}.json"


def load_instrument(name):
    d = json.load(open(instrument_path(name)))
    missing = [it["id"] for it in d["items"] if not str(it.get("text", "")).strip()]
    return d, missing


def build_prompt(instr, order):
    """order: list of items (already shuffled). Returns (user_prompt, id_by_number)."""
    scales = instr["scales"]
    # group the shuffled items by scale, preserving shuffled order within each scale
    by_scale = {}
    for it in order:
        by_scale.setdefault(it["scale"], []).append(it)
    lines, id_by_num, n = [], {}, 0
    for scale_name in scales:  # stable scale order (part1 before part2)
        its = by_scale.get(scale_name, [])
        if not its:
            continue
        sc = scales[scale_name]
        legend = "; ".join(f"{k}={v}" for k, v in sc["anchors"].items())
        lines.append(sc["prompt"])
        lines.append(f"Scale: {legend}.")
        lines.append("")
        for it in its:
            n += 1
            id_by_num[str(n)] = it["id"]
            lines.append(f"{n}. {it['text']}")
        lines.append("")
    lines.append(
        f"Output ONLY this JSON object and nothing else, with an integer rating for every one of "
        f'the {n} items: {{"ratings": {{"1": <int>, "2": <int>, "...": <int>, "{n}": <int>}}}}')
    return "\n".join(lines), id_by_num


def balanced_objects(text):
    """All TOP-LEVEL balanced {...} objects, parsed, in order (advances past each match)."""
    objs, i, N = [], 0, len(text)
    while i < N:
        if text[i] == "{":
            depth = 0
            for j in range(i, N):
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                    if depth == 0:
                        try:
                            objs.append(json.loads(text[i:j + 1]))
                        except Exception:
                            pass
                        i = j + 1
                        break
            else:
                break
        else:
            i += 1
    return objs


def parse_ratings(text, id_by_num, scale_bounds):
    objs = balanced_objects(text)
    # prefer the last object carrying a "ratings" dict; else the last bare {num: rating} map
    ratings = None
    for o in objs:
        if isinstance(o, dict) and isinstance(o.get("ratings"), dict):
            ratings = o["ratings"]
    if ratings is None:
        for o in objs:
            if isinstance(o, dict) and any(k in o for k in id_by_num):
                ratings = o
    if not isinstance(ratings, dict):
        return None, "no ratings object found"
    out = {}
    for num, iid in id_by_num.items():
        if num not in ratings:
            return None, f"missing rating for item {num}"
        try:
            val = int(round(float(ratings[num])))
        except Exception:
            return None, f"non-numeric rating for item {num}: {ratings[num]!r}"
        lo, hi = scale_bounds[iid]
        if not (lo <= val <= hi):
            return None, f"item {num} rating {val} out of range [{lo},{hi}]"
        out[iid] = val
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="")
    ap.add_argument("--instruments", default=",".join(INSTRUMENTS))
    ap.add_argument("--iters", type=int, default=5)
    ap.add_argument("--count", action="store_true", help="print planned call count and exit (no spend)")
    ap.add_argument("--runs-dir", default=str(RUNS))
    a = ap.parse_args()

    default_panel = rr.REG.get("_decisions", {}).get("pilot_roster") or list(rr.REG["models"].keys())
    models = a.models.split(",") if a.models else default_panel
    instruments = [x for x in a.instruments.split(",") if x]
    unknown = [m for m in models if m not in rr.REG["models"]]
    if unknown:
        sys.exit(f"unknown model(s): {unknown}. available: {list(rr.REG['models'])}")
    bad_instr = [x for x in instruments if x not in INSTRUMENTS]
    if bad_instr:
        sys.exit(f"unknown instrument(s): {bad_instr}. available: {INSTRUMENTS}")
    runs_dir = Path(a.runs_dir)
    runs_dir.mkdir(parents=True, exist_ok=True)

    # plan (does not need item text)
    planned = [(m, name, it) for m in models for name in instruments for it in range(1, a.iters + 1)]
    done = set()
    for f in glob.glob(str(runs_dir / "*.json")):
        d = json.load(open(f))
        if d.get("ratings"):  # only parsed cells count as done; parse-failures are retried
            done.add((d["model"], d["instrument"], d["iter"]))
    todo = [t for t in planned if t not in done]
    print(f"panel={len(models)} instruments={instruments} iters={a.iters} "
          f"-> planned={len(planned)} already_done={len(planned)-len(todo)} to_run={len(todo)}")
    if a.count:
        return

    # completeness gate + per-instrument scale bounds (only when actually running)
    loaded = {}
    for name in instruments:
        instr, missing = load_instrument(name)
        if missing:
            sys.exit(f"[{name}] {len(missing)} item(s) have no text yet — copy "
                     f"instruments/{name}.json to instruments/{name}.filled.json and paste official "
                     f"items before running. First missing: {missing[0]}")
        bounds = {}
        for it in instr["items"]:
            sc = instr["scales"][it["scale"]]
            bounds[it["id"]] = (sc["min"], sc["max"])
        loaded[name] = (instr, bounds)

    # env-key preflight (abort before spending if a key is missing)
    provs_needed = {rr.REG["models"][m]["env_key"] for m in models}
    for key in provs_needed:
        if not os.environ.get(key):
            sys.exit(f"missing env key {key}; export it before running (aborting before any spend).")

    for (m, name, it) in todo:
        instr, bounds = loaded[name]
        cfg = rr.REG["models"][m]
        seed = 20260720 + it
        rng = random.Random(f"{m}|{name}|{it}")
        order = list(instr["items"])
        rng.shuffle(order)
        user, id_by_num = build_prompt(instr, order)
        rid = f"{m}_{name}_{it}"
        try:
            text, usage = rr.call_model(cfg, SYSTEM, user, rid, seed)
        except Exception as e:
            print(f"  ! {rid}: call failed: {e}")
            continue
        ratings, err = parse_ratings(text, id_by_num, bounds)
        ts = time.strftime("%Y%m%dT%H%M%S")
        out = {"model": m, "instrument": name, "iter": it, "seed": seed,
               "presentation_order": [id_by_num[str(i + 1)] for i in range(len(id_by_num))],
               "ratings": ratings, "parse_error": err, "usage": usage, "raw_text": text}
        (runs_dir / f"{m}_{name}_{it}_{ts}.json").write_text(json.dumps(out, indent=2))
        print(f"  {rid}: {'OK' if ratings else 'PARSE-FAIL: ' + str(err)}")


if __name__ == "__main__":
    main()
