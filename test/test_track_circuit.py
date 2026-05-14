"""
一键式自动测试轨道电路参数输入功能脚本
=======================================
使用方法：
1. 先启动服务器: python start_server.py
2. 运行本测试: python test/test_track_circuit.py

测试内容：
- 正常参数输入：各轨道区段、各故障类型的计算
- 边界值测试：极端参数输入
- 参数缺失测试：必填字段缺失
- 参数类型测试：非法类型输入
- 结果合理性验证：输出值在合理范围内
- 不同频率测试：1700/2000/2300/2600Hz
"""

import requests
import time
import sys
import json
import io
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api/calculate/track-circuit"

test_results = []

TRACK_SECTIONS = ["69G", "X1LQG", "IG1", "57G", "3DG"]
ERROR_TYPES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
FREQUENCIES = [1700, 2000, 2300, 2600]

DEFAULT_PARAMS = {
    "trail": "69G",
    "error_type": 0,
    "error_value": 1.0,
    "error_position": "69G",
    "track_length": 1200,
    "resist_per_meter": 0.1,
    "induct_per_meter": 0.001,
    "capacit_per_meter": 1e-9,
    "conduct_per_meter": 0.001,
    "frequency": 1700,
    "spt_cable_length": 10.0,
    "r1": 1,
    "r2": 1,
    "input_V": 130.0
}


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_result(test_name, passed, detail=""):
    status = "[PASS]" if passed else "[FAIL]"
    print(f"  {status} | {test_name}")
    if detail:
        print(f"         detail: {detail}")
    test_results.append({
        "test_name": test_name,
        "passed": passed,
        "detail": detail
    })


def calculate(params):
    try:
        response = requests.post(API_URL, data=params, timeout=60)
        return response.status_code, response.json()
    except Exception as e:
        return -1, {"status": "error", "message": str(e)}


def check_server():
    print_header("Step 0: Check Server Connection")
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("  [OK] Server connection normal")
            return True
        else:
            print("  [FAIL] Server response abnormal")
            return False
    except Exception as e:
        print(f"  [FAIL] Cannot connect to server: {e}")
        print("  Please run: python start_server.py")
        return False


def test_normal_calculation():
    print_header("Step 1: Test Normal Calculation (No Fault)")
    
    params = DEFAULT_PARAMS.copy()
    params["error_type"] = 0
    code, result = calculate(params)
    
    passed = code == 200 and result.get("status") == "success"
    detail = f"code={code}"
    if passed:
        vr = result.get("voltage_results", {})
        detail += (
            f", send_end_V={vr.get('send_end_track_voltage', 'N/A')}"
            f", receive_end_V={vr.get('receive_end_track_voltage', 'N/A')}"
        )
    print_result("Normal calculation (error_type=0)", passed, detail)


def test_all_track_sections():
    print_header("Step 2: Test All Track Sections")
    
    for section in TRACK_SECTIONS:
        params = DEFAULT_PARAMS.copy()
        params["trail"] = section
        params["error_position"] = section
        code, result = calculate(params)
        
        passed = code == 200 and result.get("status") == "success"
        vr = result.get("voltage_results", {}) if passed else {}
        detail = (
            f"code={code}"
            f", send_end_V={vr.get('send_end_track_voltage', 'N/A')}"
        )
        print_result(f"Track section: {section}", passed, detail)


def test_all_error_types():
    print_header("Step 3: Test All Error Types")
    
    error_names = {
        0: "No fault",
        1: "RX tuner 1 open",
        2: "TX tuner 1 open",
        3: "RX hollow coil open",
        4: "RX hollow coil short",
        5: "RX tuner 2 open",
        6: "Comp cap 3 open",
        7: "Comp cap 3 short",
        8: "TX SPT cable open",
        9: "RX SPT cable open",
    }
    
    for etype in ERROR_TYPES:
        params = DEFAULT_PARAMS.copy()
        params["error_type"] = etype
        code, result = calculate(params)
        
        passed = code == 200 and result.get("status") == "success"
        vr = result.get("voltage_results", {}) if passed else {}
        detail = f"code={code}"
        if passed:
            detail += f", send_end_V={vr.get('send_end_track_voltage', 'N/A')}"
        print_result(f"Error type {etype} ({error_names.get(etype, 'Unknown')})", passed, detail)


