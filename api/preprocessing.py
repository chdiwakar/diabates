"""Input preparation for the diabetes prediction service."""
import pandas as pd

FEATURES = ["gender", "age", "hypertension", "heart_disease", "smoking_history", "bmi", "HbA1c_level", "blood_glucose_level"]

def clean_prediction_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop(columns=["diabetes"], errors="ignore")
    missing = [name for name in FEATURES if name not in df.columns]
    extra = [name for name in df.columns if name not in FEATURES]
    if missing:
        raise ValueError(f"Missing required features: {missing}")
    if extra:
        raise ValueError(f"Unexpected features: {extra}")
    return df[FEATURES]
