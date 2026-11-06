# Lab 7 — Diabetes Data Pipeline

## Objective
Add a reproducible, validated preprocessing and training pipeline for the supplied diabetes prediction dataset without changing Labs 1–6.

## Dataset
`data/raw/diabetes_prediction_dataset.csv` (100,000 rows; target `diabetes`). The pipeline uses numeric and categorical fields and does not overwrite the original `data/raw/diabetes.csv`.

## Stages
1. Load data and record source/schema evidence.
2. Validate required columns, numeric fields, missing values in key fields, nonnegative measurements, and binary target.
3. Deduplicate and make a stratified train/test split using random seed 42.
4. Validate saved split outputs.
5. Fit a scikit-learn pipeline with numeric imputation/scaling, categorical imputation/one-hot encoding, and logistic regression.

## Run
`python -m pip install -r requirements.txt pyyaml`
`python src/mlops_pipeline/churn_prediction_pipeline.py`

Evidence is written under `artifacts/`, `reports/`, `logs/`, and `data/processed/labs7_9/`. The original project files are retained.
