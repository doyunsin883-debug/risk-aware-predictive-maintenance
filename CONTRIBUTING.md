# Contributing

Issues and pull requests that improve reproducibility, tests, documentation, or methodological clarity are welcome.

1. Open an issue describing the proposed change and its research impact.
2. Create a focused branch and avoid committing environments, secrets, or unverified binary artifacts.
3. Run `python -m pytest` and `python scripts/verify_artifacts.py`.
4. If a numerical result changes, update the relevant notebook, `results/core_metrics.json`, papers, and README together; explain why the change is methodologically justified.

Do not replace a locked test result merely because another split or seed looks better. New validation designs should be reported as new experiments.
