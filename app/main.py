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

    # 📊 Data Preview
    st.subheader("Data Preview")
    st.dataframe(df.head())

    # 📊 KPI Cards
    st.subheader("📊 Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows", len(df))

    if "sales" in df.columns:
        col2.metric("Total Sales", int(df["sales"].sum()))
        col3.metric("Average Sales", round(df["sales"].mean(), 2))
    else:
        col2.metric("Columns", len(df.columns))
        col3.metric("Non-null values", df.count().sum())

    # 🔍 Query Input
    query = st.text_input("Ask your question")

    if query:
        try:
            # Generate pandas code
            code = generate_pandas_code(query, df.columns.tolist())

            st.subheader("Generated Code")
            st.code(code, language="python")

            # Execute code
            result = execute_code(code, df)

            st.subheader("Result")
            st.write(result)

            # 📊 Plot (if possible)
            try:
                if hasattr(result, "plot"):
                    result.plot(kind="bar")
                    st.pyplot(plt)
            except:
                pass

            # ⭐ Convert result to DataFrame for download
            if isinstance(result, pd.Series):
                result_df = result.reset_index()
            elif isinstance(result, pd.DataFrame):
                result_df = result
            else:
                result_df = pd.DataFrame({"Result": [result]})

            # ⭐ Download Button
            csv = result_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Download Report",
                data=csv,
                file_name="analysis_report.csv",
                mime="text/csv"
            )

            st.success("Report ready for download 🚀")

            # 📊 Smart Insights
            st.subheader("📊 Insight")

            if "sales" in query.lower() and "sales" in df.columns:
                st.write(f"Total sales is {df['sales'].sum()}, indicating overall performance.")

            elif "product" in query.lower() and "sales" in df.columns:
                top_product = df.groupby("product")["sales"].sum().idxmax()
                st.write(f"Product {top_product} is the top performer based on sales.")

            elif "region" in query.lower() and "sales" in df.columns:
                top_region = df.groupby("region")["sales"].sum().idxmax()
                st.write(f"Region {top_region} contributes the highest sales.")

            else:
                st.write("Basic data trends observed from dataset.")

            # 🔥 Explain Button
            if st.button("Explain Result"):
                st.write("This result shows patterns and trends extracted from your dataset for decision-making.")

        except Exception as e:
            st.error("Error occurred:")
            st.write(e)