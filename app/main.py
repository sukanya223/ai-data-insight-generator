import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from llm import generate_pandas_code
from utils import execute_code

st.set_page_config(page_title="AI Data Insight Generator")

st.title("📊 AI Data Insight Generator")
st.write("Upload a CSV file and ask questions about your data.")

file = st.file_uploader("Upload CSV", type=["csv"])

if file is not None:
    try:
        df = pd.read_csv(file)
    except Exception:
        st.error("Invalid or empty CSV file. Please upload a valid dataset.")
        st.stop()

    st.subheader("Data Preview")
    st.dataframe(df.head())

    query = st.text_input("Ask your question")

    if query:
        try:
            # Generate code
            code = generate_pandas_code(query, df.columns.tolist())
            st.subheader("Generated Code")
            st.code(code, language="python")

            # Execute code
            result = execute_code(code, df)

            st.subheader("Result")
            st.write(result)

            # Plot if possible
            try:
                if hasattr(result, "plot"):
                    result.plot(kind="bar")
                    st.pyplot(plt)
            except:
                pass

            # Insight Section
            st.subheader("📊 Insight")

            if "sales" in query.lower():
                st.write("Sales distribution analyzed successfully.")
            elif "product" in query.lower():
                st.write("Top performing products identified based on sales.")
            elif "region" in query.lower():
                st.write("Regional performance comparison generated.")
            else:
                st.write("Basic data analysis generated.")

        except Exception as e:
            st.error("Error occurred:")
            st.write(e)