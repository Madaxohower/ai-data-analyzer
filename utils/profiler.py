import pandas as pd
from dataclasses import dataclass


@dataclass
class ColumnProfile:
    name: str
    dtype: str
    null_count: int
    null_pct: float
    unique_count: int
    sample_values: list


@dataclass
class DataProfile:
    shape: tuple[int, int]
    columns: list[ColumnProfile]
    duplicate_rows: int
    numeric_cols: list[str]
    categorical_cols: list[str]
    datetime_cols: list[str]

def profile(df: pd.DataFrame) -> DataProfile:
    return DataProfile(
        shape=df.shape,
        duplicate_rows=int(df.duplicated().sum()),
        numeric_cols=df.select_dtypes(include="number").columns.tolist(),
        categorical_cols=df.select_dtypes(include=["object", "category"]).columns.tolist(),
        datetime_cols=df.select_dtypes(include="datetime").columns.tolist(),
        columns=[
            ColumnProfile(
                name=col,
                dtype=str(df[col].dtype),
                null_count=int(df[col].isnull().sum()),
                null_pct=round(df[col].isnull().mean() * 100, 1),
                unique_count=int(df[col].nunique()),
                sample_values=df[col].dropna().head(3).tolist(),
            )
            for col in df.columns
        ],
    )