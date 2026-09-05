import numpy as np

from risk_pm.spc import fit_imr_limits


def test_fit_imr_limits_matches_hand_calculation():
    values = np.array([10.0, 12.0, 11.0, 13.0])
    limits = fit_imr_limits(values)
    expected_mr_bar = (2.0 + 1.0 + 2.0) / 3.0
    expected_sigma = expected_mr_bar / 1.128
    assert np.isclose(limits.i_cl, 11.5)
    assert np.isclose(limits.i_lcl, 11.5 - 3.0 * expected_sigma)
    assert np.isclose(limits.i_ucl, 11.5 + 3.0 * expected_sigma)
    assert np.isclose(limits.mr_ucl, 3.267 * expected_mr_bar)
    assert limits.mr_lcl == 0.0
