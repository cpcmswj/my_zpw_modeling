#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建波形导入演示数据文件

生成一个包含不同波形数据的Excel文件，用于演示waveform_import功能。
"""

import os
import math
from openpyxl import Workbook


def generate_sine_wave(samples, frequency, amplitude, phase=0):
    """生成正弦波数据"""
    wave = []
    for i in range(samples):
        t = i / 1000  # 假设采样频率为1000Hz
        value = amplitude * math.sin(2 * math.pi * frequency * t + phase)
        wave.append(value)
    return wave


def generate_square_wave(samples, frequency, amplitude):
    """生成方波数据"""
    wave = []
    for i in range(samples):
        t = i / 1000  # 假设采样频率为1000Hz
        value = amplitude if math.sin(2 * math.pi * frequency * t) >= 0 else -amplitude
        wave.append(value)
    return wave


def generate_triangle_wave(samples, frequency, amplitude):
    """生成三角波数据"""
    wave = []
    period = 1000 / frequency  # 周期（采样点）
    for i in range(samples):
        t = (i % period) / period
        if t < 0.25:
            value = 4 * amplitude * t
        elif t < 0.75:
            value = amplitude - 4 * amplitude * (t - 0.25)
        else:
            value = -amplitude + 4 * amplitude * (t - 0.75)
        wave.append(value)
    return wave


def generate_noise(samples, amplitude):
    """生成噪声数据"""
    import random
    wave = []
    for _ in range(samples):
        value = amplitude * (random.random() * 2 - 1)
        wave.append(value)
    return wave


def create_demo_file():
    """创建演示数据文件"""
    # 创建工作簿
    wb = Workbook()
    
    # 创建正弦波工作表
    ws_sine = wb.active
    ws_sine.title = "正弦波"
    
    # 添加表头
    ws_sine['A1'] = "时间 (ms)"
    ws_sine['B1'] = "1Hz正弦波"
    ws_sine['C1'] = "2Hz正弦波"
    ws_sine['D1'] = "5Hz正弦波"
    
    # 生成数据
    samples = 2000  # 2秒的数据，采样频率1000Hz
    sine1 = generate_sine_wave(samples, 1, 1)
    sine2 = generate_sine_wave(samples, 2, 0.8)
    sine3 = generate_sine_wave(samples, 5, 0.5)
    
    # 填充数据
    for i in range(samples):
        ws_sine[f'A{i+2}'] = i
        ws_sine[f'B{i+2}'] = sine1[i]
        ws_sine[f'C{i+2}'] = sine2[i]
        ws_sine[f'D{i+2}'] = sine3[i]
    
    # 创建方波和三角波工作表
    ws_other = wb.create_sheet(title="方波和三角波")
    
    # 添加表头
    ws_other['A1'] = "时间 (ms)"
    ws_other['B1'] = "1Hz方波"
    ws_other['C1'] = "2Hz三角波"
    ws_other['D1'] = "噪声"
    
    # 生成数据
    square = generate_square_wave(samples, 1, 1)
    triangle = generate_triangle_wave(samples, 2, 0.8)
    noise = generate_noise(samples, 0.2)
    
    # 填充数据
    for i in range(samples):
        ws_other[f'A{i+2}'] = i
        ws_other[f'B{i+2}'] = square[i]
        ws_other[f'C{i+2}'] = triangle[i]
        ws_other[f'D{i+2}'] = noise[i]
    
    # 保存文件
    output_dir = "static"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, "waveform_demo.xlsx")
    wb.save(output_path)
    print(f"演示数据文件已生成：{output_path}")


if __name__ == "__main__":
    create_demo_file()
