#!/usr/bin/env python3
"""Regenerate the three CMRB pilot visuals from the raw run data. Stdlib only.

Reads:  <root>/ccas_bank_full.json, <root>/runs_v2/*.json,
        <root>/human-responses/responses/**/*.json, <root>/scenario_bank.py
Writes (to <root>/private/reanalysis/ by default):
  figure_payload.json, radar_payload_v3.json, radar48_payload.json
  compression_radar_v3.html   (68 humans + models on the 12 baseline scenarios)
  model_radar48.html          (models on 4 axes, all 48 scenarios)
  model_strips48.html         (linear range strips, all 48 scenarios)

The HTML templates live next to this file as tpl_*.html with a __PAYLOAD__ marker.
Run:  python3 build_figures.py            (paths resolve to the repo root)
Env:  CMRB_ROOT overrides the scenario-bank root; CMRB_VIZ_OUT overrides output dir.

To render PNGs (optional, needs Node + playwright), point a headless Chromium at
each file:// URL and screenshot fullPage. Not required to produce the HTML.

NOTE ON SIGNS: option pole codings in ccas_bank_full.json must be correct
(pole_a = -1 side, pole_b = +1 side). A global sign inversion was fixed on
2026-07-19; the pre-fix bank is at private/_pre_review/ccas_bank_full.preflip.json.
If the human baseline does NOT read autonomous/skeptical/narrow/universal, the
poles are inverted again and every directional claim will be backwards.
"""
import json, glob, os, random, statistics, sys
from pathlib import Path

ROOT = Path(os.environ.get("CMRB_ROOT", Path(__file__).resolve().parents[2]))
TPL_DIR = Path(__file__).resolve().parent
OUT = Path(os.environ.get("CMRB_VIZ_OUT", ROOT / "private" / "reanalysis"))
sys.path.insert(0, str(ROOT))
from scenario_bank import compute_dimensional_score

random.seed(20260719)
BOOT = 100_000

BANK = json.load(open(ROOT / "ccas_bank_full.json"))
DIMS = [d["id"] for d in BANK["dimensions"]]
DMETA = {d["id"]: d for d in BANK["dimensions"]}
BASE = {s["id"] for s in BANK["scenarios"] if s.get("has_human_baseline")}
DROP = {"gemini3pro", "gemini35flash", "command_a"}   # vendors dropped from the pilot
LAB = {"opus": "Anthropic", "sonnet": "Anthropic", "gpt55": "OpenAI", "o3": "OpenAI",
       "grok45": "xAI", "mistral_large": "Mistral", "deepseek_v4": "DeepSeek",
       "minimax": "MiniMax", "kimi": "Moonshot", "inkling": "ThinkingMachines",
       "llama33": "Meta", "gemini3pro": "Google", "gemini35flash": "Google",
       "command_a": "Cohere"}
HUMAN = ROOT / "human-responses" / "responses"
RUNS = ROOT / "runs_v2"


def polelabel(d, side):
    p = d["pole_a"] if side == "a" else d["pole_b"]
    return p["label"] if isinstance(p, dict) else p


def pct(s, q):
    s = sorted(s); n = len(s)
    if n == 1: return s[0]
    i = (q / 100) * (n - 1); lo = int(i); f = i - lo
    return s[lo] + f * (s[min(lo + 1, n - 1)] - s[lo])


def complete_neutral_cells():
    cells = {}; src = {}
    for f in sorted(glob.glob(str(RUNS / "*_neutral_*.json"))):
        d = json.load(open(f))
        if len(d.get("responses", [])) == 240 and d["model_name"] not in DROP:
            m = d["model_name"]
            if m in cells: raise SystemExit(f"duplicate complete neutral run for {m}: {src[m]} and {f}; archive one to runs_v2/_superseded/")
            cells[m] = d; src[m] = f
    return cells


