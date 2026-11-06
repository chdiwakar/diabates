# CI Setup Notes (Diabetes Labs 7–9)

The new Lab 7–9 pipeline is self-contained and saves its model locally. It does not require an MLflow tracking server or GitHub secret. Existing MLflow configuration, database, and Labs 1–6 scripts are left unchanged.

For a future remote MLflow setup, configure tracking URI and credentials as GitHub Actions secrets; never commit credentials. If you later add registry promotion, require the quality gate to pass first and review the workflow permissions.
