#!/usr/bin/env python3
"""Concurrent generation runner for the refreshed pilot. Thread-pooled with a
per-provider concurrency cap (to avoid 429s), retry/backoff on transient errors,
and per-cell resumable writes (a completed model/frame file is skipped on rerun,
so a crash resumes cleanly). Reuses the validated calling + parsing layer in
refresh_runner. Stdlib only. Run through an interactive shell so keys load:
    zsh -ic 'python3 concurrent_runner.py --workers 24 --per-provider 5'
Filters: --models a,b  --frames neutral,...  --iters N  --limit N(scenarios)
"""
import argparse, json, os, sys, time, threading, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import random
import refresh_runner as rr

PROVIDER_CAPS = {'google': 3, 'openai': 4, 'cohere': 3, 'mistral': 5, 'anthropic': 6, 'xai': 6, 'together': 6}
from scenario_bank import compute_dimensional_score, normalize_weights

ROOT = Path(__file__).resolve().parent
REG, BANK, FRAMES = rr.REG, rr.BANK, rr.FRAMES


def call_with_retry(cfg, system, user, rid, seed, tries=8):
    for a in range(tries):
        try:
            text, usage = rr.call_model(cfg, system, user, rid, seed)
            if text and text.strip():
                return text, usage
            if a < tries - 1:
                time.sleep(min(45, 3 * 2 ** a) + random.uniform(0, 2)); continue
            return text, usage  # empty after retries; parse fallback will flag it
        except urllib.error.HTTPError as e:
            if e.code in (408, 409, 425, 429, 500, 502, 503, 504) and a < tries - 1:
                wait = None
                try:
                    ra = e.headers.get("Retry-After")
                    if ra: wait = float(ra)
                except Exception:
                    wait = None
                if wait is None:
                    wait = min(60, 3 * 2 ** a)
                time.sleep(min(90, wait) + random.uniform(0, 2)); continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if a < tries - 1:
                time.sleep(min(45, 3 * 2 ** a) + random.uniform(0, 2)); continue
            raise
    raise RuntimeError("unreachable")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="")
    ap.add_argument("--frames", default="")
    ap.add_argument("--iters", type=int, default=5)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--per-provider", type=int, default=5)
    ap.add_argument("--runs-dir", default=str(ROOT / "runs"))
    a = ap.parse_args()

    models = a.models.split(",") if a.models else list(REG["models"].keys())
    frames = a.frames.split(",") if a.frames else list(FRAMES.keys())
    scenarios = BANK["scenarios"][:a.limit] if a.limit else BANK["scenarios"]
    runs_dir = Path(a.runs_dir); runs_dir.mkdir(parents=True, exist_ok=True)

    for mn in models:
        if not os.environ.get(REG['models'][mn]['env_key']):
            sys.exit('missing env key '+REG['models'][mn]['env_key']+' for '+mn+'; aborting before spend')
    provs = sorted({REG["models"][m]["provider"] for m in models})
    sems = {p: threading.Semaphore(PROVIDER_CAPS.get(p, a.per_provider)) for p in provs}

    # Build cells, skipping any already-complete (resumable).
    cells = []
    for mn in models:
        for fr in frames:
            done = list(runs_dir.glob(f"{mn}_{fr}_*.json"))
            complete = False
            for df in done:
                try:
                    d = json.load(open(df)); resp = d.get("responses", [])
                    if len(resp) == a.iters*len(scenarios) and d.get("call_failures",0) <= 0.1*len(resp):
                        complete = True; break
                except Exception:
                    pass
            if complete:
                continue
            cells.append((mn, fr))
    if not cells:
        print("nothing to do (all cells complete)", flush=True); return

    tasks = []  # (cell_key, model_name, cfg, frame, iter, scenario)
    for (mn, fr) in cells:
        cfg = REG["models"][mn]
        for it in range(a.iters):
            for s in scenarios:
                tasks.append(((mn, fr), mn, cfg, fr, it, s))
    # interleave tasks round-robin across providers so every provider semaphore
    # stays busy from the start (otherwise same-provider models serialize at the cap)
    from collections import defaultdict, deque
    bypro = defaultdict(list)
    for t in tasks:
        bypro[REG["models"][t[1]]["provider"]].append(t)
    queues = [deque(v) for v in bypro.values()]
    tasks = []
    while any(queues):
        for q in queues:
            if q:
                tasks.append(q.popleft())
    expected = {}
    for t in tasks:
        expected[t[0]] = expected.get(t[0], 0) + 1
    results = {k: [] for k in expected}
    lock = threading.Lock()
    counts = {"done": 0, "fail": 0}

    def work(task):
        cell, mn, cfg, fr, it, s = task
        seed = 1000 + it
        rid = f"{mn}-{fr}-i{it}-{s['id']}"
        rec = {"scenario_id": s["id"], "dimension_id": s["dimension_id"], "iteration": it,
               "frame": fr, "request_id": rid, "seed": seed}
        sem = sems[cfg["provider"]]
        with sem:
            try:
                text, usage = call_with_retry(cfg, FRAMES[fr], rr.alloc_prompt(s), rid, seed)
                jw, rw, failed = rr.parse_weights(text, s)
                rec.update({"reasoning": text, "judgment_weights": jw, "reasoning_weights": rw,
                            "extraction_failed": failed, "usage": usage})
            except Exception as e:
                rec.update({"reasoning": None,
                            "judgment_weights": normalize_weights([1.0] * len(s["judgment"]["options"])),
                            "reasoning_weights": normalize_weights([1.0] * len(s["reasoning"]["options"])),
                            "extraction_failed": True, "call_failed": True, "usage": None,
                            "error": f"{type(e).__name__}: {str(e)[:200]}"})
        return cell, rec

    t0 = time.time()
    total = len(tasks)
    print(f"{len(cells)} cells, {total} calls, {a.workers} workers, {a.per_provider}/provider", flush=True)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(work, t) for t in tasks]
        for f in as_completed(futs):
            cell, rec = f.result()
            with lock:
                results[cell].append(rec)
                counts["done"] += 1
                if rec.get("call_failed"): counts["fail"] += 1
                n = counts["done"]
                if n % 200 == 0 or n == total:
                    el = time.time() - t0
                    print(f"  {n}/{total}  fail {counts['fail']}  {el:.0f}s  "
                          f"{n/el:.1f} calls/s  eta {(total-n)/max(n/el,0.01):.0f}s", flush=True)
                # write a cell as soon as it is fully collected
                if len(results[cell]) == expected[cell]:
                    mn, fr = cell
                    resp = sorted(results[cell], key=lambda r: (r["iteration"], r["scenario_id"]))
                    good = [r for r in resp if not r.get("extraction_failed") and not r.get("call_failed")]
                    scores = compute_dimensional_score(good, BANK)
                    cfg = REG["models"][mn]
                    tok = {"input": 0, "output": 0, "reasoning": 0}
                    for r in resp:
                        uu = r.get("usage") or {}
                        for kk in tok: tok[kk] += (uu.get(kk) or 0)
                    out = {"model_name": mn, "provider": cfg["provider"], "model": cfg["model_id"],
                           "frame": fr, "iterations": a.iters, "n_scenarios": len(scenarios),
                           "temperature": "provider default (omitted)", "instrument": "direct-allocation v2",
                           "n_scored": len(good), "tokens": tok, "dimensional_scores": scores, "responses": resp,
                           "extraction_failures": sum(r.get("extraction_failed") for r in resp),
                           "call_failures": sum(r.get("call_failed", False) for r in resp)}
                    ts = time.strftime("%Y%m%d_%H%M%S")
                    json.dump(out, open(runs_dir / f"{mn}_{fr}_{ts}.json", "w"), indent=2)
                    print(f"  wrote {mn}_{fr}  (fail {out['call_failures']}, extfail {out['extraction_failures']})", flush=True)
    print(f"done {counts['done']} calls, {counts['fail']} failures, {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
