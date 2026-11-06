from common import load_config, path, write_json
import pandas as pd, numpy as np, joblib
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
def main():
    c=load_config(); b=path(c['paths']['processed_dir']); X=pd.read_csv(b/'X_train_raw.csv'); y=np.load(b/'y_train.npy')
    cats=X.select_dtypes(include=['object','category']).columns.tolist(); nums=[x for x in X.columns if x not in cats]
    num=Pipeline([('imputer',SimpleImputer(strategy='median')),('scaler',StandardScaler())]); cat=Pipeline([('imputer',SimpleImputer(strategy='most_frequent')),('onehot',OneHotEncoder(handle_unknown='ignore'))])
    prep=ColumnTransformer([('num',num,nums),('cat',cat,cats)])
    model=Pipeline([('preprocessor',prep),('classifier',LogisticRegression(max_iter=300,class_weight='balanced',random_state=int(c['project']['random_state'])))])
    model.fit(X,y); dest=path(c['paths']['model_path']); dest.parent.mkdir(parents=True,exist_ok=True); joblib.dump(model,dest)
    write_json('artifacts/lab7_9_production_model_report.json', {'stage':'Lab 7 - Model Training','model':'LogisticRegression with preprocessing pipeline','features':list(X.columns),'training_rows':len(X),'model_path':str(dest.relative_to(path('.'))),'status':'PASSED'})
    print(f'[SUCCESS] Trained and saved model to {dest}')
if __name__=='__main__': main()
