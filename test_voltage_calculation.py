import sys
import os

# 添加父目录到系统路径，以便导入jisuan_guidao模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from templates.error_of_trail import Error_Of_Trail

# 测试电压计算
def test_voltage_calculation():
    print("开始测试电压计算...")
    
    try:
        # 创建Error_Of_Trail实例
        error_instance = Error_Of_Trail(
            trail="测试轨道",
            error_type=0,  # 无故障
            error_value=0,
            error_position="69G",
            length_parameter=300.0,  # 轨道长度300m
            SPT_cable_length=10.0,  # SPT电缆长度10km
            r1=1,
            r2=2
        )
        
        # 重新初始化参数
        error_instance.reinitialize_parameters(
            error_type=0,
            error_value=0,
            error_position="69G",
            length_parameter=300.0,
            SPT_cable_length=10.0,
            resist_per_meter=0.01408,  # 每米电阻
            induct_per_meter=1.3135543773053626e-06,  # 每米电感
            capacit_per_meter=1.0e-9,  # 每米电容
            conduct_per_meter=1.0e-6,  # 每米电导
            r1=1,
            r2=2
        )
        
        # 调用call_matrix_main方法获取计算结果
        result = error_instance.call_matrix_main()
        
        print("\n计算结果:")
        print(f"送端轨面电压: {result['voltage_results']['send_end_track_voltage']} V")
        print(f"受端轨面电压: {result['voltage_results']['receive_end_track_voltage']} V")
        print(f"主轨入电压: {result['voltage_results']['main_track_input_voltage']} V")
        print(f"轨出1电压: {result['voltage_results']['main_track_output_voltage_1']} V")
        print(f"输入阻抗: {result['input_impedance']} Ω")
        print(f"输入电流: {result['input_current']} A")
        print(f"主轨道阻抗: {result['Z_rail']} Ω")
        print(f"调谐区阻抗: {result['Z_tuner']} Ω")
        
        # 检查电压值是否不为0
        if (result['voltage_results']['send_end_track_voltage'] > 0 and
            result['voltage_results']['receive_end_track_voltage'] > 0 and
            result['voltage_results']['main_track_input_voltage'] > 0):
            print("\n✅ 测试成功：电压值计算正确，不为0")
        else:
            print("\n❌ 测试失败：电压值为0或计算错误")
            
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_voltage_calculation()
