"""End-to-end diabetes prediction pipeline for Labs 7-9."""
from pathlib import Path
import subprocess, sys, json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
STEPS = [
    "01_load_data.py", "02_validate_data.py", "03_preprocessing.py",
    "04_validate_outputs.py", "05_train_registry.py",
    "06_model_evaluation.py", "07_quality_gate.py",
    "08_automate_lifecycle.py", "09_inference.py"
]

def main():
    started = datetime.now(timezone.utc)
    statuses = []
    log_path = ROOT / "logs" / "diabetes_prediction_pipeline_run_log.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    for step in STEPS:
        print(f"\\n========== {step} ==========")
        result = subprocess.run([sys.executable, str(ROOT / "src" / "mlops_pipeline" / step)], cwd=ROOT)
        statuses.append({"step": step, "return_code": result.returncode})
        if result.returncode:
            payload = {"started_utc": started.isoformat(), "finished_utc": datetime.now(timezone.utc).isoformat(), "steps": statuses, "status": "FAILED"}
            log_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            raise SystemExit(result.returncode)
    payload = {"started_utc": started.isoformat(), "finished_utc": datetime.now(timezone.utc).isoformat(), "steps": statuses, "status": "PASSED"}
    log_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("[SUCCESS] Diabetes Labs 7-9 pipeline completed.")

if __name__ == "__main__":
    main()
