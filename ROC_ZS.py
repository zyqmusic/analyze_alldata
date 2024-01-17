import pandas as pd
from sklearn.metrics import roc_curve, auc, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

# 读取 Excel 文件中的指定 sheet 到 DataFrame
file_path = "data/alldata1218.xlsx"
sheet_name = "ZS"
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 去除包含空值的行
df.dropna(subset=["group（MCI=1, Health=2）", "ASD", "CR", "AS_TS"], inplace=True)

# 提取目标列
y = df['group（MCI=1, Health=2）']

# 调整目标列的标签值为二元标签
y_binary = (y == 1).astype(int)

# 指定需要绘制 ROC 曲线的列
columns_of_interest = ["ASD", "CR", "AS_TS"]

# 绘制 ROC 曲线
plt.figure(figsize=(12, 8))

for col in columns_of_interest:
    # 提取当前列的分数
    scores = df[col]

    # 计算 ROC 曲线的相关指标
    fpr, tpr, thresholds = roc_curve(y_binary, scores, pos_label=1)
    roc_auc = auc(fpr, tpr)

    # 计算 Youden Index
    youden_index = tpr - fpr

    # 计算混淆矩阵
    conf_matrix = confusion_matrix(y_binary, scores >= 0.5)  # Using a fixed threshold of 0.5 for simplicity

    # 计算敏感度和特异性
    sensitivity = conf_matrix[1, 1] / (conf_matrix[1, 1] + conf_matrix[1, 0])
    specificity = conf_matrix[0, 0] / (conf_matrix[0, 0] + conf_matrix[0, 1])

    # 绘制 ROC 曲线
    plt.plot(tpr, fpr, label='{} ROC curve (AUC = {:.2f})'.format(col, roc_auc))

    # 标注 AUC、Sensitivity 和 Specificity 值
    plt.text(0.5, 0.2, 'Sensitivity ({}): {:.2f}'.format(col, sensitivity), ha='center', va='center',
             backgroundcolor='white')
    plt.text(0.5, 0.3, 'Specificity ({}): {:.2f}'.format(col, specificity), ha='center', va='center',
             backgroundcolor='white')

    # 标注 Youden Index 值
    optimal_youden_index_index = np.argmax(youden_index)
    optimal_youden_index = youden_index[optimal_youden_index_index]
    optimal_threshold_youden = thresholds[optimal_youden_index_index]
    plt.text(0.5, 0.4, 'Youden Index ({}): {:.2f}'.format(col, optimal_youden_index), ha='center', va='center',
             backgroundcolor='white')
    plt.scatter(tpr[optimal_youden_index_index], fpr[optimal_youden_index_index], marker='o',
                label='Optimal Youden Index for {}'.format(col))

# 绘制对角线
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('True Positive Rate')
plt.ylabel('False Positive Rate')
plt.title('ROC Curves for Attention Shift Time with AUC, Sensitivity, and Youden Index (Flipped Axes)')
plt.legend(loc="lower right")
plt.show()
