"""Lab 13: summarize inference request success and latency from JSONL logs."""

from pathlib import Path
import json, pandas as pd
ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/"logs/inference/inference_log.jsonl"
REPORT=ROOT/"outputs/monitoring/api_performance_report.json"

def main():
    if not LOG.exists(): raise FileNotFoundError("No API inference log yet. Start the API and call /predict first.")
    raw = LOG.read_text(encoding="utf-8")
    rows = [json.loads(x) for x in raw.replace("\\n", "\n").splitlines() if x.strip()]
    if not rows: raise ValueError("Inference log is empty.")
    df=pd.DataFrame(rows); total=len(df); success=int((df.status=="success").sum()); failure=total-success
    latency=pd.to_numeric(df.get("latency_ms"),errors="coerce").dropna()
    report={"stage":"Lab 13 - API Performance Monitoring","total_requests":total,"successful_requests":success,
            "failed_requests":failure,"success_rate":success/total,"failure_rate":failure/total,
            "latency_mean_ms":float(latency.mean()) if len(latency) else None,
            "latency_p95_ms":float(latency.quantile(.95)) if len(latency) else None}
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__": main()
