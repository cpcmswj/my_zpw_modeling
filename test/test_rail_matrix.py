#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试钢轨传输矩阵相关方法
"""

import numpy as np
import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jisuan_guidao import Variable

def test_iron_rail_method():
    """
    测试iron_rail方法
    """
    print("\n=== 测试 iron_rail 方法 ===")
    
    # 创建Variable实例
    variable = Variable(
        name="track_circuit",
        value=1.0,
        length_guidao=1000.0,
        resist_per_meter=1.0e-3,#1Ω/km
        induct_per_meter=1.3e-6,  # 每米电感为1.3uH
        capacit_per_meter=1.0e-9,
        conduct_per_meter=1000,#漏泄电导为漏泄电阻的倒数，漏泄电阻取1Ω/km
        frequency=1700
    )
    
    # 测试不同长度的钢轨传输矩阵
    lengths = [100, 500, 1000, 2000]
    
    for length in lengths:
        try:
            matrix = variable.iron_rail(length)
            print(f"长度 {length}m 的钢轨传输矩阵:")
            print(matrix)
            
            # 检查矩阵是否有效
            if np.all(np.isfinite(matrix)):
                print(f"✓ 矩阵有效，无无效值")
            else:
                print(f"✗ 矩阵包含无效值")
                
        except Exception as e:
            print(f"✗ 计算长度 {length}m 的钢轨传输矩阵时出错: {e}")

def test_whole_iron_rail_with_capacitance_method():
    """
    测试whole_iron_rail_with_capacitance方法
    """
    print("\n=== 测试 whole_iron_rail_with_capacitance 方法 ===")
    
    # 创建Variable实例
    variable = Variable(
        name="track_circuit",
        value=1.0,
        length_guidao=1000.0,
        resist_per_meter=0.1,
        induct_per_meter=1.0e-3,
        capacit_per_meter=1.0e-9,
        conduct_per_meter=1.0e-6,
        frequency=1700
    )
    
    # 测试不同参数的钢轨传输矩阵
    test_cases = [
        # (段数, 每段长度, 电阻, 电感, 电容)
        (10, 100, 0, 0, 1.0e-6),  # 10段，每段100m
        (20, 50, 0, 0, 1.0e-6),   # 20段，每段50m
        (5, 200, 0, 0, 1.0e-6),    # 5段，每段200m
    ]
    
    for i, (segments, segment_length, R_cb, L_cb, C_b) in enumerate(test_cases):
        try:
            matrix = variable.whole_iron_rail_with_capacitance(
                segments, segment_length, R_cb, L_cb, C_b
            )
            print(f"测试用例 {i+1}: 段数={segments}, 每段长度={segment_length}m")
            print(matrix)
            
            # 检查矩阵是否有效
            if np.all(np.isfinite(matrix)):
                print(f"✓ 矩阵有效，无无效值")
            else:
                print(f"✗ 矩阵包含无效值")
                
        except Exception as e:
            print(f"✗ 计算测试用例 {i+1} 时出错: {e}")

def test_edge_cases():
    """
    测试边界情况
    """
    print("\n=== 测试边界情况 ===")
    
    # 创建Variable实例
    variable = Variable(
        name="track_circuit",
        value=1.0,
        length_guidao=1000.0,
        resist_per_meter=0.1,
        induct_per_meter=1.0e-3,
        capacit_per_meter=1.0e-9,
        conduct_per_meter=1.0e-6,
        frequency=1700
    )
    
    # 测试非常短的长度
    print("\n测试非常短的长度 (0.1m):")
    try:
        matrix = variable.iron_rail(0.1)
        print(matrix)
        if np.all(np.isfinite(matrix)):
            print("✓ 矩阵有效")
        else:
            print("✗ 矩阵无效")
    except Exception as e:
        print(f"✗ 出错: {e}")
    
    # 测试频率为0的情况
    print("\n测试频率为0的情况:")
    variable2 = Variable(
        name="track_circuit",
        value=1.0,
        length_guidao=1000.0,
        resist_per_meter=0.1,
        induct_per_meter=1.0e-3,
        capacit_per_meter=1.0e-9,
        conduct_per_meter=1.0e-6,
        frequency=0
    )
    try:
        matrix = variable2.iron_rail(100)
        print(matrix)
        if np.all(np.isfinite(matrix)):
            print("✓ 矩阵有效")
        else:
            print("✗ 矩阵无效")
    except Exception as e:
        print(f"✗ 出错: {e}")

if __name__ == "__main__":
    print("开始测试钢轨传输矩阵相关方法...")
    
    test_iron_rail_method()
    test_whole_iron_rail_with_capacitance_method()
    test_edge_cases()
    
    print("\n测试完成!")
