# Risk-Aware Predictive Maintenance Decision System

An independent industrial-engineering study that connects **process monitoring → failure prediction → operating and maintenance decisions** in one auditable workflow.

[![quality](https://github.com/doyunsin883-debug/risk-aware-predictive-maintenance/actions/workflows/quality.yml/badge.svg)](https://github.com/doyunsin883-debug/risk-aware-predictive-maintenance/actions/workflows/quality.yml) [![License: MIT](https://img.shields.io/badge/Code-MIT-0B7285.svg)](LICENSE)

[Korean paper](reports/risk_aware_predictive_maintenance_paper_ko.pdf) · [English paper](reports/risk_aware_predictive_maintenance_paper_en.pdf) · [Reproducibility](REPRODUCIBILITY.md) · [Model card](MODEL_CARD.md) · [한국어 README](README.md)

## Locked test result

The AI4I 2020 data contain 10,000 observations and 339 failures (3.39%). Rows were split contiguously into 70/15/15 blocks. The Gradient Boosting classifier and its 0.65 threshold were selected on validation data and then locked before evaluating the final 1,500-row test block.

| Metric | Test value | Operational reading |
|---|---:|---|
| Accuracy | 0.9833 | Secondary under severe class imbalance |
| Precision | 0.5526 | 21 failures among 38 alerts |
| Recall | 0.7241 | 21 of 29 failures detected |
| F1 | 0.6269 | Precision–recall balance |
| ROC-AUC | 0.9615 | Ranking across thresholds |
| PR-AUC | 0.7463 | Positive-class ranking performance |

Confusion matrix: **TN 1,454 · FP 17 · FN 8 · TP 21**.

## Research design

1. Audit the data, rare labels, and failure-mode inconsistencies.
2. Estimate I–MR control limits only from the training block.
3. Engineer temperature difference and mechanical power.
4. compare Logistic Regression, Random Forest, and Gradient Boosting on validation data.
5. Lock the model and threshold, then open the test block once.
6. Translate the score into a constrained speed–torque search, tool-wear sensitivity analysis, and an illustrative two-mode linear program.

![Locked test confusion matrix](https://raw.githubusercontent.com/doyunsin883-debug/risk-aware-predictive-maintenance/main/assets/readme/confusion_matrix.png)

## Reproduce

```bash
git clone https://github.com/doyunsin883-debug/risk-aware-predictive-maintenance.git
cd risk-aware-predictive-maintenance
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-reproduce.txt
python scripts/verify_artifacts.py
python scripts/reproduce_core_results.py --verify
```

The notebooks follow the narrative order `01_eda` → `02_sqc` → `03_ml` → `04_optimization`. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for environment and artifact details.

## Scope and limitations

This repository is a reproducible decision prototype, not a field-validated maintenance policy. AI4I is synthetic; row order is pseudo-time; the study uses one contiguous split; scores are not calibrated probabilities; and the optimization examples are conditional on a finite grid and constructed planning assumptions. The reported operating point is one tied grid minimum, not a unique continuous optimum.

## Author and research status

**Doyun Shin**, Department of Industrial Engineering, Gachon University. This is an independent research manuscript and portfolio; it is not represented as journal-accepted or published work.

Generative AI primarily assisted selected Python drafts and debugging, with additional language/layout support in manuscript preparation. Two clearly labeled concept images were generated with an image-generation tool. All reported numbers, tables, and empirical figures were checked against the stored data, notebooks, and model artifacts. The author made the research and interpretive decisions and accepts responsibility for the work.

Data: UCI AI4I 2020, DOI [10.24432/C5HS5C](https://doi.org/10.24432/C5HS5C), CC BY 4.0. Code: [MIT](LICENSE). See [DATA_AND_ASSET_NOTICE.md](DATA_AND_ASSET_NOTICE.md) for provenance.
