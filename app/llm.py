def generate_pandas_code(question, columns):
    question = question.lower()

    if "total" in question and "product" in question:
        return "result = df.groupby('product')['sales'].sum()"

    elif "region" in question:
        return "result = df.groupby('region')['sales'].sum()"

    elif "average" in question:
        return "result = df['sales'].mean()"

    elif "top" in question:
        return "result = df.groupby('product')['sales'].sum().sort_values(ascending=False).head(1)"

    else:
        return "result = df.head()"