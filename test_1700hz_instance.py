#!/usr/bin/env python3
# 测试 1700Hz 频率的 Error_Of_Trail_Amplitude_Phase 实例
# 参数: 轨道电路长度 1000m, 道床电阻 1Ω/km

import sys
import os
import numpy as np

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from templates.error_of_trail_amplitude_phase import Error_Of_Trail_Amplitude_Phase

def complex_to_amplitude_phase_str(complex_num):
    """将复数转换为幅值和相角的字符串表示"""
    try:
        if isinstance(complex_num, (int, float)):
            complex_num = complex(complex_num)
        amplitude = np.abs(complex_num)
        phase = np.angle(complex_num) * 180 / np.pi  # 转换为角度
        return f"幅值: {amplitude:.4f}, 相角: {phase:.2f}°"
    except Exception as e:
        return f"无效值: {e}"

def format_complex_value(value):
    """格式化复数或其他类型的值"""
    if isinstance(value, complex):
        return complex_to_amplitude_phase_str(value)
    elif isinstance(value, (np.ndarray)):
        # 处理数组
        if value.ndim == 2 and value.shape == (2, 2):
            # 处理2x2矩阵
            result = "\n"
            for i in range(2):
                for j in range(2):
                    result += f"  [{i},{j}]: {format_complex_value(value[i, j])}\n"
            return result
        else:
            # 处理其他数组
            return str(value)
    else:
        return str(value)

def create_and_test_instance():
    """创建并测试指定参数的实例"""
    print("=" * 80)
    print("测试 1700Hz 频率的 Error_Of_Trail_Amplitude_Phase 实例")
    print("=" * 80)
    print("参数配置:")
    print(f"- 频率: 1700Hz")
    print(f"- 轨道电路长度: 1000m")
    print(f"- 道床电阻: 1Ω/km (0.001Ω/m)")
    print(f"- 故障类型: 无故障 (0)")
    print(f"- 故障位置: 69G (对应 1700Hz)")
    print("=" * 80)
    
    # 创建实例
    try:
        instance = Error_Of_Trail_Amplitude_Phase(
            trail="test_1700hz",
            error_type=0,  # 无故障
            error_value=0,
            error_position="69G",  # 对应 1700Hz
            length_parameter=1000,  # 轨道电路长度 1000m
            SPT_cable_length=1000  # SPT电缆长度
        )
        print("✓ 实例创建成功!")
        print(f"  实际使用的频率: {instance.frequency_table()} Hz")
        print(f"  故障状态: {instance.status()}")
        print(f"  故障特征: {instance.character()}")
        print(f"  调谐单元类型: {instance.find_BA_type_tuning_zone()}")
        print(f"  邻接区段: {instance.find_neibour_zone()}")
        
        # 测试输入阻抗计算
        print("\n测试输入阻抗计算:")
        try:
            input_current, input_impedance, Z_rail, Z_tuner = instance.call_input(130.0, 0.001)
            print(f"  输入电流: {format_complex_value(input_current)}")
            print(f"  输入阻抗: {format_complex_value(input_impedance)}")
            print(f"  钢轨阻抗: {format_complex_value(Z_rail)}")
            print(f"  调谐区阻抗: {format_complex_value(Z_tuner)}")
        except Exception as e:
            print(f"  输入阻抗计算出错: {e}")
        
        # 测试传输矩阵计算
        print("\n测试传输矩阵计算:")
        try:
            result = instance.call_matrix()
            print(f"  传输矩阵计算完成")
            if isinstance(result, dict):
                print(f"  矩阵形状: {result['matrix'].shape}")
                print(f"  传输矩阵:")
                print(f"  {format_complex_value(result['matrix'])}")
                print(f"  电压结果:")
                for key, value in result['voltage_results'].items():
                    print(f"    {key}: {value:.4f} V")
            else:
                print(f"  矩阵形状: {result.shape}")
                print(f"  传输矩阵:")
                print(f"  {format_complex_value(result)}")
        except Exception as e:
            print(f"  传输矩阵计算出错: {e}")
        
        # 测试输出电压计算
        print("\n测试输出电压计算:")
        try:
            output_voltage = instance.count_output()
            print(f"  输出电压: {format_complex_value(output_voltage)}")
        except Exception as e:
            print(f"  输出电压计算出错: {e}")
            
    except Exception as e:
        print(f"✗ 实例创建失败: {e}")
    
    print("=" * 80)
    print("测试完成!")
    print("=" * 80)

if __name__ == "__main__":
    create_and_test_instance()

# 运行说明:
# 1. 打开命令提示符 (cmd.exe)
# 2. 导航到项目目录: cd C:\Users\阳\Documents\trae_projects\py_bishe
# 3. 运行测试: python test_1700hz_instance.py
