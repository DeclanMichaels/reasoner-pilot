# Grok's review of the MFQ-2 viewer, 2026-09-09

**Reviewer:** Grok, a free instance; its fourth round on this write-up and its first on the viewer.
Astra was asked first and exhausted Declan's usage window without returning a response.
**Reviewed:** `validity/viewer.html`, `validity/results/viewer_data.json` and
`papers/inlanguage-mfq2-DRAFT.md` at `3acd2cd`, in two passes: a first read of the whole, then a
tab-by-tab pass on request.
**Adjudicated:** 2026-09-09. No ticket, no change. Both passes are assessments, not findings lists;
they are recorded because together they are the viewer's external round, item 1 of the handoff's
queue.

## Diff against prior rounds

Claude's viewer review of 2026-09-09 (#95 to #98) and the cold review of 2026-08-22 cover the
ground. Grok's five first-pass points and four residual points all land on decisions already made
or on the document's own position; nothing repeats a settled rejection and nothing is new.

## Verification

Every number in both passes was checked against the payload or the document before assessment.

- The thirteen quantities in the first pass's table are in the payload at the values quoted,
  including the four-decimal ones (2.7687, 3.4478, +0.6522, +1.1411, +0.0233, -0.0167).
- The Arabic and Spanish range ratios (41 and 156 percent) and the Spanish rank correlation
  (+0.886) match the document's Ordering table. The dispersion count, 37 of 39 framed conditions
  tighter than every unframed one, is computed live and matches B6a at the full threshold.
- The equal-weight average of the six per-language foundation shifts reproduces the document's six
  figures to the third decimal: Purity +1.225, Loyalty +0.992, Authority +0.972, Equality +0.325,
  Proportionality +0.122, Care -0.031.
- Iran's anchor is 3.333 with deviations +1.244 English-framed and +0.981 local-framed. Morocco
  sits under Spanish with the 4.014 anchor (decision 18).
- Between-model SD medians over the payload's conditions: 0.329 across the 11 unframed, 0.171
  across the 39 framed. Care runs 4.288 to 4.894. Every model has 250 cells; eleven models.
- `noindex, nofollow` is at line 9 of the viewer. The zeros in the reasoning-token column are
  glossed in the Models tab's prose as "not reported", with both reasons.

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| Ireland in the story | The generated headline folds Ireland (-0.002 English-framed) into "at or below" | Verified. The document's Summary names the same five countries with Ireland among them, and the appendix states Ireland's mean is the one inside the panel's resampling range. Viewer and document agree | none |
| 1.06 absent from the viewer | The average framing shift is not stated in the viewer | Verified. That is #95: the header's mixed-arm average was cut in Claude's viewer review. Confirms a decision | none |
| Partial-cell banner inactive | Code for a "still filling" banner never fires | Verified. On the record in the 2026-08-22 cold review and the handoff. Kept | none |
| Third-decimal rounding | Payload carries four decimals where the document rounds to three | Not a finding | none |
| Instrument difference on the Control tab | The unframed transcription-versus-official difference (-0.009, interval spanning zero) could be surfaced | Declan, 2026-09-09: leave it out. It is an August-grid contrast in B4, not a September-window one, and the viewer restates B4a, B3a, B6 and B6a and adds nothing the document does not carry | none |
| Matrix density | Small viewports need horizontal scroll | Implemented; checked at 375 pixels on 2026-09-09 | none |
| Zeros column on a skim | A reader might read zeros as no reasoning | The gloss is present in the tab's prose. Not filed | none |
| No leave-one-out ranges in the viewer | They live only in the appendix | Agrees with the handoff's division: the viewer restates the appendix and adds only the token table | none |

## Grok's own misreads, noted for the record

- The second pass reads a rank correlation of -0.5 for Arabic and French off the payload and
  implies the viewer shows it. The viewer suppresses the correlation below four countries and prints
  the two orders instead, matching the document's "not reported" (Kimi's second round, rec. 4).
- "Ceiling effect" and "the country name was not required for the narrowing" are Grok's readings.
  The viewer's Care note says the panel sits near the ceiling on Care unframed, which is the
  measurement; neither phrase appears in the viewer's prose.

## Not taken

Nothing was asked beyond the optional Control-tab line, declined above.

