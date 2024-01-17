import pandas as pd
import matplotlib.pyplot as plt

# 读取 Excel 文件为 DataFrame
file_path = "data/alldata1218.xlsx"
df = pd.read_excel(file_path, engine='openpyxl', sheet_name='all')

# 将数值日期转换为日期格式
df['time'] = pd.to_datetime(df['time'])

# 按每 7 天统计一次数量
counts_per_week = df.groupby(pd.Grouper(key='time', freq='7D')).size()

# 创建条形图
plt.figure(figsize=(12, 6))
plt.bar(counts_per_week.index.astype(str), counts_per_week.values, width=0.8, color='skyblue')
plt.xlabel('Time')
plt.ylabel('number')
plt.title('CHH_TIME')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
