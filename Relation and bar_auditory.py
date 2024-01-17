import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# Read the Excel file into a DataFrame
file_path = "data/alldata1218.xlsx"
df = pd.read_excel(file_path, sheet_name="all")

# Select columns of interest
columns_of_interest = ["age", "Threshold", "Bias"]

# Select columns
df_selected = df[columns_of_interest]

# Convert non-numeric columns to numeric, set non-convertible values to NaN
df_selected = df_selected.apply(pd.to_numeric, errors='coerce')

# Fill missing values with NaN
df_selected.fillna(value=np.nan, inplace=True)

# Handle missing values for NaT type
for column in df_selected.columns:
    if pd.api.types.is_datetime64_any_dtype(df_selected[column]):
        df_selected[column] = df_selected[column].astype('float64')

# Calculate Spearman correlations with age, ignoring missing values
correlation_results = {}
for column in df_selected.columns:
    if column != "age":
        correlation_results[column] = spearmanr(df_selected["age"], df_selected[column], nan_policy='omit').correlation

# Print results
print("Spearman Correlation with age:")
print(f"{df_selected['age'].name}: {1.0}")  # The correlation of age with itself is 1
for column, correlation in correlation_results.items():
    print(f"{column}: {correlation}")

# Plot linear regression graphs with regression curves
for column in df_selected.columns:
    if column != "age":
        plt.figure(figsize=(12, 8))
        sns.regplot(x="age", y=column, data=df_selected[["age", column]])
        plt.title(f"Regression plot between age and {column}")
        plt.xlabel("age")
        plt.ylabel(column)
        plt.show()

# Plot bar graphs for every 0.25 years on the y-axis
plt.figure(figsize=(12, 8))
threshold_bins = np.arange(df_selected["Threshold"].min(), df_selected["Threshold"].max() + 0.25, 0.25)
sns.histplot(df_selected, x="Threshold", bins=threshold_bins, stat="count", kde=False, color="skyblue")
plt.title("Bar Plot: Count of Threshold (Bars every 0.25 threshold)")
plt.xlabel("Threshold")
plt.ylabel("Count")
plt.show()

# Plot bar graphs for every 0.25 years on the y-axis
plt.figure(figsize=(12, 8))
bias_bins = np.arange(df_selected["Bias"].min(), df_selected["Bias"].max() + 0.25, 0.25)
sns.histplot(df_selected, x="Bias", bins=bias_bins, stat="count", kde=False, color="salmon")
plt.title("Bar Plot: Count of Bias (Bars every 0.25 Bias)")
plt.xlabel("Bias")
plt.ylabel("Count")
plt.show()