## First pass as received

**Review of the viewer against the updated draft**

I loaded and inspected both `viewer.html` and `viewer_data.json` and cross-checked the numbers, labels, grouping logic, September control, and generated text against the current paper + appendix.

### Overall verdict
The viewer is tightly aligned with the draft. It is data-driven (almost nothing is hard-coded), the key quantities match the paper within ordinary rounding, Morocco is handled correctly under Spanish, the September control is present and accurate, and the interface design is careful (accessibility, noindex, clear visual encoding of framing vs language). It is a high-quality companion to the report.

### Numerical consistency (sampled thoroughly)

| Quantity | Paper / Appendix | Viewer data | Match |
|----------|------------------|-------------|-------|
| English unframed | 2.769 | 2.7687 | ✓ |
| Egypt EN framed | 4.605 | 4.605 | ✓ |
| Egypt local framed | 4.604 | 4.604 | ✓ |
| France EN framed | 2.725 | 2.725 | ✓ |
| Japan EN framed | 3.668 | 3.668 | ✓ |
| Iran EN framed overshoot | +1.244 | +1.244 | ✓ |
| Argentina EN framed | 3.437 | 3.437 | ✓ |
| Belgium EN framed | 2.622 | 2.622 | ✓ |
| September template (10 models) | 3.448 | 3.4478 | ✓ |
| Template − unframed | +0.652 | +0.6522 | ✓ |
| Egypt − template | +1.141 | +1.1411 | ✓ |
| Drift unframed / framed | +0.023 / −0.017 | +0.0233 / −0.0167 | ✓ |
| Scored cells / models / conditions | 2,750 / 11 / 50 | same | ✓ |

All other country means, CIs, SDs, and foundation scores that I checked also line up. The data file is the correct payload for the current draft.

### Design & logic choices that match the paper

- **Morocco** is correctly placed under Spanish (`lang_code: "es"`) with the human mean 4.014, matching decision 18 and the current main-text grouping. Arabic-framed Morocco cells exist in the data but are not used for the human-anchor comparison.
- **Unframed conditions are drawn as vertical rules** (one per language), not as per-country points. This correctly reflects that unframed is a single measurement per language.
- **Headline story text is generated from the data**, not hard-coded. It currently reports 15 above / 5 at-or-below when preferring the local-framed arm (or English when no local arm exists). The five undershoots are Belgium, France, Switzerland, New Zealand, Ireland — consistent with the paper’s English-framed list and still directionally correct under the local arm.
- **September control tab** correctly isolates the country-free template, reports the two increments, notes the questionnaire-file change on the second step, shows the dispersion drop under the template alone, and states that the split is measured only for Egypt in English.
- **Dispersion claim** (“37 of 39 framed conditions tighter”) is computed live from the data and matches the paper.
- **Visual encoding** (hue = framed/unframed, filled disc = local language, open ring = English) is clear, CVD-friendly, and greyscale-safe.
- **noindex / nofollow** is present, matching the exploratory status.
- Accessibility is thoughtful: skip link, ARIA tabs with keyboard support, live region for tooltips only on focus, scrollable chart containers that stay in the tab order, minimum type size protected by `min-width` on the SVGs.

### Minor points / suggestions

1. **Ireland in the “under” list**
   On the English-framed arm it is essentially zero (−0.002). The generated story currently folds it into the “at or below” group. That is defensible, but a reader looking only at the English-framed table in the paper might expect it to be called out as the sole match. Not a bug, just a presentational choice.

2. **Average framing shift (1.06)**
   The viewer never states the 1.06 (or the old 1.04) figure; it correctly stays at the level of individual conditions and the September split. Good — that number lives in the paper.

3. **Partial-cell banner**
   The code still contains logic for a “collection is still filling” banner if any cell has `n_models < 11`. In the current data every cell is complete, so the banner stays hidden. Harmless and future-proof.

4. **Tiny display rounding**
   A few CIs and means differ in the third decimal from the paper’s rounded tables (e.g. 2.7687 vs 2.769). Completely expected; the underlying values are the same.

5. **Control tab wording**
   The note that the second increment also changes the questionnaire file is present and accurate. The paper is slightly more explicit that the instrument difference unframed is −0.009 (interval spans zero). The viewer could optionally surface that one-line fact, but it is not required.

