from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import os

# 使用简单的密码哈希实现（避免bcrypt的72字节限制）
import hashlib
import secrets

class PasswordHasher:
    def hash(self, password):
        """对密码进行哈希处理"""
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return f"$pbkdf2$100000${salt}${hashed.hex()}"
    
    def verify(self, password, hashed):
        """验证密码"""
        try:
            # 检查是否是哈希密码
            if hashed.startswith('$pbkdf2$'):
                parts = hashed.split('$')
                if len(parts) == 5:
                    iterations = int(parts[2])
                    salt = parts[3]
                    stored_hash = parts[4]
                    
                    # 计算哈希
                    computed_hash = hashlib.pbkdf2_hmac(
                        'sha256',
                        password.encode('utf-8'),
                        salt.encode('utf-8'),
                        iterations
                    )
                    return computed_hash.hex() == stored_hash
            # 兼容旧的明文密码
            return password == hashed
        except:
            # 如果解析失败，尝试作为明文密码处理
            return password == hashed

# 创建密码哈希器实例
pwd_context = PasswordHasher()
print("[OK] 密码哈希器初始化成功")

# 导入jisuan_guidao.py中的函数和类
from jisuan_guidao import (
    Variable,
    VoltageCurrent,
    calculate_current,
    calculate_impedance,
    calculate_admittance
)

# 导入Error_Of_Trail类
from templates.error_of_trail import Error_Of_Trail

# 创建FastAPI应用实例
app = FastAPI()

# 配置模板和静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 获取端口配置
PORT = int(os.environ.get("PORT", 8000))

# 根路径，返回新的首页
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("time_series_generator.html", {"request": request})

# 图片查看器页面 - 使用模板引擎
@app.get("/image-viewer", response_class=HTMLResponse)
async def read_image_viewer(request: Request):
    return templates.TemplateResponse("image_viewer.html", {"request": request})

# 测试图片页面 - 使用模板引擎
@app.get("/test-image", response_class=HTMLResponse)
async def read_test_image(request: Request):
    return templates.TemplateResponse("test_image.html", {"request": request})

# 铁路区段图片查看器页面
@app.get("/section-image-viewer", response_class=HTMLResponse)
async def read_section_image_viewer(request: Request):
    return templates.TemplateResponse("section_image_viewer.html", {"request": request})

# 整合系统页面
@app.get("/integrated-system", response_class=HTMLResponse)
async def read_integrated_system(request: Request):
    return templates.TemplateResponse("integrated_system.html", {"request": request})

# 故障模拟比较系统页面
@app.get("/comparison-system", response_class=HTMLResponse)
async def read_comparison_system(request: Request):
    return templates.TemplateResponse("comparison_system.html", {"request": request})

# FSK信号查看器页面
@app.get("/fsk-signal-viewer", response_class=HTMLResponse)
async def read_fsk_signal_viewer(request: Request):
    return templates.TemplateResponse("fsk_signal_viewer.html", {"request": request})

# 交替发送0和1的2FSK信号查看器页面
@app.get("/alternating-2fsk-viewer", response_class=HTMLResponse)
async def read_alternating_2fsk_viewer(request: Request):
    return templates.TemplateResponse("alternating_2fsk_viewer.html", {"request": request})

# 批量故障模拟页面
@app.get("/batch-simulation", response_class=HTMLResponse)
async def read_batch_simulation(request: Request):
    return templates.TemplateResponse("batch_simulation.html", {"request": request})

# 开发者调试页面
@app.get("/developer-debug", response_class=HTMLResponse)
async def read_developer_debug(request: Request):
    return templates.TemplateResponse("developer_debug.html", {"request": request})

# 正弦波波形生成器页面
@app.get("/sine-wave-generator", response_class=HTMLResponse)
async def read_sine_wave_generator(request: Request):
    return templates.TemplateResponse("sine_wave_generator.html", {"request": request})

# 波形导入与显示页面
@app.get("/waveform-import", response_class=HTMLResponse)
async def read_waveform_import(request: Request):
    return templates.TemplateResponse("waveform_import.html", {"request": request})

# XY坐标图绘制页面
@app.get("/xy-plot", response_class=HTMLResponse)
async def read_xy_plot(request: Request):
    return templates.TemplateResponse("xy_plot.html", {"request": request})

# 时间序列故障模拟页面
@app.get("/time-series-simulation", response_class=HTMLResponse)
async def read_time_series_simulation(request: Request):
    return templates.TemplateResponse("time_series_simulation.html", {"request": request})

# 故障状态时间序列对比页面
@app.get("/comparison-time-series", response_class=HTMLResponse)
async def read_comparison_time_series(request: Request):
    return templates.TemplateResponse("comparison_time_series.html", {"request": request})

# 轨道参数设置页面
@app.get("/track-parameters", response_class=HTMLResponse)
async def read_track_parameters(request: Request):
    return templates.TemplateResponse("track_parameters.html", {"request": request})

# 时序数据生成页面
@app.get("/time-series-generator", response_class=HTMLResponse)
async def read_time_series_generator(request: Request):
    return templates.TemplateResponse("time_series_generator.html", {"request": request})

