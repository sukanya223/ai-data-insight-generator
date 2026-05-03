from openai import OpenAI
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_pandas_code(question, columns):
    prompt = f"""
You are a data analyst.

Given a pandas dataframe named df with columns: {columns}

Convert the user's question into pandas code.

IMPORTANT:
- Store final answer in variable called result
- Only return python code
- Do not explain anything

Question: {question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    code = response.choices[0].message.content
    code = code.replace("```python", "").replace("```", "")
    return code