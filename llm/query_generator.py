from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.schema_reader import get_schema_context
from langchain.sql_database import SQLDatabase
from sqlalchemy import text
import pandas as pd
import numpy as np
import os

# Set your Gemini API Key
os.environ["GOOGLE_API_KEY"] = "your_gemini_api_key_here"

def is_money_related(question: str) -> bool:
    money_keywords = [
        "amount", "price", "revenue", "income", "sales", "cost", "profit",
        "earning", "total value", "money", "spend", "spent", "expenditure"
    ]
    question_lower = question.lower()
    return any(word in question_lower for word in money_keywords)

def generate_sql_and_output(user_input: str, llm_choice: str = "ollama"):
    db = SQLDatabase.from_uri("sqlite:///db/database.db")
    schema_info = get_schema_context()

    # Select LLM and prompt template
    if llm_choice == "gemini":
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)
        prompt_template = PromptTemplate(
            input_variables=["schema", "question"],
            template="""
You are a professional data analyst assistant. Based on the database schema below, write a syntactically correct SQLite SQL query to answer the given question.
Use correct column names from schema
Instructions:
- Use correct table and column names as per the schema.
- Use functions like SUM, AVG, MAX as needed.
- Format "total sales" as SUM(sales.total_sales) if relevant.
- Fully qualify columns like sales.total_sales, ads.clicks, etc.
- Output should ONLY be a valid SQL query.

Schema:
{schema}

Question:
{question}

SQL Query:
"""
        )
    else:
        llm = Ollama(model="llama3.2:latest", temperature=0.1)
        prompt_template = PromptTemplate(
            input_variables=["schema", "question"],
            template="""
You are an expert SQL generator. Based on the schema provided below, write a valid and executable SQLite SQL query to answer the user's question.

Example:
Output should ONLY be a valid SQL query.
SELECT * FROM sales LIMIT 5
Calculate the RoAS (Return on Ad Spend):
SELECT SUM(CASE WHEN ad_spend > 0 THEN ad_sales / ad_spend ELSE 0 END) FROM ads;

Guidelines:
- Use correct column names from schema
- Interpret "Total sales" as the SUM of the revenue column in the sales table.
- Always use fully qualified column names (e.g., ads.ad_spend, sales.revenue)
- Use proper SQL aggregation functions like SUM(), COUNT(), AVG(), etc.
- Avoid table aliases unless absolutely necessary.
- Return only the SQL query. No explanations, markdown, or extra formatting.

Schema:
{schema}

Question:
{question}

Output:
"""
        )

    # Run LLMChain to generate SQL
    chain = LLMChain(llm=llm, prompt=prompt_template)
    generated_sql = chain.run({
        "schema": schema_info,
        "question": user_input
    }).strip()

    # Execute the generated SQL
    engine = db._engine
    try:
        with engine.connect() as conn:
            result = conn.execute(text(generated_sql)).fetchall()

        if not result:
            return generated_sql, "No results found."

        # If only one value returned
        if len(result) == 1 and len(result[0]) == 1:
            value = result[0][0]
            if isinstance(value, (int, float, np.number)):
                if is_money_related(user_input):
                    return generated_sql, f"₹ {value:,.2f}"
                else:
                    return generated_sql, f"{value}"
            else:
                return generated_sql, str(value)

        # Return as DataFrame
        try:
            df = pd.DataFrame(result, columns=result[0].keys())
        except Exception:
            df = pd.DataFrame(result)

        return generated_sql, df

    except Exception as e:
        return generated_sql, f"❌ SQL Execution Error: {str(e)}"