# 构建电路模型API端点
@app.post("/api/build-circuit-model")
async def build_circuit_model(
    trackSection: str = Form(...),
    faultType: int = Form(...),
    trackLength: float = Form(...),
    cableLength: float = Form(...),
    frequency: int = Form(...),
    inputVoltage: float = Form(...),
    ballastResist: float = Form(...)
):
    try:
        # 导入Error_Of_Trail_Amplitude_Phase类
        from templates.error_of_trail_amplitude_phase import Error_Of_Trail_Amplitude_Phase
        
        print(f"接收到构建电路模型请求:")
        print(f"轨道区段: {trackSection}")
        print(f"故障类型: {faultType}")
        print(f"轨道长度: {trackLength}")
        print(f"电缆长度: {cableLength}")
        print(f"频率: {frequency}")
        print(f"输入电压: {inputVoltage}")
        print(f"道碴电阻: {ballastResist}")
        
        # 创建故障实例
        fault = Error_Of_Trail_Amplitude_Phase(
            trail="track_circuit",
            error_type=faultType,
            error_value=1.0,
            error_position=trackSection,
            length_parameter=trackLength,
            SPT_cable_length=cableLength
        )
        
        # 构建电路模型
        print("开始构建电路模型...")
        result = fault.build_circuit_model()
        print("电路模型构建完成")
        
        # 计算输入电压对应的输出
        print("计算输入电压对应的输出...")
        fault.input_V = inputVoltage
        
        # 计算输出电压
        try:
            output_voltage = fault.count_output()
            print(f"输出电压: {output_voltage}")
        except Exception as e:
            print(f"计算输出电压时出错: {e}")
            output_voltage = None
        
        # 计算主轨入电压和轨出1电压
        try:
            # 调用 call_matrix_main 方法计算主轨入电压
            fault.call_matrix_main()
            
            # 获取主轨入电压
            if hasattr(fault, 'output_voltage_main'):
                try:
                    # 尝试获取 voltage_main 作为主轨入电压
                    if hasattr(fault, 'voltage_main'):
                        main_rail_input_voltage = fault.voltage_main
                        print(f"从 voltage_main 获取主轨入电压: {main_rail_input_voltage}")
                    else:
                        # 尝试从 output_voltage_main 获取主轨入电压
                        main_rail_input_voltage = fault.output_voltage_main
                        # 检查是否为数组或列表
                        if isinstance(main_rail_input_voltage, (list, np.ndarray)):
                            # 尝试获取第一个元素
                            if len(main_rail_input_voltage) > 0:
                                main_rail_input_voltage = main_rail_input_voltage[0]
                        # 检查是否为复数
                        if isinstance(main_rail_input_voltage, complex):
                            # 计算复数的模
                            main_rail_input_voltage = abs(main_rail_input_voltage)
                        print(f"主轨入电压: {main_rail_input_voltage}")
                except Exception as e:
                    print(f"获取主轨入电压时出错: {e}")
                    main_rail_input_voltage = None
            else:
                main_rail_input_voltage = None
                print("警告：未找到主轨入电压")
            
            # 获取轨出1电压（这里假设轨出1电压是主轨入电压的一部分）
            if main_rail_input_voltage is not None:
                # 轨出1电压通常是主轨入电压经过衰耗盘后的电压
                # 这里使用一个简化的计算方式，实际项目中需要根据具体电路计算
                rail_output_1_voltage = main_rail_input_voltage * 0.9 if isinstance(main_rail_input_voltage, (int, float, complex)) else None
                rail_output_2_voltage = main_rail_input_voltage * 0.1 if isinstance(main_rail_input_voltage, (int, float, complex)) else None
                print(f"轨出1电压: {rail_output_1_voltage}")
                print(f"轨出2电压: {rail_output_2_voltage}")
            else:
                rail_output_1_voltage = None
                rail_output_2_voltage = None
                print("警告：无法计算轨出1电压和轨出2电压")
        except Exception as e:
            print(f"计算主轨入电压和轨出1电压时出错: {e}")
            import traceback
            traceback.print_exc()
            main_rail_input_voltage = inputVoltage
            rail_output_1_voltage = None
            rail_output_2_voltage = None
        
        # 构建响应
        response_data = {
            "status": "success",
            "message": "电路模型构建成功",
            "data": {
                "trackSection": trackSection,
                "faultType": faultType,
                "trackLength": trackLength,
                "cableLength": cableLength,
                "frequency": frequency,
                "inputVoltage": inputVoltage,
                "ballastResist": ballastResist,
                "outputVoltage": str(output_voltage) if output_voltage is not None else "计算失败",
                "mainRailInputVoltage": str(main_rail_input_voltage) if main_rail_input_voltage is not None else "计算失败",
                "railOutput1Voltage": str(rail_output_1_voltage) if rail_output_1_voltage is not None else "计算失败",
                "railOutput2Voltage": str(rail_output_2_voltage) if rail_output_2_voltage is not None else "计算失败",
                "faultStatus": fault.status()
            }
        }
        
        return JSONResponse(response_data)
        
    except Exception as e:
        print(f"构建电路模型时出错: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"status": "error", "message": f"构建电路模型失败: {str(e)}"},
            status_code=500
        )

# 仿真模型API端点
@app.post("/api/simulate-model")
async def simulate_model(
    trackSection: str = Form(...),
    faultType: int = Form(...),
    trackLength: float = Form(...),
    cableLength: float = Form(...),
    frequency: int = Form(...),
    inputVoltage: float = Form(...),
    ballastResist: float = Form(...),
    voltageLevel: int = Form(3)
):
    try:
        # 导入Error_Of_Trail_Amplitude_Phase类
        from templates.error_of_trail_amplitude_phase import Error_Of_Trail_Amplitude_Phase
        
        print(f"接收到模型仿真请求:")
        print(f"轨道区段: {trackSection}")
        print(f"故障类型: {faultType}")
        print(f"轨道长度: {trackLength}")
        print(f"电缆长度: {cableLength}")
        print(f"频率: {frequency}")
        print(f"输入电压: {inputVoltage}")
        print(f"道碴电阻: {ballastResist}")
        print(f"电压档位: {voltageLevel}")
        
        # 创建故障实例
        fault = Error_Of_Trail_Amplitude_Phase(
            trail="track_circuit",
            error_type=faultType,
            error_value=1.0,
            error_position=trackSection,
            length_parameter=trackLength,
            SPT_cable_length=cableLength
        )
        
        # 构建电路模型
        print("开始构建电路模型...")
        model_result = fault.build_circuit_model()
        print("电路模型构建完成")
        
        # 根据电压档位确定电压范围
        def get_voltage_range(level):
            switcher = {
                1: (161, 170),
                2: (146, 154),
                3: (128, 135),
                4: (104.5, 110.5),
                5: (75, 79.5),
                6: (75, 170)
            }
            return switcher.get(level, (75, 170))
        
        # 获取电压范围
        min_voltage, max_voltage = get_voltage_range(voltageLevel)
        print(f"电压范围: {min_voltage}V - {max_voltage}V")
        
        # 生成多组输入电压
        # 生成13个等间距的电压值
        import numpy as np
        input_voltages = np.linspace(min_voltage, max_voltage, 13).tolist()
        # 保留1位小数
        input_voltages = [round(v, 1) for v in input_voltages]
        print(f"使用多组输入电压: {input_voltages}")
        
        # 存储多组仿真结果
        simulation_results = []
        
        for voltage in input_voltages:
            print(f"\n计算输入电压 {voltage}V 对应的输出...")
            fault.input_V = voltage
            
            # 计算输入阻抗
            try:
                input_current, input_impedance, Z_rail, Z_tuner = fault.call_input(voltage, ballastResist / 1000)
                print(f"输入电流: {input_current}")
                print(f"输入阻抗: {input_impedance}")
                print(f"钢轨阻抗: {Z_rail}")
                print(f"调谐区阻抗: {Z_tuner}")
            except Exception as e:
                print(f"计算输入阻抗时出错: {e}")
                input_current = None
                input_impedance = None
                Z_rail = None
                Z_tuner = None
            
            # 计算输出电压
            try:
                output_voltage = fault.count_output()
                print(f"输出电压: {output_voltage}")
            except Exception as e:
                print(f"计算输出电压时出错: {e}")
                output_voltage = None
            
            # 计算主轨入电压和轨出1电压
            try:
                # 调用 call_matrix_main 方法计算主轨入电压
                fault.call_matrix_main()
                
                # 获取主轨入电压
                if hasattr(fault, 'output_voltage_main'):
                    try:
                        # 尝试获取 voltage_main 作为主轨入电压
                        if hasattr(fault, 'voltage_main'):
                            main_rail_input_voltage = fault.voltage_main
                            print(f"从 voltage_main 获取主轨入电压: {main_rail_input_voltage}")
                        else:
                            # 尝试从 output_voltage_main 获取主轨入电压
                            main_rail_input_voltage = fault.output_voltage_main
                            # 检查是否为数组或列表
                            if isinstance(main_rail_input_voltage, (list, np.ndarray)):
                                # 尝试获取第一个元素
                                if len(main_rail_input_voltage) > 0:
                                    main_rail_input_voltage = main_rail_input_voltage[0]
                            # 检查是否为复数
                            if isinstance(main_rail_input_voltage, complex):
                                # 计算复数的模
                                main_rail_input_voltage = abs(main_rail_input_voltage)
                            print(f"主轨入电压: {main_rail_input_voltage}")
                    except Exception as e:
                        print(f"获取主轨入电压时出错: {e}")
                        main_rail_input_voltage = None
                else:
                    main_rail_input_voltage = None
                    print("警告：未找到主轨入电压")
                
                # 获取轨出1电压（这里假设轨出1电压是主轨入电压的一部分）
                if main_rail_input_voltage is not None:
                    # 轨出1电压通常是主轨入电压经过衰耗盘后的电压
                    # 这里使用一个简化的计算方式，实际项目中需要根据具体电路计算
                    rail_output_1_voltage = main_rail_input_voltage * 0.9 if isinstance(main_rail_input_voltage, (int, float, complex)) else None
                    rail_output_2_voltage = main_rail_input_voltage * 0.1 if isinstance(main_rail_input_voltage, (int, float, complex)) else None
                    print(f"轨出1电压: {rail_output_1_voltage}")
                    print(f"轨出2电压: {rail_output_2_voltage}")
                else:
                    rail_output_1_voltage = None
                    rail_output_2_voltage = None
                    print("警告：无法计算轨出1电压和轨出2电压")
            except Exception as e:
                print(f"计算主轨入电压和轨出1电压时出错: {e}")
                import traceback
                traceback.print_exc()
                main_rail_input_voltage = voltage
                rail_output_1_voltage = None
                rail_output_2_voltage = None
            
            # 存储当前电压的仿真结果
            simulation_results.append({
                "inputVoltage": voltage,
                "outputVoltage": str(output_voltage) if output_voltage is not None else "计算失败",
                "inputCurrent": str(input_current) if input_current is not None else "计算失败",
                "inputImpedance": str(input_impedance) if input_impedance is not None else "计算失败",
                "railImpedance": str(Z_rail) if Z_rail is not None else "计算失败",
                "tunerImpedance": str(Z_tuner) if Z_tuner is not None else "计算失败",
                "mainRailInputVoltage": str(main_rail_input_voltage) if main_rail_input_voltage is not None else "计算失败",
                "railOutput1Voltage": str(rail_output_1_voltage) if rail_output_1_voltage is not None else "计算失败",
                "railOutput2Voltage": str(rail_output_2_voltage) if rail_output_2_voltage is not None else "计算失败"
            })
        
        # 构建响应
        response_data = {
            "status": "success",
            "message": "模型仿真成功",
            "data": {
                "trackSection": trackSection,
                "faultType": faultType,
                "trackLength": trackLength,
                "cableLength": cableLength,
                "frequency": frequency,
                "ballastResist": ballastResist,
                "faultStatus": fault.status(),
                "voltageLevel": voltageLevel,
                "voltageRange": {
                    "min": min_voltage,
                    "max": max_voltage
                },
                "simulationResults": simulation_results
            }
        }
        
        return JSONResponse(response_data)
        
    except Exception as e:
        print(f"模型仿真时出错: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"status": "error", "message": f"模型仿真失败: {str(e)}"},
            status_code=500
        )

