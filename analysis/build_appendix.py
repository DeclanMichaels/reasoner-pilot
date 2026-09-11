#!/usr/bin/env python3
"""Numbers-appendix statistics for the Reasoner pilot. Stdlib only.
Reads the same raw runs as build_figures.py; writes results/appendix_stats.json
and prints a summary. Reproducible: python3 analysis/build_appendix.py
"""
import json, glob, os, statistics, math, random, sys
from pathlib import Path
ROOT = Path(os.environ.get("REASONER_ROOT", Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(ROOT))
from scenario_bank import compute_dimensional_score
random.seed(20260720)
BANK = json.load(open(ROOT/"scenarios.json"))
DIMS = [d["id"] for d in BANK["dimensions"]]
DMETA = {d["id"]: d for d in BANK["dimensions"]}
NAME = {d["id"]: d["name"] for d in BANK["dimensions"]}
BASE = {s["id"] for s in BANK["scenarios"] if s.get("has_human_baseline")}
DROP = {"gemini3pro", "gemini35flash", "command_a"}
LAB = {"opus":"Anthropic","sonnet":"Anthropic","gpt55":"OpenAI","o3":"OpenAI","grok45":"xAI",
       "mistral_large":"Mistral","deepseek_v4":"DeepSeek","minimax":"MiniMax","kimi":"Moonshot",
       "inkling":"ThinkingMachines","llama33":"Meta","gemini3pro":"Google","gemini35flash":"Google","command_a":"Cohere"}
RUNS = ROOT/"runs"; HUMAN = ROOT/"human-responses"/"responses"
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
    if key in cells: raise SystemExit(f"duplicate complete run for {key}: {_src[key]} and {f}; archive one to runs/_superseded/")
    cells[key]=d; _src[key]=f
allmodels=sorted({m for (m,fr) in cells})
models=[m for m in allmodels if m not in DROP]
extra=[m for m in allmodels if m in DROP]
FR=["neutral","individualist","collectivist","hierarchical","egalitarian","irrelevant","nonsense_geometry","nonsense_color"]
def axis_scores(resps, subset, jw=0.6, rw=0.4):
    good=[r for r in resps if (subset is None or r["scenario_id"] in subset) and not r.get("extraction_failed")]
    return {s["dimension_id"]:s["combined"] for s in compute_dimensional_score(good,BANK,judgment_weight=jw,reasoning_weight=rw)}
hum={a:[] for a in DIMS}
hum12={a:[] for a in DIMS}            # the respondents who answered all twelve baseline scenarios
hum_item={}                            # per-item human scores: scenario_id -> [score]
hum_resp=[]                            # (respondent, n_items, instrument) for the exposure table
hum_by_w={}                            # human axis scores under each question weighting, for A8
SCEN_DIM={s_["id"]:s_["dimension_id"] for s_ in BANK["scenarios"]}
for f in glob.glob(str(HUMAN/"**"/"*.json"),recursive=True):  # unsorted, as pinned: the A3 draws depend on this order
    d=json.load(open(f))
    resp=[{"scenario_id":r["scenario_id"],"judgment_weights":r["judgment"]["weights"],"reasoning_weights":r["reasoning"]["weights"]} for r in d["responses"]]
    seen={r["dimension"] for r in d["responses"]}
    hum_resp.append((f, len(resp), d.get("instrument")))
    py={s["dimension_id"]:s["combined"] for s in compute_dimensional_score(resp,BANK)}
    for a in DIMS:
        if a in seen and py.get(a) is not None:
            hum[a].append(py[a])
            if len(resp)==12: hum12[a].append(py[a])
    for r in resp:
        one={s["dimension_id"]:s["combined"] for s in compute_dimensional_score([r],BANK)}
        hum_item.setdefault(r["scenario_id"],[]).append(one[SCEN_DIM[r["scenario_id"]]])
    for label,(jw,rw) in {"judgment_only":(1.0,0.0),"reasoning_only":(0.0,1.0),"combined":(0.6,0.4)}.items():
        pw={s["dimension_id"]:s["combined"] for s in compute_dimensional_score(resp,BANK,judgment_weight=jw,reasoning_weight=rw)}
        for a in DIMS:
            if a in seen and pw.get(a) is not None: hum_by_w.setdefault(label,{a_:[] for a_ in DIMS})[a].append(pw[a])
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
# pf[fr][i] is model models[i]'s displacement under framing fr. The intervals resample MODELS
# (each model carrying all its framings), not the pooled model-by-framing values: a model's
# framed displacements share its unframed baseline, so pooled resampling treats one model's
# four numbers as four independent models. Own generator so the A3 draws above are unchanged.
def grp_stats(idx):
    c=mean(pf[fr][i] for i in idx for fr in CULT); n=mean(pf[fr][i] for i in idx for fr in NONS); p=mean(pf[fr][i] for i in idx for fr in PLAC)
    return {"cultural":c,"nonsense":n,"placebo":p,"cultural_minus_nonsense":c-n,"nonsense_over_cultural":n/c}
_rng=random.Random(20260910); CLB=20000
_pt=grp_stats(range(len(models)))
_bs=[grp_stats([_rng.randrange(len(models)) for _ in models]) for _ in range(CLB)]
def _ci(k): v=sorted(b[k] for b in _bs); return [round(pctl(v,0.025),3),round(pctl(v,0.975),3)]
frame_disp={k:{"mean":round(_pt[k],3),"ci":_ci(k)} for k in ("cultural","nonsense","placebo","cultural_minus_nonsense","nonsense_over_cultural")}
frame_disp["interval"]={"unit":"models","draws":CLB,"seed":20260910,"n_models":len(models)}
frame_disp["per_frame"]={fr:round(mean(pf[fr]),3) for fr in pf}
frame_disp["per_model_nonsense_over_cultural"]={m:round(mean(pf[fr][i] for fr in NONS)/mean(pf[fr][i] for fr in CULT),3) for i,m in enumerate(models)}

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
# Reasoning tokens are whatever the provider's usage object reports. A cell whose responses
# carry no numeric reasoning count is "not reported", never zero: the Anthropic, Cohere and
# Mistral adapters record None, and Together returns null for Llama.
cent={a:mean(pos_all[m][a] for m in models) for a in DIMS}
distc={m:math.sqrt(sum((pos_all[m][a]-cent[a])**2 for a in DIMS)) for m in models}
tokens={"per_model":{},"distance_from_center":{m:round(distc[m],3) for m in models},"n":len(models)}
for m in models:
    rs=cells[(m,"neutral")]["responses"]
    rv=[(r.get("usage") or {}).get("reasoning") for r in rs]; ov=[(r.get("usage") or {}).get("output") for r in rs]
    num=[v for v in rv if isinstance(v,(int,float))]
    # No share of output: providers differ on whether reasoning tokens sit inside the output
    # count (xAI reports them outside it), so the ratio is not comparable across the panel.
    if num:
        tokens["per_model"][m]={"reported":True,"n_reported":len(num),"n_responses":len(rs),"reasoning_mean":round(mean(num),1)}
    else:
        tokens["per_model"][m]={"reported":False,"n_reported":0,"n_responses":len(rs),"reasoning_mean":None}
tokens["reported_models"]=[m for m in models if tokens["per_model"][m]["reported"]]
tokens["not_reported_models"]=[m for m in models if not tokens["per_model"][m]["reported"]]
_rep=[tokens["per_model"][m]["reasoning_mean"] for m in tokens["reported_models"]]
tokens["reported_min"]=round(min(_rep),1); tokens["reported_max"]=round(max(_rep),1)
disp_between={}
for fr in FR:
    bb=mean(pstd([axis_scores(cells[(m,fr)]["responses"],BASE)[a] for m in models]) for a in DIMS)
    aa=mean(pstd([axis_scores(cells[(m,fr)]["responses"],None)[a] for m in models]) for a in DIMS)
    disp_between[fr]={"b12":round(bb,4),"all48":round(aa,4)}
_nb=disp_between["neutral"]["b12"]; _na=disp_between["neutral"]["all48"]
for fr in FR:
    disp_between[fr]["b12_x"]=round(disp_between[fr]["b12"]/_nb,1)
    disp_between[fr]["all48_x"]=round(disp_between[fr]["all48"]/_na,1)
# Human item exposure: most respondents answered one baseline scenario per axis.
from collections import Counter
exposure={"respondents_by_items":{str(k):v for k,v in sorted(Counter(n for _,n,_ in hum_resp).items())},
          "respondents_by_items_and_instrument":{f"{n} items, {inst}":c for (n,inst),c in sorted(Counter((n,i) for _,n,i in hum_resp).items())},
          "twelve_item_humans":{a:{"n":len(hum12[a]),"human_sd":round(pstd(hum12[a]),4),"model_sd":comp[a]["model_sd"],
                                   "ratio":round(pstd(hum12[a])/comp[a]["model_sd"],2)} for a in DIMS},
          "per_item":[]}
for s_ in BANK["scenarios"]:
    sid=s_["id"]
    if sid not in BASE: continue
    a=s_["dimension_id"]; hv=hum_item[sid]
    mv=[axis_scores(cells[(m,"neutral")]["responses"],{sid})[a] for m in models]
    exposure["per_item"].append({"item":sid,"axis":NAME[a],"n_humans":len(hv),"human_sd":round(pstd(hv),4),
                                 "model_sd":round(pstd(mv),4),"ratio":round(pstd(hv)/pstd(mv),2)})
# Extraction exclusions: responses whose allocations could not be parsed are excluded from
# every score; a file of 240 responses is not a cell of 240 scored answers.
exclusions={"per_model":{},"total_excluded":0,"total_responses":0}
for m in allmodels:
    row={}
    for fr in FR:
        if (m,fr) in cells:
            rs=cells[(m,fr)]["responses"]; ex=sum(1 for r in rs if r.get("extraction_failed")); cf=sum(1 for r in rs if r.get("call_failed"))
            row[fr]={"excluded":ex,"call_failed":cf}
            if m in models: exclusions["total_excluded"]+=ex; exclusions["total_responses"]+=len(rs)
    exclusions["per_model"][m]={"frames":row,"excluded":sum(v["excluded"] for v in row.values()),"responses":240*len(row),"in_panel":m in models}
# Range coverage on all 48: the span of the eleven unframed positions as a share of the fixed range 2.
range_cov={a:{"min":round(min(pos_all[m][a] for m in models),4),"max":round(max(pos_all[m][a] for m in models),4),
              "span":round(max(pos_all[m][a] for m in models)-min(pos_all[m][a] for m in models),4),
              "pct_of_range":round(100*(max(pos_all[m][a] for m in models)-min(pos_all[m][a] for m in models))/2,2)} for a in DIMS}
# Human/model ratio under each question weighting, both sides re-scored.
sens_jr_ratio={}
for label,(jw,rw) in {"judgment_only":(1.0,0.0),"reasoning_only":(0.0,1.0),"combined":(0.6,0.4)}.items():
    pm={m:axis_scores(cells[(m,"neutral")]["responses"],BASE,jw,rw) for m in models}
    sens_jr_ratio[label]={a:{"human_sd":round(pstd(hum_by_w[label][a]),4),"model_sd":round(pstd([pm[m][a] for m in models]),4),
                             "ratio":round(pstd(hum_by_w[label][a])/pstd([pm[m][a] for m in models]),2)} for a in DIMS}
# Allocation style (Kimi round one, finding 3): how points are spread across options, unframed b12,
# models and humans on the same measure; and the compression ratio after collapsing every
# allocation on both sides onto its largest option, which removes the spread-of-points component.
SC_BY_ID={s_["id"]:s_ for s_ in BANK["scenarios"]}
def _style(sid, jw, rw):
    out={}
    for q,w in (("judgment",jw),("reasoning",rw)):
        poles=[o["pole"] for o in SC_BY_ID[sid][q]["options"]]; tot=sum(w) or 1.0; w=[x/tot for x in w]
        out[q]={"neutral_share":sum(x for x,pp in zip(w,poles) if pp==0),"full_pole_share":sum(x for x,pp in zip(w,poles) if abs(pp)==1),
                "entropy":-sum(x*math.log(x) for x in w if x>0)/math.log(len(w)),"max_share":max(w)}
    return out
def _style_mean(rows):
    return {q:{k:round(mean(r[q][k] for r in rows),3) for k in ("neutral_share","full_pole_share","entropy","max_share")} for q in ("judgment","reasoning")}
def _wta(w):
    if not w or sum(w)==0: return w
    i=max(range(len(w)),key=lambda k:w[k]); return [1.0 if k==i else 0.0 for k in range(len(w))]
def _sharp(r): return {"scenario_id":r["scenario_id"],"judgment_weights":_wta(r["judgment_weights"]),"reasoning_weights":_wta(r["reasoning_weights"])}
alloc={"per_model":{},"humans":None,"winner_take_all":{}}
_hum_rows=[]; _humw={a:[] for a in DIMS}
for f in glob.glob(str(HUMAN/"**"/"*.json"),recursive=True):  # unsorted, as above
    d=json.load(open(f)); resp=[{"scenario_id":r["scenario_id"],"judgment_weights":r["judgment"]["weights"],"reasoning_weights":r["reasoning"]["weights"]} for r in d["responses"]]
    _hum_rows+=[_style(r["scenario_id"],r["judgment_weights"],r["reasoning_weights"]) for r in resp]
    seen={r["dimension"] for r in d["responses"]}; pw={s["dimension_id"]:s["combined"] for s in compute_dimensional_score([_sharp(r) for r in resp],BANK)}
    for a in DIMS:
        if a in seen and pw.get(a) is not None: _humw[a].append(pw[a])
alloc["humans"]={"n_responses":len(_hum_rows),**_style_mean(_hum_rows)}
_mw={a:[] for a in DIMS}
for m in models:
    good=[r for r in cells[(m,"neutral")]["responses"] if r["scenario_id"] in BASE and not r.get("extraction_failed")]
    alloc["per_model"][m]={"n_responses":len(good),**_style_mean([_style(r["scenario_id"],r["judgment_weights"],r["reasoning_weights"]) for r in good])}
    pw={s["dimension_id"]:s["combined"] for s in compute_dimensional_score([_sharp(r) for r in good],BANK)}
    for a in DIMS: _mw[a].append(pw[a])
for a in DIMS:
    alloc["winner_take_all"][a]={"human_sd":round(pstd(_humw[a]),4),"model_sd":round(pstd(_mw[a]),4),"ratio":round(pstd(_humw[a])/pstd(_mw[a]),2),"ratio_as_published":comp[a]["ratio"]}
# Exclusion sensitivity (Kimi finding 4): score the excluded responses with the runner's stored
# fallback allocation and compare the b12 model SD; and Kimi's geometry displacement both ways.
excl_sens={}
for a in DIMS:
    inc=[]
    for m in models:
        al=[r for r in cells[(m,"neutral")]["responses"] if r["scenario_id"] in BASE]
        inc.append({s["dimension_id"]:s["combined"] for s in compute_dimensional_score(al,BANK)}[a])
    excl_sens[a]={"model_sd_excluding":comp[a]["model_sd"],"model_sd_including_fallback":round(pstd(inc),4),
                  "max_model_shift":round(max(abs(x-y) for x,y in zip([pos_b12[m][a] for m in models],inc)),3)}
_kg_ex=axis_scores(cells[("kimi","nonsense_geometry")]["responses"],None); _kg_in={s["dimension_id"]:s["combined"] for s in compute_dimensional_score(cells[("kimi","nonsense_geometry")]["responses"],BANK)}
excl_sens["kimi_geometry_displacement"]={"excluding":round(mean(abs(_kg_ex[a]-pos_all["kimi"][a]) for a in DIMS),3),"including_fallback":round(mean(abs(_kg_in[a]-pos_all["kimi"][a]) for a in DIMS),3)}
MODELS_JSON=json.load(open(ROOT/"models.json"))["models"]
model_ids={m:{"provider":MODELS_JSON[m]["provider"],"model_id":MODELS_JSON[m]["model_id"]} for m in allmodels if m in MODELS_JSON}
out={"n_human":n_h,"n_models":len(models),"models":models,"labs":sorted(set(LAB[m] for m in models)),
     "model_ids":model_ids,"human_exposure":exposure,"exclusions":exclusions,"exclusion_sensitivity":excl_sens,"allocation_style":alloc,"range_coverage_all48":range_cov,
     "compression":comp,"frame_displacement":frame_disp,"direction":direction,"nonsense_direction":nons_dir,
     "clustering":{"axis_fingerprint":{"nearest_neighbors":nn_axis,"same_lab_nn_count":same_axis},
                   "scenario_fingerprint":{"n_scenarios":n_common,"nearest_neighbors":nn_scen,"same_lab_nn_count":same_scen}},
     "reliability":reliab,"sensitivity":{"scope":sens_scope,"judgment_reasoning":sens_jr,"judgment_reasoning_ratio":sens_jr_ratio,"including_excluded":sens_incl},
     "reasoning_tokens":tokens,"between_model_dispersion":disp_between}
json.dump(out, open(ROOT/"results"/"appendix_stats.json","w"), indent=2)

print("=== COMPRESSION (b12), n_human", n_h, "n_models", len(models), "===")
for a in DIMS:
    c=comp[a]; print(f"{NAME[a]:16} hsd {c['human_sd']:.3f} msd {c['model_sd']:.3f} ratio {c['ratio']}x CI[{c['ratio_ci'][0]}-{c['ratio_ci'][1]}] p={c['p']:.5f}")
print("=== FRAMING DISPLACEMENT ===")
print("cultural", frame_disp["cultural"], "nonsense", frame_disp["nonsense"], "placebo", frame_disp["placebo"])
print("nonsense/cultural", frame_disp["nonsense_over_cultural"], "difference", frame_disp["cultural_minus_nonsense"])
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
for m in models: print(f"  {m:14} {str(tokens['per_model'][m]['reasoning_mean']):>8}  dist {distc[m]:.3f}")
print("=== REASONING TOKENS === reported:", tokens["reported_models"], "not reported:", tokens["not_reported_models"])
print("=== BETWEEN-MODEL DISPERSION per framing ===")
for fr in FR: print(f"  {fr:20} b12 {disp_between[fr]['b12']:.3f} (x{disp_between[fr]['b12_x']})   all48 {disp_between[fr]['all48']:.3f} (x{disp_between[fr]['all48_x']})")
print("wrote appendix_stats.json")
