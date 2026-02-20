import jisuan_guidao
import circuit_tool

print('模块导入成功')

# 测试串联阻抗计算
z1 = 10 + 20j
z2 = 5 + 10j
series_z = circuit_tool.calculate_series_impedance(z1, z2)
print('测试串联阻抗计算:', series_z)

# 测试并联阻抗计算
parallel_z = circuit_tool.calculate_parallel_impedance(z1, z2)
print('测试并联阻抗计算:', parallel_z)

# 测试电流分配计算
voltage = 220 + 0j
currents = circuit_tool.calculate_current_distribution(voltage, z1, z2)
print('测试电流分配计算:', currents)

# 测试根据总电流计算各阻抗电流
# 先计算总电流
 total_current = sum(currents)
print('总电流:', total_current)

# 使用总电流计算各阻抗电流
currents_from_total = circuit_tool.calculate_current_from_total(total_current, z1, z2)
print('测试根据总电流计算各阻抗电流:', currents_from_total)

# 测试jisuan_guidao模块是否仍然正常工作
rail_params = jisuan_guidao.get_rail_parameters(1700)
print('测试get_rail_parameters:', rail_params)

print('所有测试完成')
