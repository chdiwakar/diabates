# Lab 13 — End-to-End Monitoring and Controlled Retraining

## Objectives
- Monitor feature distribution changes using PSI for numeric features and total variation distance for categorical features.
- Compare the model's prediction distribution between baseline and evolved feature batches.
- Track API success/failure rates and inference latency from structured JSONL events.
- Establish a safe retraining gate that requires reviewed labels.

## Execution
1. Prepare the deployment model: `python src/mlops_pipeline/11_prepare_deployment.py`
2. Run the monitor: `python src/mlops_pipeline/12_monitor_trigger.py`
3. Call the API `/predict` endpoint to create request logs.
4. Summarize API performance: `python src/mlops_pipeline/12_api_performance_monitoring.py`
5. Supply a reviewed labelled CSV before running `python src/mlops_pipeline/12_retrain_model.py`.

## Outputs
- `outputs/monitoring/data_drift_report.json`
- `outputs/monitoring/prediction_drift_report.json`
- `outputs/monitoring/concept_drift_report.json`
- `outputs/monitoring/monitor_trigger_report.json`
- `outputs/monitoring/api_performance_report.json`
- `outputs/retraining/retraining_report.json` (only after labelled data is supplied)

## Safety and interpretation
The evolved dataset modifies feature distributions for a controlled lab demonstration. It does not contain verified outcomes. Consequently, the workflow never invents diabetes labels or promotes a candidate automatically. A drift flag triggers investigation; it does not prove model degradation.
