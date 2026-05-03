def execute_code(code, df):
    local_vars = {"df": df}

    try:
        exec(code, {}, local_vars)
        return local_vars.get("result", "No result returned")
    except Exception as e:
        return f"Error: {e}"