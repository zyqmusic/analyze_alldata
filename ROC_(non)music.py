import pandas as pd
from sklearn.metrics import roc_curve, auc, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

# 读取 Excel 文件为 DataFrame
file_path = "data/music_nonmusic.xlsx"
df = pd.read_excel(file_path)

# 去除包含空值的行
df.dropna(subset=['Nbias', 'Nthreshold'], inplace=True)

# 提取目标列
y = df['group(nonmusic=1, music=2)']

# 调整目标列的标签值为二元标签
y_binary = (y == 2).astype(int)

# 提取 Nbias 和 Nthreshold 列
scores_bias = df['Nbias']
scores_threshold = df['Nthreshold']

# 计算 ROC 曲线的相关指标
fpr_bias, tpr_bias, thresholds_bias = roc_curve(y_binary, scores_bias, pos_label=1)
roc_auc_bias = auc(fpr_bias, tpr_bias)

fpr_threshold, tpr_threshold, thresholds_threshold = roc_curve(y_binary, scores_threshold, pos_label=1)
roc_auc_threshold = auc(fpr_threshold, tpr_threshold)

# 计算 Youden Index 和最佳阈值
youden_index_bias = tpr_bias - fpr_bias
optimal_threshold_bias_index = np.argmax(youden_index_bias)
optimal_threshold_bias = thresholds_bias[optimal_threshold_bias_index]

youden_index_threshold = tpr_threshold - fpr_threshold
optimal_threshold_threshold_index = np.argmax(youden_index_threshold)
optimal_threshold_threshold = thresholds_threshold[optimal_threshold_threshold_index]

# 计算混淆矩阵
conf_matrix_threshold = confusion_matrix(y_binary, scores_threshold >= optimal_threshold_threshold)

# 计算敏感度和特异性
sensitivity_threshold = conf_matrix_threshold[1, 1] / (conf_matrix_threshold[1, 1] + conf_matrix_threshold[1, 0])
specificity_threshold = conf_matrix_threshold[0, 0] / (conf_matrix_threshold[0, 0] + conf_matrix_threshold[0, 1])

# 绘制 ROC 曲线
plt.figure(figsize=(8, 8))

# 绘制 Nbias 列的 ROC 曲线
plt.plot(fpr_bias, tpr_bias, color='darkorange', lw=2, label='Nbias ROC curve (AUC = {:.2f})'.format(roc_auc_bias))
plt.scatter(fpr_bias[optimal_threshold_bias_index], tpr_bias[optimal_threshold_bias_index], marker='o', color='red', label='Optimal Threshold for Nbias')

# 绘制 Nthreshold 列的 ROC 曲线
plt.plot(fpr_threshold, tpr_threshold, color='green', lw=2, label='Nthreshold ROC curve (AUC = {:.2f})'.format(roc_auc_threshold))
plt.scatter(fpr_threshold[optimal_threshold_threshold_index], tpr_threshold[optimal_threshold_threshold_index], marker='o', color='blue', label='Optimal Threshold for Nthreshold')

# 绘制对角线
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')

# 标注 AUC 和 Youden Index 值
plt.text(0.5, 0.7, 'Optimal Threshold (Nbias): {:.2f}'.format(optimal_threshold_bias), ha='center', va='center', backgroundcolor='white')
plt.text(0.5, 0.4, 'Optimal Threshold (Nthreshold): {:.2f}'.format(optimal_threshold_threshold), ha='center', va='center', backgroundcolor='white')
plt.text(0.5, 0.3, 'Sensitivity (Nthreshold): {:.2f}'.format(sensitivity_threshold), ha='center', va='center', backgroundcolor='white')
plt.text(0.5, 0.2, 'Specificity (Nthreshold): {:.2f}'.format(specificity_threshold), ha='center', va='center', backgroundcolor='white')

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves for Nbias and Nthreshold with AUC and Youden Index')
plt.legend(loc="lower right")
plt.show()
