import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import numpy as np

# 读取Excel文件
file_path = "data/hospital.xlsx"
sheet_name = "H_TRR"
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 选择需要的行范围
data1 = df.loc[2:20, "number"]
data2 = df.loc[21:39, "number"]

# 计算data1和data2中指定列的均值
columns_of_interest = [
    "Time difference between dyslexic and non-dyslexic reading",
    "Non-impaired reading time",
    "Impaired reading time",
    "ST_TS",
    "Distraction time",
    "Correct rate of color selection",
    "AS_TS",
    "Choose the hit ratio of T",
    "Leakage rate",
    "Choose the average reaction time for each T",
    "Click the average order of red T",
    "The success rate when T appears in the upper left area",
    "The success rate when T appears in the upper right area",
    "The success rate of the search when T appears in the lower left area",
    "The success rate when T appears in the lower right area",
    "VS_TS",
    "Accuracy of Positive Selection (%)",
    "Accuracy of Negative Selection (%)",
    "Reaction Time for Positive Selection (milliseconds)",
    "Reaction Time for Negative Selection (milliseconds)",
    "Stop Signal Reaction Time (milliseconds)",
    "Stop Signal Success Rate (%)",
    "Effect Size, RT.A - RT.P (milliseconds)",
    "ASN_TS",
    "Low difficulty average error (degrees)",
    "High difficulty average error (degrees)",
    "Long-term memory accuracy (%)",
    "Memory test total score",
    "Hearing total accuracy (%)",
    "High pitch accuracy rate (%)",
    "Average Reaction Time for High Tones(ms)",
    "Accuracy Rate for Low Tones (%)",
    "Average Reaction Time for Low Tones (ms)",
    "AD_TS",
    "Probability of Switching Strategy when Facing Low Probability Events (%)",
    "Number of Occurrences of Low Probability Events",
    "Flexibility in Switching Strategy (%)",
    "DC_TS",
    "RT.M",
    "RT.K",
    "CR.C",
    "CR.F",
    "CR.P",
    "MR",
    "TN.P",
    "Threshold",
    "Bias",
    "AC_TS"
]

# 提取data1和data2中指定列的数据，并将number列转换为数值类型
data1_values = df.loc[2:20, columns_of_interest].apply(pd.to_numeric, errors='coerce')
data2_values = df.loc[21:39, columns_of_interest].apply(pd.to_numeric, errors='coerce')

# 使用NaN填充缺失值
data1_values.fillna(value=pd.NA, inplace=True)
data2_values.fillna(value=pd.NA, inplace=True)

# 循环计算每一列的均值和Pearson相关系数
for col in columns_of_interest:
    # 删除当前列中包含NaN的行，并确保数据长度一致
    data1_values_col = data1_values[col].dropna()
    data2_values_col = data2_values[col].dropna()

    # 通过最小长度截断数据
    min_length = min(len(data1_values_col), len(data2_values_col))
    data1_values_col = data1_values_col[:min_length]
    data2_values_col = data2_values_col[:min_length]

    # 计算当前列的均值
    data1_mean = data1_values_col.mean()
    data2_mean = data2_values_col.mean()

    # 打印当前列的均值
    print(f"{col} 的 data1 均值: {data1_mean:.2f}")
    print(f"{col} 的 data2 均值: {data2_mean:.2f}")

    # 计算当前列的Pearson相关系数
    correlation, _ = pearsonr(data1_values_col, data2_values_col)
    print(f"{col} 的 Pearson相关系数: {correlation:.2f}")
    print("-" * 30)

    # 画散点图
    plt.scatter(data1_values_col, data2_values_col, label=f'{col} (r={correlation:.2f})')

    # 计算并画回归曲线
    coef = np.polyfit(data1_values_col, data2_values_col, 1)
    poly1d_fn = np.poly1d(coef)
    plt.plot(data1_values_col, poly1d_fn(data1_values_col), 'r--')

    # 添加标签和图例
    plt.title(f'Scatter plot with Regression Line - {col}')
    plt.xlabel('Data1')
    plt.ylabel('Data2')
    plt.legend()

    # 保存图像
    plt.savefig(f'scatter_plot_{col}.png')

    # 显示图像
    plt.show()

    print("-" * 30)

