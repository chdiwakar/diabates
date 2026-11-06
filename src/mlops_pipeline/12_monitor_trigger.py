"""Lab 13: run the monitoring sequence and produce a single decision report."""
from pathlib import Path
import subprocess, sys, json
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[2]
SCRIPTS=["12_create_evolved_dataset.py","12_data_drift.py","12_prediction_drift.py","12_concept_drift.py"]
REPORT=ROOT/"outputs/monitoring/monitor_trigger_report.json"

def main():
    results=[]
    for script in SCRIPTS:
        print(f"\\n========== {script} ==========")
        p=subprocess.run([sys.executable,str(ROOT/"src/mlops_pipeline"/script)],cwd=ROOT)
        results.append({"script":script,"return_code":p.returncode})
        if p.returncode: raise SystemExit(p.returncode)
    data=json.loads((ROOT/"outputs/monitoring/data_drift_report.json").read_text())
    pred=json.loads((ROOT/"outputs/monitoring/prediction_drift_report.json").read_text())
    payload={"stage":"Lab 13 - Monitoring Trigger","timestamp_utc":datetime.now(timezone.utc).isoformat(),
             "data_drift_detected":data["drift_detected"],"prediction_drift_detected":pred["drift_detected"],
             "retraining_recommended":bool(data["drift_detected"] or pred["drift_detected"]),
             "steps":results,"status":"PASSED"}
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text(json.dumps(payload,indent=2),encoding="utf-8")
    print(json.dumps(payload,indent=2))
if __name__=="__main__": main()
