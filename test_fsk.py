#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSK信号生成程序测试脚本

该脚本用于测试FSK信号生成程序的核心功能，包括：
1. 生成指定长度的FSK信号
2. 支持不同的二进制数据
3. 支持不同的频率参数
"""

import numpy as np
from build_fsk_signal import generate_fsk_signal, generate_random_data, save_fsk_signal

def test_generate_fsk_signal():
    """
    测试生成FSK信号的功能
    """
    print("=== 测试生成FSK信号 ===\n")
    
    # 测试参数
    test_cases = [
        # (data, f0, f1, fs, num_points, description)
        ([0, 1, 0, 1], 1.0, 3.0, 10.0, 16, "16点 - 4位数据 - 简单交替")
    ]
    
    for data, f0, f1, fs, num_points, description in test_cases:
        print(f"测试: {description}")
        print(f"数据: {data}")
        print(f"f0: {f0}Hz, f1: {f1}Hz, fs: {fs}Hz, 点数: {num_points}")
        
        try:
            # 生成FSK信号
            time, signal = generate_fsk_signal(data, f0, f1, fs, num_points)
            
            # 检查结果
            assert len(time) == num_points, f"时间序列长度错误: 预期 {num_points}, 实际 {len(time)}"
            assert len(signal) == num_points, f"信号长度错误: 预期 {num_points}, 实际 {len(signal)}"
            
            print(f"✓ 生成成功 - 时间序列: {len(time)}点, 信号: {len(signal)}点")
            
            # 显示前几个点
            print("前5个点:")
            for i in range(min(5, num_points)):
                print(f"  时间: {time[i]:.6f}s, 信号值: {signal[i]:.6f}")
            
            # 保存测试信号
            save_fsk_signal(time, signal, data, f0, f1, fs)
            print(f"✓ 信号已保存")
            
        except Exception as e:
            print(f"✗ 生成失败: {e}")
        
        print()

def test_generate_fsk_different_lengths():
    """
    测试不同长度的FSK信号生成
    """
    print("=== 测试不同长度的FSK信号 ===\n")
    
    # 测试参数
    valid_lengths = [16, 32, 64, 128]
    data = [0, 1, 0, 1]
    f0 = 1.0
    f1 = 3.0
    fs = 10.0
    
    for num_points in valid_lengths:
        print(f"测试长度: {num_points}点")
        print(f"数据: {data}")
        
        try:
            # 生成FSK信号
            time, signal = generate_fsk_signal(data, f0, f1, fs, num_points)
            
            # 检查结果
            assert len(time) == num_points, f"时间序列长度错误: 预期 {num_points}, 实际 {len(time)}"
            assert len(signal) == num_points, f"信号长度错误: 预期 {num_points}, 实际 {len(signal)}"
            
            print(f"✓ 生成成功 - 时间序列: {len(time)}点, 信号: {len(signal)}点")
            
            # 保存测试信号
            save_fsk_signal(time, signal, data, f0, f1, fs)
            print(f"✓ 信号已保存")
            
        except Exception as e:
            print(f"✗ 生成失败: {e}")
        
        print()

def test_generate_random_data():
    """
    测试生成随机数据的功能
    """
    print("=== 测试生成随机数据 ===\n")
    
    # 测试不同长度的随机数据生成
    lengths = [2, 4, 8, 16]
    
    for length in lengths:
        print(f"生成 {length}位随机数据")
        data = generate_random_data(length)
        print(f"✓ 生成成功: {data}")
        assert len(data) == length, f"数据长度错误: 预期 {length}, 实际 {len(data)}"
        
        # 检查数据是否只包含0和1
        for bit in data:
            assert bit in [0, 1], f"数据包含无效值: {bit}"
        
        print(f"✓ 数据验证成功")
        print()

def main():
    """
    主测试函数
    """
    print("FSK信号生成程序测试脚本\n")
    
    # 运行所有测试
    test_generate_fsk_signal()
    test_generate_fsk_different_lengths()
    test_generate_random_data()
    
    print("=== 所有测试完成 ===")

if __name__ == "__main__":
    main()
