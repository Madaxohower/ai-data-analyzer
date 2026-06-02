from typing import Generator
from groq import Groq
from config import AI_API_KEY, DEFAULT_MODEL, MAX_TOKENS

client = Groq(api_key=AI_API_KEY)

MODES: dict[str, str] = {
    "Analyst": (
        "You are a senior data analyst. Given a dataset summary, provide clear and "
        "actionable insights. Use bullet points for lists. Reference specific values, "
        "highlight patterns, anomalies, and trends."
    ),
    "Code Gen": (
        "You are a Python data engineer. Given a dataset summary, generate clean and "
        "runnable Python code using pandas. Always wrap code in ```python blocks and "
        "add a short comment explaining each step."
    ),

 "Cleaner": (
        "You are a data quality expert. Analyze the dataset for missing values, "
        "duplicates, outliers, and inconsistent formatting. Provide specific, "
        "prioritized recommendations with pandas code snippets."
    ),
}

def stream_response(
    data_context: str,
    messages: list[dict],
    model: str = DEFAULT_MODEL,
    mode: str = "Analyst",
) -> Generator[str, None, None]:
    system = MODES.get(mode, MODES["Analyst"])
    full_messages = [
        {"role": "system", "content": f"{system}\n\nDataset:\n{data_context}"},
        *messages,
    ]
    stream = client.chat.completions.create(
        model=model,
        messages=full_messages,
        max_tokens=MAX_TOKENS,
        stream=True,
    )
    for chunk in stream:
        token = chunk.choices[0].delta.content
        if token:
            yield token