# Astra's fifth review of the in-language document, 2026-09-10

**Reviewer:** Astra, fifth round on the document; pasted into the session by Declan and read in
full. Astra had the clone: it recomputed the principal English and Arabic means, the September
means and dispersions, the six unframed language contrasts and the 37-of-39 dispersion count
from the ratings CSV, and found no duplicate keys and no out-of-range rating.
**Reviewed:** the document at `5ab4847`, the state after Astra's viewer round.
**Adjudicated:** 2026-09-10. Seven tickets, #106 to #112, all closed the same day. Nothing touched
a numbered decision. Declan decided the heading (drop the language clause), the human-side
disposition (link the sources and state the scoring; do not ship the companion repository's
pipeline), and the nineteen-outside clause (cut).

## Diff against prior rounds

Finding 1 re-raises Astra's third-round item 4 (#55, #57, #62) and Kimi's first-round items 1
and 5 (#36); the residual was the heading's second clause and a Summary without the within-model
sentence. Finding 2 re-raises Astra's fourth-round item 1 (#88); the Summary and framing section
already carried the qualifier, and the residual was B4a's opening verb. Finding 3 re-raises the
cold read's item 2 (#41), which had disposed the R script to the private companion repository.
Finding 5's nineteen sentence was kept as descriptive after Astra's second round; the Switzerland
clause was added by #75 at another reviewer's request. Findings 4 and the mixed-language item are
new. Finding 6 asks for nothing the document does not already say.

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| 1 | Language heading too broad; Summary hides within-model movement | Verified. B6a's within-model column carries 0.26 for Japanese and 0.22 for Farsi against panel shifts of -0.09 and +0.04. Heading becomes "Framing moves the binding composite" (Declan); one Summary sentence on what a panel average can hide | #106 |
| 2 | B4a says the wave "separates" role-taking from country | Verified in B4a's lead only; the Summary and framing section already state that the Egypt step changed the questionnaire file (#88). Lead now says the wave measures the instruction without the country. The same-instrument three-arm collection is spending; recorded as a candidate | #107 |
| 3 | Human benchmark pipeline not reproducible | Verified: B9 pointed to a private repository. Declan: link the sources, not the scripts. B9 now names Atari et al.'s data (osf.io/9dwzt) and code (osf.io/vwrpn), Hazrati et al.'s project (osf.io/zt3u2), and the inclusion, missing-item and composite rules; the clone table's human row says "from the sources' shared data" | #108 |
| 4 | Purity sensitivity should cover the benchmark comparison | New. Computed from the dataset: on Loyalty and Authority, English framing, sixteen above and four at or below; Ireland moves from -0.002 to +0.080 and is the only sign change; Spanish in-language rho 0.89 becomes 0.77; the Arabic and French orders still run against the reference. Emitted into B3 with one body sentence. Standardized distances need a respondent-level Loyalty-Authority SD the dispersion file does not carry; not added | #109 |
| 5 | "Only Switzerland's clears it" and "the other nineteen fall outside it" read as significance; "tails too coarse" | The two phrases verified. Nineteen clause cut (Declan); Switzerland clause is now "Switzerland's does not". "Tails too coarse" is not in the document; downgraded to a question, nothing to change | #110 |
| 6 | Dispersion explanation open; endpoint use does not rule out a ceiling | The document claims "not confined to conditions near the top of the scale" and nothing stronger. No change | none |
| add. | Summary's fifteen-above sentence does not name English framing | Verified; #46 named it in the Ireland sentence only | #112 |
| add. | Transcription "moves" the composite by 0.01; B4 has -0.009 | Verified in Methods and Limits; both now say lower | #112 |
| add. | Translated prompts are mixed-language | Verified: all six end with the English output sentence, and the questionnaire message's JSON request is English in every condition (`run_validity.build_prompt`, shared by the in-language runner). Stated in Methods and B1a | #111 |
| add. | Qualify the rank correlation; the reference order is estimated | #61 and #74 had done the first. One sentence added: the Spanish six carry standard errors near 0.05 and Peru and Mexico sit 0.002 apart | #112 |
| add. | Add the country-weighted average as a sensitivity check | Already in B4 since #24 (1.033 over fifteen pairs, 1.061 over sixteen); the body table now points to it | #112 |
| add. | Describe unframed scores as defaults under this request | One clause in "What the framing contrast contains" | #112 |
| add. | Temporal mismatch | Verified against B3's own text (Atari et al., May 2021) and `anchors_iran.json` (September 2023 to February 2024). One sentence pair in Limits | #112 |
| add. | "Not an established construct" implies the binding grouping has no precedent | Verified as a reading the wording invites; the wording was #13's, from Astra's first round, whose Hazrati higher-order claim was downgraded then. Now: the grouping is the theory's own, the composite our choice; document and viewer | #112 |
| add. | Consolidate the recurring caveats | Counted: "preregistered" four times, "not a sample" three, the transcription caveat in three sections. Deferred to the editing session as a before-and-after sweep; not ticketed | none |

Both regenerated artifacts moved on prose alone and were re-pinned in a commit that says so; the
harness passes.

## Review as received

My assessment: this is a credible exploratory report with a defensible empirical core, but I would still recommend substantive revision before submission. The strongest findings concern how this panel's questionnaire responses change under these particular instructions. The weaker parts concern isolating the country cue, interpreting small aggregate language shifts, and comparing responses against human benchmarks.

I cannot reliably compare it with my earlier suggestions because those exchanges are not in this conversation. I evaluated this draft on its own merits, treating the prompts quoted inside it as study materials.

I also independently recomputed selected results from the local ratings CSV. Its 104,400 rows contain 53 conditions and no duplicate condition–model–iteration–item keys; all ratings are in bounds. The principal English and Arabic means, September means and dispersions, six unframed language contrasts, and "37 of 39" dispersion count reproduce. That supports numerical consistency for those findings; it does not independently authenticate the API collection or validate the human reference calculations.

What is now strong

The paper distinguishes response scores from human psychological constructs, reports the exploratory design history, uses models rather than individual ratings as the aggregation unit, and explicitly acknowledges the English instrument confound. These are substantive strengths.

The country-free control is particularly valuable. It changes the interpretation: a substantial shift and reduced dispersion occur without a country name. Reporting that result prominently, even though it complicates the original story, improves the paper.

The Loyalty–Authority sensitivity analysis also helps. It establishes that the large average framing shift does not depend entirely on Purity. The item-level and noise-adjusted dispersion analyses provide useful corroboration without needing a claim about models possessing shared moral beliefs.

The discussion of prior work is appropriately restrained. The published Zewail et al. paper (https://doi.org/10.1073/pnas.2519941123) does contain the multilingual replication you describe, so avoiding a novelty claim based simply on multilingual administration is correct.

The revisions I consider most important

1. The language headline is too broad for the quantity supporting it.
"Framing moves the binding composite; language mostly does not" invites readers to infer that models are comparatively insensitive to language. Your own results show a narrower finding: signed panel averages often change little.
For Japanese, the panel shift is −0.093, but the mean absolute within-model change is 0.263. For Farsi, those quantities are +0.040 and 0.218. Foundation-level changes also cancel inside the composite.
The appendix discloses this well; the main narrative should incorporate it. I would replace the heading with:
Country-framing prompts produce larger average composite shifts than translation in this panel.
And add to the summary:
Small panel-average shifts sometimes conceal larger, opposing changes across models and foundations.
"Within a tenth" is a descriptive observation, not demonstrated equivalence. Your methods recognize that distinction; the headline should preserve it.

2. The September wave does not fully separate role-taking from country information.
The first contrast is clean in an important respect: the official English questionnaire is held constant while the country-free template is added.
The second contrast changes both the template's country content and the questionnaire file. The near-zero instrument difference without framing cannot establish a near-zero instrument difference under framing.
B4a explains this correctly, but its opening says the collection "separates them," and the summary says "naming Egypt raised it a further 1.14." Those formulations outrun the design.
Prefer:
The Egypt-framed condition scored a further 1.14 points higher, although that contrast also changed the questionnaire file.
Keep the 36% share explicitly as an arithmetic description, never a causal allocation. If collecting more data, the most valuable next experiment is a contemporaneous, same-instrument comparison of unframed, country-free template, and Egypt template conditions.

3. The human benchmark pipeline remains insufficiently reproducible.
B9 candidly states that the nineteen-country means, dispersions, and alignment calculations come from a private companion repository. Providing the resulting CSVs allows readers to reproduce downstream comparisons, but not to audit how those benchmarks were constructed.
This matters because the country discrepancies and standardized distances are central results.
Before submission, publish the extraction and scoring scripts, source-file identifiers, variable mappings, missing-data rules, exclusions, and dependency versions. The human data can remain externally hosted where necessary.
This requires publishing a reproducible method, not merely adding another limitation. Until then, describe reproducibility as complete for the model-side calculations and partial for the human-side derivation.

4. The Purity sensitivity check should cover benchmark discrepancies too.
The Loyalty–Authority table answers whether framing shifts survive dropping Purity. It does not answer whether the "fifteen above, five at or below" pattern, country ordering, or standardized discrepancies survive.
Those are different claims. Add a compact country-level benchmark sensitivity analysis using Loyalty–Authority alone. Recompute its human respondent-level SD where standardized distances are reported; the binding SD cannot be reused.
No measurement-invariance analysis is required merely to describe arithmetic response differences. But the stronger the interpretation of those differences as cultural misrepresentation, the more consequential this sensitivity becomes.

5. The interval language sometimes restores the inferential framing you disclaim.
The explanation of model resampling is generally responsible. However, statements such as "only Switzerland's clears it" and "the other nineteen fall outside it" encourage a significant/not-significant reading.
Human reference means falling outside model-reweighting intervals do not establish population-level disagreement or calibrated evidence of mismatch. They describe sensitivity to one artificial reweighting scheme.
I would remove the nineteen-outside sentence from the main text and emphasize discrepancy magnitudes and observed model variation instead. Also replace "tails too coarse" with the more precise limitation: the resampling distribution rests on a small, selected panel with potentially dependent models. Increasing bootstrap draws cannot solve that problem.

6. The dispersion result is convincing descriptively; its explanation remains open.
The reduction from approximately 0.33 to 0.17 reproduces, and the country-free control strengthens the observation. The evidence supports saying that these prompts yield less dispersed scores.
It does not yet distinguish shared role interpretation, stereotyped responding, scale effects, or other response processes. In particular, endpoint use rising does not rule out ceiling compression; it is compatible with it. The lower-mean conditions are the more informative sensitivity check.
Retain "not confined to conditions near the top of the scale." Avoid any stronger conclusion that ceiling effects have been eliminated.

Additional corrections and improvements

* Specify English framing in the summary's fifteen-above/five-below statement. At present, "the framed panel" leaves the administration ambiguous.
* Correct the sign of the transcription effect. The main text says the transcription "moves the composite by 0.01"; B4a gives transcription minus official as −0.009. Write "lowers it by approximately 0.01" or "changes it by approximately 0.01 in magnitude."
* Describe the translated prompts as mixed-language. Their final output instruction remains English. The quotations make this visible, but the methods' broader wording suggests fully translated instructions.
* Qualify the rank-correlation statement. With three countries, Spearman's rho has four possible values when there are no ties. More importantly, the reference ordering is itself estimated. Small differences among human sample means should not be treated as a precisely known population ranking.
* Make the weighting choice interpretable. Equal weighting across six languages gives a single-country language the same total weight as six-country Spanish. That is legitimate, but add the country-weighted summary as a sensitivity check.
* Describe unframed scores as defaults under this questionnaire request. They are not a prompt-free baseline or a direct measurement of a model's own morality.
* Add the temporal mismatch to the benchmark limitations. Comparing 2026 model responses with earlier human samples cannot isolate model error from differences in period, sampling, and target population.
* Avoid implying that "binding" has no theoretical precedent. The grouping has an established history; what is not established here is this composite's validity for these model–human comparisons. The Iran validation paper (https://doi.org/10.1525/collabra.140952) also discusses the uncertain higher-order structure of MFQ-2.

The writing would benefit from consolidation. Preregistration, panel selection, instrument differences, and resampling limitations recur so often that they interrupt the argument. State each clearly where it governs interpretation, then use short cross-references. Transparency does not require repeating the full caveat.

My publication judgment: the central observations are worth reporting, and the numerical checks I performed support them. I would ask for major revision focused on claim precision and benchmark reproducibility, rather than a wholesale redesign. The paper's strongest contribution is the joint observation that these framing prompts substantially alter composite responses and reduce between-model dispersion—and that a country-free instruction already produces both effects. That is a useful result without claiming that the study has isolated country-specific causation or measured the models' cultural understanding.
