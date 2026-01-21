#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轨道电路建模演示文件

此文件演示如何使用Error_Of_Trail类构建轨道电路模型并分析不同故障情况。
包括以下内容：
1. 无故障情况下的电路建模
2. 不同故障类型的建模与分析
3. 模型参数的展示
4. 故障特性的分析
"""

import numpy as np
from templates.error_of_trail import Error_Of_Trail

def print_separator(title):
    """打印分隔线，用于区分不同部分的输出"""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}")

def demo_no_fault():
    """演示无故障情况下的电路建模"""
    print_separator("无故障情况建模演示")
    
    # 创建无故障实例
    error_instance = Error_Of_Trail(
        trail="main_track", 
        error_type=0, 
        error_value=0, 
        error_position="69G"
    )
    
    print(f"轨道信息: {error_instance.character()}")
    print(f"状态: {error_instance.status()}")
    
    # 构建电路模型
    model_info = error_instance.build_circuit_model()
    
    # 检查是否有错误
    if "error" in model_info:
        print(f"建模错误: {model_info['error']}")
        return
    
    print("\n基本参数:")
    for key, value in model_info["basic_params"].items():
        print(f"{key}: {value}")
    
    print("\n组件参数:")
    for key, value in model_info["component_params"].items():
        print(f"{key}: {value}")
    
    print("\n故障信息:")
    for key, value in model_info["fault_info"].items():
        print(f"{key}: {value}")
    
    # 测试输入电压响应
    input_voltage = 3+4j  # 复数输入电压
    current, impedance = error_instance.call_input(input_voltage, 1.0)
    print(f"\n输入电压: {input_voltage}V")
    print(f"计算电流: {current:.4f}A")
    print(f"等效阻抗: {impedance:.4f}Ω")
    
    # 计算输出电压
    try:
        output_voltage = error_instance.count_output()
        print(f"输出电压: {output_voltage:.4f}V")
    except Exception as e:
        print(f"计算输出电压时出错: {e}")
    
    # 展示传输矩阵
    print("\n传输矩阵信息:")
    print(f"主轨道传输矩阵:\n{model_info['matrices']['main_track_matrix']}")
    print(f"小轨道传输矩阵:\n{model_info['matrices']['small_track_matrix']}")

def demo_with_faults():
    """演示不同故障类型的建模"""
    print_separator("故障情况建模演示")
    
    # 定义要测试的故障类型
    fault_types = [
        (1, "接收端调谐单元1断路"),
        (3, "接收端空心线圈断路"),
        (4, "接收端空芯线圈短路"),
        (7, "补偿电容3短路")
    ]
    
    for fault_type, fault_desc in fault_types:
        print_separator(f"故障类型: {fault_desc}")
        
        # 创建故障实例
        error_instance = Error_Of_Trail(
            trail="main_track", 
            error_type=fault_type, 
            error_value=1, 
            error_position="69G"
        )
        
        print(f"轨道信息: {error_instance.character()}")
        print(f"状态: {error_instance.status()}")
        
        # 构建电路模型
        model_info = error_instance.build_circuit_model()
        
        # 检查是否有错误
        if "error" in model_info:
            print(f"建模错误: {model_info['error']}")
            continue
        
        # 测试输入电压响应
        input_voltage = 10.0  # 10V输入电压
        current, impedance = error_instance.call_input(input_voltage, 1.0)
        print(f"\n输入电压: {input_voltage}V")
        print(f"计算电流: {current:.4f}A")
        print(f"等效阻抗: {impedance:.4f}Ω")
        
        # 计算输出电压
        try:
            output_voltage = error_instance.count_output()
            print(f"输出电压: {output_voltage:.4f}V")
        except Exception as e:
            print(f"计算输出电压时出错: {e}")
        
        # 简要展示传输矩阵
        print("\n传输矩阵摘要:")
        print(f"主轨道传输矩阵大小: {model_info['matrices']['main_track_matrix'].shape}")
        print(f"小轨道传输矩阵大小: {model_info['matrices']['small_track_matrix'].shape}")

def compare_different_positions():
    """比较不同轨道区段的建模结果"""
    print_separator("不同轨道区段建模比较")
    
    # 测试不同的轨道区段
    positions = ["69G", "57G"]
    
    for position in positions:
        print_separator(f"轨道区段: {position}")
        
        # 创建无故障实例
        error_instance = Error_Of_Trail(
            trail="test_track", 
            error_type=0, 
            error_value=0, 
            error_position=position
        )
        
        print(f"轨道信息: {error_instance.character()}")
        print(f"状态: {error_instance.status()}")
        
        # 构建电路模型
        model_info = error_instance.build_circuit_model()
        
        # 检查是否有错误
        if "error" in model_info:
            print(f"建模错误: {model_info['error']}")
            continue
        
        # 显示基本参数
        basic_params = model_info["basic_params"]
        print(f"\n载频率: {basic_params['frequency']}Hz")
        print(f"补偿电容: {basic_params['capacitance']}uF")
        print(f"补偿电容步长: {basic_params['capacitance_step']}m")
        print(f"变压器变比: {basic_params['transformer_ratio']}")
        
        # 显示组件参数
        component_params = model_info["component_params"]
        print(f"调谐区参数: {component_params['tuner_params']} mΩ")
        print(f"SPT电缆参数: {component_params['spt_params']}")
        
        # 测试输入电压响应
        input_voltage = 5.0  # 5V输入电压
        current, impedance = error_instance.call_input(input_voltage, 1.0)
        print(f"\n输入电压: {input_voltage}V")
        print(f"计算电流: {current:.4f}A")
        print(f"等效阻抗: {impedance:.4f}Ω")

def main():
    """主函数，运行所有演示"""
    print("轨道电路建模系统演示")
    print("This system demonstrates the modeling and analysis of railway track circuits")
    
    # 运行无故障演示
    demo_no_fault()
    
    # 运行故障演示
    demo_with_faults()
    
    # 运行不同区段比较
    compare_different_positions()
    
    print_separator("演示完成")
    print("轨道电路建模系统演示已完成。")
    print("该系统可以用于:")
    print("1. 分析正常情况下的轨道电路参数")
    print("2. 模拟不同类型的故障并分析其影响")
    print("3. 比较不同轨道区段的电路特性")
    print("4. 计算输入输出电压电流关系")

if __name__ == "__main__":
    main()
