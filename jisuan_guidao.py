import numpy as np

"""
函数表
======

1. 查表函数
----------
find_capacitance(frequency)          - 根据载频率查表获取补偿电容值
find_capacitance_step(frequency)     - 根据载频率查表获取补偿电容步长
find_transformer_ratio(frequency)     - 根据载频率查表获取变压器变比
find_tuner_parameters(frequency)      - 根据载频率查表获取调谐区参数（电阻和感抗）
find_transformer_input_impedance(frequency) - 根据载频率查表获取衰耗盘接收端变压器输入阻抗
find_SPTcable_parameters(frequency)   - 根据载频率查表获取单节SPT电缆的参数（传输常数、特性阻抗、阻抗角）
find_tuning_unit_parameters(f, unit) - 查表获取F1、F2调谐单元各元件参数的计算值
find_tuning_unit_impedance(angular_frequency, F) - 根据载频率和调谐单元类型查表获取调谐单元的等效阻抗
find_tuning_unit_impedance_matrix(angular_frequency, F) - 根据载频率和调谐单元类型查表获取调谐单元的等效传输矩阵
find_attenuation(r1, r2)             - 根据端子查表获取衰耗盘接收端变压器次级线圈匝数
find_track_circuit_length(ballast_resist, cable_length, frequency) - 根据道碴电阻、SPT电缆长度和载频率查表获取轨道电路传输长度
find_resist_V1V2(frequency)          - 根据载频率查表获取V1V2间电阻

2. 电流、阻抗、导纳计算
----------------------
calculate_current(voltage, resist, induct, capacit, angular_frequency=0) - 使用电压向量和电阻电容电感来计算电流向量
calculate_impedance(resist, induct, capacit, angular_frequency=0)        - 计算阻抗，返回模和复数形式
calculate_admittance(resist, induct, capacit, angular_frequency=0)       - 计算导纳，返回模和复数形式
calculate_series_impedance(*impedances)                                - 计算任意个阻抗的串联
calculate_parallel_impedance(*impedances)                              - 计算任意个阻抗的并联

3. 电缆相关计算
--------------
SPTcable_matrix(frequency, length)                   - 根据电缆参数和长度计算电缆矩阵
SPTcable_impedance(frequency, Z_cable_I, Z_cable_o, length) - 根据电缆参数和长度计算电缆特性阻抗
attenuation_matrix(r1, r2)                           - 根据衰耗盘次级线圈的端子计算衰耗盘四端口等效电路的传输矩阵

4. Variable类 - 变量结构体类，用于储存和计算各种电气参数
---------------------------------------------------
__init__(name, value, length_guidao, resist_per_meter, induct_per_meter, capacit_per_meter, conduct_per_meter, frequency) - 初始化变量
get_Z_complex(length)                               - 计算单位长度钢轨的复数阻抗
get_Y_complex(length)                               - 计算单位长度钢轨的复数导纳
get_gamma_complex(length)                           - 计算单位长度钢轨的复数传播常数
get_Z_c_complex(length)                             - 计算单位长度钢轨的特性阻抗
iron_rail(length)                                - 计算钢轨等效传输特性矩阵
capacitance_matrix(R_cb, L_cb, C_b)             - 计算轨间补偿电容传输矩阵
transformer_matrix_input()                       - 计算接收端匹配变压器四端口传输特性传输矩阵
transformer_impedance_input(Z_cable)             - 计算接收端匹配变压器输入端等效阻抗
transformer_matrix_output()                      - 计算发送端匹配变压器四端口传输特性传输矩阵
transformer_impedance_output(Z_gfs)              - 计算发送端匹配变压器输入端等效阻抗
module_cable_matrix(R, L, C)                     - 根据电缆参数计算单节电缆模拟网络等效
SVA_matrix(L_SVA, R_ca)                          - 空芯线圈四端口网络传输矩阵
tuning_unit_matrix(F)                            - 调谐单元四端口网络传输矩阵

5. VoltageCurrent类 - 电压电流向量类，分为虚部和实部
--------------------------------------------------
__init__(voltage_real, voltage_imag, current_real, current_imag) - 初始化电压电流向量
get_voltage_complex() - 返回电压的复数形式
get_current_complex() - 返回电流的复数形式
get_matrix() - 返回电压电流的矩阵形式
get_matrix_transpose() - 返回电压电流矩阵的转置形式
get_sinx() - 返回电压电流的正弦值
from_amplitude_frequency(voltage_amplitude, voltage_phase, current_amplitude, current_phase) - 从幅值和相位构建电压电流向量

6. tuning_zone_parameters类 - 调谐区参数类
--------------------------------------------------
__init__(Variable, L_BA) - 初始化调谐区参数，计算相关阻抗值
tuning_zone_matrix() - 计算调谐区四端口网络传输矩阵
tuning_zone_matrix_f1() - 计算F1调谐单元断路时的调谐区传输矩阵
tuning_zone_matrix_f2(SPT_length) - 计算F2调谐单元断路时的调谐区传输矩阵
tuning_zone_matrix_SVA_1() - 计算空芯线圈断路时的调谐区传输矩阵
tuning_zone_matrix_SVA_2() - 计算空芯线圈短路时的调谐区传输矩阵
iron_rail_with_capacitance(n, l_nc, R_cb, L_cb, C_cb) - 计算轨道电路等效传输特性矩阵（包含补偿电容）
UI_counter(V_in, F) - 计算调谐区输入输出电压电流关系

全局变量
--------
frequency_parameters_table    - 综合参数表，包含载频率对应的补偿电容、变压器变比、调谐区电阻和感抗、衰耗盘接收端变压器输入阻抗、SPT电缆传输常数、SPT电缆特性阻抗、SPT电缆阻抗角
                                格式：[序号, 频率(Hz), 补偿电容(uF), 变压器变比n（不是1：n), 调谐区电阻(mΩ), 调谐区感抗(mΩ), 衰耗盘接收端变压器输入阻抗(Ω), SPT电缆传输常数(dB/km), SPT电缆特性阻抗(Ω), SPT电缆阻抗角(°)]
track_circuit_length_table    - 轨道电路传输长度参数表，包含道碴电阻、SPT电缆长度、载频率对应的轨道电路传输长度
                                格式：[序号, 道碴电阻(Ω·km), SPT电缆长度(km), 频率(Hz), 轨道电路传输长度(km)]
"""

