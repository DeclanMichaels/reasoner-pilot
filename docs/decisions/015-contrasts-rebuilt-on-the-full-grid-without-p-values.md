# 015 - The contrast set is rebuilt on the full grid, and p-values leave the appendix

**Date:** 2026-09-08
**Status:** active

## The decision

Appendix B4's declared family T1 to T10 and its Family B are replaced by one contrast set built on
the completed grid. For every country with both languages it reports four contrasts and their
interaction: framing in English, framing in the local language, language without framing, language
with framing, all computed within models before aggregation. Each contrast reports the difference,
its 95 percent model-resampling interval, the per-model sign count and the leave-one-out range.

No p-values and no Holm correction appear in the appendix. The exact sign-flip enumeration stays in
`audit_inlanguage.py`'s stdout as a verification trail. Every interval is labelled as model
resampling, never as a confidence interval or a bound.

The current B4 is kept as errata, the way decision 11 kept the old English comparator, with the
date and the reason.

## Why

Three findings from Astra's review of 2026-09-08, each verified against the text.

Family B claimed one comparison per language and tested three of six. French, Spanish and Russian
had no unframed-versus-English test. Family A mixed language contrasts, anchor comparisons and one
framing contrast, which is the shape of an analysis written on the first collection and carried
across the expansion.

B4 read percentile bootstrap intervals as bounds: "any Egypt language effect is within 0.054". A
resample of eleven values does not bound an effect. The appendix's own definition of the interval,
as sensitivity to panel composition, already said what it is; the sentences contradicted it.

The sign-flip test's null needs the eleven models to be exchangeable and their paired differences
symmetric about zero. Eleven models from nine labs, three on one host and some sharing lineage,
have not been shown to satisfy that, and naming the model as the unit does not supply it. The
interval leans on the same exchangeability but claims only what the appendix states: how far a
panel figure moves when these eleven are resampled. The p-value claimed a calibrated error rate
under a null the design cannot justify, so it was the less accurate of the two. Dropping it also
removes the Holm tax that a thirty-contrast family would otherwise impose, which matters because
that tax would have been paid in the currency of the unjustified null.

The declared family was itself post hoc, written after the first collection. Rebuilding does not
lower the study's status, which is exploratory throughout (decision 2), but it does reopen a family
that round two of review deliberately kept intact to avoid re-cutting after seeing results. It is
reopened now for a coverage finding, not for the results, and this entry is the record of that.

## Rejected alternatives

**Keep the declared family and disclose its coverage.** Rejected: three of six languages stays
three of six, and the disclosure would describe a gap rather than close it.

**Rebuild the contrast set and keep Holm-corrected p-values.** Rejected: with eleven models the
smallest attainable exact p is 2/2048, and Holm over about thirty contrasts lifts the floor to
about 0.03, so results at p = 0.002 would land near 0.06. The labels that survive or fall would be
statements about a null we cannot justify.

## Consequences and gotchas

B4 and B5 regenerate through `audit_inlanguage.py`'s markdown emitter; the viewer's test readouts
and the paper's Family B sentences follow. "Arabic is the only language whose interval excludes
zero" was true over three languages and is re-derived over six.

Every quantity this produces was chosen after the data were seen. That is true of everything in
this write-up and is stated where the reader meets it; the register rule is that it is stated once,
plainly, and not narrated as a virtue.

Issue #18 carries the work.
