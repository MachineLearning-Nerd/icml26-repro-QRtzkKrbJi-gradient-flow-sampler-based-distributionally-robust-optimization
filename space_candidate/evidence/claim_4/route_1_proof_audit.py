"""Route 1: reconstruct the exponent dependency of the v1 proof."""

from __future__ import annotations

import json


def main() -> int:
    v1_outer = 2
    inner = 2
    corrected_outer = 4
    v1_total = v1_outer + inner
    corrected_total = corrected_outer + inner
    if v1_total != 4 or corrected_total != 6:
        raise AssertionError("complexity exponent arithmetic changed")
    output = {
        "route": 1,
        "status": "INCONCLUSIVE_FOR_EXACT_CLAIM",
        "v1_outer_exponent": v1_outer,
        "inner_exponent": inner,
        "v1_total_exponent": v1_total,
        "corrected_outer_exponent": corrected_outer,
        "corrected_total_exponent": corrected_total,
        "finding": (
            "the v1 proof depends on the falsified Claim 3 outer rate"
        ),
        "why_not_falsification": (
            "invalid proof dependency is not a lower-bound counterexample"
        ),
    }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
