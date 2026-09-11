# Claude's cold review of the Reasoner pilot paper and appendix, 2026-09-10

**Reviewer:** Claude (Fable 5.1), the workflow that rewrote both documents earlier today. Not an
independent adversarial review; the external rounds are, and the first (Astra) is held until this
one is adjudicated.
**Reviewed:** `papers/reasoner-pilot.md` and `papers/reasoner-appendix.md` at `5961507`, with the
run files, `results/appendix_stats.json`, the call layer (`refresh_runner.py`), the scoring
function (`scenario_bank.py`), the scenario bank and `CONTEXT.md`.
**Adjudicated:** 2026-09-11, together with ChatGPT's round of 2026-09-10, which raised items 1 to 6
with more precision (`reviews/chatgpt-paper-review-2026-09-10.md`). Tickets #120 to #131. Items 1
to 4, 7, 8, 10 and 11 applied; 5 and 6 decided by Declan (clause dropped; scenario grain leads);
9 added as one clause; 12 noted. **Correction:** "Every number reproduced" below was wrong on the
three A5 intervals, which differed from the JSON by 0.001 to 0.002; ChatGPT caught it.

## What was checked

Every number in both files against `appendix_stats.json` or by recomputation from `runs/`: the
four compression ratios, intervals and p-values; the human means and medians; the four reliability
ratios; the seven per-framing displacements, the three group means and the 0.56 and 0.95; the four
direction shifts and their 11 of 11; the nonsense-direction means and 0 of 11; both nearest-
neighbour tables and the Opus top three; the eleven token means and distances, the -0.48 and the
four axis correlations; the b12 and all-48 SDs; the three weighting rows; the 13-model SDs; the
decision 8 ratios and noise shares; the range coverage (4.0 to 7.9), Kimi's token share (95.5),
Sonnet's 0.27 and DeepSeek, GPT-5.5 and Grok's 0.72 to 0.73; the human per-axis n (68 on each);
the scenario split (twelve per axis, three per axis in the baseline twelve); the option counts
(93 questions with three, 3 with four); the loading set; the blank-question rule in the code; the
three quotes against the run files. Every number reproduced. The findings are about method
statements the code does not support, exclusions the documents do not report, and numbers with
no artifact.

## Diff against prior rounds

None exist for this paper. The five corrections in `5961507` and #119's class (a phrase cleared as
absent that was present) are the only record.

## Findings, ranked

