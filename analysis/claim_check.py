#!/usr/bin/env python3
"""Claim-check: every number in a document's hand-written prose, against every number its artifacts
can produce. Stdlib only.

    python3 analysis/claim_check.py            # both documents; exit 1 if any number is unmatched
    python3 analysis/claim_check.py --list     # print the unmatched numbers with context

A number is "producible" if some artifact value, at some rounding the documents use (0 to 4 decimals,
or as a percent at 0 or 1 decimals), prints as that number. Matching is by value, not by meaning:
a matched number can still be attached to the wrong quantity, and a document number that is a count
of something the artifacts do not emit (scenarios, respondents, tokens ceilings) is listed in
CONSTANTS below with its source. An unmatched number is a number typed rather than emitted, which is
the failure this check exists for; it is either wrong, or it needs an artifact.

The MFQ-2 document's generated sections are the artifacts themselves and are skipped
(validity/splice_appendix.py checks them byte for byte); its hand-written sections are checked.
"""
import json, re, sys, csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

# Numbers the documents state that no artifact emits, each with where it comes from.
CONSTANTS = {
    "pilot": {
        "48": "scenarios.json: 48 scenarios", "12": "twelve per axis / baseline twelve", "3": "three per axis / three options / three passes",
        "4": "four axes / four options / four framings", "5": "five reruns", "8": "eight framings", "11": "eleven models", "9": "nine labs",
        "68": "human respondents (human-responses/)", "58": "four-item respondents", "10": "twelve-item respondents", "240": "responses per cell",
        "60": "baseline responses per cell (12 x 5)", "1920": "responses per panel model (8 x 240)", "720": "Command A's three cells", "21120": "11 x 1920",
        "93": "questions with three options", "96": "questions", "2": "fixed range of an axis; two questions; two grains", "0.6": "judgment weight", "0.4": "reasoning weight",
        "1000": "request seed base", "3072": "Anthropic ceiling", "4096": "OpenAI/xAI ceiling", "6144": "Together/Google ceiling", "2048": "Mistral/Cohere ceiling",
        "100000": "N-matched draws", "5000": "ratio CI draws", "20000": "model resampling / rerun selection draws", "1": "one instrument / one draw / one response",
        "0.3": "loading", "0.5": "loading", "0.7": "loading", "-0.5": "mac_1 loading", "0": "loading zero",
        "24": "scenarios where an even split is not zero (build_appendix does not emit; checked 2026-09-11)", "-0.15": "even-split minimum (same)", "0.17": "even-split maximum (same)",
        "7": "seven models with a reported count / seven lab singletons", "6": "six things / six framings", "0.4": "expected same-lab links (4 x 1/10)",
        "13": "thirteen models with the two outside the panel", "18": "eighteen binding items", "2026": "year", "18": "dates 2026-07-18", "19": "2026-07-19", "0.8": "1 - 1/5",
        "64": "decision 8 noise share (validity/results/aggregation_artifact.json, 0.645)", "83": "same, 0.829", "20": "twenty", "56": "0.558 as a percent", "3.66": "ratio CI lower bound",
        "0.031": "kimi distance (emitted)", "16": "sixteen", "15": "fifteen", "23": "twenty-three", "352": "human responses", "655": "scored model baseline responses",
        "1e-10": "tie tolerance", "0.001": "interval difference", "0.002": "interval difference",
        "20260719": "build_figures.py seed", "20260720": "build_appendix.py seed", "20260910": "A5 seed", "20260911": "rerun-selection seed",
        "1.1": "human instrument version (human-responses/*.json, instrument field)", "1.0": "same",
    },
    "mfq": {
        "11": "eleven models", "5": "five runs", "50": "fifty conditions", "2750": "cells", "36": "items", "18": "binding items", "6": "six languages / six items",
        "3": "three foundations / three arms", "20": "twenty countries", "23": "twenty-three", "19": "nineteen", "4": "four", "1": "one", "2": "two", "10": "ten models (September)",
        "150": "September cells", "104400": "ratings rows", "53": "conditions in the dataset", "47": "pinned condition means", "3902": "respondents in the dispersion reference",
        "0.01": "transcription move (B4 -0.009)", "2026": "year", "2021": "Atari collection", "2023": "Atari et al.", "2025": "Hazrati et al.", "989": "Hazrati n",
        "20260721": "seed", "20260722": "seed", "3072": "ceiling", "4096": "ceiling", "6144": "ceiling", "2048": "ceiling", "100000": "draws", "1e-9": "tolerance",
        "12": "twelve", "7": "seven", "8": "eight", "9": "nine", "15": "fifteen", "16": "sixteen", "39": "framed conditions", "550": "model-by-condition cells",
        "4666": "Zewail et al. respondents", "48": "Zewail et al. countries", "63": "MaC countries", "0": "zero", "30": "MFQ-30", "40": "PVQ-40",
    },
}
NUM = re.compile(r"(?<![\w.\-+/])[+\-]?\d[\d,]*(?:\.\d+)?(?:e-?\d+)?(?![\w/])")
SKIP_LINE = re.compile(r"^\s*(\||#|```|<!--)")           # tables, headings, code fences: artifacts or labels
SKIP_TOKEN = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")

