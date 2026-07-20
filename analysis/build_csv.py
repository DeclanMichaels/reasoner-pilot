#!/usr/bin/env python3
"""Export tidy CSV tables of the Reasoner pilot for external inspection. Stdlib only.
Writes to results/csv/. The raw JSON runs remain the source of truth;
these tables are the same data in long (tidy) form, joinable on scenario_id.
Humans are anonymized to sequential ids (h01..). Run: python3 analysis/build_csv.py
"""
import json, glob, os, csv, statistics, sys
from pathlib import Path
ROOT = Path(os.environ.get("REASONER_ROOT", Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(ROOT))
from scenario_bank import compute_dimensional_score
BANK = json.load(open(ROOT/"scenarios.json"))
DIMS = [d["id"] for d in BANK["dimensions"]]
NAME = {d["id"]: d["name"] for d in BANK["dimensions"]}
BASE = {s["id"] for s in BANK["scenarios"] if s.get("has_human_baseline")}
DROP = {"gemini3pro", "gemini35flash", "command_a"}
LAB = {"opus":"Anthropic","sonnet":"Anthropic","gpt55":"OpenAI","o3":"OpenAI","grok45":"xAI",
       "mistral_large":"Mistral","deepseek_v4":"DeepSeek","minimax":"MiniMax","kimi":"Moonshot",
       "inkling":"ThinkingMachines","llama33":"Meta"}
RUNS = ROOT/"runs"; HUMAN = ROOT/"human-responses"/"responses"
OUT = ROOT/"results"/"csv"; OUT.mkdir(parents=True, exist_ok=True)
def w(name, header, rows):
    with open(OUT/name, "w", newline="") as f:
        c = csv.writer(f); c.writerow(header); c.writerows(rows)
    print(f"{name}: {len(rows)} rows")

# 1. the instrument: one row per (scenario, question, option)
rows=[]
for s in BANK["scenarios"]:
    for q in ("judgment","reasoning"):
        for i,o in enumerate(s[q]["options"]):
            rows.append([s["id"], s["dimension_id"], NAME[s["dimension_id"]],
                         int(bool(s.get("has_human_baseline"))), q, i,
                         (o["text"] if isinstance(o,dict) else o),
                         (o["pole"] if isinstance(o,dict) else "")])
w("scenarios.csv", ["scenario_id","axis_id","axis_name","has_human_baseline","question","option_index","option_text","loading"], rows)

# load complete cells (one per (model,frame); _superseded/ excluded by non-recursive glob)
cells={}; _src={}
for f in sorted(glob.glob(str(RUNS/"*.json"))):
    d=json.load(open(f))
    if len(d.get("responses",[]))!=240 or d["model_name"] in DROP: continue
    key=(d["model_name"], d["frame"])
    if key in cells: raise SystemExit(f"duplicate complete run for {key}: {_src[key]} and {f}; archive one to runs/_superseded/")
    cells[key]=d; _src[key]=f
models=sorted({m for (m,fr) in cells})
def axis_scores(resps, subset):
    good=[r for r in resps if (subset is None or r["scenario_id"] in subset) and not r.get("extraction_failed")]
    return {s["dimension_id"]:round(s["combined"],4) for s in compute_dimensional_score(good,BANK)}
def run_sd(resps, subset):
    by={}
    for r in resps: by.setdefault(r.get("iteration",0),[]).append(r)
    per={a:[] for a in DIMS}
    for it,rs in by.items():
        sc=axis_scores(rs,subset)
        for a in DIMS:
            if a in sc: per[a].append(sc[a])
    return {a:(round(statistics.pstdev(per[a]),4) if len(per[a])>1 else 0.0) for a in DIMS}

# 2. model axis scores (b12 and all48 subsets) with run-to-run SD
rows=[]
for (m,fr),d in sorted(cells.items()):
    for subset,tag in ((BASE,"b12"),(None,"all48")):
        sc=axis_scores(d["responses"],subset); sd=run_sd(d["responses"],subset)
        for a in DIMS:
            if a in sc: rows.append([m,LAB[m],fr,tag,a,NAME[a],sc[a],sd[a]])
w("model_scores.csv", ["model","lab","frame","subset","axis_id","axis_name","score","run_sd"], rows)

# 3. model allocations (every option of every response, all 5 iterations) + reasoning text
alloc=[]; reason=[]
for (m,fr),d in sorted(cells.items()):
    for r in d["responses"]:
        sid=r["scenario_id"]; it=r.get("iteration",0)
        for q,wl in (("judgment",r.get("judgment_weights",[])),("reasoning",r.get("reasoning_weights",[]))):
            for i,wt in enumerate(wl):
                alloc.append([m,LAB[m],fr,sid,it,q,i,round(float(wt),4)])
        reason.append([m,LAB[m],fr,sid,it,int(bool(r.get("extraction_failed"))),(r.get("reasoning") or "").strip()])
w("model_allocations.csv", ["model","lab","frame","scenario_id","iteration","question","option_index","weight"], alloc)
w("model_reasoning.csv", ["model","lab","frame","scenario_id","iteration","extraction_failed","reasoning_text"], reason)

# 4. human scores + allocations (anonymized sequential ids)
hs=[]; ha=[]
for idx,f in enumerate(sorted(glob.glob(str(HUMAN/"**"/"*.json"),recursive=True)), start=1):
    d=json.load(open(f)); rid=f"h{idx:02d}"
    resp=[{"scenario_id":x["scenario_id"],"judgment_weights":x["judgment"]["weights"],"reasoning_weights":x["reasoning"]["weights"]} for x in d["responses"]]
    seen={x["dimension"] for x in d["responses"]}
    sc={s["dimension_id"]:round(s["combined"],4) for s in compute_dimensional_score(resp,BANK)}
    for a in DIMS:
        if a in seen and sc.get(a) is not None: hs.append([rid,a,NAME[a],sc[a]])
    for x in d["responses"]:
        for q in ("judgment","reasoning"):
            for i,wt in enumerate(x[q]["weights"]):
                ha.append([rid,x["scenario_id"],q,i,round(float(wt),4)])
w("human_scores.csv", ["respondent_id","axis_id","axis_name","score"], hs)
w("human_allocations.csv", ["respondent_id","scenario_id","question","option_index","weight"], ha)
print("wrote CSVs to", OUT)
