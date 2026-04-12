#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
随机参数生成器

用于生成随机化的参数，包括SPT电缆参数和F1F2调谐单元各元件的参数。

使用方法：
    from random_parameters import generate_random_SPT_cable_params, generate_random_tuning_unit_params
    
    # 生成随机SPT电缆参数
    gamma_cable, Z_d, phi = generate_random_SPT_cable_params(frequency, variation=0.1)
    
    # 生成随机F1F2调谐单元参数
    param = generate_random_tuning_unit_params(f, unit, variation=0.05)
"""

import random
import numpy as np

# SPT电缆参数范围表
# 格式：[频率(Hz), 中间值, 增减区间]
SPT_CABLE_RANGES = {
    1700: {
        'gamma_cable': {'center': 0.63, 'interval': 0.063},     # 传输常数中间值0.63dB/km, ±0.13
        'Z_d': {'center': 396, 'interval': 12},            # 特性阻抗中间值396Ω, ±44
        'phi': {'center': -39, 'interval': 1.2}            # 阻抗角中间值-39°, ±1.2
    },
    2000: {
        'gamma_cable': {'center': 0.68, 'interval': 0.068},
        'Z_d': {'center': 367, 'interval': 11},
        'phi': {'center': -38, 'interval': 1.1}
    },
    2300: {
        'gamma_cable': {'center': 0.72, 'interval': 0.072},
        'Z_d': {'center': 343, 'interval': 10},
        'phi': {'center': -37, 'interval': 1.1}
    },
    2600: {
        'gamma_cable': {'center': 0.75, 'interval': 0.075},
        'Z_d': {'center': 325, 'interval': 10},
        'phi': {'center': -36, 'interval': 1.1}
    }
}

# F1F2调谐单元参数范围表
# 格式：[类型, 元件, 下限, 上限]
TUNING_UNIT_RANGES = {
    'F1': {
        'L1': {'min': 33.5, 'max': 34.6},   # L1, uH，测量值
        'C1': {'min': 121.0, 'max': 127.0}    # C1, uF，测量值
    },
    'F2': {
        'L2': {'min': 88.0, 'max': 89.0},   # L2, uH，测量值
        'C2': {'min': 89.0, 'max': 93.0},    # C2, uF，测量值
        'C3': {'min': 228.0, 'max': 260.0}   # C3, uF，测量值
    }
}

# 电平档位参数范围表（信号输出端电压幅值）
# 格式：[档位, 下限(V), 上限(V)]
VOLTAGE_LEVEL_RANGES = {
    1: {'min': 161, 'max': 170},      # 档位1: 161-170V
    2: {'min': 146, 'max': 154},       # 档位2: 146-154V
    3: {'min': 128, 'max': 135},        # 档位3: 128-135V
    4: {'min': 104.5, 'max': 110.5},        # 档位4: 104.5-110.5V
    5: {'min': 75, 'max': 79.5}         # 档位5: 75-79.5V
}

# 轨道电路长度区间表
# 格式：[区间编号, 下限(m), 上限(m)]
TRACK_CIRCUIT_LENGTH_RANGES = {}
# 生成300~350, 351~400……直到1401~1450的区间
for i in range(0, 23):
    lower = 300 + i * 50
    upper = 350 + i * 50
    if i > 0:
        lower += 1
    TRACK_CIRCUIT_LENGTH_RANGES[i+1] = {'min': lower, 'max': upper}

def generate_random_SPT_cable_params(frequency, variation=0.1):
    """生成随机的SPT电缆参数
    
    参数：
        frequency: int, 频率(Hz)，取值为1700, 2000, 2300, 2600
        variation: float, 随机变化范围，默认为10%
    
    返回：
        tuple: (gamma_cable, Z_d, phi)，传输常数(dB/km)、特性阻抗(Ω)、阻抗角(°)
    """
    if frequency not in SPT_CABLE_RANGES:
        raise ValueError(f"不支持的频率: {frequency}，支持的频率为: {list(SPT_CABLE_RANGES.keys())}")
    
    ranges = SPT_CABLE_RANGES[frequency]
    
    # 根据中间值和增减区间生成随机值
    gamma_center = ranges['gamma_cable']['center']
    gamma_interval = ranges['gamma_cable']['interval']
    gamma_cable = random.uniform(gamma_center - gamma_interval, gamma_center + gamma_interval)
    
    Z_d_center = ranges['Z_d']['center']
    Z_d_interval = ranges['Z_d']['interval']
    Z_d = random.uniform(Z_d_center - Z_d_interval, Z_d_center + Z_d_interval)
    
    phi_center = ranges['phi']['center']
    phi_interval = ranges['phi']['interval']
    phi = random.uniform(phi_center - phi_interval, phi_center + phi_interval)
    
    return gamma_cable, Z_d, phi

def generate_random_tuning_unit_params(f, unit, variation=None):
    """生成随机的F1F2调谐单元参数
    
    参数：
        f: int, 调谐单元类型，1表示F1，2表示F2
        unit: int, 元件编号，1-3表示不同元件
        variation: float, 已弃用，保留用于兼容性
    
    返回：
        float: 随机生成的参数值
    """
    # 映射单元类型
    unit_map = {
        1: {
            1: 'L1',  # L1, uH
            2: 'C1'   # C1, uF
        },
        2: {
            1: 'L2',  # L2, uH
            2: 'C2',  # C2, uF
            3: 'C3'   # C3, uF
        }
    }
    
    # 检查输入有效性
    if f not in unit_map:
        raise ValueError(f"不支持的调谐单元类型: {f}，支持的类型为: {list(unit_map.keys())}")
    
    if unit not in unit_map[f]:
        raise ValueError(f"不支持的元件编号: {unit}，支持的编号为: {list(unit_map[f].keys())}")
    
    # 获取参数类型
    tuner_type = 'F1' if f == 1 else 'F2'
    param_name = unit_map[f][unit]
    
    # 获取下限和上限
    param_info = TUNING_UNIT_RANGES[tuner_type][param_name]
    min_val = param_info['min']
    max_val = param_info['max']
    
    # 生成随机值
    random_val = random.uniform(min_val, max_val)
    
    return random_val

def generate_random_frequency_params(frequency, variation=0.1):
    """生成完整的随机频率参数集
    
    参数：
        frequency: int, 频率(Hz)
        variation: float, 随机变化范围
    
    返回：
        dict: 包含所有随机参数的字典
    """
    return {
        'SPT_cable': {
            'gamma_cable': generate_random_SPT_cable_params(frequency, variation)[0],
            'Z_d': generate_random_SPT_cable_params(frequency, variation)[1],
            'phi': generate_random_SPT_cable_params(frequency, variation)[2]
        },
        'F1': {
            'L1': generate_random_tuning_unit_params(1, 1, variation),
            'C1': generate_random_tuning_unit_params(1, 2, variation)
        },
        'F2': {
            'L2': generate_random_tuning_unit_params(2, 1, variation),
            'C2': generate_random_tuning_unit_params(2, 2, variation),
            'C3': generate_random_tuning_unit_params(2, 3, variation)
        }
    }

def generate_random_voltage_level_params(level):
    """根据电平档位生成随机的输出电压幅值
    
    参数：
        level: int, 电平档位，取值为1, 2, 3, 4, 5
    
    返回：
        float: 随机生成的输出电压幅值(V)
    """
    if level not in VOLTAGE_LEVEL_RANGES:
        raise ValueError(f"不支持的电平档位: {level}，支持的档位为: {list(VOLTAGE_LEVEL_RANGES.keys())}")
    
    voltage_range = VOLTAGE_LEVEL_RANGES[level]
    min_voltage = voltage_range['min']
    max_voltage = voltage_range['max']
    
    # 生成随机电压值
    voltage = random.uniform(min_voltage, max_voltage)
    
    return voltage

def generate_random_track_circuit_length(range_number):
    """根据区间编号生成随机的轨道电路长度
    
    参数：
        range_number: int, 区间编号，取值为1-23
                     1: 300~350m
                     2: 351~400m
                     ...
                     23: 1401~1450m
    
    返回：
        float: 随机生成的轨道电路长度(m)
    """
    if range_number not in TRACK_CIRCUIT_LENGTH_RANGES:
        raise ValueError(f"不支持的区间编号: {range_number}，支持的编号为: {list(TRACK_CIRCUIT_LENGTH_RANGES.keys())}")
    
    length_range = TRACK_CIRCUIT_LENGTH_RANGES[range_number]
    min_length = length_range['min']
    max_length = length_range['max']
    
    # 生成随机长度值
    length = random.uniform(min_length, max_length)
    
    return length

if __name__ == "__main__":
    # 测试生成随机SPT电缆参数
    print("=== 测试随机SPT电缆参数生成 ===")
    for freq in [1700, 2000, 2300, 2600]:
        gamma, Z_d, phi = generate_random_SPT_cable_params(freq, variation=0.1)
        print(f"频率 {freq}Hz: 传输常数={gamma:.3f}dB/km, 特性阻抗={Z_d:.1f}Ω, 阻抗角={phi:.1f}°")
    
    # 测试生成随机调谐单元参数
    print("\n=== 测试随机调谐单元参数生成 ===")
    # F1参数
    print("F1调谐单元:")
    for unit in [1, 2]:
        param = generate_random_tuning_unit_params(1, unit, variation=0.05)
        param_name = "L1 (uH)" if unit == 1 else "C1 (uF)"
        print(f"  {param_name}: {param:.3f}")
    
    # F2参数
    print("F2调谐单元:")
    for unit in [1, 2, 3]:
        param = generate_random_tuning_unit_params(2, unit, variation=0.05)
        if unit == 1:
            param_name = "L2 (uH)"
        elif unit == 2:
            param_name = "C2 (uF)"
        else:
            param_name = "C3 (uF)"
        print(f"  {param_name}: {param:.3f}")
    
    # 测试生成完整参数集
    print("\n=== 测试生成完整参数集 ===")
    params = generate_random_frequency_params(1700, variation=0.1)
    print(f"SPT电缆参数: {params['SPT_cable']}")
    print(f"F1参数: {params['F1']}")
    print(f"F2参数: {params['F2']}")
    
    # 测试生成随机电平档位参数
    print("\n=== 测试随机电平档位参数生成 ===")
    for level in [1, 2, 3, 4, 5]:
        voltage = generate_random_voltage_level_params(level)
        range_info = VOLTAGE_LEVEL_RANGES[level]
        print(f"  档位{level}: 电压={voltage:.2f}V (范围: {range_info['min']}-{range_info['max']}V)")
    
    # 测试生成随机轨道电路长度
    print("\n=== 测试随机轨道电路长度生成 ===")
    # 测试几个不同的区间
    test_ranges = [1, 5, 10, 15, 20, 23]
    for range_num in test_ranges:
        length = generate_random_track_circuit_length(range_num)
        range_info = TRACK_CIRCUIT_LENGTH_RANGES[range_num]
        print(f"  区间{range_num}: 长度={length:.2f}m (范围: {range_info['min']}-{range_info['max']}m)")