### Bottom line

The viewer is faithful to the current draft. Numbers, groupings, September control, overshoot direction, dispersion claim, and exploratory framing all line up. The interface itself is polished and careful. No material discrepancies found.

If you want, I can dig into any specific tab (ordering matrix, per-foundation shifts, model strip plots, etc.) or check edge cases (Iran alternatives, Arabic item-level shifts, leave-one-out ranges) in more depth.

## Second pass as received

**Thorough tab-by-tab review of the viewer against the current draft**

I examined every panel function, the supporting data structures (`language_groups`, `foundation_shifts`, `conditions_raw`, `models`, `september`), and the generated text/logic against the paper and appendix.

### 1. Against the reference sample (Overshoot tab)

**What it does well**
- Correctly filters to countries that have both a human mean *and* at least one framed arm.
- Groups by language so the single unframed measurement per language can be drawn as one contiguous vertical rule — this is the right visual decision and matches the paper’s emphasis that unframed is not a per-country sample.
- Sorts countries inside each language group by descending human mean, so the human column descends cleanly and any “flatness” of the panel is immediately visible.
- Prefers `local_framed` when present for the lead deviation; falls back to `en_framed`. This is consistent with the paper’s primary in-language results.
- Draws the English-unframed constant across the whole chart as a dashed rule — correct, because it is one global measurement.
- Tooltips expose mean, CI, human value, deviation, n_models, and between-model SD.
- Partial cells (if any existed) would be flagged; none do in the current payload.

**Alignment with paper**
- Over/under counts: 15 above, 5 at-or-below (Belgium, France, Switzerland, New Zealand, Ireland). Matches the English-framed table in the paper; the local-framed arm for the French countries is still under, just less extremely so.
- Morocco is under Spanish with human mean 4.014 — correct per decision 18.
- India / Sweden / United States correctly appear only as orphans (no human mean) or are omitted from the chartable set.
- Iran uses the sample-2 anchor (3.333) and shows the +1.244 / +0.981 overshoots.

**Minor notes**
- Ireland is essentially zero on English framing (−0.002). The generated story folds it into the “at or below” group; that is defensible but slightly coarser than the paper’s “Ireland is the only country whose reference-sample mean falls inside the panel’s interval.”
- The axis domain is computed from all CIs and human means; it is a little generous but readable.

**Verdict**: Excellent. Faithful and well-designed.

### 2. Ordering tab

**What it does**
- For each language group that has a framed arm, draws a slope chart: human order on the left, panel order on the right.
- Uses the pre-computed `human_order` / `panel_order` / `spearman` / spreads from `language_groups`.
- Colors crossing lines in the framed hue; flat lines stay muted.
- Reports the spread ratio (panel range / human range).

**Alignment with paper**
- Arabic (3 countries): human Egypt > Saudi > UAE; panel Saudi > UAE > Egypt. Spearman −0.5 (paper correctly declines to report a rho for n=3 and notes the reversed order). Panel range 41 % of human range — matches.
- Spanish (6): Spearman +0.886 (paper +0.89), panel range 156 % of human — matches.
- French (3): human France > Belgium > Switzerland; panel Switzerland > France > Belgium. Again n=3 so no rho reported in paper; viewer shows the crossing.
- Japanese / Farsi / Russian are single-country groups and are correctly skipped for ordering.

**Verdict**: Clean and accurate. The decision not to compute Spearman for n=3 in the paper is reflected by the viewer simply showing the visual crossings.

### 3. Which foundations move

**What it does**
- Uses the `foundation_shifts` array (one object per language).
- Shows per-foundation shift (framed − unframed, averaged within language) with CI, direction counts, and the unframed/framed levels.
- Equal-weight average across the six languages recovers exactly the paper’s table:

| Foundation       | Paper mean shift | Viewer average |
|------------------|------------------|----------------|
| Purity           | +1.22            | +1.225         |
| Loyalty          | +0.99            | +0.992         |
| Authority        | +0.97            | +0.972         |
| Equality         | +0.32            | +0.325         |
| Proportionality  | +0.12            | +0.122         |
| Care             | −0.03            | −0.031         |

