"""Fail-closed evaluator-visible, historical-subset, and security audit."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import argparse
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "space_candidate"
JUDGED = (
    ROOT
    / "historical"
    / "judged_space_735012f52396955c5734e8fc568adfdf2abda757"
)
PROTECTED = (
    CANDIDATE
    / "historical"
    / "judged_space_735012f52396955c5734e8fc568adfdf2abda757"
)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SECRET_PATTERNS = (
    re.compile(r"hf_[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"][^'\"]+"),
)
EXPECTED_VERDICTS = {
    1: "VERIFIED",
    2: "FALSIFIED",
    3: "FALSIFIED",
    4: "BLOCKED",
    5: "FALSIFIED",
    6: "VERIFIED",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def flatten_nodes(node: dict[str, object]) -> list[dict[str, object]]:
    nodes = [node]
    for child in node.get("children", []):
        nodes.extend(flatten_nodes(child))
    return nodes


def resolve_link(
    source: Path, target: str, slug_paths: dict[str, Path]
) -> Path | None:
    target = target.strip()
    if target.startswith(("#/", "#")):
        slug = target.removeprefix("#/")
        if slug not in slug_paths:
            raise AssertionError(f"unknown navigation slug {target} in {source}")
        return slug_paths[slug]
    if target.startswith(("http://", "https://", "mailto:")):
        return None
    relative = target.split("#", 1)[0].split("?", 1)[0]
    if not relative:
        return None
    resolved = (source.parent / relative).resolve()
    resolved.relative_to(CANDIDATE.resolve())
    if not resolved.is_file():
        raise AssertionError(f"broken local link {target} in {source}")
    return resolved


def evaluator_traversal() -> dict[str, object]:
    logbook = json.loads((CANDIDATE / "logbook.json").read_text(encoding="utf-8"))
    nodes = flatten_nodes(logbook["root"])
    slug_paths = {
        str(node["slug"]): CANDIDATE / str(node["file"]) for node in nodes
    }
    queue = deque([CANDIDATE / "README.md", slug_paths[str(logbook["root"]["slug"])]])
    opened: set[Path] = set()
    discovered: set[Path] = set(queue)
    while queue:
        source = queue.popleft()
        if source in opened:
            continue
        if not source.is_file():
            raise AssertionError(f"missing traversal file {source}")
        opened.add(source)
        if source.suffix != ".md":
            continue
        text = source.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            resolved = resolve_link(source, target, slug_paths)
            if resolved is None:
                continue
            discovered.add(resolved)
            relative_resolved = resolved.relative_to(CANDIDATE)
            if (
                resolved.suffix == ".md"
                and relative_resolved.parts
                and relative_resolved.parts[0] == "pages"
                and resolved not in opened
            ):
                queue.append(resolved)

    required_pages = {
        CANDIDATE / "pages/current/index.md",
        CANDIDATE / "pages/current/verification.md",
        CANDIDATE / "pages/current/visibility.md",
        CANDIDATE / "pages/current/report.md",
        CANDIDATE / "pages/current/release.md",
        CANDIDATE / "pages/current/red-team.md",
        CANDIDATE / "pages/current/historical.md",
    }
    required_pages.update(
        CANDIDATE / f"pages/current/claims/claim-{claim_id}.md"
        for claim_id in EXPECTED_VERDICTS
    )
    missing_pages = sorted(
        path.relative_to(CANDIDATE).as_posix()
        for path in required_pages
        if path not in opened
    )
    if missing_pages:
        raise AssertionError(f"canonical traversal missed pages: {missing_pages}")

    common_tokens = (
        "uv run --frozen --no-dev python -m reproduction.run_all",
        "uv.lock",
        "313c0a3d56185c5f1a74d2d6945e0dafd6445bf7",
        "seed",
        "cpu-upgrade",
        "64 logical CPUs",
        "runtime",
        "Raw:",
        "control",
    )
    for claim_id, verdict in EXPECTED_VERDICTS.items():
        page = CANDIDATE / f"pages/current/claims/claim-{claim_id}.md"
        text = page.read_text(encoding="utf-8")
        normalized_text = " ".join(text.split()).lower()
        required_tokens = common_tokens + (verdict, "confidence")
        absent = [
            token
            for token in required_tokens
            if " ".join(token.split()).lower() not in normalized_text
        ]
        if absent:
            raise AssertionError(f"Claim {claim_id} missing tokens: {absent}")
        contract = CANDIDATE / f"evidence/claim_{claim_id}/claim_contract.json"
        source = CANDIDATE / f"evidence/claim_{claim_id}/source_audit.md"
        verifier = CANDIDATE / f"evidence/claim_{claim_id}/verifier.py"
        for path in (contract, source, verifier):
            if path not in discovered:
                raise AssertionError(
                    f"Claim {claim_id} evidence is not evaluator-reachable: "
                    f"{path.relative_to(CANDIDATE)}"
                )

    visibility = (CANDIDATE / "pages/current/visibility.md").read_text(
        encoding="utf-8"
    )
    expected_columns = (
        "| Claim | Canonical page | Code visible | Data inline | Raw link | "
        "Checker | Control | Exact claim tested | Reviewer verdict |"
    )
    if expected_columns not in visibility:
        raise AssertionError("visibility matrix columns changed")
    if visibility.count("| [Claim ") != 6:
        raise AssertionError("visibility matrix must contain exactly six claim rows")
    return {
        "opened_files": sorted(
            path.relative_to(CANDIDATE).as_posix() for path in opened
        ),
        "discovered_local_files": len(discovered),
        "missing_pages": missing_pages,
    }


def historical_subset() -> dict[str, object]:
    mappings = []
    for line in (JUDGED / "manifest.sha256").read_text(encoding="utf-8").splitlines():
        expected, raw_relative = line.split("  ", 1)
        relative = raw_relative.removeprefix("./")
        same_path = CANDIDATE / relative
        protected_path = PROTECTED / relative
        if same_path.is_file() and sha256(same_path) == expected:
            location = relative
        elif protected_path.is_file() and sha256(protected_path) == expected:
            location = protected_path.relative_to(CANDIDATE).as_posix()
        else:
            raise AssertionError(f"judged file not preserved: {relative}")
        mappings.append({"judged_path": relative, "candidate_path": location})
    if len(mappings) != 17:
        raise AssertionError(f"expected 17 judged files, got {len(mappings)}")
    return {"judged_files": len(mappings), "mappings": mappings}


def manifest_and_security() -> dict[str, object]:
    allowlist_path = CANDIDATE / "upload_allowlist.txt"
    manifest_path = CANDIDATE / "manifest.sha256"
    paths = allowlist_path.read_text(encoding="utf-8").splitlines()
    if paths != sorted(set(paths)):
        raise AssertionError("upload allowlist is not sorted and unique")
    if "manifest.sha256" not in paths or "upload_allowlist.txt" not in paths:
        raise AssertionError("allowlist must contain itself and the manifest")
    manifest = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        expected, raw_relative = line.split("  ", 1)
        manifest[raw_relative.removeprefix("./")] = expected
    if set(manifest) != set(paths) - {"manifest.sha256"}:
        raise AssertionError("manifest paths do not match the exact allowlist")

    scanned = 0
    for relative in paths:
        target = CANDIDATE / relative
        if not target.is_file():
            raise AssertionError(f"allowlisted file missing: {relative}")
        text = target.read_text(encoding="utf-8")
        if relative != "manifest.sha256" and sha256(target) != manifest[relative]:
            raise AssertionError(f"manifest hash mismatch: {relative}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                raise AssertionError(f"possible secret in {relative}")
        scanned += 1
    return {
        "allowlisted_text_files": len(paths),
        "manifest_entries": len(manifest),
        "secret_scan_files": scanned,
        "secret_matches": 0,
    }


def run_candidate_verifier() -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "reproduction/run_all.py"],
        cwd=CANDIDATE,
        capture_output=True,
        text=True,
    )
    print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="")
    if completed.returncode != 0:
        raise RuntimeError(
            f"evaluator-visible verifier failed with exit {completed.returncode}"
        )
    if '"status": "PASS"' not in completed.stdout:
        raise AssertionError("candidate verifier emitted no PASS summary")
    return {"exit_code": completed.returncode, "status": "PASS"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--structure-only", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    args = parser.parse_args()
    if args.candidate_dir is not None:
        global CANDIDATE, PROTECTED
        CANDIDATE = args.candidate_dir.resolve()
        PROTECTED = (
            CANDIDATE
            / "historical"
            / "judged_space_735012f52396955c5734e8fc568adfdf2abda757"
        )
    structure_only = args.structure_only
    candidate_verifier = (
        {"status": "SKIPPED_FOR_SHORT_LOCAL_STRUCTURE_AUDIT"}
        if structure_only
        else run_candidate_verifier()
    )
    traversal = evaluator_traversal()
    subset = historical_subset()
    security = manifest_and_security()
    summary = {
        "candidate_verifier": candidate_verifier,
        "evaluator_traversal": traversal,
        "historical_subset": subset,
        "manifest_and_security": security,
        "status": "PASS",
    }
    print("\n=== EVALUATOR-VISIBLE RELEASE AUDIT ===")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
