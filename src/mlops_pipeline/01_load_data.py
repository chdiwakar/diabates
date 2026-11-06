from common import load_config, path, write_json
import pandas as pd

def main():
    c=load_config(); p=path(c['data']['raw_path'])
    if not p.exists(): raise FileNotFoundError(f'Dataset not found: {p}')
    df=pd.read_csv(p)
    if df.empty: raise ValueError('Dataset is empty')
    out=path(c['paths']['processed_dir'])/'loaded_data.csv'; out.parent.mkdir(parents=True,exist_ok=True); df.to_csv(out,index=False)
    write_json('artifacts/data_load_report.json', {'stage':'Lab 7 - Data Loading','source':str(p.relative_to(path('.'))),'rows':len(df),'columns':list(df.columns),'status':'PASSED'})
    print(f'[SUCCESS] Loaded {len(df)} rows from {p.name}')
if __name__=='__main__': main()
