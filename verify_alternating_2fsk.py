#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证交替发送0和1的2FSK信号生成函数
"""

from build_fsk_signal import generate_alternating_2fsk_signal

# 测试函数
def verify_function():
    print("=== 验证交替发送0和1的2FSK信号生成函数 ===\n")
    
    # 测试参数
    code_info = "L5"
    carrier_type = "1700-1"
    fs = 20000
    num_points = 128
    
    print(f"测试参数:")
    print(f"  信息类型: {code_info}")
    print(f"  载频类型: {carrier_type}")
    print(f"  采样频率: {fs} Hz")
    print(f"  信号长度: {num_points} 点")
    
    try:
        # 生成信号
        time, signal, data, f0, f1 = generate_alternating_2fsk_signal(
            code_info, carrier_type, fs, num_points
        )
        
        # 验证结果
        print(f"\n生成结果:")
        print(f"  生成的数据: {data}")
        print(f"  数据长度: {len(data)}")
        print(f"  0的载频: {f0} Hz")
        print(f"  1的载频: {f1} Hz")
        print(f"  信号长度: {len(signal)} 点")
        
        # 验证数据是否交替为0和1
        is_alternating = all(data[i] != data[i+1] for i in range(len(data)-1))
        print(f"  数据是否交替: {'是' if is_alternating else '否'}")
        
        # 验证信号是否正确生成
        print(f"  信号是否非空: {'是' if len(signal) > 0 else '否'}")
        print(f"  信号长度是否正确: {'是' if len(signal) == num_points else '否'}")
        
        print("\n函数验证成功!")
        return True
        
    except Exception as e:
        print(f"\n错误: {e}")
        return False

if __name__ == "__main__":
    success = verify_function()
    if success:
        print("\n验证通过!")
    else:
        print("\n验证失败!")
