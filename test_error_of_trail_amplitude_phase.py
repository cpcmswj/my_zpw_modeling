#!/usr/bin/env python3
# 测试 error_of_trail_amplitude_phase.py 文件

import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from templates.error_of_trail_amplitude_phase import Error_Of_Trail_Amplitude_Phase

print("测试 Error_Of_Trail_Amplitude_Phase 类")
print("=" * 60)

# 创建测试实例
test_instance = Error_Of_Trail_Amplitude_Phase('test', 0, 0, '69G', 1000, 100)

# 测试基本方法
print("1. 基本属性测试:")
print(f"   故障状态: {test_instance.status()}")
print(f"   故障特征: {test_instance.character()}")
print(f"   调谐单元类型: {test_instance.find_BA_type_tuning_zone()}")
print(f"   邻接区段: {test_instance.find_neibour_zone()}")
print(f"   频率: {test_instance.frequency_table()} Hz")
print()

# 测试 call_input 方法
print("2. 输入阻抗测试:")
try:
    input_current, input_impedance, Z_rail, Z_tuner = test_instance.call_input(10.0, 1.0)
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
    matrix = test_instance.call_matrix()
    print(f"   传输矩阵:")
    print(matrix)
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

# 测试不同故障类型
print("5. 不同故障类型测试:")
fault_types = [0, 1, 2, 3, 4, 5, 6, 7]
for fault_type in fault_types:
    try:
        fault_instance = Error_Of_Trail_Amplitude_Phase('test', fault_type, 0, '69G', 1000, 100)
        status = fault_instance.status()
        print(f"   故障类型 {fault_type}: {status}")
    except Exception as e:
        print(f"   故障类型 {fault_type} 测试出错: {e}")
print()

print("测试完成!")
print("=" * 60)
