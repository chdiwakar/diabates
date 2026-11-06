import os, json, joblib, numpy as np, mlflow, mlflow.sklearn
from mlflow_config import configure_mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score

def train_and_track(run_name, params):
    Xtr=np.load("data/processed/X_train_final.npy"); Xte=np.load("data/processed/X_test_final.npy"); ytr=np.load("data/processed/y_train.npy"); yte=np.load("data/processed/y_test.npy")
    configure_mlflow()
    with mlflow.start_run(run_name=run_name):
        mlflow.log_params(params); mlflow.log_param("model_family","RandomForest")
        model=RandomForestClassifier(**params); model.fit(Xtr,ytr); pred=model.predict(Xte); prob=model.predict_proba(Xte)[:,1]
        metrics={"accuracy":accuracy_score(yte,pred),"precision":precision_score(yte,pred,zero_division=0),"recall":recall_score(yte,pred,zero_division=0),"f1_score":f1_score(yte,pred,zero_division=0),"roc_auc":roc_auc_score(yte,prob)}
        mlflow.log_metrics(metrics)
        if os.path.exists("data/processed/dataset_metadata.json"): mlflow.log_artifact("data/processed/dataset_metadata.json",artifact_path="metadata")
        if os.path.exists("models/preprocessor.pkl"): mlflow.log_artifact("models/preprocessor.pkl",artifact_path="preprocessing_pipeline")
        mlflow.sklearn.log_model(
    sk_model=model,
    name="model",
    skops_trusted_types=["sklearn.tree._tree.Tree"]
)

        print(run_name, {k:round(v,4) for k,v in metrics.items()})
if __name__ == "__main__":
    train_and_track("RandomForest_Baseline", {"n_estimators":100,"max_depth":10,"random_state":42})
    train_and_track("RandomForest_Tuned", {"n_estimators":200,"max_depth":15,"random_state":42})
