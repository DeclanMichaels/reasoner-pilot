# Astra's review of the MFQ-2 viewer, 2026-09-10

**Reviewer:** Astra, its fifth round on this write-up and its first on the viewer. The first attempt
on 2026-09-09 exhausted Declan's usage window without returning; this is the completed review,
returned the next day. The full text was on this machine at
`~/Documents/Codex/2026-09-10/tw/outputs/viewer-review.md`, 80 lines, read in full.
**Reviewed:** `validity/viewer.html` served locally with its payload, and
`papers/inlanguage-mfq2-DRAFT.md`, at `9fc022e`. Astra recomputed from the ratings CSV every
grid condition's composite and foundation means, the per-model composites, the 36 foundation
shifts, the dispersion medians (0.331 unframed, 0.171 framed, 37 of 39) and three bootstrap
intervals, all matching the payload within its four-decimal rounding.
**Adjudicated:** 2026-09-10. Six tickets, #99 to #104, all closed the same day. Nothing touched a
numbered decision; #99 implements decision 18 in a place the viewer had missed.

## Diff against prior rounds

Finding 1 is new. Finding 2 is new for the viewer; the document has carried the three
qualifications since the paper rounds. Finding 3 is the residue of #95, which cut the header's
mixed-arm average and kept the fifteen-five split without settling its arm; Grok's viewer round
flagged the mixed rule and called it consistent, and that adjudication passed it. Finding 4's
three-country half is #74, done; the rest is new. Finding 5 is new. In finding 6 the zeros item
is Grok's, declined the day before and now filed with two reviewers behind it; the other five are
new.

## Verification

Every finding was checked against the viewer source, the payload and the document before
assessment.

- `condAnchor` keyed on the country alone, so `ar_framed_Morocco` in the Models tab drew the
  4.014 marker. The Overshoot tab's own note says those cells enter no comparison.
- The document's What we did section carries the index-we-chose sentence, the Purity intercept
  caution and the same-thing disclaimer; none was in the viewer. The matrix note said "report
  more binding morality".
- The document's fifteen-five table is labelled English framing, which every country received;
  the story used the translated arm where one existed. Fifteen countries have a translated arm.
- "Not a difference this design resolves" had no interval behind it. A six-country Spearman takes
  36 values. "Bounds nothing" is `CONTEXT.md`'s definition of the model-resampling interval.
- The two composite contrasts the document leads with, translation minus English unframed and
  in-language framed minus unframed, appeared nowhere in the viewer together.
- Footer: no links. The "Every cell" tab filtered to anchored countries. Zeros printed for absent
  token counts. "Bracketed figures" described a table whose cells printed points; the brackets
  were on the chart marks' tooltips. The administration sentence attributed Iran's to Atari et al.
  The Control tab said "separates them".

## Adjudication

| # | finding | disposition | ticket |
|---|---|---|---|
| 1 | The Models tab draws Morocco's human marker on the Arabic-framed arm | Verified. The English arm is anchored for every country; a translated arm only when it is the language the sample answered in. A note says why the marker is withheld | #99, `4649a42` |
| 2 | The viewer omits the document's three measurement qualifications; "more binding morality" | Verified. A note under the first chart carries the three sentences; the matrix note says what a positive cell is. Declan: the Loyalty-and-Authority table stays in the document, pointed to | #100, `d819748` |
| 3 | The headline story summarises the translated arm where the document's table is English | Verified. The story is now the English-framed arm, names it, gives the translated count, and points at the chart for the other arm. The chart keeps both marks | #101, `59bb943` |
| 4 | "Resolves", "a handful of values", "establishes nothing either way", "bounds nothing" | Verified on the first three; cut. Declan: "bounds nothing" is the glossary's definition and stays; the footer already says the interval is not a population confidence interval | #102, `47dfcd2` |
| 5 | No direct language-versus-framing display | Verified. Declan: add it as one table. The builder emits `language_contrasts`, per language the unframed panel, translation minus English, and framed minus unframed averaged over its countries with Morocco under Spanish, each with a seeded model-resampling interval and a sign count, plus the equal-weight framing average. The Foundations tab opens with it. Its twelve figures match the document's two tables; the pinned payload moved by the new block only | #103, `407eac1`, `e85e112` |
| 6 | Six labels: links, tab name, zeros, intervals, Iran, Control wording | Verified on all six. Footer links to the document and the dataset at the 44 px target rule; "Every framed cell"; "not reported" in the cells; the interval printed under each table mean; "by Atari et al. except for Iran"; "estimates the two increments" | #104, `a11b3ed` |

