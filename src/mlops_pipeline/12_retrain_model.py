"""Lab 13 retraining entry point: retrain only on supplied, correctly labelled data.

This deliberately refuses to manufacture labels from drifted feature-only batches.
Place a reviewed labelled dataset at data/monitoring/labelled_retraining_data.csv
with all model features and the configured target column before running.
"""
from pathlib import Path
import yaml, pandas as pd, joblib, json
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"data/monitoring/labelled_retraining_data.csv"
REPORT=ROOT/"outputs/retraining/retraining_report.json"

def main():
    if not DATA.exists():
        raise FileNotFoundError("No reviewed labelled retraining data found. Add data/monitoring/labelled_retraining_data.csv; synthetic labels are intentionally not generated.")
    cfg=yaml.safe_load((ROOT/"config.yaml").read_text(encoding="utf-8"))
    target=cfg["data"]["target"]; df=pd.read_csv(DATA)
    if target not in df: raise ValueError(f"Target column '{target}' is missing.")
    X=df.drop(columns=[target]); y=df[target].astype(int)
    if set(y.unique())-set([0,1]): raise ValueError("Target must contain only 0/1 labels.")
    cats=X.select_dtypes(include=["object","category"]).columns.tolist(); nums=[c for c in X if c not in cats]
    prep=ColumnTransformer([("num",Pipeline([("imputer",SimpleImputer(strategy="median")),("scale",StandardScaler())]),nums),
                            ("cat",Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),("onehot",OneHotEncoder(handle_unknown="ignore"))]),cats)])
    candidate=Pipeline([("preprocessor",prep),("classifier",LogisticRegression(max_iter=500,class_weight="balanced",random_state=42))])
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
    candidate.fit(Xtr,ytr); prob=candidate.predict_proba(Xte)[:,1]; pred=candidate.predict(Xte)
    report={"stage":"Lab 13 - Controlled Retraining","training_rows":len(Xtr),"validation_rows":len(Xte),
            "accuracy":float(accuracy_score(yte,pred)),"roc_auc":float(roc_auc_score(yte,prob)),
            "status":"CANDIDATE_ONLY","note":"Candidate is saved separately and is not automatically promoted."}
    dest=ROOT/"deployment"/"candidate_model.pkl"; dest.parent.mkdir(parents=True,exist_ok=True); joblib.dump(candidate,dest)
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__": main()
