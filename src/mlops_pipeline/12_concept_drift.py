"""Lab 13: evaluate the frozen model on baseline and labelled drift simulation."""
from pathlib import Path
import json, numpy as np, pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
ROOT=Path(__file__).resolve().parents[2]
MODEL=ROOT/"deployment/model.pkl"
BASE_X = ROOT / "data/processed/labs7_9/X_test_raw.csv"
BASE_Y = ROOT / "data/processed/labs7_9/y_test.npy"
REPORT=ROOT/"outputs/monitoring/concept_drift_report.json"

def main():
    import joblib
    if not MODEL.exists(): raise FileNotFoundError("Run Lab 11 deployment preparation first.")
    X=pd.read_csv(BASE_X); y=np.load(BASE_Y); model=joblib.load(MODEL)
    pred=model.predict(X); prob=model.predict_proba(X)[:,1]
    metrics={"accuracy":float(accuracy_score(y,pred)),"precision":float(precision_score(y,pred,zero_division=0)),
             "recall":float(recall_score(y,pred,zero_division=0)),"f1":float(f1_score(y,pred,zero_division=0))}
    if len(np.unique(y))>1: metrics["roc_auc"]=float(roc_auc_score(y,prob))
    payload={"stage":"Lab 13 - Concept Drift Baseline","evaluation":"held-out labelled test data","metrics":metrics,
             "note":"Feature drift is simulated separately. Concept drift requires trustworthy new labels; no labels are fabricated here."}
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text(json.dumps(payload,indent=2),encoding="utf-8")
    print(json.dumps(payload,indent=2))
if __name__=="__main__": main()