## Not taken

The human foundation profiles' sample-size weighting, below 0.0004 by Astra's own check. The
proposed "is not a population confidence interval" as a replacement for "bounds nothing", for the
reason in row 4.

## Left over

The changed tabs were screenshotted at 375 pixels after the fixes: no horizontal body scroll, wide
tables scrolling in their own containers, the story, the note, the intervals and the "not
reported" cells all legible. The pass caught one thing in the round's own work, footer links that
broke onto their own lines; they are now plain inline links with a padded hit box. The Every shift
table on the Foundations tab prints its intervals at 14 px, below the 15 px floor; it predates this
round and is a candidate ticket, not fixed here.

## Review as received

# MFQ-2 viewer review

Reviewed 10 September 2026: http://localhost:8017/viewer.html and the accompanying inlanguage-mfq2-DRAFT.md.

**Verdict:** The viewer's core arithmetic is supported by the published ratings dataset. It is a useful exploratory display, but needs corrections before it is a scientifically faithful standalone companion to the paper. The strongest problems concern a prohibited reference comparison, omitted validity limitations, and ambiguous interpretation—not a wholesale numerical failure.

This was a read-only review. No project files or study data were changed.

## Findings, in priority order

### 1. Models displays the Morocco comparison that the paper excludes

**Confirmed behavior:** Open Models and choose “Arabic, framed as Morocco.” The plot displays “reference sample 4.01” alongside a panel mean of 4.582. The first tab and paper explicitly say the Arabic Morocco arm does not enter comparisons against the human mean, because the human administration was in Spanish.

**Cause:** `validity/viewer.html`, function `condAnchor()`, lines 811–816, extracts only the country from the condition key. It returns Morocco's anchor regardless of administration language.

**Fix:** Suppress the human marker for the excluded Arabic Morocco arm, and state why. Define permitted reference comparisons centrally so every tab applies the same rule. Retain the English comparisons that the study deliberately reports. This is an actual inconsistency with the stated analysis policy, not a claim that all cross-language comparisons are inherently forbidden.

### 2. The viewer drops the paper's central measurement-validity limits

The paper explicitly describes binding as an author-selected summary index, cautions about Purity's cross-group intercept noninvariance, and disclaims equivalence between human and model scores as measures of the same underlying thing. Those cautions are absent from the viewer. The Every cell tab instead says positive differences mean models report “more binding morality.” That invites a stronger interpretation than the paper supports.

**Fix:** Put a short qualification beside the first chart: these are questionnaire response-score differences; the composite is an author-selected index; cross-country Purity comparisons carry the paper's measurement caveat; human–model measurement equivalence has not been established. Replace “more binding morality” with “higher mean ratings on Loyalty, Authority and Purity.” Add the paper's Loyalty–Authority sensitivity result or link directly to it.

This finding is about fidelity to the supplied paper. I did not independently reproduce the source studies' measurement-invariance analysis.

### 3. The headline does not identify which comparison it summarizes

The paper's 15-above/5-at-or-below result uses English framing for every country. The viewer's `boot()` function instead chooses the translated arm where present and English otherwise. The first chart and its gap column use that same mixed rule. Both yield 15/5 in the current data; the count is not false. They nevertheless summarize different quantities.

Examples: Iran is +1.244 in English versus +0.981 in Farsi; Japan is +1.016 versus +0.782. The table explains its fallback below the numbers, but the headline does not. The introduction also suggests all countries were administered in their country's language, although eight have no translated arm and Morocco is intentionally grouped under Spanish.

**Fix:** Label the headline explicitly as English-framed, matching the paper, or explicitly describe the mixed rule. Label gap columns and ordering views with the selected arm. Replace “that country's language” with “the administered translation, where available.”

### 4. Some statistical prose overstates what was computed

Ordering says the French ranges are within 7%, “which is not a difference this design resolves.” The generator computes point ranges but supplies no uncertainty analysis for their difference. That is not enough to determine what the design resolves. The same tab says six-country Spearman correlation takes only “a handful” of values; enumeration gives 36 possible values without ties.

