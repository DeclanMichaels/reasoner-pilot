# Gemini's review of the in-language paper and appendix, 2026-09-08

**Reviewer:** Gemini; its second round on this write-up (the first was 2026-08-23, `1cef617`).
**Reviewed:** the documents after Astra's second round and DeepSeek's were worked through, at or
after `9d0d099`: it quotes B1a's corrected unframed-protocol sentence and `NEUTRAL_SYSTEM = ""`.
**Adjudicated:** 2026-09-08. Three tickets, #31 to #33, all closed the same day.

## Diff against prior rounds

Nothing repeats a settled rejection. Its four primary items are the same four every family has
raised - panel composition, temperature, five runs, the framing prompt's two components - and
three of them are design advice for a future collection, which is spend and a successor's design.

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| 1, B1 | Kimi-K2.6 replaced mid-collection; disaggregate Kimi-K3 | **Misreading, invited by B1's wording.** K2.6 produced no cell, scored or unscored, in any of the fifty conditions; its only scored files are MFQ-30 and PVQ-40 in the convergent-validity module. B1 reworded. The advice to define the panel before collection is decisions 9 and 10's territory and stands as disclosed | #31 |
| 2, B1a | Temperature unlogged; record defaults retrospectively | Downgraded: documentation is undated relative to the collection and defaults change. B1a says they are not reconstructed and why. Pinning is the standing open item | #33 |
| 3 | Five runs; recommends twenty or thirty | Not taken here: new collection. The paper's Limits already carry it | none |
| 4 | Framing confounds country with role-taking; run a country-neutral framing arm | Verified as a limitation and already stated after Astra's second round. The nearest existing measurement, E2 in the English baseline audit (+0.026 [-0.042, +0.090]), is now cited in B1a and the paper, with the caveat that it brackets rather than isolates. The arm itself is new collection | #32 |
| B4 row | Annotate the bootstrap as descriptive | Already done: B4's lead paragraph and every header say model-resampling interval | none |
| B8 row | Harmonise seeding in future | Future collection; B8 states the asymmetry | none |

## Review as received

Here is an evaluation of the draft manuscript and statistical appendix for **"Country framing shifts MFQ-2 responses more than questionnaire language in an eleven-model panel."**

---

### Key Strengths

* **Methodological Rigor & Reproducibility:** The study design is transparent and systematic. Re-evaluating Muthen-Asparouhov alignment on human data, archiving raw responses, using standard-library execution scripts, and enforcing deterministic parsing rules build confidence in the pipeline.

* **Integrity & Disclosure:** The draft openly acknowledges its exploratory nature, late additions, and the lack of preregistration without attempting to frame findings post-hoc.

* **Analytical Nuance:** The distinction made between model capability/behavior and true psychological alignment—specifically noting that LLM scores and human survey scores are not directly equivalent constructs—is methodologically sound.

---

### Primary Areas for Improvement

#### 1. Inconsistent Model Panel & Roster Management

* **The Problem:** The manuscript states an eleven-model panel was analyzed, but `models.json` initially registered fifteen models. Four models (including Google Gemini variants and Cohere Command A) were excluded mid-collection due to rate limits and vendor access policies. Additionally, Moonshot's `kimi` model was replaced mid-collection by `kimi_k3` due to server availability.

* **Impact:** Replacing models mid-study or dropping models due to API rate limits undermines panel consistency.
* **Recommendation:** Explicitly define the panel scope *before* collection begins. For rate-limiting or provider changes, pause collection rather than swapping models, or designate the swapped model run as a separate sensitivity cohort to preserve structural validity.

#### 2. Uncontrolled Temperature & Sampling Parameters

* **The Problem:** The protocol explicitly notes: *"No temperature is sent, so each model ran at its provider's default, which the run records do not capture..."*

* **Impact:** Different provider defaults (e.g., Anthropic vs. OpenAI vs. Together) introduce varied stochasticity. While the text correctly notes that a fixed temperature would not make stochasticity identical, leaving temperature logging unrecorded makes variance comparison between providers noisier than necessary.

* **Recommendation:** Always set and log an explicit temperature (or `top_p`) setting across all API request payloads.

#### 3. Low Run Count Relative to Intra-Model Variance

* **The Problem:** Each cell relies on only five iterations per model ($N = 5$). The authors note that the median within-model spread across five runs is 0.129, compared to a median between-model spread of 0.188.

* **Impact:** Because intra-model variance is relatively high compared to inter-model variance, five runs leave substantial run-to-run noise in the final aggregate model means.

* **Recommendation:** Increase iterations per condition (e.g., $N \ge 20$ or $30$) to effectively dampen repeated-generation noise, especially given the low token count required for JSON ratings.

#### 4. Baseline System Prompt Discrepancies

* **The Problem:** Unframed conditions send an empty system prompt (`NEUTRAL_SYSTEM = ""`). Framed conditions, however, introduce two shifts simultaneously: specifying the country target *and* enforcing role-taking behavior ("You are completing a self-report questionnaire AS a typical... person").

* **Impact:** Confounding role-play instruction with geographic identity makes it difficult to determine whether the observed mean shift stems specifically from the target country identity or generally from adopting an persona.
* **Recommendation:** Include a generic, country-neutral framing baseline (e.g., "You are completing a self-report questionnaire as a typical, ordinary person...") to isolate the specific effect of geographic naming.

---

### Technical & Statistical Revisions

| Section | Issue Identified | Action Required |
| --- | --- | --- |
| **B1. Sample** | Mid-study replacement of `kimi` (K2.6) with `kimi_k3`. | Disaggregate `kimi_k3` from primary panel figures or run a stability check across providers. |
| **B1a. Request** | Default temperature setting unlogged. | Record provider defaults retrospectively where known, or rerun key cells with pinned temperature. |
| **B4. Contrasts** | Percentile bootstrap intervals on 11 models have coarse tails. | Annotate tables clearly to indicate that 11-draw bootstraps serve descriptive rather than inferential bounds. |
| **B8. Presentation** | Multi-country translated runs share presentation seeds within languages, while English runs do not. | Harmonize the seeding strategy across English and non-English scripts in future revisions. |

---

### Concluding Assessment

The draft is exceptionally clear, honest about its exploratory boundaries, and well-executed overall. Resolving the baseline role-play confound, increasing the per-cell run count, and fixing API generation parameters will significantly strengthen the manuscript for formal peer review.
