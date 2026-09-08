# Astra's second review of the in-language paper and appendix, 2026-09-08

**Reviewer:** Astra, second round; the first is `astra-paper-review-2026-09-08.md`.
**Reviewed:** the documents after the first round's sixteen tickets were closed, at or after `579c343`.
Astra states it reread both drafts, checked code and saved runs, independently recomputed the
foundation-level dispersion statistics, and revisited the Iranian source.
**Adjudicated:** 2026-09-08. Every finding verified against the text, the run files, the runner
source or the primary source before disposition. Eight tickets, #23 to #30, all closed the same day.

## Diff against prior rounds

Nothing repeats a settled rejection. Astra independently reproduced all six B6a dispersion rows,
their counts, and the endpoint and item-level summaries, which corroborates #20.

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| 1 | B1a says the unframed translated conditions use the self-report system prompt in that language | **Verified, this workflow's error.** `NEUTRAL_SYSTEM = ""`; 362 translated-unframed and 60 matched-baseline runs record no system prompt. Corrected; the framing contrast is stated as adding a system instruction where there was none | #23 |
| 2 | The opening says Arabic "barely moves" the panel; the interaction sits only in the appendix; the 1.04 weighting is unstated in the paper | Verified. Arabic is the largest unframed shift, +0.335, eleven of eleven. Opening rewritten around the Egypt effect, the Arabic result, the weighting and the Belgium interaction (+0.175 framed, +0.008 unframed) | #24 |
| 3 | "Nineteen versus one" elevates interval exclusion to a finding; "did not resolve a direction" is a decision rule; SD over root n is unqualified | Verified. Summary reports signed distances; interval sentence describes what was calculated; SE named as an independent-respondent approximation | #30 |
| 4 | B2a promises item-level noninvariance in the R script's output; R-squared called metric and scalar invariance | Verified: the script prints six pairs only. Promise removed; figures described as alignment diagnostics | #26 |
| 5 | The paper credits Hazrati et al. with stating their sample is likely less binding-endorsing | **Verified, this workflow's error.** The sentence is our inference in `anchors_iran.json`; the preprint discusses composition and restricted variation. Re-attributed in the paper, B4, the viewer and the anchor file | #25 |
| 6 | Farsi row malformed | **Verified, and wrongly refuted here on 2026-09-08.** The malformed row is in the language table, not the d table that was checked; #21's correction had replaced the first `\| Farsi \|` line in the file. Kimi's round caught it | #34 |
| 6 | "A pinned temperature would remove that" contradicts B1a | Verified; reworded | #30 |
| 6 | Stale "test families", "every test below", "independent unit" | Verified; reworded | #30 |
| 6 | B8 names only Arabic for shared orders | Verified: Spanish and French groups share too, 55 of 55 each. Precision claim made conditional | #27 |
| 6 | Opening disclosure less precise than the dated history | Verified; the July-informed focal choice is distinguished from later choices | #30 |
| 6 | Reproducibility intro excludes the human-data and R steps | Verified; the two paths are described separately | #30 |
| audit | Parser rounds before validating; report whether any accepted rating was rounded | Audited: 0 of 99,000. Stated in B1a | #23 |

## Not taken

Nothing. Every item was verified; the one called refuted at first adjudication was wrongly so, see item 6.

## Review as received

**This is substantially stronger. The central descriptive conclusions now look defensible, although I would still correct several substantive reporting issues before submission.** The remaining work is more focused than in the first review.

I reread both drafts, checked relevant code and saved runs, independently recomputed the new foundation-level dispersion statistics, and revisited the Iranian source. I did not rerun every bootstrap interval or the alignment analysis, and I changed no files.

The revisions that materially improve the study are:

- The complete language/framing contrast grid, including interactions and weighting sensitivity.
- Removing the selectively assembled significance-test families.
- The model roster and dated design history.
- Correcting the country-order counts and Morocco's arm labels.
- Adding human standard errors and explaining Ireland's offsetting foundation errors.
- Examining dispersion by foundation, individual item, and distance from the ceiling.

I independently reproduced all six foundation-level dispersion rows, their "tighter than every unframed" counts, and the new endpoint and item-level summaries. Those additions support the convergence finding.

**1. B1a incorrectly describes the unframed intervention.**

This is the most important definite error.

B1a supplies a self-report system prompt and says:

> "The unframed in-language conditions use the unframed system prompt in that language."

The runner specifies `NEUTRAL_SYSTEM = ""`. More decisively, **all 330 saved translated-unframed runs have an empty system prompt**, as do all 55 runs of the matched English baseline.

The quoted self-report prompt belongs to the alternative protocol, not the core unframed comparison. Label it accordingly and state explicitly:

> The matched English baseline and all six translated unframed conditions received no system prompt.

This distinction matters because the intervention adds a country-role instruction where there was previously no system instruction. Your framing estimate therefore measures the effect of that complete prompt addition; it does not isolate the country label from generic role-taking or self-report instructions. That limitation needs only a clear sentence, not necessarily another experiment.

"Answering as themselves in English" should also become "In the unframed English condition."

