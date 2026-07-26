# Claim 3 — FALSIFIED

## Exact claim

Version-1 Theorem 1 states that the last-iterate outer loop reaches
`E||grad Phi(theta_S)||² <= epsilon²` in `O(1/epsilon²)` iterations under
Assumptions 1–3, with constant step `O(1/L_Phi)` and sufficiently controlled
sampler error.

## Exact admissible instance

The entropy-Wasserstein construction has `Phi(theta)=theta²+constant`,
`L_Phi=2`, an exact inner sampler (`delta_sample=0`), a 1-Lipschitz gradient
observable, and unit stochastic-gradient variance. The exact recurrence and
independently calibrated constant steps give:

| epsilon | minimum iterations | `S epsilon²/log(1/epsilon)` |
|---:|---:|---:|
| 0.20 | 48 | 1.193 |
| 0.10 | 231 | 1.003 |
| 0.05 | 1,076 | 0.898 |
| 0.02 | 7,973 | 0.815 |
| 0.01 | 35,635 | 0.774 |

This certifies `Omega(epsilon^-2 log(1/epsilon))`, contradicting the claimed
`O(epsilon^-2)` last-iterate rate. The antithetic zero-variance control reaches
`epsilon=0.01` in 8 iterations within the `epsilon^-2=10,000` budget and exits
1, so stochastic variance is the intended hard mechanism.

Code: [certificate](../../../evidence/claim_3/certificate.py),
[calibrated generator](../../../evidence/claim_3/generate_raw.py),
[checker](../../../evidence/claim_3/independent_checker.py),
[verifier](../../../evidence/claim_3/verifier.py), and
[control](../../../evidence/claim_3/negative_control.py).

Raw: [first hits](../../../evidence/claim_3/raw_results.json),
[checker output](../../../evidence/claim_3/independent_checker_output.json),
[control output](../../../evidence/claim_3/negative_control_output.json).
Contract and source:
[claim contract](../../../evidence/claim_3/claim_contract.json) and
[source audit](../../../evidence/claim_3/source_audit.md).

## Reproducibility

Run `uv run --frozen --no-dev python -m reproduction.run_all` with Python
3.12 and the linked repository-level [`uv.lock`](../../../uv.lock). Evidence
SHA: `313c0a3d56185c5f1a74d2d6945e0dafd6445bf7`. The exact recurrence,
golden-section calibration, and first-hit search are deterministic (seed: not
applicable). The HF `cpu-upgrade` job reported 64 logical CPUs; the verifier
is single-process. Claim-verifier runtime was 1.536713 s (8.479088 s
cumulative).

## Verdict and version note

**FALSIFIED · HIGH confidence.** Current v3 changes the outer result to
`epsilon^-4` with an iteration-dependent step and changes total complexity to
`epsilon^-6`; this independent source drift is not used as the counterexample.
