import pandas as pd
import json
from eda import generate_plots, summarize_dataset
from report import generate_pdf_report
from tools import profile_dataset, get_cleaning_plan
from executor import execute_cleaning_plan

# Load dataset
df = pd.read_csv("data/Sample.csv")

# Step 1: Profile dataset
profile = profile_dataset(df)
print("\n=== Dataset Profile ===\n")
print(profile)

# Step 2: Ask LLM for cleaning plan
plan = get_cleaning_plan(profile)
print("\n=== Raw LLM Response ===\n")
print(plan)

# Step 3: Parse JSON safely
try:
    actions = json.loads(plan)
    print("\n=== Parsed Cleaning Plan ===\n")
    print(json.dumps(actions, indent=2))
except Exception as e:
    print("\n⚠️ Could not parse JSON:", e)
    actions = {"actions": []}  # fallback to empty list if parsing fails

# Step 4: Apply cleaning plan
cleaned_df = execute_cleaning_plan(df, actions)

print("\n=== Cleaned DataFrame Preview ===\n")
print(cleaned_df)

# Step 5: EDA summary
summary = summarize_dataset(cleaned_df)
print("\n=== EDA Summary ===\n")
print(summary)

# Step 6: Generate charts
generate_plots(cleaned_df)
print("\n✅ Plots saved to eda_plots/ directory")

# Step 7: Generate PDF report
generate_pdf_report(
    df=cleaned_df,
    actions=actions,
    summary=summary,
    plot_dir="eda_plots",
    output_file="Data_Analysis_Report.pdf"
)