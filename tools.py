import pandas as pd
import json
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3")

def profile_dataset(df: pd.DataFrame) -> str:
    """Profiles the dataset: columns, dtypes, missing values, and sample rows."""
    profile = {
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "sample_rows": df.head(3).to_dict(orient="records"),
    }
    return json.dumps(profile, indent=2)

def get_cleaning_plan(profile: str) -> str:
    prompt = f"""
    You are a data cleaning assistant.

    Dataset profile:
    {profile}

    Suggest cleaning actions using only these tools:
    - handle_missing_values (strategies: mean, median, mode, drop)
    - remove_duplicates
    - standardize_types (e.g. convert_to_datetime, convert_to_int)
    - clean_strings (e.g. trim_whitespace, lowercase, remove_special_chars)
    - normalize_categories (e.g. unify_labels, one_hot_encode)

    Respond strictly in this JSON format:
    {{
      "actions": [
        {{"tool": "handle_missing_values", "column": "Age", "strategy": "median"}},
        {{"tool": "remove_duplicates"}},
        {{"tool": "standardize_types", "column": "PurchaseDate", "action": "convert_to_datetime"}}
      ]
    }}
    """
    response = llm.invoke(prompt)
    return response
