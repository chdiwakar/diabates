from common import load_config, path, write_json
import pandas as pd, joblib
def main():
    c=load_config(); df=pd.read_csv(path(c['data']['raw_path'])); target=c['data']['target']; X=df.drop(columns=[target]) if target in df.columns else df
    model=joblib.load(path(c['paths']['model_path'])); out=pd.DataFrame({'prediction':model.predict(X),'probability_diabetes':model.predict_proba(X)[:,1]})
    dest=path(c['paths']['inference_output']); dest.parent.mkdir(parents=True,exist_ok=True); out.to_csv(dest,index=False)
    write_json('artifacts/inference_report.json',{'stage':'Lab 8 - Inference','input_rows':len(X),'output_rows':len(out),'output_path':str(dest.relative_to(path('.'))),'status':'PASSED'})
    print(f'[SUCCESS] Wrote {len(out)} inference predictions to {dest}')
if __name__=='__main__': main()
