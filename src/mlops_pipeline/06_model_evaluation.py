from common import load_config, path, write_json
import pandas as pd, numpy as np, joblib
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,confusion_matrix
def main():
    c=load_config(); b=path(c['paths']['processed_dir']); model=joblib.load(path(c['paths']['model_path'])); X=pd.read_csv(b/'X_test_raw.csv'); y=np.load(b/'y_test.npy'); pred=model.predict(X); prob=model.predict_proba(X)[:,1]
    metrics={'accuracy':float(accuracy_score(y,pred)),'precision':float(precision_score(y,pred,zero_division=0)),'recall':float(recall_score(y,pred,zero_division=0)),'f1_score':float(f1_score(y,pred,zero_division=0)),'roc_auc':float(roc_auc_score(y,prob))}
    report={'stage':'Lab 8 - Model Evaluation','metrics':metrics,'confusion_matrix':confusion_matrix(y,pred).tolist(),'test_rows':len(y)}
    write_json(c['paths']['evaluation_report'],report); write_json('reports/evaluation_report.json',report)
    print('[SUCCESS] Evaluation metrics:',metrics)
if __name__=='__main__': main()
