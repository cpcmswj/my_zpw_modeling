import numpy as np

# 创建一个numpy数组
arr = np.array([1, 2, 3, 4, 5])
print("创建的数组:", arr)

# 数组运算
print("数组加法:", arr + 1)
print("数组乘法:", arr * 2)

# 矩阵运算
matrix = np.array([[1, 2], [3, 4]])
print("矩阵:", matrix)
print("矩阵转置:", matrix.T)
print("矩阵乘法:", np.dot(matrix, matrix))
#矩阵求逆
print("矩阵逆:", np.linalg.inv(matrix))
#提取矩阵元素
print("提取第一行:", matrix[0])
print("提取第一列:", matrix[:, 0])
print("提取子矩阵:", matrix[0:2, 0:2])
#提取单个元素
print("提取单个元素:", matrix[1, 1])
# 统计函数
print("平均值:", np.mean(arr))
print("标准差:", np.std(arr))
print("最大值:", np.max(arr))
print("最小值:", np.min(arr))

#向量点积
print("向量点积:", np.dot(arr, arr))
#向量叉积
#print("向量叉积:", np.cross(arr, arr))

#开方
print("开方:", np.sqrt(arr))
#三角函数
print("正弦:", np.sin(arr))
print("余弦:", np.cos(arr))
print("正切:", np.tan(arr))
#反三角函数
print("反正弦:", np.arcsin(arr))
print("反余弦:", np.arccos(arr))
print("反正切:", np.arctan(arr))
#双曲线函数
print("双曲正弦:", np.sinh(arr))
print("双曲余弦:", np.cosh(arr))
print("双曲正切:", np.tanh(arr))
#复数计算
print("复数加法:", np.array([1+2j, 3+4j]) + np.array([1-2j, 3-4j]))
print("复数乘法:", np.array([1+2j, 3+4j]) * np.array([1-2j, 3-4j]))
print("复数共轭:", np.conj(np.array([1+2j, 3+4j])))
print("复数模:", np.abs(np.array([1+2j, 3+4j])))
print("复数相位:", np.angle(np.array([1+2j, 3+4j])))

print("sinh:", np.sinh(6.3))
print("cosh:", np.cosh(6.3))
print("tanh:", np.tanh(6.3))
