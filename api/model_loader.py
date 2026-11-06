"""Load the validated local deployment bundle for the Diabetes API."""
from pathlib import Path
import json, joblib

ROOT = Path(__file__).resolve().parents[1]

class ModelLoader:
    def __init__(self):
        self.model = None
        self.load_error = None
        self.metadata = {}
        self.model_name = "Diabetes_Prediction_Production_Model"
        self.model_version = "local-bundle"
        self.run_id = None

    def load(self):
        bundle = ROOT / "deployment"
        model_path = bundle / "model.pkl"
        metadata_path = bundle / "model_metadata.json"
        if not model_path.exists():
            # Backward-compatible fallback for the original Lab 10/11 project.
            model_path = ROOT / "models" / "diabetes_lab7_9_pipeline.joblib"
        try:
            self.model = joblib.load(model_path)
            if metadata_path.exists():
                self.metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                self.model_name = self.metadata.get("model_name", self.model_name)
                self.model_version = self.metadata.get("model_version", self.model_version)
                self.run_id = self.metadata.get("run_id")
            print(f"[SUCCESS] Loaded diabetes model: {model_path}")
        except Exception as exc:
            self.load_error = str(exc)
            raise

    @property
    def ready(self):
        return self.model is not None

    def is_ready(self):
        return self.ready

model_loader = ModelLoader()
