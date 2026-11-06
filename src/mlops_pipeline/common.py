"""Shared helpers for the additive Labs 7-9 diabetes pipeline."""
from pathlib import Path
import json, yaml

ROOT = Path(__file__).resolve().parents[2]
def load_config():
    with (ROOT / "config.yaml").open(encoding="utf-8") as f:
        return yaml.safe_load(f)
def path(value):
    p = Path(value)
    return p if p.is_absolute() else ROOT / p
def write_json(dest, payload):
    dest = path(dest); dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
