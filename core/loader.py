import pandas as pd
from pathlib import Path


def load_file(file) -> pd.DataFrame:
    ext = Path(file.name).suffix.lower()
    loaders = {
        ".csv":  lambda f: pd.read_csv(f),
        ".xlsx": lambda f: pd.read_excel(f),
        ".xls":  lambda f: pd.read_excel(f),
        ".json": lambda f: pd.read_json(f),
    }
    if ext not in loaders:
        raise ValueError(f"Unsupported file type '{ext}'. Use CSV, Excel, or JSON.")
    return loaders[ext](file)
