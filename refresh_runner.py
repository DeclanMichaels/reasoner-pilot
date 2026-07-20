#!/usr/bin/env python3
"""Reasoner refreshed-pilot runner: DIRECT ALLOCATION (with token accounting).

Each model, per scenario, reasons in free text AND outputs its own judgment/
reasoning weight allocation in one response. Weights are the PRIMARY measure,
scored by scenario_bank.compute_dimensional_score (same as humans). Failed/
unparseable responses are excluded from scoring. Free text is kept for coding.
Per-call token usage is recorded, including the reasoning/thinking-token split
where the provider exposes it (deliberation is itself signal). Stdlib only.
    zsh -ic 'python3 refresh_runner.py --models opus,grok45 --frames neutral --iters 1 --limit 3'
"""
import argparse, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scenario_bank import compute_dimensional_score, normalize_weights

ROOT = Path(__file__).resolve().parent
REG = json.load(open(ROOT / "models.json"))
BANK = json.load(open(ROOT / "scenarios.json"))
FRAMES = json.load(open(ROOT / "framings.json"))["prompts"]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def _post(url, headers, body, timeout=180):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
        headers={**headers, "User-Agent": UA, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def _u_openai(d):
    u = d.get("usage", {}) or {}
    det = u.get("completion_tokens_details", {}) or {}
    return {"input": u.get("prompt_tokens"), "output": u.get("completion_tokens"),
            "reasoning": det.get("reasoning_tokens")}


def _anthropic(model, system, user, key, rid, mx=3072):
    b = {"model": model, "max_tokens": mx, "messages": [{"role": "user", "content": user}],
         "metadata": {"user_id": rid}}
    if system: b["system"] = system
    d = _post("https://api.anthropic.com/v1/messages", {"x-api-key": key, "anthropic-version": "2023-06-01"}, b)
    txt = "".join(p.get("text", "") for p in d["content"] if p.get("type") == "text").strip()
    u = d.get("usage", {}) or {}
    return txt, {"input": u.get("input_tokens"), "output": u.get("output_tokens"), "reasoning": None}


def _openai_compat(url, model, system, user, key, rid, seed, max_key="max_tokens", mx=4096, extra=None):
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    b = {"model": model, "messages": msgs, max_key: mx, "stream": False}
    if extra: b.update(extra)
    d = _post(url, {"Authorization": "Bearer " + key}, b)
    return (d["choices"][0]["message"]["content"] or "").strip(), _u_openai(d)


def _google(model, system, user, key, mx=6144):
    b = {"contents": [{"parts": [{"text": user}]}], "generationConfig": {"maxOutputTokens": mx}}
    if system: b["systemInstruction"] = {"parts": [{"text": system}]}
    d = _post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}", {}, b)
    parts = d["candidates"][0].get("content", {}).get("parts", []) or []
    txt = ""
    for p in reversed(parts):
        if not p.get("thought") and "text" in p:
            txt = p["text"].strip(); break
    if not txt:
        txt = next((p["text"].strip() for p in parts if "text" in p), "")
    um = d.get("usageMetadata", {}) or {}
    th = um.get("thoughtsTokenCount", 0) or 0
    return txt, {"input": um.get("promptTokenCount"),
                 "output": (um.get("candidatesTokenCount", 0) or 0) + th, "reasoning": th or None}


def _cohere(model, system, user, key, mx=2048):
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    d = _post("https://api.cohere.com/v2/chat", {"Authorization": "Bearer " + key},
              {"model": model, "messages": msgs, "max_tokens": mx, "stream": False})
    txt = "".join(c.get("text", "") for c in d["message"]["content"]).strip()
    u = (d.get("usage", {}) or {}).get("tokens", {}) or {}
    return txt, {"input": u.get("input_tokens"), "output": u.get("output_tokens"), "reasoning": None}


def call_model(cfg, system, user, rid, seed):
    """Returns (text, usage_dict)."""
    p, m, k = cfg["provider"], cfg["model_id"], os.environ[cfg["env_key"]]
    if p == "anthropic": return _anthropic(m, system, user, k, rid)
    if p == "openai":    return _openai_compat("https://api.openai.com/v1/chat/completions", m, system, user, k, rid, seed, "max_completion_tokens", 4096, {"seed": seed, "user": rid})
    if p == "xai":       return _openai_compat("https://api.x.ai/v1/chat/completions", m, system, user, k, rid, seed, mx=4096, extra={"seed": seed, "user": rid})
    if p == "together":  return _openai_compat("https://api.together.xyz/v1/chat/completions", m, system, user, k, rid, seed, mx=6144, extra={"seed": seed})
    if p == "mistral":   return _openai_compat("https://api.mistral.ai/v1/chat/completions", m, system, user, k, rid, seed, mx=2048, extra={"random_seed": seed})
    if p == "google":    return _google(m, system, user, k)
    if p == "cohere":    return _cohere(m, system, user, k)
    raise ValueError("unknown provider " + p)


