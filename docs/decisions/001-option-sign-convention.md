# 001 - A global option-sign convention, fixed before release

**Date:** 2026-07-19
**Status:** historic

## The decision

`pole_a` is the -1 side and `pole_b` the +1 side, globally, fixed on 2026-07-19. Every run and
every output in this repository is post-fix.

## Why

A per-scenario sign convention makes an axis score's direction depend on how one item happened
to be authored, and the error is invisible in the output: a sign-flipped scenario produces a
plausible number in the wrong direction.

## Consequences and gotchas

Any run file or analysis predating the fix is not comparable and is not in this repository.
