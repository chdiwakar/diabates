"""Lab 11: validate and package the approved diabetes model for serving."""
from pathlib import Path
import json, shutil, joblib, yaml
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]

def main():
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    model_path = ROOT / config["paths"]["model_path"]
    if not model_path.exists():
        raise FileNotFoundError(f"Train the Lab 7-9 pipeline first: {model_path}")
    model = joblib.load(model_path)
    if not hasattr(model, "predict") or not hasattr(model, "predict_proba"):
        raise TypeError("The deployment artifact must support predict and predict_proba.")
    deployment = ROOT / "deployment"
    deployment.mkdir(exist_ok=True)
    shutil.copy2(model_path, deployment / "model.pkl")
    metadata = {
        "project": "diabetes-prediction-mlops",
        "model_name": "Diabetes_Prediction_Production_Model",
        "model_version": "local-bundle",
        "model_stage": "Production",
        "model_artifact": "deployment/model.pkl",
        "target": config["data"]["target"],
        "features": ["gender", "age", "hypertension", "heart_disease", "smoking_history", "bmi", "HbA1c_level", "blood_glucose_level"],
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "note": "Local deployment bundle copied from the validated Lab 7-9 sklearn Pipeline."
    }
    (deployment / "model_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print("[SUCCESS] Deployment bundle created in deployment/")

if __name__ == "__main__":
    main()
