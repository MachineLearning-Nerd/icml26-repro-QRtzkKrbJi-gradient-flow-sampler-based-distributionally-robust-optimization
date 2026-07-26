# Current exact evidence: Gradient Flow Sampler-based DRO

![Five exact outcomes; Claim 4 blocked](images/headline_outcomes.svg)

**Previous live judged score: 4/12.**  
**Conservative projected score range: 8–10/12.**  
**Best-supported possible score: 10/12 — forecast only, not a judge result.**

The judged contract is arXiv `2510.25956v1` (PDF SHA-256
`796d3cb25e2a9062ab4e81201daa7837c4bf615399063b0ed439c9e17e6db8d6`).
Current arXiv v3 changes the two complexity theorems. All important source
anchors, assumptions, raw numbers, code, controls, and limitations are linked
from this page.

| Claim | Current result | Confidence | Forecast points | One-line basis |
|---|---|---|---:|---|
| [1 — six algorithms](#/claim-1-current) | VERIFIED | HIGH | 2 | Algorithms 1–6 execute; defining transitions and operations independently checked |
| [2 — necessary sampler time](#/claim-2-current) | FALSIFIED | HIGH | 2 | Admissible exact case is gradient-accurate at time 0 for every tolerance |
| [3 — outer `epsilon^-2`](#/claim-3-current) | FALSIFIED | HIGH | 2 | Exact stochastic instance requires an extra `log(1/epsilon)` factor |
| [4 — total `epsilon^-4`](#/claim-4-current) | BLOCKED | LOW | 0 | Four routes completed; no valid proof or counterexample |
| [5 — CIFAR strict dominance](#/claim-5-current) | FALSIFIED | MEDIUM | 2 | Authors' exact vector curves contain 49 nonzero proposed-vs-baseline violations |
| [6 — half-bridge](#/claim-6-current) | VERIFIED | HIGH | 2 | Universal symbolic identity plus continuous independent checks |

## Run the current verifier

```bash
uv run --frozen --no-dev python -m reproduction.run_all
```

- Scientific evidence Git SHA: `313c0a3d56185c5f1a74d2d6945e0dafd6445bf7`
- Managed evidence run: `6e093d35-cc64-4a3c-8760-4afba7778df4`
- Backend/flavor: Hugging Face `cpu-upgrade`; no GPU
- Allocation reported by the job: 64 logical CPUs
- Scientific execution contract: one process/core
- Six-claim cumulative scientific runtime: 8.479088 seconds
- Exact environment: Python 3.12 and [`uv.lock`](../../uv.lock)

[Open the current verifier](#/current-verification) ·
[Open the visibility matrix](#/visibility-matrix) ·
[Read the visual report](#/visual-report) ·
[Read the release forecast](#/release-report) ·
[Read the evaluator-blind review](#/red-team-review)

## Historical safety

The prior judged Space revision
`735012f52396955c5734e8fc568adfdf2abda757` remains reachable as
[Historical rejected baseline](#/historical-rejected-baseline). Its toy
“Verification run” is not the current verifier.
