# the Reasoner pilot visuals

Self-contained regeneration of the three pilot figures from the raw run data.
Stdlib only (no numpy/pandas). Any session can rebuild the figures with one command.

## Run

```
python3 build_figures.py
```

Resolves the repo root automatically (this dir is `<root>/analysis/`).
Override with `REASONER_ROOT=/path/to/scenario-bank` and/or `REASONER_FIG_OUT=/path/to/out`.

## Inputs (all under the repo root)

- `scenarios.json` — 48-scenario bank. Option pole signs must be correct
  (`pole_a` = -1 side, `pole_b` = +1 side). See the sign note below.
- `runs/*.json` — one file per (model, frame) cell, 240 responses each.
- `human-responses/responses/**/*.json` — 68 respondents, raw allocation weights.
- `scenario_bank.py` — provides `compute_dimensional_score`, the single scorer used
  for both humans and models.

## Outputs (to `results/` by default)

Payloads: `figure_payload.json`, `radar_payload_v3.json`, `radar48_payload.json`.
Figures (self-contained HTML, dark theme, data inlined):

1. `compression_radar_v3.html` — 68 humans vs the model panel on the 12 baseline
   scenarios. Radar of individual dots + true-scale strips + N-matched bootstrap.
2. `model_radar48.html` — models on the 4 axes over all 48 scenarios; envelope +
   "spans X% of axis" labels.
3. `model_strips48.html` — linear companion; each axis's full -1..+1 with the model
   band as a shaded sliver.

Templates are `tpl_*.html` (with a `__PAYLOAD__` marker); `build_figures.py` injects
the computed payload as inline JSON. To render PNGs, point a headless Chromium at
each `file://` and screenshot full-page (optional; not needed for the HTML).

## SIGN CHECK (important)

`build_figures.py` prints each axis's human mean and which pole it leans to. The
68-respondent WEIRD baseline must read **Autonomous / Skeptical / Narrow / Universal**.
If it reads the opposite (Relational / Deferential / Broad / Relational), the bank's
option pole signs are inverted and every directional claim is backwards. A global
inversion was fixed 2026-07-19; the pre-fix bank is preserved at
`private/_pre_review/scenarios.preflip.json`. The JS collector used for human
data collection carries the same pole table and must match the bank.
