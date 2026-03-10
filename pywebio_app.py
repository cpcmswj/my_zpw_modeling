#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用PyWebIO创建的轨道电路故障模拟系统
包含故障模拟和批量故障模拟两个功能模块
"""

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio_battery import *
import webbrowser
import threading
import time
import os

# 全局变量
global_modules = {}

def open_browser(url):
    """在新线程中打开浏览器"""
    def _open_browser():
        time.sleep(1)  # 等待服务器启动
        webbrowser.open(url)
    threading.Thread(target=_open_browser).start()

def fault_simulation():
    """故障模拟功能模块"""
    put_markdown("## 轨道电路故障模拟")
    
    # 这里可以复制integrated_system.html中的功能
    put_text("故障模拟功能开发中...")
    put_button("打开原始故障模拟页面", onclick=lambda: webbrowser.open("http://localhost:8000/integrated-system"))

def batch_simulation():
    """批量故障模拟功能模块"""
    put_markdown("## 批量故障模拟")
    
    # 这里可以复制batch_simulation.html中的功能
    put_text("批量故障模拟功能开发中...")
    put_button("打开原始批量模拟页面", onclick=lambda: webbrowser.open("http://localhost:8000/batch-simulation"))

def select_module(module):
    """处理模块选择"""
    clear(scope="content")
    with use_scope("content"):
        if module == "fault":
            fault_simulation()
        elif module == "batch":
            batch_simulation()

def main():
    """主函数"""
    put_markdown("# 轨道电路故障模拟系统")
    put_text("使用PyWebIO构建的轨道电路故障模拟系统，包含故障模拟和批量故障模拟两个功能模块。")
    
    # 创建内容区域
    with use_scope("content"):
        put_markdown("## 欢迎使用轨道电路故障模拟系统")
        put_text("请从右侧悬浮窗选择功能模块。")
    
    # 注册回调函数
    from pywebio.session import register_callback
    register_callback('select_module', select_module)
    
    # 创建悬浮窗
    put_html('''
    <div style="position: fixed; top: 20px; right: 20px; width: 200px; background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); z-index: 1000;">
        <h3 style="margin-top: 0; color: #3498db;">功能选择</h3>
        <button onclick="pywebio.call('select_module', 'fault')" style="width: 100%; margin-bottom: 10px; padding: 10px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer;">故障模拟</button>
        <button onclick="pywebio.call('select_module', 'batch')" style="width: 100%; padding: 10px; background: #27ae60; color: white; border: none; border-radius: 4px; cursor: pointer;">批量故障模拟</button>
    </div>
    ''')
    
    # 保持会话
    hold()



if __name__ == "__main__":
    # 启动服务器
    port = 8081
    url = f"http://localhost:{port}"
    print(f"启动PyWebIO服务器，访问地址: {url}")
    open_browser(url)
    start_server(main, port=port, debug=True)
