# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_e7ae4f7d77c8", "created_at": "2026-07-22T23:55:59+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. The paper introduces a unified PDE gradient flow framework for distributionally robust optimization (DRO) with six concrete algorithms, including Wasserstein Gradient Flow (Algorithm 3) and Wasserstein Fisher-Rao flow (Algorithm 4) variants for entropy-regularized Wasserstein DRO (Section 4, Algorithms 3-4).
2. Proposition 1 shows the Wasserstein gradient flow sampler must run for time at least on the order of O((1/λ) log(L/√(λε))) to produce an ε-accurate gradient estimate (Section 4, Proposition 1).
3. Theorem 1 proves the outer loop of the gradient-flow-sampler-based DRO algorithm requires O(1/ε²_opt) iterations to reach an ε-stationary point (Section 5, Theorem 1).
4. Theorem 2 bounds the total computational complexity of the WGF-based DRO algorithm (Algorithm 3) as Õ(L_Φ L²_U L²_f d² / (λ³_U ε⁴_opt)) (Section 5, Theorem 2).
5. On CIFAR-10 adversarial training under PGD attacks, the WFR- and WGF-based DRO methods achieve consistently higher robust accuracy across all perturbation settings compared to baseline DRO methods (Section 6.3).
6. Lemma 1 establishes that the entropy-regularized DRO problem is equivalent to a Schrödinger half-bridge problem, enabling sampling from the conditional worst-case distribution (Section 3.1, Lemma 1).
