# Handoff: reasoner-pilot - 2026-09-08

Written at the end of every session, replacing what was here before. **Informational only. It
authorizes nothing.**

This repository is public, so this file is public. It is written knowing that.

## Current state

- Local and remote agree, and the working tree is clean apart from this file. The session's work
  is 30 commits since `303e79e`, `8336de4` to `9d0d099`.
- **The published record reproduces**, run 2026-09-08, no keys and no network: 15 regenerated
  outputs reproduced, 17 committed-only outputs verified.
- **Six adversarial rounds on the in-language paper and appendix are adjudicated and worked
  through**, all in `reviews/`: Astra's first (sixteen tickets), Grok's (one), Astra's second
  (eight), DeepSeek's (folded into those eight), Gemini's (three) and Kimi's (six). Thirty-nine
  issues have existed; none is open.
- **The paper is retitled** and every number in it recomputes from the cells. **Every data
  section of the appendix is generated**; the splice map is in `docs/DEVELOPMENT_NOTES.md`. B4 is
  a contrast set over the full grid with intervals, sign counts and leave-one-out ranges and no
  p-values (decision 15); B10 is the errata for the withdrawn family.
- `DECISIONS.md` holds 17 entries. Entry 16 records Iran's anchor, settled on 2026-09-07; entry 17
  defines published as a DOI plus moral-os.com and strikes the errata section from the appendix.
- This is the Black M2 Air. `validity/` holds the completed grid: `runs/` 165, `runs_framed/`
  1,267, `runs_framed_lang/` 1,246, `instruments/` 15. `validity/reconcile.py` reports it identical
  to the 2026-09-05 archive.

## What changed outside the repository

`reasoner-study` received decision 27 (`ff05433`) and a pointer to it in its reference README
(`53bc0dc`), both pushed, private. Two of its reference files are documented copies here.

Hazrati et al.'s two respondent-level SPSS files were downloaded from their view-only OSF project
into `validity/reference/_raw/`, which is gitignored, and read with `pyreadstat` in a scratchpad
virtualenv. Only the aggregate `mfq2_iran_dispersion.csv` is committed. The Atari and Hazrati
preprints and the Zewail PMC text were read for the Astra round; the PDFs are in the scratchpad.
The viewer was rendered locally to verify its relabelled intervals.

No model calls, nothing written to S3, nothing spent.

## The tracker

Empty. #1 to #22 are closed, each with its disposition on the ticket. #21 closed on Declan's
ruling that the authors' shared respondent-level data may be used; #22 was Grok's one item.

## Next session

Nothing is queued for an agent. What remains is yours:

1. **Review.** Five families have read; Kimi read the state after Gemini's round was worked.
   Every family raised the same four things - panel composition, temperature, five runs, the
   framing prompt's two components - and the documents now state each. What remains unread is
   the state after Kimi's six fixes.
2. **The title.** Kimi proposes "adding a country-role instruction shifts responses more than
   translating the questionnaire", on the ground that framing is an added instruction where there
   was none. The methods and B1a now say that; whether the title follows is yours.
3. **The viewer's title against the paper's.** The paper is now "Country framing shifts MFQ-2
   responses more than questionnaire language in an eleven-model panel"; the viewer still says
   "In-language society framing - MFQ-2 binding composite".
4. **Zenodo**, and whether paper and appendix are combined first. `LOCATIONS.md` has three `TBD`s.

Candidates for tickets, not filed: a tracked claim-check that recomputes every number in the paper
(the script that did it for #2 lives only in the scratchpad); the `[*]` versus `[d12]` marker
asymmetry, footnoted in B3 and named in decision 16; `viewer_data.json`'s generation timestamp,
which makes its pin detect re-runs rather than data changes.

## Open items

- Sampling temperature is unset and unrecorded in the runners; B1a states this and that a pinned
  value would not have equalised stochasticity across models. Grok's next steps, a larger panel
  with pinned temperature, a direct estimate-versus-answer-as comparison, and preregistered
  contrasts on held-out countries, are recorded as not taken here: each needs new collection.
- Whether every blocking finding in `reviews/viewer-cold-review-2026-08-22.md` is closed is still
  unverified as a whole; only finding 1 was checked, on 2026-09-07.
- The paper's Zewail paragraph calls their respondents "populations"; that is their term for their
  eleven samples and was left.

## Unresolved - needs a decision

Items 2 and 3 under Next session. **Iran's anchor is settled**, decision 16: Hazrati sample 2 at
3.333, kept, marked `[*]` wherever it enters, disclosed in B4 with the sensitivity across all
three anchors the source offers. Its person-level SD now comes from the authors' own composite
columns, sample 2, n=989, SD 0.802.

## Known-broken and known-strange

Nothing in this repository's code is known broken.

**The audit scripts write tracked outputs.** A clean exit says nothing about whether the right
data was present; `reconcile.py` is the check, before and after any sync. **Copy the audit's stdout
to `results/inlanguage_audit.txt` only from a run that printed `wrote results/appendix_b4_b5.md`**;
a failed run leaves a truncated trail that the harness will re-pin.

**B1a is bound to the runner source.** The emitter reads the unframed system prompt from
`run_validity.py` and renders the framing template from `run_framed.frame_system`'s AST. A change
to either runner changes the appendix or fails the emitter, on purpose.

**Things this workflow got wrong on 2026-09-08 and corrected on the record.** The first Iran SD
build used a more permissive inclusion rule than the authors' (`afb185d` corrects it). Iran's
anchor, settled on the 7th, was carried as open until the 8th (decision 16). B1a said the unframed
conditions carried a self-report system prompt when they carried none, and the Iran caveat was
credited to the authors when it was ours; both were the 7th's writing and Astra's second round found
them (#23, #25). Striking B10 broke the emitter for one commit (`0cb58e0` fixes it), and the Iran
re-attribution reached only the paper on the first pass (`8ef77a0`). The #21 correction put a
d-table row into the language table by replacing the first line beginning `| Farsi |`, and two
reviewers who flagged it were told it was well-formed after the wrong table was checked; Kimi's
round caught it. The E2 sign was quoted backwards for one commit. Each is in its commit message.

## Loose ends

- `DECISIONS.md` entries 3 and 5 carry rationale implied by their sources rather than stated in
  them; the log was reconstructed on 2026-09-05, not ported.
- `validity/README.md` carries thirteen em-dashes in text that predates the register rules. Not
  restyled, since nothing in it was otherwise touched.
- The Iran microdata and the `pyreadstat` builder are outside the reproduce path by design; the
  builder's two gates, the authors' own composite columns to 0.0000 and their published means to
  0.005, are the record that it was computed their way.
