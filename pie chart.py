import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Read Excel file into DataFrame, extract CHH sheet
file_path = "data/alldata1218.xlsx"
df_chh = pd.read_excel(file_path, engine='openpyxl', sheet_name='CHH_new')

# Categorize 'age' column
bins = [0, 30, 50, float('inf')]
labels = ['younger', 'adult', 'older']
df_chh['age_group'] = pd.cut(df_chh['age'], bins=bins, labels=labels, right=False)

# Perform t-test for each age group with 'gender(1=female, 2=male)'
for age_group in labels:
    age_group_data = df_chh[df_chh['age_group'] == age_group]
    t_stat_gender, p_value_gender = ttest_ind(
        age_group_data[age_group_data['gender(1=female, 2=male)'] == 1]['age'],
        age_group_data[age_group_data['gender(1=female, 2=male)'] == 2]['age']
    )
    print(f"T-test for {age_group} age group and gender - t-statistic: {t_stat_gender}, p-value: {p_value_gender}")

    # Perform t-test for each age group with 'education age'
    t_stat_education_age, p_value_education_age = ttest_ind(
        age_group_data[age_group_data['gender(1=female, 2=male)'] == 1]['education age'],
        age_group_data[age_group_data['gender(1=female, 2=male)'] == 2]['education age'],
        nan_policy='omit'
    )
    print(f"T-test for {age_group} age group and education age - t-statistic: {t_stat_education_age}, p-value: {p_value_education_age}")

# Check and handle non-numeric values before calculating mean
numeric_columns = df_chh.select_dtypes(include=['number']).columns
df_numeric = df_chh[numeric_columns]

# Calculate mean values for each column
mean_values = df_numeric.mean()
print("\nMean Values:")
print(mean_values)

# Plot pie charts with gradient colors
plt.figure(figsize=(15, 5))

# Define a custom gradient color map for the bins
colors = [
    (32 / 255.0, 112 / 255.0, 180 / 255.0, 1.0),
    (32 / 255.0, 112 / 255.0, 180 / 255.0, 0.7),
    (32 / 255.0, 112 / 255.0, 180 / 255.0, 0.5),
    (32 / 255.0, 112 / 255.0, 180 / 255.0, 0.3),
    (32 / 255.0, 112 / 255.0, 180 / 255.0, 0.1),
]
# 创建颜色映射
cmap = LinearSegmentedColormap.from_list("age_bins", colors, N=len(bins)-1)

# 饼图 for 'gender'
plt.subplot(1, 3, 1)
gender_labels = df_chh['gender(1=female, 2=male)'].map({1: 'Female', 2: 'Male'})
gender_labels.value_counts().plot.pie(autopct='%1.1f%%', labels=gender_labels.unique(), colors=colors)
plt.title('Gender Distribution')

# 饼图 for 'age'
plt.subplot(1, 3, 2)
df_chh['age_group'].value_counts().plot.pie(autopct='%1.1f%%', colors=colors)
plt.title('Age Group Distribution')

# 饼图 for 'education age'
plt.subplot(1, 3, 3)
df_chh['education age'].value_counts().plot.pie(autopct='%1.1f%%', colors=colors)
plt.title('Education Age Distribution')

plt.tight_layout()
plt.show()
