# Handoff: reasoner-pilot - 2026-09-07

Written at the end of every session, replacing what was here before. **Informational only. It
authorizes nothing.**

This repository is public, so this file is public. It is written knowing that.

## Current state

- Local and remote agree. The working tree is clean.
- **The published record reproduces.** `python3 analysis/test_reproduce.py` reports 15 reproduced,
  0 mismatched, 0 missing, run 2026-09-05. No keys and no network.
- The document set is installed: `CLAUDE.md`, `CONTEXT.md`, `DECISIONS.md` with 13 entries under
  `docs/decisions/`, `docs/DEVELOPMENT_NOTES.md`, and this file.
- Four issues are open on the tracker, numbered 1 to 4. It had none before today.
- The 2026-09-05 entries below were written on the Black M2 Air. The 2026-09-07 session ran on the
  Silver M5 Air, which holds the completed grid in `validity/`; that grid is now also in S3.

## What changed outside the repository

The S3 validity archive was restored into `validity/` on this machine: 890 run files, 8.1 MB, from
`s3://model-training-artifacts-727165268164-us-east-1-an/archive-reasoner-pilot-validity/`. The
data remains gitignored and is not committed.

That sync also overwrote five tracked files with their 2026-08-21 versions. All five were restored
from git and the tree is clean. Nothing else outside the repository changed: no model runs, no data
written, nothing spent.

Eleven labels were created here yesterday. No deployments were made.

2026-09-07, on the M5 Air: the completed grid was written to
`s3://model-training-artifacts-727165268164-us-east-1-an/archive-reasoner-pilot-validity/2026-09-05/`,
2,692 objects, 7.8 MB, STANDARD: the 2,690 gitignored data files plus a sha256 manifest and a
coverage note, no tracked files. Restored into a scratch directory and verified byte for byte
against the working copy. The 2026-08-21 objects at the prefix root were not touched. Nothing under
`validity/` was run or written. Nothing spent beyond the S3 writes.

## Open items

- **#4, the completed grid is now two-copy.** Counted on disk 2026-09-07: 50 conditions, 11
  models, 550 cells, every cell with exactly 5 reruns carrying ratings, 2,750 scored cells.
  Archived to the dated S3 prefix above; restore verified on the M5 Air only. Still open,
  `ready-for-human`: a restore test on a machine that does not hold the data, and closing.
- **#3, the documented restore command reverts tracked code**, silently, to the archive's date.
- **#1, the appendix regeneration**, labelled `blocked-on-phase`. It cannot run on this machine.
  `papers/inlanguage-mfq2-appendix-DRAFT.md` still describes eleven models, 20 conditions and 1,100
  cells against a paper describing fifty conditions and 2,750 cells.
- **#2, reconciling the paper against the regenerated appendix**, `ready-for-human`, waiting on #1.
- Sampling temperature is unset and unrecorded in the runners, so every collection here was made at
  five unrecorded provider defaults.
- `LOCATIONS.md` carries three `TBD` entries: the Zenodo DOI, the OSF component links, and the final
  moral-os.com URLs. `CITATION.cff` has a commented `doi:` waiting on the first.
- The in-language viewer's title and the paper's title differ.
- Whether every blocking finding in `reviews/viewer-cold-review-2026-08-22.md` is closed has not
  been re-verified against the review.
- `validity/results/` outputs are not covered by `analysis/reproduce_manifest.json`, which pins the
  15 pilot outputs only.

## Unresolved - needs a decision

- **Iran's human anchor.** `validity/anchors_iran.json` uses Hazrati, Nejat and Daneshi (2025)
  sample 2 at 3.333. The settled MFQ-2 source rule names Iran in its prohibition. Iran is the only
  Farsi country so it carries that group everywhere, and the anchor file's own caveats say the
  sample is likely less binding-endorsing than the general population, which biases the overshoot
  toward the finding. Three coherent versions are set out in the review and the sensitivity is
  computed.
- Whether the in-language write-up gets a Zenodo DOI, and whether the paper and appendix are
  combined before it.
- Whether the viewer title and the paper title are brought into line, and which one moves.

## Known-broken and known-strange

Nothing in this repository's code is known broken, and the published outputs reproduce. The
findings that look like defects and are not, and the two restore traps found today, are in
`docs/DEVELOPMENT_NOTES.md`.

One worth repeating because it makes a shortfall invisible: after restoring the archive here,
`audit_inlanguage.py` runs clean and reconciles. It is analysing the original three-language family,
not the grid the paper describes, so a clean run is not evidence the right data is present.

## Loose ends

- The restored run data sits in `validity/` on this machine, gitignored. It is the older
  three-language subset and is not a substitute for the M5 Air's copy.
- `DECISIONS.md` was reconstructed rather than ported, from commit bodies, the README, the papers
  and the framing library. Entries 3 and 5 carry rationale implied by those sources rather than
  stated in them.
- The in-language write-up is still a draft that grew out of its results, so decisions recorded from
  it are expected to be revisited during review rather than treated as settled.
