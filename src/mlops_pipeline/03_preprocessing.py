from common import load_config, path, write_json
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
def main():
    c=load_config(); base=path(c['paths']['processed_dir']); df=pd.read_csv(base/'loaded_data.csv').drop_duplicates()
    target=c['data']['target']; X=df.drop(columns=[target]); y=df[target].astype(int)
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=float(c['data']['test_size']),random_state=int(c['project']['random_state']),stratify=y)
    for name,frame in [('X_train_raw',Xtr),('X_test_raw',Xte)]: frame.to_csv(base/f'{name}.csv',index=False)
    np.save(base/'y_train.npy',ytr.to_numpy()); np.save(base/'y_test.npy',yte.to_numpy())
    write_json('artifacts/lab7_9_preprocessing_summary_report.json', {'stage':'Lab 7 - Preprocessing Split','rows_after_deduplication':len(df),'train_rows':len(Xtr),'test_rows':len(Xte),'features':list(X.columns),'target':target,'random_state':int(c['project']['random_state']),'status':'PASSED'})
    print(f'[SUCCESS] Split data: train={len(Xtr)}, test={len(Xte)}')
if __name__=='__main__': main()
