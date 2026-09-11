# ChatGPT's review of the Reasoner pilot paper and appendix, 2026-09-10

**Reviewer:** ChatGPT, one of the model families Declan runs adversarial review through; first
round on this paper. It had the clone: it reran `analysis/build_appendix.py` and matched the
committed `results/appendix_stats.json`, read the runners, the scoring function, the human
records and the coding artifacts, and recomputed four diagnostics of its own.
**Reviewed:** the documents at `5961507`, before any change from the cold review.
**Adjudicated:** 2026-09-11. Twelve tickets, #120 to #131. Every computation in the round was
reproduced before filing: the 58/10 respondent split and instrument versions, the ten-respondent
ratios (5.72, 3.69, 6.67, 4.84), the twelve per-item ratios (3.29 to 8.40), the weighting ratios,
the model-cluster bootstrap to four decimals (seed 20260910), the zero imputation in `rtok()`,
`random.sample` without replacement, the 205 exclusions, the old coder premise, the o3-Llama
country error, and the three A5 intervals that differed from the JSON by 0.001 to 0.002. Nothing
touches a numbered decision. Declan's decisions, 2026-09-11: WEIRD clause dropped; scenario grain
leads; A5 re-pinned on the model-cluster bootstrap with Cohen's d dropped; reasoning tokens
reported for seven and not reported for four, correlations dropped, Kimi contrasted with GPT-5.5;
the five-model coding cut from the paper; opening sentence narrowed, title left for later; new
collection and loading audit not scoped, consent pointed at `DATA-LICENSE.md` and decision 6.

## Diff against prior rounds

The cold review of the same day (`reviews/claude-cold-review-pilot-2026-09-10.md`) had raised
the reshuffle claim (its 1), the missing reasoning counts (2), the exclusions (3), the unpinned
numbers (4), the WEIRD citation (5) and the axis-grain weakness (6). This round raises each with
more precision and adds the rest. The cold review's claim that every number reproduced was wrong
on the three A5 intervals; recorded there.

## Adjudication

| # | finding | disposition | ticket |
|---|---|---|---|
| 1 | Human baseline misdescribed: 58 respondents one item per axis (v1.1), 10 all twelve (v1.0); axis ratios not exposure-matched | Verified from the records and recomputed. Description corrected in Summary, Instrument, Limits, A1; per-item and ten-respondent tables emitted into A3; exposure stated as the limitation it is. The assignment-scheme simulation and larger collection are not scoped (Declan) | #120 |
| 2 | Reshuffle claim conflicts with the runners | Verified (cold review 1). Cut; glossary Rerun entry corrected | #121 |
| 3 | A5 intervals resample pooled values, not models; printed intervals off the JSON by 0.001 to 0.002; Cohen's d standardises a mixture | Verified and recomputed. Builder resamples models (20,000 draws, seed 20260910); difference and ratio intervals added; d dropped; `appendix_stats.json` re-pinned, a published-number change recorded in the commit | #122 |
| 4 | Missing reasoning counts imputed as zero | Verified. Seven reported, four not reported; correlations dropped; Kimi against GPT-5.5; accounting stated; no share of output, since xAI counts reasoning outside output | #123 |
| 5 | 0 of 100,000 without replacement is not p < 0.00001 | Verified. Reported as the count, sampling named, p dropped, the three-in-100,000 bound stated; the corrected-SD recount (still 0) added | #124 |
| 6 | Same-lab baseline is 0.4 expected links; o3-Llama are both US | Verified. Results lead with the scenario grain and state the baseline; A6 corrected | #125 |
| 7 | Exclusions unreported; scoring hierarchy misdescribed | Verified (cold review 3). Exclusion table in A1; A2 states the pooled scoring and the axis-level fallback; the paper's position sentence rewritten | #126 |
| 8 | Construct claims overstated; 24 scenarios where an even split is not zero; mac_1 lacks a positive reasoning option | Verified from the bank. Opening sentence narrowed; A2 qualified with the count; a Validity clause added. Loading audit not scoped; title later (Declan) | #127 |
| 9 | Framing shows perspective-following; scaffold shared by all framings; inert control defined by its result | Verified against the prompts. A5, A9 and Limits say the prompts prescribe the principle and share the scaffold; What comes next describes a prespecified control | #128 |
| 10 | Coding was two LLM passes on a prompt asserting triangles superior to circles, prior roster | Verified in `coder_prompt.md` and the codebook. Cut from the paper; the artifacts' status in `results/` is open | #129 |
| 11 | Unpinned prose numbers; A8 weighting shows model SD only; decision 8 code unnamed; exact model IDs; "frontier" | Verified. Range coverage, weighting ratios, per-model ratios and IDs emitted and tabled; `validity/aggregation_artifact.py` named. "Frontier" left (Declan: readers judge) | #130 |
| 12 | WEIRD uncited; A9 convergent-validity wording; "Models correct"; recruitment and consent; sign check circular | Verified. Clause dropped (Declan); A9 reworded, the sign check stated; column renamed; consent pointed at the licence and decision 6. Title and "converge" left for later | #131 |

## Shape of the round

Mechanical and thorough: every claim it made about the code and the records was true, and its
four diagnostics reproduced exactly. It read the repository rather than the prose. Its
positioning asks (a new title, "no association detected in this exploratory analysis", a
defensible core conclusion) were not adopted as written; the underlying corrections were.
