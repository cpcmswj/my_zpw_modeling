import jisuan_guidao

print('模块导入成功')
print('测试get_rail_parameters:', jisuan_guidao.get_rail_parameters(1700))
print('测试SPTcable_parameters:', jisuan_guidao.find_SPTcable_parameters(1700))

# 测试SPTcable_matrix函数
print('测试SPTcable_matrix:', jisuan_guidao.SPTcable_matrix(1700, 1000))

# 测试tuning_zone_parameters初始化
try:
    variable = jisuan_guidao.Variable('test', 1000, 1000, 0.01408, 0.00001, 1e-9, 1e-6, 1700)
    tzp = jisuan_guidao.tuning_zone_parameters(variable, 29, 1, 2, 1)
    print('tuning_zone_parameters初始化成功')
    print('Z_FBA:', tzp.Z_FBA)
    print('Z_JBA:', tzp.Z_JBA)
except Exception as e:
    print('错误:', e)

print('所有测试完成')
