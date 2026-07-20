#!/usr/bin/env python3
"""Numbers-appendix statistics for the CMRB pilot. Stdlib only.
Reads the same raw runs as build_figures.py; writes private/reanalysis/appendix_stats.json
and prints a summary. Reproducible: python3 private/viz/build_appendix.py
"""
import json, glob, os, statistics, math, random, sys
from pathlib import Path
ROOT = Path(os.environ.get("CMRB_ROOT", Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(ROOT))
from scenario_bank import compute_dimensional_score
random.seed(20260720)
BANK = json.load(open(ROOT/"ccas_bank_full.json"))
DIMS = [d["id"] for d in BANK["dimensions"]]
DMETA = {d["id"]: d for d in BANK["dimensions"]}
NAME = {d["id"]: d["name"] for d in BANK["dimensions"]}
BASE = {s["id"] for s in BANK["scenarios"] if s.get("has_human_baseline")}
DROP = {"gemini3pro", "gemini35flash", "command_a"}
LAB = {"opus":"Anthropic","sonnet":"Anthropic","gpt55":"OpenAI","o3":"OpenAI","grok45":"xAI",
       "mistral_large":"Mistral","deepseek_v4":"DeepSeek","minimax":"MiniMax","kimi":"Moonshot",
       "inkling":"ThinkingMachines","llama33":"Meta","gemini3pro":"Google","gemini35flash":"Google","command_a":"Cohere"}
RUNS = ROOT/"runs_v2"; HUMAN = ROOT/"human-responses"/"responses"
def pstd(xs): return statistics.pstdev(xs)
def mean(xs): return statistics.mean(xs)
def pctl(s,q):
    s=sorted(s); n=len(s)
    if n==1: return s[0]
    i=q*(n-1); lo=int(i); f=i-lo; return s[lo]+f*(s[min(lo+1,n-1)]-s[lo])

cells={}; _src={}
for f in sorted(glob.glob(str(RUNS/"*.json"))):  # one complete file per (model,frame); _superseded/ excluded (non-recursive glob)
    d=json.load(open(f))
    if len(d.get("responses",[]))!=240: continue
    key=(d["model_name"], d["frame"])
    if key in cells: raise SystemExit(f"duplicate complete run for {key}: {_src[key]} and {f}; archive one to runs_v2/_superseded/")
    cells[key]=d; _src[key]=f
allmodels=sorted({m for (m,fr) in cells})
models=[m for m in allmodels if m not in DROP]
extra=[m for m in allmodels if m in DROP]
FR=["neutral","individualist","collectivist","hierarchical","egalitarian","irrelevant","nonsense_geometry","nonsense_color"]
def axis_scores(resps, subset, jw=0.6, rw=0.4):
    good=[r for r in resps if (subset is None or r["scenario_id"] in subset) and not r.get("extraction_failed")]
    return {s["dimension_id"]:s["combined"] for s in compute_dimensional_score(good,BANK,judgment_weight=jw,reasoning_weight=rw)}
hum={a:[] for a in DIMS}
for f in glob.glob(str(HUMAN/"**"/"*.json"),recursive=True):
    d=json.load(open(f))
    resp=[{"scenario_id":r["scenario_id"],"judgment_weights":r["judgment"]["weights"],"reasoning_weights":r["reasoning"]["weights"]} for r in d["responses"]]
    seen={r["dimension"] for r in d["responses"]}
    py={s["dimension_id"]:s["combined"] for s in compute_dimensional_score(resp,BANK)}
    for a in DIMS:
        if a in seen and py.get(a) is not None: hum[a].append(py[a])
n_h=len(hum[DIMS[0]])
pos_b12={m:axis_scores(cells[(m,"neutral")]["responses"],BASE) for m in models}
pos_all={m:axis_scores(cells[(m,"neutral")]["responses"],None) for m in models}

BOOT=100000; CIB=5000
comp={}
for a in DIMS:
    hsd=pstd(hum[a]); mv=[pos_b12[m][a] for m in models]; msd=pstd(mv)
    le=sum(1 for _ in range(BOOT) if pstd(random.sample(hum[a],len(mv)))<=msd)
    ratios=[]
    for _ in range(CIB):
        hh=[random.choice(hum[a]) for _ in hum[a]]; mm=[random.choice(mv) for _ in mv]
        dm=pstd(mm)
        if dm>0: ratios.append(pstd(hh)/dm)
    ratios.sort()
    comp[a]={"human_sd":round(hsd,4),"model_sd":round(msd,4),"ratio":round(hsd/msd,2),"p":le/BOOT,
             "ratio_ci":[round(pctl(ratios,0.025),2),round(pctl(ratios,0.975),2)],
             "human_mean":round(mean(hum[a]),4),"model_mean":round(mean(mv),4),"human_p50":round(pctl(hum[a],0.5),4)}
CULT=["individualist","collectivist","hierarchical","egalitarian"]; NONS=["nonsense_geometry","nonsense_color"]; PLAC=["irrelevant"]
pf={fr:[] for fr in FR if fr!="neutral"}
for m in models:
    neu=pos_all[m]
    for fr in FR:
        if fr=="neutral": continue
        p=axis_scores(cells[(m,fr)]["responses"],None)
        pf[fr].append(mean(abs(p[a]-neu[a]) for a in DIMS))
def grp(frames): return [v for fr in frames for v in pf[fr]]
def ci(vals,B=5000):
    bs=[]
    for _ in range(B):
        s=[random.choice(vals) for _ in vals]; bs.append(mean(s))
    bs.sort(); return round(mean(vals),3),[round(pctl(bs,0.025),3),round(pctl(bs,0.975),3)]
cult_m,cult_ci=ci(grp(CULT)); nons_m,nons_ci=ci(grp(NONS)); plac_m,plac_ci=ci(grp(PLAC))
cv=grp(CULT); nv=grp(NONS)
sp=math.sqrt(((len(cv)-1)*statistics.variance(cv)+(len(nv)-1)*statistics.variance(nv))/(len(cv)+len(nv)-2))
cohend=(mean(cv)-mean(nv))/sp if sp>0 else float("nan")
frame_disp={"cultural":{"mean":cult_m,"ci":cult_ci},"nonsense":{"mean":nons_m,"ci":nons_ci},
            "placebo":{"mean":plac_m,"ci":plac_ci},"nonsense_over_cultural":round(nons_m/cult_m,3),
            "cohen_d_cultural_vs_nonsense":round(cohend,2),"per_frame":{fr:round(mean(pf[fr]),3) for fr in pf}}

TARGET={"individualist":("moral_agent",+1),"collectivist":("moral_agent",-1),
        "egalitarian":("authority",+1),"hierarchical":("authority",-1)}
direction={}
for fr,(ax,sgn) in TARGET.items():
    shifts=[(axis_scores(cells[(m,fr)]["responses"],None)[ax]-pos_all[m][ax])*sgn for m in models]
    direction[fr]={"axis":NAME[ax],"mean_signed_shift_expected_dir":round(mean(shifts),3),
                   "n_models_correct_dir":sum(1 for s in shifts if s>0),"n":len(shifts)}
nons_dir={}
for fr in NONS:
    for ax in ["moral_agent","authority"]:
        shifts=[axis_scores(cells[(m,fr)]["responses"],None)[ax]-pos_all[m][ax] for m in models]
        nons_dir[fr+"|"+ax]={"mean_shift":round(mean(shifts),3),"n_positive":sum(1 for s in shifts if s>0),"n":len(shifts)}
def pearson(x,y):
    n=len(x); mx=sum(x)/n; my=sum(y)/n
    num=sum((a-mx)*(b-my) for a,b in zip(x,y))
    dx=math.sqrt(sum((a-mx)**2 for a in x)); dy=math.sqrt(sum((b-my)**2 for b in y))
    return num/(dx*dy) if dx>0 and dy>0 else 0.0
def nn_table(vecs):
    L=len(vecs[models[0]]); cons=[mean(vecs[m][i] for m in models) for i in range(L)]
    dev={m:[vecs[m][i]-cons[i] for i in range(L)] for m in models}
    t={}
    for m in models:
        rs=sorted(((round(pearson(dev[m],dev[m2]),3),m2) for m2 in models if m2!=m), reverse=True)
        br,best=rs[0]
        t[m]={"nearest":best,"r":br,"same_lab":LAB[m]==LAB[best],"lab":LAB[m],"nn_lab":LAB[best],
              "top3":[[m2,r] for r,m2 in rs[:3]]}
    return t, sum(1 for m in t if t[m]["same_lab"])
# fingerprint A: 4-axis all48 position deviation from panel consensus (panel grain)
vA={m:[pos_all[m][a] for a in DIMS] for m in models}
nn_axis, same_axis = nn_table(vA)
# fingerprint B: per-scenario deviation from panel consensus (fine grain, robustness)
per_scen={m:{} for m in models}
for s in BANK["scenarios"]:
    sid=s["id"]; did=s["dimension_id"]
    for m in models:
        rs=[r for r in cells[(m,"neutral")]["responses"] if r["scenario_id"]==sid and not r.get("extraction_failed")]
        if not rs: continue
        sc={x["dimension_id"]:x["combined"] for x in compute_dimensional_score(rs,BANK)}
        if did in sc: per_scen[m][sid]=sc[did]
common=[s["id"] for s in BANK["scenarios"] if all(s["id"] in per_scen[m] for m in models)]
vB={m:[per_scen[m][sid] for sid in common] for m in models}
nn_scen, same_scen = nn_table(vB)
n_common=len(common)

def run_sd_cell(d, subset):
    by={}
    for r in d["responses"]: by.setdefault(r.get("iteration",0),[]).append(r)
    per={a:[] for a in DIMS}
    for it,rs in by.items():
        sc=axis_scores(rs,subset)
        for a in DIMS:
            if a in sc: per[a].append(sc[a])
    return {a:pstd(per[a]) for a in DIMS}
within={a:[] for a in DIMS}
for m in models:
    r=run_sd_cell(cells[(m,"neutral")],BASE)
    for a in DIMS: within[a].append(r[a])
reliab={a:{"within_run_sd_median":round(statistics.median(within[a]),4),"between_model_sd":comp[a]["model_sd"],
           "between_over_within":round(comp[a]["model_sd"]/statistics.median(within[a]),2) if statistics.median(within[a])>0 else None} for a in DIMS}
sens_scope={a:{"model_sd_b12":comp[a]["model_sd"],"model_sd_all48":round(pstd([pos_all[m][a] for m in models]),4)} for a in DIMS}
sens_jr={}
for label,(jw,rw) in {"judgment_only":(1.0,0.0),"reasoning_only":(0.0,1.0),"combined":(0.6,0.4)}.items():
    p={m:axis_scores(cells[(m,"neutral")]["responses"],BASE,jw,rw) for m in models}
    sens_jr[label]={a:round(pstd([p[m][a] for m in models]),4) for a in DIMS}
incl=models+[m for m in extra if (m,"neutral") in cells]
sens_incl={"models_included":incl,"n":len(incl),
           "model_sd":{a:round(pstd([axis_scores(cells[(m,"neutral")]["responses"],BASE)[a] for m in incl]),4) for a in DIMS}}
def rtok(r):
    u=r.get("usage") or {}; v=u.get("reasoning"); return v if isinstance(v,(int,float)) else 0
tokmean={m:mean([rtok(r) for r in cells[(m,"neutral")]["responses"]]) for m in models}
cent={a:mean(pos_all[m][a] for m in models) for a in DIMS}
distc={m:math.sqrt(sum((pos_all[m][a]-cent[a])**2 for a in DIMS)) for m in models}
Tvec=[tokmean[m] for m in models]; nz=[t for t in Tvec if t>0]
tokens={"per_model":{m:round(tokmean[m],1) for m in models},"min":round(min(Tvec),1),"max":round(max(Tvec),1),
        "min_nonzero":round(min(nz),1) if nz else 0.0,"n":len(models),"distance_from_center":{m:round(distc[m],3) for m in models},
        "r_tokens_distance":round(pearson(Tvec,[distc[m] for m in models]),3),
        "r_tokens_axis":{a:round(pearson(Tvec,[pos_all[m][a] for m in models]),3) for a in DIMS}}
disp_between={}
for fr in FR:
    bb=mean(pstd([axis_scores(cells[(m,fr)]["responses"],BASE)[a] for m in models]) for a in DIMS)
    aa=mean(pstd([axis_scores(cells[(m,fr)]["responses"],None)[a] for m in models]) for a in DIMS)
    disp_between[fr]={"b12":round(bb,4),"all48":round(aa,4)}
_nb=disp_between["neutral"]["b12"]; _na=disp_between["neutral"]["all48"]
for fr in FR:
    disp_between[fr]["b12_x"]=round(disp_between[fr]["b12"]/_nb,1)
    disp_between[fr]["all48_x"]=round(disp_between[fr]["all48"]/_na,1)
out={"n_human":n_h,"n_models":len(models),"models":models,"labs":sorted(set(LAB[m] for m in models)),
     "compression":comp,"frame_displacement":frame_disp,"direction":direction,"nonsense_direction":nons_dir,
     "clustering":{"axis_fingerprint":{"nearest_neighbors":nn_axis,"same_lab_nn_count":same_axis},
                   "scenario_fingerprint":{"n_scenarios":n_common,"nearest_neighbors":nn_scen,"same_lab_nn_count":same_scen}},
     "reliability":reliab,"sensitivity":{"scope":sens_scope,"judgment_reasoning":sens_jr,"including_excluded":sens_incl},
     "reasoning_tokens":tokens,"between_model_dispersion":disp_between}
json.dump(out, open(ROOT/"private"/"reanalysis"/"appendix_stats.json","w"), indent=2)

print("=== COMPRESSION (b12), n_human", n_h, "n_models", len(models), "===")
for a in DIMS:
    c=comp[a]; print(f"{NAME[a]:16} hsd {c['human_sd']:.3f} msd {c['model_sd']:.3f} ratio {c['ratio']}x CI[{c['ratio_ci'][0]}-{c['ratio_ci'][1]}] p={c['p']:.5f}")
print("=== FRAMING DISPLACEMENT ===")
print("cultural", frame_disp["cultural"], "nonsense", frame_disp["nonsense"], "placebo", frame_disp["placebo"])
print("nonsense/cultural", frame_disp["nonsense_over_cultural"], "cohen_d", frame_disp["cohen_d_cultural_vs_nonsense"])
print("per_frame", frame_disp["per_frame"])
print("=== DIRECTION (cultural, expected dir) ===")
for fr,d in direction.items(): print(fr, d)
print("=== NONSENSE DIRECTION ===")
for k,v in nons_dir.items(): print(k,v)
print(f"=== CLUSTERING axis-fingerprint (same-lab nn={same_axis}) ===")
for m in models: print(f"{m:14} -> {nn_axis[m]['nearest']:14} r={nn_axis[m]['r']} same_lab={nn_axis[m]['same_lab']} ({nn_axis[m]['lab']}/{nn_axis[m]['nn_lab']})")
print(f"=== CLUSTERING scenario-fingerprint (n_scen {n_common}, same-lab nn={same_scen}) ===")
for m in models: print(f"{m:14} -> {nn_scen[m]['nearest']:14} r={nn_scen[m]['r']} same_lab={nn_scen[m]['same_lab']} ({nn_scen[m]['lab']}/{nn_scen[m]['nn_lab']})")
print("=== RELIABILITY ===")
for a in DIMS: print(f"{NAME[a]:16}", reliab[a])
print("=== SENSITIVITY scope (b12 vs all48 model SD) ===")
for a in DIMS: print(f"{NAME[a]:16}", sens_scope[a])
print("=== SENSITIVITY judgment/reasoning/combined (model SD b12) ===")
for k,v in sens_jr.items(): print(f"{k:14}", v)
print(f"=== SENSITIVITY including excluded ({','.join(extra)}) ===")
print(sens_incl)
print("=== REASONING TOKENS (neutral) ===")
for m in sorted(models,key=lambda m:-tokmean[m]): print(f"  {m:14} {tokmean[m]:7.0f}  dist {distc[m]:.3f}")
print("span",tokens["min"],"to",tokens["max"],"min_nonzero",tokens["min_nonzero"],
      "| r(tokens,dist)=",tokens["r_tokens_distance"],"r(tokens,axis)=",tokens["r_tokens_axis"])
print("=== BETWEEN-MODEL DISPERSION per framing ===")
for fr in FR: print(f"  {fr:20} b12 {disp_between[fr]['b12']:.3f} (x{disp_between[fr]['b12_x']})   all48 {disp_between[fr]['all48']:.3f} (x{disp_between[fr]['all48_x']})")
print("wrote appendix_stats.json")
