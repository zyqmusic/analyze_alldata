import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# 读取Excel文件中的sheet
file_path = "data/alldata1218.xlsx"
sheet_name = "(non)music"
df = pd.read_excel(file_path, sheet_name)

# 提取age、Threshold和Bias列
age = df['age']
threshold = df['Threshold']
bias = df['Bias']
group = df['group(music=1, nonmusic=2)']

# 删除包含无穷大或非数值的样本
valid_indices = np.isfinite(age) & np.isfinite(bias)  # 注意这里用bias列
age_valid = age[valid_indices]
bias_valid = bias[valid_indices]

# 绘制散点图
plt.scatter(age_valid[group[valid_indices] == 1], bias_valid[group[valid_indices] == 1], c='skyblue', label='music', edgecolors='black')
plt.scatter(age_valid[group[valid_indices] == 2], bias_valid[group[valid_indices] == 2], c='salmon', label='nonmusic', edgecolors='black')

# 添加x轴和y轴标签
plt.xlabel('Age')
plt.ylabel('Bias')

# 添加图例
plt.legend()

# 在右上角写出不同颜色对应group的label
plt.text(0.95, 0.95, 'music', color='skyblue', ha='right', va='top')
plt.text(0.95, 0.90, 'nonmusic', color='salmon', ha='right', va='top')

# 数据拟合
def func(x, a, b):
    return a * x + b

# 使用curve_fit进行拟合
params, covariance = curve_fit(func, age_valid, bias_valid)

# 生成拟合曲线的x值
x_fit_curve = np.linspace(min(age_valid), max(age_valid), 100)
# 计算拟合曲线的y值
y_fit_curve = func(x_fit_curve, *params)

# 绘制拟合曲线
plt.plot(x_fit_curve, y_fit_curve, color='forestgreen', label='Fit Curve')

# 显示图形
plt.show()
