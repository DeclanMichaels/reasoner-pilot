# Kimi's second review of the in-language document, 2026-09-08

**Reviewer:** Kimi, second round on this write-up.
**Reviewed:** the paper and appendix at `be5f64e`, after Astra's third round. Kimi rechecked the
headline contrasts (0.05 and 0.08, 1.06 as the mean of the three foundation shifts, 66 percent of
range, the Arabic decomposition, the Ireland cancellation) and found no arithmetic error.
**Adjudicated:** 2026-09-08. Eleven tickets, #72 to #82, all closed the same day. Two of the
three questions put to Declan went with the recommendation given: the binding composite stays the
lead and the Loyalty-Authority composite gets a column; the Arabic shift gets an item-level table.
The third, a country-neutral arm with the framing template, is spending and is not run.

## Diff against prior rounds

Ireland (major 3b) re-raises Astra's first, second and third rounds and stands as adjudicated.
Temperature and the country-neutral arm as new collection (major 1, recommendation 1) re-raise
Gemini's round and Kimi's first; the document already says a further collection sets and records
temperature, and the arm is recorded as a future design. Promoting the Morocco two-arm comparison
(strengths) conflicts with decision 18, Declan's, that the Arabic arm is data and not a comparison.
Re-leading with the Loyalty-Authority composite (major 2) would move the focal quantity after
seeing the results; the report's first line records that the quantity was fixed on 2026-07-20.
Everything else is new and was taken.

## Adjudication

| item | finding | disposition | ticket |
|---|---|---|---|
| 1b | Unframed spread might be inflated by the absence of any system prompt | Verified checkable from the four English unframed variants: a country-free prompt leaves spread at 0.28 on the official file and moves it 0.37 to 0.31 on ours, against 0.17 framed. Emitted in B6a, mirrored in the report | #73 |
| 1c, rec. 3 | The Summary's opening pairs a contrast that changes the questionnaire file (+1.84) with one that does not (+0.34) | Verified. Re-led on the in-language contrasts, Egypt +1.50 and the Arabic average +1.59; the +1.84 moved to the body with its caveat | #72 |
| 1, rec. 1 | Attribution to "country framing" outruns the design; add a country-neutral arm | The document states the two components everywhere the contrast is named. The arm is spending; not run, recorded as a future design | none |
| 2, rec. 2 | Lead with the Loyalty-Authority composite | Declined: the focal quantity was fixed before any translated cell existed. A framing-by-language table with binding and Loyalty-Authority columns (1.063 and 0.982) is added to B6a and the report; Declan | #79 |
| 3a, rec. 4 | rho on three countries is a discrete four-valued number | Verified. Not reported for Arabic or French in the report, the appendix or the viewer; orders and ranges kept | #74 |
| 3b | Ireland's interval sentence does test-like work | Re-raise; stands | none |
| 3c | French framing +0.13 is within run noise | Verified: Belgium's and France's intervals span zero, the within-model median is 0.129. Flagged where French is the exception | #75 |
| 4 | Iran anchors the largest distance | Decision 16 stands; the Summary marks the +1.244 as Iran on its own anchor | #76 |
| 5, rec. 5 | Models not named in the report; release not stated | Verified. The eleven named by vendor string in the methods; a Data and code section names the repository, the ratings dataset and what is withheld | #77 |
| incons. | Five providers, six named; the July collection; "the authors" at the Iran SD | All verified and fixed | #76 |
| incons. | Floor effects unchecked | Verified: unframed Purity 1.97 with the largest unframed spread, 0.449, so a floor would compress the unframed spread, the larger one. One sentence in B6a | #78 |
| incons., rec. 6 | The Arabic shift is never examined item by item | Taken: B6a gains the 36-item table. Broad, not concentrated: all 18 binding items up, Purity +0.38 to +0.82, Equality +0.18 to +0.47, Care within 0.04. No mechanism offered (report-scope rule); Declan | #80 |
| strengths | Promote the Morocco two-arm sentence | Declined: decision 18 | none |

On the round Declan also decided that the report and appendix become one document (decision 20,
#81), and asked for a cold read of the result (#82), which made eight wording fixes.