# 综合参数表，包含载频率对应的补偿电容、变压器变比、调谐区电阻和感抗
# 格式：[序号, 频率(Hz), 补偿电容(uF), 变压器变比n（不是1：n), 调谐区(BA/SVA引接线)电阻(mΩ), 调谐区感抗(mΩ),衰耗盘接收端变压器输入阻抗(Ω),SPT电缆传输常数(dB/km),SPT电缆特性阻抗（Ω）,SPT电缆阻抗角（°）,钢轨阻抗（Ω/km），钢轨阻抗角(°)]
frequency_parameters_table = [
    [1, 1700, 55, 12, 8.3, 31.4, 36, 0.63, 396, -39,14.08,85.2],
    [2, 2000, 50, 10, 10.1, 35.2, 43.2, 0.68, 367, -38,16.44,85.44],
    [3, 2300, 46, 10, 11.9, 39, 48.6, 0.72, 343, -37,18.708,85.62],
    [4, 2600, 40, 9, 13.6, 42.6, 55, 0.75, 325, -36,21.147,85.78]
]
#SPT电缆的参数有区间，上表中取中间值

# 轨道电路传输长度参数表 (3*3*4表格)
# 维度1: 道碴电阻(Ω·km) - [1, 1.2, 1.5]
# 维度2: SPT电缆长度(km) - [10, 12.5, 15]
# 维度3: 频率(Hz) - [1700, 2000, 2300, 2600]
# 格式：track_circuit_length_table[道碴电阻索引][电缆长度索引][频率索引] = 轨道电路传输长度(km)
# 道碴电阻索引: 0=1Ω·km, 1=1.2Ω·km, 2=1.5Ω·km
# 电缆长度索引: 0=10km, 1=12.5km, 2=15km
# 频率索引: 0=1700Hz, 1=2000Hz, 2=2300Hz, 3=2600Hz
track_circuit_length_table = [
    # 道碴电阻=1.0Ω·km
    [
        # 电缆长度=10km
        [1.5, 1.5, 1.5, 1.46],
        # 电缆长度=12.5km
        [1.5, 1.4, 1.4, 1.3],
        # 电缆长度=15km
        [1.4, 1.4, 1.3, 1.3]
    ],
    # 道碴电阻=1.2Ω·km
    [
        # 电缆长度=10km
        [1.75, 1.7, 1.65, 1.6],
        # 电缆长度=12.5km
        [1.6, 1.6, 1.6, 1.5],
        # 电缆长度=15km
        [1.5, 1.5, 1.4, 1.4]
    ],
    # 道碴电阻=1.5Ω·km
    [
        # 电缆长度=10km
        [1.9, 1.9, 1.8, 1.8],
        # 电缆长度=12.5km
        [1.8, 1.8, 1.8, 1.7],
        # 电缆长度=15km
        [1.7, 1.6, 1.6, 1.5]
    ]
]

def find_capacitance_step(frequency):
    """根据载频率查表获取补偿电容步长值,此处取理论值，单位为米，之后可能改为其他查表"""
    if frequency == 1700 or frequency == 2000:
        #理论间距为60米
        return 60
    elif frequency == 2300 or frequency == 2600:
        #理论间距为80米
        return 80
    else:
        print("未找到该补偿电容步长参数/频率错误")
        return 0

def find_capacitance(frequency):
    """根据载频率查表获取补偿电容值"""
    for item in frequency_parameters_table:
        if item[1] == frequency:
            return item[2]
    return 0

def find_transformer_ratio(frequency):
    """根据载频率查表获取变压器变比"""
    for item in frequency_parameters_table:
        if item[1] == frequency:
            return item[3]
    return 0

def find_tuner_parameters(frequency):
    """根据载频率查表获取调谐区参数（电阻和感抗）"""
    for item in frequency_parameters_table:
        if item[1] == frequency:
            return item[4], item[5]
    return 0, 0

def find_transformer_input_impedance(frequency):
    """根据载频率查表获取衰耗盘接收端变压器输入阻抗"""
    for item in frequency_parameters_table:
        if item[1] == frequency:
            return item[6]
    return 0

def find_SPTcable_parameters(frequency, randomize=False, variation=0.1):
    """根据载频率获取单节SPT电缆的参数(传输常数gamma_cable和特性阻抗Z_d和阻抗角phi)
    
    参数：
        frequency: int, 载频率(Hz)
        randomize: bool, 是否使用随机生成的值，默认为False
        variation: float, 随机变化范围，默认为10%
    
    返回：
        tuple: (传输常数gamma_cable, 特性阻抗Z_d, 阻抗角phi)
    """
    if randomize:
        # 使用随机生成的参数
        try:
            from random_parameters import generate_random_SPT_cable_params
            return generate_random_SPT_cable_params(frequency, variation)
        except ImportError:
            print("无法导入random_parameters模块，使用原始查表值")
    
    # 使用原始查表值
    for item in frequency_parameters_table:
        if item[1] == frequency:
            return item[7], item[8], item[9]
    return 0, 0, 0

def find_tuning_unit_parameters(f, unit, randomize=False, variation=0.05):
    """获取F1、F2调谐单元各元件参数的计算值
    
    参数：
        f: int, 调谐单元类型，1表示F1，2表示F2
        unit: int, 元件编号，1-3表示不同元件
        randomize: bool, 是否使用随机生成的值，默认为False
        variation: float, 随机变化范围，默认为5%
    
    返回：
        float: 调谐单元元件参数值
    """
    if randomize:
        # 使用随机生成的参数
        try:
            from random_parameters import generate_random_tuning_unit_params
            return generate_random_tuning_unit_params(f, unit, variation)
        except ImportError:
            print("无法导入random_parameters模块，使用原始查表值")
    
    # 使用原始查表值
    if f == 1:  # F1
        if unit == 1:  # L1,单位uH
            return 37.145
        elif unit == 2:  # C1,单位uF
            return 128.91
    elif f == 2:  # F2
        if unit == 1:  # L2,单位uH
            return 97.387
        elif unit == 2:  # C2,单位uF
            return 90.0
        elif unit == 3:  # C3,单位uF
            return 236.604
    print("未找到该调谐单元参数")
    return 0

