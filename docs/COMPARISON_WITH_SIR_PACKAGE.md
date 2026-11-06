# Comparison with sir-provided Churn Prediction package

Your original Diabetes MLOps Labs 7-9 project was preserved. The sir's package is a separate Churn Prediction project; its churn model, churn-specific schemas, model artifacts, and reports cannot be copied directly into the Diabetes project because they expect different features and a different target.

Added to this copy of the Diabetes project: `api/` FastAPI serving layer, `requirements-api.txt`, `requirements-test.txt`, `Dockerfile`, `.dockerignore`, `k8s/deployment.yaml`, `k8s/service.yaml`, `tests/test_api.py`, and Lab 10/11 run guides. The API is adapted to the existing `models/diabetes_lab7_9_pipeline.joblib` and feature columns recorded in `data/processed/labs7_9/X_train_raw.csv`.

The sir's Lab 11 guide includes containerization and Kubernetes stages. Docker and API execution must be run on your laptop; test results are not claimed until you run them.
