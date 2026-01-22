#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动服务器并打开页面脚本

用于快速启动FastAPI服务器并在浏览器中打开各个页面。

使用方法：
    python start_server.py               # 启动服务器并打开所有页面
    python start_server.py index         # 启动服务器并只打开首页
    python start_server.py fsk_signal    # 启动服务器并只打开FSK信号页面
    python start_server.py --help        # 查看帮助信息
"""

import argparse
import subprocess
import webbrowser
import time
import os
import sys

# 定义页面映射
define_pages = {
    'index': 'http://127.0.0.1:8000/',
    'image_viewer': 'http://127.0.0.1:8000/image-viewer',
    'section_image': 'http://127.0.0.1:8000/section-image-viewer',
    'integrated': 'http://127.0.0.1:8000/integrated-system',
    'comparison': 'http://127.0.0.1:8000/comparison-system',
    'fsk_signal': 'http://127.0.0.1:8000/fsk-signal-viewer',
    'test_image': 'http://127.0.0.1:8000/test-image'
}

def start_server():
    """启动Uvicorn服务器"""
    print("正在启动FastAPI服务器...")
    try:
        # 启动Uvicorn服务器，使用默认事件循环
        cmd = [
            sys.executable,
            "-m", "uvicorn",
            "main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--workers", "1",
            "--log-level", "info"
        ]
        
        # 在后台启动服务器
        server_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待服务器启动
        time.sleep(2)
        
        # 检查服务器是否启动成功
        if server_process.poll() is not None:
            print("❌ 服务器启动失败！")
            stdout, stderr = server_process.communicate()
            print(f"错误信息：{stderr}")
            return None
        
        print("✅ 服务器已成功启动！")
        print(f"服务器地址：http://127.0.0.1:8000/")
        print("要停止服务器，请按 Ctrl+C 或关闭终端窗口")
        print("=" * 50)
        
        return server_process
        
    except Exception as e:
        print(f"❌ 启动服务器时出错：{e}")
        return None

def open_pages(pages_to_open):
    """打开指定的页面
    
    参数：
        pages_to_open: list, 要打开的页面列表
    """
    print(f"\n正在打开 {len(pages_to_open)} 个页面...")
    
    for page_name in pages_to_open:
        if page_name in define_pages:
            url = define_pages[page_name]
            print(f"🔗 打开页面：{page_name} -> {url}")
            webbrowser.open(url)
            time.sleep(0.5)  # 延迟打开，避免浏览器冲突
        else:
            print(f"❌ 未知页面：{page_name}")
    
    print("✅ 所有页面已打开！")
    print("=" * 50)

def show_help():
    """显示帮助信息"""
    print("快速启动服务器并打开页面脚本")
    print("=" * 50)
    print("使用方法：")
    print("    python start_server.py [页面名称1] [页面名称2] ...")
    print("\n可用页面：")
    for page, url in define_pages.items():
        print(f"    {page:15} -> {url}")
    print("\n示例：")
    print("    python start_server.py               # 打开所有页面")
    print("    python start_server.py index         # 只打开首页")
    print("    python start_server.py fsk_signal integrated  # 打开多个页面")
    print("=" * 50)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="快速启动服务器并打开页面脚本",
        add_help=False
    )
    
    # 添加帮助选项
    parser.add_argument(
        '-h', '--help',
        action='store_true',
        help='显示帮助信息'
    )
    
    # 添加页面参数
    parser.add_argument(
        'pages',
        nargs='*',
        help='要打开的页面名称'
    )
    
    args = parser.parse_args()
    
    # 显示帮助信息
    if args.help:
        show_help()
        return
    
    # 启动服务器
    server_process = start_server()
    if not server_process:
        return
    
    # 确定要打开的页面
    pages_to_open = args.pages if args.pages else list(define_pages.keys())
    
    # 打开页面
    open_pages(pages_to_open)
    
    # 等待用户输入，保持程序运行
    try:
        print("\n服务器正在运行中...")
        print("按 Ctrl+C 停止服务器")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n正在停止服务器...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("✅ 服务器已停止！")

if __name__ == "__main__":
    main()
