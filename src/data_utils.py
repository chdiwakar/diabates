from pathlib import Path
import pandas as pd

DATASET_NAME = 'diabetes.csv'
RAW_DIR = Path('data/raw')

def find_dataset_file(name=DATASET_NAME):
    candidates = [RAW_DIR / name, Path(name)]
    candidates += list(Path('.').glob(f'archive*/{name}'))
    candidates += list(Path('.').glob(f'**/{name}'))
    for p in candidates:
        if p.exists() and p.is_file():
            return p
    return None

def load_train():
    p = find_dataset_file()
    if p is None:
        raise FileNotFoundError(f"{DATASET_NAME} not found. Put it in data/raw/.")
    print(f'[INFO] Using diabetes dataset: {p}')
    return pd.read_csv(p), p

def load_test(required=False):
    return None, None
