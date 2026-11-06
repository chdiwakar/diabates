"""Compatibility launcher for API performance monitoring."""
from pathlib import Path
import runpy
if __name__=="__main__":
    runpy.run_path(str(Path(__file__).with_name("12_api_performance_monitoring.py")),run_name="__main__")
