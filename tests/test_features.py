import numpy as np
import pandas as pd

from risk_pm.features import POWER, TEMP_DIFF, add_physical_features


def test_add_physical_features_uses_physical_definitions():
    frame = pd.DataFrame(
        {
            "Air temperature [K]": [300.0],
            "Process temperature [K]": [310.0],
            "Rotational speed [rpm]": [60.0],
            "Torque [Nm]": [10.0],
        }
    )
    result = add_physical_features(frame)
    assert result.loc[0, TEMP_DIFF] == 10.0
    assert np.isclose(result.loc[0, POWER], 2.0 * np.pi * 10.0 / 1000.0)
    assert TEMP_DIFF not in frame.columns
