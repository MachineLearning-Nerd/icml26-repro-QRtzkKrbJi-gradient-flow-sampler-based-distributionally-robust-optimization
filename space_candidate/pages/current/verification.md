# Current cumulative verifier

This page supersedes the old toy page titled “Verification run.”

## Exact command and environment

```bash
uv run --frozen --no-dev python -m reproduction.run_all
```

- [Current fail-closed entrypoint](../../reproduction/run_all.py)
- [Pinned `pyproject.toml`](../../pyproject.toml)
- [Pinned `uv.lock`](../../uv.lock)
- Python 3.12; one repository-level `.venv`; no conda or unmanaged pip
- No GPU requested or used

The entrypoint discovers Claims 1–6, runs every current verifier, requires the
exact verdict mapping, and exits nonzero on any checker, raw-output, or
negative-control mismatch.

## Latest cumulative scientific run

| Field | Value |
|---|---|
| Git SHA | `313c0a3d56185c5f1a74d2d6945e0dafd6445bf7` |
| Run | `6e093d35-cc64-4a3c-8760-4afba7778df4` |
| Backend | Hugging Face `cpu-upgrade` |
| Image | `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` |
| CPU allocation | 64 logical CPUs reported by OS |
| Scientific core contract | 1 process/core |
| Scientific runtime | 8.479088 seconds |
| Managed wall status duration | 37 seconds |
| Cost | Hugging Face job; exact monetary billing not exposed by `orx` |

## Raw verifier output

| Claim | Exit | Current output |
|---|---:|---|
| 1 | 0 | `VERIFIED`; six algorithms; six defects rejected |
| 2 | 0 | `FALSIFIED`; first-hit time 0 versus positive claimed scale |
| 3 | 0 | `FALSIFIED`; exact extra logarithmic factor |
| 4 | 0 | `BLOCKED`; all four routes present |
| 5 | 0 | `FALSIFIED`; WGF 20 and WFR 29 nonzero violations |
| 6 | 0 | `VERIFIED`; symbolic residual 0 |

Expected controls:

| Claim | Control | Expected exit |
|---|---|---:|
| 1 | Six operation defects | 1 |
| 2 | Nonsymmetric `theta=1` instance | 1 |
| 3 | Antithetic zero-variance oracle | 1 |
| 4 | Corrected exponent composition | 1 |
| 5 | Dominance-satisfying synthetic curves | 1 |
| 6 | Wrong-temperature Gibbs law | 1 |

Every recorded control output is linked from its [claim page](#/current-index).

