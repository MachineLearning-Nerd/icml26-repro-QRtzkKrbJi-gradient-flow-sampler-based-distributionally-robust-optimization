"""Fail-closed checker for the exact Figure 6 all-settings quantifier."""

from __future__ import annotations

import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from vector_extractor import extract_rows, indexed_rows  # noqa: E402


def main() -> int:
    rows = extract_rows()
    if len(rows) != 3 * 4 * 11:
        raise AssertionError("expected 132 vector points")
    index = indexed_rows()
    for epsilon in ("0.2", "0.02", "0.002"):
        for method in ("WGF", "WFR", "Dual", "WRM"):
            for point in range(11):
                row = index[(epsilon, method, point)]
                if abs(float(row["delta"]) - 0.008 * point) > 2e-6:
                    raise AssertionError("x-axis calibration mismatch")
                if not 0.0 <= float(row["test_error_percent"]) <= 100.0:
                    raise AssertionError("invalid plotted percentage")

    violations: list[dict[str, float | str]] = []
    counts = {"WGF": 0, "WFR": 0}
    for epsilon in ("0.2", "0.02", "0.002"):
        for proposed in ("WGF", "WFR"):
            for baseline in ("Dual", "WRM"):
                for point in range(1, 11):
                    method_row = index[(epsilon, proposed, point)]
                    baseline_row = index[(epsilon, baseline, point)]
                    error_margin = float(
                        method_row["test_error_percent"]
                    ) - float(baseline_row["test_error_percent"])
                    if error_margin > 0.0:
                        counts[proposed] += 1
                        violations.append(
                            {
                                "epsilon": epsilon,
                                "delta": round(0.008 * point, 3),
                                "proposed": proposed,
                                "baseline": baseline,
                                "proposed_error_percent": float(
                                    method_row["test_error_percent"]
                                ),
                                "baseline_error_percent": float(
                                    baseline_row["test_error_percent"]
                                ),
                                "accuracy_deficit_percentage_points": error_margin,
                            }
                        )

    if counts["WGF"] == 0 or counts["WFR"] == 0:
        raise AssertionError("strict all-settings claim was not contradicted for both methods")

    strongest: dict[str, dict[str, float | str]] = {}
    for proposed in ("WGF", "WFR"):
        strongest[proposed] = max(
            (item for item in violations if item["proposed"] == proposed),
            key=lambda item: float(item["accuracy_deficit_percentage_points"]),
        )

    required = {
        "WGF": {
            "epsilon": "0.2",
            "delta": 0.008,
            "baseline": "WRM",
        },
        "WFR": {
            "epsilon": "0.2",
            "delta": 0.008,
            "baseline": "WRM",
        },
    }
    for method, expected in required.items():
        for key, value in expected.items():
            if strongest[method][key] != value:
                raise AssertionError(f"unexpected strongest {method} counterexample")
        if float(strongest[method]["accuracy_deficit_percentage_points"]) <= 2.0:
            raise AssertionError("counterexample is too close to vector precision")

    result = {
        "status": "PASS",
        "verdict": "FALSIFIED",
        "source_point_count": len(rows),
        "tested_attack_point_count": 10,
        "epsilon_count": 3,
        "baseline_methods": ["Dual", "WRM"],
        "violation_counts": counts,
        "strongest_counterexamples": strongest,
        "all_settings_quantifier_holds": False,
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
