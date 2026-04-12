#!/usr/bin/env python3
# 测试特定参数的 Error_Of_Trail_Amplitude_Phase 实例

import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from templates.error_of_trail_amplitude_phase import Error_Of_Trail_Amplitude_Phase

print("测试特定参数的 Error_Of_Trail_Amplitude_Phase 实例")
print("=" * 60)
print("参数设置:")
print("- 频率: 1700Hz")
print("- 轨道电路长度: 1000m")
print("- 道床电阻: 1Ω/km (即 0.001Ω/m)")
print()

# 创建测试实例
# 选择 69G 作为故障位置，因为它对应 1700Hz 频率
test_instance = Error_Of_Trail_Amplitude_Phase(
    trail='test',
    error_type=0,  # 无故障
    error_value=0,
    error_position='69G',  # 对应 1700Hz
    length_parameter=1000,  # 轨道电路长度 1000m
    SPT_cable_length=100  # SPT电缆长度，使用默认值
)

print("测试实例创建成功!")
print(f"实际使用的频率: {test_instance.frequency_table()} Hz")
print()

# 测试基本方法
print("1. 基本属性测试:")
print(f"   故障状态: {test_instance.status()}")
print(f"   故障特征: {test_instance.character()}")
print(f"   调谐单元类型: {test_instance.find_BA_type_tuning_zone()}")
print(f"   邻接区段: {test_instance.find_neibour_zone()}")
print()

# 测试 call_input 方法，使用指定的道床电阻
print("2. 输入阻抗测试 (道床电阻: 1Ω/km):")
try:
    # 注意：call_input 方法的第二个参数是每米道床漏阻，所以 1Ω/km 转换为 0.001Ω/m
    input_current, input_impedance, Z_rail, Z_tuner = test_instance.call_input(10.0, 0.001)
    print(f"   输入电流: {input_current}")
    print(f"   输入阻抗: {input_impedance}")
    print(f"   钢轨阻抗: {Z_rail}")
    print(f"   调谐区阻抗: {Z_tuner}")
except Exception as e:
    print(f"   测试 call_input 时出错: {e}")
print()

# 测试 call_matrix 方法
print("3. 传输矩阵测试:")
try:
    matrix_result = test_instance.call_matrix()
    print(f"   传输矩阵:")
    print(matrix_result)
    
    # 打印电压结果
    if hasattr(test_instance, 'voltage_results'):
        print(f"   电压结果:")
        for key, value in test_instance.voltage_results.items():
            print(f"     {key}: {value} V")
except Exception as e:
    print(f"   测试 call_matrix 时出错: {e}")
print()

# 测试 count_output 方法
print("4. 输出电压测试:")
try:
    output_voltage = test_instance.count_output()
    print(f"   输出电压: {output_voltage}")
except Exception as e:
    print(f"   测试 count_output 时出错: {e}")
print()

print("测试完成!")
print("=" * 60)
