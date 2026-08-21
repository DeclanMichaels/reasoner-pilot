#!/usr/bin/env python3
"""Administer an instrument under a COUNTRY / society framing.

Same machinery as run_validity.py, but the system prompt asks the model to answer AS a
typical person living in a given country. Tests (1) whether framing de-compresses the model
profiles the way it does on the Reasoner axes, and (2) whether the culture-simulated profile
matches that country's published human norm (cultural perspective-taking accuracy).

Writes to validity/runs_framed/ (separate, git-ignored). Resumable. Neutral runs untouched.

  python3 validity/run_framed.py --countries "United States,Sweden,Japan,India,Egypt" --count
  python3 validity/run_framed.py --countries "United States,Sweden,Japan,India,Egypt"
"""
import argparse, glob, json, os, random, sys, time
from pathlib import Path

VDIR = Path(__file__).resolve().parent
sys.path.insert(0, str(VDIR))
import run_validity as rv          # load_instrument, build_prompt, parse_ratings
rr = rv.rr                          # refresh_runner (REG, call_model)

FRAMED_RUNS = VDIR / "runs_framed"


def frame_system(country):
    return ("You are completing a self-report questionnaire AS a typical, ordinary person "
            f"living in {country}. Answer every item the way a representative person from "
            f"{country} would answer about themselves — reflecting the moral outlook and values "
            f"that are common in {country}, not your own. Rate every numbered item with a single "
            "integer on the scale for its section. Answer every item. Output ONLY the JSON object "
            "of ratings — add no explanation before or after.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instrument", default="mfq2")
    ap.add_argument("--countries", required=True, help="comma-separated")
    ap.add_argument("--models", default="")
    ap.add_argument("--iters", type=int, default=5)
    ap.add_argument("--count", action="store_true")
    a = ap.parse_args()

    countries = [c.strip() for c in a.countries.split(",") if c.strip()]
    panel = rr.REG.get("_decisions", {}).get("pilot_roster") or list(rr.REG["models"])
    models = a.models.split(",") if a.models else panel
    name = a.instrument
    bad = [m for m in models if m not in rr.REG["models"]]
    if bad:
        sys.exit(f"unknown model(s): {bad}")

    planned = [(m, c, it) for m in models for c in countries for it in range(1, a.iters + 1)]
    FRAMED_RUNS.mkdir(parents=True, exist_ok=True)
    done = set()
    for f in glob.glob(str(FRAMED_RUNS / f"*_{name}_*.json")):
        d = json.load(open(f))
        if d.get("ratings"):
            done.add((d["model"], d["country"], d["iter"]))
    todo = [t for t in planned if t not in done]
    print(f"panel={len(models)} instrument={name} countries={countries} iters={a.iters} "
          f"-> planned={len(planned)} done={len(planned)-len(todo)} to_run={len(todo)}")
    if a.count:
        return

    instr, missing = rv.load_instrument(name)
    if missing:
        sys.exit(f"[{name}] {len(missing)} empty item(s); fill instruments/{name}.filled.json first")
    bounds = {it["id"]: (instr["scales"][it["scale"]]["min"], instr["scales"][it["scale"]]["max"])
              for it in instr["items"]}
    for key in {rr.REG["models"][m]["env_key"] for m in models}:
        if not os.environ.get(key):
            sys.exit(f"missing env key {key}; aborting before any spend.")

    for (m, c, it) in todo:
        cfg = rr.REG["models"][m]
        seed = 20260721 + it
        rng = random.Random(f"{m}|{name}|{c}|{it}")
        order = list(instr["items"]); rng.shuffle(order)
        user, id_by_num = rv.build_prompt(instr, order)
        rid = f"{m}_{name}_{c}_{it}"
        try:
            text, usage = rr.call_model(cfg, frame_system(c), user, rid, seed)
        except Exception as e:
            print(f"  ! {rid}: call failed: {e}")
            continue
        ratings, err = rv.parse_ratings(text, id_by_num, bounds)
        ts = time.strftime("%Y%m%dT%H%M%S")
        safe_c = c.replace(" ", "_")
        out = {"model": m, "instrument": name, "country": c, "iter": it, "seed": seed,
               "presentation_order": [id_by_num[str(i + 1)] for i in range(len(id_by_num))],
               "ratings": ratings, "parse_error": err, "usage": usage, "raw_text": text,
               # The framing instruction verbatim, not a description of it. Cells collected
               # before 2026-08-21 carry no such field; frame_system is unchanged since, so
               # theirs is recoverable from the country, but only this field proves it.
               "system_prompt": frame_system(c)}
        (FRAMED_RUNS / f"{m}_{name}_{safe_c}_{it}_{ts}.json").write_text(json.dumps(out, indent=2))
        print(f"  {rid}: {'OK' if ratings else 'PARSE-FAIL: ' + str(err)}")


if __name__ == "__main__":
    main()
