from common import load_config, path, write_json
def run_quality_gate():
    c=load_config(); report_path=path(c['paths']['evaluation_report']); metric=c['quality_gate']['metric']; minimum=float(c['quality_gate']['minimum_value'])
    if not report_path.exists(): raise FileNotFoundError(f'Evaluation report not found: {report_path}')
    report=__import__('json').loads(report_path.read_text(encoding='utf-8')); actual=float(report['metrics'].get(metric,0.0)); passed=actual>=minimum
    result={'stage':'Lab 8 - Model Quality Gate','metric':metric,'minimum_value':minimum,'actual_value':actual,'status':'PASSED' if passed else 'FAILED'}
    write_json(c['paths']['quality_gate_report'],result); write_json('reports/quality_gate_report.json',result)
    print(f"[{'SUCCESS' if passed else 'ERROR'}] Quality gate {result['status']}: {metric}={actual:.4f}, required>={minimum:.4f}")
    return passed
if __name__=='__main__':
    if not run_quality_gate(): raise SystemExit(1)
