# Reproducibility record

This document separates the stored result from the environment needed to reproduce it.

## Reference environment

- Python 3.14.0
- NumPy 2.5.2
- pandas 3.0.5
- SciPy 1.18.1
- scikit-learn 1.9.0
- Matplotlib 3.11.1
- joblib 1.6.0

Install the exact package set with:

```bash
python -m pip install -r requirements-reproduce.txt
```

The serialized estimator was produced with scikit-learn 1.9.0. Loading pickle/joblib artifacts from untrusted sources is unsafe; verify the hashes before loading:

```bash
python scripts/verify_artifacts.py
```

## Locked analysis decisions

| Item | Value or rule |
|---|---|
| Split | Contiguous 70/15/15 by observation order |
| Training rows | 0–6,999 |
| Validation rows | 7,000–8,499 |
| Test rows | 8,500–9,999 |
| Final estimator | Gradient Boosting, 200 estimators, learning rate 0.05, random state 42 |
| Threshold | 0.65, selected on validation data |
| Test confusion matrix | TN 1,454; FP 17; FN 8; TP 21 |
| Operating grid | Speed 1,331–1,880 rpm; torque 23.10–55.90 Nm; 60 × 60 |
| Reported grid point | 1,768.339 rpm; 41.446 Nm; 7.675 kW; score 1.3046% |

## Verification levels

### Level 1 — artifact integrity

`python scripts/verify_artifacts.py` checks every serialized artifact against `results/artifact_sha256.json`.

### Level 2 — locked test evaluation

`python scripts/reproduce_core_results.py --verify` loads the frozen feature list, estimator, threshold, and test feature table. It recomputes accuracy, precision, recall, F1, ROC-AUC, PR-AUC, and the confusion matrix. The command exits non-zero if any metric differs from `results/core_metrics.json` beyond numerical tolerance.

### Level 3 — analytical narrative

Run or inspect the notebooks in order:

1. `notebooks/01_eda.ipynb`
2. `notebooks/02_sqc.ipynb`
3. `notebooks/03_ml.ipynb`
4. `notebooks/04_optimization.ipynb`

Notebook outputs are retained as an audit trail. Exact chart appearance may vary slightly across Matplotlib versions; the numeric checkpoints are the primary reproduction targets.

## Known limits to reproducibility

AI4I has no real timestamps, machine identifiers, intervention logs, or maintenance costs. The row order is therefore only a pseudo-temporal device. The optimization notebook uses fixed scenario values and a finite grid. Its planning budget is illustrative. Reproducing the code does not convert those assumptions into field evidence.
