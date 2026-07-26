"""Fail-closed verifier for the exact Figure 6 falsification."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def run(name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HERE / name)],
        cwd=HERE,
        capture_output=True,
        text=True,
    )


def parse(completed: subprocess.CompletedProcess[str]) -> dict[str, object]:
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise AssertionError("child process emitted no JSON")
    return json.loads(lines[-1])


def main() -> int:
    source = json.loads(
        (HERE / "official_vector_paths.json").read_text(encoding="utf-8")
    )
    if source["source"]["git_sha"] != (
        "6f9fb5c9e432b5cc6ad62916b36f102984b4d076"
    ):
        raise AssertionError("official result revision changed")
    expected_hashes = {
        "0.2": "0f266bdbdf96fdb1c1c7e73256e17d7cb015d69ff307e93b8639d6bcf0ec5a4f",
        "0.02": "d3404bd83f2d4b563eeff2faa6d597529a058ef542abfb31ab5aeabc2c5c0dc4",
        "0.002": "ed08b8b03c9da7bb23278a50238858cd73166d68f1b35062adb4e8da570dba36",
    }
    for epsilon, expected in expected_hashes.items():
        if source["source"]["files"][epsilon]["sha256"] != expected:
            raise AssertionError("official result PDF hash changed")

    checker_process = run("independent_checker.py")
    if checker_process.returncode != 0:
        raise AssertionError(checker_process.stderr)
    checker = parse(checker_process)
    recorded_checker = json.loads(
        (HERE / "independent_checker_output.json").read_text(encoding="utf-8")
    )
    if checker != recorded_checker:
        raise AssertionError("recorded independent-checker output changed")
    if checker["verdict"] != "FALSIFIED":
        raise AssertionError("strict quantifier was not falsified")
    if checker["all_settings_quantifier_holds"] is not False:
        raise AssertionError("universal claim unexpectedly holds")
    for method in ("WGF", "WFR"):
        if checker["violation_counts"][method] <= 0:
            raise AssertionError(f"no counterexample for {method}")
        if (
            checker["strongest_counterexamples"][method][
                "accuracy_deficit_percentage_points"
            ]
            <= 2.0
        ):
            raise AssertionError("counterexample margin is not robust")

    control_process = run("negative_control.py")
    control = parse(control_process)
    if control_process.returncode != 1:
        raise AssertionError("dominance-satisfying control did not exit 1")
    recorded_control = json.loads(
        (HERE / "negative_control_output.json").read_text(encoding="utf-8")
    )
    if {"exit_code": control_process.returncode, **control} != recorded_control:
        raise AssertionError("recorded negative-control output changed")
    if (
        control["status"] != "NO_COUNTEREXAMPLE_AS_EXPECTED"
        or control["violations"] != 0
    ):
        raise AssertionError("negative control failed for another reason")

    raw = json.loads(
        (HERE / "raw_counterexamples.json").read_text(encoding="utf-8")
    )
    for method in ("WGF", "WFR"):
        raw_margin = raw["accuracy_deficit_vs_wrm_percentage_points"][method]
        checked_margin = checker["strongest_counterexamples"][method][
            "accuracy_deficit_percentage_points"
        ]
        if abs(raw_margin - checked_margin) > 1e-12:
            raise AssertionError("inline counterexample differs from raw vector")

    print(
        json.dumps(
            {
                "claim_id": 5,
                "verdict": "FALSIFIED",
                "confidence": "MEDIUM",
                "source": "official full CIFAR-10 Figure 6 vector PDFs",
                "source_point_count": checker["source_point_count"],
                "nonzero_attack_points_per_curve": checker[
                    "tested_attack_point_count"
                ],
                "violation_counts": checker["violation_counts"],
                "strongest_counterexamples": checker[
                    "strongest_counterexamples"
                ],
                "negative_control_exit_code": control_process.returncode,
                "interpretation_risk": "paper prose says qualitative high degree; live judged claim asserts strict all-settings dominance",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
