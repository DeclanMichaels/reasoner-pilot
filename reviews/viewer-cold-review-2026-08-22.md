# Cold review: in-language MFQ-2 viewer

Reviewed 2026-08-22 against `reasoner-pilot/validity/viewer.html` and
`results/viewer_data.json` (both byte-identical to the deployed copies at
`moral-os-website/experiments/`), with numbers checked against
`results/inlanguage_grid_audit.txt`, `results/inlanguage_audit.txt`,
`reasoner-study/instruments/MFQ-PVQ/mfq/reference/mfq2_country_means.csv` and
`validity/anchors_iran.json`. Rendered in Chromium at 1440, 1280, 1024, 640 and
390 CSS px and at 200 percent zoom, and screenshots read rather than the CSS.

**External-facing: independent adversarial review done? This is the first pass;
no independent review has run on the viewer.**

## What holds

Every binding-composite figure on the page reconciles exactly with the audit
output: the 45 condition means, the six unframed in-language values, the four
per-country arms, the deviations, the spread ratios (Arabic 47 percent, Spanish
234 percent) and the rank correlations. Nothing is transcribed; the headline
sentence and the French-exception clause are computed from the data at load.

Contrast passes everywhere, including the diverging ramp. The worst step on the
matrix is the hot pole at 5.25:1 against `#eaeaf0`, and the cold pole is 5.43:1,
so the pole cap in Encoding Rule 6 is doing exactly what it was written to do
and no cell needs an ink switch. Chart ink, dim text, warning colour, banner and
link all clear 4.5:1.

The main chart applies Rule 3 and Rule 5 correctly: the population mean is a
white caret in primary ink, and each unframed condition is one rule rather than
nineteen repeated dots.

## Blocking, before this goes to reviewers

**1. Iran's human anchor contradicts a settled decision, and it carries the
largest overshoot in the study.**

`3_settled.json`, `mfq2_human_means_source`: the human means are Atari 2023
Study 2 only, and independent MFQ-2 validation means are not pooled in, with
Iran named in the prohibition. The viewer anchors Iran to Hazrati et al. 2025
sample 2 at 3.333.

That cell is not a marginal one. Iran's deviation is +0.981 in Farsi and +1.244
in English, the largest in the grid, larger than Japan. Iran is the only Farsi
country, so it carries the whole Farsi row in the main chart, the whole Farsi
foundation profile, the Farsi group in every by-language reading, and one of the
two charts on the page that has a human reference at all.

`anchors_iran.json` states the problems itself: convenience Telegram and
snowball samples, 68 to 71 percent female, mean age 26 to 28, and the file's own
words, "likely less binding-endorsing than the general Iranian population". That
biases the overshoot upward, in the direction of the finding. It also records a
0-4 administration with a +1 linear shift applied, and collection beginning a
year after Woman, Life, Freedom with possible period effects.

The audit already computed the sensitivity (C5): the overshoot moves from +1.244
to +1.346 on sample 1 and +1.273 on the n-weighted pool. None of that reaches
the page. The footer says "except Iran (Hazrati et al. 2025, sample 2)" in dim
15px text at the very bottom, which reads as a citation, not as a caveat.

This is your call, not mine, and there are three coherent versions: drop Iran
from the anchored set and report its panel values uncharted alongside India,
Sweden and the United States; keep it and mark it in the chart, the table and a
banner the way partial cells were marked; or keep it and change the settled
decision deliberately, in `3_settled.json`, with the reason. What is not
survivable is the current state, where a reviewer who reads the settled file and
the anchors file finds the objection and the answer to it already written down
and neither on the page.

**2. "Care does not move up anywhere" is contradicted by the chart directly
above it.**

Foundations tab, closing note. Care shifts: Arabic +0.127, Spanish +0.095, Farsi
+0.036, French +0.020, Russian -0.170, Japanese -0.324. It moves up in four of
six languages, and the chart draws those four marks to the right of zero where
the reader can see them. What is true is that no upward Care shift clears
p <= .05. The sentence needs the word that makes it true.

**3. The same note generalizes across languages in the way French breaks.**

