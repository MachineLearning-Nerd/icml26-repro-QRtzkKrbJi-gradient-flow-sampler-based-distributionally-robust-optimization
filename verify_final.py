"""Verify the final local shape of the normalized repository."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_REPOSITORY = (
    "MachineLearning-Nerd/"
    "icml26-gradient-flow-sampler-distributionally-robust-optimization"
)
EXPECTED_REMOTE = "https://github.com/" + EXPECTED_REPOSITORY
EXPECTED_IDENTITY = (
    "MachineLearning-Nerd",
    "MachineLearning-Nerd@users.noreply.github.com",
)
EXPECTED_BRANCHES = {
    "main",
    "baseline/judged-4-12",
    "audit/claim-1-algorithm-conformance",
    "audit/claim-2-necessary-time",
    "audit/claim-3-outer-rate",
    "audit/claim-4-complexity",
    "audit/claim-5-figure-6",
    "audit/claim-6-half-bridge",
    "release/evaluator-visible",
}
EXPECTED_VERDICTS = {
    "C1": ("VERIFIED_HIGH", "VERIFIED"),
    "C2": ("FALSIFIED_HIGH", "FALSIFIED"),
    "C3": ("FALSIFIED_HIGH", "FALSIFIED"),
    "C4": ("BLOCKED_LOW", "BLOCKED"),
    "C5": ("FALSIFIED_MEDIUM", "FALSIFIED"),
    "C6": ("VERIFIED_HIGH", "VERIFIED"),
}
EXPECTED_ARTIFACTS = {
    "paper_2510.25956v1.pdf": (
        "796d3cb25e2a9062ab4e81201daa7837c4bf615399063b0ed439c9e17e6db8d6"
    ),
    "paper_2510.25956v3.pdf": (
        "88720453447d8affcefd3e63097c52f512d5b275766ba3e73dff9af2ca1c0f8f"
    ),
    "source/arxiv/2510.25956v1.tar": (
        "35a471bd60c11517db90b8e337064019c5a07faa621718aeca9800d425604488"
    ),
}


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def load(relative: str) -> object:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_file(relative: str) -> Path:
    path = ROOT / relative
    if not path.is_file():
        raise AssertionError(f"missing required file: {relative}")
    return path


def verify_release_manifest(relative_root: str) -> int:
    root = ROOT / relative_root
    allowlist_path = root / "upload_allowlist.txt"
    manifest_path = root / "manifest.sha256"
    paths = allowlist_path.read_text(encoding="utf-8").splitlines()
    if paths != sorted(set(paths)):
        raise AssertionError(f"{relative_root} allowlist is not sorted and unique")
    manifest: dict[str, str] = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        manifest[relative.removeprefix("./")] = expected
    if set(manifest) != set(paths) - {"manifest.sha256"}:
        raise AssertionError(f"{relative_root} manifest and allowlist differ")
    for relative in paths:
        target = root / relative
        if not target.is_file():
            raise AssertionError(f"missing allowlisted file: {relative_root}/{relative}")
        if relative != "manifest.sha256" and sha256(target) != manifest[relative]:
            raise AssertionError(f"manifest mismatch: {relative_root}/{relative}")
    return len(manifest)


def verify_claims() -> int:
    document = load("claims.json")
    if document["overall_status"] != "MIXED_RESULTS":
        raise AssertionError("unexpected overall claim status")
    if document["evidence_release_gate"] != "PASSED":
        raise AssertionError("evidence release gate is not passed")
    claims = {claim["id"]: claim for claim in document["claims"]}
    if set(claims) != set(EXPECTED_VERDICTS):
        raise AssertionError("claim set changed")
    for claim_id, (status, verdict) in EXPECTED_VERDICTS.items():
        claim = claims[claim_id]
        if claim["status"] != status:
            raise AssertionError(f"{claim_id} status changed")
        if not claim["producer"] or not claim["limitation"]:
            raise AssertionError(f"{claim_id} lacks production or scope text")
        for evidence in claim["evidence"]:
            require_file(evidence)
        contract = load(
            f"published_space/evidence/claim_{claim_id[1:]}/claim_contract.json"
        )
        verdict_key = {
            "C4": "verdict_after_routes",
            "C5": "verdict_if_checker_passes",
        }.get(claim_id, "verdict_if_all_pass")
        if contract[verdict_key] != verdict:
            raise AssertionError(f"{claim_id} contract verdict changed")
    return len(claims)


def verify_sources() -> None:
    source = load("sources/paper/source_manifest.json")
    judged = source["judged_contract"]
    current = source["current_source"]
    if judged["version"] != "2510.25956v1":
        raise AssertionError("judged paper version changed")
    if current["version"] != "2510.25956v3":
        raise AssertionError("current paper version changed")
    if judged["pdf_sha256"] != EXPECTED_ARTIFACTS["paper_2510.25956v1.pdf"]:
        raise AssertionError("source manifest v1 hash changed")
    if current["pdf_sha256"] != EXPECTED_ARTIFACTS["paper_2510.25956v3.pdf"]:
        raise AssertionError("source manifest v3 hash changed")
    verdict = load("sources/judge/verdict.json")
    if len(verdict) != 1 or verdict[0]["sha"] != (
        "735012f52396955c5734e8fc568adfdf2abda757"
    ):
        raise AssertionError("judged verdict snapshot changed")
    score = sum(
        {"toy": 1, "inconclusive": 0}[claim["verdict"]]
        for claim in verdict[0]["claims"]
    )
    if score != 4:
        raise AssertionError(f"historical score changed: {score}")


def normalize_remote(url: str) -> str:
    if url.startswith("git@github.com:"):
        url = "https://github.com/" + url.removeprefix("git@github.com:")
    return url.rstrip("/").removesuffix(".git")


def verify_git_state() -> tuple[int, int]:
    if git("branch", "--show-current") != "main":
        raise AssertionError("current branch is not main")
    branches = {
        line for line in git("branch", "--format=%(refname:short)").splitlines() if line
    }
    if branches != EXPECTED_BRANCHES:
        raise AssertionError(f"unexpected local branches: {sorted(branches)}")
    remote_refs = git(
        "for-each-ref",
        "--format=%(refname:short)",
        "refs/remotes/origin",
    ).splitlines()
    if any("/orx/" in ref or ref.endswith("/master") for ref in remote_refs):
        raise AssertionError("legacy remote branch remains")
    if git("status", "--porcelain"):
        raise AssertionError("worktree is not clean")
    remote = normalize_remote(git("config", "--get", "remote.origin.url"))
    if remote != EXPECTED_REMOTE:
        raise AssertionError(f"unexpected origin: {remote}")
    identities = git(
        "log",
        "--all",
        "--format=%an%x09%ae%x09%cn%x09%ce",
    ).splitlines()
    for row in identities:
        author_name, author_email, committer_name, committer_email = row.split(
            "\t"
        )
        if (author_name, author_email) != EXPECTED_IDENTITY or (
            committer_name,
            committer_email,
        ) != EXPECTED_IDENTITY:
            raise AssertionError(f"non-canonical commit identity: {row}")
    if "co-authored-by:" in git("log", "--all", "--format=%B").lower():
        raise AssertionError("co-author trailer remains")
    return len(branches), int(git("rev-list", "--all", "--count"))


def main() -> int:
    manifest = load("EVIDENCE_MANIFEST.json")
    required = set(manifest["required_files"]) | {
        "EVIDENCE_MANIFEST.json",
        "verify_final.py",
    }
    for relative in required:
        require_file(relative)
    for relative, expected in EXPECTED_ARTIFACTS.items():
        if sha256(require_file(relative)) != expected:
            raise AssertionError(f"artifact hash changed: {relative}")
    if manifest["repository"] != EXPECTED_REPOSITORY:
        raise AssertionError("repository identity in evidence manifest changed")
    claims = verify_claims()
    verify_sources()
    published_entries = verify_release_manifest("published_space")
    candidate_entries = verify_release_manifest("space_candidate")
    branches, commits = verify_git_state()
    required_headings = (
        "## What the paper does",
        "## How each claim is produced",
        "## Citation",
        "## Thank you",
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if any(heading not in readme for heading in required_headings):
        raise AssertionError("README is missing a required paper-first section")
    print(
        "VERIFY_FINAL_PASS: "
        f"{len(required)} required files, {branches} branches, "
        f"{claims} claim contracts, {commits} reachable commits, "
        f"{published_entries + candidate_entries} release-manifest entries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
