import jisuan_guidao

print("=== 测试查表函数 ===")
frequencies = [1700, 2000, 2300, 2600, 3000]

for freq in frequencies:
    print(f"\n频率: {freq}Hz")
    
    # 测试find_capacitance函数
    capacitance = jisuan_guidao.find_capacitance(freq)
    print(f"补偿电容: {capacitance}uF")
    
    # 测试find_transformer_ratio函数
    transformer_ratio = jisuan_guidao.find_transformer_ratio(freq)
    print(f"变压器变比: {transformer_ratio}")
    
    # 测试find_tuner_parameters函数
    tuner_params = jisuan_guidao.find_tuner_parameters(freq)
    print(f"调谐区参数: {tuner_params}")

print("\n=== 测试完成 ===")