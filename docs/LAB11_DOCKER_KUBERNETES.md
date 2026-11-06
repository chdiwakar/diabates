# Lab 11 - Containerization and Deployment (Diabetes adaptation)

## Build and run Docker
Run commands from this folder (project root):

```powershell
docker build -t diabetes-mlops-api:1.0 .
docker run --rm -d --name diabetes-api -p 8000:8000 diabetes-mlops-api:1.0
docker ps
curl.exe http://localhost:8000/health
curl.exe http://localhost:8000/metadata
docker logs diabetes-api
docker stop diabetes-api
```

Open `http://localhost:8000/docs` to test the API. Example JSON for `POST /predict`:

```json
{
  "gender": "Female", "age": 45, "hypertension": 0, "heart_disease": 0,
  "smoking_history": "never", "bmi": 27.5, "HbA1c_level": 5.8,
  "blood_glucose_level": 120
}
```

## Reproducibility / failure recovery evidence
- Record `docker --version`, `docker compose version`, and `docker image inspect diabetes-mlops-api:1.0`.
- Missing model: build fails at `COPY` or `/health` returns 503; restore the model artifact and rebuild.
- Port conflict: change host port, e.g. `-p 8001:8000`.
- App crash: inspect `docker logs diabetes-api`, fix the reported issue, rebuild and rerun.
- Compare local and container outputs with the same request payload; probabilities should match within normal floating-point tolerance.

## Kubernetes (optional; requires a local Kubernetes cluster enabled in Docker Desktop)
```powershell
docker build -t diabetes-mlops-api:1.0 .
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get deployments,pods,services
kubectl port-forward service/diabetes-api-service 8000:8000
```
For Docker Desktop Kubernetes, the image built locally is typically available to the cluster. If using a remote cluster, push the image to a registry and update the image field first.

Scale and recover:
```powershell
kubectl scale deployment/diabetes-api --replicas=3
kubectl get pods
kubectl rollout status deployment/diabetes-api
kubectl rollout undo deployment/diabetes-api
```

**Important:** Kubernetes commands are provided for execution, not represented as already verified. Capture your actual command output for the lab report.