"Framing lifts the three binding foundations by roughly a full scale point."
French loyalty is +0.295, French authority is -0.011, French purity is +0.093.
This is failure pattern 30 in a different shape, and the handoff's own rule for
the composite ("do not write that models overshoot when framed without the
French exception in the same sentence") applies to the foundations too.

**4. The page tells a reviewer the collection is still filling. It is not.**

No cell in the data has fewer than 11 models; the partial-cell banner never
fires. But two notes state it unconditionally as present tense: the legend on
tab 1 ("fewer than 11 models have landed in that cell") and the matrix note ("a
cell marked * has fewer than 11 models in it - the collection is still
filling"). A reader is told to discount marks that do not exist, and told the
study is unfinished when it is complete. The conditional machinery is right;
these two strings are outside it.

**5. `viewer_data.json` does not reproduce from the current build script.**

Re-running `build_viewer_data.py` against the same runs produces a file that
differs from the committed one: Japanese proportionality `down` = 5 rebuilt
against 4 committed (with `up` = 6 and 11 models, the committed pair sums to 10).
The committed stamp is 11:33:45 and `build_viewer_data.py` was last modified at
16:33, so the deployed data predates the script that is supposed to produce it.

`up` and `down` are not read by the viewer, so nothing displayed is wrong. That
is luck, not verification, and it is exactly the provenance link failure pattern
24 exists for. Rebuild, rediff, redeploy before review, and the diff should then
be the timestamp alone.

## The two you flagged

**6. "The answer is no, but not by much" answers a question the page never
asks.**

The heading is "Which foundations move" and the lede asks nothing, so "no" has
no antecedent. Reading forward, the intended question is whether the composite
is picking up a general lift in every answer, and the intended answer is no. But
"no, but not by much" then works against itself: the qualifier is trying to
carry the fact that the non-binding foundations move somewhat, and the reader
cannot tell which claim is being hedged.

The fix is to put the question in the chart's own lede, which Encoding Rule 1
asks for anyway, and then answer it flatly. Something on the order of: the
composite averages three of six foundations, so the question is whether framing
lifted everything or only those three. Then the note states the answer without
the "but".

**7. Four of the six foundation profiles have no human reference, and the page
does not say why.**

"Where that leaves the panel" draws the white caret only when the language group
has exactly one country and that country has per-foundation human values. In
practice that is Japan and Iran. Arabic, Spanish, French and Russian show no
reference at all, and the strongest chart on the page, Arabic with purity at
+1.85, is one of them.

There are two different reasons collapsed into one silence. Arabic, Spanish and
French have multiple countries, so there is no single profile to draw, which is
a real constraint and worth one sentence. Russia is a single country and has no
per-foundation values in the reference set at all, which is a data gap and a
different sentence. The lede's "Where a published human profile exists for the
country, the white caret is the population" is technically true and leaves the
reader to work out which case they are looking at.

Worth noting what falls out of this: the only two charts on the page that carry
a per-foundation human reference are Japan and Iran, and Iran's is the anchor in
finding 1.

## Encoding, against your own rules

**8. The matrix does the thing tab 1 was built to avoid, and lets it set the
colour scale.** Rule 5 says a constant is drawn once. The English-unframed
condition is one number, 2.769, and the in-language-unframed conditions are one
per language; tab 1 correctly draws them as rules. The matrix draws them as 32
separately coloured cells, one per country, which is a claim about sample size
made by layout.

It also costs the reader the actual comparison. The colour cap is the largest
absolute deviation, 1.498, and that value comes from Egypt's unframed cell,
which is just a restatement of how far Egypt's human mean sits from 2.769. The
framed columns, which are the real content, run -0.885 to +1.244 and get
squashed toward the neutral midpoint. Egypt's +0.338 and Argentina's +0.154 read
as nearly the same colour.

Dropping the two unframed columns, or capping on the framed columns only, gives
the framed cells the full ramp.

**9. Solid versus hollow means three different things in three charts on one
page.** Rule 9 says if two charts in a viewer disagree about what solid-versus-
hollow means, both are wrong. Here: tab 1, hollow ring = English and solid disc =
in-language; foundations chart A, filled = clears p <= .05 and hollow = does not;
foundations chart B, hollow ring = unframed and solid disc = framed. A reader who
learns the legend on tab 1 is then wrong twice.

Chart B is the cheapest to fix, since hue already carries framing there and fill
is redundant. Chart A needs a different channel for significance.

**10. `--human` ink carries three meanings.** It is the population reference in
tab 1, chart B and the models strip; it is the zero line in foundations chart A;
and it is "this country did not change rank" in the ordering slopegraph, which is
why Peru's line is white. Rule 3 reserves that ink for a measured reference. The
zero line and the unmoved-rank line both want dim ink.

**11. The models strip draws every condition in the framed hue.** The dots are
`var(--framed)` unconditionally, so selecting "English, unframed" or "Arabic,
unframed" gives orange marks for an unframed condition. Hue is meant to be
framing across the whole viewer.

## Statistics a reviewer will go at

**12. Thirty-six uncorrected p-values on the foundations tab, in a viewer whose
audit Holm-corrects.** Six foundations times six languages, each reported against
p <= .05 with filled-versus-hollow marks, and nothing on the page mentions
multiplicity. The grid audit reports Holm(10) and Holm(22) columns for its own
family. The inconsistency is more exposed than the raw p-values would be on
their own.

Related: many cells print p = 0.001, which is the floor of an exact sign-flip
test on 11 models (2/2048 = 0.00098), not a measured value. Worth rendering as
"p <= .001".

**13. Rank correlations carry no uncertainty, on three, four and five
countries.** Arabic rho = 0.00 on four countries is the sharpest single result in
the study and appears in bold in the header as "no relationship at all". On four
items, rho = 0 is the single most likely value under the null and a 95 percent
interval spans most of the scale. The caveat that exists ("with only n countries
a rank correlation can only take a few values") fires at `n < 4`, so only French
gets it. It should fire for every group here.

Two related points. French's spread ratio of 107 percent is reported as "the
panel exaggerates the differences", which is a 7 percent difference described as
a finding. And Spanish's human order separates Peru at 3.514 from Mexico at
3.512, which both display as 3.51; the human means have standard errors in the
reference file that appear nowhere on the page.

**14. "More thinking is not obviously buying a different answer"** is the scope
rule's prohibited form. Under `report_scope_what_we_did_what_models_did` the
reportable version is the association as observed: models that spent more
reasoning tokens per call did not land closer to or further from the rest of the
panel. The current phrasing reads as a negative causal finding, and the table
invites a correlation the page never computes, on seven models that report.

## Accessibility, measured

Rendered and measured rather than read off the CSS.

The SVG text is declared at `font-size="15"` inside a 980-unit viewBox, so its
on-screen size is 15 times the container scale, not 15px:

| Viewport | Chart width | Effective label size | Horizontal scroll |
|---|---|---|---|
| 1440 | 1082 | 16.6px | no |
| 1280 | 1082 | 16.6px | no |
| 1024 | 926 | 14.2px | no |
| 640 (= 1280 at 200%) | 560 | 8.6px | yes, 830 vs 640 |
| 390 | 310 | 4.7px | yes, 830 vs 390 |

Two rules break. The 15px floor fails at 1024, which is an ordinary laptop
width, and collapses at 200 percent zoom. And "the page must work without
zooming or horizontal scrolling at ordinary laptop widths and at 200 percent
zoom" fails at 200 percent, where the seven-column tables force the document to
830px against a 640px viewport.

The fix for the type is to scale the declared size by the inverse of the
container scale, or set SVG text in a size that lands at or above 15px at the
narrowest supported width. The fix for the tables is a wrapping element with
`overflow-x: auto`, so the table scrolls inside its own box and the page body
does not.

ARIA gaps, all small and all in the tab machinery:

- Tab buttons have no `id`, so the panels cannot and do not carry
  `aria-labelledby`; panels have no `tabindex`.
- Arrow keys do not move between tabs. Verified: ArrowRight on the tablist
  leaves the selection where it was. The ARIA tabs pattern expects it.
- The tooltip is `role="status" aria-live="polite"` and its content is rewritten
  on every `mousemove`, so a screen reader announces continuously while the
  pointer crosses the chart. It wants to be silent on hover and announced on
  focus.
- Focused marks have no Escape to dismiss the tooltip.

## Smaller things

**15. Four raw pipeline keys leak into the Models dropdown.** The comment above
`condName` says nobody should have to read `ar_framed_Egypt`, and then
`en_baseline_official_selfreport`, `en_baseline_ours_nosystem`,
`en_baseline_ours_selfreport` and `en_neutral_ours` appear verbatim in the
list. These are the English-baseline confound arms, not study conditions;
either label them as the audit arms they are or filter them out.

**16. The models strip has a label collision.** With "Arabic, framed as Egypt"
selected, "people 4.27" sits on top of the axis tick "4.25", and the caret line
runs through sonnet's value label "4.24". The caret label is drawn at the same
height as the tick labels whenever the human mean is near a tick.

**17. Two different nineteens.** The provenance chip says "19 countries" (ours),
and the not-charted note says "the MFQ-2 nineteen-nation set" (Atari's, which is
a different nineteen: it has Ireland, Kenya, New Zealand and South Africa, and
not India, Sweden, the United States or Iran). The note is true, and I checked
it against the reference CSV, but the collision makes a reader think three of
our own nineteen are missing their own means.

**18. Japanese, Farsi and Russian vanish from the Ordering tab** without a line
saying a single-country group has no order to correlate. A reader arriving from
a six-language chart notices three are gone.

**19. The "Mean" column on the shift table** averages six language groups of one
to five countries with equal weight, and the header says only "Mean". Care's
mean of -0.04 is a group of one, Japan at -0.32, outweighing four positive
groups. Say what is being averaged.

**20. Undefined columns.** "Cells" (225 = 45 conditions times 5 iterations) and
"Reasoning share" are never defined, while the two columns beside them are
defined carefully in the note.

**21. The matrix has no language column,** so the French block that the headline
depends on is scattered through a table sorted by human mean. Adding the column,
or grouping by language as tab 1 does, puts the three blue rows together.

## Suggested order

Findings 1 through 5 before anyone else sees it. Finding 1 needs a decision from
you; the other four are edits. Then 6 through 11, which are the ones a
design-literate reviewer will find and which are all your own rules. Then the
statistics group, which is what a methods reviewer will find. The accessibility
type fix is mechanical and worth doing in the same pass since it touches every
chart.
