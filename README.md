🧠 AI SQL Agent for E-commerce Analytics
An intelligent AI-powered SQL agent that lets you ask questions in plain English and get insights from your e-commerce data. It uses a local LLaMA3 LLM via Ollama, processes your uploaded Excel sheets into SQL tables, auto-generates accurate SQL queries, and delivers data results and visualizations—all in a clean Streamlit interface.
🚀 Features
💬 Natural Language to SQL using local LLaMA 3.2 (via Ollama)
📊 Excel uploads auto-converted to SQL tables
📄 RAG-enhanced query generation with LangChain
🧠 Schema-aware LLM responses
📈 Visual output: Tables, charts, and summary insights
⚡ Fast, private, and fully local (no API required unless using Gemini)
🔐 Modular design for easy debugging, extensibility, and clean logs
project/
├── app.py # Streamlit app entry point
├── data/ # Raw Excel/CSV data files
│ ├── sales.xlsx
│ ├── ads.xlsx
│ └── eligibility.xlsx
├── db/
│ ├── database.db # SQLite DB (auto-created)
│ └── load_data.py # Converts Excel to SQL tables
├── llm/
│ └── query_generator.py # LangChain + LLaMA/Gemini SQL generator
├── utils/
│ ├── schema_reader.py # Extracts DB schema for LLM input
│ └── charts.py # Auto-generates Plotly charts from query results
├── requirements.txt # Python dependencies
└── .gitignore # Ignores venv, DB, logs, Excel, etc.
