"""Create a reproducible, clearly labelled synthetic feature-drift batch for Lab 13."""
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/processed/labs7_9/X_test_raw.csv"
OUTPUT = ROOT / "data/monitoring/drift/evolved_data.csv"
SEED = 42

def main():
    rng = np.random.default_rng(SEED)
    df = pd.read_csv(SOURCE)
    if "age" in df: df["age"] = (df["age"] + rng.normal(5, 4, len(df))).clip(0, 100)
    if "bmi" in df: df["bmi"] = (df["bmi"] * rng.normal(1.12, .06, len(df))).clip(10, 70)
    if "HbA1c_level" in df: df["HbA1c_level"] = (df["HbA1c_level"] + rng.normal(.8, .5, len(df))).clip(3, 20)
    if "blood_glucose_level" in df: df["blood_glucose_level"] = (df["blood_glucose_level"] + rng.normal(18, 12, len(df))).clip(50, 500)
    if "smoking_history" in df:
        df["smoking_history"] = rng.choice(["never","No Info","former","current","not current","ever"], len(df),
                                             p=[.25,.15,.20,.20,.12,.08])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)
    print(f"[SUCCESS] Synthetic feature-drift batch saved: {OUTPUT} ({len(df)} rows)")
    print("[NOTE] This is simulated data for monitoring exercises, not real patient data.")

if __name__ == "__main__": main()
