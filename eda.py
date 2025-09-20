import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict

def summarize_dataset(df: pd.DataFrame) -> Dict[str, Dict]:
    """
    Returns a summary dictionary:
    - Numeric columns: mean, median, std, min, max
    - Categorical columns: value counts (including bools and low-cardinality numerics)
    """
    summary = {}

    # Numeric columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    summary['numeric'] = df[numeric_cols].describe().to_dict()

    # Categorical columns (object, category, bool)
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

    # Include numeric columns with low unique values as categorical
    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        if df[col].nunique() <= 10 and col not in categorical_cols:
            categorical_cols.append(col)

    # Generate categorical counts
    summary['categorical'] = {col: df[col].value_counts().to_dict() for col in categorical_cols}

    return summary


def generate_plots(df: pd.DataFrame, output_dir="eda_plots") -> None:
    """
    Generate and save plots for numeric and categorical columns.
    Numeric: histograms with KDE
    Categorical: bar plots
    """
    os.makedirs(output_dir, exist_ok=True)

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

    # Include low-cardinality numeric columns as categorical
    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        if df[col].nunique() <= 10 and col not in categorical_cols:
            categorical_cols.append(col)

    # Numeric plots
    for col in numeric_cols:
        plt.figure()
        sns.histplot(df[col], kde=True, bins=20)
        plt.title(f"{col} distribution")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/{col}_hist.png")
        plt.close()

    # Categorical plots
    for col in categorical_cols:
        plt.figure()
        df[col].value_counts().plot(kind='bar')
        plt.title(f"{col} counts")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/{col}_bar.png")
        plt.close()
