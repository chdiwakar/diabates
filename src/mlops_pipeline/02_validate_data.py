from common import load_config, path, write_json
import pandas as pd
REQUIRED={'gender','age','hypertension','heart_disease','smoking_history','bmi','HbA1c_level','blood_glucose_level','diabetes'}
def validate(df):
    errors=[]; missing=sorted(REQUIRED-set(df.columns))
    if missing: errors.append('Missing columns: '+', '.join(missing))
    if 'diabetes' in df and not set(df['diabetes'].dropna().unique()).issubset({0,1}): errors.append('diabetes must contain only 0/1')
    for col in ['age','bmi','HbA1c_level','blood_glucose_level','hypertension','heart_disease','diabetes']:
        if col in df and not pd.api.types.is_numeric_dtype(df[col]): errors.append(f'{col} must be numeric')
        elif col in df and df[col].isna().any(): errors.append(f'{col} contains missing values')
    for col in ['age','bmi','HbA1c_level','blood_glucose_level']:
        if col in df and (df[col].dropna()<0).any(): errors.append(f'{col} contains negative values')
    return errors
def main():
    c=load_config(); df=pd.read_csv(path(c['paths']['processed_dir'])/'loaded_data.csv'); errors=validate(df)
    write_json('artifacts/data_validation_report.json', {'stage':'Lab 7 - Data Validation','rows':len(df),'errors':errors,'status':'FAILED' if errors else 'PASSED'})
    if errors: raise SystemExit('Data validation failed: '+'; '.join(errors))
    print('[SUCCESS] Dataset schema and values validated')
if __name__=='__main__': main()
