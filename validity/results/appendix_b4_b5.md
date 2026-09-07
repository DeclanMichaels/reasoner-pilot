## B4. The test families

Two families, one per headline claim, both post hoc and both exploratory. Paired tests use per-model differences; anchor tests subtract the constant from each model's mean. Exact sign-flip permutation: with eleven models the minimum attainable two-sided p is 2/2048, reported as 0.001. Nothing was pre-registered.

**Family A, the framing claim.** Ten comparisons, Holm across the ten.

| test | difference | 95% CI | exact p | Holm |
|---|--:|:--:|--:|--:|
| T1 Egypt: EN-framed vs AR-framed | +0.001 | [-0.054, +0.048] | 1.0000 | 1.0000 |
| T2 Japan: EN-framed vs JA-framed | +0.233 | [+0.098, +0.384] | 0.0059 | 0.0234 |
| T3 JA-neutral vs Japan anchor | +0.024 | [-0.155, +0.233] | 0.8330 | 1.0000 |
| T4 FA-framed vs Iran anchor [*] | +0.981 | [+0.815, +1.144] | 0.0010 | 0.0098 |
| T5 FA-neutral vs EN-neutral | +0.040 | [-0.117, +0.184] | 0.6357 | 1.0000 |
| T6 AR-neutral vs EN-neutral | +0.335 | [+0.201, +0.483] | 0.0010 | 0.0098 |
| T7 AR-framed vs Egypt anchor | +0.337 | [+0.218, +0.450] | 0.0020 | 0.0117 |
| T8 Japan: framed vs neutral (in-lang) | +0.759 | [+0.592, +0.921] | 0.0010 | 0.0098 |
| T9 EN-framed Iran vs Iran anchor [*] | +1.244 | [+1.137, +1.338] | 0.0010 | 0.0098 |
| T10 Iran: EN-framed vs FA-framed | +0.263 | [+0.148, +0.380] | 0.0029 | 0.0146 |

Nulls are reported as bounds, not as demonstrated absence: any Egypt language effect is within 0.054, and any Japanese-neutral displacement from the Japanese mean is within 0.233.

**Family B, the language claim.** One comparison per language, asking whether that language's unframed condition departs from the panel's English default. Holm across the three. T5 and T6 sit in both families; the double membership is disclosed rather than removed by re-cutting family A, and every conclusion holds under either cut.

| test | difference | 95% CI | exact p | Holm | models moving up |
|---|--:|:--:|--:|--:|--:|
| T5 FA-neutral vs EN-neutral | +0.040 | [-0.117, +0.184] | 0.6357 | 0.8613 | 7 of 11 |
| T6 AR-neutral vs EN-neutral | +0.335 | [+0.201, +0.483] | 0.0010 | 0.0029 | 11 of 11, none down |
| T11 JA-neutral vs EN-neutral | -0.093 | [-0.299, +0.111] | 0.4307 | 0.8613 | 3 of 11 |

Arabic is the only language whose interval excludes zero, and no model moves against it. Farsi splits 7 up to 4 down and Japanese 3 up to 8 down. As bounds: any Farsi departure from the English default is within 0.184, and any Japanese departure is within 0.299.

One further comparison is reported outside both families as a single descriptive: the English default sits +0.117 from the Japanese human mean.

**[*] The Iran anchor, and what it costs.** Nineteen of the twenty anchors are Atari et al. (2023) Study 2. Iran is not in that set; its anchor is Hazrati, Nejat and Daneshi (2025), a different paper with different collection conditions. That sample is a Telegram and snowball convenience sample, n=989, 68 to 71 percent female, mean age 26 to 28, 57 to 59 percent educated to bachelor's or above, and the anchor file records it as likely less binding-endorsing than the general Iranian population - which would bias this overshoot upward. Collection began a year after the Woman, Life, Freedom movement and the authors note possible period effects. Iran is the only Farsi country, so it carries that group throughout.

Every anchor the source offers is shown. The one in use is the largest of the three, so the overshoot reported throughout is the smallest of the three:

| Iran anchor | binding | EN-framed overshoot | FA-framed overshoot |
|---|--:|--:|--:|
| sample 2, n=989 (in use) | 3.333 | +1.244 | +0.981 |
| sample 1, n=392 | 3.231 | +1.346 | +1.083 |
| n-weighted pool of both | 3.304 | +1.273 | +1.010 |

The sign and the ordering of the Iran result do not depend on the choice. Its magnitude does, by up to 0.102.

## B5. Robustness: leave-one-model-out

Japanese neutral panel mean with each model removed spans 2.603 to 2.714 around an anchor of 2.652. English-framed Iran overshoot spans +1.220 to +1.284; Farsi-framed Iran overshoot spans +0.933 to +1.030. Every individual model overshoots both Iran conditions. T11, the Japanese language effect, spans -0.162 to -0.020 under the same sweep.

