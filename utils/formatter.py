import pandas as pd
from config import MAX_CONTEXT_ROWS


def build_context(df: pd.DataFrame) -> str:
    col_info = "\n".join(
        f"  {col} ({dtype}) — {df[col].isnull().mean() * 100:.1f}% null"
        for col, dtype in df.dtypes.items()
    )
    parts = [
        f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns",
        f"Columns: {', '.join(df.columns.tolist())}",
        f"\nColumn types & null rates:\n{col_info}",
        "\nStatistical summary:\n" + df.describe(include="all").to_string(),
        f"\nFirst {min(MAX_CONTEXT_ROWS, len(df))} rows:\n"
        + df.head(MAX_CONTEXT_ROWS).to_string(index=False),
    ]
    return "\n".join(parts)