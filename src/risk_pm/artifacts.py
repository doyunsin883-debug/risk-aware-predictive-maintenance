"""Loading and scoring helpers for the frozen research artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd


@dataclass(frozen=True)
class FrozenArtifacts:
    model: Any
    features: list[str]
    threshold: float


def load_artifacts(model_dir: str | Path) -> FrozenArtifacts:
    """Load trusted local joblib artifacts from ``model_dir``.

    Pickle-compatible formats may execute code during loading. Call this only
    for artifacts whose provenance and hashes have been verified.
    """

    directory = Path(model_dir)
    return FrozenArtifacts(
        model=joblib.load(directory / "final_gradient_boosting_model.pkl"),
        features=list(joblib.load(directory / "final_feature_set.pkl")),
        threshold=float(joblib.load(directory / "final_threshold.pkl")),
    )


def score_frame(frame: pd.DataFrame, artifacts: FrozenArtifacts) -> pd.DataFrame:
    """Return model scores and thresholded alerts for a prepared feature frame."""

    missing = [name for name in artifacts.features if name not in frame.columns]
    if missing:
        raise KeyError(f"Prepared feature columns are missing: {missing}")
    score = artifacts.model.predict_proba(frame[artifacts.features])[:, 1]
    return pd.DataFrame(
        {
            "failure_score": score,
            "failure_alert": (score >= artifacts.threshold).astype("int8"),
        },
        index=frame.index,
    )
