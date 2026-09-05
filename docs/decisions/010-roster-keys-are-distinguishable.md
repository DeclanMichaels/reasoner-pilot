# 010 - A swapped model gets a distinguishable roster key

**Date:** 2026-08-21
**Status:** active

## The decision

When a provider withdraws a model mid-programme, the replacement enters under its own roster key
rather than inheriting the old one. Kimi-K2.6 went off serverless at Together and K3 took its
place under a new key.

## Why

A roster key that silently changes which model it refers to makes two collections look
comparable when they are not. This is the third time a provider has withdrawn a served model,
after Qwen and GLM dropped from the panel in July, so it is a recurring condition rather than an
incident.

## Consequences and gotchas

Verified against the live API rather than inferred from the error text.