def find_tuning_unit_impedance(angular_frequency, F, randomize=False, variation=0.05):
    """根据载频率和调谐单元类型获取调谐单元的等效阻抗
    
    参数：
        angular_frequency: float, 角频率
        F: int, 调谐单元类型，1表示F1，2表示F2
        randomize: bool, 是否使用随机生成的值，默认为False
        variation: float, 随机变化范围，默认为5%
    
    返回：
        complex: 调谐单元的等效阻抗
    """
    if F == 1:
        Z = 1j * angular_frequency * find_tuning_unit_parameters(1, 1, randomize, variation) + \
            1 / (1j * angular_frequency * find_tuning_unit_parameters(1, 2, randomize, variation))
        return Z
    elif F == 2:
        Z1 = 1 / (1j * angular_frequency * find_tuning_unit_parameters(2, 3, randomize, variation))
        Z2 = 1j * angular_frequency * find_tuning_unit_parameters(2, 1, randomize, variation) + \
            1 / (1j * angular_frequency * find_tuning_unit_parameters(2, 2, randomize, variation))
        Z = Z1 * Z2 / (Z1 + Z2)
        return Z
    print("未找到该调谐单元参数")
    return 0

def find_tuning_unit_impedance_matrix(angular_frequency, F, randomize=False, variation=0.05):
    """根据载频率（角频率）和调谐单元类型获取调谐单元的等效传输矩阵
    输入输出关系: [V_out, I_out]^T = T * [V_in, I_in]^T
    其中T为调谐单元传输矩阵，[V_in, I_in]^T为输入端电压电流向量，[V_out, I_out]^T为输出端电压电流向量
    
    参数：
        angular_frequency: float, 角频率
        F: int, 调谐单元类型，1表示F1，2表示F2
        randomize: bool, 是否使用随机生成的值，默认为False
        variation: float, 随机变化范围，默认为5%
    
    返回：
        np.array: 调谐单元的等效传输矩阵
    """
    if F == 1:
        Z = 1j * angular_frequency * find_tuning_unit_parameters(1, 1, randomize, variation) + \
            1 / (1j * angular_frequency * find_tuning_unit_parameters(1, 2, randomize, variation))
        return np.array([[1, 0], [-1 / Z, 1]])
    elif F == 2:
        Z1 = 1 / (1j * angular_frequency * find_tuning_unit_parameters(2, 3, randomize, variation))
        Z2 = 1j * angular_frequency * find_tuning_unit_parameters(2, 1, randomize, variation) + \
            1 / (1j * angular_frequency * find_tuning_unit_parameters(2, 2, randomize, variation))
        Z = Z1 * Z2 / (Z1 + Z2)
        return np.array([[1, 0], [-1 / Z, 1]])
    
    print("未找到该调谐单元参数")
    return np.eye(2)

def find_attenuation(r1, r2):
    """根据端子查表获取衰耗盘接收端变压器次级线圈匝数"""
    if r1 == 1 and r2 == 2:
        return 1
    elif r1 == 3 and r2 == 4:
        return 2
    elif r1 == 4 and r2 == 5:
        return 4
    elif r1 == 3 and r2 == 5:
        return 6
    elif r1 == 6 and r2 == 7:
        return 14
    elif r1 == 8 and r2 == 9:
        return 42
    elif r1 == 9 and r2 == 10:
        return 84
    elif r1 == 8 and r2 == 10:
        return 126
    error_msg = f"未找到该衰耗盘参数/端子错误：r1={r1}, r2={r2}。请检查端子输入是否正确。"
    print(error_msg)
    return 0

def find_track_circuit_length(ballast_resist, cable_length, frequency):
    """根据道碴电阻、SPT电缆长度和载频率查表获取轨道电路传输长度"""
    # 定义参数到索引的映射
    ballast_resist_map = {1: 0, 1.2: 1, 1.5: 2}
    cable_length_map = {10: 0, 12.5: 1, 15: 2}
    frequency_map = {1700: 0, 2000: 1, 2300: 2, 2600: 3}
    
    # 检查参数是否在映射中
    if ballast_resist not in ballast_resist_map or cable_length not in cable_length_map or frequency not in frequency_map:
        return 0
    
    # 获取索引
    ballast_index = ballast_resist_map[ballast_resist]
    cable_index = cable_length_map[cable_length]
    frequency_index = frequency_map[frequency]
    
    # 从表格中获取轨道电路传输长度
    return track_circuit_length_table[ballast_index][cable_index][frequency_index]

def find_resist_V1V2(frequency):
    """V1V2端即接收端输入变压器的输入阻抗"""
    if frequency == 1700:
        return 36.0
    elif frequency == 2000:
        return 43.2
    elif frequency == 2300:
        return 48.6
    elif frequency == 2600:
        return 55.0
    else:
        print("未找到该接收端输入变压器参数/频率错误")
        return 0


def find_cable_simulation_length(spt_cable_length):
    """根据SPT电缆长度查表获取电缆模拟网络长度
    
    参数:
        spt_cable_length: float, SPT电缆长度(km)
    
    返回:
        float: 电缆模拟网络长度(km)
    """
    # 电缆模拟网络长度查表
    # 这里根据常见的SPT电缆长度与电缆模拟网络长度的对应关系创建表格
    # 实际应用中可能需要根据具体设备参数进行调整
    cable_simulation_table = {
        10: 0.1,    # 10km SPT电缆对应0.1km电缆模拟网络
        12.5: 0.125, # 12.5km SPT电缆对应0.125km电缆模拟网络
        15: 0.15,   # 15km SPT电缆对应0.15km电缆模拟网络
        17.5: 0.175, # 17.5km SPT电缆对应0.175km电缆模拟网络
        20: 0.2     # 20km SPT电缆对应0.2km电缆模拟网络
    }
    
    # 如果输入的SPT电缆长度在表格中，直接返回对应的值
    if spt_cable_length in cable_simulation_table:
        return cable_simulation_table[spt_cable_length]
    
    # 如果不在表格中，进行线性插值
    # 首先获取表格中的所有长度值并排序
    sorted_lengths = sorted(cable_simulation_table.keys())
    
    # 如果输入长度小于最小值，返回最小值对应的模拟网络长度
    if spt_cable_length <= sorted_lengths[0]:
        return cable_simulation_table[sorted_lengths[0]]
    
    # 如果输入长度大于最大值，返回最大值对应的模拟网络长度
    if spt_cable_length >= sorted_lengths[-1]:
        return cable_simulation_table[sorted_lengths[-1]]
    
    # 否则进行线性插值
    for i in range(len(sorted_lengths) - 1):
        if sorted_lengths[i] <= spt_cable_length <= sorted_lengths[i+1]:
            # 获取两个端点的值
            x1 = sorted_lengths[i]
            y1 = cable_simulation_table[x1]
            x2 = sorted_lengths[i+1]
            y2 = cable_simulation_table[x2]
            
            # 线性插值
            slope = (y2 - y1) / (x2 - x1)
            interpolated_value = y1 + slope * (spt_cable_length - x1)
            return interpolated_value
    
    # 兜底返回，应该不会执行到这里
    return 0.1


