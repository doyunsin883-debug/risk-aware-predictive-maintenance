"""Individuals and moving-range control-chart calculations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


D2_FOR_RANGE_OF_TWO = 1.128
D4_FOR_RANGE_OF_TWO = 3.267


@dataclass(frozen=True)
class IMRLimits:
    i_cl: float
    i_lcl: float
    i_ucl: float
    mr_cl: float
    mr_lcl: float
    mr_ucl: float


def fit_imr_limits(values: pd.Series | np.ndarray) -> IMRLimits:
    """Estimate conventional 3-sigma I–MR limits from an ordered baseline."""

    series = pd.Series(values, dtype="float64").dropna()
    if len(series) < 2:
        raise ValueError("At least two non-missing ordered observations are required")

    moving_range = series.diff().abs().dropna()
    i_cl = float(series.mean())
    mr_cl = float(moving_range.mean())
    sigma = mr_cl / D2_FOR_RANGE_OF_TWO
    return IMRLimits(
        i_cl=i_cl,
        i_lcl=i_cl - 3.0 * sigma,
        i_ucl=i_cl + 3.0 * sigma,
        mr_cl=mr_cl,
        mr_lcl=0.0,
        mr_ucl=D4_FOR_RANGE_OF_TWO * mr_cl,
    )


def individuals_alarm(values: pd.Series, limits: IMRLimits) -> pd.Series:
    """Flag points outside the individuals-chart limits."""

    return ((values < limits.i_lcl) | (values > limits.i_ucl)).astype("int8")


def moving_range_alarm(values: pd.Series, limits: IMRLimits) -> pd.Series:
    """Flag adjacent absolute changes outside the moving-range limits."""

    moving_range = values.astype(float).diff().abs()
    return ((moving_range < limits.mr_lcl) | (moving_range > limits.mr_ucl)).fillna(False).astype("int8")
