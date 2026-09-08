# Handoff: reasoner-pilot - 2026-09-08

Written at the end of every session, replacing what was here before. **Informational only. It
authorizes nothing.**

This repository is public, so this file is public. It is written knowing that.

## Current state

- Local and remote agree, and the working tree is clean apart from this file. The session's work
  is thirteen commits, `8336de4` to `afb185d`.
- **The published record reproduces**, full run 2026-09-08, no keys and no network: 15
  regenerated outputs reproduced, 17 committed-only outputs verified.
- **The in-language paper and appendix have been through one adversarial round and its tickets
  are closed.** Sixteen tickets from Astra's review of 2026-09-08 were filed, worked and closed the
  same day; the adjudication and the review as received are `reviews/astra-paper-review-2026-09-08.md`.
  The paper is retitled. Every data section of the appendix is generated; the splice map is in
  `docs/DEVELOPMENT_NOTES.md`.
- **The declared test family is withdrawn.** B4 is a contrast set over the full grid, reported as
  intervals, sign counts and leave-one-out ranges, no p-values. Decision 15 says why; B10 carries
  the errata.
- No issue is open. `DECISIONS.md` holds 15 entries.
- This is the Black M2 Air. `validity/` holds the completed grid, and `validity/reconcile.py`
  reports it identical to the 2026-09-05 archive.

## What changed outside the repository

`reasoner-study` received decision 27 (`ff05433`) and a pointer to it in its reference README
(`53bc0dc`), both pushed, private. Two of its reference files were copied into
`validity/reference/` here as documented copies.

Three primary sources were read for the review: the Atari et al. (2023) preprint (OSF `q6c9r`),
the Hazrati et al. (2025) preprint v3 (OSF `43t5s`) with its OSF project file listing, and the
Zewail et al. (2026) PMC full text. The PDFs and a `pypdf` virtualenv are in the session
scratchpad, outside any repository. The viewer was rendered locally to verify its relabelled
intervals.

No model calls, nothing written to S3, nothing spent.

## The tracker

- Nothing is open. #21 closed on 2026-09-08: Declan ruled the authors' shared respondent-level
  files may be used; `validity/reference/build_iran_dispersion.py` derives the SDs off the
  reproduce path and the appendix reads only its CSV. #1 to #21 are closed with their
  dispositions on the tickets.

## Next session

Nothing is queued for an agent and nothing is open. What remains is yours:

1. **Review.** Everything pushed since `303e79e` on 2026-09-07 - the regenerated appendix, the
   paper corrections, the rebuilt contrast set, decision 15 - has had no independent adversarial
   review. Astra reviewed the state at `8336de4`; the state now is materially different.
2. **The Iran anchor.** Sample 2 (3.333, in use, the largest of the three, so the reported
   overshoot is the smallest) against the n-weighted pool (3.304). B4 shows all three.
3. **The viewer's title against the paper's.** The paper is now "Country framing shifts MFQ-2
   responses more than questionnaire language in an eleven-model panel"; the viewer still says
   "In-language society framing - MFQ-2 binding composite".
4. **Zenodo**, and whether paper and appendix are combined first. `LOCATIONS.md` has three `TBD`s.

Candidates for tickets, not filed: a tracked claim-check that recomputes every number in the paper
(the script that did it for #2 lives only in the scratchpad); the `[*]` versus `[d12]` marker
asymmetry, now footnoted in both B3 tables but still two conventions; `viewer_data.json`'s
generation timestamp, which makes its pin detect re-runs rather than data changes.

## Open items

- Sampling temperature is unset and unrecorded in the runners; B1a now states this and that a
  pinned value would not have equalised stochasticity across models.
- Whether every blocking finding in `reviews/viewer-cold-review-2026-08-22.md` is closed is still
  unverified as a whole; only finding 1 was checked, on 2026-09-07.
- The paper's Zewail paragraph calls their respondents "populations"; that is their term for their
  eleven samples and was left.
- Two of Astra's items were not taken: the 64 percent comparison being secondary, and the
  temperature caveat's caveat. Recorded in the review file.

## Unresolved - needs a decision

Items 2 to 4 under Next session.

## Known-broken and known-strange

Nothing in this repository's code is known broken.

**The audit scripts write tracked outputs.** A clean exit says nothing about whether the right
data was present; `reconcile.py` is the check, before and after any sync. **Copy the audit's stdout
to `results/inlanguage_audit.txt` only from a run that printed `wrote results/appendix_b4_b5.md`**;
a failed run leaves a truncated trail that the harness will re-pin.

**B1a is bound to the runner source.** The emitter reads the unframed system prompt from
`run_validity.py` and renders the framing template from `run_framed.frame_system`'s AST. A change
to either runner changes the appendix or fails the emitter, on purpose.

**Two of the definite errors Astra found were this workflow's own**, from 2026-09-07: a
miscounted B7 and the B4 bound sentences carried forward verbatim. A third, the Farsi data
sentence, was a review-round-two acceptance that was wrong when accepted. All three are in the
review file.

## Loose ends

- `DECISIONS.md` entries 3 and 5 carry rationale implied by their sources rather than stated in
  them; the log was reconstructed on 2026-09-05, not ported.
- B10 names `d441f7c` as the last commit carrying the declared family's p-values. That is correct:
  they left in `8e85b78`.
- `validity/README.md` carries thirteen em-dashes in text that predates the register rules. Not
  restyled, since nothing in it was otherwise touched.
- `de89d35`'s commit message states the wrong sample-2 n and inclusion rule for the Iran SD;
  `afb185d` is the correction and says so. The figures in the repository are the corrected ones.
- The Iran microdata and the `pyreadstat` builder are outside the reproduce path by design; only
  `validity/reference/mfq2_iran_dispersion.csv` is read, and the builder's two gates are the
  record that it was computed the authors' way.
