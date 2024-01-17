import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# 读取 Excel 文件中的指定 sheet 为 DataFrame
file_path = "data/alldata1218.xlsx"
df = pd.read_excel(file_path, sheet_name='AC')

# 创建 'group' 列
df['group'] = df['group(AC=1, AC_new=2)'].map({1: 'AC', 2: 'AC_new'})

# 选择需要绘制箱图的列
columns_to_plot = ['Threshold', 'Bias', 'RT.M', 'CR.C', 'CR.F', 'CR.P', 'MR', 'TN.P']

# 为每列指定特定颜色
colors_dict = {
    'Threshold': [165, 218, 240],
    'Bias': [251, 160, 149],
    'RT.M': [255, 221, 113],
    'CR.C': [102, 204, 102],
    'CR.F': [119, 187, 255],
    'CR.P': [255, 159, 64],
    'MR': [168, 102, 210],
    'TN.P': [255, 102, 255]
}

# 转换颜色值为范围在 [0, 1] 的浮点数
colors_dict = {key: [x / 255.0 for x in value] for key, value in colors_dict.items()}

# 设置字体大小
plt.rcParams.update({'font.size': 12})

# 创建一个新的图形，包含多个子图
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
fig.suptitle('Box Plots by Column')

# 创建一个列表用于存储t-test和p-value结果
ttest_results = []

# 遍历每一列进行箱图绘制和t-test计算
for col, ax in zip(columns_to_plot, axes.flatten()):
    # 获取当前列的颜色
    colors = colors_dict.get(col, 'gray')

    # 在颜色中添加 alpha 通道来调整颜色深浅
    color_ac = tuple([x * 0.8 for x in colors] + [0.6])  # AC组，颜色稍浅
    color_ac_new = tuple(colors + [1.0])  # AC_new组，颜色稍深

    # 去除包含0值的行
    df_filtered = df[df[col] != 0]

    # 画出箱图，不去除极端值
    sns.boxplot(x='group', y=col, data=df_filtered,
                palette={'AC': color_ac, 'AC_new': color_ac_new}, width=0.7, ax=ax, showfliers=False, hue='group',
                saturation=1.0, linewidth=1.2)
    sns.swarmplot(x='group', y=col, data=df_filtered,
                  color='gray', ax=ax, marker='o', size=4)  # 添加灰色散点图

    ax.set_title(col)
    ax.set_xlabel('Group')
    ax.set_ylabel('Values')

    # 执行t-test
    ac_values = df_filtered[df_filtered['group'] == 'AC'][col]
    ac_new_values = df_filtered[df_filtered['group'] == 'AC_new'][col]
    print(ac_values, ac_new_values)

    t_stat, p_value = ttest_ind(ac_values, ac_new_values)

    # 显示t-test结果
    ax.text(0.5, 0.95, f"t-test: {t_stat:.2f}\n p-value: {p_value:.4f}", transform=ax.transAxes, ha='center', va='top')

    # 将结果添加到列表
    ttest_results.append({'Column': col, 't-test': t_stat, 'p-value': p_value})

# 将列表转换为DataFrame
ttest_results_df = pd.DataFrame(ttest_results)

# 显示t-test和p-value结果
print("\nT-test and p-value results:");
print(ttest_results_df);

# 添加图例
handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right', title='Group')

# 调整布局
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
