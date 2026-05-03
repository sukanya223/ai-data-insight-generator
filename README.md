# AI Data Insight Generator

An AI-powered data analytics tool that enables users to explore datasets using natural language queries and generate actionable insights, visualizations, and downloadable reports.

---

##  Overview

AI Data Insight Generator is a lightweight analytics system that allows users to:
- Upload CSV datasets
- Ask questions in natural language
- Generate insights and visualizations
- Export analysis reports

This project simulates a real-world AI analytics assistant using a hybrid rule-based NLP system.

---

##  Features

-  Upload and analyze CSV datasets
-  KPI Dashboard (Total Rows, Sales, Averages)
-  Automatic Insight Generation (Top 3 insights)
-  Natural Language Query → Data Analysis
-  Data Visualization (charts)
-  Downloadable Reports (CSV)
-  Explain Results Feature
-  Clean and interactive UI (Streamlit-based)

---

##  How It Works

1. User uploads a dataset
2. System analyzes structure and key metrics
3. User asks a question (e.g., "Total sales by product")
4. Query is converted into executable Pandas code
5. Results are displayed with charts and insights
6. User can download the report

---

##  Tech Stack

- **Python**
- **Pandas**
- **Streamlit**
- **Matplotlib**
- Rule-based NLP (for query understanding)

---

##  Example Queries

- Total sales by product
- Sales by region
- Average sales
- Top performing product


## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/sukanya223/ai-data-insight-generator.git
cd ai-data-insight-generator
