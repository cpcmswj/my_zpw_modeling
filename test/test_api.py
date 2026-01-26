import requests

# API端点URL
url = 'http://localhost:8000/api/calculate/track-circuit'

# 表单数据
data = {
    'trail': 'test',
    'error_type': 0,
    'error_value': 0,
    'error_position': '69G',
    'track_length': 100,
    'resist_per_meter': 0.1,
    'induct_per_meter': 1.0e-3,
    'capacit_per_meter': 1.0e-9,
    'conduct_per_meter': 0.0,
    'spt_cable_length': 10.0,
    'frequency': 1700
}

print("正在测试API...")
print(f"请求URL: {url}")
print(f"请求数据: {data}")

try:
    # 发送POST请求
    response = requests.post(url, data=data)
    
    # 打印响应状态码
    print(f"\n响应状态码: {response.status_code}")
    
    # 打印响应内容
    print("响应内容:")
    print(response.json())
    
    print("\n✅ API测试成功！")
except Exception as e:
    print(f"\n❌ API测试失败: {e}")
    import traceback
    traceback.print_exc()