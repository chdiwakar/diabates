# Diabetes Prediction MLOps — Labs 1–13

This repository follows the organization and end-to-end MLOps workflow of the supplied Churn Prediction project while retaining the diabetes dataset, target, features and prediction task.

## Dataset and target

The main Labs 7–13 workflow uses `data/raw/diabetes_prediction_dataset.csv` with target column `diabetes`. Its eight input features are `gender`, `age`, `hypertension`, `heart_disease`, `smoking_history`, `bmi`, `HbA1c_level`, and `blood_glucose_level`.

The original Pima-style dataset `data/raw/diabetes.csv` and its `Outcome` target are retained for the original Labs 1–6 experiments. Do not mix the two datasets in one training run: they have different feature schemas and target names.

## 1. Environment setup (Windows PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## 2. Labs 1–6: original baseline, tracking, pipeline and registry exercises

The existing Lab 1–6 scripts and source files are preserved. The Pima-style dataset is used by these scripts.

```powershell
python pipelines\run_lab3_baseline.py
python pipelines\run_lab4_tracking.py
python pipelines\run_lab5_pipeline.py
python pipelines\run_lab6_registry.py
```

Start the MLflow UI in a separate terminal:
```powershell
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```
Open `http://127.0.0.1:5000`.

## 3. Labs 7–9: reproducible production pipeline

The main end-to-end pipeline uses the eight-feature diabetes prediction dataset:
```powershell
python src/mlops_pipeline/diabetes_prediction_pipeline.py
```
It loads and validates data, creates a stratified split, fits preprocessing and a classifier, evaluates metrics, applies the configured quality gate, records lifecycle eligibility and generates predictions.

## 4. Lab 10: API serving

First prepare the deployment bundle (Lab 11 below), then start the API:
```powershell
python src/mlops_pipeline/11_prepare_deployment.py
python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```
Open `http://127.0.0.1:8000/docs`. Endpoints: `/`, `/health`, `/metadata`, `/predict`, and `/predict/batch`. Successful and failed requests are appended to `logs/inference/inference_log.jsonl`.

## 5. Lab 11: Docker and Kubernetes

Build and run the container:
```powershell
python deployment/deploy_production.py
docker run --rm -p 8000:8000 diabetes-prediction-api:latest
```
For Kubernetes with Docker Desktop Kubernetes enabled:
```powershell
python deployment/deploy_production.py --k8s
kubectl get deployments
kubectl get pods
kubectl get services
```
Apply the service separately:
```powershell
kubectl apply -f k8s/service.yaml
```

## 6. Labs 12–13: monitoring, drift and controlled retraining

Create a deterministic synthetic feature-drift batch and run monitoring:
```powershell
python src/mlops_pipeline/12_monitor_trigger.py
```
This produces data drift, prediction drift, concept-drift baseline and monitoring-trigger reports under `outputs/monitoring/`.

For API latency and success-rate monitoring, first make requests to `/predict`, then run:
```powershell
python src/mlops_pipeline/12_api_performance_monitoring.py
```

Retraining is intentionally guarded. It requires a reviewed, labelled file at `data/monitoring/labelled_retraining_data.csv`, containing the same eight features and target column `diabetes`:
```powershell
python src/mlops_pipeline/12_retrain_model.py
```
The candidate is saved separately as `deployment/candidate_model.pkl`; it is not automatically promoted to production. Synthetic feature-drift data is not treated as labelled training data.

## 7. Tests

```powershell
python -m pytest -q
```

## Main project structure

- `data/raw/` — source diabetes datasets
- `data/processed/` — reproducible train/test data and metadata
- `src/` — preprocessing, training, evaluation and lifecycle scripts
- `src/mlops_pipeline/` — numbered Labs 7–13 pipeline stages
- `pipelines/` — Labs 3–6 launchers
- `models/` — trained model and preprocessing artifacts
- `deployment/` — deployment bundle and deployment helper
- `api/` — FastAPI application, schemas and inference logging
- `k8s/` — Kubernetes deployment and service manifests
- `artifacts/`, `reports/`, `outputs/`, `logs/` — machine-readable evidence and run outputs
- `.github/workflows/` — CI, failure-test and monitoring workflows

## Important notes

1. The Labs 1–6 Pima dataset and Labs 7–13 eight-feature dataset are separate experiments. Their feature schemas and target columns must not be mixed.
2. The Lab 13 evolved dataset is synthetic and exists only to demonstrate feature and prediction drift.
3. Concept drift cannot be established without trustworthy labels for newly observed records. The report therefore records baseline held-out performance and explicitly avoids inventing labels.
4. A drift alert is a signal for investigation, not automatic permission to retrain or promote a model.
5. Docker and Kubernetes deployment commands require Docker Desktop; Kubernetes commands additionally require a working Kubernetes context.
