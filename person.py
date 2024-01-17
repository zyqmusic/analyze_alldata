import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取 Excel 文件中的指定 sheet 到 DataFrame
file_path = "data/alldata1218.xlsx"
sheet_name = "AC"
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 提取需要计算 person 相关系数的列
columns_to_compare = ['Threshold', 'Bias', 'RT.M', 'CR.C', 'CR.F', 'CR.P', 'MR', 'TN.P']

# 提取分组列
group_column = 'group(AC=1, AC_new=2)'

# 选择数据并去除含有缺失值的行
data_selected = df[[group_column] + columns_to_compare].dropna()

# 根据分组列拆分数据
group1_data = data_selected[data_selected[group_column] == 1]
group2_data = data_selected[data_selected[group_column] == 2]

# 分别计算两组的 person 相关系数
correlation_group1 = group1_data[columns_to_compare].corr(method='pearson')
correlation_group2 = group2_data[columns_to_compare].corr(method='pearson')

# 打印相关系数
print("Group 1 (AC) - Pearson Correlation Matrix:")
print(correlation_group1)

print("\nGroup 2 (AC_new) - Pearson Correlation Matrix:")
print(correlation_group2)

# 分别绘制两组的热力图
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.heatmap(correlation_group1, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title(f'Group 1 (AC) - Pearson Correlation Heatmap')

plt.subplot(1, 2, 2)
sns.heatmap(correlation_group2, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title(f'Group 2 (AC_new) - Pearson Correlation Heatmap')

plt.tight_layout()
plt.show()
