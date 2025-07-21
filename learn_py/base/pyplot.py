import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread


"""
#绘制图形
x = np.arange(0, 6, 0.1) #以0.1为单位，生成(0,6)的数据
y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y1, label="sin")
plt.plot(x, y2, linestyle="--", label="cos") #用虚线绘制

plt.xlabel("x")
plt.ylabel("y")
plt.title("sin & cos")
plt.legend()
plt.show()

"""

# 读取图片
img = imread("D:\文件夹集合\毕设过程材料\演示内容\lg.png")
plt.imshow(img)
plt.show()