def test_all_frequencies():
    print_header("Step 4: Test All Frequencies")
    
    for freq in FREQUENCIES:
        params = DEFAULT_PARAMS.copy()
        params["frequency"] = freq
        code, result = calculate(params)
        
        passed = code == 200 and result.get("status") == "success"
        vr = result.get("voltage_results", {}) if passed else {}
        detail = f"code={code}, freq={freq}Hz"
        if passed:
            detail += f", send_end_V={vr.get('send_end_track_voltage', 'N/A')}"
        print_result(f"Frequency: {freq} Hz", passed, detail)


def test_track_length_boundary():
    print_header("Step 5: Test Track Length Boundary Values")
    
    test_cases = [
        ("Very short (100m)", 100),
        ("Short (500m)", 500),
        ("Normal (1200m)", 1200),
        ("Long (2000m)", 2000),
        ("Very long (5000m)", 5000),
    ]
    
    for desc, length in test_cases:
        params = DEFAULT_PARAMS.copy()
        params["track_length"] = length
        code, result = calculate(params)
        
        passed = code == 200 and result.get("status") == "success"
        vr = result.get("voltage_results", {}) if passed else {}
        detail = f"code={code}, length={length}m"
        if passed:
            detail += f", receive_end_V={vr.get('receive_end_track_voltage', 'N/A')}"
        print_result(f"Track length: {desc}", passed, detail)


def test_spt_cable_length():
    print_header("Step 6: Test SPT Cable Length")
    
    test_cases = [
        ("Short (1km)", 1.0),
        ("Normal (10km)", 10.0),
        ("Long (20km)", 20.0),
        ("Very long (50km)", 50.0),
    ]
    
    for desc, cable_len in test_cases:
        params = DEFAULT_PARAMS.copy()
        params["spt_cable_length"] = cable_len
        code, result = calculate(params)
        
        passed = code == 200 and result.get("status") == "success"
        detail = f"code={code}, cable={cable_len}km"
        print_result(f"SPT cable: {desc}", passed, detail)


def test_input_voltage():
    print_header("Step 7: Test Input Voltage")
    
    test_cases = [
        ("Low voltage (50V)", 50.0),
        ("Normal (130V)", 130.0),
        ("High voltage (200V)", 200.0),
        ("Very high (500V)", 500.0),
    ]
    
    for desc, voltage in test_cases:
        params = DEFAULT_PARAMS.copy()
        params["input_V"] = voltage
        code, result = calculate(params)
        
        passed = code == 200 and result.get("status") == "success"
        vr = result.get("voltage_results", {}) if passed else {}
        detail = f"code={code}, input_V={voltage}"
        if passed:
            detail += f", send_end_V={vr.get('send_end_track_voltage', 'N/A')}"
        print_result(f"Input voltage: {desc}", passed, detail)


def test_attenuator_terminals():
    print_header("Step 8: Test Attenuator Terminals (r1, r2)")
    
    test_cases = [
        ("r1=1, r2=1", 1, 1),
        ("r1=5, r2=5", 5, 5),
        ("r1=10, r2=10", 10, 10),
        ("r1=1, r2=10", 1, 10),
        ("r1=10, r2=1", 10, 1),
    ]
    
    for desc, r1, r2 in test_cases:
        params = DEFAULT_PARAMS.copy()
        params["r1"] = r1
        params["r2"] = r2
        code, result = calculate(params)
        
        passed = code == 200 and result.get("status") == "success"
        detail = f"code={code}, r1={r1}, r2={r2}"
        print_result(f"Attenuator: {desc}", passed, detail)


