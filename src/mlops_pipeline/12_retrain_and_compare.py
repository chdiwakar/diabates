"""Alias for the guarded Lab 13 retraining process."""
from pathlib import Path
import runpy
if __name__=="__main__":
    runpy.run_path(str(Path(__file__).with_name("12_retrain_model.py")),run_name="__main__")
