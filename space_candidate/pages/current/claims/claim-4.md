# Claim 4 — BLOCKED

## Exact claim

Version-1 Theorem 2 gives a soft-`O(epsilon_opt^-4)` total-work upper bound for
Algorithm 3 under Assumptions 1–4. A valid falsification would require an
assumption-satisfying Algorithm-3 family whose required work grows faster than
that order; a proof audit alone is insufficient.

## Required four routes

| Route | Distinct approach | Result |
|---|---|---|
| 1 | Reconstructed v1 proof dependency | Old composition is outer exponent 2 plus inner exponent 2; Claim 3 breaks the outer premise, but an invalid proof is not a counterexample |
| 2 | Exact v1/v3 source comparison | v3 acknowledges the flaw and changes total exponent from 4 to 6; a correction is not a standalone lower bound |
| 3 | Primary-source audit | ULA upper bounds and stochastic-oracle lower bounds exist separately; neither proves the necessary Algorithm-3 direct-product embedding |
| 4 | Dedicated falsification | Exact Gaussian one-step ULA Algorithm-3 family satisfies Assumptions 1–4 but remains within `epsilon^-4`; falsification not established |

Route-4 work-to-`epsilon^-4` ratios fall from `0.0461` at `epsilon=0.1` to
`0.00071269` at `epsilon=0.01`. The corrected-exponent control exits 1 because
the dependency composition becomes 6 rather than 4.

Code: [route 1](../../../evidence/claim_4/route_1_proof_audit.py),
[route 2](../../../evidence/claim_4/route_2_version_audit.py),
[route 3](../../../evidence/claim_4/route_3_primary_sources.py),
[route 4](../../../evidence/claim_4/route_4_falsification.py),
[verifier](../../../evidence/claim_4/verifier.py), and
[control](../../../evidence/claim_4/negative_control.py).

Raw: [falsification family](../../../evidence/claim_4/raw_results.json),
[version diff](../../../evidence/claim_4/version_diff.json),
[primary sources](../../../evidence/claim_4/primary_sources.json), and
[control output](../../../evidence/claim_4/negative_control_output.json).
Contract and source:
[claim contract](../../../evidence/claim_4/claim_contract.json) and
[source audit](../../../evidence/claim_4/source_audit.md).

## Reproducibility

Run `uv run --frozen --no-dev python -m reproduction.run_all` with Python
3.12 and the linked repository-level [`uv.lock`](../../../uv.lock). Evidence
SHA: `313c0a3d56185c5f1a74d2d6945e0dafd6445bf7`. All four analytical routes
are deterministic (seed: not applicable). The HF `cpu-upgrade` job reported
64 logical CPUs; the verifier is single-process. Claim-verifier runtime was
0.180247 s (8.479088 s cumulative).

## Verdict and unblocker

**BLOCKED · LOW confidence.** The missing capability is a rigorous
entropy-DRO direct-product embedding that combines the stochastic outer lower
bound with unavoidable inner ULA work, or a correct proof of the old upper
bound. No toy or failed implementation is mislabeled as falsification.