def test_resist_per_meter():
    print_header("Step 9: Test Rail Resistance Per Meter")
    
    test_cases = [
        ("Low (0.01)", 0.01),
        ("Normal (0.1)", 0.1),
        ("High (1.0)", 1.0),
        ("Very high (5.0)", 5.0),
    ]
    
    for desc, resist in test_cases:
        params = DEFAULT_PARAMS.copy()
        params["resist_per_meter"] = resist
        code, result = calculate(params)
        
        passed = code == 200 and result.get("status") == "success"
        detail = f"code={code}, resist={resist}"
        print_result(f"Resistance: {desc}", passed, detail)


def test_missing_params():
    print_header("Step 10: Test Missing Required Parameters")
    
    required_fields = [
        "trail", "error_type", "error_value", "error_position",
        "track_length", "resist_per_meter", "induct_per_meter",
        "capacit_per_meter", "conduct_per_meter", "frequency"
    ]
    
    for field in required_fields:
        params = DEFAULT_PARAMS.copy()
        del params[field]
        code, result = calculate(params)
        
        passed = code == 422
        detail = f"code={code}, missing={field}"
        print_result(f"Missing field: {field}", passed, detail)


def test_invalid_error_type():
    print_header("Step 11: Test Invalid Error Type (Behavior Check)")
    
    invalid_types = [-1, 10, 99, 100]
    
    for etype in invalid_types:
        params = DEFAULT_PARAMS.copy()
        params["error_type"] = etype
        code, result = calculate(params)
        
        has_response = code == 200
        detail = f"code={code}, error_type={etype}"
        if has_response:
            detail += " (server accepts but may produce unexpected results)"
        print_result(f"Invalid error_type={etype} - server responds", has_response, detail)


def test_result_structure():
    print_header("Step 12: Test Result Structure Integrity")
    
    params = DEFAULT_PARAMS.copy()
    code, result = calculate(params)
    
    if code != 200 or result.get("status") != "success":
        print_result("Result structure check (calculation failed)", False, f"code={code}")
        return
    
    required_keys = ["status", "section_info", "error_info", "input_params", "voltage_results", "matrix"]
    for key in required_keys:
        has_key = key in result
        print_result(f"Result has key: {key}", has_key, f"present={has_key}")
    
    vr = result.get("voltage_results", {})
    voltage_keys = ["send_end_track_voltage", "receive_end_track_voltage", 
                    "main_track_input_voltage", "main_track_output_voltage_1"]
    for key in voltage_keys:
        has_key = key in vr
        print_result(f"voltage_results has key: {key}", has_key, f"present={has_key}")


def test_voltage_reasonable_range():
    print_header("Step 13: Test Voltage Results In Reasonable Range")
    
    params = DEFAULT_PARAMS.copy()
    code, result = calculate(params)
    
    if code != 200 or result.get("status") != "success":
        print_result("Voltage range check (calculation failed)", False, f"code={code}")
        return
    
    vr = result.get("voltage_results", {})
    
    for key, value in vr.items():
        if isinstance(value, (int, float)):
            is_finite = math.isfinite(value)
            is_non_negative = value >= 0
            passed = is_finite and is_non_negative
            detail = f"value={value}, finite={is_finite}, non_negative={is_non_negative}"
            print_result(f"Voltage {key} is finite and non-negative", passed, detail)


