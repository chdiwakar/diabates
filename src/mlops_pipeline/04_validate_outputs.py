from common import load_config, path, write_json
import pandas as pd, numpy as np
def main():
    c=load_config(); b=path(c['paths']['processed_dir']); errors=[]
    for f in ['X_train_raw.csv','X_test_raw.csv','y_train.npy','y_test.npy']:
        if not (b/f).exists(): errors.append(f'Missing output: {f}')
    if not errors:
        xt=pd.read_csv(b/'X_train_raw.csv'); xv=pd.read_csv(b/'X_test_raw.csv'); yt=np.load(b/'y_train.npy'); yv=np.load(b/'y_test.npy')
        if len(xt)!=len(yt): errors.append('Train feature/label row counts differ')
        if len(xv)!=len(yv): errors.append('Test feature/label row counts differ')
        if list(xt.columns)!=list(xv.columns): errors.append('Train/test feature schemas differ')
    write_json('artifacts/output_validation_report.json', {'stage':'Lab 7 - Output Validation','errors':errors,'status':'FAILED' if errors else 'PASSED'})
    if errors: raise SystemExit('; '.join(errors))
    print('[SUCCESS] Processed outputs validated')
if __name__=='__main__': main()
