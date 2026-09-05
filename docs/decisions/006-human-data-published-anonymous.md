# 006 - Human responses are published, anonymised at collection

**Date:** 2026-07-20
**Status:** active

## The decision

The 68 human responses ship in this repository. Respondents are identified only by a random UUID
with no name, email or contact field. The `_server` block holding hashes of IP and user agent,
used during collection to recognise returning respondents, was removed before publishing. The
coarse `_meta` browser telemetry is retained.

## Why

The human baseline is what makes every model figure mean anything, so withholding it would make
the central comparison unreproducible. Publishing it required the identifying material to be
gone rather than obscured.

## Rejected alternatives

Withholding the human data and publishing only derived statistics.

## Consequences and gotchas

`DATA-LICENSE.md` governs reuse. Nothing under `human-responses/` is altered, and no re-
identification work is done on it. The sample is a convenience sample within one to two degrees
of the author and cannot speak for any non-Western population.
