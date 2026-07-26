# Gradient Flow Sampler-based DRO — reproduction campaign

This branch is the frozen OpenResearch control for the live judged state of
[Gradient Flow Sampler-based Distributionally Robust Optimization](https://arxiv.org/abs/2510.25956).
The previous Hugging Face logbook received **4/12** from revision
`735012f52396955c5734e8fc568adfdf2abda757`.

No score increase is claimed here. The old toy checks are preserved under
`historical/` and labeled **Historical rejected baseline**. The fixed cumulative
command is:

```bash
uv run --frozen --no-dev python -m reproduction.run_all
```

The exact judged-contract source is arXiv v1; the current paper is v3. See
`sources/paper/source_audit.md` for the source drift, assumptions, and
quantifiers.
