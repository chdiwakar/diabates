import os, json, joblib, sys
from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_utils import load_train

TARGET = 'Outcome'
FEATURES = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
ZERO_AS_MISSING = ['Glucose','BloodPressure','SkinThickness','Insulin','BMI']

def prepare_raw(df):
    df = df.drop_duplicates().copy()
    if TARGET not in df.columns:
        raise ValueError(f'Missing target column: {TARGET}')
    for c in ZERO_AS_MISSING:
        df[c] = df[c].replace(0, np.nan)
    y = df[TARGET].astype(int)
    if not set(y.unique()).issubset({0, 1}):
        raise ValueError('Outcome must contain only 0/1 values.')
    X = df[FEATURES]
    return X, y

def run_preprocessing():
    print('[INFO] Starting Diabetes Prediction preprocessing...')
    df, source = load_train()
    X, y = prepare_raw(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    num_cols = FEATURES
    num_pipe = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
    preprocessor = ColumnTransformer([('numeric', num_pipe, num_cols)])
    X_train_final = preprocessor.fit_transform(X_train)
    X_test_final = preprocessor.transform(X_test)
    os.makedirs('data/processed', exist_ok=True); os.makedirs('models', exist_ok=True)
    np.save('data/processed/X_train_final.npy', X_train_final); np.save('data/processed/X_test_final.npy', X_test_final)
    np.save('data/processed/y_train.npy', y_train.to_numpy(dtype=np.int64)); np.save('data/processed/y_test.npy', y_test.to_numpy(dtype=np.int64))
    joblib.dump(preprocessor, 'models/preprocessor.pkl')
    metadata = {'dataset_name':'Pima Indians Diabetes Dataset','source_file':str(source),'target':TARGET,'target_mapping':{'0':'No Diabetes','1':'Diabetes'},'zero_as_missing':ZERO_AS_MISSING,'train_shape':list(X_train_final.shape),'test_shape':list(X_test_final.shape),'numerical_features':num_cols,'categorical_features':[],'random_state':42}
    with open('data/processed/dataset_metadata.json','w') as f: json.dump(metadata,f,indent=4)
    print(f'[INFO] Raw records: {len(df)} | Train: {len(y_train)} | Test: {len(y_test)}')
    print('[SUCCESS] Preprocessing completed successfully!')
if __name__ == '__main__': run_preprocessing()
