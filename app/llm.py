def generate_pandas_code(question, columns):
    question = question.lower()

    if "total sales by product" in question:
        return "result = df.groupby('product')['sales'].sum()"

    elif "sales by region" in question:
        return "result = df.groupby('region')['sales'].sum()"

    elif "average sales" in question:
        return "result = df['sales'].mean()"

    elif "top product" in question:
        return "result = df.groupby('product')['sales'].sum().sort_values(ascending=False).head(1)"

    elif "count" in question:
        return "result = df.count()"

    else:
        return "result = df.head()"