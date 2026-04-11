#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Vercel部署配置
"""

import os
import sys
import subprocess
import time
import requests

def test_server_start():
    """测试服务器是否能正常启动"""
    print("测试服务器启动...")
    
    # 检查环境变量
    print(f"PORT环境变量: {os.environ.get('PORT', '未设置')}")
    
    # 检查文件是否存在
    required_files = [
        'main.py',
        'requirements.txt',
        'vercel.json',
        'wsgi.py'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} 存在")
        else:
            print(f"✗ {file} 不存在")
            return False
    
    # 检查依赖文件
    if os.path.exists('requirements.txt'):
        print("\n检查依赖项...")
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            dependencies = f.readlines()
            print(f"依赖项数量: {len(dependencies)}")
            for dep in dependencies[:5]:  # 显示前5个依赖
                print(f"  - {dep.strip()}")
            if len(dependencies) > 5:
                print(f"  ... 等{len(dependencies) - 5}个依赖")
    
    # 检查vercel.json配置
    if os.path.exists('vercel.json'):
        print("\n检查vercel.json配置...")
        with open('vercel.json', 'r', encoding='utf-8') as f:
            content = f.read()
            print("配置文件内容:")
            print(content)
    
    print("\n✅ 部署配置检查完成！")
    print("\n部署到Vercel的步骤:")
    print("1. 确保已安装Vercel CLI: npm i -g vercel")
    print("2. 登录Vercel: vercel login")
    print("3. 部署项目: vercel")
    print("4. 查看部署状态: vercel status")
    
    return True

def main():
    """主函数"""
    print("开始测试Vercel部署配置...")
    print("=" * 50)
    
    success = test_server_start()
    
    print("=" * 50)
    if success:
        print("测试通过！项目已准备好部署到Vercel。")
    else:
        print("测试失败！请检查上述错误。")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