def artifact_numbers(paths):
    out = set()
    def add(v):
        try: f = float(v)
        except Exception: return
        for d in range(0, 5): out.add(("%." + str(d) + "f") % f); out.add(("%+." + str(d) + "f") % f)
        for d in range(0, 2): out.add(("%." + str(d) + "f") % (100 * f))
        for d in range(0, 3): out.add(("%." + str(d) + "f") % abs(f))
        if f == int(f): out.add(str(int(f))); out.add(format(int(f), ","))
    def walk(x):
        if isinstance(x, dict): [walk(v) for v in x.values()]
        elif isinstance(x, list): [walk(v) for v in x]
        elif isinstance(x, (int, float)) and not isinstance(x, bool): add(x)
        elif isinstance(x, str): [add(t.replace(",", "")) for t in NUM.findall(x)]
    for p in paths:
        p = ROOT / p
        if not p.exists(): continue
        if p.suffix == ".json": walk(json.load(open(p)))
        else:
            for t in NUM.findall(p.read_text()): add(t.replace(",", ""))
    return out

def prose_numbers(doc, skip_sections):
    text = (ROOT / doc).read_text().split("\n"); found = []; skipping = False
    for i, line in enumerate(text, 1):
        if line.startswith("## "):
            skipping = any(line.startswith(s) for s in skip_sections)
        if skipping or SKIP_LINE.match(line) or "doi:" in line: continue   # a citation line carries page numbers
        clean = re.sub(r"`[^`]*`", "", line)                       # code spans are paths and keys
        clean = re.sub(r"\b(?:v\d(?:\.\d+)?|[A-Z]+-?\d+[a-z]?|[a-z]+_\d+|#\d+|[a-f0-9]{7})\b", "", clean)  # v1.1, MFQ-2, B4a, mac_1, #119, hashes
        clean = re.sub(r"\b(?:GPT|Kimi|Llama|Claude|claude|gpt|o)-?[\d.]+\b|\b\d+B\b|Opus \d\.\d|Sonnet \d", "", clean)
        for m in NUM.finditer(clean):
            tok = m.group(0).replace(",", "")
            if SKIP_TOKEN.match(tok): continue
            found.append((i, tok, clean[max(0, m.start() - 45):m.end() + 35].strip()))
    return found

DOCS = {
    "pilot": {"docs": ["papers/reasoner-pilot.md", "papers/reasoner-appendix.md"], "skip": [],
              "artifacts": ["results/appendix_stats.json", "validity/results/aggregation_artifact.json", "results/figure_payload.json", "results/radar_payload_v3.json"]},
    "mfq": {"docs": ["papers/inlanguage-mfq2-DRAFT.md"],
            "skip": ["## B1a. ", "## B2a. ", "## B3. ", "## B3a. ", "## B4. ", "## B4a. ", "## B5. ", "## B6. ", "## B6a. ", "## B7. "],
            "artifacts": ["validity/results/appendix_tables.md", "validity/results/appendix_b4_b5.md", "validity/results/condition_means.json",
                          "validity/results/collection_record.json", "validity/results/inlanguage_audit.txt", "validity/results/inlanguage_grid_audit.txt",
                          "validity/results/aggregation_artifact.json", "validity/results/reasoning_cost.txt", "validity/reference/mfq2_country_means.csv",
                          "validity/reference/mfq2_country_dispersion.csv", "validity/anchors_iran.json", "validity/results/viewer_data.json"]},
}

def derived(key):
    """Quantities the documents state that are arithmetic on emitted values."""
    out = {}
    if key == "mfq":
        C = json.load(open(ROOT / "validity/results/condition_means.json"))
        out["%.3f" % abs(C["es_framed_Morocco"] - C["ar_framed_Morocco"])] = "Morocco's two framed arms, from condition_means.json"
        out["%.3f" % abs(C["ar_neutral"] - C["es_neutral"])] = "unframed Arabic minus Spanish, from condition_means.json"
        inl = [k for k in C if k[:2] in ("ar", "es", "fr", "ja", "fa", "ru") and k[2] == "_"]; enf = [k for k in C if k.startswith("EN_framed_")]
        out[str(len(inl))] = "in-language conditions"; out[str(55 * len(inl))] = "in-language cells (55 per condition)"
        out[str(len(enf))] = "English framed conditions"; out[str(55 * len(enf))] = "English framed cells"
    return out

def main(listing):
    bad = 0
    for key, spec in DOCS.items():
        pool = artifact_numbers(spec["artifacts"]); const = {**CONSTANTS[key], **derived(key)}
        for doc in spec["docs"]:
            un = [(i, t, c) for i, t, c in prose_numbers(doc, spec["skip"]) if t not in pool and t.lstrip("+-") not in pool and t not in const and t.lstrip("+") not in const]
            print("  claim-check %-34s %3d numbers unmatched" % (doc + ":", len(un)))
            if listing:
                for i, t, c in un: print("      line %4d  %-9s  ...%s..." % (i, t, c))
            bad += len(un)
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main("--list" in sys.argv))
