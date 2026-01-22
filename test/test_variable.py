import jisuan_guidao
import numpy as np

# 测试find_capacitance函数
print("=== 测试find_capacitance函数 ===")
frequencies = [1700, 2000, 2300, 2600, 3000]
for freq in frequencies:
    cap = jisuan_guidao.find_capacitance(freq)
    print(f"{freq}Hz对应的电容值: {cap}uF")

# 测试Variable类
print("\n=== 测试Variable类 ===")
try:
    # 创建Variable实例
    variable = jisuan_guidao.Variable(
        name="test",
        value=1.0,
        length_guidao=100.0,
        resist_per_meter=0.1,
        induct_per_meter=1.0e-3,
        capacit_per_meter=1.0e-9
    )
    
    print("Variable实例创建成功")
    print(f"电阻导轨: {variable.resist_guidao}Ω")
    print(f"电感导轨: {variable.induct_guidao}H")
    print(f"电容导轨: {variable.capacit_guidao}F")
    print(f"阻抗模: {variable.impedance}Ω")
    print(f"导纳模: {variable.admittance}S")
    print(f"复数阻抗: {variable.Z_complex}Ω")
    print(f"复数导纳: {variable.Y_complex}S")
    print(f"传播系数复数: {variable.gamma_complex}")
    print(f"特性阻抗复数: {variable.Z_c_complex}Ω")
    
    # 测试iron_rail方法
    iron_rail_matrix = variable.iron_rail()
    print("\n钢轨等效传输特性矩阵:")
    print(iron_rail_matrix)
    
    # 测试capacitance_matrix方法
    capacitance_matrix = variable.capacitance_matrix(R_cb=0.1, L_cb=1.0e-6, C_cb=50e-6)
    print("\n轨间补偿电容传输矩阵:")
    print(capacitance_matrix)
    
    print("\n所有测试通过!")
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()