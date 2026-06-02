import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def numeric_distributions(df: pd.DataFrame, cols: list[str]) -> go.Figure:
    n = len(cols)
    ncols = min(n, 3)
    nrows = (n + ncols - 1) // ncols
    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=cols)
    for i, col in enumerate(cols):
        fig.add_trace(
            go.Histogram(x=df[col], name=col, showlegend=False),
            row=i // ncols + 1,
            col=i % ncols + 1,
        )
    fig.update_layout(height=280 * nrows, title_text="Numeric Distributions")
    return fig


def correlation_heatmap(df: pd.DataFrame, cols: list[str]) -> go.Figure:
    corr = df[cols].corr()
    return px.imshow(
        corr,
        text_auto=".2f",
        title="Correlation Matrix",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
    )

def missing_values_chart(df: pd.DataFrame) -> go.Figure | None:
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=True)
    if missing.empty:
        return None
    return px.bar(
        x=missing.values,
        y=missing.index,
        orientation="h",
        labels={"x": "Missing Count", "y": "Column"},
        title="Missing Values by Column",
    )


def top_categories(df: pd.DataFrame, col: str, top_n: int = 10) -> go.Figure:
    counts = df[col].value_counts().head(top_n)
    return px.bar(
        x=counts.index.astype(str),
        y=counts.values,
        labels={"x": col, "y": "Count"},
        title=f"Top {top_n} — {col}",
    )