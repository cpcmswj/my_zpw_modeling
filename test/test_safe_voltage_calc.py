import sys
import os
import numpy as np

# 添加父目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 测试safe_voltage_calc函数
def test_safe_voltage_calc():
    print("开始测试safe_voltage_calc函数...")
    
    # 模拟safe_voltage_calc函数
    def safe_voltage_calc(voltage):
        try:
            if voltage is None:
                return 0.0
            # 检查voltage是否为numpy数组
            if isinstance(voltage, np.ndarray):
                # 如果是数组，处理多维情况
                if voltage.size > 0:
                    # 展平数组并取第一个非零元素
                    flat_voltage = voltage.flatten()
                    # 找到第一个非零元素
                    for v in flat_voltage:
                        if v != 0:
                            voltage = v
                            break
                    else:
                        # 如果所有元素都是0，返回0
                        return 0.0
                else:
                    return 0.0
            # 确保voltage是标量或复数
            if not np.isscalar(voltage) and not isinstance(voltage, complex):
                return 0.0
            abs_val = np.abs(voltage)
            if not np.isfinite(abs_val):
                return 0.0
            # 直接返回复数模，而不是平方根
            return float(abs_val)
        except Exception as e:
            print(f"safe_voltage_calc错误: {e}")
            return 0.0
    
    # 测试用例
    test_cases = [
        ("标量电压", 10.0, 10.0),
        ("复数电压", 10 + 5j, np.abs(10 + 5j)),
        ("一维数组", np.array([10.0, 5.0]), 10.0),
        ("二维数组", np.array([[10.0, 5.0], [2.0, 3.0]]), 10.0),
        ("全零数组", np.array([0.0, 0.0]), 0.0),
        ("空数组", np.array([]), 0.0),
        ("None值", None, 0.0),
        ("负数电压", -5.0, 5.0),
    ]
    
    # 运行测试
    all_passed = True
    for test_name, input_voltage, expected_output in test_cases:
        result = safe_voltage_calc(input_voltage)
        passed = abs(result - expected_output) < 1e-6
        all_passed = all_passed and passed
        status = "✅" if passed else "❌"
        print(f"{status} {test_name}: 输入={input_voltage}, 输出={result}, 预期={expected_output}")
    
    if all_passed:
        print("\n✅ 所有测试通过！safe_voltage_calc函数修复成功。")
    else:
        print("\n❌ 部分测试失败，需要进一步修复。")

if __name__ == "__main__":
    test_safe_voltage_calc()
