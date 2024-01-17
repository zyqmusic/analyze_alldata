import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取 Excel 文件中的指定 sheet 为 DataFrame
file_path = "data/alldata1218.xlsx"
df = pd.read_excel(file_path, engine='openpyxl', sheet_name='all')

# 选择需要计算 Pearson 相关系数的列
columns_to_corr = ['RT.M', 'RT.K', 'CR.C', 'CR.F', 'CR.P', 'MR', 'TN.P', 'Threshold', 'Bias', 'AC_TS']

# 去除包含 0 值的行
df_filtered = df[columns_to_corr]

# 计算 Pearson 相关系数矩阵
correlation_matrix = df_filtered.corr()

# 设置字体大小
plt.rcParams.update({'font.size': 12})

# 创建热力图
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)

plt.title('Heatmap of Pearson Correlation Coefficients for Auditory Categorization')
plt.show()
