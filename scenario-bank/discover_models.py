#!/usr/bin/env python3
"""Query each provider's model-list endpoint to discover current API model IDs
and confirm each key works. Stdlib only (urllib). Keys read from env; never printed.
Run:  zsh -ic 'python3 discover_models.py'
"""
import json, os, urllib.request, urllib.error

def get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def ids_from(d):
    if isinstance(d, list):
        return [x.get("id") or x.get("name") for x in d if isinstance(x, dict)]
    for k in ("data", "models"):
        if isinstance(d.get(k), list):
            return [x.get("id") or x.get("name") for x in d[k] if isinstance(x, dict)]
    return []

def show(name, ids, filt=None):
    if filt:
        ids = [i for i in ids if i and any(f in i.lower() for f in filt)]
    ids = sorted(set(i for i in ids if i))
    print(f"\n=== {name} ({len(ids)}) ===")
    for i in ids:
        print("  ", i)

E = os.environ
try:
    show("anthropic", ids_from(get("https://api.anthropic.com/v1/models",
        {"x-api-key": E["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"})))
except Exception as e: print("anthropic ERR", e)
try:
    show("openai", ids_from(get("https://api.openai.com/v1/models",
        {"Authorization": f"Bearer {E['OPENAI_API_KEY']}"})),
        filt=["gpt-5", "gpt-4o", "o1", "o3", "o4", "reason"])
except Exception as e: print("openai ERR", e)
try:
    show("xai", ids_from(get("https://api.x.ai/v1/models",
        {"Authorization": f"Bearer {E['XAI_API_KEY']}"})))
except Exception as e: print("xai ERR", e)
try:
    show("google", ids_from(get(
        f"https://generativelanguage.googleapis.com/v1beta/models?key={E['GEMINI_API_KEY']}&pageSize=200", {})),
        filt=["gemini-2.5", "gemini-3", "gemini-flash"])
except Exception as e: print("google ERR", e)
try:
    show("cohere", ids_from(get("https://api.cohere.com/v1/models",
        {"Authorization": f"Bearer {E['COHERE_API_KEY']}"})), filt=["command"])
except Exception as e: print("cohere ERR", e)
try:
    show("mistral", ids_from(get("https://api.mistral.ai/v1/models",
        {"Authorization": f"Bearer {E['MISTRAL_API_KEY']}"})),
        filt=["large", "medium"])
except Exception as e: print("mistral ERR", e)
try:
    show("together", ids_from(get("https://api.together.xyz/v1/models",
        {"Authorization": f"Bearer {E['TOGETHER_API_KEY']}"})),
        filt=["glm", "qwen", "deepseek", "llama-3.3", "llama-4", "maverick",
              "minimax", "inkling", "thinking", "kimi"])
except Exception as e: print("together ERR", e)
