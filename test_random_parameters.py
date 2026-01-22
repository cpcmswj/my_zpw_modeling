#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试随机参数生成功能

用于测试random_parameters.py和jisuan_guidao.py中的随机参数生成功能。
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_random_parameters():
    """测试随机参数生成模块"""
    print("=== 测试random_parameters模块 ===")
    
    try:
        from random_parameters import (
            generate_random_SPT_cable_params,
            generate_random_tuning_unit_params,
            generate_random_frequency_params
        )
        
        # 测试SPT电缆参数生成
        print("\n1. 测试SPT电缆参数生成：")
        for freq in [1700, 2000, 2300, 2600]:
            gamma, Z_d, phi = generate_random_SPT_cable_params(freq)
            print(f"   频率 {freq}Hz: 传输常数={gamma:.3f}dB/km, 特性阻抗={Z_d:.1f}Ω, 阻抗角={phi:.1f}°")
        
        # 测试调谐单元参数生成
        print("\n2. 测试调谐单元参数生成：")
        # F1参数
        print("   F1调谐单元:")
        for unit in [1, 2]:
            param = generate_random_tuning_unit_params(1, unit)
            param_name = "L1 (uH)" if unit == 1 else "C1 (uF)"
            print(f"     {param_name}: {param:.3f}")
        
        # F2参数
        print("   F2调谐单元:")
        for unit in [1, 2, 3]:
            param = generate_random_tuning_unit_params(2, unit)
            if unit == 1:
                param_name = "L2 (uH)"
            elif unit == 2:
                param_name = "C2 (uF)"
            else:
                param_name = "C3 (uF)"
            print(f"     {param_name}: {param:.3f}")
        
        # 测试完整参数集生成
        print("\n3. 测试完整参数集生成：")
        params = generate_random_frequency_params(1700)
        print(f"   SPT电缆参数: {params['SPT_cable']}")
        print(f"   F1参数: {params['F1']}")
        print(f"   F2参数: {params['F2']}")
        
        print("\n✅ random_parameters模块测试成功!")
        return True
        
    except Exception as e:
        print(f"❌ random_parameters模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_jisuan_guidao_randomize():
    """测试jisuan_guidao中的随机化功能"""
    print("\n=== 测试jisuan_guidao中的随机化功能 ===")
    
    try:
        from jisuan_guidao import (
            find_SPTcable_parameters,
            find_tuning_unit_parameters,
            find_tuning_unit_impedance,
            find_tuning_unit_impedance_matrix
        )
        
        frequency = 1700
        angular_freq = 2 * 3.14159 * frequency
        
        # 测试SPT电缆参数随机化
        print("\n1. 测试SPT电缆参数随机化：")
        # 使用原始值
        gamma_orig, Z_d_orig, phi_orig = find_SPTcable_parameters(frequency, randomize=False)
        # 使用随机值
        gamma_rand, Z_d_rand, phi_rand = find_SPTcable_parameters(frequency, randomize=True, variation=0.1)
        
        print(f"   原始值: 传输常数={gamma_orig:.3f}dB/km, 特性阻抗={Z_d_orig:.1f}Ω, 阻抗角={phi_orig:.1f}°")
        print(f"   随机值: 传输常数={gamma_rand:.3f}dB/km, 特性阻抗={Z_d_rand:.1f}Ω, 阻抗角={phi_rand:.1f}°")
        
        # 测试调谐单元参数随机化
        print("\n2. 测试调谐单元参数随机化：")
        # 使用原始值
        L1_orig = find_tuning_unit_parameters(1, 1, randomize=False)
        # 使用随机值
        L1_rand = find_tuning_unit_parameters(1, 1, randomize=True, variation=0.05)
        
        print(f"   F1-L1原始值: {L1_orig:.3f} uH")
        print(f"   F1-L1随机值: {L1_rand:.3f} uH")
        
        # 测试调谐单元阻抗随机化
        print("\n3. 测试调谐单元阻抗随机化：")
        # 使用原始值
        Z_orig = find_tuning_unit_impedance(angular_freq, 1, randomize=False)
        # 使用随机值
        Z_rand = find_tuning_unit_impedance(angular_freq, 1, randomize=True, variation=0.05)
        
        print(f"   F1阻抗原始值: {abs(Z_orig):.2f} Ω")
        print(f"   F1阻抗随机值: {abs(Z_rand):.2f} Ω")
        
        # 测试调谐单元阻抗矩阵随机化
        print("\n4. 测试调谐单元阻抗矩阵随机化：")
        # 使用原始值
        T_orig = find_tuning_unit_impedance_matrix(angular_freq, 1, randomize=False)
        # 使用随机值
        T_rand = find_tuning_unit_impedance_matrix(angular_freq, 1, randomize=True, variation=0.05)
        
        print(f"   原始矩阵:\n{T_orig}")
        print(f"   随机矩阵:\n{T_rand}")
        
        print("\n✅ jisuan_guidao随机化功能测试成功!")
        return True
        
    except Exception as e:
        print(f"❌ jisuan_guidao随机化功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("开始测试随机参数生成功能...")
    print("=" * 60)
    
    test1 = test_random_parameters()
    test2 = test_jisuan_guidao_randomize()
    
    print("\n" + "=" * 60)
    if test1 and test2:
        print("🎉 所有测试通过! 随机参数生成功能正常工作。")
        return 0
    else:
        print("❌ 部分测试失败! 请检查代码。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