def build_figure_payload():
    """Humans + models on the 12 baseline scenarios (apples-to-apples)."""
    hum = {d: [] for d in DIMS}
    for f in sorted(glob.glob(str(HUMAN / "**" / "*.json"), recursive=True)):
        d = json.load(open(f))
        resp = [{"scenario_id": r["scenario_id"],
                 "judgment_weights": r["judgment"]["weights"],
                 "reasoning_weights": r["reasoning"]["weights"]} for r in d["responses"]]
        seen = {r["dimension"] for r in d["responses"]}
        py = {s["dimension_id"]: s["combined"] for s in compute_dimensional_score(resp, BANK)}
        for ax in DIMS:
            if ax in seen and py.get(ax) is not None:
                hum[ax].append(py[ax])
    cells = complete_neutral_cells()
    models = {}
    for m, d in cells.items():
        good = [r for r in d["responses"] if r["scenario_id"] in BASE and not r.get("extraction_failed")]
        sc = {s["dimension_id"]: s["combined"] for s in compute_dimensional_score(good, BANK)}
        models[m] = {ax: sc.get(ax) for ax in DIMS}
    order = sorted(models, key=lambda m: (LAB[m], m))
    axes = []
    for ax in DIMS:
        h = hum[ax]; mv = [models[m][ax] for m in order]; meta = DMETA[ax]
        axes.append({"id": ax, "name": meta["name"], "poleA": polelabel(meta, "a"),
                     "poleB": polelabel(meta, "b"),
                     "humans": [round(x, 4) for x in h],
                     "hmean": round(statistics.mean(h), 4), "hsd": round(statistics.pstdev(h), 4),
                     "p10": round(pct(h, 10), 4), "p50": round(pct(h, 50), 4), "p90": round(pct(h, 90), 4),
                     "p25": round(pct(h, 25), 4), "p75": round(pct(h, 75), 4),
                     "msd": round(statistics.pstdev(mv), 4),
                     "models": {m: round(models[m][ax], 4) for m in order}})
    return {"n_human": len(hum[DIMS[0]]), "order": order,
            "lab": {m: LAB[m] for m in order}, "axes": axes}


def build_bootstrap(fig):
    """N-matched bootstrap: is the model panel tighter than a same-size human draw?"""
    order = fig["order"]; lab = fig["lab"]; axes = []
    for a in fig["axes"]:
        h = a["humans"]; mv = [a["models"][m] for m in order]
        hsd = statistics.pstdev(h); msd = statistics.pstdev(mv)
        le = sum(1 for _ in range(BOOT) if statistics.pstdev(random.sample(h, len(mv))) <= msd)
        axes.append({"id": a["id"], "name": a["name"], "poleA": a["poleA"], "poleB": a["poleB"],
                     "p50": a["p50"], "hmean": a["hmean"], "hsd": round(hsd, 4), "msd": round(msd, 4),
                     "ratio": round(hsd / msd, 2), "pval": le / BOOT, "humans": a["humans"],
                     "models": [{"m": m, "lab": lab[m], "v": a["models"][m]} for m in order]})
    labs = []
    for m in order:
        if lab[m] not in labs: labs.append(lab[m])
    return {"n_human": fig["n_human"], "n_model": len(order), "labs": labs, "axes": axes}


def build_radar48():
    """Models' 4-axis positions over all 48 scenarios (neutral frame)."""
    cells = complete_neutral_cells()
    models = sorted(cells); axes = []
    for dm in BANK["dimensions"]:
        did = dm["id"]
        mv = {m: round({s["dimension_id"]: s["combined"]
                        for s in cells[m]["dimensional_scores"]}[did], 4) for m in models}
        vals = list(mv.values())
        axes.append({"id": did, "name": dm["name"], "poleA": polelabel(dm, "a"),
                     "poleB": polelabel(dm, "b"), "models": mv,
                     "min": round(min(vals), 4), "max": round(max(vals), 4),
                     "mean": round(statistics.mean(vals), 4), "sd": round(statistics.pstdev(vals), 4)})
    return {"models": models, "lab": {m: LAB[m] for m in models}, "axes": axes,
            "scope": "all 48 scenarios, neutral frame"}


def inject(template_name, payload, out_name):
    tpl = open(TPL_DIR / template_name).read()
    open(OUT / out_name, "w").write(tpl.replace("__PAYLOAD__", json.dumps(payload)))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fig = build_figure_payload()
    json.dump(fig, open(OUT / "figure_payload.json", "w"), indent=2)
    boot = build_bootstrap(fig)
    json.dump(boot, open(OUT / "radar_payload_v3.json", "w"))
    r48 = build_radar48()
    json.dump(r48, open(OUT / "radar48_payload.json", "w"), indent=2)
    inject("tpl_compression_radar.html", boot, "compression_radar_v3.html")
    inject("tpl_model_radar48.html", r48, "model_radar48.html")
    inject("tpl_model_strips.html", r48, "model_strips48.html")
    print(f"models: {len(fig['order'])}  humans: {fig['n_human']}")
    for a in boot["axes"]:
        print(f"  {a['name']:<16} human {a['hmean']:+.3f} ({a['poleB'] if a['hmean']>0 else a['poleA']})"
              f"  ratio {a['ratio']}x  p={a['pval']:.5f}")
    print("wrote 3 payloads + 3 html ->", OUT)


if __name__ == "__main__":
    main()
