#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试将电路模型参数导出为CSV文件的功能
"""

from templates.error_of_trail import Error_Of_Trail
from output_csv import export_circuit_model_to_csv

def test_export_circuit_model():
    """测试导出电路模型参数到CSV文件"""
    # 创建无故障实例
    error_instance = Error_Of_Trail(
        trail="main_track", 
        error_type=0, 
        error_value=0, 
        error_position="69G"
    )
    
    print("创建无故障实例成功")
    print(f"轨道信息: {error_instance.character()}")
    print(f"状态: {error_instance.status()}")
    
    # 构建电路模型
    model_info = error_instance.build_circuit_model()
    print("构建电路模型成功")
    
    # 测试导出基本电路模型参数
    export_circuit_model_to_csv("circuit_model_basic.csv", model_info, include_matrices=False)
    print("导出基本电路模型参数成功")
    
    # 测试导出包含矩阵的电路模型参数
    export_circuit_model_to_csv("circuit_model_with_matrices.csv", model_info, include_matrices=True)
    print("导出包含矩阵的电路模型参数成功")
    
    # 创建故障实例
    error_instance_fault = Error_Of_Trail(
        trail="main_track", 
        error_type=1, 
        error_value=1, 
        error_position="69G"
    )
    
    print("\n创建故障实例成功")
    print(f"轨道信息: {error_instance_fault.character()}")
    print(f"状态: {error_instance_fault.status()}")
    
    # 构建故障电路模型
    model_info_fault = error_instance_fault.build_circuit_model()
    print("构建故障电路模型成功")
    
    # 测试导出故障电路模型参数
    export_circuit_model_to_csv("circuit_model_fault.csv", model_info_fault, include_matrices=False)
    print("导出故障电路模型参数成功")

if __name__ == "__main__":
    test_export_circuit_model()
