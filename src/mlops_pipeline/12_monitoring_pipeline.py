"""Run Lab 13 monitoring, including request-level API performance if logs exist."""
from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[2]
for name in ["12_monitor_trigger.py","12_api_performance_monitoring.py"]:
    script=ROOT/"src/mlops_pipeline"/name
    result=subprocess.run([sys.executable,str(script)],cwd=ROOT)
    if result.returncode: raise SystemExit(result.returncode)
