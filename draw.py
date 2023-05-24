import matplotlib.pyplot as plt
import numpy as np

# 定义两个表格的数据
simple_natural = [[0,103,1032,1442,416],[498,1468,5899,2785,128],[697,1207,992,0,428]]
conventional_natural = [[0,94,1015,1034,399],[567,1681,6341,3193,126],[628,1003,567,0,447]]

# 定义柱状图的标签和颜色
labels = ["Grand Slam", "Small Slam", "Game", "Part Score", "Other"]
colors = ["red", "green", "orange"]

# 定义一个函数来画出堆叠柱状图
def plot_stacked_bar(data, title):
    # data是一个二维列表，表示表格的数据，每一行表示一种结果（叫高了，正好，叫低了）
    # title是一个字符串，表示表格的标题
    # 创建一个新的图形
    plt.figure()
    # 设置图形的标题和坐标轴标签
    plt.title(title)
    plt.xlabel("Contract")
    plt.ylabel("Count")
    # 设置x轴的刻度和标签
    x = range(len(labels))
    plt.xticks(x, labels)
    # 设置y轴的范围和刻度间隔
    plt.ylim(0,10000)
    plt.yticks(range(0,10001,1000))
    # 初始化一个列表，表示每个柱子的底部位置
    bottom = [0] * len(labels)
    # 遍历每一行数据，画出对应的柱子，并更新底部位置
    for i in range(len(data)):
        plt.bar(x, data[i], width=0.8, color=colors[i], bottom=bottom)
        bottom = [bottom[j] + data[i][j] for j in range(len(labels))]
    # 添加图例，显示每种颜色对应的结果
    plt.legend(["Overbid", "Just Right", "Underbid"])
    # 显示图形
    plt.show()

# 调用函数，画出两个表格对应的堆叠柱状图
plot_stacked_bar(simple_natural, "Simple Natural")
plot_stacked_bar(conventional_natural, "Conventional Natural")
