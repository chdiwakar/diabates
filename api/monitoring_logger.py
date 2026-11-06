"""Append-only JSONL inference event logger used by Lab 13 monitoring."""
import json, threading, uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "logs" / "inference" / "inference_log.jsonl"
_LOCK = threading.Lock()

def log_inference(input_data, prediction=None, diabetes_probability=None, latency_ms=None,
                  status="success", error=None, model_name="Diabetes_Prediction_Production_Model",
                  model_version="local-bundle", run_id=None, request_id=None):
    request_id = request_id or uuid.uuid4().hex[:12]
    event = {
        "request_id": request_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": dict(input_data),
        "prediction": prediction,
        "diabetes_probability": diabetes_probability,
        "latency_ms": latency_ms,
        "status": status,
        "error": error,
        "model_name": model_name,
        "model_version": model_version,
        "run_id": run_id
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _LOCK, LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, default=str) + chr(10))
    return request_id
