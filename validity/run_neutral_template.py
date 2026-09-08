#!/usr/bin/env python3
"""The September wave: the framing template with its country slots removed, plus a drift check.

Three English conditions, eleven models x five iterations, 165 cells (decision 21, ticket #83):

    neutral_template        mfq2_en   the framing template with " living in {country}",
                                      " from {country}" and " in {country}" deleted; nothing added
    official_nosystem_sept  mfq2_en   the unframed comparator rerun, same seeds and shuffle key as
                                      run_english_baseline.py's official_nosystem, so item order matches
    framed_egypt_sept       mfq2      English-framed Egypt rerun, same seeds and shuffle key as
                                      run_framed.py, so item order matches the August cell

No temperature is sent, to match the August grid (the standing set-and-record rule is set aside
here on purpose: sending one would put temperature and window into the same contrast). Any
temperature a provider reports in its response body is recorded; none is expected.

    python3 validity/run_neutral_template.py --plan
    python3 validity/run_neutral_template.py --models deepseek_v4 --iters 2 --cells neutral_template   # preflight
    python3 validity/run_neutral_template.py
"""
import argparse, glob, json, os, random, sys, time
from pathlib import Path

VDIR = Path(__file__).resolve().parent
sys.path.insert(0, str(VDIR))
import run_validity as rv
import run_framed as rf
rr = rv.rr

OUT = VDIR / "runs_neutral_template"
WAVE = "2026-09"

# Derived from the framing template in run_framed.py by deleting the country slots, and asserted
# against the literal, so the appendix can quote it from source and it cannot drift.
_S = "␀"
NEUTRAL_TEMPLATE = (rf.frame_system(_S).replace(" living in " + _S, "").replace(" from " + _S, "")
                    .replace(" in " + _S, ""))
assert _S not in NEUTRAL_TEMPLATE
assert NEUTRAL_TEMPLATE == (
    "You are completing a self-report questionnaire AS a typical, ordinary person. Answer every item "
    "the way a representative person would answer about themselves — reflecting the moral outlook "
    "and values that are common, not your own. Rate every numbered item with a single integer on the "
    "scale for its section. Answer every item. Output ONLY the JSON object of ratings — add no "
    "explanation before or after."), NEUTRAL_TEMPLATE

# (condition, instrument, system prompt, seed base, shuffle-key function)
CELLS = [
    ("neutral_template",       "mfq2_en", NEUTRAL_TEMPLATE,         20260722, lambda m, it: f"{m}|mfq2_en|neutral_template|{it}"),
    ("official_nosystem_sept", "mfq2_en", "",                       20260722, lambda m, it: f"{m}|mfq2_en|neutral|{it}"),
    ("framed_egypt_sept",      "mfq2",    rf.frame_system("Egypt"), 20260721, lambda m, it: f"{m}|mfq2|Egypt|{it}"),
]

# Keep the provider's response body so any reported temperature can be recorded. refresh_runner
# discards it; wrapping _post here leaves that module untouched for the other runners.
_last = {}
_orig_post = rr._post


def _post_keep(url, headers, body, timeout=180):
    d = _orig_post(url, headers, body, timeout)
    _last["body"] = d
    return d


rr._post = _post_keep


def _reported_temperature(d):
    if not isinstance(d, dict):
        return None
    if "temperature" in d:
        return d["temperature"]
    for sub in ("generationConfig", "parameters", "metadata"):
        if isinstance(d.get(sub), dict) and "temperature" in d[sub]:
            return d[sub]["temperature"]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="")
    ap.add_argument("--cells", default="", help="comma-separated condition names; default all three")
    ap.add_argument("--iters", type=int, default=5)
    ap.add_argument("--plan", action="store_true")
    a = ap.parse_args()

    panel = rr.REG.get("_decisions", {}).get("pilot_roster") or list(rr.REG["models"])
    models = a.models.split(",") if a.models else panel
    bad = [m for m in models if m not in rr.REG["models"]]
    if bad:
        sys.exit(f"unknown model(s): {bad}")
    cells = [c for c in CELLS if not a.cells or c[0] in a.cells.split(",")]

    planned = [(m, c, it) for m in models for c in cells for it in range(1, a.iters + 1)]
    OUT.mkdir(parents=True, exist_ok=True)
    done = set()
    for f in glob.glob(str(OUT / "*.json")):
        d = json.load(open(f))
        if d.get("ratings"):
            done.add((d["model"], d["condition"], d["iter"]))
    todo = [(m, c, it) for (m, c, it) in planned if (m, c[0], it) not in done]
    print(f"panel={len(models)} conds={len(cells)} iters={a.iters} planned={len(planned)} "
          f"done={len(planned)-len(todo)} to_run={len(todo)}")
    if a.plan:
        for name, instr, sysp, base, _ in cells:
            print(f"  {name:24s} {instr:8s} seed base {base} system={'none' if not sysp else sysp[:60] + '...'}")
        return

    instrs = {}
    for (_, instr_name, _, _, _) in cells:
        if instr_name not in instrs:
            instr, missing = rv.load_instrument(instr_name)
            if missing:
                sys.exit(f"[{instr_name}] {len(missing)} empty items")
            instrs[instr_name] = instr
    for key in {rr.REG["models"][m]["env_key"] for m in models}:
        if not os.environ.get(key):
            sys.exit(f"missing env key {key}; aborting before spend")

    for (m, (cond, instr_name, sys_prompt, base, keyf), it) in todo:
        instr = instrs[instr_name]
        bounds = {x["id"]: (instr["scales"][x["scale"]]["min"], instr["scales"][x["scale"]]["max"])
                  for x in instr["items"]}
        cfg = rr.REG["models"][m]
        seed = base + it
        rng = random.Random(keyf(m, it))
        order = list(instr["items"])
        rng.shuffle(order)
        user, id_by_num = rv.build_prompt(instr, order)
        rid = f"{m}_{cond}_{it}"
        _last.clear()
        try:
            text, usage = rr.call_model(cfg, sys_prompt, user, rid, seed)
        except Exception as e:
            print(f"  ! {rid}: call failed: {e}")
            continue
        ratings, err = rv.parse_ratings(text, id_by_num, bounds)
        ts = time.strftime("%Y%m%dT%H%M%S")
        out = {"model": m, "instrument": instr_name, "condition": cond, "wave": WAVE,
               "language": "english", "country": "Egypt" if cond == "framed_egypt_sept" else None,
               "iter": it, "seed": seed,
               "presentation_order": [id_by_num[str(i + 1)] for i in range(len(id_by_num))],
               "ratings": ratings, "parse_error": err, "usage": usage, "raw_text": text,
               "system_prompt": sys_prompt,
               "temperature_sent": None,
               "temperature_reported": _reported_temperature(_last.get("body")),
               "collected": ts,
               "instrument_source": ("official Atari et al. 2023 OSF supplement" if instr_name.endswith("_en")
                                     else "our transcription from moralfoundations.org")}
        (OUT / f"{m}_{cond}_{it}_{ts}.json").write_text(json.dumps(out, indent=2))
        print(f"  {rid}: {'OK' if ratings else 'PARSE-FAIL: ' + str(err)}  temp_reported={out['temperature_reported']}")


if __name__ == "__main__":
    main()
