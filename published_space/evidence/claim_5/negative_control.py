"""A dominance-satisfying synthetic control must not yield a counterexample."""

from __future__ import annotations

import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from vector_extractor import indexed_rows  # noqa: E402


def main() -> int:
    rows = indexed_rows()
    violations = 0
    for epsilon in ("0.2", "0.02", "0.002"):
        for proposed in ("WGF", "WFR"):
            for baseline in ("Dual", "WRM"):
                for point in range(1, 11):
                    baseline_error = float(
                        rows[(epsilon, baseline, point)][
                            "test_error_percent"
                        ]
                    )
                    synthetic_proposed_error = min(
                        float(
                            rows[(epsilon, "Dual", point)][
                                "test_error_percent"
                            ]
                        ),
                        float(
                            rows[(epsilon, "WRM", point)][
                                "test_error_percent"
                            ]
                        ),
                    ) - 1.0
                    if synthetic_proposed_error > baseline_error:
                        violations += 1
    if violations:
        print(
            json.dumps(
                {
                    "status": "CONTROL_MALFUNCTION",
                    "violations": violations,
                },
                sort_keys=True,
            )
        )
        return 2
    print(
        json.dumps(
            {
                "status": "NO_COUNTEREXAMPLE_AS_EXPECTED",
                "violations": 0,
                "reason": "both proposed curves were placed one percentage point below the better baseline at every attacked setting",
            },
            sort_keys=True,
        )
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
