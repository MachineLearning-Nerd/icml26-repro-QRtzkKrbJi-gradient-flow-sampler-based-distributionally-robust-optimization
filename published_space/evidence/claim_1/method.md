# Claim 1 method

## Instance

The checker uses six deterministic nominal points in eight dimensions and the non-quadratic loss

`loss(theta,y) = theta dot y + 0.35 sum(log(2 cosh(y_j)))`.

Its sample Hessian is bounded by `0.35 I`. With `tau=0.8` and `epsilon=0.7`, every conditional negative potential is strongly convex, the conditional law is proper, and the RGO prerequisite `tau < 1/L` holds with margin.

## Implementation-led checks

`algorithms.py` implements each numbered algorithm separately. Trace counters expose the operations that define each pseudocode:

1. nominal draw, conditional gradient flow, output;
2. Algorithm-1 call and projected descent;
3. particle initialization, Gaussian draw, equation-(12) update, average outer gradient;
4. location update, Fisher-Rao mass update, normalization, exercised birth-death, weighted outer gradient;
5. deviated initialization, kernel pairs, score force, repulsion, transport, average outer gradient;
6. potential minimizer, Gaussian proposal, both accept and reject decisions, average outer gradient.

The independent checker also reconstructs a seeded WGF transition directly from equation (12), reconstructs a seeded SVGD transition independently from the score and kernel derivatives, verifies WFR mass conservation after birth-death, and confirms the RGO log envelope never exceeds zero. Its RGO acceptance rate must lie strictly between 0.1 and 0.999.

## Controls

The negative-control process injects six different defects: bypass Algorithm 1's flow, reverse Algorithm 2's descent direction, remove Algorithm 3's noise, remove Algorithm 4's reaction flow, reverse Algorithm 5's repulsion, and make Algorithm 6 accept every proposal. All six must be detected, then the control exits 1.

## Reproduction command

`uv run --frozen --no-dev python -m reproduction.run_all`

Environment: repository `.venv`, Python 3.12, exact `uv.lock`. Seeds are 101-106 and 310-314 for accepted checks; 401-404 for controls.