def calculate_cable_simulation_matrix(variable, spt_cable_length):
    """根据SPT电缆长度计算电缆模拟网络的传输矩阵
    
    参数:
        variable: Variable实例，包含频率等参数
        spt_cable_length: float, SPT电缆长度(km)
    
    返回:
        np.array: 电缆模拟网络的传输矩阵
    """
    # 查表获取电缆模拟网络长度
    simulation_length = find_cable_simulation_length(spt_cable_length)
    
    # ZPW2000中电缆模拟网络的一次参数 (参见论文内容)
    # R=23.5Ω/km, L=0.75mH/km, C=29nF/km
    R_per_km = 23.5  # Ω/km
    L_per_km = 0.75e-3  # H/km (0.75mH/km)
    C_per_km = 29e-9  # F/km (29nF/km)
    
    # 根据模拟网络长度计算实际参数
    R = R_per_km * simulation_length
    L = L_per_km * simulation_length
    C = C_per_km * simulation_length
    
    # 调用module_cable_matrix方法计算传输矩阵
    return variable.module_cable_matrix(R, L, C)


def get_rail_parameters(frequency):
    """根据频率查表获取钢轨阻抗和阻抗角，计算并返回钢轨每米电阻和电感
    
    参数:
        frequency: float, 频率(Hz)
    
    返回:
        tuple: (resist_per_meter, induct_per_meter) 钢轨每米电阻(Ω/m)和电感(H/m)
    """
    # 从频率参数表中构建钢轨参数字典
    rail_params_dict = {}
    for row in frequency_parameters_table:
        freq = row[1]
        impedance_per_km = row[10]  # 钢轨阻抗，单位为Ω/km
        impedance_per_meter = impedance_per_km / 1000  # 转换为Ω/m
        impedance_angle = row[11]  # 钢轨阻抗角，单位为度
        rail_params_dict[freq] = {"impedance": impedance_per_meter, "impedance_angle": impedance_angle}
    
    # 如果频率在表格中，直接使用对应的值
    if frequency in rail_params_dict:
        params = rail_params_dict[frequency]
        impedance = params["impedance"]
        impedance_angle = params["impedance_angle"]
    else:
        # 如果频率不在表格中，进行线性插值
        # 获取表格中的所有频率值并排序
        sorted_frequencies = sorted(rail_params_dict.keys())
        
        # 如果输入频率小于最小值，使用最小值的参数
        if frequency <= sorted_frequencies[0]:
            params = rail_params_dict[sorted_frequencies[0]]
            impedance = params["impedance"]
            impedance_angle = params["impedance_angle"]
        # 如果输入频率大于最大值，使用最大值的参数
        elif frequency >= sorted_frequencies[-1]:
            params = rail_params_dict[sorted_frequencies[-1]]
            impedance = params["impedance"]
            impedance_angle = params["impedance_angle"]
        # 否则进行线性插值
        else:
            for i in range(len(sorted_frequencies) - 1):
                if sorted_frequencies[i] <= frequency <= sorted_frequencies[i+1]:
                    # 获取两个端点的值
                    f1 = sorted_frequencies[i]
                    z1 = rail_params_dict[f1]["impedance"]
                    a1 = rail_params_dict[f1]["impedance_angle"]
                    f2 = sorted_frequencies[i+1]
                    z2 = rail_params_dict[f2]["impedance"]
                    a2 = rail_params_dict[f2]["impedance_angle"]
                    
                    # 线性插值
                    slope_z = (z2 - z1) / (f2 - f1)
                    slope_a = (a2 - a1) / (f2 - f1)
                    impedance = z1 + slope_z * (frequency - f1)
                    impedance_angle = a1 + slope_a * (frequency - f1)
                    break
            else:
                # 兜底返回，使用1700Hz的参数
                params = rail_params_dict[1700]
                impedance = params["impedance"]
                impedance_angle = params["impedance_angle"]
    
    # 将角度转换为弧度
    impedance_angle_rad = np.radians(impedance_angle)
    
    # 计算每米电阻和电感
    # 电阻 = 阻抗 * cos(阻抗角)
    # 电感 = 阻抗 * sin(阻抗角) / (2 * π * 频率)
    resist_per_meter = impedance * np.cos(impedance_angle_rad)
    induct_per_meter = impedance * np.sin(impedance_angle_rad) / (2 * np.pi * frequency)
    
    return resist_per_meter, induct_per_meter

def SPTcable_matrix(frequency, length):
    """根据电缆参数和长度计算电缆矩阵,gamma_cable为单位长度电缆的传输常数 Z_d为单位长度电缆的特性阻抗 length为电缆长度
    输入输出关系: [V_out, I_out]^T = T * [V_in, I_in]^T
    其中T为电缆传输矩阵，[V_in, I_in]^T为输入端电压电流向量，[V_out, I_out]^T为输出端电压电流向量"""
    # 计算电缆的复数阻抗
    gamma_cable = find_SPTcable_parameters(frequency)[0]
    Z_d = find_SPTcable_parameters(frequency)[1] * np.exp(1j * find_SPTcable_parameters(frequency)[2] * np.pi / 180)
    Q_cable = np.array([[np.cosh(gamma_cable * length), Z_d * np.sinh(gamma_cable * length)],
                      [np.sinh(gamma_cable * length) / Z_d, np.cosh(gamma_cable * length)]])
    return Q_cable

def SPTcable_impedance(frequency, Z_cable_I, Z_cable_o, length):
    """根据电缆参数和长度计算电缆特性阻抗,gamma_cable为单位长度电缆的传输常数 Z_d为单位长度电缆的特性阻抗 Z_cable_I为电缆输入端的等效阻抗 Z_cable_o为电缆输出端的等效阻抗 length为电缆长度"""
    if length == 0:
        print("电缆长度为0,需要修正")
        return 1
    gamma_cable = find_SPTcable_parameters(frequency)[0]
    Z_d = find_SPTcable_parameters(frequency)[1] * np.exp(1j * find_SPTcable_parameters(frequency)[2] * np.pi / 180)
    # 计算电缆的特性阻抗
    Z_cable = (Z_cable_I * np.cosh(gamma_cable * length) + Z_d * np.sinh(gamma_cable * length)) / (Z_cable_o / Z_d * np.sinh(gamma_cable * length) + np.cosh(gamma_cable * length))
    return Z_cable

