# In-language MFQ-2: does the caricature survive official translation?

Extension of the society-framed MFQ-2 run (see society_framing_mfq2.md), which left a confound
standing: the human country norms were collected in local languages, but our framed models
answered in English. This run administers the official MFQ-2 translations from Atari et al.'s
OSF materials (Arabic, Japanese, Farsi; keying independently confirmed by the Farsi file's own
scoring block), each in two conditions: framed ("as a typical person from {country}", with the
framing instruction itself in the target language, our translation, disclosed) and neutral (no
system prompt, items in-language). Same 11-model panel, 5 iterations, protocol-matched to the
07-20 run. 329/330 cells valid (one kimi cell failed format twice; that model-condition rests on
4 iterations). Design: the neutral in-language condition separates answering-in-Arabic from
answering-as-an-Egyptian, which no prior condition could do.

Human anchors: Egypt 4.27 and Japan ~2.65 binding (Atari et al. 2023 Table 7); Iran 3.33
(Hazrati, Nejat & Daneshi 2025, N=989, Persian MFQ-2, rescaled 0-4 to 1-5; see
validity/anchors_iran.json for the sampling caveats, which are real: young, online, ~70% female).

## The verdict table (binding composite, 1-5)

| country | human | EN-framed | LANG-framed | LANG-neutral | EN overshoot | LANG overshoot |
|---|--:|--:|--:|--:|--:|--:|
| Egypt | 4.27 | 4.61 | 4.61 | 3.03 | +0.34 | +0.34 |
| Japan | 2.65 | 3.67 | 3.46 | 2.66 | +1.02 | +0.81 |
| Iran | 3.33 | 4.59 | 4.36 | 2.72 | +1.26 | +1.03 |

English neutral baseline (07-20): 2.71, between-model SD 0.34.

## Finding 1: the stereotype survives translation

Egypt's overshoot is byte-for-byte identical in Arabic (+0.34, panel SD 0.15 vs 0.15). Japan's
shrinks by about a fifth (+1.02 to +0.81) but persists. The shared-caricature signature
(collapsed between-model SD under framing, 0.15-0.22) reproduces in every framed in-language
condition. The caricature is not an artifact of English administration.

## Finding 2: the default is language-indexed, but what the language carries varies enormously

Japanese neutral lands at 2.66 against a human mean of 2.65. Unframed, in Japanese, the panel IS
the Japanese population, on the population that the 07-20 run showed the models distort most
when framed. Arabic neutral moves to 3.03 (a third of a point above the English default, with
the panel's widest disagreement, SD 0.46), carrying some binding signal but nowhere near Egypt's
4.27. Farsi neutral is 2.72, indistinguishable from the English default of 2.71: the language
carries nothing.

So the models hold an accurate Japanese profile in their weights, reachable by nothing more than
the language of administration, and the framing instruction drags them AWAY from it (+0.81).
For Japan, telling a model to be Japanese makes it less accurate than speaking Japanese to it.
The 07-20 conclusion sharpens: the Japan distortion is not missing knowledge, it is the framing
selecting the stereotype over knowledge the model demonstrably has.

## Finding 3: Iran is where the template fails worst

English-framed Iran (added 2026-07-24 to close the audit's open hole) lands at 4.59, within 0.02 of
English-framed Egypt: the English template does not distinguish the two countries, and its Iran
overshoot (+1.26, every model, LOO floor +1.23) is the largest measured in the program. In-language
framing shrinks it by 0.23 (paired, CI [+0.14,+0.32]), replicating the Japanese shrink. Framed-as-Iran in Farsi lands at 4.36, one full point above the measured Iranian 3.33, the
largest in-language overshoot in the set. The models template Iran as Egypt (framed 4.36 vs
4.61) but the real populations sit a point apart (3.33 vs 4.27). Per-foundation, the error
concentrates exactly in binding: authority 4.48 vs real 3.05, loyalty 4.45 vs 3.63, purity 4.14
vs 3.32, while equality is dead-on (2.65 vs 2.67). The anchor's convenience-sample skew (young,
online, post-2022 collection) means the true population overshoot is somewhat smaller than
+1.03, but a directional error this size in authority alone does not reduce to sampling.

## What this changes

The two layers are dissociable. Language of administration carries population knowledge (all of
it for Japanese, some for Arabic, none for Farsi); the framing instruction applies a
tradition-template (uniformly, regardless of what the language carried). Which layer dominates
determines whether a "culturally adapted" deployment is accurate or caricatured, and the answer
differs by culture. For the Reasoner program: cultural framing prompts are not a shortcut to
population accuracy even when the model demonstrably contains the population; in-language
administration belongs in the confirmatory design as its own condition.

Reproduce: validity/run_framed_lang.py (raw cells in git-ignored validity/runs_framed_lang/),
analysis validity/analyze_lang.py, instruments built by validity/build_lang_instruments.py from
the official OSF translation files. Framing-instruction translations are ours and are recorded
in each output cell. 2026-07-23.
