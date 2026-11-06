# Operations Runbook

## Start the API
1. Run `python src/mlops_pipeline/11_prepare_deployment.py`.
2. Run `python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000`.
3. Check `/health` and `/metadata`.
4. Use `/docs` to submit a prediction.

## Monitor the API
- Logs: `logs/inference/inference_log.jsonl`
- Report: `outputs/monitoring/api_performance_report.json`
- Run: `python src/mlops_pipeline/12_api_performance_monitoring.py`

## Investigate drift
- Run: `python src/mlops_pipeline/12_monitor_trigger.py`
- Inspect data and prediction drift reports.
- Confirm data quality and label availability before any retraining.

## Container deployment
- Build: `python deployment/deploy_production.py`
- Kubernetes: `python deployment/deploy_production.py --k8s`
- Check: `kubectl get pods` and `kubectl rollout status deployment/diabetes-api`
