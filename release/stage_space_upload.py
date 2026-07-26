"""Copy only manifest-verified text files into a fresh upload directory."""

from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "space_candidate"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    destination = args.destination.resolve()
    if not destination.is_dir() or any(destination.iterdir()):
        raise ValueError("destination must be an existing empty directory")

    paths = (CANDIDATE / "upload_allowlist.txt").read_text(
        encoding="utf-8"
    ).splitlines()
    manifest = {}
    for line in (CANDIDATE / "manifest.sha256").read_text(
        encoding="utf-8"
    ).splitlines():
        expected, raw_relative = line.split("  ", 1)
        manifest[raw_relative.removeprefix("./")] = expected

    copied = []
    for relative in paths:
        source = CANDIDATE / relative
        source.read_text(encoding="utf-8")
        if relative != "manifest.sha256" and sha256(source) != manifest[relative]:
            raise AssertionError(f"manifest mismatch before staging: {relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(relative)

    staged = sorted(
        path.relative_to(destination).as_posix()
        for path in destination.rglob("*")
        if path.is_file()
    )
    if staged != paths:
        raise AssertionError("staged tree differs from exact allowlist")
    print(f"staged {len(staged)} manifest-verified UTF-8 files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
