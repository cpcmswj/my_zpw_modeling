#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSK信号生成程序

该程序用于生成二进制频移键控(FSK)信号，支持调整信号长度为16、32、64或128点。

功能包括：
1. 生成指定长度的FSK信号
2. 支持自定义频率参数
3. 支持随机数据或手动输入数据
4. 可视化生成的信号
5. 保存生成的信号数据
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import os

code_dic={"L5":21.3,"L4":23.5,"L3":10.3,"L2":12.5,"HB":24.6,"HU":26.8,
        "L":11.4,"LU":13.6,"LU2":15.8,"U":16.9,"H":29.0,"frequency_change":25.7,
        "U2S":20.2,"U2":14.7,"UUS":19.1,"occupancy_check":27.9,"L6":22.4}
        #低频频率及包含的信息，frequency_change为载频切换，occupancy_check为占用检查


def get_low_frequency(info):
    """
    根据信息查询对应的低频频率
    
    参数：
        info (str): 包含的信息，如"L5", "L4", "HB"等
        
    返回：
        float: 对应的低频频率
    """
    if info in code_dic:
        return code_dic[info]
    else:
        raise ValueError(f"未知的信息类型: {info}，请从以下选项中选择: {list(code_dic.keys())}")


def generate_fsk_signal(data, f0, f1, fs, num_points):
    """
    生成FSK信号
    
    参数：
        data (list): 二进制数据序列，元素为0或1
        f0 (float): 表示0的频率
        f1 (float): 表示1的频率
        fs (float): 采样频率
        num_points (int): 生成的信号长度（点）
    
    返回：
        tuple: (time, signal)，时间序列和对应的FSK信号
    """
    # 计算每个数据位的采样点数
    if len(data) == 0:
        raise ValueError("数据序列不能为空")
    
    # 计算每个比特的采样点数
    samples_per_bit = num_points // len(data)
    
    # 生成时间序列
    time = np.linspace(0, num_points / fs, num_points)
    
    # 生成FSK信号
    signal = np.zeros(num_points)
    
    for i, bit in enumerate(data):
        start = i * samples_per_bit
        end = start + samples_per_bit
        if i == len(data) - 1:
            end = num_points  # 确保最后一个比特覆盖剩余所有采样点
        
        # 选择当前比特对应的频率
        freq = f0 if bit == 0 else f1
        
        # 生成当前比特的信号
        signal[start:end] = np.sin(2 * np.pi * freq * time[start:end])
    
    return time, signal

def generate_random_data(length):
    """
    生成随机二进制数据
    
    参数：
        length (int): 数据长度
    
    返回：
        list: 随机生成的二进制数据序列
    """
    return [random.randint(0, 1) for _ in range(length)]

def input_manual_data():
    """
    手动输入二进制数据
    
    返回：
        list: 手动输入的二进制数据序列
    """
    data_str = input("请输入二进制数据（例如：01010101）: ")
    try:
        data = [int(bit) for bit in data_str]
        for bit in data:
            if bit not in [0, 1]:
                raise ValueError("数据只能包含0和1")
        return data
    except ValueError as e:
        print(f"输入错误: {e}")
        return input_manual_data()

def plot_fsk_signal(time, signal, data, f0, f1, fs):
    """
    绘制FSK信号
    
    参数：
        time (array): 时间序列
        signal (array): FSK信号
        data (list): 二进制数据序列
        f0 (float): 表示0的频率
        f1 (float): 表示1的频率
        fs (float): 采样频率
    """
    plt.figure(figsize=(12, 6))
    
    # 绘制FSK信号
    plt.plot(time, signal, linewidth=2)
    
    # 绘制数据位分隔线
    num_points = len(signal)
    samples_per_bit = num_points // len(data)
    for i in range(len(data) + 1):
        plt.axvline(x=i * samples_per_bit / fs, color='r', linestyle='--', alpha=0.7)
    
    # 绘制数据标签
    for i, bit in enumerate(data):
        plt.text((i + 0.5) * samples_per_bit / fs, max(signal) * 0.9,
                 str(bit), ha='center', va='top', fontsize=12, color='blue', weight='bold')
    
    plt.title(f'FSK Signal (f0={f0}Hz, f1={f1}Hz, fs={fs}Hz, Points={len(signal)})')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.tight_layout()
    
    # 显示图表
    plt.show()

def save_fsk_signal(time, signal, data, f0, f1, fs):
    """
    保存FSK信号到文件
    
    参数：
        time (array): 时间序列
        signal (array): FSK信号
        data (list): 二进制数据序列
        f0 (float): 表示0的频率
        f1 (float): 表示1的频率
        fs (float): 采样频率
    """
    # 创建保存目录
    save_dir = "fsk_signals"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 生成文件名
    data_str = ''.join(map(str, data))
    filename = f"{save_dir}/fsk_signal_{len(signal)}points_f0_{f0}Hz_f1_{f1}Hz_data_{data_str[:20]}.csv"
    
    # 保存数据
    with open(filename, 'w') as f:
        # 写入参数信息
        f.write(f"# FSK Signal Parameters\n")
        f.write(f"# Data: {data_str}\n")
        f.write(f"# f0: {f0}Hz\n")
        f.write(f"# f1: {f1}Hz\n")
        f.write(f"# Sampling Frequency: {fs}Hz\n")
        f.write(f"# Number of Points: {len(signal)}\n")
        f.write("# Time (s), Signal Amplitude\n")
        
        # 写入信号数据
        for t, s in zip(time, signal):
            f.write(f"{t:.8f}, {s:.8f}\n")
    
    print(f"信号已保存到: {filename}")

