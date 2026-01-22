import requests

# 测试阻抗计算API
def test_impedance_calculation():
    print("测试阻抗计算API...")
    url = "http://127.0.0.1:8000/api/calculate/impedance"
    data = {
        "resist": 100,
        "induct": 0.01,
        "capacit": 0.00001,
        "angular_frequency": 2 * 3.14159 * 50  # 50Hz
    }
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {result}")
        
        # 验证是否包含复数形式
        if "impedance_complex" in result["result"]:
            print("✅ 阻抗包含复数形式")
        
        return result
    except Exception as e:
        print(f"测试失败: {e}")
        return None

# 测试导纳计算API
def test_admittance_calculation():
    print("\n测试导纳计算API...")
    url = "http://127.0.0.1:8000/api/calculate/admittance"
    data = {
        "resist": 100,
        "induct": 0.01,
        "capacit": 0.00001,
        "angular_frequency": 2 * 3.14159 * 50  # 50Hz
    }
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {result}")
        
        # 验证是否包含复数形式
        if "admittance_complex" in result["result"]:
            print("✅ 导纳包含复数形式")
        
        return result
    except Exception as e:
        print(f"测试失败: {e}")
        return None

# 测试变量计算API
def test_variable_calculation():
    print("\n测试变量计算API...")
    url = "http://127.0.0.1:8000/api/calculate/variable"
    data = {
        "name": "test_variable",
        "value": 100,
        "length_guidao": 1000,
        "resist_per_meter": 0.01,
        "induct_per_meter": 1e-6,
        "capacit_per_meter": 1e-9
    }
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {result}")
        
        # 验证复数形式是否正确包含
        complex_fields = ["impedance", "admittance", "gamma", "Z_c"]
        all_passed = True
        for field in complex_fields:
            if field in result["result"] and "complex" in result["result"][field]:
                print(f"✅ {field} 包含复数形式")
            else:
                print(f"❌ {field} 缺少复数形式")
                all_passed = False
        
        if all_passed:
            print("✅ 所有参数都包含复数形式")
        
        return result
    except Exception as e:
        print(f"测试失败: {e}")
        return None

if __name__ == "__main__":
    print("开始测试FastAPI API端点...\n")
    
    # 运行所有测试
    test_impedance_calculation()
    test_admittance_calculation()
    test_variable_calculation()
    
    print("\n所有测试完成！")
