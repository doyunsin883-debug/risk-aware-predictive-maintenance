# Results ledger

## Data split

| Block | Rows | Failures | Failure rate |
|---|---:|---:|---:|
| Train | 7,000 | 278 | 3.971% |
| Validation | 1,500 | 32 | 2.133% |
| Test | 1,500 | 29 | 1.933% |

## Validation model comparison at threshold 0.50

| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.2500 | 0.6875 | 0.3667 | 0.9023 | 0.4458 |
| Random Forest | 0.7500 | 0.6562 | 0.7000 | 0.9736 | 0.7455 |
| Gradient Boosting | 0.3968 | 0.7812 | 0.5263 | 0.9857 | 0.7718 |

At the selected threshold of 0.65, validation precision is 0.5435, recall 0.7812, and F1 0.6410, with TP 25, FP 21, and FN 7.

## Locked test

| Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---:|---:|---:|---:|---:|---:|
| 0.9833 | 0.5526 | 0.7241 | 0.6269 | 0.9615 | 0.7463 |

Confusion matrix: TN 1,454; FP 17; FN 8; TP 21.

## Interpretation checkpoints

- Mechanical power produced the largest validation PR-AUC permutation loss (0.5909), followed by tool wear (0.3325), rotational speed (0.1001), and torque (0.0859).
- SPC alarm variables added little unique permutation importance once continuous measurements and their interaction were present. This is not evidence that alarms are operationally useless.
- Test mode coverage was PWF 7/7, OSF 16/17, and TWF 1/7. Sparse and overlapping strata prevent formal subgroup claims.
- Validation-to-test recall fell by about 0.057, while PR-AUC remained close to the model-selection value.