def attenuation_matrix(r1, r2):
    """根据衰耗盘次级线圈的端子(和接收器门限电路输入端连接)计算衰耗盘四端口等效电路的传输矩阵
    输入输出关系: [V_out, I_out]^T = T * [V_in, I_in]^T
    其中T为衰耗盘传输矩阵，[V_in, I_in]^T为输入端电压电流向量，[V_out, I_out]^T为输出端电压电流向量"""
    N_rirj = find_attenuation(r1, r2)  # 获取衰耗盘次级线圈匝数
    if N_rirj == 0:
        # 当未找到匹配的端子组合时，返回单位矩阵，避免除以零错误
        print("警告：衰耗盘端子组合无效，使用单位矩阵代替")
        return np.array([[1, 0], [0, 1]])
    return np.array([[N_rirj / 116, 0], [0, 116 / N_rirj]])

def calculate_current(voltage, resist, induct, capacit, angular_frequency=0):
    """使用电压向量和电阻电容电感来计算电流向量"""
    
    voltage_complex = voltage[0] + 1j * voltage[1]
    
    # 计算复数阻抗 (R + jωL)
    impedance_complex = resist + 1j * (angular_frequency * induct)
    
    # 使用复数除法计算电流
    current_complex = voltage_complex / impedance_complex  # pyright: ignore[reportUnreachable]

    # 将复数电流转换回实部和虚部的向量形式
    current = np.array([current_complex.real, current_complex.imag])
    return current

def calculate_impedance(resist, induct, capacit, angular_frequency=0):
    """计算阻抗，返回模和复数形式"""
    impedance_complex = resist + 1j * (angular_frequency * induct)
    
    if angular_frequency == 0:
        impedance_mod = np.sqrt(resist ** 2 + (induct / capacit) ** 2)
    else:
        impedance_mod = np.abs(impedance_complex)
    
    return impedance_mod, impedance_complex

def calculate_admittance(resist, induct, capacit, angular_frequency=0):
    """计算导纳，返回模和复数形式"""
    conductance = 1 / resist if resist != 0 else 0
    admittance_complex = conductance + 1j * (angular_frequency * capacit)
    
    if angular_frequency == 0:
        admittance_mod = np.sqrt(capacit ** 2 + (induct / resist) ** 2) \
            if resist != 0 else float('inf')
    else:
        admittance_mod = np.abs(admittance_complex)
    
    return admittance_mod, admittance_complex

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

