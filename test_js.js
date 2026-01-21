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

// 切换图片
function changeImage() {
    const select = document.getElementById('imageSelect');
    // 使用第一张图片作为默认值
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
    
    // 隐藏所有标签内容
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }
    
    // 移除所有按钮的活动状态
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }
    
    // 显示当前标签内容和按钮
    document.getElementById(tabName).classList.add('active');
    evt.currentTarget.classList.add('active');
}

// 计算数据
async function calculateData() {
    const resultDisplay = document.getElementById('resultDisplay');
    resultDisplay.innerHTML = '<p class="loading">正在计算数据...</p>';
    
    try {
        // 获取表单数据
        const formData = new FormData(document.getElementById('dataForm'));
        
        // 转换为对象以便处理
        const data = {
            name: document.getElementById('trackName').value,
            length: parseFloat(document.getElementById('trackLength').value),
            resistance: parseFloat(document.getElementById('resistance').value),
            inductance: parseFloat(document.getElementById('inductance').value),
            capacitance: parseFloat(document.getElementById('capacitance').value),
            frequency: parseFloat(document.getElementById('frequency').value),
            error_type: parseInt(document.getElementById('errorType').value)
        };
        
        // 模拟计算（这里可以替换为实际的API调用）
        // 实际使用时，这里应该是调用后端API
        const result = await simulateCalculation(data);
        
        // 显示结果
        let html = '<h3>计算结果</h3>';
        html += '<div class="card">';
        html += `<p><strong>轨道名称:</strong> ${result.name}</p>`;
        html += `<p><strong>轨道长度:</strong> ${result.length} m</p>`;
        html += `<p><strong>总阻抗:</strong> ${result.total_impedance.toFixed(6)} Ω</p>`;
        html += `<p><strong>总导纳:</strong> ${result.total_admittance.toFixed(6)} S</p>`;
        html += `<p><strong>传播系数:</strong> ${result.propagation_constant.toFixed(6)}</p>`;
        html += `<p><strong>特性阻抗:</strong> ${result.characteristic_impedance.toFixed(6)} Ω</p>`;
        html += `<p><strong>错误类型:</strong> ${result.error_type}</p>`;
        html += '</div>';
        
        resultDisplay.innerHTML = `<p class="success">✅ 数据计算成功！</p>${html}`;
    } catch (error) {
        resultDisplay.innerHTML = `<p class="error">❌ 计算失败: ${error.message}</p>`;
    }
}

// 模拟计算函数（实际应替换为API调用）
function simulateCalculation(data) {
    return new Promise(resolve => {
        setTimeout(() => {
            // 计算总阻抗
            const total_impedance = data.resistance + 1j * (2 * Math.PI * data.frequency * data.inductance) + 1 / (1j * (2 * Math.PI * data.frequency * data.capacitance));
            // 计算总导纳
            const total_admittance = 1 / total_impedance;
            // 计算传播系数
            const propagation_constant = Math.sqrt(total_impedance * total_admittance);
            // 计算特性阻抗
            const characteristic_impedance = Math.sqrt(total_impedance / total_admittance);
            
            resolve({
                name: data.name,
                value: 0,
                length: data.length,
                total_impedance: total_impedance,
                total_admittance: total_admittance,
                propagation_constant: propagation_constant,
                characteristic_impedance: characteristic_impedance,
                error_type: getErrorType(data.error_type)
            });
        }, 500);
    });
}

// 获取错误类型描述
function getErrorType(error_type) {
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
    return errorTypes[error_type] || "未知错误类型";
}

// 清除表单
function clearForm() {
    document.getElementById('dataForm').reset();
}