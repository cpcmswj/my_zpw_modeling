import numpy as np

"""
电路工具模块
============

包含电路分析中常用的工具函数，如阻抗串联、并联计算，以及电流分配计算等。
"""

def calculate_series_impedance(*impedances):
    """计算任意个阻抗的串联
    
    Args:
        *impedances: 复数形式的阻抗列表
    
    Returns:
        complex: 串联后的总阻抗
    """
    if not impedances:
        return 0
    
    total_impedance = 0
    for impedance in impedances:
        total_impedance += impedance
    
    return total_impedance

def calculate_parallel_impedance(*impedances):
    """计算任意个阻抗的并联
    
    Args:
        *impedances: 复数形式的阻抗列表
    
    Returns:
        complex: 并联后的总阻抗
    """
    if not impedances:
        return 0
    
    total_admittance = 0
    for impedance in impedances:
        if impedance != 0:
            total_admittance += 1 / impedance
        else:
            return 0  # 如果有任何一个阻抗为0，并联总阻抗为0
    
    if total_admittance == 0:
        return 0
    
    return 1 / total_admittance

def calculate_current_distribution(voltage, *impedances):
    """计算阻抗并联时的电流分配
    
    Args:
        voltage: 施加在并联阻抗上的电压（复数形式）
        *impedances: 复数形式的阻抗列表
    
    Returns:
        list: 每个阻抗上的电流（复数形式）
    """
    if not impedances:
        return []
    
    currents = []
    for impedance in impedances:
        if impedance != 0:
            current = voltage / impedance
            currents.append(current)
        else:
            # 如果阻抗为0，电流为无穷大（在实际电路中会短路）
            currents.append(float('inf'))
    
    return currents

def calculate_current_from_total(current_total, *impedances):
    """根据总电流和并联阻抗计算各个阻抗上的电流
    
    Args:
        current_total: 并联电路的总电流（复数形式）
        *impedances: 复数形式的阻抗列表
    
    Returns:
        list: 每个阻抗上的电流（复数形式）
    """
    if not impedances:
        return []
    
    # 计算总阻抗
    total_impedance = calculate_parallel_impedance(*impedances)
    
    # 计算并联电路的电压
    voltage = current_total * total_impedance
    
    # 计算每个阻抗上的电流
    return calculate_current_distribution(voltage, *impedances)
