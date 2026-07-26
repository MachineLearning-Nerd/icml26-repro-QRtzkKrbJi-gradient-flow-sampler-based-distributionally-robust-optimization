"""Fail-closed cumulative verifier for Claim 6."""

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


def parse_output(completed: subprocess.CompletedProcess[str]) -> dict[str, object]:
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise AssertionError("checker emitted no machine-readable output")
    return json.loads(lines[-1])


def main() -> int:
    certificate_process = run("certificate.py")
    if certificate_process.returncode != 0:
        raise AssertionError(certificate_process.stderr)
    certificate = parse_output(certificate_process)
    if certificate["symbolic_integrand_residual"] != "0":
        raise AssertionError("symbolic certificate is not exact")

    checker_process = run("independent_checker.py")
    if checker_process.returncode != 0:
        raise AssertionError(checker_process.stderr)
    checker = parse_output(checker_process)
    if checker["status"] != "PASS" or checker["case_count"] != 4:
        raise AssertionError("independent continuous checker did not pass")
    recorded_checker = json.loads(
        (HERE / "independent_checker_output.json").read_text(encoding="utf-8")
    )
    checker_summary = {
        "case_count": checker["case_count"],
        "exit_code": checker_process.returncode,
        "max_identity_residual": checker["max_identity_residual"],
        "max_mass_error": checker["max_mass_error"],
        "max_raw_generator_delta": checker["max_raw_generator_delta"],
        "minimum_perturbation_objective_gap": checker[
            "minimum_perturbation_objective_gap"
        ],
        "minimum_proposal_kl": checker["minimum_proposal_kl"],
        "status": checker["status"],
    }
    if checker_summary != recorded_checker:
        raise AssertionError("recorded independent-checker output changed")

    control_process = run("negative_control.py")
    control = parse_output(control_process)
    if control_process.returncode != 1:
        raise AssertionError("wrong-temperature control did not exit 1")
    if control["status"] != "REJECTED_AS_EXPECTED":
        raise AssertionError("wrong-temperature control failed for another reason")
    recorded_control = json.loads(
        (HERE / "negative_control_output.json").read_text(encoding="utf-8")
    )
    if recorded_control != {"exit_code": 1, **control}:
        raise AssertionError("recorded negative-control output changed")

    result = {
        "claim_id": 6,
        "verdict": "VERIFIED",
        "certificate": {
            "exit_code": certificate_process.returncode,
            "symbolic_integrand_residual": certificate[
                "symbolic_integrand_residual"
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
            "reason": control["reason"],
            "stationarity_span": control["stationarity_span"],
        },
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
