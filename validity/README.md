# Convergent validity (model panel)

An **exploratory** check on whether the Reasoner's four axes move with established
moral/values frameworks in the directions their labels imply. It administers three
standard instruments to the same 11-model panel and correlates their scores against
each model's neutral Reasoner axis positions.

- **MFQ-30** (Graham et al. 2011) — 5 foundations; individualizing/binding split.
- **MFQ-2** (Atari et al. 2023) — 6 foundations (splits Fairness into Equality and
  Proportionality); built with cross-cultural invariance in mind.
- **PVQ-40** (Schwartz) — 10 basic values + 4 higher-order dimensions, ipsative-centered.

**This is not the decisive validity evidence.** n = 11 (models), so correlations are
suggestive, not confirmatory; LLM questionnaire responses have their own validity
limits; and models are not the population that ultimately matters. Human convergent
validity requires **co-administering** MFQ/PVQ with the Reasoner in the confirmatory
sample — it cannot be recovered from the existing pilot data, which contains only the
Reasoner scenarios. This module is the model-side down payment on that program, and a
pre-registered one: the expected correlation pattern is committed in
`convergent_validity.py` (`EXPECTED`) before the run.

## Pre-registered expectations (axis polarity: higher = autonomous / skeptical / narrow / universal)

- **Moral Agent** (+autonomous) → + self-direction, + openness; − MFQ binding, − loyalty
- **Authority** (+skeptical) → − MFQ Authority foundation, − conservation; + openness
- **Moral Domain** (+narrow) → − binding, − Sanctity/Purity; + individualizing
- **Obligation Scope** (+universal) → + universalism, + self-transcendence, + Fairness/Equality; − Loyalty

The score reported is "predicted directions confirmed: k / N."

## Items are NOT included here

The instrument files ship as **scaffolds with empty `text` fields** — only structure
and scoring keys. The item wording is a proprietary research instrument (free for
research use, but not redistributed in this repo). Before running:

1. Obtain the official items:
   - MFQ-30: <https://moralfoundations.org/questionnaires/> (`MFQ30.item-key.doc`)
   - MFQ-2: moralfoundations.org / Atari et al. (2023) OSF supplement
   - PVQ-40: Schwartz's official portraits + value key (Schwartz materials / ESS docs)
2. Copy each scaffold to a git-ignored filled copy and paste the official wording into it:
   `cp instruments/mfq30.json instruments/mfq30.filled.json` (then fill `text`), likewise
   `mfq2.filled.json`, `pvq40.filled.json`. The loaders prefer `*.filled.json` when present,
   and `.gitignore` keeps those out of git. **Verify each item's foundation/value against the
   official key** — a reworded or mis-keyed item silently invalidates a score.

The runner refuses to run any instrument with an empty item.

## Run it

```bash
# from the repo root, with the panel's API keys exported
python3 validity/build_instruments.py         # (re)generate empty scaffolds
python3 validity/run_validity.py --count       # print the call count, no spend
python3 validity/run_validity.py               # administer to the panel (resumable)
python3 validity/score_validity.py             # -> results/instrument_scores.json
python3 validity/convergent_validity.py        # -> results/convergent_validity.{md,json}
```

## Call count

One API call per (model, instrument, iteration); the whole scale is presented in one
prompt with item order randomized per iteration. Default 5 iterations:

**11 models × 3 instruments × 5 iterations = 165 calls.**

Adjust with `--models`, `--instruments`, `--iters` (e.g. `--iters 3` → 99). Each call is
one questionnaire (~30–40 items in, a small JSON of ratings out, plus reasoning tokens on
reasoning models), so total spend is modest — dominated by the pricier models (Opus,
GPT-5.5, o3) rather than the count. Run `--count` for the exact plan after any filtering.

## Design notes / limitations

- **Single-prompt administration**: the full scale is rated in one response (as a human
  takes it), not one call per item; item order is randomized across the 5 iterations to
  blunt within-prompt order effects (Iurino & Saucier recommend randomizing MFQ order).
- **PVQ centering**: value scores are ipsatized (minus each model's mean rating), per
  Schwartz, to reduce scale-use bias — consistent with why the Reasoner avoids raw Likert.
- **MFQ catch items** are administered and reported (`_catch_mean`) but excluded from scoring.
- Correlations use each model's **neutral** Reasoner axis scores on the 12 baseline items (b12).
