# Grok's review of the in-language paper and appendix, 2026-09-08

**Reviewer:** Grok, one of the model families Declan runs adversarial review through; its third
round on this write-up (the second was 2026-08-24, `c8e2f0a`).
**Reviewed:** `papers/inlanguage-mfq2-DRAFT.md` and `papers/inlanguage-mfq2-appendix-DRAFT.md` after
the Astra round was worked through: it cites B6a, B1a, the withdrawn family, the relabelled
intervals and the generated failure count, so it read the state at or after `579c343`.
**Adjudicated:** 2026-09-08. This round is an assessment, not a findings list; it is recorded because
it is the first independent read of the post-Astra state.

## Diff against prior rounds

Nothing repeats a settled rejection. Grok's own 2026-08-24 request for an interpretive sentence on
the fifteen-above shape is not repeated; this round says the dispersion finding's account is "left
open", which is the paper's position. Every number it states matches the documents: 1.04 and 0.05,
46 of 2,796, Care 4.29 to 4.89, endpoint use rising 0.234 to 0.267, the seed and the draw count.

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| Interpretive reach | The contrast is "sometimes phrased in ways that invite stronger causal language" | Verified in two sentences: the summary's "makes the models agree with each other" and the section lead "the models agree with each other more". Internal-state phrasing #12 removed elsewhere. Replaced with the observed dispersion | #22 |
| Post-hoc design | Quantities chosen after results | Agrees with the paper's own line, stated once where the reader meets it | none |
| Panel of 11 | Coarse intervals, non-random panel | Stated in the paper; nothing to change without new collection | none |
| Human anchors | Stratified online-panel samples, not censuses; invariance does not license model-human commensurability | Both now stated, B2a and #13 | none |
| Protocol asymmetries | Temperature unlogged; retries condition on parseable JSON; Arabic shared order; comparator changed mid-study | All documented in B1a, B7, B8 and decision 11 | none |
| Next steps (1)-(3) | Larger panel with pinned temperature; direct estimate-versus-answer-as comparison; preregistered contrasts on held-out countries | Not taken here: the pilot is kept as-is and each needs new collection. Temperature is an open item; the other two belong to a successor design | none |

## Not taken

The three next steps, for the reason above. Nothing else was asked.

## Review as received

**Honest review: solid exploratory work with strong transparency and careful reporting, but limited by post-hoc design, panel size, and interpretive caution.**

The two documents form a clear pair: a concise main text and a detailed, script-generated statistical appendix. The core claim is straightforward and data-driven—country framing (system prompt to answer as a typical resident of a named country) produces much larger average shifts on the MFQ-2 binding composite (Loyalty + Authority + Purity) than switching questionnaire language, while also tightening between-model dispersion. The average framing shift is reported as 1.04 points; language effects average ~0.05 signed (larger for Arabic). Against published human reference means the framed panel overshoots for most countries and undershoots for a Western European / New Zealand / Ireland cluster. These patterns are documented thoroughly.

### Strengths in rigor and quality

**Transparency is excellent.** The work is explicitly labeled exploratory, with no preregistration and every quantity chosen after seeing data. Decisions (comparator change, Morocco handling, model replacement, withdrawal of p-value family) are logged with dates and rationales. The appendix is regenerated from scripts (`audit_inlanguage.py`, `build_appendix_tables.py`, etc.) with a fixed seed (20260723), bootstrap 100k iterations, and seeded streams so intervals do not depend on the order of other computations. Sign-flip enumeration is exact (2,048 patterns). Failed calls were retried to success and documented (46 of 2,796); unparsed replies are retained on disk. Presentation-order audit, roster, protocol details (seeds, token ceilings, system-prompt wording, parser logic), and dated design history are all present. AI assistance in methodology is disclosed. This level of documentation is better than many published LLM papers.

