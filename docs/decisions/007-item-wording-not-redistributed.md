# 007 - Instrument item wording is not redistributed; derived results are

**Date:** 2026-07-20
**Status:** active

## The decision

Filled instruments and raw per-cell run files for the convergent-validity module stay local and
gitignored. Derived results carrying no item text are published under `validity/results/`.

## Why

The MFQ and PVQ item wording is not ours to republish. Splitting at the derived-results boundary
keeps the findings public without redistributing the instruments.

## Consequences and gotchas

The consequence is a real one: the convergent-validity numbers cannot be regenerated from a
fresh clone. Check `.gitignore` before adding anything under `validity/`.
