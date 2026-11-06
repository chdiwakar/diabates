# Git Workflow for Labs 7–9

1. Create a feature branch: `git checkout -b labs-7-9-diabetes-pipeline`
2. Review additions: `git status --short`
3. Run locally: `python -m pip install -r requirements.txt pyyaml` then `python src/mlops_pipeline/churn_prediction_pipeline.py`
4. Run failure checks: `python src/mlops_pipeline/10_failure_injection.py`
5. Commit: `git add .github config.yaml data/raw/diabetes_prediction_dataset.csv docs src/mlops_pipeline reports outputs logs notebooks tests GIT_WORKFLOW.md`
6. `git commit -m "Add diabetes MLOps labs 7-9"`
7. Push and open a pull request. Review the Lab 8 CI run and manually dispatch Lab 9.

Do not add local credentials or personal tokens to Git. Generated files can be reviewed before committing; existing Labs 1–6 files are not modified by this addition.
