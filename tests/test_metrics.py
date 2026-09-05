import numpy as np

from risk_pm.metrics import binary_metrics


def test_binary_metrics_preserves_error_counts():
    y_true = np.array([0, 0, 1, 1])
    scores = np.array([0.1, 0.8, 0.7, 0.2])
    result = binary_metrics(y_true, scores, threshold=0.5)
    assert (result["tn"], result["fp"], result["fn"], result["tp"]) == (1, 1, 1, 1)
    assert result["precision"] == 0.5
    assert result["recall"] == 0.5
