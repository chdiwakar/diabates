from common import load_config, path, write_json
import json, datetime
def main():
    c=load_config(); gate=path(c['paths']['quality_gate_report'])
    if not gate.exists(): raise FileNotFoundError('Quality gate report missing; evaluation must run first')
    result=json.loads(gate.read_text()); promoted=result.get('status')=='PASSED'
    payload={'stage':'Lab 8 - Lifecycle Automation','decision':'PROMOTION_ELIGIBLE' if promoted else 'BLOCKED','reason':'Quality gate passed' if promoted else 'Quality gate failed','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASSED' if promoted else 'BLOCKED'}
    write_json('artifacts/lifecycle_report.json',payload)
    if not promoted: raise SystemExit('Model lifecycle promotion blocked by quality gate')
    print('[SUCCESS] Model is eligible for promotion (no external registry mutation performed).')
if __name__=='__main__': main()
