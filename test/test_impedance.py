import numpy as np
from jisuan_guidao import calculate_series_impedance, calculate_parallel_impedance

# 测试串联阻抗计算
print("测试串联阻抗计算:")
# 创建一些测试阻抗（复数形式）
z1 = 10 + 20j  # 10Ω电阻与20Ω感抗串联
z2 = 5 + 10j   # 5Ω电阻与10Ω感抗串联
z3 = 15 + 5j   # 15Ω电阻与5Ω感抗串联

# 测试两个阻抗串联
series_total = calculate_series_impedance(z1, z2)
print(f"z1 + z2 = {series_total:.2f}")

# 测试三个阻抗串联
series_total_3 = calculate_series_impedance(z1, z2, z3)
print(f"z1 + z2 + z3 = {series_total_3:.2f}")

# 测试并联阻抗计算
print("\n测试并联阻抗计算:")
# 测试两个阻抗并联
parallel_total = calculate_parallel_impedance(z1, z2)
print(f"z1 || z2 = {parallel_total:.2f}")

# 测试三个阻抗并联
parallel_total_3 = calculate_parallel_impedance(z1, z2, z3)
print(f"z1 || z2 || z3 = {parallel_total_3:.2f}")

# 测试边界情况
print("\n测试边界情况:")
# 测试空输入
print(f"空输入串联: {calculate_series_impedance()}")
print(f"空输入并联: {calculate_parallel_impedance()}")

# 测试含零阻抗的并联
print(f"含零阻抗并联: {calculate_parallel_impedance(z1, 0, z2)}")