**Methodological choices are mostly sensible for the goals.** The model is the independent unit: five iterations averaged first, then panel means and between-model SDs. Intervals are percentile bootstrap over the 11 models and are correctly described as descriptive ranges under resampling of "models like these," not confidence intervals for a broader population. Measurement-invariance checks (loadings/intercepts R² from the human data) are recomputed and reported; the authors correctly note these speak only to the human samples. Contrasts are computed within-model then averaged, with leave-one-out ranges and sign counts. The binding composite is treated as a chosen summary index, not an established construct. Per-foundation tables and dispersion breakdowns (B6, B6a) prevent over-interpretation of the composite alone. Care stays high (4.29–4.89) across every condition; that is a clean, hard-to-miss observation.

**Writing and structure.** The main text is concise, prioritizes the framing-vs-language contrast and the dispersion finding, and keeps the "where the panel lands" results secondary. Tables are readable. The appendix supplies the full grid, every contrast with interval / sign count / LOO range, human anchors with sources and caveats, and the Iran sensitivity. Limits are candid (no prereg, Iran's different study, Morocco language mismatch, small runs per model, one panel / one instrument / one window, provider temperature defaults unlogged).

### Limitations and points of caution

**Post-hoc design and quantity selection.** Everything was chosen after results were visible. Binding became focal early; the final contrast set, weighting scheme for the 1.04 average, and which countries/languages to emphasize were decided with data in hand. The withdrawn p-value family (and the explicit decision to drop them) is good practice, but the remaining narrative still rests on selected contrasts. Readers should treat the specific magnitudes and the "framing >> language" ranking as descriptive of this grid, not as confirmatory tests.

**Panel of 11 is small and non-representative.** Intervals are coarse; LOO ranges are useful but limited. The models are a convenience panel (specific versions from five providers). Claims about "the panel" or "models" are appropriately hedged in places, but the dispersion finding (framed conditions tighter) and the overshoot pattern are still easy to over-generalize. Five iterations per cell is modest relative to between-model spread; averaging reduces but does not eliminate run-to-run noise.

**Human anchors and external validity.** Nineteen anchors come from Atari et al. (2023) Study 2; Iran is from a different convenience sample with noted demographic and possible period biases (the authors correctly show sensitivity). The human samples themselves are online-panel stratified samples, not population censuses; the paper notes education and traditional-community gaps. Measurement invariance is high in the human data, but that does not license treating model scores as commensurate with human scores. The overshoot/undershoot pattern is therefore a pattern of questionnaire responses under specific prompts, not direct evidence of "cultural accuracy."

**Protocol details that affect interpretation.** No temperature was pinned; provider defaults differ and were not logged. Retries condition the scored sample on parseable JSON. Arabic-framed countries share presentation order (deliberate pairing); English-framed countries do not. The unframed English comparator was changed mid-study (old version retained as errata). These are documented, but they introduce small asymmetries.

**Interpretive reach.** The paper mostly stays within the data, but the framing-vs-language contrast is sometimes phrased in ways that invite stronger causal language than an observational grid supports. Dispersion reduction under framing is robust in the tables; whether it reflects "agreement," stereotype collapse, or scale-endpoint effects is left open (endpoint use actually rises slightly). The comparison to Zewail et al. (2026) is fair and usefully distinguishes "estimate the average person" from "answer as one," but the present design does not directly pit the two tasks against each other.

### Overall assessment

Rigor is high for an exploratory LLM study: thorough documentation, reproducible numbers, honest limits, and avoidance of overclaiming statistical significance. Quality of presentation is good—clear main text, exhaustive appendix, careful attention to sources and caveats. The central descriptive results (large framing shifts, small language shifts for most languages, reduced dispersion under framing, systematic overshoots relative to the published human means) are solidly supported by the reported tables.

The main risks are the usual ones for this genre: post-hoc quantity selection, a small non-random panel, and the temptation to read questionnaire-score differences as cultural insight. Treat the numbers as a well-documented map of how these 11 models behave under these exact prompts and instruments. That map is useful; it is not a preregistered test of a general theory of cultural framing in LLMs.

If the authors intend to expand this, the highest-leverage next steps would be (1) a larger, more diverse model panel with pinned temperature and more iterations, (2) a direct task comparison (estimate vs. answer-as), and (3) preregistered contrasts on a held-out set of countries or foundations. As it stands, the draft is already more careful and transparent than most comparable work.
