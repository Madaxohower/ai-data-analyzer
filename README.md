# AI Data Analyzer

An AI-powered data analysis web application built with Streamlit and Groq. Upload any CSV, Excel, or JSON dataset and interact with it using natural language — get instant insights, visualizations, and data quality reports.

---

## Features

- **Natural Language Analysis** — Ask questions about your data in plain English; responses stream in real time
- **3 AI Modes** — Switch between Analyst (insights), Code Gen (Python code), and Cleaner (data quality fixes)
- **3 Groq Models** — LLaMA 3.3 70B, LLaMA 3.1 8B Instant, Mixtral 8x7B
- **Interactive Visualizations** — Auto-generated histograms, correlation heatmap, missing values chart, and category distributions powered by Plotly
- **Column Profiler** — Per-column breakdown of data types, null rates, unique counts, and sample values
- **Quick Prompts** — One-click suggested analyses
- **Export Chat** — Download the full conversation as a `.txt` file
- **Streamlit Cloud Ready** — Deploys in minutes with secret management support

---

## Project Structure

```
ai_data_analyzer/
├── main.py              # Streamlit app — UI, tabs, chat loop
├── config.py            # API key, model list, settings
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore
├── core/
│   ├── loader.py        # File ingestion (CSV, Excel, JSON)
│   └── analyzer.py      # Groq API streaming + AI modes
└── utils/
    ├── formatter.py     # DataFrame → prompt context builder
    ├── profiler.py      # Smart column profiling (dataclasses)
    └── visualizer.py    # Plotly chart generators
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Madaxohower/ai-data-analyzer.git
cd ai-data-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy `.env.example` to `.env` and add your APIkey

```bash
cp .env.example .env
```

```env
AI_API_KEY=your_ai_api_key_here
```
### 5. Run the app

```bash
streamlit run main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage

1. **Upload** a CSV, Excel, or JSON file from the sidebar
2. **Select** a model and analysis mode
3. **Ask** a question or click a quick prompt
4. Switch to the **Visualize** tab for auto-generated charts
5. Switch to the **Profile** tab for a full column breakdown

### Example Prompts

```
Summarize this dataset and highlight key insights
Identify data quality issues and suggest fixes
What are the strongest correlations in this data?
Identify outliers and anomalies
Generate Python code for exploratory data analysis
```

---

## Deployment (Streamlit Cloud)

1. Push the project to a **public GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set the main file path to `main.py`
4. Under **Advanced settings → Secrets**, add:

```toml
AI_API_KEY = YOUR_API_KEY
```

5. Click **Deploy** — the app will be live in under a minute

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [Groq](https://groq.com) | LLM inference API |
| [Pandas](https://pandas.pydata.org) | Data loading and processing |
| [Plotly](https://plotly.com) | Interactive visualizations |
| [Python-dotenv](https://pypi.org/project/python-dotenv/) | Local environment variables |

---
