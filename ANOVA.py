import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
from scipy.stats import ttest_rel, ttest_ind, chisquare, ks_2samp, wilcoxon

# 读取Excel文件中的指定sheet为DataFrame
file_path = "data/hospital.xlsx"
sheet_name = "AC"
df = pd.read_excel(file_path, sheet_name='AC')

# 列名
columns_to_compare = [
    ('Threshold', 'Threshold_new'),
    ('Bias', 'Bias_new'),
    ('RT.M', 'RT.M_new'),
    ('RT(M/K)', 'RT(M/K)_new'),
    ('CR.C', 'CR.C_new'),
    ('CR.F', 'CR.F_new'),
    ('CR.P', 'CR.P_new'),
    ('MR', 'MR_new'),
    ('TN.P', 'TN.P_new')
]

# 进行检验
for col1, col2 in columns_to_compare:
    data = df[[col1, col2]].dropna()

    if pd.api.types.is_numeric_dtype(data[col1]) and pd.api.types.is_numeric_dtype(data[col2]):
        # 对于数值型数据
        if data[col1].equals(data[col2]):
            print(f"{col1} 和 {col2} 的数据相同，无需检验。")
        else:
            # 两个独立样本的均值比较
            t_stat, p_value = ttest_ind(data[col1], data[col2])
            print(f"{col1} 和 {col2} 的独立样本 t 检验结果 - t-statistic: {t_stat}, p-value: {p_value}")
    else:
        # 对于非数值型数据
        if len(data[col1].unique()) == len(data[col2].unique()) and set(data[col1].unique()) == set(data[col2].unique()):
            print(f"{col1} 和 {col2} 的数据相同，无需检验。")
        else:
            # 两个独立样本的分布比较 (使用卡方检验)
            chi_stat, chi_p_value = chisquare(data[col1].value_counts(), data[col2].value_counts())
            print(f"{col1} 和 {col2} 的卡方检验结果 - chi-square statistic: {chi_stat}, p-value: {chi_p_value}")

    # 两个相关样本的均值比较 (使用配对样本 t 检验)
    t_stat_rel, p_value_rel = ttest_rel(data[col1], data[col2])
    print(f"{col1} 和 {col2} 的配对样本 t 检验结果 - t-statistic: {t_stat_rel}, p-value: {p_value_rel}")

    # 对于非数值型数据的配对样本分布比较 (使用符号检验)
    if not pd.api.types.is_numeric_dtype(data[col1]):
        # 符号检验只适用于非数值型数据
        wilcoxon_stat, wilcoxon_p_value = wilcoxon(data[col1], data[col2])
        print(f"{col1} 和 {col2} 的符号检验结果 - Wilcoxon statistic: {wilcoxon_stat}, p-value: {wilcoxon_p_value}")

    print("\n")

# 创建一个字典来保存ANOVA的结果
anova_results = {}

# 遍历每一对列进行ANOVA
for col1, col2 in columns_to_compare:
    data = df[[col1, col2]].dropna()

    # 添加检查，确保数据点的数量不小于2
    if len(data) >= 2:
        # 执行ANOVA
        anova_result = f_oneway(data[col1], data[col2])

        # 将结果存储到字典中
        anova_results[f"{col1} vs {col2}"] = anova_result

        # 画出散点图
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=col1, y=col2, data=data, hue=df['Group'], palette='Set1')
        plt.title(f'Scatter Plot ({col1} vs {col2})')
        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.legend(title='Group')
        plt.show()
    else:
        print(f"数据点数量不足，无法进行ANOVA和画出散点图 ({col1} vs {col2})。")

# 打印ANOVA结果
for comparison, result in anova_results.items():
    print(f"ANOVA结果 ({comparison}): F-statistic: {result.statistic}, p-value: {result.pvalue}")
