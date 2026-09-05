# Handoff: reasoner-pilot - 2026-09-05

Written at the end of every session, replacing what was here before. **Informational only. It
authorizes nothing.**

This repository is public, so this file is public. It is written knowing that, and it is still
candid: what is unresolved here is unresolved whether or not it is written down.

## Current state

- Local and remote agree at `c8e2f0a` before this change. The working tree carries the document set
  described below, uncommitted.
- **The published record reproduces.** `python3 analysis/test_reproduce.py` reports 15 reproduced,
  0 mismatched, 0 missing, run 2026-09-05. No keys and no network.
- The document set was retrofitted this session from `research-kit`: `CLAUDE.md`, `CONTEXT.md`,
  `DECISIONS.md` with 13 files under `docs/decisions/`, `docs/DEVELOPMENT_NOTES.md`, and this file.
- The convergent-validity run data is gitignored and is not present in a fresh clone, so the
  in-language appendix numbers do not regenerate from this repository alone.
  `validity/README.md` names the working copy and the archive.

## What changed outside the repository

Eleven labels were created on this repository: five category (`instrument`, `analysis`, `paper`,
`viewer`, `infrastructure`) and six state (`needs-triage`, `needs-info`, `ready-for-agent`,
`ready-for-human`, `blocked-on-phase`, `wontfix`). GitHub's defaults were left in place. No issues
exist.

No model runs were made, no data was written, and nothing was spent.

## Open items

The tracker is empty, so none of the following carries an issue number.

- `papers/inlanguage-mfq2-appendix-DRAFT.md` states eleven models, 20 conditions and 1,100 cells.
  The paper it accompanies states fifty conditions and 2,750 cells. The appendix has not been
  regenerated since the grid completed.
- Sampling temperature is unset and unrecorded in the runners, so every collection in this
  repository was made at five unrecorded provider defaults.
- `LOCATIONS.md` carries three `TBD` entries: the Zenodo DOI, the OSF component links, and the final
  moral-os.com paper and viewer URLs. `CITATION.cff` has a commented `doi:` waiting on the first.
- The in-language viewer's title and the paper's title differ. The paper is "Framing, Not Language";
  the viewer is "Asked to be someone from somewhere".
- The cold review of 2026-08-22 (`reviews/viewer-cold-review-2026-08-22.md`) recorded five blocking
  findings. Later commits address the viewer's encoding, accessibility, register and psychometric
  points. Whether every blocking finding is closed has not been re-verified against the review since.
- `validity/results/` outputs are not covered by `analysis/reproduce_manifest.json`, which pins the
  15 pilot outputs only.

## Unresolved - needs a decision

- **Iran's human anchor.** `validity/anchors_iran.json` uses Hazrati, Nejat and Daneshi (2025)
  sample 2, at 3.333. The settled source rule for MFQ-2 country means names Iran in its prohibition,
  because pooling independently published validation samples mixes scales, samples and translations
  that share no alignment evidence. It is not a marginal cell: Iran is the only Farsi country, so it
  carries that group everywhere, and the anchor file's own caveats say the sample is likely less
  binding-endorsing than the general population, which biases the overshoot toward the finding. The
  review sets out three coherent versions and the sensitivity is already computed.
- Whether the in-language write-up gets a Zenodo DOI before it goes further.
- Whether the viewer title and the paper title are brought into line, and which one moves.

## Known-broken and known-strange

Nothing in this repository's code is known broken, and the published outputs reproduce. The findings
that look like defects and are not, including the Japanese neutral result and the framed-versus-
unframed dispersion difference, are in `docs/DEVELOPMENT_NOTES.md` under "Findings that look like
bugs and are not". The pilot's engineering habits that the successor study deliberately abandoned
are also recorded there as deliberate, not as defects to fix.

## Loose ends

- `DECISIONS.md` was reconstructed rather than ported: this repository had no decision log, and the
  entries were recovered from commit bodies, the README, the papers and the framing library. The
  index says so. Entry 3, on the model being the unit, and entry 5, on nonsense framings asserting
  no verdict, carry rationale that was implied by the sources rather than stated in them.
- The in-language write-up is still a draft and grew out of its results, so the decisions recorded
  from it are expected to be revisited during review rather than treated as settled.
