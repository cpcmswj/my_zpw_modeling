# SPT电缆工具模块
# 导入 jisuan_guidao 中与 SPT 电缆相关的方法
import numpy as np
from jisuan_guidao import (
    find_SPTcable_parameters,
    SPTcable_matrix,
    SPTcable_impedance,
    find_cable_simulation_length,
    calculate_cable_simulation_matrix
)


# 导出所有导入的函数
__all__ = [
    'find_SPTcable_parameters',
    'SPTcable_matrix',
    'SPTcable_impedance',
    'find_cable_simulation_length',
    'calculate_cable_simulation_matrix'
]

def another_spt_cable_function(frequency, cable_length,num_conductors):
    """另一个 SPT 电缆函数"""
    R=23.6*cable_length#每根导体23.5Ω/km
    C=27e-9#27nf电容
    # 电阻部分：num_conductors 根电阻为 R 的导体并联
    # 使用 R1*R2/(R1+R2) 公式计算两个电阻并联，然后递归计算多个电阻并联
    if num_conductors == 1:
        parallel_R = R
    else:
        # 先计算两个电阻并联的等效电阻
        R12 = R * R / (R + R)  # R/2
        # 再与剩余的电阻并联，使用公式 R1*R2/(R1+R2) 递归计算
        parallel_R = R12
        for _ in range(num_conductors - 2):
            parallel_R = parallel_R * R / (parallel_R + R)
    Z=parallel_R+1/(1j*frequency*2*np.pi*C)
    
    return Z



# 示例使用
if __name__ == "__main__":
    # 测试 SPT 电缆参数获取
    frequency = 1700  # Hz
    spt_params = find_SPTcable_parameters(frequency)
    print(f"SPT电缆参数 (频率: {frequency}Hz):")
    print(f"传输常数: {spt_params[0]} dB/km")
    print(f"特性阻抗: {spt_params[1]} Ω")
    print(f"阻抗角: {spt_params[2]} °")
    
    # 测试 SPT 电缆矩阵计算
    cable_length = 10  # 10km
    cable_matrix = SPTcable_matrix(frequency, cable_length)
    print(f"\nSPT电缆矩阵 (长度: {cable_length}km):")
    print(cable_matrix)
    
    # 测试 SPT 电缆阻抗计算
    Z_cable_o = 50  # 输出端阻抗
    # 注意：SPTcable_impedance 函数内部会将输入的长度除以 1000，假设输入的单位是米
    # 所以如果我们要输入千米，需要乘以 1000 来抵消这个转换
    cable_impedance = SPTcable_impedance(frequency, Z_cable_o, cable_length * 1000)
    print(f"\nSPT电缆阻抗 (长度: {cable_length}km):")
    print(cable_impedance)
    
    # 测试电缆模拟网络长度计算
    spt_cable_length = 12.5  # km
    simulation_length = find_cable_simulation_length(spt_cable_length)
    print(f"\n电缆模拟网络长度 (SPT电缆长度: {spt_cable_length}km):")
    print(f"{simulation_length}km")
    
    # 比较 another_spt_cable_function 和原有方式的计算结果
    print("\n=== 比较两种方法的计算结果 ===")
    
    # 测试参数
    test_frequency = 1700  # Hz
    test_cable_length = 10  # km
    
    # 使用原有 SPTcable_impedance 计算
    # 注意：SPTcable_impedance 函数内部会将输入的长度除以 1000，假设输入的单位是米
    # 所以如果我们要输入千米，需要乘以 1000 来抵消这个转换
    original_result = SPTcable_impedance(test_frequency, 50, test_cable_length * 1000)
    print(f"原有 SPTcable_impedance 结果:")
    print(f"阻抗: {original_result}")
    print(f"阻抗幅值: {np.abs(original_result)} Ω")
    print(f"阻抗角度: {np.angle(original_result, deg=True)} °")
    
    # 测试不同的导体数目
    conductor_counts = [4, 6, 8, 9, 12, 14, 19, 21, 24, 28, 30, 33, 37, 42, 44, 48, 52, 56, 61]
    print("\n=== 测试不同导体数目 ===")
    
    # 存储最小差异和对应的导体数目
    min_difference = float('inf')
    best_conductor_count = None
    best_result = None
    
    for num_conductors in conductor_counts:
        # 使用 another_spt_cable_function 计算
        another_result = another_spt_cable_function(test_frequency, test_cable_length, num_conductors)
        
        # 计算差异
        amplitude_diff = abs(np.abs(another_result) - np.abs(original_result))
        angle_diff = abs(np.angle(another_result, deg=True) - np.angle(original_result, deg=True))
        # 综合差异（使用欧几里得距离）
        total_diff = np.sqrt(amplitude_diff**2 + (angle_diff/10)**2)  # 角度差异缩放10倍
        
        print(f"\n导体数目: {num_conductors}")
        print(f"another_spt_cable_function: {np.abs(another_result):.2f} Ω, {np.angle(another_result, deg=True):.2f} °")
        print(f"差异: 幅值 {amplitude_diff:.2f} Ω, 角度 {angle_diff:.2f} °, 综合 {total_diff:.2f}")
        
        # 更新最小差异
        if total_diff < min_difference:
            min_difference = total_diff
            best_conductor_count = num_conductors
            best_result = another_result
    
    # 输出最佳结果
    print(f"\n=== 最佳结果 ===")
    print(f"最佳导体数目: {best_conductor_count}")
    print(f"最佳结果: {np.abs(best_result):.2f} Ω, {np.angle(best_result, deg=True):.2f} °")
    print(f"与原有方法的差异: 幅值 {abs(np.abs(best_result) - np.abs(original_result)):.2f} Ω, 角度 {abs(np.angle(best_result, deg=True) - np.angle(original_result, deg=True)):.2f} °")
    
    # 测试不同频率（使用最佳导体数目）
    frequencies = [1700, 2000, 2300, 2600]  # 常见的载频率
    print("\n=== 不同频率下的比较（使用最佳导体数目）===")
    for freq in frequencies:
        another_result_freq = another_spt_cable_function(freq, test_cable_length, best_conductor_count)
        # 注意：SPTcable_impedance 函数内部会将输入的长度除以 1000，假设输入的单位是米
        # 所以如果我们要输入千米，需要乘以 1000 来抵消这个转换
        original_result_freq = SPTcable_impedance(freq, 50, test_cable_length * 1000)
        
        print(f"\n频率: {freq} Hz")
        print(f"another_spt_cable_function: {np.abs(another_result_freq):.2f} Ω, {np.angle(another_result_freq, deg=True):.2f} °")
        print(f"原有方法: {np.abs(original_result_freq):.2f} Ω, {np.angle(original_result_freq, deg=True):.2f} °")
        print(f"差异: 幅值 {abs(np.abs(another_result_freq) - np.abs(original_result_freq)):.2f} Ω, 角度 {abs(np.angle(another_result_freq, deg=True) - np.angle(original_result_freq, deg=True)):.2f} °")
