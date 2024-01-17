import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm

# 读取Excel文件中的sheet
file_path = "data/alldata1218.xlsx"
sheet_name = "all"
df = pd.read_excel(file_path, sheet_name)

# 选择列
column_of_interest = "Bias"
data = df[column_of_interest]

# 计算均值、中位数和标准差
mean_value = data.mean()
median_value = data.median()  # 添加计算中位数
std_dev = data.std()

# 计算截断点
cutoff_value = mean_value + 2 * std_dev

# 绘制直方图
plt.figure(figsize=(12, 8))
sns.histplot(data, bins=30, kde=True, color='skyblue')

# 绘制均值、中位数和标准差的线
plt.axvline(median_value, color='blue', linestyle='dashed', linewidth=2, label='Median')
plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label='Mean')
plt.axvline(mean_value - std_dev, color='orange', linestyle='dashed', linewidth=2, label='Mean +/- 1 SD')
plt.axvline(mean_value - 2 * std_dev, color='green', linestyle='dashed', linewidth=2, label='Mean +/- 2 SD')
plt.axvline(mean_value + std_dev, color='orange', linestyle='dashed', linewidth=2)  # 添加 mean + 1 SD
plt.axvline(mean_value + 2 * std_dev, color='green', linestyle='dashed', linewidth=2)  # 添加 mean + 2 SD

# 绘制正态分布曲线
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mean_value, std_dev)
plt.plot(x, p, 'k', linewidth=2, label='Normal Distribution')

# 添加标签和图例
plt.title(f"Distribution of {column_of_interest}")
plt.xlabel(column_of_interest)
plt.ylabel("Frequency")
plt.legend()

# 显示图形
plt.show()
