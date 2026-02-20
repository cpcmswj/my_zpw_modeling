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

freq_dic={"1700-1":[1701.4,1712.4,1690.4],"1700-2":[1689.7,1709.7,1687.7],
        "2000-1":[2001.4,2012.4,1990.4],"2000-2":[1998.7,2009.7,1987.7],
        "2300-1":[2301.4,2312.4,2290.4],"2300-2":[2298.7,2309.7,2287.7],
        "2600-1":[2601.4,2612.4,2590.4],"2600-2":[2598.7,2609.7,2587.7]}
        #载频类型及对应的频率值，数组内分别为中心值、上边频、下边频
        
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


def get_carrier_frequency(carrier_type):
    """
    根据载频类型查询对应的频率值
    
    参数：
        carrier_type (str): 载频类型，如"1700-1", "1700-2", "2000-1"等
        
    返回：
        list: 对应的频率值数组，分别为中心值、上边频、下边频
    """
    if carrier_type in freq_dic:
        return freq_dic[carrier_type]
    else:
        raise ValueError(f"未知的载频类型: {carrier_type}，请从以下选项中选择: {list(freq_dic.keys())}")


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


def generate_2fsk_signal(data, f0, f1, fs, num_points, modulation_type='non_coherent', phase_continuous=False):
    """
    生成2FSK信号
    
    参数：
        data (list): 二进制数据序列，元素为0或1
        f0 (float): 表示0的频率
        f1 (float): 表示1的频率
        fs (float): 采样频率
        num_points (int): 生成的信号长度（点）
        modulation_type (str): 调制类型，'non_coherent'（非相干）或'coherent'（相干）
        phase_continuous (bool): 是否保持相位连续
    
    返回：
        tuple: (time, signal)，时间序列和对应的2FSK信号
    """
    if len(data) == 0:
        raise ValueError("数据序列不能为空")
    
    # 计算每个比特的采样点数
    samples_per_bit = num_points // len(data)
    
    # 生成时间序列
    time = np.linspace(0, num_points / fs, num_points)
    
    # 生成2FSK信号
    signal = np.zeros(num_points)
    
    # 初始相位
    phase = 0.0
    
    for i, bit in enumerate(data):
        start = i * samples_per_bit
        end = start + samples_per_bit
        if i == len(data) - 1:
            end = num_points  # 确保最后一个比特覆盖剩余所有采样点
        
        # 选择当前比特对应的频率
        freq = f0 if bit == 0 else f1
        
        # 生成当前比特的信号
        if phase_continuous:
            # 连续相位2FSK
            # 计算当前比特的相位增量
            phase_increment = 2 * np.pi * freq / fs
            for j in range(start, end):
                signal[j] = np.sin(phase)
                phase += phase_increment
        else:
            # 非连续相位2FSK
            # 生成当前比特区间的时间
            bit_time = time[start:end] - time[start]
            # 使用不同的调制方式
            if modulation_type == 'coherent':
                # 相干2FSK，保持相位连续性
                phase = (2 * np.pi * freq * time[start]) % (2 * np.pi)
                signal[start:end] = np.sin(2 * np.pi * freq * bit_time + phase)
            else:
                # 非相干2FSK
                signal[start:end] = np.sin(2 * np.pi * freq * bit_time)
    
    return time, signal


def generate_gfsk_signal(data, f0, f1, fs, num_points, bt=0.5, sigma=None):
    """
    生成高斯频移键控（GFSK）信号
    
    参数：
        data (list): 二进制数据序列，元素为0或1
        f0 (float): 表示0的频率
        f1 (float): 表示1的频率
        fs (float): 采样频率
        num_points (int): 生成的信号长度（点）
        bt (float): 带宽时间乘积，默认0.5
        sigma (float): 高斯滤波器的标准差，默认None，根据bt自动计算
    
    返回：
        tuple: (time, signal)，时间序列和对应的GFSK信号
    """
    if len(data) == 0:
        raise ValueError("数据序列不能为空")
    
    # 计算每个比特的采样点数
    samples_per_bit = num_points // len(data)
    
    # 生成时间序列
    time = np.linspace(0, num_points / fs, num_points)
    
    # 计算频率偏移
    freq_dev = abs(f1 - f0) / 2
    
    # 生成矩形脉冲序列
    pulse = np.zeros(num_points)
    for i, bit in enumerate(data):
        start = i * samples_per_bit
        end = start + samples_per_bit
        if i == len(data) - 1:
            end = num_points  # 确保最后一个比特覆盖剩余所有采样点
        
        # 生成NRZ编码
        pulse[start:end] = 2 * bit - 1  # 将0转换为-1，1保持为1
    
    # 设计高斯滤波器
    if sigma is None:
        # 根据带宽时间乘积计算标准差
        sigma = samples_per_bit / (2 * np.sqrt(2 * np.log(2))) / bt
    
    # 生成高斯脉冲
    gaussian_pulse = np.exp(-0.5 * (np.arange(-3*sigma, 3*sigma+1) / sigma) ** 2)
    gaussian_pulse /= np.sum(gaussian_pulse)  # 归一化
    
    # 对矩形脉冲进行高斯滤波
    filtered_pulse = np.convolve(pulse, gaussian_pulse, mode='same')
    
    # 生成频率调制信号
    signal = np.zeros(num_points)
    phase = 0.0
    
    for i in range(num_points):
        # 积分计算相位
        phase += 2 * np.pi * freq_dev * filtered_pulse[i] / fs
        signal[i] = np.sin(2 * np.pi * ((f0 + f1) / 2) * time[i] + phase)
    
    return time, signal


