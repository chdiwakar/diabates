# Lab 9 — Failure Handling and Recovery

The manual GitHub Actions workflow `.github/workflows/lab9_failure_tests.yml` first runs the normal pipeline and then executes `src/mlops_pipeline/10_failure_injection.py`. The failure tests check that (1) a missing required column is rejected, (2) a non-binary target is rejected, and (3) the original source dataset remains readable after test failures are simulated in memory.

Evidence is written to `reports/failure_report.json` and `artifacts/failure_simulation_report.json`. These are controlled validation tests, not destructive corruption of the source CSV. The workflow status must be confirmed from GitHub Actions after push/dispatch.
