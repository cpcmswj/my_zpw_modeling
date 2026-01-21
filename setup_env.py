#!/usr/bin/env python
"""
环境配置脚本 - 帮助在Trae中快速设置Python环境
"""

import os
import sys
import subprocess


def run_command(cmd):
    """运行命令并返回结果"""
    print(f"执行命令: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"退出码: {result.returncode}")
    if result.stdout:
        print(f"输出: {result.stdout}")
    if result.stderr:
        print(f"错误: {result.stderr}")
    return result.returncode


def setup_venv():
    """设置虚拟环境"""
    print("\n=== 设置Python虚拟环境 ===")
    
    # 检查Python是否可用
    if run_command("python --version") != 0:
        print("Python不可用，尝试使用py命令...")
        python_cmd = "py"
        if run_command("py --version") != 0:
            print("错误: Python未安装或未添加到环境变量")
            return False
    else:
        python_cmd = "python"
    
    # 创建虚拟环境
    if os.path.exists("venv"):
        print("虚拟环境已存在，跳过创建")
    else:
        if run_command(f"{python_cmd} -m venv venv") != 0:
            print("错误: 创建虚拟环境失败")
            return False
    
    # 激活虚拟环境并安装依赖
    print("\n=== 安装依赖 ===")
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    # 使用pip安装依赖
    pip_cmd = f"{python_cmd} -m pip"
    if run_command(f"{pip_cmd} install --upgrade pip") != 0:
        print("警告: 更新pip失败")
    
    if os.path.exists("requirements.txt"):
        if run_command(f"{pip_cmd} install -r requirements.txt") != 0:
            print("警告: 安装依赖失败")
    else:
        print("警告: requirements.txt文件不存在")
    
    print("\n=== 环境配置完成 ===")
    print("\n使用说明:")
    print("1. 激活虚拟环境:")
    print(f"   - {activate_cmd}")
    print("2. 运行示例脚本:")
    print("   - python example_numpy.py")
    print("3. 退出虚拟环境:")
    print("   - deactivate")
    
    return True


if __name__ == "__main__":
    setup_venv()