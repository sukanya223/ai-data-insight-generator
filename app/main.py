import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from llm import generate_pandas_code
from utils import execute_code

# Page config
st.set_page_config(page_title="AI Data Insight Generator", layout="wide")

# Header
st.markdown("""
<h1 style='text-align: center;'>📊 AI Data Insight Generator</h1>
<p style='text-align: center; color: gray;'>Turn your data into actionable insights instantly</p>
<hr>
""", unsafe_allow_html=True)

# Upload Section
st.subheader("📁 Upload Your Dataset")
file = st.file_uploader("Upload CSV", type=["csv"])

if file is not None:
    try:
        df = pd.read_csv(file)
    except:
        st.error("Invalid file. Please upload a valid CSV.")
        st.stop()

    # Data Preview (Expandable)
    with st.expander("🔍 Preview Data"):
        st.dataframe(df.head())

    # KPI Section
    st.markdown("## 📊 Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows", len(df))

    if "sales" in df.columns:
        col2.metric("Total Sales", f"{df['sales'].sum():,.0f}")
        col3.metric("Average Sales", f"{df['sales'].mean():,.2f}")
    else:
        col2.metric("Columns", len(df.columns))
        col3.metric("Non-null Values", df.count().sum())

    # Top Insights Section
    st.markdown("## 💡 Top Insights")

    insights = []

    if "sales" in df.columns:
        insights.append(f"💡 Total sales: {df['sales'].sum():,.0f}")

    if "product" in df.columns and "sales" in df.columns:
        top_product = df.groupby("product")["sales"].sum().idxmax()
        insights.append(f"💡 Top product: {top_product}")

    if "region" in df.columns and "sales" in df.columns:
        top_region = df.groupby("region")["sales"].sum().idxmax()
        insights.append(f"💡 Top region: {top_region}")

    for insight in insights:
        st.success(insight)

    # Query Section
    st.markdown("## 🔍 Ask Questions")

    query = st.text_input("Type your question (e.g., Total sales by product)")

    if query:
        try:
            code = generate_pandas_code(query, df.columns.tolist())

            with st.expander("🧠 Generated Code"):
                st.code(code, language="python")

            result = execute_code(code, df)

            st.markdown("## 📈 Results")
            st.write(result)

            # Plot
            try:
                if hasattr(result, "plot"):
                    result.plot(kind="bar")
                    st.pyplot(plt)
            except:
                pass

            # Download Report
            if isinstance(result, pd.Series):
                result_df = result.reset_index()
            elif isinstance(result, pd.DataFrame):
                result_df = result
            else:
                result_df = pd.DataFrame({"Result": [result]})

            csv = result_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Download Report",
                data=csv,
                file_name="analysis_report.csv",
                mime="text/csv"
            )

            # Insight Section
            st.markdown("## 📊 Insight")

            if "sales" in query.lower() and "sales" in df.columns:
                st.info(f"Total sales is {df['sales'].sum():,.0f}, showing overall performance.")

            elif "product" in query.lower() and "sales" in df.columns:
                top_product = df.groupby("product")["sales"].sum().idxmax()
                st.info(f"{top_product} is the highest performing product.")

            elif "region" in query.lower() and "sales" in df.columns:
                top_region = df.groupby("region")["sales"].sum().idxmax()
                st.info(f"{top_region} region generates the highest revenue.")

            else:
                st.info("General data trends displayed.")

            # Explain Button
            if st.button("🧠 Explain Result"):
                st.write("This result highlights patterns and trends derived from your dataset to support decision-making.")

        except Exception as e:
            st.error("Something went wrong")
            st.write(e)