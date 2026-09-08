# Convergent validity (model panel)

An **exploratory** check on whether the Reasoner's four axes move with established
moral/values frameworks in the directions their labels imply. It administers standard
instruments to the same 11-model panel and correlates their scores against each model's
neutral Reasoner axis positions.

- **MFQ-30** (Graham et al. 2011) — 5 foundations; individualizing/binding split. *(default)*
- **PVQ-40** (Schwartz) — 10 basic values + 4 higher-order dimensions, ipsative-centered.
  Unequal item counts per value (universalism 6, security 5, three values 3, rest 4);
  administered in the **male ('he') portrait form** consistently. *(default)*
- **MFQ-2** (Atari et al. 2023) — 6 foundations (splits Fairness into Equality and
  Proportionality); built with cross-cultural invariance in mind. **Optional / opt-in** —
  not administered by default (largely redundant with MFQ-30); add with
  `--instruments mfq30,pvq40,mfq2` once its items are filled.

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

The score reported is "predicted directions confirmed: k / N", where N counts only the
predictions whose instrument was actually administered (MFQ-2 predictions are marked
"untested" and excluded from the ratio when MFQ-2 is not run).

## Items are NOT included here

The instrument files ship as **scaffolds with empty `text` fields** — only structure
and scoring keys. **The item wording is not redistributed in this repository**; obtain it
from the authoritative sources below and paste it into local, git-ignored `*.filled.json`
copies. Before running:

1. Obtain the official items:
   - MFQ-30: <https://moralfoundations.org/questionnaires/> (`MFQ30.item-key.doc`) —
     free for research/non-commercial use.
   - MFQ-2: moralfoundations.org / Atari et al. (2023) OSF supplement.
   - PVQ-40: Schwartz (2021), "A Repository of Schwartz Value Scales", *Online Readings in
     Psychology and Culture* 2(2):9, <https://scholarworks.gvsu.edu/orpc/vol2/iss2/9/> —
     licensed **CC BY-NC-ND 3.0** (attribution, non-commercial, verbatim only). We use the
     **male ('he') portrait form**. Because the license is non-commercial and no-derivatives,
     the wording is kept out of this (Apache-2.0) repo rather than bundled.
2. Copy each scaffold to a git-ignored filled copy and paste the official wording into it:
   `cp instruments/mfq30.json instruments/mfq30.filled.json` (then fill `text`), likewise
   `mfq2.filled.json`, `pvq40.filled.json`. The loaders prefer `*.filled.json` when present,
   and `.gitignore` keeps those out of git. **Verify each item's foundation/value against the
   official key** — a reworded or mis-keyed item silently invalidates a score.

The runner refuses to run any instrument with an empty item.

## Where the run data lives

The per-cell run files (`runs/`, `runs_framed/`, `runs_framed_lang/`) and the filled
instruments are git-ignored for the reasons above, so this repository is not a copy of
them. They live in two places:

- **Working copy** — `validity/` in your local clone. `audit_inlanguage.py`,
  `analyze_framed.py` and `overshoot_framed.py` read them from there and will not run
  without them.
- **Archive** — `s3://model-training-artifacts-727165268164-us-east-1-an/archive-reasoner-pilot-validity/2026-09-05/`
  (STANDARD). A snapshot of the completed grid, taken 2026-09-05 from the Silver M5 Air:
  2,690 data files, 7.5 MB, under `runs/`, `runs_framed/`, `runs_framed_lang/` and
  `instruments/`, plus `ARCHIVE_MANIFEST.sha256` and `ARCHIVE_NOTE.txt` saying what it
  covers. It contains no tracked file. Restore into a scratch directory, verify, then merge:

      aws sso login
      aws s3 sync s3://model-training-artifacts-727165268164-us-east-1-an/archive-reasoner-pilot-validity/2026-09-05/ /tmp/restore/
      (cd /tmp/restore && shasum -a 256 -c ARCHIVE_MANIFEST.sha256 --quiet && echo OK)
      python3 validity/reconcile.py --archive /tmp/restore        # classify BEFORE touching validity/
      for d in runs runs_framed runs_framed_lang; do rsync -a --delete /tmp/restore/$d/ validity/$d/; done
      rsync -a /tmp/restore/instruments/ validity/instruments/    # no --delete: the tracked scaffolds live here
      python3 validity/reconcile.py --archive /tmp/restore        # must print RECONCILED
      git status                                                  # must be clean

  `reconcile.py` is read-only and stdlib. It puts every local file in one of four buckets -
  identical to the archive, differs, recoverable from git, or nowhere else - and exits non-zero
  on the last two. Run it before the replace so nothing unique is overwritten, and after so the
  working copy is known to be the archive. The three run directories are replaced rather than
  merged: an older collection left in place shares their names, and the audit scripts glob whole
  directories.

  Verified 2026-09-07 on the Black M2 Air, which had never held the grid: 2,690 files restored,
  all 2,690 checksums match. The working copy there was then classified and replaced: 122 files
  identical, 0 differing, 783 present only locally, of which 780 were byte-identical to files
  tracked under `archive-2026-07/` and 3 were the tracked scaffolds.

  The objects at the prefix root, `archive-reasoner-pilot-validity/` itself, are the 2026-08-21
  snapshot: Arabic, Farsi and Japanese only, 929 objects, with tracked files mixed in. Syncing
  it into `validity/` reverts those files to that date (issue 3). Do not restore from it.

Appendices B3, B4 and B5 of the in-language MFQ-2 write-up are regenerated from this data
by `audit_inlanguage.py`. Without it those numbers cannot be recomputed.

## Run it

```bash
# from the repo root, with the panel's API keys exported
python3 validity/build_instruments.py         # (re)generate empty scaffolds
python3 validity/run_validity.py --count       # print the call count, no spend
python3 validity/run_validity.py               # administer MFQ-30 + PVQ-40 to the panel (resumable)
python3 validity/score_validity.py             # -> results/instrument_scores.json
python3 validity/convergent_validity.py        # -> results/convergent_validity.{md,json}
```

## Call count

One API call per (model, instrument, iteration); the whole scale is presented in one
prompt with item order randomized per iteration. Default is MFQ-30 + PVQ-40, 5 iterations:

**11 models × 2 instruments × 5 iterations = 110 calls.**

Adding MFQ-2 (`--instruments mfq30,pvq40,mfq2`) makes it 165. Adjust with `--models`,
`--instruments`, `--iters` (e.g. `--iters 3` → 66). Each call is one questionnaire
(~30–40 items in, a small JSON of ratings out, plus reasoning tokens on reasoning models),
so total spend is modest — dominated by the pricier models (Opus, GPT-5.5, o3) rather than
the count. Run `--count` for the exact plan after any filtering.

## Design notes / limitations

- **Single-prompt administration**: the full scale is rated in one response (as a human
  takes it), not one call per item; item order is randomized across the 5 iterations to
  blunt within-prompt order effects (Iurino & Saucier recommend randomizing MFQ order).
- **PVQ centering**: value scores are ipsatized (minus each model's mean rating), per
  Schwartz, to reduce scale-use bias — consistent with why the Reasoner avoids raw Likert.
- **MFQ catch items** are administered and reported (`_catch_mean`) but excluded from scoring.
- Correlations use each model's **neutral** Reasoner axis scores on the 12 baseline items (b12).
