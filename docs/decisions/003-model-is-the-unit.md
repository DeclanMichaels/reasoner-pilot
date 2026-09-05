# 003 - The model is the unit, and reruns are averaged first

**Date:** 2026-07-20
**Status:** active

## The decision

Each model's five reruns are averaged before it enters any panel figure. Intervals are
percentile bootstrap over models.

## Why

Pooling reruns as independent observations lets a model that answers at length outvote the rest,
and it counts rerun noise as if it were between-model variation. Averaging first costs precision
and buys a figure that means what it says.

## Consequences and gotchas

Intervals resample eleven values, so their tails are coarse and are a range rather than a
calibrated bound. The eleven are not a probability sample of any population of models, so an
interval here is not a confidence interval for models in general. The averaging also produces a
real aggregation artifact against single human responses; see entry 8.