def generate_alternating_2fsk_signal(code_info, carrier_type, fs, num_points):
    """
    生成交替发送0和1的2FSK信号
    从code_dic中选择频率作为频率差，从freq_dic中选择上下边频分别作为0和1的载频
    
    参数：
        code_info (str): 从code_dic中选择的信息类型，用于确定频率差
        carrier_type (str): 从freq_dic中选择的载频类型，用于确定上下边频
        fs (float): 采样频率
        num_points (int): 生成的信号长度（点）
    
    返回：
        tuple: (time, signal, data, f0, f1)，时间序列、对应的2FSK信号、生成的二进制数据、表示0的频率、表示1的频率
    """
    # 从code_dic中获取频率差
    if code_info not in code_dic:
        raise ValueError(f"未知的信息类型: {code_info}，请从以下选项中选择: {list(code_dic.keys())}")
    freq_diff = code_dic[code_info]
    
    # 从freq_dic中获取上下边频
    if carrier_type not in freq_dic:
        raise ValueError(f"未知的载频类型: {carrier_type}，请从以下选项中选择: {list(freq_dic.keys())}")
    freq_values = get_carrier_frequency(carrier_type)
    center_freq = freq_values[0]
    upper_freq = freq_values[1]  # 上边频
    lower_freq = freq_values[2]  # 下边频
    
    # 使用下边频作为0的载频，上边频作为1的载频
    # 结合code_dic中的频率差来调整载频
    f0 = lower_freq
    f1 = upper_freq
    
    # 生成交替发送0和1的二进制数据
    # 计算数据长度，确保每个比特至少有一定数量的采样点
    min_samples_per_bit = 10  # 每个比特的最小采样点数
    max_data_length = num_points // min_samples_per_bit
    data_length = min(max_data_length, 16)  # 最多16个比特
    
    # 生成交替的0和1数据
    data = [i % 2 for i in range(data_length)]
    
    # 生成2FSK信号
    time, signal = generate_2fsk_signal(data, f0, f1, fs, num_points)
    
    return time, signal, data, f0, f1


