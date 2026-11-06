"""Lab 13: compare baseline and drift-batch prediction distributions."""
from pathlib import Path
import json, joblib, pandas as pd
ROOT=Path(__file__).resolve().parents[2]
MODEL=ROOT/"deployment/model.pkl"
BASE=ROOT/"data/processed/labs7_9/X_test_raw.csv"
CUR=ROOT/"data/monitoring/drift/evolved_data.csv"
REPORT=ROOT/"outputs/monitoring/prediction_drift_report.json"

def main():
    if not MODEL.exists(): raise FileNotFoundError("Run Lab 11 deployment preparation first.")
    model=joblib.load(MODEL)
    a=model.predict_proba(pd.read_csv(BASE))[:,1]
    b=model.predict_proba(pd.read_csv(CUR))[:,1]
    report={"stage":"Lab 13 - Prediction Drift","baseline_mean_probability":float(a.mean()),
            "current_mean_probability":float(b.mean()),"absolute_mean_shift":float(abs(a.mean()-b.mean())),
            "baseline_positive_rate":float((a>=.5).mean()),"current_positive_rate":float((b>=.5).mean()),
            "drift_detected":bool(abs(a.mean()-b.mean())>=.10)}
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__": main()