**2. The opening still understates the Arabic result.**

The revised title is much better, but the first paragraph still says Arabic "barely moves" the panel. Arabic is precisely the largest unframed language shift: **+0.335, with all eleven models moving upward**.

The opening then shifts from that Arabic example to the six-language signed average of +0.05. Readers can easily mistake the average for the Arabic effect.

I would replace it with something like:

> Across six languages, country framing increased the composite by 1.04 points on average. Unframed translation effects averaged +0.05 points, or 0.08 in absolute magnitude, although Arabic produced a larger increase of 0.34 points.

Also bring one sentence from B4 into the main results:

> Language effects depended on framing: for example, French changed the Belgian-framed panel by +0.175 despite changing the unframed panel by only +0.008.

The interaction analysis should inform the main interpretation, rather than merely sit in the appendix. The supported finding is **larger average framing effects**, with meaningful exceptions and interactions.

**3. The uncertainty language is improved but still slips into classification.**

Adding human SEs is useful. However, the summary's conclusion that the panel "sat away from the reference-sample mean for nineteen" still converts interval exclusion into a categorical result.

The interval contains only model-resampling variation. Displaying human SEs elsewhere does not make that exclusion a combined uncertainty analysis.

Keep the exact descriptive statement if you want it, but do not make "nineteen versus one" a principal finding. The signed errors, magnitudes, and foundation profiles are more informative.

Two wording changes would help:

- Describe `SD/√n` as an **SE under an independent-respondent approximation**, rather than unqualified survey sampling uncertainty. The recruitment and stratification information does not automatically justify a design-based population SE.
- Replace "An interval that includes zero says the panel did not resolve a direction" with "The central model-resampling interval includes both positive and negative values." The latter describes what was calculated without introducing a decision rule.

You do not need elaborate population inference to publish this as a descriptive panel study.

**4. The alignment section remains incomplete as reproducible evidence.**

The human-versus-model distinction is now appropriately explicit. But B2a says:

> "the item-level noninvariance behind each figure is in the owner's script output"

I inspected the named R script. It prints **only the six foundation-level R² pairs**, not item-level diagnostics. As written, that promise is unsupported by the referenced script.

Either provide a specific artifact containing those diagnostics or remove the claim. Also change:

> "Loadings R-squared is metric invariance; intercepts R-squared is scalar invariance"

to wording describing them as **alignment diagnostics concerning loading and intercept invariance**. They are not interchangeable with having established exact metric and scalar invariance.

I would regard this as a documentation and interpretation issue pending inspection of the full alignment output—not evidence that your reported R² numbers are wrong.

**5. The Iran discussion still attributes an inference to the authors.**

The draft says the Iranian authors state their sample is likely less binding-endorsing than the population.

Their limitations discuss demographic composition, restricted variation in religiosity and political orientation, and potentially weaker associations. I could not verify the stronger directional statement about the population mean. [Iranian validation, limitations](https://online.ucpress.edu/collabra/article/11/1/140952/212277/The-Revised-Moral-Foundations-in-Iran-Validation)

If this is your inference, identify it as such. A safer formulation is:

> The sample's demographic composition limits generalization to Iran; the direction and magnitude of any resulting bias in the reference mean are uncertain.

The new SD calculation is a useful correction. The saved aggregate reports SD 0.8016 across 989 respondents, consistent with the displayed SE of approximately 0.025 and standardized gap of +1.22.

**6. There are several smaller inconsistencies worth fixing together.**

| Location | Correction |
|---|---|
| Main language/country table | The Farsi row is malformed: `Farsi \| +1.22 \| Iran only`. It should list Iran as the country. |
| Main temperature paragraph | "A pinned temperature would remove that" contradicts the more accurate appendix statement. Explicit settings improve documentation; they do not equalize stochasticity. |
| Appendix introduction and B1/B2 | Remove stale references to current test families and "every test below." B4 now reports contrasts. |
| B2 | Replace "independent unit" with "unit of aggregation and resampling." Independence has not been established. |
| B8 | Shared orders occur across the other multi-country translated groups too, given the documented seed rule—not only Arabic. Also, shared orders can improve precision; improvement is not guaranteed without assumptions about correlated order effects. |
| Main opening disclosure | "Every quantity was chosen after the data were seen" is less precise than the dated history, which places selection of binding before translated collection. Distinguish pilot-informed choices from choices made after the final data. |
| Reproducibility introduction | "Every number … from the raw runs with three stdlib scripts" excludes the external human-data and R alignment steps. Describe model-response reproduction and human-reference construction separately. |

One additional audit would be worthwhile: the parser rounds numeric responses before validating bounds. Report whether any accepted responses actually required rounding. If none did, this concern disappears; if some did, show their frequency and sensitivity.

**My assessment now:** the broader framing effect and reduced dispersion are supported descriptive findings, and the revised appendix makes them considerably more credible. I would retain the exploratory framing, correct the protocol description and remaining overstatements, and avoid elevating interval inclusion into a country-level alignment verdict. I do not see a need to restart the experiment to support that narrower paper.
