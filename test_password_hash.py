#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试密码加密功能
"""

import requests
import json

# 测试服务器地址
BASE_URL = "http://127.0.0.1:8000"

def test_register(username, password):
    """测试注册功能"""
    print(f"\n=== 测试注册: {username} ===")
    url = f"{BASE_URL}/api/register"
    data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(url, data=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    return response.json()

def test_login(username, password):
    """测试登录功能"""
    print(f"\n=== 测试登录: {username} ===")
    url = f"{BASE_URL}/api/login"
    data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(url, data=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    return response.json()

def main():
    """主测试函数"""
    print("开始测试密码加密功能...")
    
    # 测试1: 注册新用户
    test_user = "test_user"
    test_password = "test1234"
    register_result = test_register(test_user, test_password)
    
    if register_result.get("status") == "success":
        # 测试2: 使用新用户登录
        login_result = test_login(test_user, test_password)
        
        if login_result.get("status") == "success":
            print("\n✅ 密码加密功能测试成功！")
        else:
            print("\n❌ 登录测试失败！")
    else:
        print("\n❌ 注册测试失败！")
    
    # 测试3: 测试现有用户（可能会失败，因为密码是明文）
    print("\n=== 测试现有用户登录 ===")
    existing_result = test_login("admin", "1234")
    if existing_result.get("status") == "success":
        print("✅ 现有用户登录成功（明文密码也能验证）")
    else:
        print("⚠️  现有用户登录失败（可能是因为密码是明文）")

if __name__ == "__main__":
    main()
