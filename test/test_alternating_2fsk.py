#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试交替发送0和1的2FSK信号生成函数
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from build_fsk_signal import generate_alternating_2fsk_signal, plot_fsk_signal


def test_alternating_2fsk():
    """
    测试交替发送0和1的2FSK信号生成函数
    """
    print("=== 测试交替发送0和1的2FSK信号生成 ===\n")
    
    # 测试参数
    test_cases = [
        {"code_info": "L5", "carrier_type": "1700-1", "fs": 20000, "num_points": 128},
        {"code_info": "L4", "carrier_type": "2000-1", "fs": 25000, "num_points": 128},
        {"code_info": "HB", "carrier_type": "2300-1", "fs": 30000, "num_points": 128},
        {"code_info": "HU", "carrier_type": "2600-1", "fs": 35000, "num_points": 128},
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"测试用例 {i+1}:")
        print(f"  信息类型: {test_case['code_info']}")
        print(f"  载频类型: {test_case['carrier_type']}")
        print(f"  采样频率: {test_case['fs']} Hz")
        print(f"  信号长度: {test_case['num_points']} 点")
        
        try:
            # 生成信号
            time, signal, data, f0, f1 = generate_alternating_2fsk_signal(
                test_case['code_info'],
                test_case['carrier_type'],
                test_case['fs'],
                test_case['num_points']
            )
            
            # 验证结果
            print(f"  生成成功!")
            print(f"  生成的数据: {data}")
            print(f"  数据长度: {len(data)}")
            print(f"  0的载频: {f0} Hz")
            print(f"  1的载频: {f1} Hz")
            print(f"  信号长度: {len(signal)} 点")
            
            # 验证数据是否交替为0和1
            is_alternating = all(data[i] != data[i+1] for i in range(len(data)-1))
            print(f"  数据是否交替: {'是' if is_alternating else '否'}")
            
            # 绘制信号（可选）
            # plot_fsk_signal(time, signal, data, f0, f1, test_case['fs'])
            
        except Exception as e:
            print(f"  错误: {e}")
        
        print()


def test_edge_cases():
    """
    测试边缘情况
    """
    print("=== 测试边缘情况 ===\n")
    
    # 测试无效的信息类型
    print("测试无效的信息类型:")
    try:
        time, signal, data, f0, f1 = generate_alternating_2fsk_signal(
            "INVALID_CODE", "1700-1", 20000, 128
        )
        print("  错误: 应该抛出ValueError")
    except ValueError as e:
        print(f"  正确: {e}")
    
    # 测试无效的载频类型
    print("\n测试无效的载频类型:")
    try:
        time, signal, data, f0, f1 = generate_alternating_2fsk_signal(
            "L5", "INVALID_CARRIER", 20000, 128
        )
        print("  错误: 应该抛出ValueError")
    except ValueError as e:
        print(f"  正确: {e}")
    
    # 测试小信号长度
    print("\n测试小信号长度:")
    try:
        time, signal, data, f0, f1 = generate_alternating_2fsk_signal(
            "L5", "1700-1", 20000, 16
        )
        print(f"  生成成功!")
        print(f"  生成的数据: {data}")
        print(f"  数据长度: {len(data)}")
    except Exception as e:
        print(f"  错误: {e}")


if __name__ == "__main__":
    test_alternating_2fsk()
    test_edge_cases()
    print("测试完成!")
