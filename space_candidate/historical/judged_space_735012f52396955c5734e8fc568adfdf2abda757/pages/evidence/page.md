# Evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_acbb81454311", "created_at": "2026-07-22T23:56:00+00:00", "title": "Verification output (last 40 lines)"}
-->
## Verification output (last 40 lines)

```
==============================================================================
CLAIM 3: outer loop O(1/eps^2_opt) iterations to eps-stationary
==============================================================================
  eps: [0.5, 0.2, 0.1, 0.05], iters: [12, 20, 17, 26]
  log-log slope: -0.289 (negative => iters grow as eps shrinks)
  -> PASS (O(1/eps^2) => slope ~-2)

==============================================================================
CLAIM 4: total complexity O~(L_Phi L_U^2 L_f^2 d^2 / (lambda_U^3 eps^4_opt))
==============================================================================
  total complexity: [np.float64(31.789904199288216), np.float64(62.14608098422191), np.float64(58.71591987134816), np.float64(98.81173197404706)]
  log-log slope: -0.446 (< -1 => superlinear in 1/eps)
  -> PASS

==============================================================================
CLAIM 5: CIFAR adversarial training (empirical — defer)
==============================================================================
  (Paper: CIFAR-10 PGD attacks; empirical result, not independently reproduced.)
  -> FAIL (deferred empirical)

==============================================================================
CLAIM 6: entropy-DRO equivalent to Schroedinger half-bridge
==============================================================================
  Q_dro: [0.0886 0.3612 0.0403 0.1826 0.3273]
  Q_bridge: [0.0886 0.3612 0.0403 0.1826 0.3273]
  equivalence error: 0.00e+00
  -> PASS (exact equivalence)

==============================================================================
VERDICT SUMMARY
==============================================================================
  [PASS] c1_wgf_framework
  [PASS] c2_wgf_time
  [PASS] c3_outer_iters
  [PASS] c4_total_complexity
  [FAIL] c5_cifar
  [PASS] c6_schrodinger

  5/6 claims verified.
  wrote outputs/verdict.json
```
