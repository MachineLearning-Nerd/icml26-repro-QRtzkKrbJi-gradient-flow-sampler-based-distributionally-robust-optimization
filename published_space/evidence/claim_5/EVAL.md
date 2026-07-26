# Claim 5 evaluator record

## Verdict

**FALSIFIED**

The exact strict “both methods, every perturbation setting, compared with the baseline DRO methods” claim is contradicted by the authors' own full CIFAR-10 Figure 6 vector data. At the nonzero attacked setting `epsilon=0.2, Delta=0.008`, WRM robust accuracy is 80.5616%, compared with 78.3016% for WFR and 77.8714% for WGF. The deficits are 2.2600 and 2.6902 percentage points.

Across all nonzero plotted settings, the exhaustive checker finds 29 WFR and 20 WGF proposed-versus-baseline violations. One would suffice for each method.

## Confidence

**MEDIUM**. The numerical contradiction is exact, full-scale, source-pinned, and reproducible. The material remaining interpretation risk is that the paper's literal phrase “high degree of robustness” is qualitative and weaker than the live judged claim's strict dominance wording.

## Limitations and deviations

- This is a machine-checked falsification from the authors' exact committed result curves, not an independent retraining.
- The official repository omits the required pre-extracted feature tensor, uses one repeat, and contains caption/code inconsistencies recorded in `official_code_audit.json`.
- Those reproducibility limitations are not treated as falsification evidence.
- The result does not deny that WGF/WFR may be useful or robust in a qualitative sense. It only rejects the exact universal comparison under evaluation.

## Evidence

- Exact contract and interpretation: `claim_contract.json`
- Source audit and inline counterexample: `source_audit.md`
- Raw vector paths and source hashes: `official_vector_paths.json`
- Deterministic extractor: `vector_extractor.py`
- Exhaustive checker and output: `independent_checker.py`, `independent_checker_output.json`
- Full-scale counterexample values: `raw_counterexamples.json`
- Negative control and output: `negative_control.py`, `negative_control_output.json`
- Official implementation audit: `official_code_audit.json`
- Fail-closed entrypoint: `verifier.py`