class Variable:
    """变量结构体类，用于储存和计算各种电气参数"""
    
    def __init__(self, name, value, length_guidao, resist_per_meter, induct_per_meter, capacit_per_meter, conduct_per_meter, frequency):
        self.name = name
        self.value = value
        self.length_guidao = length_guidao
        self.resist_per_meter = resist_per_meter  # 每米电阻
        self.induct_per_meter = induct_per_meter  # 每米电感
        # 以下两个参数是钢轨间漏泄导纳
        self.capacit_per_meter = capacit_per_meter  # 每米泄漏电容
        self.conduct_per_meter = conduct_per_meter  # 每米泄漏电导

        # 计算电阻（电阻 = 长度 * 电阻_per_meter）
        self.resist_guidao = length_guidao * resist_per_meter
        self.induct_guidao = length_guidao * induct_per_meter
        
        self.conduct_guidao = length_guidao * self.conduct_per_meter
        # 频率
        self.frequency = frequency
        self.angular_frequency = 2 * np.pi * self.frequency  # 角频率
        # 轨道总电容
        self.capacit_guidao = length_guidao * self.capacit_per_meter
        # Z为阻抗矩阵，Y为导纳矩阵，前为实部，后为虚部
        self.Z = np.array([self.resist_guidao, self.angular_frequency * self.induct_guidao])
        self.Y = np.array([self.conduct_guidao, self.angular_frequency * self.capacit_guidao])
        # 复数形式的阻抗和导纳
        self.Z_complex = self.get_Z_complex(self.length_guidao)
        self.Y_complex = self.get_Y_complex(self.length_guidao)
        
        # 计算阻抗和导纳的模和复数形式
        self.impedance_mod, self.impedance_complex = calculate_impedance(
            self.resist_guidao, self.induct_guidao, self.capacit_guidao, self.angular_frequency
        )
        self.admittance_mod, self.admittance_complex = calculate_admittance(
            self.resist_guidao, self.induct_guidao, self.capacit_guidao, self.angular_frequency
        )
        
        # 为了保持向后兼容性，保留原来的属性名
        self.impedance = self.impedance_mod
        self.admittance = self.admittance_mod
        
        self.gamma = np.array([
            self.resist_guidao * self.conduct_guidao - 
            (self.angular_frequency ** 2) * self.induct_guidao * self.conduct_guidao,
            self.angular_frequency * (
                self.resist_guidao * self.capacit_guidao + 
                self.conduct_guidao * self.induct_guidao
            )
        ])
        # gamma为传输系数矩阵，前为实部，后为虚部
        self.gamma_complex = self.get_gamma_complex(self.length_guidao)
        self.gamma_mod = np.abs(self.gamma_complex)
        # Z_c为特性阻抗/波阻抗
        self.Z_c = np.array([
            (self.resist_guidao * self.conduct_guidao + 
             (self.angular_frequency ** 2) * self.capacit_guidao * self.induct_guidao) / self.admittance,
            (self.conduct_guidao * self.induct_guidao - 
             self.resist_guidao * self.capacit_guidao) * self.angular_frequency / self.admittance
        ])
        # Z_c为特性阻抗/波阻抗，复数形式
        self.Z_c_complex = self.get_Z_c_complex(self.length_guidao)
    
    def get_Z_complex(self, length):
        """获取轨道阻抗"""
        return self.resist_per_meter * length + 1j * self.angular_frequency * self.induct_per_meter * length
    
    def get_Y_complex(self, length):
        """获取轨道间的漏泄导纳"""
        return self.conduct_per_meter * length + 1j * self.angular_frequency * self.capacit_per_meter * length
    
    def get_gamma_complex(self, length):
        """获取轨道传输系数"""
        return np.sqrt(self.get_Z_complex(length) * self.get_Y_complex(length))
    
    def get_Z_c_complex(self, length):
        """获取轨道特性阻抗"""
        return np.sqrt(self.get_Z_complex(length) / self.get_Y_complex(length))

    def iron_rail(self, length):
        """计算钢轨等效传输特性矩阵(此为输入端电压电流已知)
        输入输出关系: [V_out, I_out]^T = T * [V_in, I_in]^T
        其中T为钢轨传输矩阵，[V_in, I_in]^T为输入端电压电流向量，[V_out, I_out]^T为输出端电压电流向量"""
        self.iron_rail_matrix = np.array([
            [-np.cosh(self.gamma_complex * length), self.Z_c_complex * np.sinh(self.gamma_complex * length)],
            [np.sinh(self.gamma_complex * length) / self.Z_c_complex, -np.cosh(self.gamma_complex * length)]
        ])
        return self.iron_rail_matrix

    def capacitance_matrix(self, R_cb, L_cb, C_b):
        """计算轨间补偿电容传输矩阵 R_cb为电容连接线电阻 L_cb为电容连接线电感 C_b为补偿电容电容
        输入输出关系: [V_out, I_out]^T = T * [V_in, I_in]^T
        其中T为补偿电容传输矩阵，[V_in, I_in]^T为输入端电压电流向量，[V_out, I_out]^T为输出端电压电流向量"""
        if self.angular_frequency == 0:
            # 当角频率为0时，电容相当于开路，导纳为0
            matrix = np.array([
                [1, 0],
                [0, 1]
            ])
        elif C_b <= 0:
            # 当电容为0或负数时，视为短路，电容阻抗为连接线阻抗
            impedance_complex = R_cb + 1j * self.angular_frequency * L_cb
            matrix = np.array([
                [1, 0],
                [1 / impedance_complex, 1]
            ])
        else:
            # 角频率不为0且电容正常时，正常计算
            impedance_complex = R_cb + 1j * self.angular_frequency * L_cb + 1 / (1j * self.angular_frequency * C_b)
            matrix = np.array([
                [1, 0],
                [1 / impedance_complex, 1]
            ])
        return matrix

    def transformer_matrix_input(self):
        """计算接收端匹配变压器四端口传输特性传输矩阵 n为变压器变比 L_b为变压器补偿电感 C_b为变压器隔直电容
        输入输出关系: [V_out, I_out]^T = T * [V_in, I_in]^T
        其中T为变压器传输矩阵，[V_in, I_in]^T为输入端电压电流向量，[V_out, I_out]^T为输出端电压电流向量"""
        n = find_transformer_ratio(self.frequency)
        L_b = 0.1  # 变压器补偿电感10mH
        C_b = 2 * 0.0047  # 隔直电容有两个，每个4700uF
        self._transformer_matrix_input = np.array([
            [1 / n, 1j * (self.angular_frequency * L_b / n - 2 * n / (self.angular_frequency * C_b))],
            [0, n]
        ])
        return self._transformer_matrix_input
    
    def transformer_impedance_input(self, Z_cable):
        """计算接收端匹配变压器输入端等效阻抗 n为变压器变比 Z_cable为电缆端等效阻抗 L_b为变压器补偿电感 C_b为变压器隔直电容"""
        n = find_transformer_ratio(self.frequency)
        L_b = 0.1  # 变压器补偿电感10mH
        C_b = 2 * 0.0047  # 隔直电容有两个，每个4700uF
        self._transformer_impedance_input = (1 / n) * (Z_cable / n + 1j * (self.angular_frequency * L_b / n - 2 * n / (self.angular_frequency * C_b)))
        return self._transformer_impedance_input

    def transformer_matrix_output(self):
        """计算发送端匹配变压器四端口传输特性传输矩阵 n为变压器变比 L_b为变压器补偿电感 C_b为变压器隔直电容
        输入输出关系: [V_out, I_out]^T = T * [V_in, I_in]^T
        其中T为变压器传输矩阵，[V_in, I_in]^T为输入端电压电流向量，[V_out, I_out]^T为输出端电压电流向量"""
        n = find_transformer_ratio(self.frequency)
        L_b = 0.1  # 变压器补偿电感10mH
        C_b = 2 * 0.0047  # 隔直电容有两个，每个4700uF
        self._transformer_matrix_output = np.array([
            [n, 1j * (self.angular_frequency * L_b / n - 2 * n / (self.angular_frequency * C_b))],
            [0, 1 / n]
        ])
        return self._transformer_matrix_output
    
    def transformer_impedance_output(self, Z_gfs):
        """计算发送端匹配变压器输入端等效阻抗 n为变压器变比 Z_gfs为发送端钢轨等效阻抗 L_b为变压器补偿电感 C_b为变压器隔直电容"""
        n = find_transformer_ratio(self.frequency)
        L_b = 0.1  # 变压器补偿电感10mH
        C_b = 2 * 0.0047  # 隔直电容有两个，每个4700uF
        self._transformer_impedance_output = n * (Z_gfs * n + 1j * (self.angular_frequency * L_b / n - 2 * n / (self.angular_frequency * C_b)))
        return self._transformer_impedance_output
    
    def module_cable_matrix(self, R, L, C):
        """根据电缆参数计算单节电缆模拟网络等效  RLC均为模拟电缆网络的一次参数 多节即为多个单节矩阵相乘
        ZPW2000中R=23.5Ω/km,L=0.75mH/km,C=29nF/km(参见论文内容)
        输入输出关系: [V_out, I_out]^T = T * [V_in, I_in]^T
        其中T为电缆模拟网络传输矩阵，[V_in, I_in]^T为输入端电压电流向量，[V_out, I_out]^T为输出端电压电流向量"""
        # 计算电缆的复数阻抗
        Z1 = 1 / (1j * self.angular_frequency * C)
        Z2 = 2 * (1j * self.angular_frequency * L + R)
        Q_cable = np.array([[Z1 + Z2 / Z1, Z2],
                          [(2 * Z1 + Z2) / Z1 ** 2, Z1 + Z2 / Z1]])
        return Q_cable
    
    def SVA_matrix(self, L_SVA, R_ca):
        """空芯线圈四端口网络传输矩阵 L_SVA为SVA网络的电感参数 L_ca和R_ca为调谐区参数(查表)
        输入输出关系: [V_out, I_out]^T = T * [V_in, I_in]^T
        其中T为空芯线圈传输矩阵，[V_in, I_in]^T为输入端电压电流向量，[V_out, I_out]^T为输出端电压电流向量"""
        R_ca, wL_ca = find_tuner_parameters(self.frequency)
        Q_SVA = np.array([[1, 0],
                        [1 / (1j * self.angular_frequency * L_SVA + 1j * wL_ca + R_ca), 1]])
        return Q_SVA
    
    def tuning_unit_matrix(self, F):
        """调谐单元四端口网络传输矩阵 
        输入输出关系: [V_out, I_out]^T = T * [V_in, I_in]^T
        其中T为调谐单元传输矩阵，[V_in, I_in]^T为输入端电压电流向量，[V_out, I_out]^T为输出端电压电流向量"""
        # Z_z0为调谐单元的零阻抗
        Z_R5 = 1  # 之后再来补充
        Z_z0 = find_tuning_unit_impedance(self.angular_frequency, F)
        Z_3 = self.get_Z_complex(self.length_guidao / 2)
        Z_jif = (Z_ca + Z_z0 + Z_3) * (Z_ca + Z_SVA) / (Z_ca + Z_z0 + Z_3 + Z_ca + Z_SVA) + Z_3
        Z_R6 = Z_jif * Z_R5 / (Z_jif + Z_R5)
        Z_ca = R_ca + 1j * self.angular_frequency * L_ca  # 钢包铜引接线的等效阻抗
        Q_tuning_unit = np.array([[(Z_R6 + Z_ca) / Z_R6, 0],
                                [1 / Z_R6, 0]])
        return Q_tuning_unit

