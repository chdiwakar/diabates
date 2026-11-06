from typing import List, Literal
from pydantic import BaseModel, Field, ConfigDict

class DiabetesRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gender: Literal["Female", "Male", "Other"]
    age: float = Field(ge=0, le=120)
    hypertension: int = Field(ge=0, le=1)
    heart_disease: int = Field(ge=0, le=1)
    smoking_history: Literal["No Info", "never", "current", "former", "ever", "not current"]
    bmi: float = Field(gt=0, le=100)
    HbA1c_level: float = Field(gt=0, le=20)
    blood_glucose_level: float = Field(gt=0, le=1000)

class Prediction(BaseModel):
    prediction: int
    diabetes_probability: float

class BatchRequest(BaseModel):
    records: List[DiabetesRecord] = Field(min_length=1, max_length=100)

class BatchResponse(BaseModel):
    predictions: List[Prediction]
