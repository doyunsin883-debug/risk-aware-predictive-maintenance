"""Recompute and optionally verify the locked test metrics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd  # noqa: E402

from risk_pm.artifacts import load_artifacts  # noqa: E402
from risk_pm.metrics import binary_metrics  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="compare with results/core_metrics.json")
    parser.add_argument("--output", type=Path, help="optional JSON output path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    frame = pd.read_csv(ROOT / "data" / "processed" / "test_features.csv")
    artifacts = load_artifacts(ROOT / "models")
    scores = artifacts.model.predict_proba(frame[artifacts.features])[:, 1]
    actual = {
        "dataset": "AI4I 2020",
        "test_rows": int(len(frame)),
        "test_failures": int(frame["Machine failure"].sum()),
        **binary_metrics(frame["Machine failure"], scores, artifacts.threshold),
    }

    print(json.dumps(actual, indent=2, ensure_ascii=False))
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(actual, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {output}")

    if args.verify:
        expected = json.loads((ROOT / "results" / "core_metrics.json").read_text(encoding="utf-8"))
        for key, expected_value in expected.items():
            actual_value = actual[key]
            if isinstance(expected_value, float):
                if abs(actual_value - expected_value) > 1e-10:
                    raise AssertionError(f"{key}: expected {expected_value}, got {actual_value}")
            elif actual_value != expected_value:
                raise AssertionError(f"{key}: expected {expected_value}, got {actual_value}")
        print("verification: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