| # | severity | finding | verification | proposed disposition |
|---|---|---|---|---|
| 1 | high | "statement order reshuffled each time" (What we measured) is not what the runner does. `alloc_prompt` lists options in bank order on every call; neither runner shuffles anything. The only per-rerun difference is the request seed, 1000 plus the rerun index, where a provider accepts one. | `grep -i shuffle *.py` finds nothing; `refresh_runner.alloc_prompt` enumerates `s['judgment']['options']` in order. The sentence came in today from `CONTEXT.md`'s Rerun entry, which was reconstructed on 09-05 and is wrong for this collection. | Cut the clause from the paper; correct the glossary entry. Method claim, so a recorded correction. |
| 2 | high | Reasoning-token counts are provider accounting under a request that asked for no reasoning, and neither document says so. The Anthropic branch sends no thinking parameter and records reasoning as `None`; Cohere and Mistral record `None`; OpenAI, xAI and Together report `reasoning_tokens`; Google reports thoughts. "The four with none" are two Anthropic models run without extended thinking, Mistral with no field, and Llama at zero. The r = -0.48 and the "does not predict position" sentence mix configuration with behaviour. | `refresh_runner.py` lines 40 to 46, 33 to 36, 78 to 80. | A7 and What we measured state how the counts were obtained and that no reasoning setting was sent; the paper says "returned no reasoning tokens" rather than "generate none"; the Results sentence carries the caveat. |
| 3 | medium-high | Extraction failures are excluded from every score and neither document reports them. A1 says each cell is 240 responses; scoring drops responses whose weights could not be parsed. Panel totals of 1,920: Kimi 99 (5.2 percent, 31 of the 60 in its geometry cell), MiniMax 53, Mistral Large 24 (21 call failures), o3 17, Inkling 7, Grok 4, Llama 1, the rest 0. Command A, used in A8, lost 176 of 720. The Kimi geometry cell underlies the per-model ratio paragraph. | Counted from `runs/`; every builder filters `extraction_failed` (`build_appendix.py` 44, `build_figures.py` 90, `build_viewer_data.py` 55 and 93, `build_csv.py` 48). | A1 reports the exclusion per model and the worst cell; the paper's reasoning section notes Kimi's geometry cell is scored on 29 of 60. |
| 4 | medium | Four prose numbers have no artifact: 4 to 8 percent (Summary), 96 percent (Results), 0.27 and 0.72 to 0.73 (reasoning section). All recompute, by hand, today. | Not in `appendix_stats.json`; not emitted by any script. | `build_appendix.py` emits range coverage, per-model token share and per-model nonsense-to-cultural ratio; A5, A7, A8 carry them. Moves a pinned output; the commit says so. |
| 5 | medium | "the profile reported for WEIRD samples" (Results, Limitations, A9) cites nothing, and neither document cites any source. | Text. | Question for Declan: which source, or drop the clause and describe the profile as this sample's. |
| 6 | medium | Axis-grain nearest neighbours are Pearson r over four values (two degrees of freedom); A6 says the correlations are high for that reason, and the Results lead with the axis grain ("every model's nearest neighbor is from another company"). The scenario grain, 48 values, carries the claim. | A6 and `build_appendix.py` 109 to 112. | Question for Declan: lead the Results with the scenario grain and keep the axis grain in A6, or leave. |
| 7 | low-medium | Request parameters unstated: seeds go to OpenAI, xAI, Together and Mistral, not to Anthropic, Google or Cohere; token ceilings are 3072 Anthropic, 4096 OpenAI and xAI, 6144 Together and Google, 2048 Mistral and Cohere; the framing is the system prompt. The MFQ-2 document's Request paragraph has the form. | `refresh_runner.call_model`. | One Methods paragraph in the paper or A1. |
| 8 | low | The paper's "0.031 from the panel center" is on all 48 scenarios while the compression table beside it is on the baseline twelve; only A7 says which. | A7. | Add "on all 48 scenarios". |
| 9 | low | Decision 8's paragraph corrects the ratios; A3's p-value is on the uncorrected model SD. With the corrected SDs (0.065, 0.055, 0.065, 0.070) the count is still 0 of 100,000 on every axis; the smallest 11-human draw SD seen in 20,000 draws is 0.085. | Recomputed, seed 20260720. | One clause in the Rerun averaging block, or leave. |
| 10 | low | `CONTEXT.md` disagrees with the paper in two entries besides Rerun: Framing lists nine conditions including `weekday`, which was never run, and says the placebos "set the noise floor" where the paper says no framing holds the models still. | Glossary text; `runs/` has no weekday cell. | Glossary edits, with the Rerun fix. |
| 11 | low | A2 says fractional loadings are "0.3, 0.5, 0.7"; the bank's are +0.3, -0.3, +0.5, -0.5 and +0.7. | `scenarios.json`. | Say signed, or leave. |
| 12 | low | `models.json`'s internal note says "14 subjects across 8 labs"; the roster has fifteen keys and nine labs. Not in either document. | File. | Note only. |

## Shape of the round

Items 1 to 3 are the same class as #119: statements about method that nobody had checked against
the code, one of them written today from a glossary that was itself reconstructed. Items 4 and 7
are the pilot lacking what the MFQ-2 document gained through its rounds. Items 5 and 6 are
questions. Nothing here touches a numbered decision; item 1 touches `CONTEXT.md`.
