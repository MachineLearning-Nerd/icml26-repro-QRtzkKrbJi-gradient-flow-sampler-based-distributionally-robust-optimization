"""Run the immutable baseline audit and every accepted claim verifier.

This is the fixed entrypoint inherited by every OpenResearch experiment node.
Each child may add a claim verifier, but may not change this command.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = (
    ROOT
    / "historical"
    / "judged_space_735012f52396955c5734e8fc568adfdf2abda757"
)
VERDICT_PATH = ROOT / "sources" / "judge" / "verdict.json"
SOURCE_MANIFEST = ROOT / "sources" / "paper" / "source_manifest.json"
ARTIFACTS = ROOT / ".openresearch" / "artifacts"
FIXED_COMMAND = "uv run --frozen --no-dev python -m reproduction.run_all"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_sha() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def validate_historical_manifest() -> dict[str, object]:
    manifest_path = HISTORICAL / "manifest.sha256"
    checked = 0
    mismatches: list[str] = []
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        target = HISTORICAL / relative.removeprefix("./")
        if not target.is_file():
            mismatches.append(f"missing:{relative}")
        elif sha256(target) != expected:
            mismatches.append(f"hash:{relative}")
        checked += 1
    if mismatches:
        raise AssertionError(f"historical manifest mismatch: {mismatches}")
    return {
        "checked_files": checked,
        "manifest_sha256": sha256(manifest_path),
        "mismatches": mismatches,
    }


def validate_live_verdict_snapshot() -> dict[str, object]:
    rows = json.loads(VERDICT_PATH.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 1:
        raise AssertionError("verdict snapshot must contain exactly one filtered row")
    row = rows[0]
    if row["space_id"] != "DineshAI/QRtzkKrbJi":
        raise AssertionError("verdict snapshot selected by a field other than space_id")
    if row["sha"] != "735012f52396955c5734e8fc568adfdf2abda757":
        raise AssertionError("verdict snapshot is not the exact judged revision")
    points = {"toy": 1, "inconclusive": 0}
    score = sum(points.get(item["verdict"], 0) for item in row["claims"])
    if score != 4:
        raise AssertionError(f"expected historical score 4, computed {score}")
    return {
        "space_id": row["space_id"],
        "judged_sha": row["sha"],
        "judged_at": row["judged_at"],
        "computed_points": score,
        "possible_points": 12,
        "snapshot_sha256": sha256(VERDICT_PATH),
    }


def run_claim_verifiers() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for verifier in sorted(ARTIFACTS.glob("claim_*/verifier.py")):
        started = time.perf_counter()
        completed = subprocess.run(
            [sys.executable, str(verifier)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        record = {
            "verifier": verifier.relative_to(ROOT).as_posix(),
            "exit_code": completed.returncode,
            "runtime_s": round(time.perf_counter() - started, 6),
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        results.append(record)
        print(f"\n--- {record['verifier']} ---")
        print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        if completed.returncode != 0:
            raise RuntimeError(
                f"claim verifier failed: {record['verifier']} "
                f"(exit {completed.returncode})"
            )
    return results


def main() -> int:
    started = time.perf_counter()
    source_manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    historical = validate_historical_manifest()
    verdict = validate_live_verdict_snapshot()
    claims = run_claim_verifiers()
    summary = {
        "schema_version": 1,
        "campaign_status": "BASELINE" if not claims else "CLAIM_EVIDENCE",
        "fixed_command": FIXED_COMMAND,
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpu_allocation_reported_by_os": os.cpu_count(),
        "local_core_use_contract": 1,
        "historical": historical,
        "live_verdict_snapshot": verdict,
        "paper_contract_version": source_manifest["judged_contract"]["version"],
        "paper_current_version": source_manifest["current_source"]["version"],
        "claim_verifiers": claims,
        "runtime_s": round(time.perf_counter() - started, 6),
    }
    print("\n=== GFS-DRO CUMULATIVE EVIDENCE SUMMARY ===")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

