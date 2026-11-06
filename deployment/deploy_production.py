"""Build the diabetes API image and optionally deploy it to the active Kubernetes context."""
import subprocess, sys, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
IMAGE="diabetes-prediction-api:latest"
def run(args):
    print("[RUN]"," ".join(args))
    subprocess.run(args,cwd=ROOT,check=True)
def main():
    if not (ROOT/"deployment/model.pkl").exists():
        raise FileNotFoundError("Run python src/mlops_pipeline/11_prepare_deployment.py first.")
    run(["docker","build","-t",IMAGE,"."])
    # Image build is safe to run without Kubernetes; deployment is opt-in.
    if "--k8s" in sys.argv:
        run(["kubectl","apply","-f","k8s/deployment.yaml"])
        run(["kubectl","rollout","status","deployment/diabetes-api","--timeout=120s"])
    report={"status":"success","image":IMAGE,"kubernetes_deployed":"--k8s" in sys.argv}
    path=ROOT/"reports/deployment_automation_report.json"; path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__":
    try: main()
    except Exception as exc:
        print(f"[ERROR] {exc}"); raise SystemExit(1)
