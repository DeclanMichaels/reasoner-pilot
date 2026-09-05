# The Reasoner - pilot

A published, exploratory benchmark measuring the structure of moral reasoning, scoring humans and
language models in one space across four bipolar axes.

> **What this file is:** the glossary. Each entry says what a term **is**, in one or two sentences,
> plus the words ruled out for it.
>
> **What this file is not:** a spec or a place for reasoning. A sentence with a "because" in it
> belongs in `DECISIONS.md`. Only terms specific to this study belong here.

## A note the successor study needs

This vocabulary is **live here and retired there.** The confirmatory study, `reasoner-study`,
replaced the four bipolar axes with five compositional adjudicative logics, and its own glossary
lists `axis`, `pole` and `pivot` under *Avoid*. Neither file is wrong. A term that is canonical in
one and forbidden in the other is a fact about which instrument is being discussed, and the study's
own rule is that no crosswalk exists between them.

## The instrument

**The Reasoner**:
The instrument: per scenario, a judgment question and a reasoning question, each a constant-sum
allocation over that scenario's own answer options, combined into a position on one axis.

**Axis**:
One of four bipolar dimensions a scenario scores on, running from -1 to +1. The four are Moral
Agent, Authority, Moral Domain and Obligation Scope.
_Avoid_: dimension, scale, factor. Note that `dimension_id` is the field name in `scenarios.json`
and stays as-is; the prose term is axis.

**Pole**:
One end of an axis, with its own written label. Moral Agent runs relational to autonomous;
Authority deferential to skeptical; Moral Domain broad to narrow; Obligation Scope relational to
universal.

**Judgment question**:
What should happen. A constant-sum allocation over answer options **written for that scenario**.

**Reasoning question**:
Why it matters. A constant-sum allocation over answer options **written for that scenario**, not
over a fixed set shared across the bank. This is the design the successor study replaced, and the
difference is the reason no crosswalk between the two instruments exists.

**Axis score**:
A scenario's position from -1 to +1, pooling the judgment allocation and the reasoning allocation
and combining them 0.6 to 0.4.
_Avoid_: dimensional score, except as the key name `dimensional_scores` in the human response files.

**Pivot**:
Retired field name. In run files predating 2026-07-22 it means the logic or pole a stem was written
to load on.
_Avoid_: in prose. Say what is meant.

## The bank and the panel

**Scenario bank**:
The 48 scenarios in `scenarios.json`. Twelve carry `has_human_baseline` and are the only ones the
human respondents answered.
_Avoid_: item pool, instrument.

**Baseline twelve**:
The twelve scenarios with human responses. Any human-to-model comparison runs on these; the full 48
is model-side only. A number computed on one and reported as the other is a category error.
_Avoid_: the core set, the human subset.

**Panel**:
The eleven frontier models from nine labs, three of them Chinese, scored as a group. The **model is
the unit**: each model's five reruns are averaged before it enters a panel figure, so a model that
answers at length cannot outvote the rest.
_Avoid_: the models, the sample. A panel is not a probability sample of anything.

**Cell**:
One model crossed with one framing, holding all five reruns. The unit a run file stores.

**Rerun**:
One of the five repetitions of a cell. Statement order is reshuffled every rerun.
_Avoid_: iteration, trial, replicate.

**Framing**:
One of nine prompt conditions in `framings.json`, sharing a matched scaffold so only the organizing
principle varies: `neutral`, four cultural (`individualist`, `collectivist`, `hierarchical`,
`egalitarian`), two nonsense (`nonsense_geometry`, `nonsense_color`), and two non-moral placebos
(`irrelevant`, `weekday`).
_Avoid_: condition, when the framing specifically is meant; a condition is a framing crossed with
a language or an instrument.

**Nonsense framing**:
A framing naming an arbitrary principle as the basis of moral life without asserting any verdict.
The placebos are a separate thing: their principle governs daily routines rather than moral
obligation, and they set the noise floor.

## Findings the papers name

**Compression**:
The panel occupying a narrower band than a size-matched human sample on the same axis. The pilot's
figure is 5.4 to 7.7 times narrower, on eleven models and 68 humans, every ratio interval's lower
bound at or above 3.66.
_Avoid_: "three to four times" and "five models", both of which appear in older drafts and are
wrong; the first was a lower-bound reading presented as the estimate.

**Nonsense compliance**:
Models folding a nonsense framing into fluent moral reasoning rather than rejecting it.
_Avoid_: hallucination, failure. The instrument measures the response, not a defect.

**Nonsense integration**:
The scored form of that compliance, as distinct from the descriptive observation.

## The convergent-validity and in-language work

**Convergent validity module**:
The MFQ-30 and PVQ-40 runs under `validity/`, comparing axis positions against established values
instruments. Axis-based, so it belongs to this instrument and does not transfer to the successor.

**In-language grid**:
The MFQ-2 collection administered in six official translations: eleven models, fifty conditions,
2,750 scored cells, no cell missing a model.
_Avoid_: quoting the appendix's 20 conditions and 1,100 cells, which describe an earlier, smaller
collection.

**Condition**:
In the in-language work, a framing crossed with an administration language. Fifty of them.

**Framed and unframed**:
Whether a condition instructs the model to answer as a person from a named country. The two are not
comparable on dispersion: naming a country roughly halves between-model spread by construction.

## Provenance and status

**The pilot**:
This repository. Exploratory throughout, published, and kept as-is. Its findings inform the
confirmatory study's design and underwrite no registered claim there.
_Avoid_: version one, the previous study, the preliminary study.

**Convergence**:
The relationship between a finding here and a matching finding in the successor study. The
instruments share no items, so a reappearing pattern is convergence across dissimilar instruments.
_Avoid_: replication, confirmation.

**Published record**:
The papers, the appendix, the viewer and everything under `results/`. Pinned byte for byte by
`analysis/test_reproduce.py` against `analysis/reproduce_manifest.json`.
