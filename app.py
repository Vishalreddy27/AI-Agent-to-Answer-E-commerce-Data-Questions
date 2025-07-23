import streamlit as st
import pandas as pd
import sqlparse
from llm.query_generator import generate_sql_and_output  # updated
from utils.schema_reader import get_schema_context
from utils.charts import show_charts

# Default values
MODEL_OPTIONS = {
    "LLaMA 3 (Local via Ollama)": "llama",
    "Gemini 1.5 Flash (API)": "gemini"
}

# --- UI Configuration ---
st.set_page_config(page_title="🧠 LLM SQL Generator", layout="centered")
st.markdown("<h1 style='text-align:center;'>💬 Ask your Data in Natural Language</h1>", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🧠 SQL Generator Overview")
    selected_model_label = st.selectbox("Choose LLM Model", list(MODEL_OPTIONS.keys()))
    selected_model = MODEL_OPTIONS[selected_model_label]
    st.markdown(f"Using LLM: **`{selected_model_label}`**")

    st.markdown("### 📂 Data Sources")
    st.markdown("""
| Short Name   | File Name                      |
|--------------|-------------------------------|
| `ads`        | `Product-Level Ad Sales and Metrics (mapped).csv`                    |
| `eligibility`| `Product-Level Eligibility Table (mapped).csv`            |
| `sales`      | `Product-Level Total Sales and Metrics (mapped).csv`                  |
""")

    st.markdown("### 💡 Use Cases")
    st.markdown("""
- ✅ Analyze product sales, ads & eligibility  
- 📅 Get sales/ad performance by date or month  
- 🔗 Join data across multiple sheets  
- 💬 Use natural language to get insights  
""")

# --- Query Input ---
query = st.text_input("🔎 What would you like to know from the data?", key="query", help="Ask in plain English...")

if query:
    with st.spinner("🔄 Generating SQL & executing..."):
        try:
            context = get_schema_context()  # the table schema passed to LLM
            sql, result = generate_sql_and_output(query)
            formatted_sql = sqlparse.format(sql.strip(), reindent=True, keyword_case="upper")

            # Display SQL
            st.markdown("### 📄 Generated SQL")
            with st.expander("Click to view SQL"):
                st.code(formatted_sql, language="sql")

            # Display Output
            st.markdown("### 📊 Output")
            if isinstance(result, str):
                st.success(result)
            elif isinstance(result, pd.DataFrame):
                st.dataframe(result)
            elif isinstance(result, list) and all(isinstance(row, (tuple, list)) for row in result):
                df = pd.DataFrame(result)
                st.dataframe(df)
            else:
                st.warning("⚠️ Unexpected result format:")
                st.write(result)

        except Exception as e:
            st.error(f"❌ Error occurred: {e}")


# Somewhere in your Streamlit app
st.header("📉 Insights Dashboard")
show_charts()

# --- Footer ---
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("🛠️ **Developed by: [P.Vishal Reddy](mailto:p.vishalreddy@example.com)**")