class tuning_zone_parameters:
    """调谐区参数类,为了方便调用一些参数，有补偿电容的主轨道也在这里计算"""
    
    def __init__(self, Variable, L_BA,BA1_type,BA2_type):
        # 以本区段为F1频率信号为例，之后要查看论文做F2的版本
        """L_BA为长度（通常为29m） Nr1/Nr2分别为长度为L_BA/2的钢轨的四端口网络,gamma_d为单位长度电缆的传输常数(参见SPT电缆的查表)"""
        # 存储Variable实例
        self.variable = Variable
        # 获取SPT电缆参数
        spt_params = find_SPTcable_parameters(Variable.frequency)
        gamma_d = spt_params[0]  # 传输常数
        Z_d = spt_params[1] * np.exp(1j * spt_params[2] * np.pi / 180)  # 特性阻抗（复数形式）
        
        # 设置默认的L_SVA值（空芯线圈电感）
        self.L_SVA = 33.5e-6  # 33.5uH
        
        self.Z_g = Variable.get_Z_complex(L_BA / 2)
        self.angular_frequency = Variable.angular_frequency
        R_ca, wL_ca = find_tuner_parameters(Variable.frequency)
        self.Z_ca = R_ca + 1j * wL_ca  # 钢包铜引接线的等效阻抗
        """Z_BA1和Z_BA2是F1和F2调谐单元的等效阻抗"""
        self.Z_BA1 = find_tuning_unit_impedance(self.angular_frequency, BA1_type)
        self.Z_BA2 = find_tuning_unit_impedance(self.angular_frequency, BA2_type)
        self.Z_Nr2_out = self.Z_BA2 + self.Z_ca
        self.Z_Nr2_in = (self.Z_Nr2_out * np.cosh(gamma_d * L_BA / 2) + Z_d * np.sinh(gamma_d * L_BA / 2)) / (self.Z_Nr2_out / Z_d + np.cosh(gamma_d * L_BA / 2))

        self.Z_SVA_out = self.Z_Nr2_in
        self.Z_SVA_in = self.Z_SVA_out / (1 + self.Z_SVA_out / (1j * self.angular_frequency * self.L_SVA + 1j * wL_ca + R_ca))
        
        self.Z_Nr1_out = self.Z_SVA_in
        self.Z_Nr1_in = (self.Z_Nr1_out * np.cosh(gamma_d * L_BA / 2) + Z_d * np.sinh(gamma_d * L_BA / 2)) / (self.Z_Nr1_out / Z_d + np.cosh(gamma_d * L_BA / 2))
        self.Z_FBA = self.Z_Nr1_in
        self.Z_JBA = self.Z_Nr1_in
    
    def tuning_zone_matrix(self):
        """调谐区四端口网络传输矩阵
        输入输出关系: [V_out, I_out]^T = T * [V_in, I_in]^T
        其中T为调谐区传输矩阵，[V_in, I_in]^T为输入端电压电流向量，[V_out, I_out]^T为输出端电压电流向量"""
        self.tuning_zone_matrix = np.array([[self.Z_Nr1_out, self.Z_Nr1_in],
                                          [self.Z_Nr2_out, self.Z_Nr2_in]])
        return self.tuning_zone_matrix
    
    def tuning_zone_matrix_f1(self):
        """SVA断路时调谐区四端口网络传输矩阵"""
        self.tuning_zone_matrix_f1 = np.array([[self.Z_BA2 / (2 * self.Z_g + 2 * self.Z_ca), 0],
                                          [-(1 / self.Z_BA1 + 1 / (2 * self.Z_g + 2 * self.Z_ca)), 1]])
        return self.tuning_zone_matrix_f1
    
    def tuning_zone_matrix_f2(self, SPT_length):
        """F2断开时调谐区四端口网络传输矩阵"""
        Z_trans_js = self.variable.transformer_impedance_input(SPTcable_impedance(self.variable.frequency, 0, 0, SPT_length))  # 从接收端看进去的等效阻抗，即BA、SVA、BA
        self.tuning_zone_matrix_f2 = np.array([[Z_trans_js * self.Z_SVA_in / (self.Z_SVA_out * (self.Z_g + self.Z_SVA_in + self.Z_ca)), 0],
                                          [1 / self.Z_BA1 + 1 / (self.Z_g + self.Z_SVA_in + self.Z_ca), 0]])
        return self.tuning_zone_matrix_f2
    
    def tuning_zone_matrix_SVA_1(self):
        """SVA断路时调谐区四端口网络传输矩阵"""
        self.tuning_zone_matrix_SVA_1 = np.array([[self.Z_BA2 / (2 * self.Z_g + 2 * self.Z_ca), 0],
                                          [-(1 / self.Z_BA1 + 1 / (2 * self.Z_g + 2 * self.Z_ca)), 1]])
        return self.tuning_zone_matrix_SVA_1
    
    def tuning_zone_matrix_SVA_2(self):
        """SVA短路时调谐区四端口网络传输矩阵"""
        self.tuning_zone_matrix_SVA_2 = np.array([[self.Z_ca * self.Z_BA2 / ((2 * self.Z_ca + self.Z_g) * (self.Z_BA2 + self.Z_ca + self.Z_g)), 0],
                                          [-(1 / self.Z_BA1 + 1 / (self.Z_g + 2 * self.Z_ca) + self.Z_ca / ((2 * self.Z_ca + self.Z_g) * (self.Z_BA2 + self.Z_ca + self.Z_g))), 1]])
        return self.tuning_zone_matrix_SVA_2

    def iron_rail_with_capacitance(self, n, l_nc, R_cb, L_cb, C_cb):
        """计算轨道电路等效传输特性矩阵 有n个补偿电容 包含钢轨在内 l_nc为补偿电容步长 R_cb为电容连接线电阻 L_cb为电容连接线电感 C_cb为补偿电容电容
        输入输出关系: [V_out, I_out]^T = T * [V_in, I_in]^T
        其中T为轨道电路传输矩阵，[V_in, I_in]^T为输入端电压电流向量，[V_out, I_out]^T为输出端电压电流向量"""
        # 确保n为整数，补偿电容数量必须是整数
        n = int(round(n))
        # 确保n至少为1，避免计算错误
        n = max(1, n)
        g_0 = n * self.variable.get_gamma_complex(self.variable.length_guidao)
        
        # 处理补偿电容为0的情况
        if C_cb <= 0:
            # 电容短路，视为电容阻抗为0
            Z_nc = R_cb + 1j * self.variable.angular_frequency * L_cb
        else:
            Z_nc = R_cb + 1j * self.variable.angular_frequency * L_cb + 1 / (1j * self.variable.angular_frequency * C_cb)  # 补偿电容阻抗
        
        theta = np.sqrt(self.variable.get_Z_complex(1) * self.variable.get_Y_complex(1)) * l_nc
        Z_cv = self.variable.get_Z_c_complex(1)
        
        # 处理Z_nc为0的情况
        if Z_nc == 0:
            b_0 = Z_cv * np.sinh(2 * theta)
            c_0 = np.sinh(2 * theta) / Z_cv
        else:
            b_0 = Z_cv * np.sinh(2 * theta) + (Z_cv ** 2) * (np.sinh(2 * theta) ** 2) / Z_nc
            c_0 = np.sinh(2 * theta) / Z_cv + (np.cosh(2 * theta) ** 2) / Z_nc
        
        # 处理c_0为0的情况
        if c_0 == 0:
            Z_co = Z_cv
        else:
            Z_co = np.sqrt(b_0 / c_0)
        
        Z_js = self.Z_SVA_in * self.Z_BA1 / (self.Z_SVA_in + self.Z_BA1)
        Z_js = Z_js * self.Z_BA2 / (self.Z_BA2 + Z_js)  # 从接收端看进去的等效阻抗，即BA、SVA、BA
        
        # 处理Z_js为0的情况
        if Z_js == 0:
            self.iron_rail_matrix = np.array([
                [np.cosh(g_0), 0],
                [np.sinh(g_0) / Z_co, 0]
            ])
        else:
            self.iron_rail_matrix = np.array([
                [np.cosh(g_0) + Z_co * np.sinh(g_0) / Z_js, 0],
                [np.sinh(g_0) / Z_co + np.cosh(g_0) / Z_js, 0]
            ])
        return self.iron_rail_matrix
    
    def UI_counter(self, V_in, F):
        """计算调谐区输入输出电压电流关系 F为错误代码 0为正常 1为BA1断开 2为BA2断开"""
        # 输入电压被分压为两块，分属半截钢轨和线圈；属线圈的电压分压为半截钢轨、调谐单元和接引线
        if F == 0:
            V_main = V_in * (1 - self.variable.get_Z_complex(self.variable.length_guidao / 2) / (self.variable.get_Z_complex(self.variable.length_guidao / 2) + 1 / self.variable.SVA_matrix(self.L_SVA, 0)[0, 1]))
            V_out = V_main * (self.Z_BA2 / (self.Z_BA2 + self.Z_ca))
            I_in = V_in / self.Z_BA1 + V_out / self.Z_BA2 + V_main / (1 / self.variable.SVA_matrix(self.L_SVA, 0)[0, 1])
            I_out = V_out / self.Z_BA2
        # 另外的情况需要重新绘制电路图进行分析
        else:
            return None
        # V_out=V_in*self.iron_rail_matrix[0,0]+I_in*self.iron_rail_matrix[0,1]
        # I_out=V_in*self.iron_rail_matrix[1,0]+I_in*self.iron_rail_matrix[1,1]
        # V_out_complex=V_in_complex*self.iron_rail_matrix[0,0]+I_in_complex*self.iron_rail_matrix[0,1]
        # I_out_complex=V_in_complex*self.iron_rail_matrix[1,0]+I_in_complex*self.iron_rail_matrix[1,1]
        return V_out, I_out, I_in