def calculate_2fsk_parameters(data, f0, f1, fs):
    """
    计算2FSK信号的参数
    
    参数：
        data (list): 二进制数据序列
        f0 (float): 表示0的频率
        f1 (float): 表示1的频率
        fs (float): 采样频率
    
    返回：
        dict: 包含2FSK信号的参数
    """
    # 计算比特率
    bit_rate = fs / (len(data) / len(data))
    
    # 计算频率偏移
    freq_dev = abs(f1 - f0) / 2
    
    # 计算调制指数
    modulation_index = freq_dev / bit_rate
    
    # 计算带宽
    bandwidth = 2 * (freq_dev + bit_rate)
    
    return {
        'bit_rate': bit_rate,
        'frequency_deviation': freq_dev,
        'modulation_index': modulation_index,
        'bandwidth': bandwidth,
        'f0': f0,
        'f1': f1,
        'fs': fs
    }

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
    print("3. 自定义2FSK信号生成")
    print("4. 生成GFSK信号")
    print("5. 生成交替发送0和1的2FSK信号")
    print("6. 根据载频类型查询频率值")
    
    while True:
        try:
            mode_choice = int(input("请选择程序模式 (1-6): "))
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
            elif mode_choice == 3:
                # 自定义2FSK信号生成
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
                    f0 = 1000.0
                    f1 = 1500.0
                
                # 设置采样频率（默认是最高频率的10倍）
                fs = max(f0, f1) * 10
                print(f"\n使用采样频率: {fs}Hz")
                
                # 选择调制类型
                print("\n调制类型:")
                print("1. 非相干调制")
                print("2. 相干调制")
                modulation_choice = input("请选择调制类型 (1-2，默认1): ") or "1"
                modulation_type = 'non_coherent' if modulation_choice == "1" else 'coherent'
                
                # 选择是否保持相位连续
                phase_continuous = input("是否保持相位连续? (y/n，默认n): ").lower() == "y"
                
                # 生成2FSK信号
                print("\n生成2FSK信号...")
                time, signal = generate_2fsk_signal(data, f0, f1, fs, num_points, modulation_type, phase_continuous)
                
                # 计算2FSK参数
                fsk_params = calculate_2fsk_parameters(data, f0, f1, fs)
                
                # 显示生成的数据和参数
                print(f"\n生成的数据: {data}")
                print(f"数据长度: {len(data)}")
                print(f"信号长度: {len(signal)}点")
                print(f"调制类型: {modulation_type}")
                print(f"相位连续: {phase_continuous}")
                print(f"比特率: {fsk_params['bit_rate']:.2f} bps")
                print(f"频率偏移: {fsk_params['frequency_deviation']:.2f} Hz")
                print(f"调制指数: {fsk_params['modulation_index']:.2f}")
                print(f"带宽: {fsk_params['bandwidth']:.2f} Hz")
                
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
            elif mode_choice == 4:
                # 生成GFSK信号
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
                    f0 = 1000.0
                    f1 = 1500.0
                
                # 设置采样频率（默认是最高频率的10倍）
                fs = max(f0, f1) * 10
                print(f"\n使用采样频率: {fs}Hz")
                
                # 设置带宽时间乘积
                try:
                    bt = float(input("请输入带宽时间乘积 (默认0.5): ") or "0.5")
                except ValueError:
                    print("带宽时间乘积必须是数字，将使用默认值0.5")
                    bt = 0.5
                
                # 生成GFSK信号
                print("\n生成GFSK信号...")
                time, signal = generate_gfsk_signal(data, f0, f1, fs, num_points, bt)
                
                # 显示生成的数据
                print(f"\n生成的数据: {data}")
                print(f"数据长度: {len(data)}")
                print(f"信号长度: {len(signal)}点")
                print(f"带宽时间乘积: {bt}")
                
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
            elif mode_choice == 5:
                # 生成交替发送0和1的2FSK信号
                print("=== 生成交替发送0和1的2FSK信号 ===\n")
                
                # 显示可用的信息类型
                print("可用的信息类型及对应的频率:")
                for info, freq in sorted(code_dic.items()):
                    print(f"  {info}: {freq} Hz")
                
                # 选择信息类型
                while True:
                    try:
                        code_info = input("\n请选择信息类型: ")
                        if code_info not in code_dic:
                            raise ValueError(f"未知的信息类型: {code_info}，请从以下选项中选择: {list(code_dic.keys())}")
                        break
                    except ValueError as e:
                        print(e)
                
                # 显示可用的载频类型
                print("\n可用的载频类型及对应的频率值:")
                for carrier_type, freqs in sorted(freq_dic.items()):
                    print(f"  {carrier_type}: 中心值={freqs[0]}Hz, 上边频={freqs[1]}Hz, 下边频={freqs[2]}Hz")
                
                # 选择载频类型
                while True:
                    try:
                        carrier_type = input("\n请选择载频类型: ")
                        if carrier_type not in freq_dic:
                            raise ValueError(f"未知的载频类型: {carrier_type}，请从以下选项中选择: {list(freq_dic.keys())}")
                        break
                    except ValueError as e:
                        print(e)
                
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
                
                # 设置采样频率
                # 从freq_dic中获取频率值以计算合适的采样频率
                freq_values = get_carrier_frequency(carrier_type)
                max_freq = max(freq_values)
                fs = max_freq * 10  # 采样频率设为最高频率的10倍
                print(f"\n使用采样频率: {fs}Hz")
                
                # 生成交替发送0和1的2FSK信号
                print("\n生成交替发送0和1的2FSK信号...")
                time, signal, data, f0, f1 = generate_alternating_2fsk_signal(
                    code_info, carrier_type, fs, num_points
                )
                
                # 显示生成的信号信息
                print(f"\n生成结果:")
                print(f"  选择的信息类型: {code_info}")
                print(f"  选择的载频类型: {carrier_type}")
                print(f"  生成的数据: {data}")
                print(f"  数据长度: {len(data)}")
                print(f"  0的载频: {f0} Hz")
                print(f"  1的载频: {f1} Hz")
                print(f"  信号长度: {len(signal)} 点")
                
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
            elif mode_choice == 6:
                # 根据载频类型查询频率值
                print("=== 根据载频类型查询频率值 ===\n")
                
                # 显示可用的载频类型
                print("可用的载频类型及对应的频率值:")
                for carrier_type, freqs in sorted(freq_dic.items()):
                    print(f"  {carrier_type}: 中心值={freqs[0]}Hz, 上边频={freqs[1]}Hz, 下边频={freqs[2]}Hz")
                
                # 选择载频类型
                while True:
                    try:
                        carrier_type = input("\n请选择载频类型: ")
                        frequencies = get_carrier_frequency(carrier_type)
                        break
                    except ValueError as e:
                        print(e)
                
                # 显示查询结果
                print(f"\n查询结果:")
                print(f"载频类型: {carrier_type}")
                print(f"中心值: {frequencies[0]} Hz")
                print(f"上边频: {frequencies[1]} Hz")
                print(f"下边频: {frequencies[2]} Hz")
                break
            else:
                print("请输入1-6之间的数字")
        except ValueError:
            print("请输入有效的数字")
    
    print("\n程序执行完成!")

if __name__ == "__main__":
    main()
