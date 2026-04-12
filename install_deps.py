#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装项目依赖
"""

import subprocess
import sys

print("开始安装依赖...")

# 安装requirements.txt中的依赖
print("安装requirements.txt中的依赖...")
try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        capture_output=True,
        text=True,
        check=True
    )
    print("requirements.txt安装成功:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("requirements.txt安装失败:")
    print(e.stdout)
    print(e.stderr)

# 安装pywebio
print("\n安装pywebio...")
try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "pywebio", "pywebio-battery"],
        capture_output=True,
        text=True,
        check=True
    )
    print("pywebio安装成功:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("pywebio安装失败:")
    print(e.stdout)
    print(e.stderr)

print("\n依赖安装完成！")
