import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Streamlit Cloud stores secrets in st.secrets; fall back to .env locally
try:
    AI_API_KEY: str = st.secrets.get("AI_API_KEY", os.getenv("AI_API_KEY", ""))
except Exception:
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
MODELS: dict[str, str] = {
    "LLaMA 3.3 70B (Best)":   "llama-3.3-70b-versatile",
    "LLaMA 3.1 8B (Fastest)": "llama-3.1-8b-instant",
    "Mixtral 8x7B (Code)":    "mixtral-8x7b-32768",
}

DEFAULT_MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 2048
MAX_CONTEXT_ROWS = 250