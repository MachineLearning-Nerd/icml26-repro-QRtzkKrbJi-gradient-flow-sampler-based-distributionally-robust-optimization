# Claim 4 four-route method

Confidence remained LOW, so the mandated four distinct routes were completed.

## Route 1 — proof dependency

Command:

`python .openresearch/artifacts/claim_4/route_1_proof_audit.py`

This independently reconstructs the exponent multiplication and verifies that
v1's `4` is exactly `outer 2 + inner 2`. Replacing the falsified outer factor
by the corrected stochastic factor yields `6`. Result: the v1 proof does not
verify the theorem.

## Route 2 — author/version correction

Command:

`python .openresearch/artifacts/claim_4/route_2_version_audit.py`

This checks the exact v1/v3 hashes, anchors, `4 -> 6` statement change, and the
v3 acknowledgment of a flaw in the original proof. Result: authoritative
correction, but not a standalone lower-bound counterexample.

## Route 3 — independent primary sources

Commands used to retrieve the sources:

`orx paper 1903.08568 --full`

`orx paper 1912.02365 --full`

Executable audit:

`python .openresearch/artifacts/claim_4/route_3_primary_sources.py`

Vempala and Wibisono's ULA theorem supports the paper's inner KL upper-bound
shape. Arjevani et al. prove an `Omega(epsilon^-4)` bounded-variance stochastic
first-order lower bound. The two results do not automatically multiply for
Algorithm 3: a faithful entropy-DRO direct-product embedding and proof that
the inner work is unavoidable at every hard outer query are missing.

## Route 4 — dedicated falsification

Command:

`python .openresearch/artifacts/claim_4/route_4_falsification.py`

An exact Algorithm 3 Gaussian family was calibrated without formula-derived
horizons. It satisfies all four assumptions, uses a one-step ULA update, and
its optimized total work stays below `epsilon^-4`; therefore it is not a
counterexample. The route intentionally exits 1 with
`FALSIFICATION_NOT_ESTABLISHED`.

## Result

All four routes are durable and machine-checked. None supplies the missing
assumption-satisfying lower bound. The honest verdict is **BLOCKED**, not
FALSIFIED. The negative control substitutes the corrected outer exponent and
must reject the v1 exponent arithmetic.

The fixed cumulative command remains:

`uv run --frozen --no-dev python -m reproduction.run_all`
