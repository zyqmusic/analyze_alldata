import pandas as pd
from scipy.stats import spearmanr, ttest_ind

# 读取 Excel 文件为 DataFrame
file_path = "data/music_nonmusic.xlsx"
df = pd.read_excel(file_path)

# 提取目标列
group_column = df['group(nonmusic=1, music=2)']
bias_column = df['bias']
threshold_column = df['threshold']

# 计算斯皮尔曼相关性
spearman_corr_bias, _ = spearmanr(group_column, bias_column)
spearman_corr_threshold, _ = spearmanr(group_column, threshold_column)

# 打印结果
print("Spearman Correlation between 'group' and 'bias': {:.4f}".format(spearman_corr_bias))
print("Spearman Correlation between 'group' and 'threshold': {:.4f}".format(spearman_corr_threshold))

# 进行 t-检验
t_stat, p_value = ttest_ind(bias_column[group_column == 1], bias_column[group_column == 2])

# 打印 t-检验结果
print("\nT-test between 'bias' for nonmusic and music:")
print("t-statistic: {:.4f}".format(t_stat))
print("p-value: {:.4f}".format(p_value))

# 进行 t-检验
t_stat, p_value = ttest_ind(threshold_column[group_column == 1], bias_column[group_column == 2])

# 打印 t-检验结果
print("\nT-test between 'threshold' for nonmusic and music:")
print("t-statistic: {:.4f}".format(t_stat))
print("p-value: {:.4f}".format(p_value))
