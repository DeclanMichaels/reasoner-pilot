# Handoff: reasoner-pilot - 2026-09-07

Written at the end of every session, replacing what was here before. **Informational only. It
authorizes nothing.**

This repository is public, so this file is public. It is written knowing that.

## Current state

- Local and remote agree, and the working tree is clean apart from this file. The session's work
  is `303e79e`.
- **The published record reproduces**, run 2026-09-07, no keys and no network: 15 regenerated
  outputs reproduced, 17 committed-only outputs verified. The second group is new; decision 14 says
  what it is and why its guarantee is weaker.
- **This machine now holds the completed grid.** `runs/` 165, `runs_framed/` 1,267,
  `runs_framed_lang/` 1,246, `instruments/` 15, byte-identical to the 2026-09-05 S3 archive.
- **The in-language appendix generates end to end.** B3, B3a, B4, B5 and B6 come from
  `results/appendix_tables.md` and `results/appendix_b4_b5.md`, spliced verbatim. A number in the
  document that disagrees with its artifact is a splice that was not re-run.
- Three issues are open: #2, #3 and #5.
- `DECISIONS.md` holds 14 entries.
- This is the Black M2 Air.

## What changed outside the repository

**The restore test issue 4 was open for was run and passed.** The 2026-09-05 archive was synced
into a scratch directory on this machine, which had never held the grid: 2,690 files, all 2,690
manifest checksums match. The archive restores standalone.

**The working copy in `validity/` was replaced with the grid.** Before the replace, every local file
was classified against the archive: 122 identical, 0 differing, 783 present only locally. Of those
783, 780 were byte-identical to files already tracked under `validity/archive-2026-07/` and 3 were
the tracked empty scaffolds. Nothing on this machine was unique, so nothing was lost. The July
collection stands unchanged in git where it always was.

`reasoner-study` received decision 27 and was pushed (`ff05433`, private). It supersedes decision
1's consequences clause only; that entry's decision stands in force.

The Atari et al. preprint was downloaded to the session scratchpad, outside any repository, and is
not committed.

No model calls, nothing written to S3, nothing spent.

## The tracker

Three issues are open. Two were closed on 2026-09-08 with their dispositions.

- **#2, reconcile the paper against the appendix**, `paper`, `ready-for-human`. The one that blocks
  publication, and now workable since the appendix it waits on exists.
- **#5, add `validity/reconcile.py`**, `infrastructure`, `ready-for-agent`.
- **#3, fix the documented restore command**, `infrastructure`, `ready-for-agent`.
- Closed: **#1**, the appendix regeneration, done in `303e79e`. **#4**, the single-copy grid,
  resolved by the 2026-09-07 restore test on a machine that did not hold the data.

## Next session

Three issues, in this order. **#2 is `ready-for-human` by design** and its own body says why:
resolving a disagreement between two published-track documents is a judgment call about which is
correct. An agent can produce the list and the evidence; it does not decide which document wins.

1. **#2, reconcile the paper against the appendix.** The appendix now regenerates and the paper was
   rewritten on the completed grid, so where they disagree the paper is the more likely to be right,
   but not always. One disagreement is already found and is the shape of the rest: the paper says
   Care runs 4.29 to 4.88 across all fifty conditions, the computed span is 4.29 to 4.89. The
   deliverable is every numeric disagreement listed with both values, a decision on each with its
   reason, and any correction recorded visibly rather than edited into agreement.
2. **#5, add `validity/reconcile.py`.** The classification done by hand on 2026-09-07 before the
   working copy was replaced, made repeatable and read-only. Its four buckets and the stop
   conditions are in the issue.
3. **#3, fix the documented restore command.** Same area as #5 and cheaper after it exists: the
   dated prefix is already documented in `validity/README.md`, and what remains is that the old
   command and the 2026-08-21 snapshot both still exist and still revert tracked code.

Read `docs/DEVELOPMENT_NOTES.md` before touching anything under `validity/`. The audit scripts write
tracked outputs, and a clean exit says nothing about whether the right data was present.

## Open items

- **#2 has one concrete discrepancy already found.** `papers/inlanguage-mfq2-DRAFT.md:143` says Care
  runs 4.29 to 4.88 across all fifty conditions. The computed span is 4.29 to 4.89. The rest of the
  paper has not been read against the regenerated appendix.
- `validity/results/viewer_data.json` embeds a generation timestamp, so regenerating it always
  changes the file. Its pin therefore detects "someone re-ran the script", not "a number moved". The
  15 pilot outputs do not have this problem.
- The appendix uses `[*]` for a caveat and `[d12]` for a decision pointer. The asymmetry is
  undocumented and reads as arbitrary.
- Whether every blocking finding in `reviews/viewer-cold-review-2026-08-22.md` is closed is still
  unverified as a whole. Its blocking finding 1, the Iran disclosure, was checked against the viewer
  on 2026-09-07 and is addressed there; the others were not looked at.
- Sampling temperature is unset and unrecorded in the runners, so every collection here was made at
  five unrecorded provider defaults.
- `LOCATIONS.md` carries three `TBD` entries: the Zenodo DOI, the OSF component links, and the final
  moral-os.com URLs. `CITATION.cff` has a commented `doi:` waiting on the first.
- The in-language viewer's title and the paper's title differ.
- **Nothing in `303e79e` has had independent adversarial review**, and it is public.

## Unresolved - needs a decision

- **Iran's anchor is now disclosed, and the objection that blocked it was not what it appeared to
  be.** The settled rule bars pooling independent validation means into the Atari reference file; it
  does not bar a separately sourced, separately marked anchor, and the reference file here has never
  contained Iran. What remains is a live choice: the appendix uses Hazrati sample 2 at 3.333 and
  shows all three options, and sample 2 is the largest of the three, so the reported overshoot is
  the smallest available. Moving to the pooled anchor would raise it.
- Whether the in-language write-up gets a Zenodo DOI, and whether the paper and appendix are
  combined before it.
- Whether the viewer title and the paper title are brought into line, and which one moves.

## Known-broken and known-strange

Nothing in this repository's code is known broken.

**The audit scripts write tracked outputs**, so a clean exit says nothing about whether the right
data was present. Check `git status` after running anything under `validity/`. That trap and the two
restore traps are in `docs/DEVELOPMENT_NOTES.md`.

**Two claims were carried through most of this session before anyone read the source, and both were
wrong when read.** The first was that Iran's anchor contradicts a settled decision: the review said
so, the previous handoff repeated it, and the rule as written turned out to prohibit something else.
The second was our own wording that the nineteen Atari country means are "not national means": the
paper describes Study 2 as nationally stratified. Both were caught by being questioned, not by being
checked. `verify_reviewer_external_facts` already covers this; it was not applied until prompted.

## Loose ends

- `DECISIONS.md` entries 3 and 5 carry rationale implied by their sources rather than stated in
  them; the log was reconstructed on 2026-09-05, not ported.
- The in-language write-up is still a draft that grew out of its results, so decisions recorded from
  it are expected to be revisited during review rather than treated as settled.
- B6 lost the claim that Equality is the only foundation where the panel lands near a measured
  value, and B5 lost the clause about T11 not changing sign. Both stopped being true when the tables
  expanded. Neither was replaced, because a replacement reading would be ours rather than the data's.
