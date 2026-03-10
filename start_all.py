#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动所有服务
包括：
1. FastAPI服务器（端口8000）
2. PyWebIO应用（端口8080）
"""
import pywebio
import subprocess
import time
import webbrowser
import os

# 启动FastAPI服务器
def start_fastapi():
    """启动FastAPI服务器"""
    print("启动FastAPI服务器...")
    # 使用uvicorn启动FastAPI应用
    subprocess.Popen(["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

# 启动PyWebIO应用
def start_pywebio():
    """启动PyWebIO应用"""
    print("启动PyWebIO应用...")
    # 运行pywebio_app.py
    subprocess.Popen(["python", "pywebio_app.py"])

# 打开浏览器
def open_browsers():
    """打开浏览器"""
    time.sleep(2)  # 等待服务器启动
    print("打开浏览器...")
    # 打开FastAPI主页
    webbrowser.open("http://localhost:8000")
    # 打开PyWebIO应用
    webbrowser.open("http://localhost:8081")

if __name__ == "__main__":
    print("开始启动所有服务...")
    
    # 启动FastAPI服务器
    start_fastapi()
    
    # 启动PyWebIO应用
    start_pywebio()
    
    # 打开浏览器
    open_browsers()
    
    print("所有服务启动完成！")
    print("FastAPI服务器: http://localhost:8000")
    print("PyWebIO应用: http://localhost:8081")
    print("按Ctrl+C停止所有服务")
    
    # 保持脚本运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("正在停止服务...")
        print("服务已停止")
