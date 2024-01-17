import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import spearmanr

# 读取Excel文件中的sheet
file_path = "data/alldata1218.xlsx"
sheet_name = "all"
df = pd.read_excel(file_path, sheet_name)

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

# Plot scatter plots with vertical regression line and count valid data points
for column in df_selected.columns:
    if column != "age":
        plt.figure(figsize=(12, 8))
        ax = sns.regplot(x=column, y="age", data=df_selected[["age", column]], scatter_kws={'color': 'skyblue'},
                        fit_reg=False)

        # Add vertical regression line at the mean of the x-axis values
        mean_x = df_selected[column].mean()
        plt.axvline(x=mean_x, color='red', linestyle='--', label=f'Mean {column}')

        # Count and print the number of valid data points
        valid_data_points = df_selected[[column, "age"]].dropna()
        count = len(valid_data_points)
        plt.title(f"Scatter plot between {column} and age with Vertical Regression Line (n={count})")
        plt.xlabel(column)
        plt.ylabel("age")
        plt.legend()
        plt.show()