def alloc_prompt(s):
    L = [f"SCENARIO: {s['stimulus']}", "",
         f"QUESTION 1 (judgment) - {s['judgment']['question']}"]
    L += [f"  {chr(65+i)}. {o['text']}" for i, o in enumerate(s['judgment']['options'])]
    L += ["", f"QUESTION 2 (reasoning) - {s['reasoning']['question']}"]
    L += [f"  {chr(65+i)}. {o['text']}" for i, o in enumerate(s['reasoning']['options'])]
    L += ["", "First, in a few sentences, think through which considerations carry weight and why. "
          "Then allocate 100 points across the options for EACH question separately, reflecting how "
          "much genuine moral weight each option carries (not a ranking; ties and zeros are fine). "
          "End your reply with one JSON object on its own line and nothing after it:",
          '{"judgment_weights": [<points per option A,B,...>], "reasoning_weights": [<points per option A,B,...>]}']
    return "\n".join(L)


def _extract_weight_obj(text):
    best = None
    for st in (i for i, c in enumerate(text) if c == "{"):
        depth = 0
        for j in range(st, len(text)):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    frag = text[st:j + 1]
                    if "judgment_weights" in frag and "reasoning_weights" in frag:
                        try:
                            o = json.loads(frag)
                            if isinstance(o, dict) and "judgment_weights" in o and "reasoning_weights" in o:
                                best = o
                        except Exception:
                            pass
                    break
    return best


def parse_weights(text, s):
    jn = len(s["judgment"]["options"]); rn = len(s["reasoning"]["options"])
    d = _extract_weight_obj(text or "")
    if d is not None:
        try:
            jw = [max(0.0, float(x)) for x in d.get("judgment_weights", [])]
            rw = [max(0.0, float(x)) for x in d.get("reasoning_weights", [])]
            count_ok = (len(jw) == jn and len(rw) == rn)
            jw = (jw + [0.0] * jn)[:jn]; rw = (rw + [0.0] * rn)[:rn]
            if sum(jw) > 0 or sum(rw) > 0:
                return normalize_weights(jw), normalize_weights(rw), (not count_ok)
        except Exception:
            pass
    return normalize_weights([1.0] * jn), normalize_weights([1.0] * rn), True


def run_cell(model_name, cfg, frame, iters, scenarios):
    responses = []
    for it in range(iters):
        seed = 1000 + it
        for s in scenarios:
            rid = f"{model_name}-{frame}-i{it}-{s['id']}"
            rec = {"scenario_id": s["id"], "dimension_id": s["dimension_id"], "iteration": it,
                   "frame": frame, "request_id": rid, "seed": seed}
            try:
                text, usage = call_model(cfg, FRAMES[frame], alloc_prompt(s), rid, seed)
                jw, rw, failed = parse_weights(text, s)
                rec.update({"reasoning": text, "judgment_weights": jw, "reasoning_weights": rw,
                            "extraction_failed": failed, "usage": usage})
            except Exception as e:
                rec.update({"reasoning": None,
                            "judgment_weights": normalize_weights([1.0] * len(s["judgment"]["options"])),
                            "reasoning_weights": normalize_weights([1.0] * len(s["reasoning"]["options"])),
                            "extraction_failed": True, "call_failed": True, "usage": None,
                            "error": f"{type(e).__name__}: {str(e)[:200]}"})
            responses.append(rec)
    good = [r for r in responses if not r.get("extraction_failed") and not r.get("call_failed")]
    scores = compute_dimensional_score(good, BANK)
    tok = {"input": 0, "output": 0, "reasoning": 0}
    for r in responses:
        u = r.get("usage") or {}
        for kk in tok:
            tok[kk] += (u.get(kk) or 0)
    return {"model_name": model_name, "provider": cfg["provider"], "model": cfg["model_id"],
            "frame": frame, "iterations": iters, "n_scenarios": len(scenarios),
            "temperature": "provider default (omitted)", "instrument": "direct-allocation v2",
            "n_scored": len(good), "tokens": tok, "dimensional_scores": scores, "responses": responses,
            "extraction_failures": sum(r.get("extraction_failed") for r in responses),
            "call_failures": sum(r.get("call_failed", False) for r in responses)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default=""); ap.add_argument("--frames", default="")
    ap.add_argument("--iters", type=int, default=5); ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--runs-dir", default=str(ROOT / "runs"))
    a = ap.parse_args()
    models = a.models.split(",") if a.models else list(REG["models"].keys())
    frames = a.frames.split(",") if a.frames else list(FRAMES.keys())
    scenarios = BANK["scenarios"][:a.limit] if a.limit else BANK["scenarios"]
    os.makedirs(a.runs_dir, exist_ok=True)
    for mn in models:
        cfg = REG["models"][mn]
        for fr in frames:
            t0 = time.time()
            out = run_cell(mn, cfg, fr, a.iters, scenarios)
            ts = time.strftime("%Y%m%d_%H%M%S")
            json.dump(out, open(Path(a.runs_dir) / f"{mn}_{fr}_{ts}.json", "w"), indent=2)
            print(f"{mn:<14} {fr:<16} {out['n_scored']}/{len(out['responses'])} scored  "
                  f"tok in/out/think {out['tokens']['input']}/{out['tokens']['output']}/{out['tokens']['reasoning']}  "
                  f"{time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
