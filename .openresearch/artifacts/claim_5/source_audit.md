# Claim 5 source audit

## Exact sources

- Paper contract: arXiv `2510.25956v1`, PDF SHA-256 `796d3cb25e2a9062ab4e81201daa7837c4bf615399063b0ed439c9e17e6db8d6`, Section 6.3 and Figure 6, PDF page 11, extracted lines 752-803.
- Official code/results: `ZusenXu/GFS-DRO` commit `6f9fb5c9e432b5cc6ad62916b36f102984b4d076`.
- Official Figure 6 source PDFs were retrieved 2026-07-26 with the explicit User-Agent recorded in `official_vector_paths.json`. Their paths and SHA-256 hashes are recorded there.

## Statement audit

The live judged claim says both WFR and WGF have higher robust accuracy “across all perturbation settings compared to baseline DRO methods.” This creates a strict universal comparison across WGF/WFR, the plotted attack settings, and the baseline DRO methods Dual/WRM.

The literal paper is weaker and qualitative: it says WFR and WGF “consistently achieve a high degree of robustness across all settings.” It also says Dual is “comparably” robust at `epsilon=0.2`. Therefore the judged claim is an over-strong interpretation of the prose. The falsification applies to that exact judged strict-dominance claim, not to an undefined qualitative notion of a “high degree.”

## Domain and quantifiers

Figure 6 uses CIFAR-10, 512-dimensional ResNet-50-derived features, multiclass logistic regression, 10 training epochs, `tau=0.05`, three entropy values, and normalized `l2` PGD radii from 0 to 0.08. The checker conservatively excludes the clean point and tests the ten nonzero attack radii.

For every entropy value, radius, proposed method, and baseline, strict higher robust accuracy is equivalent to strict lower plotted test error. A single violation falsifies the universal. The committed authors' curves contain violations for both WGF and WFR.

## Full-scale counterexample

At `epsilon=0.2` and nonzero `Delta=0.008`, the exact vector coordinates give:

| Method | Test error | Robust accuracy |
|---|---:|---:|
| WRM | 19.4384% | 80.5616% |
| WFR | 21.6984% | 78.3016% |
| WGF | 22.1286% | 77.8714% |

Thus WRM exceeds WFR by 2.2600 and WGF by 2.6902 robust-accuracy percentage points in the paper's own full CIFAR-10 plot.
