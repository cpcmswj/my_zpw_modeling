""" 输出csv文件用 """
import csv
import numpy as np

def output_csv(filename, data):
    """ 输出csv文件 """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def export_circuit_model_to_csv(filename, model_info, include_matrices=False):
    """
    将电路模型参数导出为CSV文件
    
    Args:
        filename (str): 输出文件名
        model_info (dict): 电路模型信息，由build_circuit_model方法返回
        include_matrices (bool): 是否包含矩阵数据，默认不包含
    """
    data = []
    
    # 写入基本信息
    data.append(["电路模型参数", "", "", "", "", "", ""])
    data.append(["="*50, "", "", "", "", "", ""])
    
    # 写入基本参数
    data.append(["基本参数", "", "", "", "", "", ""])
    data.append(["参数名", "值", "单位", "", "", "", ""])
    basic_params = model_info.get("basic_params", {})
    if basic_params:
        data.append(["频率", basic_params.get("frequency"), "Hz", "", "", "", ""])
        data.append(["角频率", basic_params.get("angular_frequency"), "rad/s", "", "", "", ""])
        data.append(["补偿电容", basic_params.get("capacitance"), "uF", "", "", "", ""])
        data.append(["补偿电容步长", basic_params.get("capacitance_step"), "m", "", "", "", ""])
        data.append(["变压器变比", basic_params.get("transformer_ratio"), "", "", "", "", ""])
    data.append(["", "", "", "", "", "", ""])
    
    # 写入组件参数
    data.append(["组件参数", "", "", "", "", "", ""])
    data.append(["参数名", "值", "单位", "", "", "", ""])
    component_params = model_info.get("component_params", {})
    if component_params:
        tuner_params = component_params.get("tuner_params", "")
        data.append(["调谐区参数", f"电阻: {tuner_params[0]}, 感抗: {tuner_params[1]}", "mΩ", "", "", "", ""])
        data.append(["变压器输入阻抗", component_params.get("transformer_input_impedance"), "Ω", "", "", "", ""])
        spt_params = component_params.get("spt_params", "")
        data.append(["SPT电缆参数", f"传输常数: {spt_params[0]}, 特性阻抗: {spt_params[1]}, 阻抗角: {spt_params[2]}", "", "", "", ""])
    data.append(["", "", "", "", "", "", ""])
    
    # 写入故障信息
    data.append(["故障信息", "", "", "", "", "", ""])
    data.append(["参数名", "值", "", "", "", "", ""])
    fault_info = model_info.get("fault_info", {})
    if fault_info:
        data.append(["故障类型", fault_info.get("error_type"), "", "", "", "", ""])
        data.append(["故障状态", fault_info.get("error_status"), "", "", "", "", ""])
        data.append(["故障位置", fault_info.get("error_position"), "", "", "", "", ""])
    data.append(["", "", "", "", "", "", ""])
    
    # 如果需要，写入矩阵信息
    if include_matrices:
        data.append(["传输矩阵信息", "", "", "", "", "", ""])
        data.append(["矩阵名称", "大小", "类型", "", "", "", ""])
        matrices = model_info.get("matrices", {})
        for matrix_name, matrix in matrices.items():
            if isinstance(matrix, np.ndarray):
                data.append([matrix_name, f"{matrix.shape[0]}x{matrix.shape[1]}", "ndarray", "", "", "", ""])
        data.append(["", "", "", "", "", "", ""])
    
    # 写入详细矩阵数据（如果需要）
    if include_matrices:
        matrices = model_info.get("matrices", {})
        for matrix_name, matrix in matrices.items():
            if isinstance(matrix, np.ndarray):
                data.append([f"{matrix_name} 详细数据", "", "", "", "", "", ""])
                data.append(["行号", "列1实部", "列1虚部", "列2实部", "列2虚部", "", ""])
                for i in range(matrix.shape[0]):
                    row_data = [f"{i+1}"]
                    for j in range(matrix.shape[1]):
                        element = matrix[i, j]
                        if isinstance(element, complex):
                            row_data.extend([element.real, element.imag])
                        else:
                            row_data.extend([element, 0.0])
                    # 补全列数
                    while len(row_data) < 7:
                        row_data.append("")
                    data.append(row_data)
                data.append(["", "", "", "", "", "", ""])
    
    # 写入数据
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    
    print(f"电路模型参数已成功导出到 {filename}")
