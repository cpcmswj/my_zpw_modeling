#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Error_Of_Trail 类的 reinitialize_parameters 方法
"""

import sys
import os

# 添加父目录到系统路径，以便导入templates模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from templates.error_of_trail import Error_Of_Trail

def test_reinitialize_parameters():
    """测试 reinitialize_parameters 方法"""
    print("=== 测试 Error_Of_Trail.reinitialize_parameters 方法 ===\n")
    
    # 1. 创建初始实例
    print("1. 创建初始实例:")
    error_instance = Error_Of_Trail(
        trail="test", 
        error_type=0, 
        error_value=0, 
        error_position="69G"
    )
    print(f"初始状态: {error_instance.character()}")
    print(f"初始长度参数: {error_instance.length_parameter}m")
    print(f"初始频率: {error_instance.parameter.frequency}Hz")
    print(f"初始每米电阻: {error_instance.parameter.resist_per_meter}Ω/m")
    print()
    
    # 2. 测试重新初始化故障参数
    print("2. 测试重新初始化故障参数:")
    error_instance.reinitialize_parameters(
        error_type=1, 
        error_value=10, 
        error_position="3DG"
    )
    print(f"重新初始化后: {error_instance.character()}")
    print()
    
    # 3. 测试重新初始化长度参数
    print("3. 测试重新初始化长度参数:")
    error_instance.reinitialize_parameters(length_parameter=200.0)
    print(f"重新初始化后长度: {error_instance.length_parameter}m")
    print()
    
    # 4. 测试重新初始化材料参数
    print("4. 测试重新初始化材料参数:")
    error_instance.reinitialize_parameters(
        resist_per_meter=0.2, 
        induct_per_meter=2.0e-3, 
        capacit_per_meter=2.0e-9, 
        conduct_per_meter=2.0e-6
    )
    print()
    
    # 5. 测试一次性重新初始化所有参数
    print("5. 测试一次性重新初始化所有参数:")
    error_instance.reinitialize_parameters(
        error_type=2, 
        error_value=20, 
        error_position="IG1",
        length_parameter=150.0,
        resist_per_meter=0.15,
        induct_per_meter=1.5e-3,
        capacit_per_meter=1.5e-9,
        conduct_per_meter=1.5e-6
    )
    print(f"最终状态: {error_instance.character()}")
    print()
    
    # 6. 测试构建电路模型
    print("6. 测试构建电路模型:")
    model = error_instance.build_circuit_model()
    if model and "basic_params" in model:
        print("电路模型构建成功!")
        print(f"模型频率: {model['basic_params']['frequency']}Hz")
        print(f"模型电容: {model['basic_params']['capacitance']}uF")
    else:
        print("电路模型构建失败!")
    print()
    
    # 7. 测试输出计算
    print("7. 测试输出计算:")
    output = error_instance.count_output()
    print(f"输出电压: {output}")
    print()
    
    print("=== 测试完成 ===")

if __name__ == "__main__":
    test_reinitialize_parameters()