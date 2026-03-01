#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试轨道长度输入为1000时的情况
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from templates.error_of_trail import Error_Of_Trail

def test_track_length_1000():
    """测试轨道长度为1000时的情况"""
    print("测试轨道长度为1000时的情况...")
    
    # 创建一个实例，轨道长度为1000
    error_instance = Error_Of_Trail(
        trail="test", 
        error_type=0, 
        error_value=0, 
        error_position="69G", 
        length_parameter=1000.0, 
        SPT_cable_length=10.0
    )
    
    print(f"初始长度参数: {error_instance.length_parameter}")
    print(f"Variable.length_guidao: {error_instance.parameter.length_guidao}")
    
    # 重新初始化参数，轨道长度仍然为1000
    error_instance.reinitialize_parameters(
        length_parameter=1000.0
    )
    
    print(f"重新初始化后长度参数: {error_instance.length_parameter}")
    print(f"重新初始化后Variable.length_guidao: {error_instance.parameter.length_guidao}")
    
    # 测试其他长度值
    test_lengths = [999, 1000, 1001]
    for length in test_lengths:
        print(f"\n测试长度: {length}")
        error_instance.reinitialize_parameters(
            length_parameter=length
        )
        print(f"长度参数: {error_instance.length_parameter}")
        print(f"Variable.length_guidao: {error_instance.parameter.length_guidao}")

if __name__ == "__main__":
    test_track_length_1000()
