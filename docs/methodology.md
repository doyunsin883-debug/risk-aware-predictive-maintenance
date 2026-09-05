# Methodology notes

## 1. Observation order and leakage control

AI4I 2020 does not provide genuine timestamps. This study treats row order as pseudo-time only to demonstrate a forward holdout discipline. Rows 0–6,999 define the training baseline; 7,000–8,499 are validation; and 8,500–9,999 remain locked for final evaluation. This choice prevents random mixing but does not establish temporal stationarity.

## 2. Label audit

The target contains 339 failures. The five mode flags are TWF, HDF, PWF, OSF, and RNF. Twenty-seven rows are logically inconsistent between the aggregate target and mode flags: 18 rows have a mode flag while `Machine failure=0` (all RNF), and 9 rows have `Machine failure=1` without a mode flag. Modes can overlap. The aggregate target is retained to stay faithful to the benchmark, and the inconsistency is reported rather than silently repaired.

## 3. Statistical process control

Individuals and moving-range limits are estimated from the training block. For a variable x, the process standard deviation is approximated by `MR-bar / d2` with `d2=1.128`; the individuals limits are `x-bar ± 3 sigma`. The saved mechanical limits are:

| Variable | LCL | UCL |
|---|---:|---:|
| Torque [Nm] | 10.0605 | 69.7907 |
| Mechanical power [kW] | 3.0829 | 9.4624 |
| Rotational speed [rpm] | 1,051.9791 | 2,029.1871 |

The temperature-difference alarm is excluded from the final binary alarm feature set because the validation block exhibits a broad level shift, creating 96.13% alarm coverage with little risk discrimination. It remains diagnostically important as a baseline-change signal.

## 4. Feature engineering

`Temperature difference [K] = Process temperature [K] − Air temperature [K]`.

`Mechanical power [kW] = Torque [Nm] × 2π × Rotational speed [rpm] / 60 / 1000`.

The final estimator receives product type, six original continuous sensor variables, the two physical features, and three mechanical SPC flags.

## 5. Model and threshold selection

Logistic Regression, Random Forest, and Gradient Boosting are compared on the validation block using precision, recall, F1, ROC-AUC, and PR-AUC. Gradient Boosting provides the best validation PR-AUC and recall among the candidate models at the default threshold. A threshold sweep then selects 0.65 as an operational compromise. The threshold and estimator are frozen before the test block is evaluated.

## 6. Decision layer

The operating-point search evaluates a 60 × 60 speed–torque grid under fixed air temperature, process temperature, tool wear, product type, and saved SPC limits. It filters points by power and SPC feasibility, then reports one low-score candidate. Multiple points share the minimum, so the result is not a unique continuous optimum.

The tool-wear curve varies one feature around that fixed scenario. Its step changes reflect tree splits and must not be interpreted as a causal wear law. The final linear program demonstrates how risk scores could enter an eight-hour two-mode production model. Because its risk budget is constructed from the illustrated 60/40 schedule, it demonstrates transfer of information rather than discovering an empirical production policy.
