#这个文件用来构建故障的框架
import numpy as np
import sys
import os

# 添加父目录到系统路径，以便导入jisuan_guidao模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import jisuan_guidao as jg
import circuit_tool

"""
函数表
======

1. Error_Of_Trail类 - 轨道电路故障建模类
----------------------------------
__init__(trail, error_type, error_value, error_position) - 初始化故障实例
character() - 返回故障特征描述
status() - 返回故障状态描述
call_matrix_small() - 计算小轨道传输矩阵
call_matrix_main() - 计算主轨道传输矩阵
call_matrix() - 根据故障类型选择合适的传输矩阵
call_input(input_V, ballast_resist_per_meter=1.0) - 计算输入电压对应的电流和等效阻抗
count_output() - 计算输出电压
build_circuit_model() - 构建整体电路模型
reinitialize_parameters() - 根据用户输入的参数重新初始化Variable和tuning_zone_parameters

2. 状态码说明
----------
0: 无故障
1: 接收端调谐单元1断路
2: 发送端调谐单元1断路
3: 接收端空心线圈断路
4: 接收端空芯线圈短路
5: 接收端调谐单元2断路
6: 补偿电容3断路
7: 补偿电容3短路

3. 轨道区段载频率对应表
-------------------
69G, X1LQG, IG1: 1700Hz
57G, 3DG: 2300Hz
其他: 0Hz (无效)
"""





