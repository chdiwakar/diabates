"""FastAPI inference service with structured request monitoring."""
from contextlib import asynccontextmanager
from time import perf_counter
import uuid
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.model_loader import model_loader
from api.preprocessing import clean_prediction_data
from api.monitoring_logger import log_inference
from api.schemas import DiabetesRecord, Prediction, BatchRequest, BatchResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        model_loader.load()
    except Exception as exc:
        print(f"[ERROR] Model loading failed: {exc}")
    yield

app = FastAPI(title="Diabetes Prediction API", version="2.0.0",
              description="Labs 10-13: model serving, container deployment and monitoring",
              lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request, exc):
    log_inference({}, status="failure", error="Request validation failed")
    return JSONResponse(status_code=422, content={"status":"error","message":"Request validation failed","details":exc.errors()})

@app.get("/")
def root():
    return {"service":"Diabetes Prediction API","status":"running","docs":"/docs"}

@app.get("/health")
def health():
    if not model_loader.is_ready():
        raise HTTPException(status_code=503, detail=f"Model unavailable: {model_loader.load_error or 'not loaded'}")
    return {"status":"healthy","model_loaded":True}

@app.get("/metadata")
def metadata():
    return {"service":"Diabetes Prediction API","model_name":model_loader.model_name,
            "model_version":model_loader.model_version,"model_loaded":model_loader.is_ready(),
            "features":["gender","age","hypertension","heart_disease","smoking_history","bmi","HbA1c_level","blood_glucose_level"]}

def run_prediction(records):
    request_id = uuid.uuid4().hex[:12]
    started = perf_counter()
    inputs = [record.model_dump() for record in records]
    if not model_loader.is_ready():
        for item in inputs:
            log_inference(item, status="failure", error="Model is not available", request_id=request_id)
        raise HTTPException(status_code=503, detail="Model is not available; run Lab 11 deployment preparation.")
    try:
        frame = clean_prediction_data(pd.DataFrame(inputs))
        predictions = model_loader.model.predict(frame)
        probabilities = model_loader.model.predict_proba(frame)[:, 1]
        latency = round((perf_counter() - started) * 1000, 3)
        results = []
        for item, pred, prob in zip(inputs, predictions, probabilities):
            log_inference(item, int(pred), float(prob), latency, "success",
                          model_name=model_loader.model_name, model_version=model_loader.model_version,
                          run_id=model_loader.run_id, request_id=request_id)
            results.append({"prediction":int(pred),"diabetes_probability":float(prob)})
        return results
    except HTTPException:
        raise
    except Exception as exc:
        latency = round((perf_counter() - started) * 1000, 3)
        for item in inputs:
            log_inference(item, latency_ms=latency, status="failure", error=str(exc),
                          model_name=model_loader.model_name, model_version=model_loader.model_version,
                          run_id=model_loader.run_id, request_id=request_id)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

@app.post("/predict", response_model=Prediction)
def predict(record: DiabetesRecord):
    return run_prediction([record])[0]

@app.post("/predict/batch", response_model=BatchResponse)
def predict_batch(request: BatchRequest):
    return {"predictions":run_prediction(request.records)}