class VoltageCurrent:
    """电压电流向量类，分为虚部和实部"""
    
    def __init__(self, voltage_real, voltage_imag, current_real, current_imag):
        self.voltage_real = voltage_real
        self.voltage_imag = voltage_imag
        self.current_real = current_real
        self.current_imag = current_imag
        
        self.voltage = np.array([voltage_real, voltage_imag])
        self.current = np.array([current_real, current_imag])
        
        self.voltage_complex = voltage_real + 1j * voltage_imag
        self.current_complex = current_real + 1j * current_imag
    
    def get_voltage_complex(self):
        """返回电压的复数形式"""
        return self.voltage_complex
    
    def get_current_complex(self):
        """返回电流的复数形式"""
        return self.current_complex
    
    def get_matrix_transpose(self):
        """返回电压电流的矩阵形式（列向量）"""
        return np.array([[self.voltage_complex], [self.current_complex]])
    
    def get_matrix(self):
        """返回电压电流的矩阵形式"""
        return np.array([[self.voltage_complex, self.current_complex]])
    
    def get_sinx(self):
        """获取电压角和幅值"""
        self.voltage_frequency = np.arctan(self.voltage_imag / self.voltage_real)
        self.voltage_amplitude = np.sqrt(self.voltage_real ** 2 + self.voltage_imag ** 2)
        return self.voltage_frequency, self.voltage_amplitude
    
    @classmethod
    def from_amplitude_frequency(cls, voltage_amplitude, voltage_phase, current_amplitude, current_phase):
        """从幅值和相位构建电压电流向量
        
        Args:
            voltage_amplitude: 电压幅值
            voltage_phase: 电压相位（弧度）
            current_amplitude: 电流幅值
            current_phase: 电流相位（弧度）
        
        Returns:
            VoltageCurrent: 电压电流向量实例
        """
        # 计算电压的实部和虚部
        voltage_real = voltage_amplitude * np.cos(voltage_phase)
        voltage_imag = voltage_amplitude * np.sin(voltage_phase)
        
        # 计算电流的实部和虚部
        current_real = current_amplitude * np.cos(current_phase)
        current_imag = current_amplitude * np.sin(current_phase)
        
        # 返回新的 VoltageCurrent 实例
        return cls(voltage_real, voltage_imag, current_real, current_imag)
