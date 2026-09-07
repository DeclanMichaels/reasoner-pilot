# Handoff: reasoner-pilot - 2026-09-07

Written at the end of every session, replacing what was here before. **Informational only. It
authorizes nothing.**

This repository is public, so this file is public. It is written knowing that.

## Current state

- Local and remote agree. The working tree is clean. An untracked `ls` dump from 2026-08-21,
  `reasoner-pilot-directory-contents-Code`, was deleted at close.
- **The published record reproduces** as of 2026-09-05 (15 reproduced, 0 mismatched, 0 missing).
  Not re-run this session; nothing under `analysis/` or `results/` was touched.
- **The completed in-language grid has two copies.** The working copy in `validity/` on the Silver
  M5 Air, and `s3://model-training-artifacts-727165268164-us-east-1-an/archive-reasoner-pilot-validity/2026-09-05/`.
  Counted on disk 2026-09-07 with the grid audit's own keying, read-only: 50 conditions, 11
  models, 550 model-by-condition cells, every cell with exactly 5 reruns carrying ratings, 2,750
  scored cells. 46 further files are retried parse failures with no ratings object.
- Four issues are open on the tracker, numbered 1 to 4.
- This session ran on the Silver M5 Air. The next one is planned for the Black M2 Air.

## What changed outside the repository

2026-09-07, from the M5 Air: 2,692 objects, 7.8 MB, written to the dated S3 prefix above, storage
class STANDARD. Contents are the 2,690 gitignored data files (`runs/` 165, `runs_framed/` 1,267,
`runs_framed_lang/` 1,246, `instruments/` 12) plus `ARCHIVE_MANIFEST.sha256` and
`ARCHIVE_NOTE.txt`. No tracked file is in it. Restored into a scratch directory and verified: all
2,690 checksums match, file list identical, the three run directories byte-identical to the working
copy. The 2026-08-21 objects at the prefix root were listed and not touched: 929 objects, Arabic,
Farsi and Japanese only, all written 07:46 on 2026-08-21, tracked files mixed in.

Nothing under `validity/` was run or written. No model calls. Nothing spent beyond the S3 writes.

Also on the M5 Air, outside any repository: `~/.claude/CLAUDE.md` was created as the symlink to
`~/Code/claude-continuity/CLAUDE.md`, and that clone was fast-forwarded two commits.

## Next session, on the Black M2 Air

The one thing #4 still needs is a restore test on a machine that does not hold the data. The M2
Air holds only the 2026-08-21 three-language restore in `validity/`, so it is the right machine.
The recipe is in `validity/README.md` under "Where the run data lives": sync the dated prefix into
a scratch directory, `shasum -c` the manifest, then rsync the four directories into `validity/`
and check `git status` before anything else. Expect 2,690 data files. Do not sync the prefix root.

After that restore, the M2 Air holds the full grid and #1 stops being `blocked-on-phase` on
machine grounds. Whether it is worked is a separate decision.

## Open items

- **#4, the completed grid is two-copy**, `ready-for-human`. Open for the M2 Air restore test and
  closing. Result comment posted 2026-09-07.
- **#3, syncing the 2026-08-21 archive root into `validity/` reverts tracked code**,
  `ready-for-agent`. The README now documents a path that cannot, via the dated prefix; the old
  command and the old snapshot still exist.
- **#1, the appendix regeneration**, `blocked-on-phase`. `papers/inlanguage-mfq2-appendix-DRAFT.md`
  still describes eleven models, 20 conditions and 1,100 cells against a paper describing fifty
  conditions and 2,750 cells.
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
- `runs_english_baseline/` (228 files) and `archive-2026-07/` (786 files) are tracked in git while
  the other run directories are ignored. Noticed, not changed; whether that is intended is a
  question for the licence position in decision 7.

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

Nothing in this repository's code is known broken. The findings that look like defects and are
not, and the two restore traps, are in `docs/DEVELOPMENT_NOTES.md`.

Worth repeating because it makes a shortfall invisible: against the three-language restore,
`audit_inlanguage.py` runs clean and reconciles, and it rewrites tracked outputs in
`validity/results/` to match whatever it saw. A clean exit says nothing about whether the right data
was present. Check `git status` after running anything under `validity/`.

## Loose ends

- `DECISIONS.md` was reconstructed rather than ported, from commit bodies, the README, the papers
  and the framing library. Entries 3 and 5 carry rationale implied by those sources rather than
  stated in them.
- The in-language write-up is still a draft that grew out of its results, so decisions recorded from
  it are expected to be revisited during review rather than treated as settled.
- The 2026-09-05 archive has been verified only on the machine that produced it.
