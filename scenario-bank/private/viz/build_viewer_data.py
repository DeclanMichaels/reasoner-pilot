#!/usr/bin/env python3
"""Build the data payload for the CMRB interactive viewer. Stdlib only.
Emits private/reanalysis/viewer_data.json:
  meta, human baseline (baseline-12 distribution per axis), model scores per
  (model,frame,axis) for baseline-12 and all-48, scenario + frame prompt text,
  and one representative response per (model,frame,scenario) with mean weights + text.
"""
import glob, json, os, statistics, sys
from pathlib import Path
ROOT = Path(os.environ.get("CMRB_ROOT", Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(ROOT))
from scenario_bank import compute_dimensional_score
BANK = json.load(open(ROOT / "ccas_bank_full.json"))
PROMPTS = json.load(open(ROOT / "ccas_prompts_v2.json"))["prompts"]
DIMS = [d["id"] for d in BANK["dimensions"]]
DMETA = {d["id"]: d for d in BANK["dimensions"]}
BASE = {s["id"] for s in BANK["scenarios"] if s.get("has_human_baseline")}
DROP = {"gemini3pro", "gemini35flash", "command_a"}
LAB = {"opus":"Anthropic","sonnet":"Anthropic","gpt55":"OpenAI","o3":"OpenAI","grok45":"xAI",
       "mistral_large":"Mistral","deepseek_v4":"DeepSeek","minimax":"MiniMax","kimi":"Moonshot",
       "inkling":"ThinkingMachines","llama33":"Meta"}
HUMAN = ROOT / "human-responses" / "responses"
RUNS = ROOT / "runs_v2"

def pole(d, s): p=d["pole_a"] if s=="a" else d["pole_b"]; return p["label"] if isinstance(p,dict) else p
def pct(s,q):
    s=sorted(s); n=len(s); i=(q/100)*(n-1); lo=int(i); f=i-lo
    return s[lo]+f*(s[min(lo+1,n-1)]-s[lo])

cells_files = {}; _src = {}
for f in sorted(glob.glob(str(RUNS / "*.json"))):  # one complete file per (model,frame); _superseded/ excluded (non-recursive glob)
    d = json.load(open(f))
    if len(d.get("responses", [])) != 240 or d["model_name"] in DROP: continue
    key = (d["model_name"], d["frame"])
    if key in cells_files: raise SystemExit(f"duplicate complete run for {key}: {_src[key]} and {f}; archive one to runs_v2/_superseded/")
    cells_files[key] = d; _src[key] = f
models = sorted({m for (m,fr) in cells_files})
frames = ["neutral","individualist","collectivist","hierarchical","egalitarian","irrelevant","nonsense_geometry","nonsense_color"]

# human baseline (baseline-12)
hum = {a: [] for a in DIMS}
for f in sorted(glob.glob(str(HUMAN / "**" / "*.json"), recursive=True)):
    d=json.load(open(f))
    resp=[{"scenario_id":r["scenario_id"],"judgment_weights":r["judgment"]["weights"],"reasoning_weights":r["reasoning"]["weights"]} for r in d["responses"]]
    seen={r["dimension"] for r in d["responses"]}
    py={s["dimension_id"]:s["combined"] for s in compute_dimensional_score(resp,BANK)}
    for a in DIMS:
        if a in seen and py.get(a) is not None: hum[a].append(round(py[a],4))
humans={a:{"values":hum[a],"mean":round(statistics.mean(hum[a]),4),"sd":round(statistics.pstdev(hum[a]),4),
           "p10":round(pct(hum[a],10),4),"p25":round(pct(hum[a],25),4),"p50":round(pct(hum[a],50),4),
           "p75":round(pct(hum[a],75),4),"p90":round(pct(hum[a],90),4)} for a in DIMS}

# model scores per (model,frame): baseline-12 and all-48
def axis_scores(resps, subset):
    good=[r for r in resps if (subset is None or r["scenario_id"] in subset) and not r.get("extraction_failed")]
    return {s["dimension_id"]:round(s["combined"],4) for s in compute_dimensional_score(good,BANK)}
def run_sd(resps, subset):
    # dispersion across the 5 iterations: rerun-to-rerun wander of the axis score
    by={}
    for r in resps:
        by.setdefault(r.get("iteration",0),[]).append(r)
    per={a:[] for a in DIMS}
    for it,rs in sorted(by.items()):
        sc=axis_scores(rs,subset)
        for a in DIMS:
            if a in sc: per[a].append(sc[a])
    return {a:(round(statistics.pstdev(per[a]),4) if len(per[a])>1 else 0.0) for a in DIMS}
scores={}
for m in models:
    scores[m]={}
    for fr in frames:
        d=cells_files.get((m,fr))
        if not d: continue
        scores[m][fr]={"b12":axis_scores(d["responses"],BASE),"all48":axis_scores(d["responses"],None),
                       "b12_sd":run_sd(d["responses"],BASE),"all48_sd":run_sd(d["responses"],None)}

# scenarios + frame prompts
def opts(block): return [ (o["text"] if isinstance(o,dict) else o) for o in block["options"] ]
scenarios={}
for s in BANK["scenarios"]:
    scenarios[s["id"]]={"dimension_id":s["dimension_id"],"name":s.get("name",s["id"]),"stimulus":s.get("stimulus",""),"origin":s.get("origin"),
        "tradition":s.get("tradition"),"has_human_baseline":bool(s.get("has_human_baseline")),
        "judgment":{"question":s["judgment"].get("question",""),"options":opts(s["judgment"])},
        "reasoning":{"question":s["reasoning"].get("question",""),"options":opts(s["reasoning"])}}

# one representative response per (model,frame,scenario): first complete iter, mean weights across iters
cells={}
for (m,fr),d in cells_files.items():
    by={}
    for r in d["responses"]:
        by.setdefault(r["scenario_id"],[]).append(r)
    for sid,rs in by.items():
        good=[r for r in rs if not r.get("extraction_failed")]
        if not good: continue
        rep=max(good, key=lambda r: len(r.get("reasoning") or ""))  # fullest single run
        cells[f"{m}|{fr}|{sid}"]={"jw":[round(x,3) for x in rep["judgment_weights"]],
                                  "rw":[round(x,3) for x in rep["reasoning_weights"]],
                                  "text":(rep.get("reasoning") or "").strip()}

out={"meta":{"models":models,"frames":frames,"lab":{m:LAB[m] for m in models},
             "axes":[{"id":a,"name":DMETA[a]["name"],"poleA":pole(DMETA[a],"a"),"poleB":pole(DMETA[a],"b")} for a in DIMS],
             "n_human":len(hum[DIMS[0]])},
     "humans":humans,"scores":scores,"scenarios":scenarios,"framePrompts":{fr:PROMPTS.get(fr,"") for fr in frames},
     "cells":cells}
op=ROOT/"private"/"reanalysis"/"viewer_data.json"
json.dump(out,open(op,"w"))
print("models",len(models),"frames",len(frames),"scenarios",len(scenarios),"cells",len(cells))
print("size:", round(op.stat().st_size/1e6,2),"MB ->",op)
