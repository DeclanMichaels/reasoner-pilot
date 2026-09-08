# 021 - The September wave: the framing template without a country, matched to the August grid

**Date:** 2026-09-08
**Status:** active

## The decision

A second, small collection, kept distinct from the fifty-condition August grid: three English
conditions on the ten panel models Together and the other providers still served on 2026-09-08.
The framing template with its three country slots deleted and nothing added, on the official
English instrument; the unframed English comparator rerun; English-framed Egypt rerun. Five
iterations each, the same seed bases and shuffle keys as the August cells they pair with, so the
reruns have item-identical orders. No temperature is sent. The run files are tracked in git under
`validity/runs_neutral_template/`.

## Why

Every review round asked what part of the framing shift is the instruction to be a typical
person rather than the country named, and the design could not say: the unframed conditions send
no system prompt, and the self-report control says "about yourself", the opposite of role-taking.
The template minus its country slots sits between the two arms and splits the shift.

A September cell against an August grid carries a window the grid does not, so the two reruns
price the window directly on the two cells the new arm is subtracted from.

Not sending a temperature sets aside the standing rule on purpose: the grid ran at provider
defaults, and setting one now would put temperature and window into the same contrast. The
provider's response body is kept and any temperature it reports is recorded; none of the five
reports one.

The official instrument matches the unframed comparator, so the template-minus-unframed contrast
is clean; the framed-minus-template contrast then carries the transcription difference, already
measured unframed at -0.009.

## Rejected alternatives

A dedicated Together endpoint for DeepSeek-V4-Pro, which left the serverless tier after August:
hourly billing for fifteen calls. Substituting the dated DeepSeek-V4-Pro-0813: a different model
under decision 10, useless for a drift check. The wave runs on ten models and the August contrasts
it is set against are restricted to the same ten; the absence is infrastructural and disclosed
the way decision 9 discloses the three absent panel models.

The six translated templates: they need country-neutral translations first, and the English arm
answers the question the reviewers asked.

## Consequences and gotchas

The wave is reported as its own section, B4a, and a paragraph in B1; the fifty-condition grid's
counts do not change. Its three conditions enter the ratings dataset and `condition_means.json`.
The run files carry replies and system prompts and no item wording, which is why they can be
tracked (decision 7); the S3 archive follows when the AWS session is renewed.
