"""Score a CSV that already contains the frozen model's feature columns."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd  # noqa: E402

from risk_pm.artifacts import load_artifacts, score_frame  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    artifacts = load_artifacts(ROOT / "models")
    scored = score_frame(frame, artifacts)
    identity = frame[[column for column in ("UDI", "Product ID") if column in frame.columns]]
    output = pd.concat([identity.reset_index(drop=True), scored.reset_index(drop=True)], axis=1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(args.output, index=False)
    print(f"scored {len(output)} rows -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
