# Evaluator-visible evidence matrix

The audit below starts only from [the canonical current page](#/current-index).
No unpublished branch, OpenResearch dashboard, or hidden local path is needed
to reach any listed evidence.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | [Claim 1](#/claim-1-current) | [Algorithms](../../evidence/claim_1/algorithms.py), [verifier](../../evidence/claim_1/verifier.py) | Exact transition errors, WFR/RGO events | [Raw JSON](../../evidence/claim_1/raw_results.json) | [Independent](../../evidence/claim_1/independent_checker.py) | [Six defects](../../evidence/claim_1/negative_control_output.json) | Six numbered framework algorithms, not convergence | VERIFIED |
| 2 | [Claim 2](#/claim-2-current) | [Certificate](../../evidence/claim_2/certificate.py), [verifier](../../evidence/claim_2/verifier.py) | Full six-tolerance sweep | [Raw JSON](../../evidence/claim_2/raw_results.json) | [Independent](../../evidence/claim_2/independent_checker.py) | [`theta=1`](../../evidence/claim_2/negative_control_output.json) | Universal necessary positive runtime | FALSIFIED |
| 3 | [Claim 3](#/claim-3-current) | [Certificate](../../evidence/claim_3/certificate.py), [verifier](../../evidence/claim_3/verifier.py) | Five calibrated first hits | [Raw JSON](../../evidence/claim_3/raw_results.json) | [Independent](../../evidence/claim_3/independent_checker.py) | [Zero variance](../../evidence/claim_3/negative_control_output.json) | Last-iterate `O(epsilon^-2)` under Assumptions 1–3 | FALSIFIED |
| 4 | [Claim 4](#/claim-4-current) | [Four routes](../../evidence/claim_4/route_4_falsification.py), [verifier](../../evidence/claim_4/verifier.py) | Route findings and work ratios | [Raw JSON](../../evidence/claim_4/raw_results.json) | [Fail-closed verifier](../../evidence/claim_4/verifier.py) | [Exponent control](../../evidence/claim_4/negative_control_output.json) | Algorithm-3 total `epsilon^-4` upper order | BLOCKED |
| 5 | [Claim 5](#/claim-5-current) | [Extractor](../../evidence/claim_5/vector_extractor.py), [verifier](../../evidence/claim_5/verifier.py) | Exact full counterexample table | [Vector paths](../../evidence/claim_5/official_vector_paths.json), [raw](../../evidence/claim_5/raw_counterexamples.json) | [Exhaustive](../../evidence/claim_5/independent_checker.py) | [Dominance control](../../evidence/claim_5/negative_control_output.json) | Strict both-method/all-setting/baseline dominance | FALSIFIED |
| 6 | [Claim 6](#/claim-6-current) | [Certificate](../../evidence/claim_6/certificate.py), [verifier](../../evidence/claim_6/verifier.py) | Symbolic and continuous residuals | [Raw JSON](../../evidence/claim_6/raw_results.json) | [Continuous](../../evidence/claim_6/independent_checker.py) | [Wrong temperature](../../evidence/claim_6/negative_control_output.json) | Universal half-bridge functional identity | VERIFIED |

## Visibility conclusion

All cells are complete. Every claim page states assumptions, quantifiers,
exact command/environment, current evidence SHA, limitations, and deviations.
The current verifier is linked before any historical material.

