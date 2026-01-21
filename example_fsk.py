#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSK信号生成程序示例

该脚本演示了如何使用FSK信号生成程序生成不同参数的FSK信号，并保存和可视化生成的信号。
"""

from build_fsk_signal import generate_fsk_signal, generate_random_data, plot_fsk_signal, save_fsk_signal

def example_basic():
    """
    基本示例：生成简单的FSK信号
    """
    print("=== 基本示例 ===\n")
    
    # 示例参数
    data = [0, 1, 0, 1]  # 二进制数据
    f0 = 1.0  # 表示0的频率
    f1 = 3.0  # 表示1的频率
    fs = 10.0  # 采样频率
    num_points = 64  # 信号长度（点）
    
    print(f"数据: {data}")
    print(f"f0: {f0}Hz, f1: {f1}Hz, fs: {fs}Hz, 点数: {num_points}")
    
    # 生成FSK信号
    time, signal = generate_fsk_signal(data, f0, f1, fs, num_points)
    print(f"生成成功 - 时间序列: {len(time)}点, 信号: {len(signal)}点")
    
    # 保存信号
    save_fsk_signal(time, signal, data, f0, f1, fs)
    
    # 绘制信号
    plot_fsk_signal(time, signal, data, f0, f1, fs)

def example_random_data():
    """
    示例：使用随机数据生成FSK信号
    """
    print("\n=== 随机数据示例 ===\n")
    
    # 示例参数
    data_length = 8  # 数据长度
    f0 = 2.0  # 表示0的频率
    f1 = 5.0  # 表示1的频率
    fs = 20.0  # 采样频率
    num_points = 128  # 信号长度（点）
    
    # 生成随机数据
    data = generate_random_data(data_length)
    print(f"随机生成的数据: {data}")
    print(f"f0: {f0}Hz, f1: {f1}Hz, fs: {fs}Hz, 点数: {num_points}")
    
    # 生成FSK信号
    time, signal = generate_fsk_signal(data, f0, f1, fs, num_points)
    print(f"生成成功 - 时间序列: {len(time)}点, 信号: {len(signal)}点")
    
    # 保存信号
    save_fsk_signal(time, signal, data, f0, f1, fs)
    
    # 绘制信号
    plot_fsk_signal(time, signal, data, f0, f1, fs)

def example_different_lengths():
    """
    示例：生成不同长度的FSK信号
    """
    print("\n=== 不同长度信号示例 ===\n")
    
    # 示例参数
    data = [1, 0, 1, 0, 1, 0]  # 二进制数据
    f0 = 1.5  # 表示0的频率
    f1 = 4.5  # 表示1的频率
    fs = 15.0  # 采样频率
    
    # 生成不同长度的信号
    for num_points in [16, 32, 64, 128]:
        print(f"生成 {num_points}点信号...")
        
        # 生成FSK信号
        time, signal = generate_fsk_signal(data, f0, f1, fs, num_points)
        print(f"✓ 生成成功 - 时间序列: {len(time)}点, 信号: {len(signal)}点")
        
        # 保存信号
        save_fsk_signal(time, signal, data, f0, f1, fs)
    
    print("所有信号已生成并保存")

def main():
    """
    主示例函数
    """
    print("FSK信号生成程序示例\n")
    
    # 运行基本示例
    example_basic()
    
    # 运行随机数据示例
    example_random_data()
    
    # 运行不同长度信号示例
    example_different_lengths()
    
    print("\n=== 示例完成 ===")
    print("所有示例信号已生成并保存到 fsk_signals 目录")

if __name__ == "__main__":
    main()
