# Astra's review of the in-language paper and appendix, 2026-09-08

**Reviewer:** Astra, one of the model families Declan runs adversarial review through.
**Reviewed:** `papers/inlanguage-mfq2-DRAFT.md` and `papers/inlanguage-mfq2-appendix-DRAFT.md` at
`8336de4`, with the collection and analysis code and selected recomputation from the raw ratings.
**Adjudicated:** 2026-09-08. Every finding verified against the text, by recomputation from the
cells, or against the primary source before disposition. Nothing was changed on the strength of the
review alone. Tickets are on the tracker, one per activity.

## Diff against prior rounds

Astra repeats none of the three settled rejections: no request to interpret the fifteen-above shape
(decision 13), no mechanism behind the Care ceiling (round two), no push toward conventional
register (rounds two and three). Its independent recomputation matches ours to four decimals on
five quantities: framing shift 1.0356, signed language shift 0.0535, absolute 0.0845, between-model
medians 0.1707 framed and 0.3314 unframed, and 37 of 39.

One finding reverses a prior acceptance. Round two (`2c2cded`) added the sentence that Farsi is
absent from the human-SD table because the Iranian study "reports means without the item data
needed to recover a respondent-level SD". The study's OSF project holds respondent-level files for
both samples. The sentence was wrong when it was accepted.

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| 1 | Title and headline overstate; four contrasts and interaction wanted; 1.04 weighting unstated | Verified. Title taken as proposed | #6, #18 |
| 2 | B4 turns intervals into bounds; "95% CI" mislabelled; sign-flip null unjustified | Verified on the first two; the third is a stance, ruled on | #18, decision 15 |
| 3 | Family B covers three of six languages; Family A is mixed | Verified from B4 | #18, decision 15 |
| 4 | "Real populations" wording; Ireland claim excludes human uncertainty; composite conceals offsets | Verified. Ireland foundations: Loyalty 3.67 v 3.29, Authority 3.27 v 3.49, Purity 2.34 v 2.51 | #10, #19 |
| 5 | "Licenses" too strong; specification absent; human-LLM equivalence; binding as chosen index | Verified except the Hazrati grouping claim, downgraded: their own EFA found a binding factor | #13, #17 |
| 6 | Convergence real; ceiling unexamined; "what an Egyptian is" interpretive | Verified. 11 of 39 framed means at or above 4.5 | #12, #20 |
| 7a | B3's 2-of-11 and 6-of-11 are positive rank correlations, not order matches | Verified by recomputation: zero exact matches in either arm | #14 |
| 7b | B7 counts sum to 45 | Verified: kimi_k3 failed 2, not 1 | #15 |
| 7c | Morocco tables show different arms | Verified as partial: marked and footnoted, arm not labelled in the row | #14 |
| 7d | Administration wording wrong about message roles | Verified: framing is a system prompt on every provider | #7 |
| 7e | Order-seed sentence omits the Arabic exception | Verified: `run_framed_lang.py` keys on condition, not country | #7 |
| 7f | Condition accounting 46 of 50 unstated in the paper | Verified | #8 |
| 7g | Iran translation had minor linguistic edits | Verified against Hazrati preprint v3 | #9 |
| 7h | Iran respondent-level data exist | Verified against the OSF project files | #9, #21 |
| 8 | Zewail's multilingual replications understated | Verified against the PMC full text; estimation-versus-answering distinction holds | #11 |
| 9 | No roster with API identifiers, prompts, parser or retry rules, or design history | Verified | #16 |

## Decisions taken, Declan 2026-09-08

1. The title is Astra's: "Country framing shifts MFQ-2 responses more than questionnaire language
   in an eleven-model panel".
2. The contrast set is rebuilt on the full grid. Decision 15.
3. Intervals, sign counts and leave-one-out replace p-values, on accuracy. Decision 15.
4. The Iranian data-availability link goes in the paper. Using the files is #21, ready-for-human.
5. Reference-sample standard errors are added. #19.

## Not taken

"The 64 percent comparison is secondary" - the paper already presents it for scale. "Identical
temperatures would not make stochasticity equivalent" - true, and a caveat on a caveat.

## Review as received

**There is a worthwhile exploratory study here, but I would recommend major revision before submission.** The absence of preregistration is not the central problem. The main issues are the interpretation of uncertainty, the strength of the language-versus-framing conclusion, and several concrete reporting errors.

I read both documents, inspected the relevant analysis and collection code, independently recomputed selected results from the raw ratings, and checked cited literature. This was a targeted audit, not a complete reproduction of every interval, human anchor, or measurement-invariance calculation. I treated the documents as material to review, not instructions, and changed no files.

