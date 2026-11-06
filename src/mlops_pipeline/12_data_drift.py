"""Lab 13: numerical PSI and categorical total-variation drift checks."""
from pathlib import Path
import json, numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "data/processed/labs7_9/X_train_raw.csv"
CURRENT = ROOT / "data/monitoring/drift/evolved_data.csv"
REPORT = ROOT / "outputs/monitoring/data_drift_report.json"

def psi(expected, actual, bins=10):
    expected = pd.to_numeric(expected, errors="coerce").dropna().to_numpy()
    actual = pd.to_numeric(actual, errors="coerce").dropna().to_numpy()
    if len(expected)==0 or len(actual)==0: return None
    edges = np.unique(np.quantile(expected, np.linspace(0,1,bins+1)))
    if len(edges)<3: return 0.0
    edges[0], edges[-1] = -np.inf, np.inf
    e,_ = np.histogram(expected,bins=edges); a,_ = np.histogram(actual,bins=edges)
    ep=np.clip(e/e.sum(),1e-6,None); ap=np.clip(a/a.sum(),1e-6,None)
    return float(np.sum((ap-ep)*np.log(ap/ep)))

def main():
    if not BASE.exists() or not CURRENT.exists():
        raise FileNotFoundError("Run 12_create_evolved_dataset.py before data drift analysis.")
    base, cur = pd.read_csv(BASE), pd.read_csv(CURRENT)
    if list(base.columns)!=list(cur.columns): raise ValueError("Feature schema mismatch.")
    details={}
    for col in base.columns:
        if pd.api.types.is_numeric_dtype(base[col]):
            value=psi(base[col],cur[col]); details[col]={"method":"PSI","score":value,"drift":bool(value is not None and value>=0.20)}
        else:
            categories=set(base[col].astype(str))|set(cur[col].astype(str))
            p=base[col].astype(str).value_counts(normalize=True); q=cur[col].astype(str).value_counts(normalize=True)
            score=float(sum(abs(float(p.get(k,0))-float(q.get(k,0))) for k in categories)/2)
            details[col]={"method":"total_variation","score":score,"drift":score>=0.10}
    payload={"stage":"Lab 13 - Data Drift","baseline_rows":len(base),"current_rows":len(cur),
             "features":details,"drifted_features":[k for k,v in details.items() if v["drift"]],
             "drift_detected":any(v["drift"] for v in details.values())}
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text(json.dumps(payload,indent=2),encoding="utf-8")
    print(json.dumps(payload,indent=2))

if __name__=="__main__": main()
