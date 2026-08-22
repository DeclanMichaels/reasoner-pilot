#!/usr/bin/env python3
"""Decompose the English unframed baseline into the two things it currently confounds.

Family B asks whether answering in the local language moves the instrument. Every
in-language unframed cell was collected with the OFFICIAL Atari et al. translation and
NO system prompt. The English cell it is compared against was collected with OUR
transcription of the English MFQ-2 and WITH a self-report system prompt. Two differences
ride along with the language difference, and neither has been measured.

This runs the full 2x2 so both can be priced:

    instrument  x  system prompt
    ------------------------------------------------------------
    mfq2        x  self-report SYSTEM   replicates the published baseline
    mfq2_en     x  self-report SYSTEM   prices the instrument on its own
    mfq2        x  none                 prices the system prompt on its own
    mfq2_en     x  none                 the matched comparator for family B

Everything else mirrors run_framed_lang.py exactly, because that is what the
in-language arms were run under: same seed base, same shuffle key, same parse, same
resume rule, same output schema. The published cells in validity/runs/ used a different
seed base and shuffle key, so cell 1 is re-run here rather than reused; comparing it to
the published 2.713 also prices the convention change itself.

    python3 validity/run_english_baseline.py --plan
    python3 validity/run_english_baseline.py
"""
import argparse, glob, json, os, random, sys, time
from pathlib import Path

VDIR = Path(__file__).resolve().parent
sys.path.insert(0, str(VDIR))
import run_validity as rv
rr = rv.rr

OUT = VDIR / "runs_english_baseline"

# The self-report system prompt as run_validity.py sends it. Imported rather than
# retyped so it cannot drift from what the published cells actually received.
SELF_REPORT = rv.SYSTEM
NO_SYSTEM = ""

# (condition name, instrument, system prompt)
CELLS = [
    ("ours_selfreport",     "mfq2",    SELF_REPORT),
    ("official_selfreport", "mfq2_en", SELF_REPORT),
    ("ours_nosystem",       "mfq2",    NO_SYSTEM),
    ("official_nosystem",   "mfq2_en", NO_SYSTEM),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="")
    ap.add_argument("--iters", type=int, default=5)
    ap.add_argument("--plan", action="store_true")
    a = ap.parse_args()

    panel = rr.REG.get("_decisions", {}).get("pilot_roster") or list(rr.REG["models"])
    models = a.models.split(",") if a.models else panel
    bad = [m for m in models if m not in rr.REG["models"]]
    if bad:
        sys.exit(f"unknown model(s): {bad}")

    planned = [(m, ci, it) for m in models for ci in range(len(CELLS))
               for it in range(1, a.iters + 1)]
    OUT.mkdir(parents=True, exist_ok=True)
    done = set()
    for f in glob.glob(str(OUT / "*.json")):
        d = json.load(open(f))
        if d.get("ratings"):
            done.add((d["model"], d["condition"], d["iter"]))
    todo = [(m, ci, it) for (m, ci, it) in planned
            if (m, CELLS[ci][0], it) not in done]
    print(f"panel={len(models)} conds={len(CELLS)} iters={a.iters} "
          f"planned={len(planned)} done={len(planned)-len(todo)} to_run={len(todo)}")
    if a.plan:
        for name, instr, sysp in CELLS:
            print(f"  {name:22s} {instr:8s} system={'self-report' if sysp else 'none'}")
        return

    instrs = {}
    for (_, instr_name, _) in CELLS:
        if instr_name in instrs:
            continue
        instr, missing = rv.load_instrument(instr_name)
        if missing:
            sys.exit(f"[{instr_name}] {len(missing)} empty items")
        instrs[instr_name] = instr
    for key in {rr.REG["models"][m]["env_key"] for m in models}:
        if not os.environ.get(key):
            sys.exit(f"missing env key {key}; aborting before spend")

    for (m, ci, it) in todo:
        cond, instr_name, sys_prompt = CELLS[ci]
        instr = instrs[instr_name]
        bounds = {x["id"]: (instr["scales"][x["scale"]]["min"],
                            instr["scales"][x["scale"]]["max"]) for x in instr["items"]}
        cfg = rr.REG["models"][m]
        seed = 20260722 + it                                  # run_framed_lang's base
        rng = random.Random(f"{m}|{instr_name}|neutral|{it}")  # run_framed_lang's key
        order = list(instr["items"])
        rng.shuffle(order)
        user, id_by_num = rv.build_prompt(instr, order)
        rid = f"{m}_{cond}_{it}"
        try:
            text, usage = rr.call_model(cfg, sys_prompt, user, rid, seed)
        except Exception as e:
            print(f"  ! {rid}: call failed: {e}")
            continue
        ratings, err = rv.parse_ratings(text, id_by_num, bounds)
        ts = time.strftime("%Y%m%dT%H%M%S")
        out = {"model": m, "instrument": instr_name, "condition": cond,
               "language": "english", "country": None, "iter": it, "seed": seed,
               "presentation_order": [id_by_num[str(i + 1)] for i in range(len(id_by_num))],
               "ratings": ratings, "parse_error": err, "usage": usage, "raw_text": text,
               "system_prompt": sys_prompt,
               "instrument_source": "official Atari et al. 2023 OSF supplement"
                                    if instr_name.endswith("_en")
                                    else "our transcription from moralfoundations.org"}
        (OUT / f"{m}_{cond}_{it}_{ts}.json").write_text(json.dumps(out, indent=2))
        print(f"  {rid}: {'OK' if ratings else 'PARSE-FAIL: ' + str(err)}")


if __name__ == "__main__":
    main()