class Error_Of_Trail:
    def __init__(self,trail,error_type,error_value,error_position,length_parameter,SPT_cable_length,r1=1,r2=1):
        self.trail=trail
        self.error_type=error_type
        self.error_value=error_value
        # 故障位置
        self.error_position=error_position
        # 设置默认长度参数
        self.length_parameter = length_parameter
        # SPT电缆长度
        self.SPT_cable_length = SPT_cable_length
        # 衰耗盘端子
        self.r1 = r1
        self.r2 = r2

        # 计算频率
        frequency = self.frequency_table(self.error_position)
        # 根据频率获取钢轨参数
        resist_per_meter, induct_per_meter = jg.get_rail_parameters(frequency)
        
        # 正确初始化Variable实例
        self.parameter=jg.Variable(
            name="track_circuit",
            value=error_value,
            length_guidao=self.length_parameter,
            resist_per_meter=resist_per_meter,
            induct_per_meter=induct_per_meter,
            capacit_per_meter=1.0e-9,
            conduct_per_meter=1.0e-6,
            frequency=frequency
        )
        self.tuning_parameters=jg.tuning_zone_parameters(
            Variable=self.parameter,
            L_BA=self.length_parameter,
            BA1_type=self.find_BA_type_tuning_zone()[0],
            BA2_type=self.find_BA_type_tuning_zone()[1]
        )
    def character(self):
        return f"故障类型：{self.error_type}，故障值：{self.error_value}，故障位置：{self.error_position}"
    def status(self):
        #如果输入格式错误，返回错误提示
        if self.error_type not in range(8):
            return "错误的故障类型输入"
        #根据故障类型返回状态描述
        if self.error_type==0:
            return "无故障"
        elif self.error_type==1:
            return "接收端调谐单元1断路"
        elif self.error_type==2:
            return "发送端调谐单元1断路"
        elif self.error_type==3:
            return "接收端空心线圈断路"
        elif self.error_type==4:
            return "接收端空芯线圈短路"
        elif self.error_type==5:
            return "接收端调谐单元2断路"
        elif self.error_type==6:
            return "补偿电容3断路"
        elif self.error_type==7:
            return "补偿电容3短路"
        else:
            return "未知故障类型"
    def find_neibour_zone(self):
        """查找故障位置的邻接区段 IG1 → 3DG → X1LQG → 57G → 69G"""
        zone=self.error_position
        if zone=="IG1":
            return "3DG"
        elif zone=="3DG":
            return "X1LQG"
        elif zone=="X1LQG":
            return "57G"
        elif zone=="57G":
            return "69G"
        else:
            return "未知故障位置"
    def frequency_table(self,zone=None):
        """根据区段名查询载频率(Hz)"""
        # 如果没有传入zone参数，则使用self.error_position
        if zone is None:
            zone = self.error_position
        if zone=="69G" or zone=="X1LQG" or zone=="IG1":
            return 1700
        elif zone=="57G" or zone=="3DG":
            return 2300
        else:
            return 0
    def find_BA_type(self,frequency):
        """根据载频率查询应该使用F1还是F2"""
        
        if frequency==1700 or frequency==2000:
            return 1
        elif frequency==2300 or frequency==2600:
            return 2
        else:
            print("未知载频率")
            return 0
    def find_BA_type_tuning_zone(self):
        """根据故障位置分别查询小轨道的两端调谐单元对应F1还是F2"""
        BA1=self.find_BA_type(self.frequency_table(self.error_position))
        if self.error_position=="69G":
            BA2=2
        else:
            BA2=self.find_BA_type(self.frequency_table(self.find_neibour_zone()))
        return BA1,BA2


    def reinitialize_parameters(self, error_type=None, error_value=None, error_position=None,
                                length_parameter=None, SPT_cable_length=None, resist_per_meter=None, induct_per_meter=None,
                                capacit_per_meter=None, conduct_per_meter=None, r1=None, r2=None):
        """
        根据用户输入的参数重新初始化Variable和tuning_zone_parameters
        
        参数：
            error_type (int, optional): 故障类型
            error_value (float, optional): 故障值
            error_position (str, optional): 故障位置
            length_parameter (float, optional): 长度参数
            SPT_cable_length (float, optional): SPT电缆长度
            resist_per_meter (float, optional): 每米电阻
            induct_per_meter (float, optional): 每米电感
            capacit_per_meter (float, optional): 每米电容
            conduct_per_meter (float, optional): 每米电导
            r1 (int, optional): 衰耗盘端子1
            r2 (int, optional): 衰耗盘端子2
        """
        # 使用现有值作为默认值
        if error_type is not None:
            self.error_type = error_type
        if error_value is not None:
            self.error_value = error_value
        if error_position is not None:
            self.error_position = error_position
        if length_parameter is not None:
            self.length_parameter = length_parameter
        if SPT_cable_length is not None:
            self.SPT_cable_length = SPT_cable_length
        if r1 is not None:
            self.r1 = r1
        if r2 is not None:
            self.r2 = r2
        
        # 计算频率
        frequency = self.frequency_table(self.error_position)
        
        # 重新初始化Variable实例
        self.parameter = jg.Variable(
            name="track_circuit",
            value=self.error_value,
            length_guidao=self.length_parameter,
            resist_per_meter=resist_per_meter if resist_per_meter is not None else 0.1,
            induct_per_meter=induct_per_meter if induct_per_meter is not None else 1.0e-3,
            capacit_per_meter=capacit_per_meter if capacit_per_meter is not None else 1.0e-9,
            conduct_per_meter=conduct_per_meter if conduct_per_meter is not None else 1.0e-6,
            frequency=frequency
        )
        
        # 获取调谐单元类型
        BA_types = self.find_BA_type_tuning_zone()
        
        # 重新初始化tuning_zone_parameters实例
        self.tuning_parameters = jg.tuning_zone_parameters(
            Variable=self.parameter,
            L_BA=self.length_parameter,
            BA1_type=BA_types[0],
            BA2_type=BA_types[1]
        )
        
        print(f"重新初始化参数成功")
        print(f"故障类型: {self.error_type}, 故障值: {self.error_value}, 故障位置: {self.error_position}")
        print(f"长度参数: {self.length_parameter}m, 频率: {frequency}Hz")
        print(f"每米电阻: {self.parameter.resist_per_meter}Ω/m, 每米电感: {self.parameter.induct_per_meter}H/m")
        print(f"每米电容: {self.parameter.capacit_per_meter}F/m, 每米电导: {self.parameter.conduct_per_meter}S/m")
    def call_matrix_small(self):
        """根据故障类型选择需要调用的矩阵,接收端为小轨道"""
        self.matrix=np.array([[1, 0], [0, 1]])
        frequency = self.frequency_table(self.error_position)
        if self.error_type==0 or self.error_type==7 or self.error_type==6 or self.error_type==5:
            #SPT电缆————匹配变压器——调谐单元——空芯线圈——调谐单元——匹配变压器——SPT电缆——接收端
            #不经过补偿电容
            
            # SPT电缆矩阵
            
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.length_parameter)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.length_parameter))
            # 匹配变压器矩阵（使用transformer_matrix_input方法）
            transformer_ratio = jg.find_transformer_ratio(frequency)
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            
            # 调谐区矩阵
            self.matrix=np.dot(np.linalg.inv(self.tuning_parameters.tuning_zone_matrix()),self.matrix)

            # 匹配变压器矩阵
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            return self.matrix
        elif self.error_type==1:
            # SPT电缆矩阵
            self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            # 匹配变压器矩阵（使用transformer_matrix_input方法）
            transformer_ratio = jg.find_transformer_ratio(frequency)
            #调谐区矩阵
            self.matrix=np.dot(self.matrix,self.tuning_parameters.tuning_zone_matrix_f2(10))
             # 匹配变压器矩阵
            self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            # SPT电缆矩阵
            self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            return self.matrix
        elif self.error_type==2:
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            # 匹配变压器矩阵（使用transformer_matrix_input方法）
            transformer_ratio = jg.find_transformer_ratio(frequency)
            #调谐区矩阵
            self.matrix=np.dot(self.matrix,self.tuning_parameters.tuning_zone_matrix_f1())
             # 匹配变压器矩阵
            self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            return self.matrix
        elif self.error_type==3:
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            # 匹配变压器矩阵（使用transformer_matrix_input方法）
            transformer_ratio = jg.find_transformer_ratio(frequency)
            self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            #调谐区矩阵
            self.matrix=np.dot(self.matrix,self.tuning_parameters.tuning_zone_matrix_SVA_1())
             # 匹配变压器矩阵
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))

            return self.matrix
        elif self.error_type==4:
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            # 匹配变压器矩阵（使用transformer_matrix_input方法）
            transformer_ratio = jg.find_transformer_ratio(frequency)
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            #调谐区矩阵
            self.matrix=np.dot(self.matrix,self.tuning_parameters.tuning_zone_matrix_SVA_2())
             # 匹配变压器矩阵
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))

            return self.matrix
        
        
        else:
            return "未知故障类型"

    def call_matrix_main(self):
        """计算传输矩阵，信号流向主轨道,之后需要添加计算补偿电容个数的方式"""
        self.matrix=np.array([[1, 0], [0, 1]])
        input_VC_matrix=self.count_inputVC()
        # 计算等效输入阻抗和电流
        try:
            input_current, input_impedance, Z_rail, Z_tuner = self.call_input(10.0, 1.0)  # 使用默认输入电压10.0V和道床漏阻1.0
            # 确保返回值是有效的数值
            def safe_complex_to_float(value):
                try:
                    if isinstance(value, complex):
                        return float(np.abs(value))
                    elif isinstance(value, (int, float)):
                        return float(value)
                    else:
                        return 0.0
                except:
                    return 0.0
            
            input_current_value = safe_complex_to_float(input_current)
            input_impedance_value = safe_complex_to_float(input_impedance)
            Z_rail_value = safe_complex_to_float(Z_rail)
            Z_tuner_value = safe_complex_to_float(Z_tuner)
            
            # 保存复数形式的阻抗，用于电流分配计算
            self.Z_rail_complex = Z_rail
            self.Z_tuner_complex = Z_tuner
        except Exception as e:
            print(f"计算输入阻抗和电流时出错: {e}")
            input_current_value = 0.0
            input_impedance_value = 0.0
            Z_rail_value = 0.0
            Z_tuner_value = 0.0
            self.Z_rail_complex = 0.0
            self.Z_tuner_complex = 0.0

        if self.error_type==0 or self.error_type==3 or self.error_type==4 or self.error_type==1:
            #SPT电缆————匹配变压器——补偿电容……——钢轨……——匹配变压器——SPT电缆——接收端
            #不经过空芯线圈,不经过小轨道调谐区
            frequency = self.frequency_table(self.error_position)
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            # 匹配变压器矩阵（使用transformer_matrix_input方法）
            transformer_ratio = jg.find_transformer_ratio(frequency)
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            
            #送端轨面电压
            self.output_voltage_surface1=np.dot(self.matrix,input_VC_matrix)
            #self.output_voltage_surface1=self.count_output()
            #送端轨面电流需要分流，使用circuit_tool中的函数计算电流分配
            # 获取送端轨面电压（复数形式）
            voltage_complex = self.output_voltage_surface1[0]
            
            # 使用复数形式的阻抗计算电流分配，这样可以得到更准确的结果
            currents = circuit_tool.calculate_current_distribution(voltage_complex, self.Z_rail_complex, self.Z_tuner_complex)
            
            # 使用分配到主轨道的电流
            if len(currents) > 0:
                self.output_voltage_surface1[1] = currents[0]

            #钢轨等效，需要修正,第一个参数的计算需要后续统一单位,连接线的电阻和电容需要后续查找资料
            #self.matrix=np.dot(self.matrix,self.tuning_parameters.iron_rail_with_capacitance(self.length_parameter/jg.find_capacitance_step(frequency),jg.find_capacitance_step(frequency),0,0,jg.find_capacitance(frequency)))
            self.matrix=np.dot(self.matrix,self.parameter.whole_iron_rail_with_capacitance(self.length_parameter/jg.find_capacitance_step(frequency),jg.find_capacitance_step(frequency),0,0,jg.find_capacitance(frequency)))
            
            #受端轨面电压
            self.output_voltage_surface2=np.dot(self.parameter.whole_iron_rail_with_capacitance(self.length_parameter/jg.find_capacitance_step(frequency),jg.find_capacitance_step(frequency),0,0,jg.find_capacitance(frequency)),self.output_voltage_surface1)
            #self.output_voltage_surface2=self.count_output()

            # 匹配变压器矩阵
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            
            #匹配变压器&SPT电缆
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),np.linalg.inv(self.parameter.transformer_matrix_input()))
            #主轨入电压
            self.output_voltage_main=np.dot(self.matrix,self.output_voltage_surface2)
            #self.output_voltage_main=self.count_output()
        elif self.error_type==2:
            # SPT电缆————匹配变压器——调谐单元(断路）——钢轨及补偿电容——调谐单元——匹配变压器——SPT电缆——接收端
            frequency = self.frequency_table(self.error_position)
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            # 匹配变压器矩阵（使用transformer_matrix_input方法）
            transformer_ratio = jg.find_transformer_ratio(frequency)
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            #送端轨面电压
            self.output_voltage_surface1=self.count_output()
            #钢轨等效，需要修正,第一个参数的计算需要后续统一单位,连接线的电阻和电容需要后续查找资料
            self.matrix=np.dot(self.matrix,self.tuning_parameters.iron_rail_with_capacitance(self.length_parameter/jg.find_capacitance_step(frequency),jg.find_capacitance_step(frequency),0,0,jg.find_capacitance(frequency)))
            #受端轨面电压
            self.output_voltage_surface2=self.count_output()
            #调谐单元矩阵
            F=self.find_BA_type_tuning_zone()[1]#调谐单元类型，之后要改
            self.matrix=np.dot(self.matrix,jg.find_tuning_unit_impedance_matrix(2*np.pi*frequency,F))
             # 匹配变压器矩阵
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            #主轨入电压
            self.output_voltage_main=self.count_output()
        elif self.error_type==5:
            # SPT电缆————匹配变压器——调谐单元——钢轨及补偿电容——调谐单元（断路）——匹配变压器——SPT电缆——接收端
            frequency = self.frequency_table(self.error_position)
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            # 匹配变压器矩阵（使用transformer_matrix_input方法）
            transformer_ratio = jg.find_transformer_ratio(frequency)
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            #调谐单元矩阵
            F=self.find_BA_type(frequency)#调谐单元类型，之后要改
            self.matrix=np.dot(self.matrix,jg.find_tuning_unit_impedance_matrix(2*np.pi*frequency,F))
            #送端轨面电压
            self.output_voltage_surface1=self.count_output()
            #钢轨等效，需要修正,第一个参数的计算需要后续统一单位,连接线的电阻和电容需要后续查找资料
            self.matrix=np.dot(self.matrix,self.tuning_parameters.iron_rail_with_capacitance(self.length_parameter/jg.find_capacitance_step(frequency),jg.find_capacitance_step(frequency),0,0,jg.find_capacitance(frequency)))
            #受端轨面电压
            self.output_voltage_surface2=self.count_output()
             # 匹配变压器矩阵
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            #主轨入电压
            self.output_voltage_main=self.count_output()
        elif self.error_type==6:
            #补偿电容断路，视为没有补偿电容
            frequency = self.frequency_table(self.error_position)
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            # 匹配变压器矩阵（使用transformer_matrix_input方法）
            transformer_ratio = jg.find_transformer_ratio(frequency)
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            #调谐单元矩阵
            F=self.find_BA_type_tuning_zone()[0]#调谐单元类型，之后要改
            self.matrix=np.dot(self.matrix,jg.find_tuning_unit_impedance_matrix(2*np.pi*frequency,F))
            #送端轨面电压
            self.output_voltage_surface1=self.count_output()
            #钢轨矩阵
            self.matrix=np.dot(self.matrix,self.parameter.iron_rail(self.length_parameter))
            #受端轨面电压
            self.output_voltage_surface2=self.count_output()
            #调谐单元矩阵
            F=self.find_BA_type_tuning_zone()[1]#调谐单元类型，之后要改
            self.matrix=np.dot(self.matrix,jg.find_tuning_unit_impedance_matrix(2*np.pi*frequency,F))
            
             # 匹配变压器矩阵
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            #主轨入电压
            self.output_voltage_main=self.count_output()
        elif self.error_type==7:
            #补偿电容短路即视为电容为零
            frequency = self.frequency_table(self.error_position)
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            # 匹配变压器矩阵（使用transformer_matrix_input方法）
            transformer_ratio = jg.find_transformer_ratio(frequency)
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            #调谐单元矩阵
            F=self.find_BA_type_tuning_zone()[0]#调谐单元类型，之后要改
            self.matrix=np.dot(self.matrix,jg.find_tuning_unit_impedance_matrix(2*np.pi*frequency,F))
            #送端轨面电压
            self.output_voltage_surface1=self.count_output()
            #钢轨等效，需要修正,第一个参数的计算需要后续统一单位,连接线的电阻和电容需要后续查找资料
            self.matrix=np.dot(self.matrix,self.tuning_parameters.iron_rail_with_capacitance(self.length_parameter/jg.find_capacitance_step(frequency),jg.find_capacitance_step(frequency),0,0,0))
            #受端轨面电压
            self.output_voltage_surface2=self.count_output()
            #调谐单元矩阵
            F=self.find_BA_type_tuning_zone()[1]#调谐单元类型，之后要改
            self.matrix=np.dot(self.matrix,jg.find_tuning_unit_impedance_matrix(2*np.pi*frequency,F))
             # 匹配变压器矩阵
            self.matrix=np.dot(np.linalg.inv(self.parameter.transformer_matrix_input()),self.matrix)
            #self.matrix=np.dot(self.matrix,self.parameter.transformer_matrix_input())
            # SPT电缆矩阵
            self.matrix=np.dot(np.linalg.inv(jg.SPTcable_matrix(frequency, self.SPT_cable_length)),self.matrix)
            #self.matrix=np.dot(self.matrix,jg.SPTcable_matrix(frequency, self.SPT_cable_length))
            #主轨入电压
            self.output_voltage_main=self.count_output()
        
        # 轨出1电压，经过衰耗盘
        self.matrix=np.dot(self.matrix,jg.attenuation_matrix(self.r1,self.r2))
        self.output_voltage_main_1=self.count_output()
        # 确保所有电压属性都已设置
        if not hasattr(self, 'output_voltage_surface1'):
            self.output_voltage_surface1 = complex(0.0)
        if not hasattr(self, 'output_voltage_surface2'):
            self.output_voltage_surface2 = complex(0.0)
        if not hasattr(self, 'output_voltage_main'):
            self.output_voltage_main = complex(0.0)
        if not hasattr(self, 'output_voltage_main_1'):
            self.output_voltage_main_1 = complex(0.0)
        
        # 使用实例变量中的电压值作为结果（电压有效值：复数模的平方根）
        # 添加NaN检查，确保返回有效的数值
        def safe_voltage_calc(voltage):
            try:
                if voltage is None:
                    return 0.0
                abs_val = np.abs(voltage)
                if not np.isfinite(abs_val):
                    return 0.0
                sqrt_val = np.sqrt(abs_val)
                if not np.isfinite(sqrt_val):
                    return 0.0
                return float(sqrt_val)
            except:
                return 0.0
        
        voltage_results = {
            "send_end_track_voltage": safe_voltage_calc(self.output_voltage_surface1),
            "receive_end_track_voltage": safe_voltage_calc(self.output_voltage_surface2),
            "main_track_input_voltage": safe_voltage_calc(self.output_voltage_main),
            "main_track_output_voltage_1": safe_voltage_calc(self.output_voltage_main_1)
        }
        
        
        
        # 返回包含矩阵、电压结果、输入阻抗、电流、主轨道阻抗和调谐区阻抗的字典
        return {
            "matrix": self.matrix,
            "voltage_results": voltage_results,
            "input_impedance": input_impedance_value,
            "input_current": input_current_value,
            "Z_rail": Z_rail_value,
            "Z_tuner": Z_tuner_value
        }

    def call_input(self,input_V,ballast_resist_per_meter):
        """根据故障类型选择需要调用的等效输入阻抗 ballast_resist_per_meter为道床漏阻"""
        Z_input=0#之后要补充查表
        frequency = self.frequency_table(self.error_position)
        
        #从输入端出发，经过SPT电缆和匹配变压器，之后抵达钢轨后视为主轨道和小轨道两边的等效电阻并联？
        self.input_V=input_V
        if self.error_type==0:
            #SPT电缆————匹配变压器——调谐单元——空芯线圈——调谐单元——匹配变压器——SPT电缆——接收端
            
            # 计算钢轨阻抗（使用Variable类的impedance属性）
            Z_c=1j*1/(2*np.pi*frequency*jg.find_capacitance(frequency)*self.length_parameter/jg.find_capacitance_step(frequency))
            Z_rail = self.parameter.impedance_complex+Z_c
            Z_rail=jg.calculate_parallel_impedance(Z_rail,jg.SPTcable_impedance(frequency,Z_rail,1,self.SPT_cable_length))
            #调谐区阻抗
            Z_tuner=self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca+jg.calculate_parallel_impedance(self.tuning_parameters.Z_BA2, jg.find_resist_V1V2(frequency))
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner,self.tuning_parameters.Z_ca+1j*self.tuning_parameters.L_SVA*self.tuning_parameters.angular_frequency)+self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner,self.tuning_parameters.Z_BA1)
            


            #组合阻抗
            Z_input=Z_input+jg.calculate_parallel_impedance(Z_rail,Z_tuner)

            #输入端SPT电缆阻抗
            Z_input=jg.SPTcable_impedance(frequency,1,Z_input,self.SPT_cable_length)

            # 检查Z_input是否为异常值，如果是则改为400
            if np.isinf(Z_input) or np.isnan(Z_input) or abs(Z_input) > 1e6 or abs(Z_input) < 1e-6:
                Z_input = 400
            # 计算电流
            I=self.input_V/Z_input
            
            return I,Z_input,Z_rail,Z_tuner
        elif self.error_type==1:
            #调谐单元F2断路的情况
            
            #调谐区阻抗为
            Z_tuner=self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca+jg.find_resist_V1V2(frequency)
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner,self.tuning_parameters.Z_ca+1j*self.tuning_parameters.L_SVA*self.tuning_parameters.angular_frequency)
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner+self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca,self.tuning_parameters.Z_BA1)
            #主轨道阻抗为
            Z_c=1j*1/(2*np.pi*frequency*jg.find_capacitance(frequency)*self.length_parameter/jg.find_capacitance_step(frequency))
            Z_rail=self.parameter.impedance_complex+jg.calculate_parallel_impedance(Z_c,self.parameter.Y_complex,self.tuning_parameters.Z_ca+jg.SPTcable_impedance(frequency,jg.find_tuning_unit_impedance(self.tuning_parameters.angular_frequency,self.find_BA_type(frequency)),jg.find_resist_V1V2(frequency),self.SPT_cable_length))
            
            #发送端匹配变压器后的总阻抗为前两个阻抗并联
            Z_send=jg.calculate_parallel_impedance(Z_tuner,Z_rail)
            #发送端匹配变压器的输入阻抗中Z_gfs为Z_send
            Z_input=self.parameter.transformer_impedance_output(Z_send)
            Z_input=jg.SPTcable_impedance(frequency,0,Z_input,self.SPT_cable_length)#SPT电缆长度和输入阻抗后续需要修改
            # 检查Z_input是否为异常值，如果是则改为400
            if np.isinf(Z_input) or np.isnan(Z_input) or abs(Z_input) > 1e6 or abs(Z_input) < 1e-6:
                Z_input = 400
            #计算电流
            I=self.input_V/Z_input

            return I,Z_input,Z_rail,Z_tuner
        elif self.error_type==2:
            #调谐单元F1断路的情况
            #调谐区阻抗为
            
            Z_tuner=jg.calculate_parallel_impedance(self.tuning_parameters.Z_BA2,jg.find_resist_V1V2(frequency))
            Z_tuner=Z_tuner+self.tuning_parameters.Z_ca+self.tuning_parameters.Z_g
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner,self.tuning_parameters.Z_ca+1j*self.tuning_parameters.L_SVA*self.tuning_parameters.angular_frequency)+self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca
            
            #主轨道阻抗为
            Z_rail=self.parameter.impedance_complex+jg.calculate_parallel_impedance(self.parameter.Y_complex,self.tuning_parameters.Z_ca+jg.SPTcable_impedance(frequency,jg.find_tuning_unit_impedance(self.tuning_parameters.angular_frequency,self.find_BA_type(frequency)),jg.find_resist_V1V2(frequency),self.SPT_cable_length))
            #发送端匹配变压器后的总阻抗为前两个阻抗并联
            Z_send=jg.calculate_parallel_impedance(Z_tuner,Z_rail)
            #发送端匹配变压器的输入阻抗中Z_gfs为Z_send
            Z_input=self.parameter.transformer_impedance_output(Z_send)
            #输入端SPT电缆阻抗
            Z_input=jg.SPTcable_impedance(frequency,0,Z_input,self.SPT_cable_length)
            # 检查Z_input是否为异常值，如果是则改为400
            if np.isinf(Z_input) or np.isnan(Z_input) or abs(Z_input) > 1e6 or abs(Z_input) < 1e-6:
                Z_input = 400
            #计算电流
            I=self.input_V/Z_input

            return I,Z_input,Z_rail,Z_tuner
        elif self.error_type==3:
            #调谐区阻抗为
            
            Z_tuner=jg.calculate_series_impedance(self.tuning_parameters.Z_g,2*self.tuning_parameters.Z_ca,jg.calculate_parallel_impedance(self.tuning_parameters.Z_BA2, 100))
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner,self.tuning_parameters.Z_BA1)
           #主轨道阻抗为
            Z_rail=self.parameter.impedance_complex+jg.calculate_parallel_impedance(self.parameter.Y_complex,self.tuning_parameters.Z_ca+jg.SPTcable_impedance(frequency,jg.find_tuning_unit_impedance(self.tuning_parameters.angular_frequency,self.find_BA_type(frequency)),jg.find_resist_V1V2(frequency),self.SPT_cable_length))

            #发送端匹配变压器后的总阻抗为前两个阻抗并联
            Z_send=jg.calculate_parallel_impedance(Z_tuner,Z_rail)
            #发送端匹配变压器的输入阻抗中Z_gfs为Z_send
            Z_input=self.parameter.transformer_impedance_output(Z_send)
            Z_input=jg.SPTcable_impedance(frequency,1,Z_input,self.SPT_cable_length)#SPT电缆长度和输入阻抗后续需要修改
            # 检查Z_input是否为异常值，如果是则改为400
            if np.isinf(Z_input) or np.isnan(Z_input) or abs(Z_input) > 1e6 or abs(Z_input) < 1e-6:
                Z_input = 400
            # 计算电流
            I=self.input_V/Z_input

            return I,Z_input,Z_rail,Z_tuner

        elif self.error_type==4:
            
            Z_tuner=self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca+jg.calculate_parallel_impedance(self.tuning_parameters.Z_BA2, 100)
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner,self.tuning_parameters.Z_ca)+self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner,self.tuning_parameters.Z_BA1)
            #主轨道阻抗为
            Z_rail=self.parameter.impedance_complex+jg.calculate_parallel_impedance(self.parameter.Y_complex,self.tuning_parameters.Z_ca+jg.SPTcable_impedance(frequency,jg.find_tuning_unit_impedance(self.tuning_parameters.angular_frequency,self.find_BA_type(frequency)),jg.find_resist_V1V2(frequency),self.SPT_cable_length))

            #发送端匹配变压器后的总阻抗为前两个阻抗并联
            Z_send=jg.calculate_parallel_impedance(Z_tuner,Z_rail)
            #发送端匹配变压器的输入阻抗中Z_gfs为Z_send
            Z_input=self.parameter.transformer_impedance_output(Z_send)
            Z_input=jg.SPTcable_impedance(frequency,0,Z_input,self.SPT_cable_length)#SPT电缆长度和输入阻抗后续需要修改
            # 检查Z_input是否为异常值，如果是则改为400
            if np.isinf(Z_input) or np.isnan(Z_input) or abs(Z_input) > 1e6 or abs(Z_input) < 1e-6:
                Z_input = 400
            # 计算电流
            I=self.input_V/Z_input
            return I,Z_input,Z_rail,Z_tuner
        elif self.error_type==5:
            #接收端调谐单元2断路的情况（与error_type==1类似）
            
            #调谐区阻抗为
            Z_tuner=self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca+jg.find_resist_V1V2(frequency)
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner,self.tuning_parameters.Z_ca+1j*self.tuning_parameters.L_SVA*self.tuning_parameters.angular_frequency)
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner+self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca,self.tuning_parameters.Z_BA1)
            #主轨道阻抗为
            Z_rail=self.parameter.impedance_complex+jg.calculate_parallel_impedance(self.parameter.Y_complex,self.tuning_parameters.Z_ca+jg.SPTcable_impedance(frequency,jg.find_tuning_unit_impedance(self.tuning_parameters.angular_frequency,self.find_BA_type(frequency)),jg.find_resist_V1V2(frequency),self.SPT_cable_length))

            #发送端匹配变压器后的总阻抗为前两个阻抗并联
            Z_send=jg.calculate_parallel_impedance(Z_tuner,Z_rail)
            #发送端匹配变压器的输入阻抗中Z_gfs为Z_send
            Z_input=self.parameter.transformer_impedance_output(Z_send)
            Z_input=jg.SPTcable_impedance(frequency,0,Z_input,self.SPT_cable_length)#SPT电缆长度和输入阻抗后续需要修改
            # 检查Z_input是否为异常值，如果是则改为400
            if np.isinf(Z_input) or np.isnan(Z_input) or abs(Z_input) > 1e6 or abs(Z_input) < 1e-6:
                Z_input = 400
            #计算电流
            I=self.input_V/Z_input
            return I,Z_input,Z_rail,Z_tuner
        elif self.error_type==6:
            #补偿电容断路即无补偿电容
            
            Z_tuner=self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca+jg.calculate_parallel_impedance(self.tuning_parameters.Z_BA2, jg.find_resist_V1V2(frequency))
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner,self.tuning_parameters.Z_ca+1j*self.tuning_parameters.L_SVA*self.tuning_parameters.angular_frequency)+self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner,self.tuning_parameters.Z_BA1)
            
            #主轨道阻抗为
            Z_rail=self.parameter.impedance_complex+jg.calculate_parallel_impedance(self.parameter.Y_complex,self.tuning_parameters.Z_ca+jg.SPTcable_impedance(frequency,jg.find_tuning_unit_impedance(self.tuning_parameters.angular_frequency,self.find_BA_type(frequency)),jg.find_resist_V1V2(frequency),self.SPT_cable_length))


            #发送端匹配变压器后的总阻抗为前两个阻抗并联
            Z_send=jg.calculate_parallel_impedance(Z_tuner,Z_rail)
            #发送端匹配变压器的输入阻抗中Z_gfs为Z_send
            Z_input=self.parameter.transformer_impedance_output(Z_send)
            Z_input=jg.SPTcable_impedance(frequency,0,Z_input,self.SPT_cable_length)#SPT电缆长度和输入阻抗后续需要修改
            # 检查Z_input是否为异常值，如果是则改为400
            if np.isinf(Z_input) or np.isnan(Z_input) or abs(Z_input) > 1e6 or abs(Z_input) < 1e-6:
                Z_input = 400
            #计算电流
            I=self.input_V/Z_input
            return I,Z_input,Z_rail,Z_tuner
        elif self.error_type==7:
                
            Z_tuner=self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca+jg.calculate_parallel_impedance(self.tuning_parameters.Z_BA2, jg.find_resist_V1V2(frequency))
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner,self.tuning_parameters.Z_ca+1j*self.tuning_parameters.L_SVA*self.tuning_parameters.angular_frequency)+self.tuning_parameters.Z_g+self.tuning_parameters.Z_ca
            Z_tuner=jg.calculate_parallel_impedance(Z_tuner,self.tuning_parameters.Z_BA1)
           #主轨道阻抗为
            Z_rail=self.parameter.impedance_complex+jg.calculate_parallel_impedance(self.parameter.Y_complex,self.tuning_parameters.Z_ca+jg.SPTcable_impedance(frequency,jg.find_tuning_unit_impedance(self.tuning_parameters.angular_frequency,self.find_BA_type(frequency)),jg.find_resist_V1V2(frequency),self.SPT_cable_length))

            #发送端匹配变压器后的总阻抗为前两个阻抗并联
            Z_send=jg.calculate_parallel_impedance(Z_tuner,Z_rail)
            #发送端匹配变压器的输入阻抗中Z_gfs为Z_send
            Z_input=self.parameter.transformer_impedance_output(Z_send)
            Z_input=jg.SPTcable_impedance(frequency,0,Z_input,self.SPT_cable_length)#SPT电缆长度和输入阻抗后续需要修改
            # 检查Z_input是否为异常值，如果是则改为400
            if np.isinf(Z_input) or np.isnan(Z_input) or abs(Z_input) > 1e6 or abs(Z_input) < 1e-6:
                Z_input = 400
            #计算电流
            I=self.input_V/Z_input
            return I,Z_input,Z_rail,Z_tuner
        else:
            return 0, 0, 0, 0
    def call_matrix(self):
        """根据故障类型选择合适的传输矩阵"""
        if self.error_type in [0, 1, 2, 3, 4, 5, 6, 7]:
            result = self.call_matrix_main()
            # 如果返回的是字典，保存电压结果并返回矩阵
            if isinstance(result, dict):
                self.voltage_results = result.get('voltage_results', {})
                # 将矩阵保存到实例变量中，供count_output使用
                self.matrix = result['matrix']
                return result['matrix']
            else:
                # 兼容旧格式
                self.matrix = result
                return result
        else:
            return np.array([[1, 0], [0, 1]])
    
    def count_inputVC(self):
        """建立发送器输出端的电压电流矩阵 """
        if not hasattr(self, 'input_V'):
            self.input_V = 10.0  # 默认输入电压
        input_current = self.call_input(self.input_V, 1.0)[0]
        #后期需要修复道床漏阻
        # 确保input_current是复数类型
        if not isinstance(input_current, complex):
            input_current = complex(input_current)
        
        # 检查input_V是否为复数
        if isinstance(self.input_V, complex):
            # 如果是复数，使用其实部和虚部
            voltage_real = self.input_V.real
            voltage_imag = self.input_V.imag
        else:
            # 如果不是复数，使用其值作为实部，虚部为0
            voltage_real = self.input_V
            voltage_imag = 0.0
        
        # 使用VoltageCurrent类构建输入电压电流向量
        voltage_current = jg.VoltageCurrent(
            voltage_real=voltage_real,  # 输入电压实部
            voltage_imag=voltage_imag,  # 输入电压虚部
            current_real=input_current.real,  # 电流实部
            current_imag=input_current.imag   # 电流虚部
        )
        
        # 获取电压电流的矩阵形式（列向量）
        try:
            input_VC_matrix = voltage_current.get_matrix_transpose()
            return input_VC_matrix
        except Exception as e:
            import traceback
            traceback.print_exc()
            return None


    def count_output(self):
        """计算输出电压"""
        if not hasattr(self, 'input_V'):
            self.input_V = 10.0  # 默认输入电压
        input_current = self.call_input(self.input_V, 1.0)[0]
        
        # 确保input_current是复数类型
        if not isinstance(input_current, complex):
            input_current = complex(input_current)
        
        # 检查input_V是否为复数
        if isinstance(self.input_V, complex):
            # 如果是复数，使用其实部和虚部
            voltage_real = self.input_V.real
            voltage_imag = self.input_V.imag
        else:
            # 如果不是复数，使用其值作为实部，虚部为0
            voltage_real = self.input_V
            voltage_imag = 0.0
        
        # 使用VoltageCurrent类构建输入电压电流向量
        voltage_current = jg.VoltageCurrent(
            voltage_real=voltage_real,  # 输入电压实部
            voltage_imag=voltage_imag,  # 输入电压虚部
            current_real=input_current.real,  # 电流实部
            current_imag=input_current.imag   # 电流虚部
        )
        
        # 获取电压电流的矩阵形式（列向量）
        try:
            input_VC_matrix = voltage_current.get_matrix_transpose()
            transfer_matrix = self.matrix
            # 确保transfer_matrix是有效的矩阵
            if transfer_matrix is None or not isinstance(transfer_matrix, np.ndarray):
                return complex(0.0)
            # 执行矩阵乘法
            VC_output = np.dot(transfer_matrix, input_VC_matrix)
            result = VC_output[0][0]
            # 检查结果是否有效（非NaN和非无穷大）
            if not np.isfinite(result.real) or not np.isfinite(result.imag):
                return complex(0.0)
            return result
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"计算输出电压时出错: {e}")
            return complex(0.0)
    


    def build_circuit_model(self):
        """构建整体电路模型，调用jisuan_guidao中的函数"""
        try:
            # 1. 根据故障位置获取载频率
            frequency = self.frequency_table(self.error_position)
            if frequency == 0:
                return "无法确定载频率，无法构建电路模型"
            
            # 2. 计算角频率
            angular_frequency = 2 * np.pi * frequency
            
            # 3. 使用jisuan_guidao中的函数计算相关参数
            print(f"=== 构建电路模型 (载频率: {frequency}Hz) ===")
            
            # 3.1 获取补偿电容值
            capacitance = jg.find_capacitance(frequency)
            print(f"补偿电容: {capacitance}uF")
            
            # 3.2 获取变压器变比
            transformer_ratio = jg.find_transformer_ratio(frequency)
            print(f"变压器变比: {transformer_ratio}")
            
            # 3.3 获取调谐区参数
            tuner_params = jg.find_tuner_parameters(frequency)
            print(f"调谐区参数 (电阻, 感抗): {tuner_params} mΩ")
            
            # 3.4 获取衰耗盘接收端变压器输入阻抗
            transformer_input_impedance = jg.find_transformer_input_impedance(frequency)
            print(f"衰耗盘接收端变压器输入阻抗: {transformer_input_impedance}Ω")
            
            # 3.5 获取SPT电缆参数
            spt_params = jg.find_SPTcable_parameters(frequency)
            print(f"SPT电缆参数 (传输常数, 特性阻抗, 阻抗角): {spt_params}")
            
            # 3.6 获取补偿电容步长
            capacitance_step = jg.find_capacitance_step(frequency)
            print(f"补偿电容步长: {capacitance_step}m")
            
            # 4. 创建Variable实例
            variable = jg.Variable(
                name="track_circuit",
                value=1.0,
                length_guidao=self.length_parameter,
                resist_per_meter=0.1,
                induct_per_meter=1.0e-3,
                capacit_per_meter=1.0e-9,
                conduct_per_meter=1.0e-6,
                frequency=frequency
            )
            
            # 5. 计算钢轨等效传输特性矩阵
            iron_rail_matrix = variable.iron_rail(self.length_parameter/2)
            print(f"钢轨等效传输特性矩阵:\n{iron_rail_matrix}")
            
            # 6. 计算轨间补偿电容传输矩阵
            if capacitance > 0:
                capacitance_matrix = variable.capacitance_matrix(R_cb=0.1, L_cb=1.0e-6, C_b=capacitance*1e-6)
                print(f"轨间补偿电容传输矩阵:\n{capacitance_matrix}")
            else:
                print("未计算补偿电容传输矩阵：补偿电容值为0")
                capacitance_matrix = np.array([[1, 0], [0, 1]])
            
            # 7. 计算变压器传输矩阵
            transformer_matrix = variable.transformer_matrix_input()
            print(f"接收端匹配变压器传输矩阵:\n{transformer_matrix}")
            
            # 8. 计算SPT电缆矩阵
            spt_cable_matrix = jg.SPTcable_matrix(frequency, length=self.length_parameter)
            print(f"SPT电缆矩阵:\n{spt_cable_matrix}")
            
            # 9. 计算衰耗盘矩阵
            attenuation_mat = jg.attenuation_matrix(1, 2)
            print(f"衰耗盘矩阵:\n{attenuation_mat}")
            
            # 10. 计算调谐区参数
            BA_types = self.find_BA_type_tuning_zone()
            tuning_params = jg.tuning_zone_parameters(variable, self.length_parameter, BA_types[0], BA_types[1])
            tuning_zone_matrix = tuning_params.tuning_zone_matrix()
            print(f"调谐区传输矩阵:\n{tuning_zone_matrix}")
            
            # 11. 根据故障类型调整模型
            print(f"\n=== 故障类型: {self.status()} ===")
            
            # 根据不同故障类型调整模型参数
            if self.error_type == 0:
                print("无故障，使用正常模型")
                # 构建完整的传输矩阵链
                total_matrix = np.dot(tuning_zone_matrix, transformer_matrix)
                total_matrix = np.dot(total_matrix, spt_cable_matrix)
                total_matrix = np.dot(total_matrix, iron_rail_matrix)
                total_matrix = np.dot(total_matrix, capacitance_matrix)
                total_matrix = np.dot(total_matrix, iron_rail_matrix)
                total_matrix = np.dot(total_matrix, transformer_matrix)
                total_matrix = np.dot(total_matrix, spt_cable_matrix)
                total_matrix = np.dot(total_matrix, attenuation_mat)
            elif self.error_type == 1:
                print("接收端调谐单元1断路，修改调谐单元参数")
                # 使用F2调谐单元断路时的调谐区传输矩阵
                tuning_zone_matrix = tuning_params.tuning_zone_matrix_f2(self.length_parameter)
            elif self.error_type == 2:
                print("发送端调谐单元1断路，修改调谐单元参数")
                # 使用F1调谐单元断路时的调谐区传输矩阵
                tuning_zone_matrix = tuning_params.tuning_zone_matrix_f1()
            elif self.error_type == 3:
                print("接收端空心线圈断路，修改空芯线圈参数")
                # 使用空芯线圈断路时的调谐区传输矩阵
                tuning_zone_matrix = tuning_params.tuning_zone_matrix_SVA_1()
            elif self.error_type == 4:
                print("接收端空芯线圈短路，修改空芯线圈参数")
                # 使用空芯线圈短路时的调谐区传输矩阵
                tuning_zone_matrix = tuning_params.tuning_zone_matrix_SVA_2()
            elif self.error_type == 5:
                print("接收端调谐单元2断路，修改调谐单元参数")
                # 使用F2调谐单元断路时的调谐区传输矩阵
                tuning_zone_matrix = tuning_params.tuning_zone_matrix_f2(self.length_parameter)
            elif self.error_type == 6:
                print("补偿电容3断路，修改电容参数")
                # 补偿电容断路，使用无补偿电容的钢轨传输矩阵
                iron_rail_matrix_no_cap = variable.iron_rail(self.length_parameter)
                print(f"无补偿电容钢轨传输矩阵:\n{iron_rail_matrix_no_cap}")
            elif self.error_type == 7:
                print("补偿电容3短路，修改电容参数")
                # 补偿电容短路，使用短路电容的传输矩阵
                capacitance_short_matrix = variable.capacitance_matrix(R_cb=0.1, L_cb=1.0e-6, C_b=0)
                print(f"短路补偿电容传输矩阵:\n{capacitance_short_matrix}")
            
            # 12. 调用主轨道和小轨道传输矩阵计算方法
            print("\n=== 计算传输矩阵 ===")
            # 计算主轨道传输矩阵
            main_track_result = self.call_matrix_main()
            
            # 处理返回结果，提取矩阵和电压结果
            if isinstance(main_track_result, dict):
                main_track_matrix = main_track_result['matrix']
                voltage_results = main_track_result['voltage_results']
                
                # 输出主轨道传输矩阵
                print(f"主轨道传输矩阵:\n{main_track_matrix}")
                
                # 输出新的电压结果
                print("\n=== 电压计算结果 ===")
                print(f"送端轨面电压: {voltage_results['send_end_track_voltage']:.2f} V")
                print(f"受端轨面电压: {voltage_results['receive_end_track_voltage']:.2f} V")
                print(f"主轨入电压: {voltage_results['main_track_input_voltage']:.2f} V")
            else:
                # 兼容旧格式
                main_track_matrix = main_track_result
                voltage_results = {
                    "send_end_track_voltage": 0.0,
                    "receive_end_track_voltage": 0.0,
                    "main_track_input_voltage": 0.0
                }
                print(f"主轨道传输矩阵:\n{main_track_matrix}")
            
            # 计算小轨道传输矩阵
            small_track_matrix = self.call_matrix_small()
            print(f"小轨道传输矩阵:\n{small_track_matrix}")
            
            # 13. 构建完整的电路模型
            circuit_model = {
                "basic_params": {
                    "frequency": frequency,
                    "angular_frequency": angular_frequency,
                    "capacitance": capacitance,
                    "capacitance_step": capacitance_step,
                    "transformer_ratio": transformer_ratio
                },
                "component_params": {
                    "tuner_params": tuner_params,
                    "transformer_input_impedance": transformer_input_impedance,
                    "spt_params": spt_params
                },
                "matrices": {
                    "spt_cable_matrix": spt_cable_matrix,
                    "transformer_matrix": transformer_matrix,
                    "iron_rail_matrix": iron_rail_matrix,
                    "capacitance_matrix": capacitance_matrix,
                    "attenuation_matrix": attenuation_mat,
                    "tuning_zone_matrix": tuning_zone_matrix,
                    "main_track_matrix": main_track_matrix,
                    "small_track_matrix": small_track_matrix
                },
                "voltage_results": voltage_results,
                "fault_info": {
                    "error_type": self.error_type,
                    "error_status": self.status(),
                    "error_position": self.error_position
                },
                "variable": variable,
                "tuning_params": tuning_params
            }
            
            # 13. 返回构建好的模型信息
            return circuit_model
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"构建电路模型时出错: {e}")
            return {"error": str(e)}

#同轨道建模时发送——SPT电缆————匹配变压器——调谐单元——空芯线圈——调谐单元——匹配变压器——SPT电缆——接收端


# 示例用法
if __name__ == "__main__":
    # 创建一个无故障的实例 - 69G案例，轨道电路长度1200m
    error_instance = Error_Of_Trail(trail="test", error_type=0, error_value=0, error_position="69G", length_parameter=1200.0, SPT_cable_length=10.0)
    print(error_instance.character())
    print(error_instance.status())
    
    # 构建电路模型
    model_info = error_instance.build_circuit_model()
    print(f"\n模型信息: {model_info}")
    
    # 创建一个有故障的实例 - 69G案例，轨道电路长度1200m
    error_instance_fault = Error_Of_Trail(trail="test", error_type=1, error_value=1, error_position="69G", length_parameter=1200.0, SPT_cable_length=10.0)
    print(f"\n故障实例: {error_instance_fault.character()}")
    print(error_instance_fault.status())
    
    # 构建故障电路模型
    model_info_fault = error_instance_fault.build_circuit_model()
    print(f"\n故障模型信息: {model_info_fault}")
