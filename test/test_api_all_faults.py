import requests

# API端点URL
url = 'http://localhost:8000/api/calculate/track-circuit'

# 基础表单数据
base_data = {
    'trail': 'test',
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

# 故障类型列表
error_types = [
    (0, "无故障"),
    (1, "接收端调谐单元1断路"),
    (2, "发送端调谐单元1断路"),
    (3, "接收端空心线圈断路"),
    (4, "接收端空芯线圈短路"),
    (5, "接收端调谐单元2断路"),
    (6, "补偿电容3断路"),
    (7, "补偿电容3短路")
]

print("=== 测试所有故障类型的API响应 ===")
print(f"API端点: {url}")
print("\n基础参数:")
for key, value in base_data.items():
    if key != 'error_type':  # 排除error_type，因为我们会单独测试
        print(f"  {key}: {value}")

print("\n" + "="*50)

success_count = 0
failure_count = 0

for error_type, error_name in error_types:
    print(f"\n测试故障类型 {error_type}: {error_name}")
    print("-" * 30)
    
    # 构建完整的数据
    data = base_data.copy()
    data['error_type'] = error_type
    
    try:
        # 发送POST请求
        response = requests.post(url, data=data)
        
        # 打印响应状态码
        print(f"响应状态码: {response.status_code}")
        
        # 尝试解析JSON响应
        response_data = response.json()
        print(f"响应状态: {response_data.get('status')}")
        
        if response.status_code == 200 and response_data.get('status') == 'success':
            print("✅ 测试成功！")
            success_count += 1
        else:
            print(f"❌ 测试失败: {response_data.get('message')}")
            failure_count += 1
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        failure_count += 1

print("\n" + "="*50)
print("=== 测试结果汇总 ===")
print(f"总测试次数: {len(error_types)}")
print(f"成功次数: {success_count}")
print(f"失败次数: {failure_count}")

if failure_count == 0:
    print("\n🎉 所有测试都成功了！API修复完成。")
else:
    print(f"\n⚠️  有 {failure_count} 个测试失败，需要进一步修复。")