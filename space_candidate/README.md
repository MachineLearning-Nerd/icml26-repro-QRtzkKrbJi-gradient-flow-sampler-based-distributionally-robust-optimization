---
title: "GFS-DRO exact claim audit"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-QRtzkKrbJi
---

# GFS-DRO exact claim audit

**Current live judged score: 4/12. No score increase is claimed.**

This additive candidate replaces toy/proxy checks with exact claim contracts:
two VERIFIED, three FALSIFIED, and one rigorously BLOCKED after four routes.
The conservative forecast is 8–10/12; the best-supported possible score is
10/12, pending a future live judge.

Start at the [current canonical evidence page](#/current-index). The obvious
verifier is:

```bash
uv run --frozen --no-dev python -m reproduction.run_all
```

The previous judged revision
`735012f52396955c5734e8fc568adfdf2abda757` is preserved under
[Historical rejected baseline](#/historical-rejected-baseline).
