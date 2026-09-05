"""Verify SHA-256 hashes before loading serialized model artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "results" / "artifact_sha256.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    expected = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failed = False
    for relative, expected_hash in expected.items():
        path = ROOT / relative
        actual_hash = sha256(path)
        status = "PASS" if actual_hash == expected_hash else "FAIL"
        print(f"{status}  {relative}")
        failed |= status == "FAIL"
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
