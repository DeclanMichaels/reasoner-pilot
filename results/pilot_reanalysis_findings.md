# Pilot Compression Re-analysis: Findings (canonical)

Regenerated from the deterministic pipeline (`tighten.py` + `pilot_common.py`). Data: 68
human respondents, 5 models under neutral framing, 4 pilot axes. Each cell uses the complete
60-response run selected by `pilot_common.pick_run` (partial and duplicate runs excluded and
logged). SD is population SD. Bootstrap B = 100,000, seed 20260717. Metrics:
`reanalysis/tightened_metrics.json`.

## Bottom line
Models compress the moral-reasoning range. The finding survives the small-panel artifact the
cold reviewer flagged: it does not depend on comparing 5 model points to 68 human points.

| Axis | model SD | human SD | SD ratio | N-matched p | tighter than a 5-human draw | centroid offset (human SD) | IDR coverage |
|---|---|---|---|---|---|---|---|
| Moral Agent | 0.083 | 0.408 | 0.204 | .0026 | 4.2x | 0.82 | 18% |
| Authority | 0.042 | 0.401 | 0.104 | .0003 | 7.9x | 0.14 | 10% |
| Moral Domain | 0.079 | 0.327 | 0.240 | .0107 | 3.4x | 0.38 | 20% |
| Obligation Scope | 0.062 | 0.358 | 0.174 | .0022 | 4.9x | 0.32 | 15% |

## Reading
- **SD ratios 0.10 to 0.24**: models sit four to ten times tighter than the full human sample
  on every axis, worst on Authority.
- **N-matched, the effect holds on all four axes**: drawing 5 humans (matching the panel) and
  recomputing dispersion 100,000 times, the 5 models are as-or-more clustered than 5 random
  humans with p = .0003 to .011, roughly three to eight times tighter than a same-sized human
  draw. This is the honest, defensible version of "models compress the moral range."
- **Two distinct signals**: clustering (low model SD) is universal; centroid offset is
  axis-specific, largest on Moral Agent (0.82 human SD off the human center, 95% CI 0.56 to
  1.15), toward the autonomous pole.
- **IDR coverage (10 to 20 percent)** is reported only as the pre-bootstrap figure; interdecile
  range on 5 points is downward-biased, so it overstates compression and is not the headline.

## Frame sensitivity (from pilot_frame_shifts.py)
Cultural 0.347, nonsense 0.222 (64% of cultural), irrelevant noise floor 0.032, nonsense /
irrelevant = 7.0x. Hierarchical framing perturbs every model most; Gemini moves most (mean
cultural 0.54, peak 0.87 hierarchical), Llama least (0.19).

## Nonsense coding
253 / 300 integration, 47 silent-drop (all Sonnet), 0 resistance across all 300. Two
independent coder passes; agreement and kappa recomputed by `compute_agreement.py` from the
committed label vectors (`coding_pass1.json`, `coding_pass2.json`). See `coder_prompt.md`.

## What changed from the pre-review run
The earlier numbers were produced by an mtime-based `latest()` selector that, with tied
timestamps, could pick a partial Sonnet neutral run (4 or 12 responses instead of 60) and
arbitrary duplicates for other cells. The Figure 1 payload had in fact been built from the
4-response Sonnet fragment (Authority -0.30), which understated the compression. Selection is
now deterministic and complete-run-only, so every number here is reproducible.
