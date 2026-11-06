import os, sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_utils import load_train

EXPECTED=['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age','Outcome']
NUMERIC=EXPECTED

def validate_schema(df):
    print(f'[INFO] Validating diabetes dataset schema (Records: {len(df)})...')
    errors=[]
    missing=[c for c in EXPECTED if c not in df.columns]; extra=[c for c in df.columns if c not in EXPECTED]
    if missing: errors.append('Missing columns: '+', '.join(missing))
    if extra: errors.append('Unexpected columns: '+', '.join(extra))
    for c in NUMERIC:
        if c in df.columns and not pd.api.types.is_numeric_dtype(df[c]): errors.append(f'Datatype mismatch: {c} must be numeric')
    if 'Outcome' in df.columns and not set(df['Outcome'].dropna().unique()).issubset({0,1}): errors.append('Outcome must contain only 0/1')
    for c in ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']:
        if c in df.columns and (df[c].dropna()<0).any(): errors.append(f'Negative values found in {c}')
    if df.duplicated().any(): print(f'[INFO] Duplicate rows detected: {int(df.duplicated().sum())}; preprocessing removes duplicates.')
    os.makedirs('artifacts',exist_ok=True)
    if errors:
        pd.DataFrame({'validation_error':errors}).to_csv('artifacts/schema_validation_errors.csv',index=False)
        print('[ERROR] Schema Validation FAILED'); [print(' -',e) for e in errors]; return False
    print('[SUCCESS] Schema Validation PASSED.'); return True
if __name__=='__main__':
    df,_=load_train()
    if not validate_schema(df): raise SystemExit(1)
