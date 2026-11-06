# Lab 8 — Continuous Integration and Quality Gate

The GitHub Actions workflow `.github/workflows/lab8_ci.yml` runs on relevant pushes, pull requests, and manual dispatch. It installs the existing project requirements plus PyYAML, executes the new diabetes pipeline, and uploads reports, logs, outputs, and the additive Lab 7–9 model artifact.

The evaluation stage records accuracy, precision, recall, F1, and ROC-AUC. The quality gate checks the configured ROC-AUC threshold (default 0.70). Lifecycle automation records promotion eligibility only when the gate passes; it does not silently change the existing MLflow registry.

Run locally with `python src/mlops_pipeline/churn_prediction_pipeline.py`. Actual CI status is only known after pushing the repository and reviewing the GitHub Actions run.
