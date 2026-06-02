import pandas as pd
import streamlit as st

from config import AI_API_KEY, MODELS, DEFAULT_MODEL
from core.loader import load_file
from core.analyzer import stream_response, MODES
from utils.formatter import build_context
from utils.profiler import profile, DataProfile
from utils.visualizer import (
    numeric_distributions,
    correlation_heatmap,
    missing_values_chart,
    top_categories,
)

SUGGESTED_PROMPTS = [
    "Summarize this dataset and highlight key insights",
    "Identify data quality issues and suggest fixes",
    "What are the strongest correlations in this data?",
    "Identify outliers and anomalies",
    "Generate Python code for exploratory data analysis",
]

st.set_page_config(page_title="Groq Data Analyzer", page_icon="📊", layout="wide")

if not AI_API_KEY:
    st.error("AI_API_KEY not found. Copy .env.example to .env and add your key.")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📊 Groq Data Analyzer")
    st.caption("AI-powered data analysis")

    uploaded = st.file_uploader(
        "Upload Dataset",
        type=["csv", "xlsx", "xls", "json"],
        help="Supports CSV, Excel, and JSON",
    )
    if uploaded:
        try:
            df = load_file(uploaded)
            st.session_state.update({
                "df": df,
                "context": build_context(df),
                "data_profile": profile(df),
                "messages": [],
                "filename": uploaded.name,
            })
            st.success(f"{df.shape[0]:,} rows × {df.shape[1]} columns loaded.")
        except Exception as exc:
            st.error(str(exc))

    st.divider()

    selected_model = st.selectbox("Model", list(MODELS.keys()))
    selected_mode = st.selectbox(
        "Mode",
        list(MODES.keys()),
        help="Analyst: insights  |  Code Gen: Python code  |  Cleaner: data quality",
    )
    st.divider()

    if st.session_state.get("messages"):
        if st.button("Clear Chat", width="stretch"):
            st.session_state["messages"] = []
            st.rerun()

        chat_export = "\n\n".join(
            f"{'You' if m['role'] == 'user' else 'AI'}: {m['content']}"
            for m in st.session_state["messages"]
        )
        st.download_button(
            "Export Chat",
            data=chat_export,
            file_name="chat_export.txt",
            mime="text/plain",
            width="stretch",
        )

# ── Session init ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "df" not in st.session_state:
    st.info("👈 Upload a dataset from the sidebar to get started.")
    st.stop()

df: pd.DataFrame = st.session_state["df"]
data_profile: DataProfile = st.session_state["data_profile"]

# cast mixed-type object columns to string so Arrow serialization never fails
def _safe_display(frame: pd.DataFrame) -> pd.DataFrame:
    obj_cols = frame.select_dtypes(include=["object", "str"]).columns
    return frame.astype({c: str for c in obj_cols})

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_chat, tab_viz, tab_profile = st.tabs(["💬 Chat", "📈 Visualize", "🔍 Profile"])

# ── Chat Tab ──────────────────────────────────────────────────────────────────
with tab_chat:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing", int(df.isnull().sum().sum()))
    c4.metric("Duplicates", data_profile.duplicate_rows)

    with st.expander("Data Preview", expanded=False):
        st.dataframe(_safe_display(df.head(10)), width="stretch")

    st.divider()
    st.caption("Quick prompts — click to run:")

    cols = st.columns(len(SUGGESTED_PROMPTS))
    for i, text in enumerate(SUGGESTED_PROMPTS):
        if cols[i].button(text[:28] + "…", key=f"sp_{i}", width="stretch"):
            st.session_state["pending_prompt"] = text

    st.divider()

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask anything about your data...")
    prompt = st.session_state.pop("pending_prompt", None) or user_input

    if prompt:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.write_stream(
                stream_response(
                    data_context=st.session_state["context"],
                    messages=st.session_state["messages"],
                    model=MODELS[selected_model],
                    mode=selected_mode,
                )
            )

        st.session_state["messages"].append(
            {"role": "assistant", "content": response}
        )

# ── Visualize Tab ─────────────────────────────────────────────────────────────
with tab_viz:
    if not data_profile.numeric_cols and not data_profile.categorical_cols:
        st.info("No plottable columns found in this dataset.")
    else:
        if data_profile.numeric_cols:
            st.plotly_chart(
                numeric_distributions(df, data_profile.numeric_cols),
                width="stretch",
            )

        if len(data_profile.numeric_cols) >= 2:
            st.plotly_chart(
                correlation_heatmap(df, data_profile.numeric_cols),
                width="stretch",
            )

    missing_fig = missing_values_chart(df)
    if missing_fig:
        st.plotly_chart(missing_fig, width="stretch")
    else:
        st.success("No missing values found.")

    if data_profile.categorical_cols:
        st.subheader("Category Distribution")
        selected_cat = st.selectbox(
            "Select column",
            data_profile.categorical_cols
        )
        st.plotly_chart(
            top_categories(df, selected_cat),
            width="stretch"
        )

# ── Profile Tab ───────────────────────────────────────────────────────────────
with tab_profile:
    st.subheader(
        f"Column Profiles — {st.session_state.get('filename', 'dataset')}"
    )

    profile_rows = [
        {
            "Column": col.name,
            "Type": col.dtype,
            "Null %": f"{col.null_pct}%",
            "Unique": col.unique_count,
            "Samples": ", ".join(str(v) for v in col.sample_values),
        }
        for col in data_profile.columns
    ]

    st.dataframe(
        pd.DataFrame(profile_rows),
        width="stretch",
        hide_index=True,
    )