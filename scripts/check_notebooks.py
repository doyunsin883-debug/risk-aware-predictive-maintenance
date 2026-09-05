"""Check that every tracked notebook is valid JSON with code cells."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if len(notebooks) != 4:
        raise AssertionError(f"Expected four notebooks, found {len(notebooks)}")
    for path in notebooks:
        payload = json.loads(path.read_text(encoding="utf-8"))
        code_cells = sum(cell.get("cell_type") == "code" for cell in payload.get("cells", []))
        if code_cells == 0:
            raise AssertionError(f"No code cells in {path.name}")
        print(f"PASS  {path.name}: {code_cells} code cells")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
