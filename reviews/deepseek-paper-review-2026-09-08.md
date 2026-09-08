# DeepSeek's review of the in-language paper and appendix, 2026-09-08

**Reviewer:** DeepSeek; its third round on this write-up (rounds one and two were 2026-08-23,
`03bd7c0` and `2c2cded`).
**Reviewed:** the documents after the first Astra round, at or after `579c343`.
**Adjudicated:** 2026-09-08. Concrete claims verified by recomputation; two refuted; one question
answered from the data and emitted (#28); one sentence added (#29). The rest is assessment.

## Diff against prior rounds

Rounds one and two rejected, from this reviewer, mechanism for the Care ceiling, hypothesising an
individualistic baseline, novelty framing, hedging, and the push toward conventional academic
register; and the settled practice records that this reviewer's factual claims are verified before
anything is acted on. This round repeats the register push in new forms - a letter grade,
"hypothesis-generating", "preregister the next study", a "what we would do differently" section -
and the Care-ceiling mechanism question. Per the practice, that is a finding about the reviewer.

One thing it raised produced a rule: its reading of "an earlier draft said" as a reference to a
published document led to decision 17.

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| 7 (minor) | "The local framing effect is actually negative for France and Belgium" | **Refuted.** France +0.020, Belgium +0.058. Confused where the framed panel lands against the reference sample with the framing contrast | none |
| technical | The +1 shift assumes the 0-to-4 anchor labels match the 1-to-5 labels | Verified that they match, word for word; one sentence added | #29 |
| 2 | Uncontrolled temperature is a fatal confound for the dispersion finding | Downgraded to a question and answered from the data: temperature is fixed per model across conditions; the within-model run spread falls under framing, 0.185 to 0.114, so run noise contributes less to the framed between-model spread. Emitted in B6a | #28 |
| 8 | The 1.04 weighting should be justified or both reported | Both were already in B4; the paper now states the weighting | #24 |
| 1 | "The panel" invites reading as a sample | Not taken: the panel is a defined term, and the paper states in three places that it is not a sample. The opening now says "one of these eleven models" | #24 |
| 4, 5, 9, 10 | Morocco and the French-speaking share; Iran's anchor uncertainty; the role of the alignment check; engaging Zewail | All already stated in the documents after the first Astra round | none |
| 6 | The Care ceiling: model artifact, translation issue, or scale? | Mechanism; barred by the scope rule and rejected from this reviewer in round two | none |
| minor | "Binding composite is not a standard MFQ-2 summary" | Not verified: Atari et al. and Hazrati et al. both use the individualizing-binding grouping. The paper presents it as a chosen index regardless | none |
| minor | Denmark; sign-count definition; leave-one-out interpretation | Denmark has no MFQ-2 reference and no translation; B4 defines the sign count and the range in its lead paragraph | none |
| recommendations 1-8 | Re-frame, replicate with fixed temperature, preregister, justify weighting, integrate Care, engage Zewail, clarify invariance, add a forward section | 4, 6 and 7 were done in the Astra rounds; 2 and 3 need new collection and belong to a successor; 1, 5 and 8 are the register push | none |

## Review as received

# Review: In-Language MFQ-2 Study

## Overview

This is a study examining how language models respond to the Moral Foundations Questionnaire-2 (MFQ-2) under different framing conditions (country-specific vs. neutral) and languages (English vs. translations). The authors have been remarkably transparent about their methodology, limitations, and the exploratory nature of the work. This transparency is a genuine strength, but it also reveals significant methodological issues that limit what can be concluded.

---

## Strengths

### Exemplary Transparency

The level of disclosure here is exceptional and should be commended. The authors:

- Provide complete code paths (`validity/audit_inlanguage.py`, `validity/build_appendix_tables.py`, etc.)
- Report a fixed random seed (20260723) with bootstrap iterations (100,000)
- Document every design decision with timestamps from the commit log
- Record every condition's exact system prompt, not just a template
- Keep all raw replies (including failed parses) on disk
- Explicitly state what was not preregistered and what decisions were made post-hoc
- Provide Iran anchor sensitivity analyses showing the choice of sample affects magnitude but not sign
- Document the exact number of failed calls (46/2,796) by model

The statement that "methodology was AI-assisted and that assistance is disclosed" is appropriate given the scale of documentation.

### Careful Unit of Analysis

Averaging each model's five iterations before computing panel means is correct: it prevents models with higher variance from dominating. The model as the unit of analysis (n=11) is the right choice given the research question about model-level behavior.

### Appropriate Use of Intervals

Bootstrap intervals are described as "descriptive" and explicitly not as confidence intervals for models in general. The statement that intervals "show how far the panel figure moves when models like these are resampled" is honest about what resampling 11 values can and cannot tell you.

### Well-Documented Errata

The decision to withdraw the earlier sign-flip test family (decision 15) and maintain the quantities without p-values shows intellectual honesty. The note that "intervals were read as bounds" and "exchangeability among the eleven models has not been shown" directly addresses a common overclaim in this literature.

### Useful Negative Results

The "What the panel is not doing" section is valuable: Care never comes down across any condition, framed responses are less dispersed, and two countries a point apart in human data come out the same in the panel. These are genuinely interesting empirical patterns that don't overstate their meaning.

---

## Serious Concerns

### 1. **The Panel Is Not a Sample**

This is stated explicitly, but the framing of the results repeatedly invites the reader to treat it as one. Phrases like "the panel lands," "the panel spreads," and "across the panel" are descriptive, but the summary's opening line ("Tell a language model...") and the presentation of "the panel's" behavior as a coherent entity obscure that we're looking at 11 models chosen by convenience.

The paper should adopt consistently: "These 11 models, under these conditions, produced..." rather than generalizing to "language models" or "the panel."

### 2. **Non-Constant Temperature Is a Confound**

This is a serious methodological issue that the authors acknowledge but don't adequately address. They note:

> "We do not send a temperature, so each model answered at its provider's default, and the run records do not capture what that default was... Some part of the difference between one model's spread and another's may be a sampling temperature we never set and did not log."

This means the between-model spread is partly a function of arbitrary API defaults (which vary by provider) rather than model behavior. The observation that "framed responses were less dispersed across models" could be an artifact of how different providers handle system prompts vs. user messages under their default temperatures.

**Suggestion:** This should be treated as a fatal limitation of the specific data, and the paper should say so. Any conclusion about between-model dispersion should carry a caveat that temperature was uncontrolled and may account for part or all of the effect.

### 3. **The Design Grew From a Validation Exercise**

The paper says this upfront, but the implications are severe:

- The research question changed mid-stream (from "validating an instrument" to "comparing language and framing")
- The design was not specified in advance
- The focal quantity (binding composite) was chosen on 2026-07-20, "before any in-language cell existed" according to the appendix, but after the July 2026 collection was complete
- Countries were added as the study expanded, not sampled systematically

The statement that "no threshold was fixed before the data existed" means every reported effect is a post-hoc observation. This is not inherently invalid for exploratory work, but it should be presented as hypothesis-generating rather than hypothesis-testing.

### 4. **Morocco's Human Data Is in Spanish, Arabic Arm Was Run Anyway**

Morocco's human sample was collected in Spanish, but the paper runs it in both Arabic and Spanish. The Arabic and Spanish arms produce nearly identical model outputs (4.582 vs. 4.589), so the mismatch doesn't move Morocco's result. However, this is one of several cases where the "same language as the human norms were collected in" claim requires caveats:

- Morocco: human data in Spanish, Arabic arm run
- Belgium: 36% French-speaking, but human data administered in French
- Switzerland: 23% French-speaking, but human data administered in French

The paper notes these, but the main text's claim that "for fifteen of the twenty countries... our in-language condition uses the same language the human norms were collected in" is slightly misleading—it's true by the authors' decision rule, but the rule itself doesn't align with actual national linguistic demographics.

### 5. **Iran's Anchor Problem**

Iran's anchor comes from a different study (Hazrati et al., 2025) with different collection conditions, administered on a 0-4 scale, with a sample that "is younger, more educated and majority female relative to the country." The authors are transparent about this and show sensitivity analyses.

However, Iran is one of only two non-WEIRD countries where the panel overshoots by more than a full point (the other is Japan), and the overshoot magnitude is partially (up to 0.102) dependent on which sample is used. The fact that the sign and ranking don't depend on the choice is reassuring, but the paper should be more explicit that the "human" benchmark for Iran is substantially less certain than for the other 19 countries.

### 6. **Care Ceiling Effect**

Care ranges from 4.29 to 4.89 across all conditions, with the human reference for Japan at 3.03. This is a striking pattern, and the paper notes it. But the interpretation is unclear:

- Is this a model artifact (models rate Care uniformly high regardless of framing)?
- Is this a translation issue (Care items may be less culturally variant)?
- Does it indicate the MFQ-2's Care scale doesn't discriminate in this panel?

The paper doesn't explore this, and the Care results are basically separated from the binding composite results. If Care is invariant across conditions, the binding composite (which includes Care for the individualizing foundations? Actually binding composite excludes Care—it's Loyalty, Authority, Purity. The Care result is important for the "what the panel is not doing" section, but it's not integrated.)

### 7. **Statement Order Sharing**

The four Arabic-framed countries share the same statement order for a given model and iteration, while English-framed countries do not. The appendix notes this asymmetry "costs the English four-country contrast some precision and introduces no bias, since order is randomized."

This is a correct statement, but it's a bit glib. Sharing order within the Arabic arm means those countries' between-country contrasts are paired on presentation order, which actually *improves* precision for that comparison. The asymmetry means the Arabic and English within-language comparisons are not on the same statistical footing. The paper could quantify how much precision is lost.

### 8. **Interpreting the 1.04 Framing Effect**

The summary claims "the instruction shifts the panel by 1.04 scale points on average." This is computed as the local framing effect averaged within each language over its countries, with Morocco counted under Arabic and not Spanish, and then averaged across the six languages with equal weight.

The weighting is unusual. Weighting every (language, country) pair equally gives 1.011; including Spanish Morocco gives 1.061. The choice of weighting affects the headline number by about 5%, which isn't huge, but the method should be justified. Why equal weight to languages rather than countries? This choice makes Arabic's four countries count as one language's contribution, while Farsi's one country counts as one language's contribution.

This is a legitimate analytic choice, but it should be motivated. If the goal is to generalize across languages, equal weight to languages makes sense. If the goal is to generalize across countries, equal weight to countries makes more sense. The paper doesn't state which interpretation is intended.

### 9. **R-squared Alignment Check**

The measurement invariance check (B2a) shows loadings and intercepts R-squared > 0.99 for all foundations. This is reassuring for comparing human means across countries. However, the paper uses this check to justify comparing model outputs to human means, but the check is a property of the human samples, not of the model outputs. The statement "It says nothing about whether a model's score and a person's score measure the same thing, and nothing here claims they do" is correct, but then what is the purpose of including the check in a paper about comparing models to humans? It seems to be a gesture toward methodological rigor that doesn't actually address the relevant question.

Either the comparison between models and humans requires measurement invariance (in which case this check is insufficient because it doesn't test model-human invariance) or it doesn't (in which case the check is irrelevant). The paper should clarify this.

### 10. **The Zewail et al. (2026) Comparison**

The paper says "Whether estimating a person and answering as one differ in what they produce is a direct comparison neither study has run." This is accurate but underplays the fact that Zewail et al. (2026) had a similar design (MFQ-2, language translations, cross-national comparison) and found comparable distortions. The current study's contribution (framing vs. language, dispersion finding, baseline) is substantive, but the paper should engage more directly with how its results compare to Zewail et al.'s.

---

## Specific Technical Issues

### Statistical Tests

The paper correctly reports no p-values (decision 15). The bootstrap intervals are described as "descriptive" and "not a confidence interval." This is appropriate, but it means the paper cannot make any formal statistical claims. The result is a set of descriptive observations about 11 models, not a test of any hypothesis.

### Iran Scale Shift

> "Iran's sample was administered on a 0-4 scale and shifted linearly by +1 for comparability"

This is a linear shift of the mean, but it assumes the 0-4 scale's anchor labels correspond exactly to the 1-5 scale's anchor labels. If the scale interpretation differs (e.g., if "0" meant something different than "1" does on the other scale), the shift could be wrong. The paper should show the per-item mapping and justify the shift.

### Iran Standard Deviation

The appendix notes: "Iran's standard deviation is computed from the respondent-level data the authors share... an earlier draft said the data did not exist, and that was wrong." This correction is appreciated, but the fact that the data exist and were accessible should have been caught earlier.

### Sample Size (Human)

The human samples range from 205 to 207 respondents per country (3,902 total). The authors stratified on age, gender, and political orientation but not education. The paper notes this limitation, but it's worth emphasizing: the human "benchmarks" are not representative of the country populations in any rigorous sense; they're Qualtrics panel samples that are "educated enough to complete the surveys online."

---

## Minor Issues

### "Typical" Person Framing

The prompt asks the model to answer as a "typical, ordinary person" from each country. This is a specific task (describing a prototype) that may differ from asking the model to estimate the average person's responses (Zewail et al.). The paper notes this, but the phrase "typical person" appears in the summary as if it's a neutral description. The task is actually quite specific and may influence results.

### In-Language Framing Instructions

The framing instructions were "our translations... AI-assisted and disclosed as such." This is appropriately disclosed, but the quality of the translations is not independently verified. The paper asserts that "the Arabic template still reproduces the Egypt prompt byte for byte as first collected," but that only checks consistency, not accuracy.

### "Binding Composite" Chosen Post-Hoc

The focal quantity was chosen on 2026-07-20, "before any in-language cell existed" according to the appendix. This predates the in-language collection, so it's not a p-hacking issue. But the choice was made after the July 2026 English-only collection, and the paper acknowledges that "every quantity was chosen after the data were seen." The binding composite is not a standard MFQ-2 summary, and the decision to focus on it should be justified substantively, not just historically.

### "Models (of 11)" Column in B4

The contrast tables show "models (of 11): 11 up, 0 down" or similar. This is a useful descriptive statistic, but the paper doesn't explain how ties are handled or what "up" and "down" mean. It should define this in the text.

### "Leave-one-out range" Column in B4

This is a useful robustness check, but the paper doesn't explain how to interpret it or why it's included. It should be introduced in B4's text.

### Denmark and Other Missing Countries

The paper only includes countries that have published MFQ-2 data (plus Iran). This is the right constraint, but it means the country set is not balanced by language or region. The absence of a Danish arm, for example, is noted in the appendix's discussion of in-language instruments, but the paper doesn't explain why some languages have one country and others have four.

### France and Belgium

France and Belgium are both below their reference means in the English-framed condition, and the local framing effect is actually negative for France and Belgium (the panel is *lower* when told to answer as French or Belgian than when unframed). This is a genuinely interesting exception to the overall pattern, but the paper doesn't explore it.

---

## Recommendations

1. **Re-frame as an exploratory, descriptive study.** The current framing ("this is exploratory") is honest but the paper sometimes slips into causal language ("framing shifts," "the instruction moves"). It should consistently say "Under these conditions, the 11 models produced..." rather than generalizing.

2. **Conduct a follow-up with fixed temperature.** The uncontrolled temperature is a serious confound for the between-model dispersion finding. A replication with a documented, consistent temperature setting would strengthen the paper considerably.

3. **Preregister the next study.** The authors are honest about the exploratory nature of this work. The next iteration should be preregistered, with the design, analysis, and reporting threshold specified in advance.

4. **Justify the weighting for the 1.04 effect.** Explain why equal weight to languages rather than countries is appropriate for the headline claim. Or report both weightings.

5. **Integrate the Care result.** The Care ceiling effect is important but separated from the main narrative. It deserves more discussion.

6. **Engage more with Zewail et al. (2026).** The current paper makes a substantive contribution (within-panel contrasts, baseline, dispersion), but it should articulate more clearly how its findings relate to and extend the prior work.

7. **Clarify the measurement invariance check's role.** Either show that model-human measurement invariance is relevant to the comparison or state clearly why the human-human invariance check doesn't address the model comparison.

8. **Add a "What we would do differently" section.** The authors are already transparent about limitations. A forward-looking section would strengthen the paper by showing how the next iteration would address the identified issues.

---

## Verdict

**This is a well-documented, transparent, exploratory study with serious limitations that are mostly disclosed.** The uncontrolled temperature, the lack of preregistration, the post-hoc choice of focal quantity, the Iran anchor uncertainty, and the non-random sample of models all mean the paper should be read as descriptive rather than inferential.

The paper's strength is its transparency: every decision is documented, every limitation is stated, and the code and data are reproducible. The observed patterns (framing > language, Care ceiling, dispersion reduction, country ordering mismatches) are genuinely interesting and worth reporting as observations to be investigated further. The paper should not be cited as evidence for general claims about language models, but it is valuable as a case study of how 11 specific models behaved under these specific conditions.

**Grade: B+.** The methodology is flawed but the transparency is exemplary. With revisions that position the work more carefully as exploratory and replicate the key finding with controlled temperature, this could be a strong contribution to the literature on language models and moral psychology.
