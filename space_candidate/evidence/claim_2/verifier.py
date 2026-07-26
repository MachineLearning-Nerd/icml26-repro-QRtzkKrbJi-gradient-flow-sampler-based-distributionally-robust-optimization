"""Fail-closed verifier for the literal necessary-time claim."""

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


def output(completed: subprocess.CompletedProcess[str]) -> dict[str, object]:
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise AssertionError("sub-check emitted no JSON")
    return json.loads(lines[-1])


def main() -> int:
    certificate_process = run("certificate.py")
    if certificate_process.returncode != 0:
        raise AssertionError(certificate_process.stderr)
    certificate = output(certificate_process)
    if certificate["status"] != "PASS":
        raise AssertionError("symbolic assumptions did not pass")

    checker_process = run("independent_checker.py")
    if checker_process.returncode != 0:
        raise AssertionError(checker_process.stderr)
    checker = output(checker_process)
    if checker["status"] != "PASS":
        raise AssertionError("continuous checker did not pass")
    checker_summary = {
        "all_measured_first_hits": checker["all_measured_first_hits"],
        "exit_code": checker_process.returncode,
        "gradient_error_at_zero": checker["gradient_error_at_zero"],
        "initial_to_target_w2": checker["initial_to_target_w2"],
        "largest_claimed_scale": checker["largest_claimed_scale"],
        "smallest_epsilon": checker["smallest_epsilon"],
        "status": checker["status"],
        "tolerance_count": checker["tolerance_count"],
    }
    recorded_checker = json.loads(
        (HERE / "independent_checker_output.json").read_text(encoding="utf-8")
    )
    if checker_summary != recorded_checker:
        raise AssertionError("recorded independent-checker output changed")

    control_process = run("negative_control.py")
    control = output(control_process)
    if control_process.returncode != 1:
        raise AssertionError("asymmetric control did not exit 1")
    if control["status"] != "REJECTED_AS_EXPECTED":
        raise AssertionError("control was rejected for an unintended reason")
    recorded_control = json.loads(
        (HERE / "negative_control_output.json").read_text(encoding="utf-8")
    )
    if recorded_control != {"exit_code": 1, **control}:
        raise AssertionError("recorded control output changed")

    result = {
        "claim_id": 2,
        "verdict": "FALSIFIED",
        "literal_quantifier": "necessary lower time for every admissible case",
        "certificate": {
            "exit_code": certificate_process.returncode,
            "loss_smoothness": certificate["loss_smoothness"],
            "gradient_observable_lipschitz": certificate[
                "gradient_observable_lipschitz"
            ],
            "strong_convexity": certificate["strong_convexity"],
            "lambda_pl": certificate["lambda_pl"],
            "required_time_for_every_positive_epsilon": certificate[
                "required_time_for_every_positive_epsilon"
            ],
        },
        "independent_checker": {
            key: checker_summary[key]
            for key in checker_summary
            if key != "status"
        },
        "negative_control": {
            "exit_code": control_process.returncode,
            "status": control["status"],
            "initial_gradient_error": control["initial_gradient_error"],
            "positive_first_hit_time": control["positive_first_hit_time"],
        },
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
