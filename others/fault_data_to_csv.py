# 这个文件用于将error_of_trail中的故障类型示例输出数据整理为CSV表格
import csv
import os
import sys

# 添加父目录到系统路径，以便导入error_of_trail模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from templates.error_of_trail import Error_Of_Trail

def main():
    # 定义故障类型列表
    fault_types = [0, 1, 2, 3, 4, 5, 6, 7]
    
    # 定义故障位置列表
    #fault_positions = ["69G", "X1LQG", "IG1", "57G", "3DG"]
    fault_positions = ["69G"]
    # 定义其他参数
    error_value = 1.0
    length_parameter = 1200.0  # 轨道长度，单位：米（与示例保持一致）
    SPT_cable_length = 10.0  # SPT电缆长度，单位：米（与示例保持一致）
    input_voltages = [100.0, 110.0, 120.0, 130.0, 140.0, 150.0]  # 不同的输入电压值，单位：V
    
    # 准备CSV文件头
    csv_header = [
        "故障类型",
        "故障描述",
        "故障位置",
        "输入电压(V)",
        "发送端轨面电压(V)",
        "接收端轨面电压(V)",
        "主轨入电压(V)",
        "轨出1电压(V)",
        "发送端轨面电流(A)",
        "接收端轨面电流(A)",
        "主轨入电流(A)",
        "轨出1电流(A)",
        "频率(Hz)",
        "补偿电容(uF)",
        "变压器变比",
        "变压器输入阻抗(Ω)"
    ]
    
    # 创建CSV文件
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fault_data.csv")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)
        
        # 遍历每种故障类型、故障位置和输入电压
        for fault_type in fault_types:
            for fault_position in fault_positions:
                for input_V in input_voltages:
                    print(f"处理故障类型 {fault_type}，故障位置 {fault_position}，输入电压 {input_V}V...")
                    
                    try:
                        # 创建故障实例
                        fault = Error_Of_Trail(
                            trail="test",
                            error_type=fault_type,
                            error_value=error_value,
                            error_position=fault_position,
                            length_parameter=length_parameter,
                            SPT_cable_length=SPT_cable_length,
                            input_V=input_V
                        )
                        
                        # 构建电路模型并获取结果
                        circuit_model = fault.build_circuit_model()
                        
                        # 提取数据
                        if isinstance(circuit_model, dict):
                            voltage_results = circuit_model.get("voltage_results", {})
                            current_results = circuit_model.get("current_results", {})
                            basic_params = circuit_model.get("basic_params", {})
                            component_params = circuit_model.get("component_params", {})
                        else:
                            # 如果返回的不是字典，使用默认值
                            voltage_results = {}
                            current_results = {}
                            basic_params = {}
                            component_params = {}
                        
                        # 准备CSV行数据
                        csv_row = [
                            fault_type,
                            fault.status(),
                            fault_position,
                            input_V,
                            voltage_results.get("send_end_track_voltage", 0.0),
                            voltage_results.get("receive_end_track_voltage", 0.0),
                            voltage_results.get("main_track_input_voltage", 0.0),
                            voltage_results.get("main_track_output_voltage_1", 0.0),
                            current_results.get("send_end_track_current", 0.0),
                            current_results.get("receive_end_track_current", 0.0),
                            current_results.get("main_track_input_current", 0.0),
                            current_results.get("main_track_output_current_1", 0.0),
                            basic_params.get("frequency", 0.0),
                            basic_params.get("capacitance", 0.0),
                            basic_params.get("transformer_ratio", 0.0),
                            component_params.get("transformer_input_impedance", 0.0)
                        ]
                        
                        # 写入CSV文件
                        writer.writerow(csv_row)
                    
                    except Exception as e:
                        print(f"处理故障类型 {fault_type}，故障位置 {fault_position}，输入电压 {input_V}V 时出错: {e}")
                        # 写入错误行
                        error_row = [fault_type, f"错误: {str(e)}", fault_position, input_V] + [0.0] * (len(csv_header) - 4)
                        writer.writerow(error_row)
    
    print(f"数据已成功写入 {output_file}")

if __name__ == "__main__":
    main()
