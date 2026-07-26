# Claim 5 method

## Non-circular route

No sample size, tolerance, attack radius, or comparison point was selected from an expected formula. The checker parses all 132 relevant points from the four exact vector curves (WGF, WFR, Dual, WRM), calibrates both axes from independent tick coordinates, and exhaustively tests all 120 attacked proposed-versus-baseline comparisons.

The primary certificate is not raster digitization: `official_vector_paths.json` preserves the exact `M/L` path coordinates from the authors' three committed result PDFs. `vector_extractor.py` converts them to perturbation, test error, and robust accuracy using the recorded axis calibration.

## Independent checks

`independent_checker.py` requires:

- 11 points for each of four methods at each of three entropy values;
- every reconstructed x value to agree with `0.008 * index` within `2e-6`;
- every y value to be a valid percentage;
- at least one nonzero contradiction for WGF and separately for WFR;
- each primary counterexample to exceed two percentage points, far beyond vector-coordinate precision.

It finds 20 WGF and 29 WFR violations across the nonzero radii and both baselines.

## Negative control

The control replaces both proposed errors with a value one percentage point below the better baseline at every attacked setting. It confirms there are zero violations and exits 1 with `NO_COUNTEREXAMPLE_AS_EXPECTED`; this prevents a checker that falsifies every input from passing.

## Reproduction command

`uv run --frozen --no-dev python -m reproduction.run_all`

The extraction is deterministic and has no random seed. The locked Python environment and exact source hashes are part of the cumulative verifier.
