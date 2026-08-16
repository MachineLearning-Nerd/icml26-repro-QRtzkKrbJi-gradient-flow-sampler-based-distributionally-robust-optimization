# Environment and reproduction boundary

## Canonical command

~~~bash
uv sync --frozen
uv run --frozen --no-dev python -m reproduction.run_all
~~~

The repository-level command validates the historical judged snapshot, runs
the six published-space claim verifiers, and runs the evaluator-visible
release audit. The lockfile and Python 3.12 requirement are authoritative.

## Recorded compute

- Python: 3.12
- Dependency resolution: <code>uv.lock</code>
- Scientific verifiers: CPU-only, one process
- No GPU result is claimed
- Managed experiments used the recorded Hugging Face <code>cpu-upgrade</code>
  environment; local checks were short CPU runs
- The final six-claim scientific suite was recorded at approximately 8.5
  seconds, with setup overhead separate

## Evidence inputs

- Exact judged contract: arXiv <code>2510.25956v1</code>
- Current context: arXiv <code>2510.25956v3</code>
- Historical judge snapshot: Space revision
  <code>735012f52396955c5734e8fc568adfdf2abda757</code>
- Official code provenance: <code>ZusenXu/GFS-DRO</code> at the pinned commit
  in <code>sources/paper/source_manifest.json</code>
- Figure 6 audit: complete vector data, not raster digitization

## Boundary

Claim 2, Claim 3, and Claim 5 verdicts apply to their exact v1/judged
contracts. Claim 4 is deliberately blocked. Current v3 changes theorem
numbering and rates and is recorded as source context rather than substituted
into the v1 verdicts. Numerical results can vary outside the lockfile,
hardware, and seed boundary.