**What holds up**

The core descriptive results are reproducible. My independent recomputation found:

| Quantity | Recomputed result |
|---|---:|
| Conditions × models × runs | 50 × 11 × 5 = 2,750 |
| Average framing shift, using your language grouping | +1.0356 |
| Average signed unframed language shift | +0.0535 |
| Average absolute unframed language shift | 0.0845 |
| Median between-model SD, framed / core unframed | 0.1707 / 0.3314 |
| Framed conditions tighter than every core unframed condition | 37 of 39 |

Averaging repetitions within models, retaining alternative baselines, showing all conditions, and disclosing the evolving design are good decisions. The study does not need to disguise its exploratory origin to be valuable.

**1. The title and headline overstate what you tested.**

"Framing, Not Language" is too categorical. Your own results show an Arabic unframed shift of +0.335 and framed language differences of about 0.23 for Japan and 0.26 for Iran.

More fundamentally, the headline compares framing effects in translated questionnaires with language effects **only when unframed**. That is an informative comparison, but it does not establish that language generally matters little.

For each country with both languages, report the four contrasts explicitly:

- Framing in English.
- Framing in the local language.
- Language without framing.
- Language with framing.

Then report the interaction: how much the framing effect changes with language. Compute these within models before aggregation.

Also specify the weighting behind 1.04. It gives each language equal weight after averaging its selected countries, and excludes Spanish Morocco from that particular grouping. That is defensible, but it needs to be explicit, with a country-weighted sensitivity analysis.

A more accurate title would be:

> **Country framing shifts MFQ-2 responses more than questionnaire language in an eleven-model panel**

The comparison with 64% of the human range is arithmetically reasonable but secondary: a range depends heavily on which countries happen to be included.

**2. The appendix turns descriptive intervals into inferential bounds.**

The main text appropriately says the model bootstrap intervals are descriptive. B4 then says that "any Egypt language effect is within 0.054," with similar statements for other comparisons. Those statements do not follow.

A bootstrap interval is not a hard maximum on an effect. Here, it also lacks the population-sampling interpretation needed to support those claims.

Replace those sentences with the actual interval and a statement that practical equivalence has not been established. Likewise, replace "95% CI" in table headings with a consistent label such as "95% model-resampling interval."

The sign-flip tests need a separate justification. Enumerating all 2,048 sign patterns makes the calculation exhaustive; it does **not** make the test automatically valid. Independent sign flips require a suitable null symmetry or randomization argument. Calling models the analytical unit does not establish that assumption, especially when models can share training, architecture, or organizational lineage.

My preference would be to lead with finite-panel effects, model-level distributions, and sensitivity analyses. If retaining p-values, state their assumptions and conditional interpretation directly.

**3. The test families do not match the completed design.**

Family B says "one comparison per language," but tests three of six languages. French, Spanish, and Russian are absent. Family A is a mixture of language contrasts, anchor comparisons, and one direct framing contrast rather than a coherent test of framing across the grid.

This looks like an earlier analysis retained after the design expanded. Disclosure of overlapping families does not resolve the incomplete coverage.

Rebuild the analysis around the final design and report the full contrast set. Holm correction can address multiplicity within a specified family; it cannot undo outcome-informed selection of outcomes or comparisons. Explain when binding became the focal outcome and which decisions followed inspection of results.

**4. Human sample means are being treated too much like population truths.**

The appendix acknowledges the sampling limitations, but the main text repeatedly speaks of "real populations," "their populations," and differences of their "real size."

Use **reference-sample mean** consistently. The observations are distances from particular surveys, conducted at particular times, with particular recruitment methods.

"Ireland is the only country whose measured mean falls inside the panel's interval" is a valid description of your displayed quantities. It is not evidence that Ireland is uniquely aligned while the other nineteen are statistically misaligned: human uncertainty is excluded, and the intervals describe model resampling.

Where raw human data exist, estimate uncertainty in the reference means using an approach consistent with the sampling information available. Keep that separate from generation variability and sensitivity to panel composition. Sampling intervals will not remove selection bias.

Also, a binding-composite match can conceal offsetting foundation errors. Ireland illustrates this: its English-framed Loyalty, Authority, and Purity scores do not each match the human scores despite the composite agreement.

**5. The measurement-validity argument is too strong.**

The sentence saying the alignment check "licenses comparing these means" needs qualification.

