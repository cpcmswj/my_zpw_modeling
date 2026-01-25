from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np

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

# 根路径，返回HTML页面
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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
    frequency: float = Form(...)
):
    try:
        # 创建Error_Of_Trail实例
        error_instance = Error_Of_Trail(
            trail=trail,
            error_type=error_type,
            error_value=error_value,
            error_position=error_position
        )
        
        # 重新初始化参数
        error_instance.reinitialize_parameters(
            error_type=error_type,
            error_value=error_value,
            error_position=error_position,
            length_parameter=track_length,
            resist_per_meter=resist_per_meter,
            induct_per_meter=induct_per_meter,
            capacit_per_meter=capacit_per_meter
        )
        
        # 调用call_matrix_main方法获取计算结果
        result = error_instance.call_matrix_main()
        
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
            "matrix": result["matrix"].real.tolist()  # 只取矩阵的实部，避免JSON序列化错误
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

# 启动应用的命令（用于开发环境）
# 运行：uvicorn main:app --reload
