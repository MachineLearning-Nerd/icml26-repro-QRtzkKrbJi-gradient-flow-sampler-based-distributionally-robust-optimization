"""Build the exact text-only Space upload allowlist and SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "space_candidate"
ALLOWLIST_PATH = CANDIDATE / "upload_allowlist.txt"
MANIFEST_PATH = CANDIDATE / "manifest.sha256"
TEXT_SUFFIXES = {".json", ".lock", ".md", ".py", ".svg", ".txt"}
EXACT_FILES = {
    ".python-version",
    "README.md",
    "logbook.json",
    "pyproject.toml",
    "uv.lock",
}
PREFIXES = (
    "evidence/",
    "historical/judged_space_735012f52396955c5734e8fc568adfdf2abda757/",
    "pages/current/",
    "reproduction/",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def selected(relative: str, path: Path) -> bool:
    if relative in EXACT_FILES:
        return True
    if not relative.startswith(PREFIXES):
        return False
    return path.suffix in TEXT_SUFFIXES or path.name == ".python-version"


def main() -> int:
    mirrors = {
        ROOT / "reports/reproduction/report.md": (
            CANDIDATE / "pages/current/report.md"
        ),
        ROOT / "reports/reproduction/release_report.md": (
            CANDIDATE / "pages/current/release.md"
        ),
    }
    for source, target in mirrors.items():
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    for source in sorted((ROOT / "reports/reproduction/images").glob("*.svg")):
        target = CANDIDATE / "pages/current/images" / source.name
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    paths = sorted(
        path.relative_to(CANDIDATE).as_posix()
        for path in CANDIDATE.rglob("*")
        if path.is_file()
        and path not in {ALLOWLIST_PATH, MANIFEST_PATH}
        and selected(path.relative_to(CANDIDATE).as_posix(), path)
    )
    paths.extend(["manifest.sha256", "upload_allowlist.txt"])
    paths = sorted(set(paths))
    ALLOWLIST_PATH.write_text("\n".join(paths) + "\n", encoding="utf-8")

    entries = []
    for relative in paths:
        if relative == "manifest.sha256":
            continue
        target = CANDIDATE / relative
        target.read_text(encoding="utf-8")
        entries.append(f"{sha256(target)}  ./{relative}")
    MANIFEST_PATH.write_text("\n".join(entries) + "\n", encoding="utf-8")
    print(
        f"built text-only allowlist: {len(paths)} files; "
        f"manifest entries: {len(entries)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