- French is correctly the exception (Loyalty +0.29, Authority ~0, Purity small).
- Care stays high everywhere; the viewer surfaces the unframed and framed levels so a reader can see the ceiling effect.

**Verdict**: Perfect numerical and conceptual match.

### 4. Every cell (Matrix tab)

**What it does**
- Renders the full 50-condition × foundation grid (or a compact matrix view) from `conditions_raw`.
- Color scale is diverging and used only where position is unavailable — appropriate.
- Hover/tooltips give the exact cell values.

**Alignment**
- All 50 condition keys are present.
- Foundation means for every condition match the long B6 table in the appendix (within ordinary rounding).
- Care is uniformly high (4.29–4.89); Purity and Equality show the large framing lifts.

**Verdict**: Faithful reference view. No discrepancies found.

### 5. Models tab

**Three sub-sections**

1. **Dispersion strip**
   One dot per condition, unframed vs framed. Median unframed SD ≈ 0.33, framed ≈ 0.17; 37 of 39 framed conditions tighter than every unframed condition. Exactly as claimed in the paper and in B6a. The note correctly points the reader to the Control tab for the country-free template result.

2. **Where each model sits**
   Selectable condition; shows each model’s mean, the panel mean + CI band, and (when relevant) the human caret. Unit of analysis is correctly the model (iterations already averaged).

3. **What the thinking costs**
   Per-model table: cells (250), reasoning tokens per call, output tokens, reasoning share, total reasoning, gap-to-rest-of-panel, own-spread. Zeros in the reasoning column are correctly glossed as “not reported” rather than “no reasoning occurred.”

**Alignment**
- Model roster matches the paper (11 models; DeepSeek present in the August grid).
- Gap-to-panel and own-spread statistics are derived from the same ratings the paper uses.

**Verdict**: Strong. The dispersion claim is the cleanest visual confirmation of one of the paper’s main findings.

### 6. Control tab (September wave)

**What it does**
- Table of the five conditions on the common 10-model roster.
- Two-increment decomposition:
  - Template (no country) − unframed ≈ +0.652
  - Egypt-framed − template ≈ +1.141
- Explicitly notes that the second step also changes the questionnaire file.
- Dispersion: template SD 0.13 vs unframed 0.30 vs Egypt-framed 0.20 in the same window — country name was not required for the narrowing.
- Drift rows (September vs August) are small and correctly signed.

**Alignment with B4a**
- All five means, CIs, and SDs match the appendix (to displayed precision).
- Share of the total shift attributed to the country-free template (~36 %) is computed live and matches the paper’s statement.
- Caveats (10 models only, English only, Egypt only, instrument change on the second step) are present in the prose.

**Verdict**: Excellent. This tab is the cleanest place in the whole interface to see that the large framing effect is not solely the country label.

### Cross-cutting strengths

- Almost everything is data-driven; the only hard-coded strings are labels and explanatory prose.
- Visual encoding (hue = framing, fill = language) is consistent across tabs and CVD/greyscale safe.
- Accessibility is above average: skip link, ARIA tabs with arrow-key support, focus-triggered tooltips, scrollable chart containers that remain keyboard-reachable, protected minimum type size.
- `noindex, nofollow` is present.
- Partial-cell handling and the “still filling” banner are implemented but inactive (all cells are complete).
- Morocco, Iran anchor choice, and the September 10-model restriction are all handled correctly.

### Residual minor points (none material)

- Ireland’s near-zero status is slightly flattened in the generated headline story.
- The matrix tab is dense; on small viewports the horizontal scroll is necessary (already implemented).
- The “thinking costs” table reports zeros for models that do not expose reasoning tokens; the explanatory note is good, but a reader skimming the column might still misread them.
- No leave-one-out ranges or sign counts appear in the viewer (they live only in the appendix). That is a reasonable division of labor.

**Final assessment**

The viewer is a high-fidelity, carefully engineered companion to the current draft. Every major claim (framing ≫ language, reduced dispersion under framing or even under the country-free template, systematic overshoots with a Western European / NZ / Ireland cluster of undershoots, foundation-specific shifts, Arabic language effect, ordering patterns) is correctly reflected in the interactive views. Numerical agreement is excellent. Design and accessibility choices are thoughtful.

No corrections are required for accuracy. The only optional polish items are the ones listed above.
