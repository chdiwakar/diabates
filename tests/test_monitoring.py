from pathlib import Path
import json

def test_drift_script_files_exist():
    root=Path(__file__).resolve().parents[1]
    for name in ["12_create_evolved_dataset.py","12_data_drift.py","12_prediction_drift.py","12_monitor_trigger.py","12_retrain_model.py"]:
        assert (root/"src"/"mlops_pipeline"/name).exists()

def test_api_monitoring_logger_writes_jsonl(tmp_path, monkeypatch):
    import api.monitoring_logger as logger
    monkeypatch.setattr(logger,"LOG_PATH",tmp_path/"events.jsonl")
    logger.log_inference({"age":40},prediction=0,diabetes_probability=.2,latency_ms=3.1)
    event=json.loads((tmp_path/"events.jsonl").read_text().strip())
    assert event["status"]=="success"
    assert event["diabetes_probability"]==.2
