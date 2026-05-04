import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from llm import generate_pandas_code
from utils import execute_code
from rag import retrieve_columns, retrieve_rows

st.set_page_config(page_title="AI Data Insight Generator", layout="wide")

st.title("📊 AI Data Insight Generator")
st.write("Upload a dataset and ask questions.")

file = st.file_uploader("Upload CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    # Preview
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # KPI
    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", len(df))

    if "sales" in df.columns:
        col2.metric("Total Sales", int(df["sales"].sum()))
        col3.metric("Avg Sales", round(df["sales"].mean(), 2))

    # Query
    query = st.text_input("Ask your question")

    if query:

        # ⭐ RAG Retrieval
        relevant_cols = retrieve_columns(query, df.columns.tolist())
        relevant_rows = retrieve_rows(df, query)

        st.subheader("🔍 Relevant Columns")
        st.write(relevant_cols)

        st.subheader("🔎 Relevant Rows")
        st.dataframe(relevant_rows)

        # Generate Code
        code = generate_pandas_code(query, df.columns.tolist())

        st.subheader("🧠 Generated Code")
        st.code(code)

        # Execute
        result = execute_code(code, df)

        st.subheader("📈 Result")
        st.write(result)

        # Plot
        try:
            if hasattr(result, "plot"):
                result.plot(kind="bar")
                st.pyplot(plt)
        except:
            pass

        # ⭐ RAG Insight
        st.subheader("📊 RAG Insight")

        if "sales" in relevant_cols:
            st.write(f"Total sales (filtered): {relevant_rows['sales'].sum()}")

        if "product" in relevant_cols and "sales" in df.columns:
            top_product = relevant_rows.groupby("product")["sales"].sum().idxmax()
            st.write(f"Top product: {top_product}")

        if "region" in relevant_cols and "sales" in df.columns:
            top_region = relevant_rows.groupby("region")["sales"].sum().idxmax()
            st.write(f"Top region: {top_region}")