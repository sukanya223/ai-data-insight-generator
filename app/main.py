import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.llm import generate_pandas_code
from app.utils import execute_code

st.set_page_config(page_title="AI Data Insight Generator")

st.title("📊 AI Data Insight Generator")

st.write("Upload a CSV file and ask questions about your data.")

file = st.file_uploader("Upload CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    query = st.text_input("Ask your question")

    if query:
        try:
            code = generate_pandas_code(query, df.columns.tolist())
            st.subheader("Generated Code")
            st.code(code, language="python")

            result = execute_code(code, df)

            st.subheader("Result")
            st.write(result)

            # Plot if possible
            if hasattr(result, "plot"):
                result.plot(kind="bar")
                st.pyplot(plt)

        except Exception as e:
            st.error("Error occurred:")
            st.write(e)