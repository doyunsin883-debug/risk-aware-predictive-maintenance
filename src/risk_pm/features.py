"""Physical feature transformations used by the notebooks."""

from __future__ import annotations

import numpy as np
import pandas as pd


AIR = "Air temperature [K]"
PROCESS = "Process temperature [K]"
SPEED = "Rotational speed [rpm]"
TORQUE = "Torque [Nm]"
TEMP_DIFF = "Temperature difference [K]"
POWER = "Mechanical power [kW]"


def add_physical_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with temperature difference and mechanical power.

    Mechanical power is torque multiplied by angular velocity and converted
    from watts to kilowatts.
    """

    required = {AIR, PROCESS, SPEED, TORQUE}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    result = frame.copy()
    result[TEMP_DIFF] = result[PROCESS] - result[AIR]
    result[POWER] = result[TORQUE] * (2.0 * np.pi * result[SPEED] / 60.0) / 1000.0
    return result
