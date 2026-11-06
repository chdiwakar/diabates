# Lab 10 - Diabetes Model Serving API

This project adapts the sir-provided Lab 10 API objectives to the Diabetes Prediction model already in this repository. The existing trained pipeline is `models/diabetes_lab7_9_pipeline.joblib`; the API uses its eight recorded input features.

Endpoints: `GET /`, `GET /health`, `GET /metadata`, `POST /predict`, `POST /predict/batch`. Interactive docs: `/docs`.

Run locally from the project root after installing `requirements-api.txt`: `python -m uvicorn api.main:app --reload --port 8000`.

Test: `python -m pip install -r requirements-test.txt` then `python -m pytest tests/test_api.py -v`.