The foundations tab says a resampling interval crossing zero “establishes nothing either way.” This is too categorical: the observed estimate remains informative, and these intervals are defined as descriptive sensitivity to model reweighting, not a binary evidential test.

**Fix:** Report the observed French ranges and say uncertainty in their difference was not quantified. For Spanish, say the ranking covers only six selected countries. Describe zero-crossing literally: the central resampling range includes both positive and negative shifts. Replace “bounds nothing” with “is not a population confidence interval.”

### 5. The paper's main language-versus-framing result is unnecessarily hard to inspect

The paper leads with the small average unframed translation shift and the much larger framing shift. The viewer leads with human-reference gaps. Its unframed scores can be recovered from lines, tables, and the Models selector, but there is no direct display of the six translation-minus-English contrasts beside the six framing contrasts.

**Fix:** Add a compact comparison table or chart with language, unframed translation shift, framing shift, and country count. Show the equal-language weighting explicitly. Include the Arabic exception and the paper's caution that small panel averages can hide individual-model movement. This would make the viewer answer the paper's central question directly.

### 6. Standalone provenance and interface labels need tightening

- The interface repeatedly refers to the appendix but supplies no ordinary reader-facing links to the paper, ratings dataset, methods, or source studies; the footer names internal paths. Add usable links.
- “Every cell” displays anchored framed comparisons, not all 50 conditions or all scored runs. Rename it “Framed gaps” or similar.
- Models represents absent reasoning-token reporting as numeric zero and 0%, with the qualification below the table. Display “not reported” in the cells themselves where that is what the value means.
- The first table promises bracketed intervals, but its visible cells contain point estimates; intervals are in tooltips. Label that interaction or show intervals explicitly.
- The first tab says every country's human administration was Atari et al.'s before the next paragraph excepts Iran. Say “except Iran” in the first sentence.
- The Control tab's “separates them” wording should say it estimates two increments. It correctly discloses the questionnaire-file change later, but that change prevents a clean country-only decomposition.

## What passed

All six tabs rendered and their navigation worked in the local browser. The Models condition selector changed its plot. The inspected desktop layout has a clear hierarchy and consistent visual styling. Detailed data tables, common unframed reference lines, explicit equal-model weighting, and the dedicated September control are useful design choices.

Independent standard-library recomputation from `validity/results/mfq2_ratings.csv` found:

- 104,400 rows, representing 2,900 runs across 53 conditions: the 2,750-run August grid plus the 150-run September wave.
- Each run contained 36 distinct item IDs and integer ratings from 1 through 5.
- All 50 grid-condition binding means, their per-model binding means, and all six foundation means agreed with `validity/results/viewer_data.json` within 0.000051, allowing for its four-decimal rounding.
- All 36 language-by-foundation framing shifts agreed to the same precision.
- Between-model SD medians independently reproduced as 0.331436 unframed and 0.170650 framed, with 37 of 39 framed conditions below every unframed condition.
- Three representative 100,000-draw bootstrap intervals reproduced exactly at stored precision: English unframed [2.6081, 2.9333], Arabic unframed [2.8434, 3.3737], and English-framed Ireland [2.9556, 3.2525]. This was a spot check, not regeneration of every interval.
- Both the all-English and mixed-language headline rules produced 15 countries above their supplied human anchors.

I also checked a potential weighting issue in the foundation profiles: human means are sample-size weighted while model country means are equally weighted. The difference from equal-country human weighting is below 0.0004 for these data, so it is not a material current-result defect.

## Limits of this review

These checks establish internal consistency from the committed integer ratings to the viewer data and selected rendered values. They do not establish authenticity of the original provider responses, correctness of every translation or item mapping, or independent validity of the human reference statistics. I did not audit archived raw responses, rebuild human references from respondent-level source files, run the whole reproduction harness, or perform a full mobile/accessibility audit.

A targeted attempt to retrieve the original Atari paper from its laboratory-hosted PDF failed. Accordingly, the source study's detailed psychometric claims remain attributed to the supplied draft here, not independently certified. The full human-data reconstruction also depends on code that the draft says lives in a private companion repository.

**Recommended release threshold:** Correct the Morocco anchor, restore the measurement qualifications, identify each comparison arm explicitly, and remove unsupported inferential wording. The checked arithmetic gives a sound basis for those repairs; it does not remove the study's exploratory and measurement limitations.
