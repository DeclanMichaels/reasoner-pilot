# Society-framed MFQ-2: do the models de-compress, and do they stereotype?

An extension of the model-panel work: MFQ-2 re-administered under a **country framing** — the
system prompt asks the model to answer "as a typical person living in [country]" — for six
countries chosen to span the cross-cultural range: United States, Sweden, Japan, India, Egypt,
Nigeria. Same 11-model panel, 5 iterations = 330 calls. **Complete: all 11 models, 330/330 cells
(the ~20 rate-limited / parse-failed cells were recovered on a resume pass).**

**Confound to state up front:** the models have almost certainly seen the MFQ items *and* the
published cross-cultural norms in training, so a country-framed profile that matches the real
national mean may reflect memorized lookup rather than genuine cultural simulation. Read these
results as **steerability / behavioral repertoire**, not cultural understanding. (This is itself
an argument for the Reasoner's bespoke scenarios, which carry far less item/norm-memorization
baggage than a famous published questionnaire.)

## Result 1 — the models de-compress, hard

MFQ-2 binding composite (loyalty + authority + purity, 1–5), panel mean by condition:

| Condition | Binding | Between-model SD |
|---|--:|--:|
| Sweden | 2.23 | 0.22 |
| **Neutral (default)** | **2.71** | 0.34 |
| United States | 3.34 | 0.20 |
| Japan | 3.67 | 0.29 |
| India | 4.43 | 0.17 |
| Nigeria | 4.56 | 0.17 |
| Egypt | 4.61 | 0.15 |

Each model spans ~1.7→4.9 across countries. Within-model across-country binding SD averages
**0.86**, versus the neutral between-model SD of **0.34** — framing fans each model out ~2.5× wider
than its resting cluster. The neutral compression dissolves under framing, replicating the
Reasoner's core neutral-vs-framed effect on a fully independent instrument.

The country ordering — Egypt ≈ Nigeria > India > Japan > US > Sweden — is culturally sensible
(high binding in MENA / Sub-Saharan Africa / South Asia, low in Scandinavia). And the unframed
**default (2.71) sits at the liberal end**, essentially at Sweden and *below* the models' own
simulation of a typical American (3.34).

## Result 2 — yes, they stereotype (two signatures), but it is an *informed* stereotype

**Overshoot.** Egypt/Nigeria binding ~4.6, with authority ~4.8 and purity ~4.3, presses the 5.0
ceiling; Sweden sits at 2.23 with purity 1.55 near the floor. The models stretch the range past
what real national means plausibly reach at *both* ends — caricatured-high for the binding
cultures, caricatured-low for Sweden. (Overshoot to be quantified against Atari et al.'s published
country means.)

**Convergence into a shared caricature.** The between-model SD *collapses to 0.15–0.22* for the
binding-heavy and WEIRD anchors (Egypt 0.15, Nigeria/India 0.17; Japan is the loosest at 0.29) —
at or below the models' neutral disagreement of 0.34. Told to be "an Egyptian," the models
produce nearly the identical high-binding profile; they do not argue about what a culture looks
like, they share one picture of it. That convergence is the fingerprint of a common stereotype.

**But it is informed, not blind.** Care stays high and roughly flat across all framings (4.3–4.9),
which is correct — care is the most cross-culturally stable foundation — so the models move the
*right* foundations in the *right* order; they just push the magnitudes to the extremes and agree
with each other about them.

## The twist on the original prediction

We expected framing to spread the models *from each other*. It does the opposite: it spreads each
model *along the dimension* (across countries) while *converging the models with each other*
(within each country). Framing reveals a gallery of caricatures that are ordered correctly,
exaggerated in magnitude, and eerily agreed-upon. The WEIRD default is not the *absence* of a
stereotype — it is one portrait in that gallery, sitting at the secular-liberal end.

## Next

- Quantify overshoot precisely against Atari et al.'s per-country MFQ-2 means (extremity residual).
- Add an **abstract-descriptor** framing ("a highly religious, community-oriented society") to
  partly disentangle genuine cultural mapping from memorized country-norm lookup.
- Extend to MFQ-30 / PVQ-40 and, most importantly, to the Reasoner's own axes.

_All 11 models complete (330/330 cells). Full per-model, per-country, per-foundation numbers are
reproducible via `validity/run_framed.py` + `validity/analyze_framed.py` (raw cells in the
git-ignored `validity/runs_framed/`)._
