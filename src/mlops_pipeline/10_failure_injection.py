from common import load_config, path, write_json
import pandas as pd, tempfile, os
from importlib.machinery import SourceFileLoader
def main():
    c=load_config(); source=path(c['data']['raw_path']); df=pd.read_csv(source); cases=[]
    # Failure 1: missing required column must be detected.
    from importlib.util import spec_from_file_location, module_from_spec
    spec=spec_from_file_location('validate_data',path('src/mlops_pipeline/02_validate_data.py')); mod=module_from_spec(spec); spec.loader.exec_module(mod)
    bad=df.drop(columns=['gender'])
    errors=mod.validate(bad); cases.append({'case':'missing_required_column','failure_detected':any('gender' in e for e in errors),'expected':'validation error for gender'})
    # Failure 2: invalid target value must be detected.
    bad2=df.head(100).copy(); bad2.loc[bad2.index[0],'diabetes']=7
    errors=mod.validate(bad2); cases.append({'case':'invalid_target_value','failure_detected':any('0/1' in e for e in errors),'expected':'target restricted to 0/1'})
    # Recovery check: original dataset remains readable and unchanged.
    recovered=pd.read_csv(source); cases.append({'case':'recovery_original_dataset_readable','failure_detected':len(recovered)==len(df) and list(recovered.columns)==list(df.columns),'expected':'original dataset remains intact'})
    passed=all(x['failure_detected'] for x in cases); report={'stage':'Lab 9 - Failure Handling','cases':cases,'status':'PASSED' if passed else 'FAILED'}
    write_json(c['paths']['failure_report'],report); write_json('artifacts/failure_simulation_report.json',report)
    if not passed: raise SystemExit('One or more failure/recovery tests failed')
    print('[SUCCESS] Lab 9 failure and recovery tests passed')
if __name__=='__main__': main()
