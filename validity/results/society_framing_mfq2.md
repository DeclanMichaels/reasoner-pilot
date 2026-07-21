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

**Overshoot (quantified — see Result 3).** Against the real human MFQ-2 country means (Atari et al.
2023, Table 7), the models overshoot binding by +0.34 (Egypt) to +1.01 (Japan) points — roughly
0.5 to 1.4 SD — for the three framed countries that appear in that dataset. But the richer story is
*directional* stereotype error, not uniform inflation.

**Convergence into a shared caricature.** The between-model SD *collapses to 0.15–0.22* for the
binding-heavy and WEIRD anchors (Egypt 0.15, Nigeria/India 0.17; Japan is the loosest at 0.29) —
at or below the models' neutral disagreement of 0.34. Told to be "an Egyptian," the models
produce nearly the identical high-binding profile; they do not argue about what a culture looks
like, they share one picture of it. That convergence is the fingerprint of a common stereotype.

**But it is informed, not blind.** Care stays high and roughly flat across all framings (4.3–4.9),
which is correct — care is the most cross-culturally stable foundation — so the models move the
*right* foundations in the *right* order; they just push the magnitudes to the extremes and agree
with each other about them.

## Result 3 — the overshoot is a *template*, and it makes specific, wrong-way errors

Validating the three framed countries that appear in Atari et al.'s 19-nation table (Egypt, Japan,
Nigeria; the US, Sweden, and India are not in that Study-2 sample), model-panel means vs. the real
human M(SD), scored as z = (model − real) / SD:

| Country | Binding overshoot | Largest per-foundation distortions (z) |
|---|--|--|
| Japan | +1.01 (~1.4 SD) | authority **+2.3**, care +1.7, loyalty +1.4, proportionality +1.3 |
| Nigeria | +0.52 (~0.7 SD) | authority +1.0, care +0.7, loyalty +0.7 |
| Egypt | +0.34 (~0.5 SD) | authority +0.9; **equality −1.1** |

Two findings stand out, and they are more interesting than mere inflation.

**Japan is over-moralized wholesale.** Real Japanese are the *lowest*-endorsing sample in the entire
dataset (care 3.03, binding ≈ 2.65). The models ignore this and impose a high-care, high-authority
"traditional East Asian" template — authority +2.3 SD, care +1.7 SD, loyalty +1.4 SD over the real
means. This is the single largest distortion in the study: the model's picture of "a Japanese
person" is nearly the opposite of the data.

**Egypt's egalitarianism is erased.** The models get Egyptian binding roughly right (+0.2 to +0.9
SD) but undershoot Equality by −1.1 SD (model 2.54 vs. real 3.56) — real Egyptians value income
equality highly, and the models assume a religious/traditional society does not. Nigeria shows the
same milder error (equality −0.4 SD).

So the caricature is a **template** — high care + high binding + low equality = "traditional
society" — that the models apply uniformly. It fits the binding-heavy countries tolerably *on
binding*, but misfires systematically wherever a real culture departs from the template: Japan's
across-the-board low endorsement, and the genuine egalitarianism of religious societies. That is a
sharper and more useful result than "they exaggerate": the stereotype has a *shape*, and the shape
is wrong in identifiable, predictable ways.

## The twist on the original prediction

We expected framing to spread the models *from each other*. It does the opposite: it spreads each
model *along the dimension* (across countries) while *converging the models with each other*
(within each country). Framing reveals a gallery of caricatures that are ordered correctly,
exaggerated in magnitude, and eerily agreed-upon. The WEIRD default is not the *absence* of a
stereotype — it is one portrait in that gallery, sitting at the secular-liberal end.

## Next

- Overshoot quantified for the 3 covered countries (Result 3). Remaining: obtain MFQ-2 means for the
  US (Atari Study 1), Sweden, and India to validate the other three framed conditions.
- Add an **abstract-descriptor** framing ("a highly religious, community-oriented society") to
  partly disentangle genuine cultural mapping from memorized country-norm lookup.
- Extend to MFQ-30 / PVQ-40 and, most importantly, to the Reasoner's own axes.

_Human norms: Atari, Haidt & Graham (2023), "Morality Beyond the WEIRD," Table 7 (Study 2, 19
nations). All 11 models complete (330/330 cells). Reproducible via `validity/run_framed.py` +
`validity/analyze_framed.py`; overshoot via the same (raw cells in git-ignored `validity/runs_framed/`)._
