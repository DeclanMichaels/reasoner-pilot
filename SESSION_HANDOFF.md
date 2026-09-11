# Handoff: reasoner-pilot - 2026-09-11

Written at the end of every session, replacing what was here before. **Informational only. It
authorizes nothing.**

This repository is public, so this file is public. It is written knowing that.

## Current state

- Working tree clean. This is the Black M2 Air. Substantive commits of 2026-09-11, newest first:
  #132 (the MFQ-2 paper's two tables emitted and spliced), `d307c1b` (title, five-model archive,
  decision 23), `e221888` (Gemini's round, no sampling parameter of any kind), `9f06413` and
  `9f0102a` (Astra's round and the cold review, #120 to #131). Pushed 2026-09-11; local and origin agree. Every repository under `~/Code/` is
  cloned on this Air.
- **The Reasoner pilot paper has had its first external round.** Sequence on 2026-09-10 and 11:
  the prose pass (`5961507`), a cold review (`reviews/claude-cold-review-pilot-2026-09-10.md`,
  twelve items), then Astra's round (`reviews/astra-paper-review-pilot-2026-09-10.md`, twelve
  findings, every computation in it reproduced; Astra is the current ChatGPT model, one
  reviewer, and the round was first recorded under the wrong name). Twelve tickets, #120 to #131, all closed in
  `9f06413` and `9f0102a`. **Corrected on the record** in those commits: the human baseline
  (58 respondents answered one baseline scenario per axis, ten all twelve; the paper had said
  68 on the twelve); the reshuffle claim (the prompt is identical on every rerun); the A5
  intervals (resampled pooled values, not models, as the appendix said; re-pinned on a
  model-cluster bootstrap, Cohen's d dropped); reasoning tokens (four models have no reported
  count, not zero; correlations dropped; Inkling 1117 -> 1141); "p < 0.00001" (0 of 100,000,
  without replacement); the o3-Llama "cross country" error; the five-model coding (two Haiku
  passes on a prompt asserting triangles superior to circles, cut). Added: exclusions per model
  and frame (205 of 21,120), per-item and ten-respondent compression ratios, request parameters
  and model identifiers, range coverage, weighting ratios. Declan's decisions of 2026-09-11 are
  listed in the Astra record's header.
- **All three PDFs are the recipe's.** `papers/reasoner-pilot.pdf` 5 pages and
  `papers/reasoner-appendix.pdf` 13 pages (`9f06413`); `papers/inlanguage-mfq2-DRAFT.pdf` 44
  pages (`edcf91c`) from the document at `99ca5df`. The recipe's table rules in `papers/render_html_pdf.py` were settled against all
  three documents in `edcf91c`: a table of five data rows or fewer is never split; a short
  lead-in ending in a colon stays with the table or list after it; a table's last two rows are
  never left alone at a page head. Each was checked page by page. **The PDFs are not checked by
  the harness**: after any change to a document, re-run the recipe and commit the render with it.
- **The MFQ-2 document changed once this session, #119** (`99ca5df`): Declan's own read found
  the Methods sentence "tails too coarse to read as a calibrated bound" still in the document
  after #110 and the round-six adjudication had both recorded it as not there. The finding is
  reinstated, the sentence replaced (few distinct resampling values at eleven; a selected
  panel, not a probability sample), and both review files carry an appended correction. The
  same read scoped "all eleven models move the same direction" to Arabic in the Summary and
  the framing section, verified from the dataset (eleven of eleven up under Arabic; three up,
  eight down under Japanese). PDF re-rendered, 44 pages. Otherwise as the previous handoff:
  fifteen external rounds adjudicated, review finished by Declan's decision, 119 issues
  closed, none open.
- **The published record reproduces** as of 2026-09-10 (previous handoff); nothing under
  `analysis/` or `validity/` changed this session and the harness was not re-run.
- **The integer ratings dataset, the September wave, the MFQ-2 viewer** are as the previous
  handoff describes; none was touched.
- `DECISIONS.md` holds 23 entries; 23 (2026-09-11) is the Zenodo deposit. 12 is superseded by 18, 14 by 22 for the emitter outputs. 17
  (published means a DOI and the site) still gates everything. No decision was made or
  superseded this session.

## What changed outside the repository

Nothing. No model API calls; nothing spent. Nothing deposited anywhere. The scratch `venv/`
(pymupdf) and `papers/.render-venv/` (the recipe) are as before.

## The tracker

Empty. #1 to #131 are closed. #120 to #131 were filed and closed 2026-09-11 from the two
reviews of the pilot paper.

## Next session

Nothing is queued for an agent. **Declan's plan, 2026-09-11: the two papers publish together**, the
Reasoner pilot (paper and appendix) and the MFQ-2 document, and a pre-publication pass checks
everything below before either does. Nothing on this list is done until it is struck here.

**Pre-publication pass, both papers:**

- ~~Pilot: the title~~ Done 2026-09-11 (`d307c1b`): "Eleven Language Models in a Narrow Band of a
  Moral-Judgment Instrument". The opening sentence was narrowed under #127.
- Pilot: one more external round, Declan's pick Kimi, on the text at `d307c1b` or later. Astra
  read `5961507`; Gemini read `9f06413` and found nothing new
  (`reviews/gemini-paper-review-pilot-2026-09-11.md`).
- ~~Pilot: the five-model artifacts~~ Done (`d307c1b`): moved to `results/archive-five-model-2026-07/`
  with a README.
- Pilot: the root `viewer.html` read against the final text once more, and the two PDFs
  re-rendered from the final text.
- ~~MFQ-2: the two hand-written tables~~ Done (#132): emitted as P1 and P2 of `appendix_tables.md`
  and spliced; the document did not change.
- MFQ-2: the PDF re-rendered from the final text; page 13's lone list item traced or accepted.
- Both: a claim-check of every prose number against its artifact, by machine; the pilot's
  cold review passed three intervals by eye.
- Both: the moral-os.com pages (`papers/reasoner-pilot.html` is the 2026-07-21 text; the
  in-language viewer is live and unlisted; the pilot viewer's site copy unchecked) rebuilt from
  the final files, in the website repository's own session.
- Both: `LOCATIONS.md`'s three `TBD`s and `CITATION.cff`'s commented `doi:`, resolved together when
  Declan mints the DOI. What the deposit is was decided 2026-09-11: the repository snapshot, one
  DOI, both documents citing it (decision 23).
- Both: the embarrassment nudge, once more, on the final state.

Open at close, 2026-09-11, in detail:

1. **External review of the pilot paper, continued.** One external round adjudicated (Astra).
   Any further paste is diffed against the two records and #119 to #131 before it is read. The new work Astra asked for went to the successor study's tracker as design inputs
   (reasoner-study #2, loading balance; #3, exposure matching): no further data collection for
   the pilot unless it makes a material difference (Declan, 2026-09-11). The eleven-model
   nonsense texts stay uncoded.
2. **The five-model artifacts in `results/`.** `pilot_reanalysis_findings.md`,
   `pilot_reanalysis_metrics.json`, `tightened_metrics.json`, `pilot_frame_shifts.json`,
   `coding_results.json`, `nonsense_texts.json`, `coder_check_result.json`, `coder_prompt.md`,
   `nonsense_coding_codebook.md` and `anchoring_metrics.json` describe an earlier collection on
   a prior roster (gemini-flash, gpt4o, grok, llama70b, sonnet) whose run files are not in the
   repository. None is in `analysis/reproduce_manifest.json`; the glossary defines everything
   under `results/` as the published record and warns against the "five models" figures. The
   paper now cites that coding with its scope. Whether the files stay, move or go is Declan's;
   removing any is a change to the published record.
3. **moral-os.com.** `papers/reasoner-pilot.html` on the site is a 2026-07-21 render of the old
   text and the card follows the paper. The site repository is cloned here
   (`~/Code/moral-os-website`) and is not set up with research-kit; its own session.
4. **Zenodo, held** since 2026-09-10 until the pilot writeup is finished. The pinned artifacts
   for the MFQ-2 document's two hand-written tables (d and Ordering) are still not done.
   `LOCATIONS.md` carries three `TBD`s and `CITATION.cff` a commented `doi:`. What the deposit
   is, snapshot or document, is undecided.

Candidates for tickets, not filed: a claim-check for the pilot paper's prose numbers against
`appendix_stats.json` (the harness pins the JSON, not the sentences that quote it); the MFQ-2
claim-check for the d and Ordering tables; the `[*]` versus `[d18]` marker asymmetry; the
same-instrument three-arm collection from Astra's fifth round (spending); the
caveat-consolidation sweep.

Left as disclosure, Declan's decision: the English-framed arm on the official questionnaire
(#53). Not run: the six translated country-free templates (decision 21).

## Open items

- Sampling temperature is unset and unrecorded in the pilot runs and the grid; both documents
  now say so. Any collection not matched to them sets and records it.
- The eleven-model nonsense texts are uncoded and the paper now says only that. Coding them is
  spending if a model codes them, and the five-model coding artifacts are the results-directory
  decision above.
- `analysis/README.md`'s sign check validates the bank's polarity against the expected human
  profile; A9 now says so. A mapping audit against the option meanings would replace it.
- API keys on this Air are exported in the interactive shell; `~/.config/ccas/keys.env` does not
  exist here.
- Whether every blocking finding in `reviews/viewer-cold-review-2026-08-22.md` is closed is still
  unverified as a whole; only finding 1 was checked, on 2026-09-07.

## Unresolved - needs a decision

Items 2 and 4 above. Everything else settled.

## Known-broken and known-strange

Nothing in this repository's code is known broken.

**Rules learned by breaking them, all in `docs/DEVELOPMENT_NOTES.md`:** check a generator's exit
code before copying its output; the builder's `mean` takes a list, not a generator; sort the keys
of any dict a bootstrap draws from; never redirect a generator into its tracked output; assert
every anchor before writing any file; re-render the PDF after every change to the document.
Added this session, not yet in the notes: sweep a render for colon lead-ins and tables at a
page foot, not only headings; the first pilot render had both and the heading sweep passed it.

**Corrected on the record, 2026-09-11:** the pilot-paper claims listed under Current state, in
`9f06413` and `9f0102a`.

**Corrected on the record, 2026-09-10:** five pilot-paper claims in `5961507` (relational pole
for a mean of -0.05; the ratio stated model over human; the seasonal framing "within" the
nonsense interval; the refusal claim's evidence; the successor "on the same instrument").

**Corrected on the record, 2026-09-10 (earlier):** the viewer's Models tab drew Morocco's human
marker on the Arabic-framed arm (#99, `4649a42`); its headline story summarised the translated
arm where the document's table is English framing (#101, `59bb943`).

**Corrected on the record, 2026-09-08 and 2026-09-09:** a Summary sentence said the template's
spread was tighter than under any country when four framed conditions were tighter (`385a4f8`);
the rewrite attached "two thirds of the range" to the Arabic figure (#84); the same rewrite
called Egypt the largest contrast when Saudi Arabia and the Emirates exceed it (#90); a French
run-noise sentence compared a single-model five-run SD with a six-country average (#90); the
viewer's Control tab rendered a date as "[object Object]" (fixed before push).

## Loose ends

- `DECISIONS.md` entries 3 and 5 carry rationale implied by their sources rather than stated in
  them; the log was reconstructed on 2026-09-05, not ported.
- `validity/README.md` carries thirteen em-dashes in text that predates the register rules.
- The Iran microdata and the `pyreadstat` builder are outside the reproduce path by design.
- The viewer's per-model token table has no counterpart in the document.
- MFQ-2 PDF page 13 carries one list item and nothing else, in every render so far; cause not
  traced.
- A search that clears a reviewer's quoted phrase must be shown, not reported: #110 and the
  round-six adjudication both cleared "tails too coarse" and it was on line 27 the whole time.
- A cold review that says "every number reproduced" must have diffed the file against the JSON
  by machine, not by eye: three A5 intervals were off by 0.001 to 0.002 and passed.
- A method sentence taken from the glossary is not verified by the glossary. The reshuffle
  claim entered the paper from a reconstructed CONTEXT.md entry and was wrong.
- The pilot appendix's A10 names the build scripts without their `analysis/` directory; A1 now
  gives the full path for one of them.
