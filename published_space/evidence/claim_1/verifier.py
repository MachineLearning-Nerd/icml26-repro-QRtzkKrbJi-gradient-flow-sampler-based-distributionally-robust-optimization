"""Fail-closed verifier for the six-algorithm framework claim."""

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
        raise AssertionError("child checker emitted no JSON")
    return json.loads(lines[-1])


def main() -> int:
    checker_process = run("independent_checker.py")
    if checker_process.returncode != 0:
        raise AssertionError(checker_process.stderr)
    checker = parse(checker_process)
    recorded_checker = json.loads(
        (HERE / "independent_checker_output.json").read_text(encoding="utf-8")
    )
    if checker != recorded_checker:
        raise AssertionError("independent checker output changed")
    if checker["status"] != "PASS":
        raise AssertionError("independent checker did not pass")
    if checker["algorithms_checked"] != [1, 2, 3, 4, 5, 6]:
        raise AssertionError("not all six algorithms were checked")

    transitions = checker["transition_checks"]
    if transitions["wgf_transition_max_error"] >= 1e-14:
        raise AssertionError("WGF transition mismatch")
    if transitions["svg_transition_max_error"] >= 1e-14:
        raise AssertionError("SVGD transition mismatch")
    if transitions["wfr_weight_sum_error"] >= 1e-14:
        raise AssertionError("WFR mass invariant failed")
    if not 0.1 < transitions["rgo_acceptance_rate"] < 0.999:
        raise AssertionError("RGO rejection check is vacuous")
    if transitions["rgo_maximum_log_acceptance"] > 1e-10:
        raise AssertionError("RGO envelope is invalid")

    control_process = run("negative_control.py")
    control = parse(control_process)
    if control_process.returncode != 1:
        raise AssertionError("negative control did not exit 1")
    recorded_control = json.loads(
        (HERE / "negative_control_output.json").read_text(encoding="utf-8")
    )
    if {"exit_code": control_process.returncode, **control} != recorded_control:
        raise AssertionError("recorded negative-control output changed")
    if (
        control["status"] != "REJECTED_AS_EXPECTED"
        or control["defect_count"] != 6
    ):
        raise AssertionError("not all six injected defects were rejected")

    raw = json.loads((HERE / "raw_results.json").read_text(encoding="utf-8"))
    if raw["verdict"] != "VERIFIED":
        raise AssertionError("raw verdict changed")
    if raw["algorithm_summary"]["algorithm_4_birth_death_replacements"] <= 0:
        raise AssertionError("WFR birth-death was not exercised")
    if raw["algorithm_summary"]["algorithm_6_rejected_proposals"] <= 0:
        raise AssertionError("RGO rejection was not exercised")

    print(
        json.dumps(
            {
                "claim_id": 1,
                "verdict": "VERIFIED",
                "algorithms_checked": checker["algorithms_checked"],
                "dimension": checker["dimension"],
                "wgf_transition_max_error": transitions[
                    "wgf_transition_max_error"
                ],
                "wfr_birth_death_events": transitions[
                    "wfr_birth_death_events"
                ],
                "svg_transition_max_error": transitions[
                    "svg_transition_max_error"
                ],
                "rgo_acceptance_rate": transitions[
                    "rgo_acceptance_rate"
                ],
                "negative_control_exit_code": control_process.returncode,
                "defects_rejected": control["defect_count"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
