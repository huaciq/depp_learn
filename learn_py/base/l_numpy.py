import l_numpy as np

'''
一维数组，向量
x = np.array([1, 2, 3])
y = np.array([2, 3, 4])
print(f"x+y:{x+y}")
print(f"x-y:{x-y}")
print(f"x*y:{x*y}")
print(f"x/y:{x/y}")
'''

"""
# 这个矩阵和代数矩阵不一样，运算是对应元素进行初等运算的
A = np.array([[2, 3], [3, 4]])
B = np.array([[3, 4], [5, 6]])
# 不同shape的矩阵也能进行运算
C = np.array([10, 20])
print(f"A*C:{A*C}")


print(f"A+B:{A+B}")
print(f"A*B:{A*B}")

# 该矩阵也可以和标量运算
print(f"A*2:{A*2}")
"""

"""
# 对二维矩阵的操作
X = np.array([[1, 2], [3, 4]])
print(X)
print(X[0])  # 取得行数
print(X[0,0])  # 取得第一个元素，一行一列
print()
"""

# 也可以用数组来访问元素

X = np.array([[51, 55], [14, 19], [0, 4]])
print(X)
X = X.flatten()
print(X)#将X转换为一维数组
print(X[np.array([0, 2, 4])])

# 可以将X当作操作体
print(X > 15)
print(X[X > 15])
