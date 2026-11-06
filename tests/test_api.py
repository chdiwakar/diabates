import pytest
from fastapi.testclient import TestClient
from api.main import app

SAMPLE = {"gender":"Female","age":45,"hypertension":0,"heart_disease":0,
          "smoking_history":"never","bmi":27.5,"HbA1c_level":5.8,"blood_glucose_level":120}

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_root(client):
    r=client.get("/")
    assert r.status_code==200 and r.json()["service"]=="Diabetes Prediction API"

def test_health(client):
    r=client.get("/health")
    assert r.status_code==200 and r.json()["model_loaded"] is True

def test_metadata(client):
    r=client.get("/metadata")
    assert r.status_code==200 and "features" in r.json()

def test_predict(client):
    r=client.post("/predict",json=SAMPLE)
    assert r.status_code==200
    assert r.json()["prediction"] in (0,1)
    assert 0<=r.json()["diabetes_probability"]<=1

def test_batch(client):
    r=client.post("/predict/batch",json={"records":[SAMPLE,SAMPLE]})
    assert r.status_code==200 and len(r.json()["predictions"])==2

def test_invalid_input(client):
    bad={**SAMPLE,"age":-1}
    assert client.post("/predict",json=bad).status_code==422
