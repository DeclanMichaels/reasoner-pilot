# Gemini's review of the Reasoner pilot paper and appendix, 2026-09-11

**Reviewer:** Gemini, one of the model families Declan runs adversarial review through; first
round on this paper.
**Reviewed:** the documents at `9f06413`, after Astra's round and the cold review were applied. It
cites the A3 item-level comparisons, the exclusion tracking and the A8 weighting ratios, none of
which existed before that commit.
**Adjudicated:** 2026-09-11. No ticket; one clause added as a documentation correction below the
level of a published claim.

## Diff against prior rounds

All four of its "major vulnerabilities" are statements the current text already makes, in Limits
and the appendix, most of them put there by Astra's round (`reviews/astra-paper-review-pilot-2026-09-10.md`):

| its item | where the text already says it |
|---|---|
| no inert control; all framings share one scaffold | Limits, "No inert control"; A5; A9; What comes next (#128) |
| convenience sample of technology professionals; ratios are against that sample | Limits, "The human sample"; A1; A3 (#120) |
| provider defaults; rerun variance not on a common footing | What we measured; A1 Request; A4 |
| 0.6/0.4 is the single free parameter; 24 scenarios where an even split is not zero | A2; A8 (#127, #130) |

Its recommendations (a scaffold-only control, standardised temperatures, a broader human sample)
are the paper's own What comes next and the handoff's pre-publication list; recommendations about
future collection are outside the report's scope in any case.

## The one change

It names top-p among the parameters not set. The text had said no temperature and no reasoning
setting. The call layer (`refresh_runner.py`) sends model, messages, a token ceiling, a request
seed where accepted, a user id and nothing else, so both documents now say no sampling parameter
of any kind was sent.

## Shape of the round

Praise-heavy ("exceptionally well-executed", "rare level of scientific integrity", scores out of
ten) and no finding the text did not already carry: a round that confirms the previous one
landed, and a signal that this reviewer's round is exhausted on this text. Its closing sentence
uses "converge", the word Astra flagged in the title; noted, still Declan's call.