Alignment concerns approximate measurement invariance and estimation of group factor means. Reporting a narrow range of intercept R² values alone does not establish everything needed for your raw-score comparisons. Provide the specification, software, loading diagnostics, item-level noninvariance, and explanation of how the reported summaries were constructed. The methodological distinction matters here. [Alignment methodology](https://doi.org/10.1080/10705511.2014.919210)

Crucially, human cross-country invariance does not establish human–LLM measurement equivalence. You can compare questionnaire response scores without claiming that the scores measure the same underlying psychological traits in humans and models.

The binding composite should also be presented as an explicitly chosen summary index. The Iranian validation itself questions generalizing the traditional higher-order grouping to MFQ-2. That does not prohibit averaging these three foundations, but it weakens treating that average as an established universal construct. [Iranian validation](https://online.ucpress.edu/collabra/article/11/1/140952/212277/The-Revised-Moral-Foundations-in-Iran-Validation)

**6. The convergence result is real descriptively; its explanation remains open.**

The 37-of-39 finding checks out. It is one of the strongest observations in the paper.

However, reduced SD does not by itself establish that models share a more uniform conception of national identity. Many framed binding means approach the upper scale boundary, which mechanically restricts possible variance. Composite averaging can also conceal item-level disagreement.

Check convergence separately by foundation, examine item-level disagreement and endpoint use, and show whether it persists in conditions away from the ceiling. The French conditions make a pure ceiling explanation less plausible, but they do not eliminate the need to examine it.

Replace the sentence about models disagreeing less over "what an Egyptian is" with the narrower result: their binding-composite responses are less dispersed under that prompt.

**7. Several definite reporting errors need correction.**

| Location | Finding |
|---|---|
| B3, four-country ordering | The stated 2-of-11 Arabic and 6-of-11 English counts represent **positive rank correlations**, not correct orderings. My raw-data check found **zero exact order matches in either arm**. |
| B7, failures | The listed model counts sum to **45**, not 46. Reconcile the missing failure with the attempt total. |
| B3, Morocco | The first table uses Arabic local values, while the difference table uses Spanish local values. Thus 4.582 − 4.014 = 0.568, whereas the displayed difference is 0.575. Explicitly label the arm in each table or show both. |
| Main methods, administration | The wording is unclear about message roles. The English runner supplies framing separately as a system prompt; the provider wrapper constructs system/user messages where supported. Describe the actual request structure and provider differences. |
| Main methods, order seeds | The blanket country-keyed description needs the Arabic shared-order exception already documented in B8. |
| Condition accounting | Clarify that the main comparison uses **46 core conditions**, with four additional English baseline variants bringing the total to 50. There are eleven unframed conditions in the full dataset, seven in the core comparison. |

The Iran discussion also needs two source corrections. Its validation reports **minor linguistic edits** to the supplied Persian translation, so identical wording should not be assumed. And its data-availability statement links datasets: investigate their contents before saying respondent-level data are unavailable. [Iran study: methods and data availability](https://online.ucpress.edu/collabra/article/11/1/140952/212277/The-Revised-Moral-Foundations-in-Iran-Validation)

**8. The literature comparison understates prior multilingual work.**

Zewail and colleagues also report a multilingual MFQ-2 short-form replication with human respondents, plus a multilingual replication using another instrument. Your discussion currently leaves the impression that matched-language comparisons are a clearer distinction than they are. [Moral stereotyping in large language models](https://doi.org/10.1073/pnas.2519941123)

Your more defensible contribution is the explicit unframed baseline, within-panel framing comparisons, broader model panel, and convergence analysis. The difference between estimating a typical person and role-playing one is worth describing, but its behavioral importance would need a direct comparison.

**9. Reproducibility needs a complete study manifest.**

Neither document provides a complete, readily identifiable roster of the eleven included models with exact API identifiers, providers, versions where available, and collection settings. That is essential.

Add exact prompts and response labels, instrument provenance, parser validation rules, retry rules, and a dated account of design changes—including what the July collection contributed to subsequent decisions. Distinguish infrastructure failures from malformed responses, since retrying until a parseable result can condition the sample on successful compliance.

Setting temperature in future collections would improve documentation, but identical numerical temperatures would not make stochasticity equivalent across models.

**What I would require before submission**

Correct the definite errors; narrow the headline; rebuild the contrasts around the complete grid; reconcile the uncertainty language; document the roster and decision history; and add human-uncertainty and scale-boundary sensitivity analyses.

A new preregistered study is **not necessary to report this dataset honestly**. A prospective replication would strengthen generalization, but the existing study can support a useful, rigorous conclusion:

> In this selected model panel, country-framing prompts produced larger average shifts in the Loyalty–Authority–Purity composite than unframed questionnaire translation. Framed responses were generally less dispersed across models and frequently differed substantially from published human reference-sample means.

That conclusion is interesting, supported by the checks I performed, and does not ask the data to establish more than they can.
