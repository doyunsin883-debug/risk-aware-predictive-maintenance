# Model card — Gradient Boosting failure classifier

## Model details

- **Task:** binary classification of `Machine failure`
- **Estimator:** scikit-learn `GradientBoostingClassifier`
- **Configuration:** 200 estimators, learning rate 0.05, random state 42
- **Decision threshold:** 0.65
- **Training data:** first 7,000 rows of AI4I 2020 after feature engineering and SPC feature construction
- **Owner:** Doyun Shin, Department of Industrial Engineering, Gachon University
- **Status:** independent research prototype

## Inputs

The frozen feature list is stored in `models/final_feature_set.pkl`:

- product type
- air temperature, process temperature, rotational speed, torque, and tool wear
- temperature difference and mechanical power
- torque, power, and rotational-speed SPC alarm flags

## Evaluation

The final 1,500-row contiguous test block contained 29 failures. At threshold 0.65 the model produced TN 1,454, FP 17, FN 8, and TP 21, corresponding to precision 0.5526, recall 0.7241, F1 0.6269, ROC-AUC 0.9615, and PR-AUC 0.7463.

Failure-mode coverage was uneven: PWF 7/7, OSF 16/17, and TWF 1/7 were detected. Counts overlap because a row may carry multiple mode labels. This subgroup diagnostic exposes a tool-wear-failure weakness that aggregate recall obscures.

## Intended use

- reproducing the accompanying case study
- education in imbalanced classification, process monitoring, and decision analysis
- prototyping an auditable maintenance analytics workflow

## Out-of-scope use

- autonomous shutdown or maintenance dispatch
- safety-critical decisions without human review
- claims about field failure probability, remaining useful life, or causal effects
- transfer to another asset, plant, or sampling regime without recalibration and external validation

## Limitations and risks

The dataset is synthetic, row order is not actual time, scores are uncalibrated, and the evaluation uses one contiguous split. Pickled models can execute code during loading and must not be accepted from an untrusted source. Distribution shift, alert capacity, missed-failure cost, and subgroup behavior require continuous monitoring in any real deployment.

## Human oversight

The score should support inspection prioritization, not replace engineering judgment. A production system needs explicit escalation rules, probability calibration, rolling-origin and cross-asset validation, change detection, maintenance outcomes, and a documented rollback process.
