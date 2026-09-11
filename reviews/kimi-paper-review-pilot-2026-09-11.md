# Kimi's review of the Reasoner pilot paper and appendix, 2026-09-11

**Reviewer:** Kimi, one of the model families Declan runs adversarial review through; first round
on this paper. It read the two documents without the repository and says so.
**Reviewed:** the documents after `edfe39a`.
**Adjudicated:** 2026-09-11. Two tickets, #133 and #134. Every number it checked by hand (21,120;
205; 0.363; 0.203; 0.558; the range spans) reproduces.

## Diff against prior rounds

Its concerns 1, 2, 5, 6 and 7 (exposure mismatch, no inert control, provider heterogeneity, weak
clustering evidence, the panel not a sample) are Astra's, already in the text (#120, #128, #123,
#125, A5). Its release asks (bank with loadings, prompts, run manifests, human data, licence) are
met by the repository, which it did not have; A10 now says where each lives. The random-effects
model of the human data and the single-item reliability are the successor study's exposure
ticket (reasoner-study #3), not pilot work (Declan, 2026-09-11).

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| 3 | The models may look alike because they distribute points alike under forced choice; no analysis of allocation patterns, neutral-option use or entropy | Verified and computed. Neutral-option use is similar (models 0.17 to 0.24, humans 0.15 to 0.20) but every model's normalised allocation entropy is 0.85 to 0.95 against 0.46 to 0.51 for humans. Collapsing every allocation on both sides onto its largest option leaves the ratios at 2.35, 3.84, 3.19 and 4.03, from 6.78, 7.69, 5.37 and 5.65. Emitted; A8 table; Summary, Results and Limits carry it | #133 |
| 3 | Factor structure and inter-item consistency not reported; sign check circular | Verified. A9 lists factor structure and consistency under not established; the sign check was already stated (#131) | #134 |
| 4 | Exclusions may be informative; no missingness sensitivity | Verified and computed. Scoring the excluded responses with the stored fallback leaves every b12 model SD unchanged to three decimals (largest per-model shift 0.027); Kimi's geometry displacement 0.223 dropped, 0.196 scored. Emitted; A8. The run records carry no finish-reason field; A1 says so | #134 |
| rel. | Release the bank, prompts, runs, human data, licence | All public in the repository; A10 now names each | #134 |

## Shape of the round

The only round of the four to ask a question the text could not already answer, and the answer
moved a headline number: a good part of the published compression ratio is the models' flatter
allocations. Kimi found it without the data, from the scoring rule alone.
