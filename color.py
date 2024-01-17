import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

# 定义起始颜色（将RGB值转换为0到1的范围）
start_color =  (32 / 255.0, 112 / 255.0, 180 / 255.0)

# 画一个小矩形以显示颜色
fig, ax = plt.subplots(figsize=(1, 1))
rect = plt.Rectangle((0, 0), 1, 1, color=start_color)
ax.add_patch(rect)
plt.axis('off')
plt.show()

# 打印起始颜色的 RGB 值
print("Start Color RGB:", tuple(int(x * 255) for x in start_color))

# 获取近似色系
similar_colors = [start_color]
for i in range(1, 5):
    similar_colors.append(to_rgba(start_color, alpha=i*0.2))  # 调整 alpha 值以获取不同深浅的颜色

# 打印近似色系的 RGB 值
print("Similar Colors RGB:")
for color in similar_colors:
    rgb_values = tuple(int(x * 255) for x in color)
    print(rgb_values)
