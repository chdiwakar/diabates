import joblib, pandas as pd
from pathlib import Path

FEATURES=['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']

def main():
    print('[INFO] This diabetes project uses an 80/20 split from data/raw/diabetes.csv.')
    print('[INFO] For a new patient, create a DataFrame with these features:')
    print(FEATURES)
    print('[INFO] Load models/preprocessor.pkl and models/random_forest_model.pkl (or random_forest_baseline.pkl) to predict Outcome.')
if __name__=='__main__': main()