# 用户注册页面
@app.get("/register", response_class=HTMLResponse)
async def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# 直接返回HTML内容的图片查看器页面
@app.get("/image-viewer-direct", response_class=HTMLResponse)
async def read_image_viewer_direct():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>图片查看器 - 轨道电路故障数据观察</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f7fa;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
        }
        h2 {
            color: #3498db;
            margin: 20px 0 15px;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }
        h3 {
            color: #2980b9;
            margin: 15px 0 10px;
        }
        .btn {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
            margin: 10px 5px 10px 0;
            transition: background-color 0.3s ease;
        }
        .btn:hover {
            background-color: #2980b9;
        }
        .btn.secondary {
            background-color: #95a5a6;
        }
        .btn.secondary:hover {
            background-color: #7f8c8d;
        }
        .form-row {
            display: flex;
            gap: 15px;
            margin: 15px 0;
        }
        .form-col {
            flex: 1;
            min-width: 200px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"], input[type="number"], select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        .image-display {
            margin: 20px 0;
            padding: 20px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 4px;
            text-align: center;
        }
        .image-display img {
            max-width: 100%;
            max-height: 600px;
            object-fit: contain;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin: 10px 0;
        }
        .data-display {
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
            min-height: 100px;
            border: 1px solid #ddd;
        }
        .card {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            margin: 10px 0;
        }
        .tabs {
            margin: 20px 0;
            border-bottom: 1px solid #ddd;
        }
        .tab-button {
            background-color: #f4f7fa;
            border: none;
            border-bottom: 2px solid transparent;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .tab-button.active {
            background-color: white;
            border-bottom-color: #3498db;
            color: #3498db;
            font-weight: bold;
        }
        .tab-content {
            display: none;
            padding: 20px 0;
        }
        .tab-content.active {
            display: block;
        }
        .success { color: #27ae60; }
        .error { color: #e74c3c; }
        .loading { color: #7f8c8d; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>图片查看器 - 轨道电路故障数据观察</h1>
        <div style="margin-bottom: 20px; text-align: center;">
            <a href="/" class="btn">返回首页</a>
        </div>
        <div class="tabs">
            <button class="tab-button active" onclick="openTab(event, 'image')">图片展示</button>
            <button class="tab-button" onclick="openTab(event, 'data')">数据输入</button>
            <button class="tab-button" onclick="openTab(event, 'result')">计算结果</button>
        </div>
        <div id="image" class="tab-content active">
            <h2>图片选择与展示</h2>
            <div class="form-row">
                <div class="form-col">
                    <label for="imageSelect">选择图片:</label>
                    <select id="imageSelect" onchange="changeImage()">
                        <option value="0">0 - 无故障</option>
                        <option value="1">1 - 接收端调谐单元1断路</option>
                        <option value="2">2 - 发送端调谐单元1断路</option>
                        <option value="3">3 - 接收端空心线圈断路</option>
                        <option value="4">4 - 接收端空芯线圈短路</option>
                        <option value="5">5 - 接收端调谐单元2断路</option>
                        <option value="6">6 - 补偿电容3断路</option>
                        <option value="7">7 - 补偿电容3短路</option>
                    </select>
                </div>
                <div class="form-col">
                    <label for="imageWidth">图片宽度 (像素):</label>
                    <input type="number" id="imageWidth" value="800" min="200" max="1200">
                </div>
            </div>
            <div class="image-display">
                <h3>当前图片</h3>
                <img id="displayImage" src="/static/images/错误展示0.png" alt="错误展示0 - 无故障" style="max-width: 100%; height: auto;">
                <p id="imageDescription">错误展示0 - 无故障</p>
            </div>
        </div>
        <div id="data" class="tab-content">
            <h2>数据输入</h2>
            <form id="dataForm" onsubmit="event.preventDefault(); calculateData();">
                <div class="form-row">
                    <div class="form-col">
                        <label for="trackName">轨道名称:</label>
                        <input type="text" id="trackName" placeholder="输入轨道名称" value="测试轨道">
                    </div>
                    <div class="form-col">
                        <label for="trackLength">轨道长度 (m):</label>
                        <input type="number" id="trackLength" placeholder="输入轨道长度" value="100" min="1">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-col">
                        <label for="resistance">电阻 (Ω/m):</label>
                        <input type="number" id="resistance" placeholder="输入电阻值" value="0.1" step="0.01" min="0">
                    </div>
                    <div class="form-col">
                        <label for="inductance">电感 (H/m):</label>
                        <input type="number" id="inductance" placeholder="输入电感值" value="1.0e-3" step="0.000001" min="0">
                    </div>
                    <div class="form-col">
                        <label for="capacitance">电容 (F/m):</label>
                        <input type="number" id="capacitance" placeholder="输入电容值" value="1.0e-9" step="0.000000001" min="0">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-col">
                        <label for="frequency">频率 (Hz):</label>
                        <input type="number" id="frequency" placeholder="输入频率" value="1700" min="1">
                    </div>
                    <div class="form-col">
                        <label for="errorType">错误类型:</label>
                        <select id="errorType">
                            <option value="0">无故障</option>
                            <option value="1">接收端调谐单元1断路</option>
                            <option value="2">发送端调谐单元1断路</option>
                            <option value="3">接收端空心线圈断路</option>
                            <option value="4">接收端空芯线圈短路</option>
                            <option value="5">接收端调谐单元2断路</option>
                            <option value="6">补偿电容3断路</option>
                            <option value="7">补偿电容3短路</option>
                        </select>
                    </div>
                </div>
                <button type="submit" class="btn">计算数据</button>
                <button type="button" class="btn secondary" onclick="clearForm()">重置</button>
            </form>
        </div>
        <div id="result" class="tab-content">
            <h2>计算结果</h2>
            <div class="data-display" id="resultDisplay">
                <p class="loading">请在数据输入标签页输入参数并点击计算按钮</p>
            </div>
        </div>
    </div>
    <script>
        // 图片数据
        const images = {
            "0": {
                src: "/static/images/错误展示0.png",
                description: "错误展示0 - 无故障"
            },
            "1": {
                src: "/static/images/错误展示1.png",
                description: "错误展示1 - 接收端调谐单元1断路"
            },
            "2": {
                src: "/static/images/错误展示2.png",
                description: "错误展示2 - 发送端调谐单元1断路"
            },
            "3": {
                src: "/static/images/错误展示3.png",
                description: "错误展示3 - 接收端空心线圈断路"
            },
            "4": {
                src: "/static/images/错误展示4.png",
                description: "错误展示4 - 接收端空芯线圈短路"
            },
            "5": {
                src: "/static/images/错误展示5.png",
                description: "错误展示5 - 接收端调谐单元2断路"
            },
            "6": {
                src: "/static/images/错误展示6.png",
                description: "错误展示6 - 补偿电容3断路"
            },
            "7": {
                src: "/static/images/错误展示7.png",
                description: "错误展示7 - 补偿电容3短路"
            }
        };

        // 页面加载时初始化
        document.addEventListener('DOMContentLoaded', function() {
            changeImage();
        });

        // 切换图片
        function changeImage() {
            const select = document.getElementById('imageSelect');
            const imageInfo = images[select.value] || images["0"];
            const displayImage = document.getElementById('displayImage');
            const imageDescription = document.getElementById('imageDescription');
            const imageWidth = document.getElementById('imageWidth').value;
            displayImage.src = imageInfo.src;
            displayImage.alt = imageInfo.description;
            imageDescription.textContent = imageInfo.description;
            displayImage.style.width = imageWidth + 'px';
        }

        // 切换标签页
        function openTab(evt, tabName) {
            const tabButtons = document.getElementsByClassName('tab-button');
            const tabContents = document.getElementsByClassName('tab-content');
            for (let i = 0; i < tabContents.length; i++) {
                tabContents[i].classList.remove('active');
            }
            for (let i = 0; i < tabButtons.length; i++) {
                tabButtons[i].classList.remove('active');
            }
            document.getElementById(tabName).classList.add('active');
            evt.currentTarget.classList.add('active');
        }

        // 计算数据
        async function calculateData() {
            const resultDisplay = document.getElementById('resultDisplay');
            resultDisplay.innerHTML = '<p class="loading">正在计算数据...</p>';
            try {
                const data = {
                    name: document.getElementById('trackName').value,
                    length: parseFloat(document.getElementById('trackLength').value),
                    resistance: parseFloat(document.getElementById('resistance').value),
                    inductance: parseFloat(document.getElementById('inductance').value),
                    capacitance: parseFloat(document.getElementById('capacitance').value),
                    frequency: parseFloat(document.getElementById('frequency').value),
                    error_type: parseInt(document.getElementById('errorType').value)
                };
                const result = await simulateCalculation(data);
                let html = '<h3>计算结果</h3>';
                html += '<div class="card">';
                html += '<p><strong>轨道名称:</strong> ' + result.name + '</p>';
                html += '<p><strong>轨道长度:</strong> ' + result.length + ' m</p>';
                html += '<p><strong>总阻抗:</strong> ' + result.total_impedance.toFixed(6) + ' Ω</p>';
                html += '<p><strong>总导纳:</strong> ' + result.total_admittance.toFixed(6) + ' S</p>';
                html += '<p><strong>传播系数:</strong> ' + result.propagation_constant.toFixed(6) + '</p>';
                html += '<p><strong>特性阻抗:</strong> ' + result.characteristic_impedance.toFixed(6) + ' Ω</p>';
                html += '<p><strong>错误类型:</strong> ' + result.error_type + '</p>';
                html += '</div>';
                resultDisplay.innerHTML = '<p class="success">✅ 数据计算成功！</p>' + html;
            } catch (error) {
                resultDisplay.innerHTML = '<p class="error">❌ 计算失败: ' + error.message + '</p>';
            }
        }

        // 模拟计算函数
        function simulateCalculation(data) {
            return new Promise(resolve => {
                setTimeout(() => {
                    // 简化的实数计算（移除复数运算，使用实数近似）
                    const inductive_reactance = 2 * Math.PI * data.frequency * data.inductance;
                    const capacitive_reactance = 1 / (2 * Math.PI * data.frequency * data.capacitance);
                    const total_reactance = inductive_reactance - capacitive_reactance;
                    const total_impedance = Math.sqrt(data.resistance * data.resistance + total_reactance * total_reactance);
                    const total_admittance = 1 / total_impedance;
                    const propagation_constant = Math.sqrt(total_impedance * total_admittance);
                    const characteristic_impedance = Math.sqrt(total_impedance / total_admittance);
                    const errorTypes = {
                        0: "无故障",
                        1: "接收端调谐单元1断路",
                        2: "发送端调谐单元1断路",
                        3: "接收端空心线圈断路",
                        4: "接收端空芯线圈短路",
                        5: "接收端调谐单元2断路",
                        6: "补偿电容3断路",
                        7: "补偿电容3短路"
                    };
                    resolve({
                        name: data.name,
                        value: 0,
                        length: data.length,
                        total_impedance: total_impedance,
                        total_admittance: total_admittance,
                        propagation_constant: propagation_constant,
                        characteristic_impedance: characteristic_impedance,
                        error_type: errorTypes[data.error_type] || "未知错误类型"
                    });
                }, 500);
            });
        }

        // 清除表单
        function clearForm() {
            document.getElementById('dataForm').reset();
        }
    </script>
</body>
</html>
""")

# API端点示例
@app.get("/api/data")
async def get_data():
    return {
        "message": "Hello from FastAPI!",
        "status": "success",
        "data": {
            "items": ["item1", "item2", "item3"],
            "count": 3
        }
    }

# 带参数的API端点
@app.get("/api/items/{item_id}")
async def get_item(item_id: int, q: str = None):
    return {
        "item_id": item_id,
        "q": q,
        "description": f"This is item {item_id}"
    }

# 计算阻抗API端点
@app.post("/api/calculate/impedance")
async def calculate_impedance_api(
    resist: float = Form(...),
    induct: float = Form(...),
    capacit: float = Form(...),
    angular_frequency: float = Form(0)
):
    try:
        impedance_mod, impedance_complex = calculate_impedance(resist, induct, capacit, angular_frequency)
        return JSONResponse({
            "status": "success",
            "result": {
                "impedance_mod": float(impedance_mod),
                "impedance_complex": {
                    "real": float(impedance_complex.real),
                    "imag": float(impedance_complex.imag),
                    "magnitude": float(np.abs(impedance_complex)),
                    "phase": float(np.angle(impedance_complex, deg=True))
                },
                "resist": resist,
                "induct": induct,
                "capacit": capacit,
                "angular_frequency": angular_frequency
            }
        })
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=400
        )

# 计算导纳API端点
@app.post("/api/calculate/admittance")
async def calculate_admittance_api(
    resist: float = Form(...),
    induct: float = Form(...),
    capacit: float = Form(...),
    angular_frequency: float = Form(0)
):
    try:
        admittance_mod, admittance_complex = calculate_admittance(resist, induct, capacit, angular_frequency)
        return JSONResponse({
            "status": "success",
            "result": {
                "admittance_mod": float(admittance_mod),
                "admittance_complex": {
                    "real": float(admittance_complex.real),
                    "imag": float(admittance_complex.imag),
                    "magnitude": float(np.abs(admittance_complex)),
                    "phase": float(np.angle(admittance_complex, deg=True))
                },
                "resist": resist,
                "induct": induct,
                "capacit": capacit,
                "angular_frequency": angular_frequency
            }
        })
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=400
        )

# 计算电流API端点
@app.post("/api/calculate/current")
async def calculate_current_api(
    voltage_real: float = Form(...),
    voltage_imag: float = Form(...),
    resist: float = Form(...),
    induct: float = Form(...),
    capacit: float = Form(...)
):
    try:
        voltage = np.array([voltage_real, voltage_imag])
        current = calculate_current(voltage, resist, induct, capacit)
        return JSONResponse({
            "status": "success",
            "result": {
                "current_real": float(current[0]),
                "current_imag": float(current[1]),
                "voltage_real": voltage_real,
                "voltage_imag": voltage_imag,
                "resist": resist,
                "induct": induct,
                "capacit": capacit
            }
        })
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=400
        )

# 计算变量API端点（使用Variable类）
@app.post("/api/calculate/variable")
async def calculate_variable_api(
    name: str = Form(...),
    value: float = Form(...),
    length_guidao: float = Form(...),
    resist_per_meter: float = Form(...),
    induct_per_meter: float = Form(...),
    capacit_per_meter: float = Form(...)
):
    try:
        # 创建Variable实例
        variable = Variable(
            name=name,
            value=value,
            length_guidao=length_guidao,
            resist_per_meter=resist_per_meter,
            induct_per_meter=induct_per_meter,
            capacit_per_meter=capacit_per_meter
        )
        
        # 构建响应数据
        result = {
            "name": variable.name,
            "value": variable.value,
            "length_guidao": variable.length_guidao,
            "resist_per_meter": variable.resist_per_meter,
            "induct_per_meter": variable.induct_per_meter,
            "capacit_per_meter": variable.capacit_per_meter,
            "resist_guidao": variable.resist_guidao,
            "induct_guidao": variable.induct_guidao,
            "conduct_per_meter": variable.conduct_per_meter,
            "conduct_guidao": variable.conduct_guidao,
            "frequency": variable.frequency,
            "angular_frequency": variable.angular_frequency,
            "capacit_guidao": variable.capacit_guidao,
            
            # 阻抗（包含复数形式）
            "impedance": {
                "mod": float(variable.impedance),
                "complex": {
                    "real": float(variable.impedance_complex.real),
                    "imag": float(variable.impedance_complex.imag),
                    "magnitude": float(np.abs(variable.impedance_complex)),
                    "phase": float(np.angle(variable.impedance_complex, deg=True))
                }
            },
            
            # 导纳（包含复数形式）
            "admittance": {
                "mod": float(variable.admittance),
                "complex": {
                    "real": float(variable.admittance_complex.real),
                    "imag": float(variable.admittance_complex.imag),
                    "magnitude": float(np.abs(variable.admittance_complex)),
                    "phase": float(np.angle(variable.admittance_complex, deg=True))
                }
            },
            
            # 传播系数（包含复数形式）
            "gamma": {
                "real": float(variable.gamma[0]),
                "imag": float(variable.gamma[1]),
                "mod": float(variable.gamma_mod),
                "complex": {
                    "real": float(variable.gamma_complex.real),
                    "imag": float(variable.gamma_complex.imag),
                    "magnitude": float(np.abs(variable.gamma_complex)),
                    "phase": float(np.angle(variable.gamma_complex, deg=True))
                }
            },
            
            # 特性阻抗（波阻抗，包含复数形式）
            "Z_c": {
                "real": float(variable.Z_c[0]),
                "imag": float(variable.Z_c[1]),
                "complex": {
                    "real": float(variable.Z_c_complex.real),
                    "imag": float(variable.Z_c_complex.imag),
                    "magnitude": float(np.abs(variable.Z_c_complex)),
                    "phase": float(np.angle(variable.Z_c_complex, deg=True))
                }
            },
            
            # 新增复数形式的阻抗和导纳
            "Z_complex": {
                "real": float(variable.Z_complex.real),
                "imag": float(variable.Z_complex.imag),
                "magnitude": float(np.abs(variable.Z_complex)),
                "phase": float(np.angle(variable.Z_complex, deg=True))
            },
            "Y_complex": {
                "real": float(variable.Y_complex.real),
                "imag": float(variable.Y_complex.imag),
                "magnitude": float(np.abs(variable.Y_complex)),
                "phase": float(np.angle(variable.Y_complex, deg=True))
            }
        }
        
        return JSONResponse({
            "status": "success",
            "result": result
        })
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=400
        )

# 错误数据观察API端点
@app.post("/api/error/observe")
async def observe_error_api(
    trail: str = Form(...),
    error_type: int = Form(...),
    error_value: float = Form(...),
    error_position: str = Form(...)
):
    try:
        # 创建Error_Of_Trail实例
        error_instance = Error_Of_Trail(
            trail=trail,
            error_type=error_type,
            error_value=error_value,
            error_position=error_position,
            length_parameter=100.0
        )
        
        # 构建电路模型
        model_info = error_instance.build_circuit_model()
        
        # 构建响应数据
        result = {
            "trail": trail,
            "error_type": error_type,
            "error_value": error_value,
            "error_position": error_position,
            "error_status": error_instance.status(),
            "model_info": model_info
        }
        
        return JSONResponse({
            "status": "success",
            "result": result
        })
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=400
        )

# SPT电缆参数计算API端点
@app.post("/api/calculate/spt-cable")
async def calculate_spt_cable_api(
    length: float = Form(...),
    frequency: float = Form(...)
):
    try:
        # 导入jisuan_guidao模块
        import jisuan_guidao as jg
        
        # 获取SPT电缆参数
        spt_params = jg.find_SPTcable_parameters(frequency)
        gamma_cable_dbkm = spt_params[0]
        impedance = spt_params[1]
        impedance_angle = spt_params[2]
        
        # 计算单位长度电阻和电感
        impedance_angle_rad = impedance_angle * np.pi / 180
        unit_resistance = impedance * np.cos(impedance_angle_rad)
        unit_inductance = impedance * np.sin(impedance_angle_rad) / (2 * np.pi * frequency)
        
        # 计算总参数
        total_resistance = unit_resistance * length
        total_inductance = unit_inductance * length
        
        # 计算传输矩阵
        cable_matrix = jg.SPTcable_matrix(frequency, length)
        
        # 构建响应
        response = {
            "status": "success",
            "data": {
                "gamma_cable": gamma_cable_dbkm,
                "impedance": impedance,
                "impedance_angle": impedance_angle,
                "resistance": total_resistance,
                "inductance": total_inductance,
                "unit_resistance": unit_resistance,
                "unit_inductance": unit_inductance,
                "length": length,
                "frequency": frequency,
                "matrix": {
                    "a": cable_matrix[0][0].real,
                    "b": cable_matrix[0][1].real,
                    "c": cable_matrix[1][0].real,
                    "d": cable_matrix[1][1].real
                }
            }
        }
        
        return response
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# 轨道电路故障模拟计算API端点
@app.post("/api/calculate/track-circuit")
async def calculate_track_circuit_api(
    trail: str = Form(...),
    error_type: int = Form(...),
    error_value: float = Form(...),
    error_position: str = Form(...),
    track_length: float = Form(...),
    resist_per_meter: float = Form(...),
    induct_per_meter: float = Form(...),
    capacit_per_meter: float = Form(...),
    conduct_per_meter: float = Form(...),
    frequency: float = Form(...),
    spt_cable_length: float = Form(10.0),  # SPT电缆长度，默认10.0
    r1: int = Form(1),  # 衰耗盘端子1，默认1
    r2: int = Form(1),  # 衰耗盘端子2，默认1
    input_V: float = Form(130.0)  # 输入电压，默认130V
):
    try:
        # 创建Error_Of_Trail实例
        error_instance = Error_Of_Trail(
            trail=trail,
            error_type=error_type,
            error_value=error_value,
            error_position=error_position,
            length_parameter=track_length,
            SPT_cable_length=spt_cable_length,  # 使用前端传递的SPT电缆长度
            input_V=input_V,  # 使用前端传递的输入电压
            r1=r1,  # 传递衰耗盘端子1
            r2=r2   # 传递衰耗盘端子2
        )
        
        # 重新初始化参数
        error_instance.reinitialize_parameters(
            error_type=error_type,
            error_value=error_value,
            error_position=error_position,
            length_parameter=track_length,
            SPT_cable_length=spt_cable_length,
            input_V=input_V,  # 使用前端传递的输入电压
            resist_per_meter=resist_per_meter,
            induct_per_meter=induct_per_meter,
            capacit_per_meter=capacit_per_meter,
            conduct_per_meter=conduct_per_meter,  # 添加电导参数
            r1=r1,  # 添加衰耗盘端子1
            r2=r2   # 添加衰耗盘端子2
        )
        
        # 调用call_matrix_main方法获取计算结果
        result = error_instance.call_matrix_main()
        
        # 处理矩阵中的NaN值，确保JSON序列化成功
        def safe_matrix(matrix):
            try:
                # 转换为实数矩阵
                real_matrix = matrix.real
                # 替换NaN和无穷大值为0
                real_matrix = np.nan_to_num(real_matrix, nan=0.0, posinf=0.0, neginf=0.0)
                # 转换为列表
                return real_matrix.tolist()
            except:
                # 如果出错，返回空矩阵
                return [[0.0, 0.0], [0.0, 0.0]]
        
        # 构建响应数据
        response = {
            "status": "success",
            "section_info": {
                "id": error_position,
                "name": trail,
                "description": f"{trail}轨道区段"
            },
            "error_info": {
                "type": error_type,
                "name": error_instance.status()
            },
            "input_params": {
                "trail": trail,
                "error_type": error_type,
                "error_value": error_value,
                "error_position": error_position,
                "track_length": track_length,
                "resist_per_meter": resist_per_meter,
                "induct_per_meter": induct_per_meter,
                "capacit_per_meter": capacit_per_meter,
                "frequency": frequency
            },
            "voltage_results": result["voltage_results"],
            "current_results": result.get("current_results", {}),
            "matrix": safe_matrix(result["matrix"]),  # 处理矩阵中的NaN值
            "input_impedance": result.get("input_impedance", 0.0),
            "input_current": result.get("input_current", 0.0),
            "Z_rail": result.get("Z_rail", 0.0),
            "Z_tuner": result.get("Z_tuner", 0.0)
        }
        
        return JSONResponse(response)
    except Exception as e:
        import traceback
        print(f"API错误详情: {e}")
        print(f"错误类型: {type(e)}")
        traceback.print_exc()
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=400
        )

# 登录验证API端点
@app.post("/api/login")
async def login_api(
    username: str = Form(...),
    password: str = Form(...)
):
    try:
        import csv
        import os
        
        print(f"接收到登录请求: username={username}, password={password}")
        
        # 读取CSV文件
        csv_path = os.path.join("static", "username_code.csv")
        
        # 检查文件是否存在
        if not os.path.exists(csv_path):
            print("用户数据文件不存在")
            return JSONResponse(
                {"status": "error", "message": "用户数据文件不存在"},
                status_code=500
            )
        
        # 验证用户名和密码
        with open(csv_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if len(lines) < 2:
                print("用户数据文件格式错误")
                return JSONResponse(
                    {"status": "error", "message": "用户数据文件格式错误"},
                    status_code=500
                )
            
            # 跳过表头
            for line in lines[1:]:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        csv_username = parts[0].strip()
                        csv_password = parts[1].strip()
                        print(f"CSV用户: {csv_username}")
                        print(f"用户名匹配: {csv_username == username}")
                        # 验证密码（使用哈希验证，限制密码长度为72字节）
                        truncated_password = password[:72]  # 截断密码长度
                        password_match = pwd_context.verify(truncated_password, csv_password)
                        print(f"密码匹配: {password_match}")
                        if csv_username == username and password_match:
                            print("登录成功！")
                            return JSONResponse({
                                "status": "success",
                                "message": "登录成功",
                                "user": {
                                    "username": username
                                }
                            })
        
        # 未找到匹配的用户
        print("登录失败：用户名或密码错误")
        return JSONResponse(
            {"status": "error", "message": "用户名或密码错误"},
            status_code=401
        )
    except Exception as e:
        print(f"登录验证错误: {e}")
        return JSONResponse(
            {"status": "error", "message": "登录验证失败"},
            status_code=500
        )

# 用户注册API端点
@app.post("/api/register")
async def register_api(
    username: str = Form(...),
    password: str = Form(...)
):
    try:
        import csv
        import os
        import traceback
        
        print(f"接收到注册请求: username={username}")
        
        # 读取CSV文件
        csv_path = os.path.join("static", "username_code.csv")
        print(f"用户数据文件路径: {csv_path}")
        
        # 检查文件是否存在，如果不存在则创建
        if not os.path.exists(csv_path):
            print("用户数据文件不存在，创建新文件")
            # 创建文件并写入表头
            with open(csv_path, 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['username', 'code'])
        
        # 检查用户名是否已存在
        print("检查用户名是否已存在")
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # 跳过表头
            for row in reader:
                if len(row) >= 1 and row[0].strip() == username:
                    print(f"用户名已存在: {username}")
                    return JSONResponse(
                        {"status": "error", "message": "用户名已存在"},
                        status_code=400
                    )
        
        # 对密码进行哈希处理（限制密码长度为72字节）
        print("对密码进行哈希处理")
        # 确保密码不超过72字节
        if len(password) > 72:
            print(f"密码长度超过72字节，截断为72字节")
            password = password[:72]
        print(f"处理后的密码长度: {len(password)}")
        hashed_password = pwd_context.hash(password)
        print(f"哈希后的密码: {hashed_password}")
        
        # 添加新用户到CSV文件
        print("添加新用户到CSV文件")
        with open(csv_path, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, hashed_password])
        
        print(f"用户注册成功: {username}")
        return JSONResponse({
            "status": "success",
            "message": "注册成功",
            "user": {
                "username": username
            }
        })
    except Exception as e:
        print(f"注册错误: {e}")
        traceback.print_exc()
        return JSONResponse(
            {"status": "error", "message": f"注册失败: {str(e)}"},
            status_code=500
        )

# 批量模拟CSV下载API端点
@app.post("/api/batch-download")
async def batch_download_api(data: dict = Body(...)):
    try:
        import csv
        import io
        from datetime import datetime
        
        batch_results = data.get("results", [])
        
        if not batch_results:
            return JSONResponse(
                {"status": "error", "message": "没有可下载的数据"},
                status_code=400
            )
        
        # 创建CSV内容
        csv_lines = []
        
        # 写入BOM标记
        csv_lines.append('\ufeff')
        
        # 写入表头
        headers = [
            '时间戳',
            '轨道区段ID',
            '轨道区段名称',
            '故障类型',
            '故障类型名称',
            '轨道长度(m)',
            '钢轨电阻(Ω/m)',
            '钢轨电感(H/m)',
            '漏泄电容(F/m)',
            '钢轨漏泄电阻(Ω/km)',
            'SPT电缆长度(km)',
            '电平档位',
            '错误值',
            '衰耗盘端子1',
            '衰耗盘端子2',
            '送端轨面电压(V)',
            '受端轨面电压(V)',
            '主轨入电压(V)',
            '轨出1电压(V)',
            '送端轨面电流(A)',
            '受端轨面电流(A)',
            '主轨入电流(A)',
            '轨出1电流(A)',
            '输入阻抗(Ω)',
            '输入电流(A)',
            '主轨道阻抗(Ω)',
            '调谐区阻抗(Ω)'
        ]
        csv_lines.append(headers.join(','))
        
        # 写入数据
        for result in batch_results:
            row = [
                result.get('timestamp', ''),
                result.get('section_id', ''),
                result.get('section_name', ''),
                result.get('error_type', ''),
                result.get('error_type_name', ''),
                result.get('track_length', 0),
                result.get('resistance', 0),
                result.get('inductance', 0),
                result.get('capacitance', 0),
                result.get('leakage_resistance', 0),
                result.get('spt_cable_length', 0),
                result.get('voltage_level', 0),
                result.get('error_value', 0),
                result.get('r1', 0),
                result.get('r2', 0),
                result.get('send_end_track_voltage', 0),
                result.get('receive_end_track_voltage', 0),
                result.get('main_track_input_voltage', 0),
                result.get('main_track_output_voltage_1', 0),
                result.get('send_end_track_current', 0),
                result.get('receive_end_track_current', 0),
                result.get('main_track_input_current', 0),
                result.get('main_track_output_current_1', 0),
                result.get('input_impedance', 0),
                result.get('input_current', 0),
                result.get('Z_rail', 0),
                result.get('Z_tuner', 0)
            ]
            # 转换所有值为字符串并处理逗号
            row_str = [str(item).replace(',', ' ') for item in row]
            csv_lines.append(','.join(row_str))
        
        # 合并所有行
        csv_content = '\n'.join(csv_lines)
        
        # 编码为UTF-8字节
        csv_content_bytes = csv_content.encode('utf-8')
        
        # 生成文件名
        filename = f"批量模拟数据_{datetime.now().strftime('%Y-%m-%d')}.csv"
        
        # 返回CSV文件
        return Response(
            content=csv_content_bytes,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "text/csv; charset=utf-8"
            }
        )
    except Exception as e:
        print(f"CSV下载错误: {e}")
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=500
        )

# 批量模拟XLSX下载API端点
@app.post("/api/batch-download-xlsx")
async def batch_download_xlsx_api(data: dict = Body(...)):
    try:
        import openpyxl
        from io import BytesIO
        from datetime import datetime
        
        batch_results = data.get("results", [])
        
        if not batch_results:
            return JSONResponse(
                {"status": "error", "message": "没有可下载的数据"},
                status_code=400
            )
        
        # 创建Excel工作簿
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "批量模拟数据"
        
        # 写入表头
        headers = [
            '时间戳',
            '轨道区段ID',
            '轨道区段名称',
            '错误类型',
            '错误类型名称',
            '轨道长度(m)',
            '钢轨电阻(Ω/m)',
            '钢轨电感(H/m)',
            '漏泄电容(F/m)',
            '钢轨漏泄电阻(Ω/km)',
            'SPT电缆长度(km)',
            '电平档位',
            '错误值',
            '衰耗盘端子1',
            '衰耗盘端子2',
            '送端轨面电压(V)',
            '受端轨面电压(V)',
            '主轨入电压(V)',
            '轨出1电压(V)',
            '送端轨面电流(A)',
            '受端轨面电流(A)',
            '主轨入电流(A)',
            '轨出1电流(A)',
            '输入阻抗(Ω)',
            '输入电流(A)',
            '主轨道阻抗(Ω)',
            '调谐区阻抗(Ω)'
        ]
        ws.append(headers)
        
        # 写入数据
        for result in batch_results:
            row = [
                result.get('timestamp', ''),
                result.get('section_id', ''),
                result.get('section_name', ''),
                result.get('error_type', ''),
                result.get('error_type_name', ''),
                result.get('track_length', 0),
                result.get('resistance', 0),
                result.get('inductance', 0),
                result.get('capacitance', 0),
                result.get('leakage_resistance', 0),
                result.get('spt_cable_length', 0),
                result.get('voltage_level', 0),
                result.get('error_value', 0),
                result.get('r1', 0),
                result.get('r2', 0),
                result.get('send_end_track_voltage', 0),
                result.get('receive_end_track_voltage', 0),
                result.get('main_track_input_voltage', 0),
                result.get('main_track_output_voltage_1', 0),
                result.get('send_end_track_current', 0),
                result.get('receive_end_track_current', 0),
                result.get('main_track_input_current', 0),
                result.get('main_track_output_current_1', 0),
                result.get('input_impedance', 0),
                result.get('input_current', 0),
                result.get('Z_rail', 0),
                result.get('Z_tuner', 0)
            ]
            ws.append(row)
        
        # 调整列宽
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # 保存到内存
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        # 生成文件名
        filename = f"批量模拟数据_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        
        # 返回XLSX文件
        return Response(
            content=output.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        print(f"XLSX下载错误: {e}")
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=500
        )

# 启动应用的命令（用于开发环境）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,
        workers=1
    )
# 运行：uvicorn main:app --reload

# 时序数据存储系统（基于内存）
import uuid
from datetime import datetime
import threading

class TimeSeriesStorage:
    def __init__(self):
        self._lock = threading.Lock()
        self._sessions = {}

    def create_session(self):
        session_id = str(uuid.uuid4())
        with self._lock:
            self._sessions[session_id] = {
                'created_at': datetime.now().isoformat(),
                'results': []
            }
        return session_id

    def add_result(self, session_id, result_data):
        with self._lock:
            if session_id in self._sessions:
                self._sessions[session_id]['results'].append(result_data)
                return True
            return False

    def get_results(self, session_id):
        with self._lock:
            if session_id in self._sessions:
                return self._sessions[session_id]['results']
            return []

    def get_session_info(self, session_id):
        with self._lock:
            if session_id in self._sessions:
                return {
                    'session_id': session_id,
                    'created_at': self._sessions[session_id]['created_at'],
                    'result_count': len(self._sessions[session_id]['results'])
                }
            return None

    def clear_session(self, session_id):
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
            return False

# 全局存储实例
time_series_storage = TimeSeriesStorage()

# 创建时序数据存储会话
@app.post("/api/time-series/create-session")
async def create_time_series_session():
    session_id = time_series_storage.create_session()
    return JSONResponse({
        "status": "success",
        "session_id": session_id
    })

# 添加时序数据到会话
@app.post("/api/time-series/add-result/{session_id}")
async def add_time_series_result(session_id: str, data: dict = Body(...)):
    result = time_series_storage.add_result(session_id, data)
    if result:
        return JSONResponse({"status": "success"})
    return JSONResponse(
        {"status": "error", "message": "会话不存在"},
        status_code=404
    )

# 获取会话中的所有数据
@app.get("/api/time-series/get-results/{session_id}")
async def get_time_series_results(session_id: str):
    results = time_series_storage.get_results(session_id)
    return JSONResponse({
        "status": "success",
        "results": results,
        "count": len(results)
    })

# 获取会话信息
@app.get("/api/time-series/session-info/{session_id}")
async def get_session_info(session_id: str):
    info = time_series_storage.get_session_info(session_id)
    if info:
        return JSONResponse({
            "status": "success",
            "info": info
        })
    return JSONResponse(
        {"status": "error", "message": "会话不存在"},
        status_code=404
    )

# 清除会话
@app.delete("/api/time-series/clear-session/{session_id}")
async def clear_session(session_id: str):
    if time_series_storage.clear_session(session_id):
        return JSONResponse({"status": "success"})
    return JSONResponse(
        {"status": "error", "message": "会话不存在"},
        status_code=404
    )

# CSV文件存储系统
import csv
import os
from datetime import datetime

CSV_FILE_PATH = os.path.join("static", "time_series_data.csv")

# 清除CSV文件（初始化）
@app.post("/api/time-series/clear-csv")
async def clear_csv_file():
    try:
        # 如果文件存在则删除
        if os.path.exists(CSV_FILE_PATH):
            os.remove(CSV_FILE_PATH)
        return JSONResponse({"status": "success", "message": "CSV文件已清除"})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# 保存单条数据到CSV
@app.post("/api/time-series/save-to-csv")
async def save_to_csv(data: dict = Body(...)):
    try:
        file_exists = os.path.exists(CSV_FILE_PATH)
        file_empty = not file_exists or os.path.getsize(CSV_FILE_PATH) == 0

        with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['voltage', 'section_id', 'error_type', 'track_length',
                          'send_end_track_voltage', 'receive_end_track_voltage',
                          'main_track_input_voltage', 'main_track_output_voltage_1',
                          'input_impedance', 'input_current', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # 如果文件不存在或为空，写入表头
            if file_empty:
                writer.writeheader()

            # 写入数据行
            writer.writerow({
                'voltage': data.get('voltage', 0),
                'section_id': data.get('section_id', ''),
                'error_type': data.get('error_type', 0),
                'track_length': data.get('track_length', 0),
                'send_end_track_voltage': data.get('send_end_track_voltage', 0),
                'receive_end_track_voltage': data.get('receive_end_track_voltage', 0),
                'main_track_input_voltage': data.get('main_track_input_voltage', 0),
                'main_track_output_voltage_1': data.get('main_track_output_voltage_1', 0),
                'input_impedance': data.get('input_impedance', 0),
                'input_current': data.get('input_current', 0),
                'timestamp': data.get('timestamp', datetime.now().isoformat())
            })

        return JSONResponse({"status": "success"})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# 从CSV读取所有数据
@app.get("/api/time-series/read-from-csv")
async def read_from_csv():
    try:
        if not os.path.exists(CSV_FILE_PATH):
            return JSONResponse({"status": "success", "results": [], "count": 0})

        results = []
        with open(CSV_FILE_PATH, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 转换数值类型
                try:
                    results.append({
                        'voltage': float(row['voltage']),
                        'section_id': row['section_id'],
                        'error_type': int(row['error_type']),
                        'track_length': float(row['track_length']),
                        'send_end_track_voltage': float(row['send_end_track_voltage']),
                        'receive_end_track_voltage': float(row['receive_end_track_voltage']),
                        'main_track_input_voltage': float(row['main_track_input_voltage']),
                        'main_track_output_voltage_1': float(row['main_track_output_voltage_1']),
                        'input_impedance': float(row['input_impedance']),
                        'input_current': float(row['input_current']),
                        'timestamp': row['timestamp']
                    })
                except (ValueError, KeyError) as e:
                    # 跳过无效行
                    continue

        return JSONResponse({"status": "success", "results": results, "count": len(results)})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# 获取CSV文件状态
@app.get("/api/time-series/csv-status")
async def get_csv_status():
    try:
        if not os.path.exists(CSV_FILE_PATH):
            return JSONResponse({
                "status": "success",
                "exists": False,
                "row_count": 0
            })

        with open(CSV_FILE_PATH, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            row_count = sum(1 for row in reader) - 1  # 减去表头

        return JSONResponse({
            "status": "success",
            "exists": True,
            "row_count": max(0, row_count)
        })
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
