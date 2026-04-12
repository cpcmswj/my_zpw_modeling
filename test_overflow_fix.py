from templates.error_of_trail import Error_Of_Trail

# 创建Error_Of_Trail实例
error_instance = Error_Of_Trail('test', 0, 0, '69G', 1000, 10)

# 调用build_circuit_model方法，这应该会触发之前的溢出错误
print("开始测试build_circuit_model...")
result = error_instance.build_circuit_model()
print("测试完成，没有溢出错误！")

# 调用call_matrix_main方法，这也可能会触发溢出错误
print("\n开始测试call_matrix_main...")
result = error_instance.call_matrix_main()
print("测试完成，没有溢出错误！")

print("\n所有测试通过，溢出问题已解决！")
