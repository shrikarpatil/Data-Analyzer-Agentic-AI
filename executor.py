import pandas as pd

def execute_cleaning_plan(df: pd.DataFrame, actions: dict) -> pd.DataFrame:
    """
    Applies the cleaning plan (from LLM JSON) to the DataFrame.

    Parameters:
        df: pandas DataFrame
        actions: dict, LLM-generated JSON with cleaning steps

    Returns:
        df: cleaned DataFrame
    """
    for action in actions.get("actions", []):
        tool = action.get("tool")

        if tool == "remove_duplicates":
            df = df.drop_duplicates()
            print("✅ Removed duplicates")

        elif tool == "handle_missing_values":
            col = action.get("column")
            strat = action.get("strategy", "mean")

            if col not in df.columns:
                print(f"⚠️ Column {col} not found for missing values.")
                continue

            if strat == "median":
                df[col] = df[col].fillna(df[col].median())
            elif strat == "mean":
                df[col] = df[col].fillna(df[col].mean())
            elif strat == "mode":
                df[col] = df[col].fillna(df[col].mode()[0])
            elif strat == "drop":
                df = df.dropna(subset=[col])
            print(f"✅ Handled missing values for column {col} using {strat}")

        elif tool == "standardize_types":
            col = action.get("column")
            act = action.get("action")

            if col not in df.columns:
                print(f"⚠️ Column {col} not found for type standardization.")
                continue

            if act == "convert_to_datetime":
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif act == "convert_to_int":
                df[col] = pd.to_numeric(df[col], errors='coerce', downcast='integer')
            elif act == "convert_to_float":
                df[col] = pd.to_numeric(df[col], errors='coerce', downcast='float')
            print(f"✅ Standardized column {col} with action {act}")

        

        else:
            print(f"⚠️ Unknown tool: {tool}")

    return df
