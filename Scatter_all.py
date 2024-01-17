import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取 Excel 文件为 DataFrame
file_path = "data/hospital.xlsx"
df = pd.read_excel(file_path, sheet_name="all")

# 提取所需列
columns_of_interest = ["age", "Threshold", "Bias"]
df_selected = df[columns_of_interest]

# 绘制 "education age" 列的散点图
plt.figure(figsize=(8, 6))
sns.scatterplot(x="age", y="Threshold", data=df_selected)

# 添加拟合曲线
sns.regplot(x="age", y="Threshold", data=df_selected, scatter=False, color='red')

plt.title("Scatter Plot with Fit Line: Education Age vs Threshold")
plt.show()

# 计算 "education age" 列的均值和标准差
mean_value = df_selected["age"].mean()
std_dev = df_selected["age"].std()

# 去除极端值（mean + 2 * sd）
lower_limit = mean_value - 2 * std_dev
upper_limit = mean_value + 2 * std_dev
df_no_outliers = df_selected[(df_selected["age"] >= lower_limit) & (df_selected["age"] <= upper_limit)]

# 绘制 "education age" 列的散点图（去除极端值）
plt.figure(figsize=(8, 6))
sns.scatterplot(x="age", y="Threshold", data=df_no_outliers)

# 添加拟合曲线
sns.regplot(x="age", y="Threshold", data=df_no_outliers, scatter=False, color='red')

plt.title("Scatter Plot with Fit Line (No Outliers): Age vs Threshold")
plt.show()

# 绘制 "education age" 列的散点图
plt.figure(figsize=(8, 6))
sns.scatterplot(x="age", y="Bias", data=df_selected)

# 添加拟合曲线
sns.regplot(x="age", y="Bias", data=df_selected, scatter=False, color='red')

plt.title("Scatter Plot with Fit Line: Age vs Bias")
plt.show()

# 绘制 "education age" 列的散点图（去除极端值）
plt.figure(figsize=(8, 6))
sns.scatterplot(x="age", y="Bias", data=df_no_outliers)

# 添加拟合曲线
sns.regplot(x="age", y="Bias", data=df_no_outliers, scatter=False, color='red')

plt.title("Scatter Plot with Fit Line (No Outliers): Age vs Bias")
plt.show()