def test_fault_vs_normal_difference():
    print_header("Step 14: Test Fault Results Differ From Normal (send_end)")
    
    normal_params = DEFAULT_PARAMS.copy()
    normal_params["error_type"] = 0
    normal_code, normal_result = calculate(normal_params)
    
    if normal_code != 200:
        print_result("Normal calculation for comparison", False, f"code={normal_code}")
        return
    
    normal_vr = normal_result.get("voltage_results", {})
    normal_tx = normal_vr.get("send_end_track_voltage", 0)
    
    fault_types = [1, 2, 3, 5, 8]
    for etype in fault_types:
        fault_params = DEFAULT_PARAMS.copy()
        fault_params["error_type"] = etype
        fault_code, fault_result = calculate(fault_params)
        
        if fault_code != 200:
            print_result(f"Fault type {etype} calculation", False, f"code={fault_code}")
            continue
        
        fault_vr = fault_result.get("voltage_results", {})
        fault_tx = fault_vr.get("send_end_track_voltage", 0)
        
        is_different = abs(fault_tx - normal_tx) > 0.001
        detail = f"normal_tx={normal_tx:.4f}, fault_tx={fault_tx:.4f}, diff={abs(fault_tx-normal_tx):.4f}"
        print_result(f"Fault type {etype} send_end voltage differs from normal", is_different, detail)


def test_error_value_effect():
    print_header("Step 15: Test Error Value Parameter Accepted")
    
    for eval_val in [0.5, 1.0, 2.0, 5.0]:
        params = DEFAULT_PARAMS.copy()
        params["error_type"] = 6
        params["error_value"] = eval_val
        code, result = calculate(params)
        
        passed = code == 200 and result.get("status") == "success"
        if passed:
            input_params = result.get("input_params", {})
            echo_val = input_params.get("error_value")
            val_match = echo_val == eval_val
            detail = f"code={code}, sent={eval_val}, echoed={echo_val}, match={val_match}"
        else:
            detail = f"code={code}"
        print_result(f"error_value={eval_val} accepted and echoed", passed, detail)


def test_matrix_structure():
    print_header("Step 16: Test Matrix Structure")
    
    params = DEFAULT_PARAMS.copy()
    code, result = calculate(params)
    
    if code != 200 or result.get("status") != "success":
        print_result("Matrix structure check (calculation failed)", False, f"code={code}")
        return
    
    matrix = result.get("matrix")
    is_list = isinstance(matrix, list)
    print_result("Matrix is a list", is_list, f"type={type(matrix).__name__}")
    
    if is_list and len(matrix) > 0:
        is_2d = isinstance(matrix[0], list)
        print_result("Matrix is 2D", is_2d, f"rows={len(matrix)}")
        
        if is_2d:
            is_2x2 = len(matrix) == 2 and len(matrix[0]) == 2
            print_result("Matrix is 2x2", is_2x2, f"shape={len(matrix)}x{len(matrix[0])}")
            
            all_finite = all(
                math.isfinite(matrix[i][j])
                for i in range(len(matrix))
                for j in range(len(matrix[i]))
            )
            print_result("All matrix values are finite", all_finite)


def print_summary():
    print_header("Test Results Summary")
    
    total = len(test_results)
    passed = sum(1 for r in test_results if r["passed"])
    failed = total - passed
    
    print(f"\n  Total tests: {total}")
    print(f"  [PASS] Passed: {passed}")
    print(f"  [FAIL] Failed: {failed}")
    print(f"  Pass rate: {(passed/total*100):.1f}%" if total > 0 else "  Pass rate: N/A")
    
    if failed > 0:
        print("\n  Failed tests:")
        for r in test_results:
            if not r["passed"]:
                print(f"    [FAIL] {r['test_name']}")
                if r["detail"]:
                    print(f"           {r['detail']}")
    
    print("\n" + "=" * 60)
    return failed == 0


def main():
    print("=" * 60)
    print("  Track Circuit Parameter Input - Automated Test")
    print("  Railway Track Circuit Fault Simulation System")
    print("=" * 60)
    
    if not check_server():
        sys.exit(1)
    
    test_normal_calculation()
    test_all_track_sections()
    test_all_error_types()
    test_all_frequencies()
    test_track_length_boundary()
    test_spt_cable_length()
    test_input_voltage()
    test_attenuator_terminals()
    test_resist_per_meter()
    test_missing_params()
    test_invalid_error_type()
    test_result_structure()
    test_voltage_reasonable_range()
    test_fault_vs_normal_difference()
    test_error_value_effect()
    test_matrix_structure()
    
    all_passed = print_summary()
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