def fsk_demo():
    """
    FSK信号调制演示
    根据code_dic查询低频频率并生成FSK信号
    """
    print("=== FSK信号调制演示 ===\n")
    
    # 显示可用的信息类型
    print("可用的信息类型及对应的低频频率:")
    for info, freq in sorted(code_dic.items()):
        print(f"  {info}: {freq} Hz")
    
    # 选择信息类型
    while True:
        try:
            info = input("\n请选择信息类型: ")
            f_low = get_low_frequency(info)
            break
        except ValueError as e:
            print(e)
    
    # 载频设置
    print("\n载频设置:")
    try:
        carrier_freq = float(input("请输入载频频率 (Hz，默认1700): ") or "1700")
    except ValueError:
        print("载频必须是数字，将使用默认值1700Hz")
        carrier_freq = 1700
    
    # 生成二进制数据
    data = generate_random_data(8)  # 使用8位二进制数据
    
    # FSK参数设置
    f0 = carrier_freq  # 表示0的频率（载频）
    f1 = carrier_freq + f_low  # 表示1的频率（载频+低频）
    fs = max(f0, f1) * 10  # 采样频率
    num_points = 128  # 信号长度
    
    # 生成FSK信号
    print(f"\n生成FSK信号...")
    print(f"信息: {info}")
    print(f"低频频率: {f_low} Hz")
    print(f"载频: {carrier_freq} Hz")
    print(f"FSK参数: f0={f0}Hz, f1={f1}Hz, fs={fs}Hz")
    print(f"二进制数据: {data}")
    
    time, signal = generate_fsk_signal(data, f0, f1, fs, num_points)
    
    # 显示信号
    plot_fsk_signal(time, signal, data, f0, f1, fs)
    
    # 保存信号
    save_fsk_signal(time, signal, data, f0, f1, fs)
    
    print("\n演示完成!")


def main():
    """
    主程序
    """
    print("=== FSK信号生成程序 ===\n")
    
    # 选择程序模式
    print("程序模式:")
    print("1. 自定义FSK信号生成")
    print("2. 基于信息类型的FSK信号调制演示")
    
    while True:
        try:
            mode_choice = int(input("请选择程序模式 (1-2): "))
            if mode_choice == 1:
                # 自定义FSK信号生成
                # 选择信号长度
                valid_lengths = [16, 32, 64, 128]
                print("\n可选的信号长度:")
                for i, length in enumerate(valid_lengths):
                    print(f"{i+1}. {length}点")
                
                while True:
                    try:
                        choice = int(input("请选择信号长度 (1-4): "))
                        if 1 <= choice <= len(valid_lengths):
                            num_points = valid_lengths[choice - 1]
                            break
                        else:
                            print(f"请输入1-{len(valid_lengths)}之间的数字")
                    except ValueError:
                        print("请输入有效的数字")
                
                # 选择数据生成方式
                print("\n数据生成方式:")
                print("1. 随机生成数据")
                print("2. 手动输入数据")
                
                while True:
                    try:
                        data_choice = int(input("请选择数据生成方式 (1-2): "))
                        if data_choice == 1:
                            data_length = int(input("请输入数据长度: "))
                            data = generate_random_data(data_length)
                            break
                        elif data_choice == 2:
                            data = input_manual_data()
                            break
                        else:
                            print("请输入1或2")
                    except ValueError:
                        print("请输入有效的数字")
                
                # 设置频率参数
                print("\n频率设置:")
                try:
                    f0 = float(input("请输入表示0的频率 (Hz): "))
                    f1 = float(input("请输入表示1的频率 (Hz): "))
                except ValueError:
                    print("频率必须是数字，将使用默认值")
                    f0 = 1.0
                    f1 = 3.0
                
                # 设置采样频率（默认是最高频率的10倍）
                fs = max(f0, f1) * 10
                print(f"\n使用采样频率: {fs}Hz")
                
                # 生成FSK信号
                print("\n生成FSK信号...")
                time, signal = generate_fsk_signal(data, f0, f1, fs, num_points)
                
                # 显示生成的数据
                print(f"\n生成的数据: {data}")
                print(f"数据长度: {len(data)}")
                print(f"信号长度: {len(signal)}点")
                
                # 选择操作
                print("\n操作选项:")
                print("1. 绘制信号")
                print("2. 保存信号")
                print("3. 绘制并保存信号")
                print("4. 仅显示信号数据")
                
                while True:
                    try:
                        action_choice = int(input("请选择操作 (1-4): "))
                        if 1 <= action_choice <= 4:
                            break
                        else:
                            print("请输入1-4之间的数字")
                    except ValueError:
                        print("请输入有效的数字")
                
                if action_choice in [1, 3]:
                    # 绘制信号
                    plot_fsk_signal(time, signal, data, f0, f1, fs)
                
                if action_choice in [2, 3]:
                    # 保存信号
                    save_fsk_signal(time, signal, data, f0, f1, fs)
                
                if action_choice == 4:
                    # 显示信号数据
                    print("\n信号数据 (前20个点):")
                    for i in range(min(20, len(signal))):
                        print(f"时间: {time[i]:.6f}s, 幅值: {signal[i]:.6f}")
                
                break
            elif mode_choice == 2:
                # FSK信号调制演示
                fsk_demo()
                break
            else:
                print("请输入1或2")
        except ValueError:
            print("请输入有效的数字")
    
    print("\n程序执行完成!")

if __name__ == "__main__":
    main()
