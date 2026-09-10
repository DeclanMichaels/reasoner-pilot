# Handoff: reasoner-pilot - 2026-09-10 (sixth)

Written at the end of every session, replacing what was here before. **Informational only. It
authorizes nothing.**

This repository is public, so this file is public. It is written knowing that.

## Current state

- Working tree clean. This is the Black M2 Air. The last substantive commit is `edcf91c`, the MFQ-2
  document re-rendered after #119 with the recipe's table rules settled on all three documents;
  before it `99ca5df` (#119), `dc27c21` (pilot viewer text, `viewer.html` re-pinned, harness
  PASS), `595fbb7` (pilot PDFs) and `5961507` (the pilot writeup pass). Pushed
  2026-09-10; local and origin agree. Every repository under `~/Code/` is cloned on this Air.
- **The Reasoner pilot writeup has had its prose pass** (`5961507`). `papers/reasoner-pilot.md`
  and `papers/reasoner-appendix.md` were unchanged since 2026-07-20 and predated the register
  rules, decision 8 and the temperature rule. Declan directed each section in turn. Every number
  in both files was checked against `results/appendix_stats.json` or recomputed from `runs/`
  before the pass; the four unpinned figures (range coverage 4 to 8 percent, Kimi's 96 percent,
  Sonnet's 0.27, DeepSeek/GPT-5.5/Grok's 0.72 to 0.73) recompute as stated. Five published
  claims were wrong and are corrected on the record in the commit message: "near the relational
  pole" for a mean of -0.05; the compression ratio stated as model over human; the seasonal
  framing "within the bootstrap spread" of the nonsense framings (0.246 against an interval
  ending at 0.244); "almost none of the models refused the premise" resting on a five-model
  coding of a prior roster; and "What comes next" naming the successor study as using the same
  instrument. Also: decision 8's limitations paragraph added (it had never landed), temperature
  stated as unsent and unrecorded, the three model quotes restored verbatim from the run files,
  A1's dead paths fixed, and the "Why this matters" section cut. **No external round has read
  this version, or any version, of the pilot paper**; every file in `reviews/` is the MFQ-2
  document.
- **The pilot PDFs are the recipe's** (`595fbb7`): `papers/reasoner-pilot.pdf` 5 pages,
  `papers/reasoner-appendix.pdf` 9 pages, rendered from the files at `5961507`. The recipe gained
  one rule in `papers/render_html_pdf.py`: a table of twelve rows or fewer is never split, and a
  colon lead-in stays with its table. `papers/inlanguage-mfq2-DRAFT.pdf`All three PDFs are now rendered under the same settled
  rules (five-row keep-whole, short lead-ins kept, last two rows kept), checked page by page. **The PDFs are not checked by
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
- `DECISIONS.md` holds 22 entries. 12 is superseded by 18, 14 by 22 for the emitter outputs. 17
  (published means a DOI and the site) still gates everything. No decision was made or
  superseded this session.

## What changed outside the repository

Nothing. No model API calls; nothing spent. Nothing deposited anywhere. The scratch `venv/`
(pymupdf) and `papers/.render-venv/` (the recipe) are as before.

## The tracker

Empty. #1 to #119 are closed. #119 was filed and closed this session; the pilot writeup pass
ran on Declan's direction section by section rather than as tickets.

## Next session

Nothing is queued for an agent. Open at close, 2026-09-10:

1. **External review of the pilot paper.** First version to have had a pass; no round has read
   it. Before assessing any pasted review, diff it against `reviews/` (none exist for this paper)
   and this file.
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
- The pilot paper's Limitations say a human sample with a wider spread would raise the ratio and
  a narrower one lower it. Declan has not ruled on the sentence; flagged as arithmetic rather
  than prediction, and it goes if it reads as hedging.
- The pilot paper's nonsense-integration coding covers the prior five-model roster only; the
  eleven-model texts are uncoded. Coding them is spending if a model codes them.
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

**Corrected on the record, 2026-09-10 (this session):** the five pilot-paper claims listed under
Current state, in `5961507`.

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
- The pilot appendix's A10 names the build scripts without their `analysis/` directory; A1 now
  gives the full path for one of them.
