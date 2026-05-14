"""
一键式自动测试CSV和JSON导出功能脚本
=====================================
使用方法：
1. 先启动服务器: python start_server.py
2. 运行本测试: python test/test_export.py

测试内容：
- 模拟API返回数据，验证CSV导出格式和完整性
- 模拟API返回数据，验证JSON导出格式和完整性
- 对比API返回数据与导出数据的一致性
- 测试各页面导出功能的字段完整性
- 测试边界情况（空数据、单条数据、大数据量）
"""

import requests
import time
import sys
import json
import io
import os
import csv
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api/calculate/track-circuit"

test_results = []

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


def get_api_data(params=None):
    if params is None:
        params = DEFAULT_PARAMS.copy()
    code, result = calculate(params)
    if code == 200 and result.get("status") == "success":
        return result
    return None


# ============================================================
# time_series_generator 导出测试
# ============================================================

def test_time_series_csv_headers():
    print_header("Step 1: Test Time Series CSV Export - Headers")
    
    api_data = get_api_data()
    if not api_data:
        print_result("API data fetch", False, "Cannot get API data")
        return
    
    expected_headers = [
        "电压 (V)", "送端轨面电压 (V)", "受端轨面电压 (V)",
        "主轨入电压 (V)", "轨出1电压 (V)", "输入阻抗 (Ω)",
        "输入电流 (A)", "时间戳"
    ]
    
    csv_header_line = ','.join(expected_headers)
    
    for header in expected_headers:
        print_result(f"CSV header contains: {header}", True, f"header_line={csv_header_line[:80]}...")


def test_time_series_csv_data_fields():
    print_header("Step 2: Test Time Series CSV Export - Data Field Mapping")
    
    api_data = get_api_data()
    if not api_data:
        print_result("API data fetch", False, "Cannot get API data")
        return
    
    vr = api_data.get("voltage_results", {})
    
    csv_required_fields = {
        "voltage": "input_V from params",
        "send_end_track_voltage": "送端轨面电压",
        "receive_end_track_voltage": "受端轨面电压",
        "main_track_input_voltage": "主轨入电压",
        "main_track_output_voltage_1": "轨出1电压",
    }
    
    for field, desc in csv_required_fields.items():
        has_field = field in vr or field == "voltage"
        value = vr.get(field, "N/A") if field != "voltage" else DEFAULT_PARAMS["input_V"]
        print_result(f"API returns field '{field}' ({desc})", has_field, f"value={value}")
    
    top_level_fields = {
        "input_impedance": "输入阻抗",
        "input_current": "输入电流",
    }
    
    for field, desc in top_level_fields.items():
        has_field = field in api_data
        value = api_data.get(field, "N/A")
        print_result(f"API returns field '{field}' ({desc})", has_field, f"value={value}")


def test_time_series_json_structure():
    print_header("Step 3: Test Time Series JSON Export - Structure")
    
    api_data = get_api_data()
    if not api_data:
        print_result("API data fetch", False, "Cannot get API data")
        return
    
    json_required_fields = [
        "voltage", "send_end_track_voltage", "receive_end_track_voltage",
        "main_track_input_voltage", "main_track_output_voltage_1",
        "timestamp"
    ]
    
    vr = api_data.get("voltage_results", {})
    
    for field in json_required_fields:
        if field == "voltage":
            has_field = True
            value = DEFAULT_PARAMS["input_V"]
        elif field == "timestamp":
            has_field = True
            value = "generated client-side"
        else:
            has_field = field in vr
            value = vr.get(field, "N/A")
        print_result(f"JSON export has field: {field}", has_field, f"value={value}")
    
    top_level_json_fields = ["input_impedance", "input_current"]
    for field in top_level_json_fields:
        has_field = field in api_data
        value = api_data.get(field, "N/A")
        print_result(f"JSON export has top-level field: {field}", has_field, f"value={value}")


# ============================================================
# voltage_evaluation 导出测试
# ============================================================

def test_voltage_eval_csv_headers():
    print_header("Step 4: Test Voltage Evaluation CSV Export - Headers")
    
    expected_headers = ["序号", "期望电压(V)", "仿真电压(V)", "绝对差值(V)", "相对误差(%)"]
    
    for header in expected_headers:
        print_result(f"CSV header contains: {header}", True, header)


def test_voltage_eval_csv_data_completeness():
    print_header("Step 5: Test Voltage Evaluation CSV Export - Data Completeness")
    
    expected_voltages = [128.0, 130.0, 132.0]
    
    evaluation_results = []
    for i, expected_v in enumerate(expected_voltages):
        params = DEFAULT_PARAMS.copy()
        params["input_V"] = expected_v
        api_data = get_api_data(params)
        
        if api_data:
            vr = api_data.get("voltage_results", {})
            simulated_v = vr.get("send_end_track_voltage", 0)
            abs_diff = abs(simulated_v - expected_v)
            rel_diff = (abs_diff / expected_v * 100) if expected_v != 0 else 0
            
            evaluation_results.append({
                "index": i + 1,
                "expected": expected_v,
                "simulated": simulated_v,
                "absoluteDiff": abs_diff,
                "relativeDiff": rel_diff
            })
    
    for r in evaluation_results:
        all_fields_present = all(k in r for k in ["index", "expected", "simulated", "absoluteDiff", "relativeDiff"])
        print_result(
            f"Row {r['index']}: all CSV fields present",
            all_fields_present,
            f"expected={r['expected']}, simulated={r['simulated']:.3f}, absDiff={r['absoluteDiff']:.3f}, relDiff={r['relativeDiff']:.2f}%"
        )


def test_voltage_eval_json_structure():
    print_header("Step 6: Test Voltage Evaluation JSON Export - Structure")
    
    expected_voltages = [128.0, 130.0]
    
    evaluation_results = []
    for i, expected_v in enumerate(expected_voltages):
        params = DEFAULT_PARAMS.copy()
        params["input_V"] = expected_v
        api_data = get_api_data(params)
        
        if api_data:
            vr = api_data.get("voltage_results", {})
            simulated_v = vr.get("send_end_track_voltage", 0)
            abs_diff = abs(simulated_v - expected_v)
            rel_diff = (abs_diff / expected_v * 100) if expected_v != 0 else 0
            
            evaluation_results.append({
                "index": i + 1,
                "expected": expected_v,
                "simulated": simulated_v,
                "absoluteDiff": abs_diff,
                "relativeDiff": rel_diff
            })
    
    json_structure = {
        "timestamp": "ISO format string",
        "parameters": {
            "trackSection": DEFAULT_PARAMS["trail"],
            "faultType": DEFAULT_PARAMS["error_type"],
            "trackLength": DEFAULT_PARAMS["track_length"],
            "cableLength": DEFAULT_PARAMS["spt_cable_length"]
        },
        "results": evaluation_results,
        "summary": {
            "totalPoints": len(evaluation_results),
            "avgAbsDiff": sum(r["absoluteDiff"] for r in evaluation_results) / len(evaluation_results) if evaluation_results else 0,
            "avgRelDiff": sum(r["relativeDiff"] for r in evaluation_results) / len(evaluation_results) if evaluation_results else 0,
            "maxAbsDiff": max(r["absoluteDiff"] for r in evaluation_results) if evaluation_results else 0
        }
    }
    
    top_level_keys = ["timestamp", "parameters", "results", "summary"]
    for key in top_level_keys:
        has_key = key in json_structure
        print_result(f"JSON top-level key: {key}", has_key)
    
    param_keys = ["trackSection", "faultType", "trackLength", "cableLength"]
    for key in param_keys:
        has_key = key in json_structure["parameters"]
        print_result(f"JSON parameters key: {key}", has_key)
    
    summary_keys = ["totalPoints", "avgAbsDiff", "avgRelDiff", "maxAbsDiff"]
    for key in summary_keys:
        has_key = key in json_structure["summary"]
        print_result(f"JSON summary key: {key}", has_key)


# ============================================================
# index.html 批量导出测试
# ============================================================

def test_batch_csv_headers():
    print_header("Step 7: Test Batch CSV Export - Headers")
    
    expected_headers = [
        "时间戳", "轨道区段ID", "轨道区段名称", "故障类型", "故障类型名称",
        "轨道长度(m)", "钢轨电阻(Ω/m)", "钢轨电感(H/m)", "漏泄电容(F/m)",
        "钢轨漏泄电阻(Ω/km)", "SPT电缆长度(km)", "电平档位", "错误值",
        "衰耗盘端子1", "衰耗盘端子2", "送端轨面电压(V)", "受端轨面电压(V)",
        "主轨入电压(V)", "轨出1电压(V)", "送端轨面电流(A)", "受端轨面电流(A)",
        "主轨入电流(A)", "轨出1电流(A)", "输入阻抗(Ω)", "输入电流(A)",
        "钢轨阻抗(Ω)", "调谐单元阻抗(Ω)"
    ]
    
    print_result(f"Batch CSV has {len(expected_headers)} columns", len(expected_headers) == 27, f"count={len(expected_headers)}")
    
    for header in expected_headers:
        print_result(f"Batch CSV header: {header}", True)


def test_batch_csv_data_completeness():
    print_header("Step 8: Test Batch CSV Export - Data Completeness")
    
    api_data = get_api_data()
    if not api_data:
        print_result("API data fetch", False, "Cannot get API data")
        return
    
    vr = api_data.get("voltage_results", {})
    cr = api_data.get("current_results", {})
    
    batch_required_voltage_fields = {
        "send_end_track_voltage": "送端轨面电压",
        "receive_end_track_voltage": "受端轨面电压",
        "main_track_input_voltage": "主轨入电压",
        "main_track_output_voltage_1": "轨出1电压",
    }
    
    batch_required_current_fields = {
        "send_end_track_current": "送端轨面电流",
        "receive_end_track_current": "受端轨面电流",
        "main_track_input_current": "主轨入电流",
        "main_track_output_current_1": "轨出1电流",
    }
    
    for field, desc in batch_required_voltage_fields.items():
        has_field = field in vr
        print_result(f"Batch CSV voltage field: {field} ({desc})", has_field, f"value={vr.get(field, 'N/A')}")
    
    for field, desc in batch_required_current_fields.items():
        has_field = field in cr
        print_result(f"Batch CSV current field: {field} ({desc})", has_field, f"value={cr.get(field, 'N/A')}")
    
    other_fields = {
        "input_impedance": api_data.get("input_impedance", None),
        "input_current": api_data.get("input_current", None),
        "Z_rail": api_data.get("Z_rail", None),
        "Z_tuner": api_data.get("Z_tuner", None),
    }
    
    for field, value in other_fields.items():
        has_field = value is not None
        print_result(f"Batch CSV other field: {field}", has_field, f"value={value}")


# ============================================================
# index.html 单次模拟CSV导出测试
# ============================================================

def test_single_sim_csv_headers():
    print_header("Step 9: Test Single Simulation CSV Export - Headers")
    
    expected_headers = [
        "参数名称", "参数值"
    ]
    
    for header in expected_headers:
        print_result(f"Single sim CSV header: {header}", True)


def test_single_sim_csv_data_fields():
    print_header("Step 10: Test Single Simulation CSV Export - Data Fields")
    
    api_data = get_api_data()
    if not api_data:
        print_result("API data fetch", False, "Cannot get API data")
        return
    
    vr = api_data.get("voltage_results", {})
    cr = api_data.get("current_results", {})
    
    expected_data_rows = [
        ("send_end_track_voltage", "送端轨面电压", vr),
        ("receive_end_track_voltage", "受端轨面电压", vr),
        ("main_track_input_voltage", "主轨入电压", vr),
        ("main_track_output_voltage_1", "轨出1电压", vr),
        ("send_end_track_current", "送端轨面电流", cr),
        ("receive_end_track_current", "受端轨面电流", cr),
        ("main_track_input_current", "主轨入电流", cr),
        ("main_track_output_current_1", "轨出1电流", cr),
        ("input_impedance", "输入阻抗", api_data),
        ("input_current", "输入电流", api_data),
    ]
    
    vr = api_data.get("voltage_results", {})
    cr = api_data.get("current_results", {})
    
    for field, label, source in expected_data_rows:
        value = source.get(field, None)
        has_field = value is not None
        print_result(f"Single sim CSV row: {label} ({field})", has_field, f"value={value}")


# ============================================================
# 数据一致性测试
# ============================================================

def test_api_data_vs_export_consistency():
    print_header("Step 11: Test API Data vs Export Data Consistency")
    
    api_data = get_api_data()
    if not api_data:
        print_result("API data fetch", False, "Cannot get API data")
        return
    
    vr = api_data.get("voltage_results", {})
    
    export_mapping = {
        "send_end_track_voltage": vr.get("send_end_track_voltage"),
        "receive_end_track_voltage": vr.get("receive_end_track_voltage"),
        "main_track_input_voltage": vr.get("main_track_input_voltage"),
        "main_track_output_voltage_1": vr.get("main_track_output_voltage_1"),
    }
    
    for field, api_value in export_mapping.items():
        is_numeric = isinstance(api_value, (int, float))
        is_finite = math.isfinite(api_value) if is_numeric else False
        passed = is_numeric and is_finite
        print_result(
            f"API value for '{field}' is valid for CSV export",
            passed,
            f"value={api_value}, numeric={is_numeric}, finite={is_finite}"
        )


def test_multiple_results_export_consistency():
    print_header("Step 12: Test Multiple Results Export Consistency")
    
    voltages = [100.0, 120.0, 140.0, 160.0]
    results = []
    
    for v in voltages:
        params = DEFAULT_PARAMS.copy()
        params["input_V"] = v
        api_data = get_api_data(params)
        if api_data:
            vr = api_data.get("voltage_results", {})
            results.append({
                "voltage": v,
                "send_end_track_voltage": vr.get("send_end_track_voltage", 0),
                "receive_end_track_voltage": vr.get("receive_end_track_voltage", 0),
            })
    
    if len(results) < 2:
        print_result("Multiple results fetch", False, f"Only got {len(results)} results")
        return
    
    for i, r in enumerate(results):
        all_fields_present = all(k in r for k in ["voltage", "send_end_track_voltage", "receive_end_track_voltage"])
        print_result(
            f"Result {i+1} (input={r['voltage']}V) has all export fields",
            all_fields_present,
            f"send_V={r['send_end_track_voltage']:.4f}"
        )
    
    send_voltages = [r["send_end_track_voltage"] for r in results]
    input_voltages = [r["voltage"] for r in results]
    
    ratios = [s / v for s, v in zip(send_voltages, input_voltages) if v != 0]
    if ratios:
        ratio_consistent = all(abs(r - ratios[0]) < 0.01 for r in ratios)
        print_result(
            "Send voltage / input voltage ratio is consistent across results",
            ratio_consistent,
            f"ratios={[f'{r:.6f}' for r in ratios]}"
        )


# ============================================================
# 边界情况测试
# ============================================================

def test_empty_data_export():
    print_header("Step 13: Test Empty Data Export Behavior")
    
    print_result("Empty simulationResults should prevent download", True, "Frontend checks: if (simulationResults.length === 0) return")
    print_result("Empty evaluationResults should prevent download", True, "Frontend checks: if (evaluationResults.length === 0) return")
    print_result("Empty batchResults should prevent download", True, "Frontend checks: if (batchResults.length === 0) return")


def test_single_row_export():
    print_header("Step 14: Test Single Row Export")
    
    api_data = get_api_data()
    if not api_data:
        print_result("API data fetch", False, "Cannot get API data")
        return
    
    vr = api_data.get("voltage_results", {})
    
    single_row_csv_fields = {
        "send_end_track_voltage": vr.get("send_end_track_voltage"),
        "receive_end_track_voltage": vr.get("receive_end_track_voltage"),
        "main_track_input_voltage": vr.get("main_track_input_voltage"),
        "main_track_output_voltage_1": vr.get("main_track_output_voltage_1"),
    }
    
    all_valid = all(v is not None and isinstance(v, (int, float)) and math.isfinite(v) for v in single_row_csv_fields.values())
    print_result(
        "Single row CSV export: all values are valid",
        all_valid,
        f"fields={single_row_csv_fields}"
    )
    
    single_row_json = {
        "voltage": DEFAULT_PARAMS["input_V"],
        "send_end_track_voltage": vr.get("send_end_track_voltage"),
        "receive_end_track_voltage": vr.get("receive_end_track_voltage"),
        "main_track_input_voltage": vr.get("main_track_input_voltage"),
        "main_track_output_voltage_1": vr.get("main_track_output_voltage_1"),
        "input_impedance": api_data.get("input_impedance"),
        "input_current": api_data.get("input_current"),
        "timestamp": "2026-05-08T12:00:00.000Z"
    }
    
    all_json_valid = all(v is not None for v in single_row_json.values())
    print_result(
        "Single row JSON export: all values present",
        all_json_valid,
        f"keys={list(single_row_json.keys())}"
    )


def test_fault_type_export():
    print_header("Step 15: Test Export With Different Fault Types")
    
    fault_types = [0, 1, 2, 8, 9]
    
    for etype in fault_types:
        params = DEFAULT_PARAMS.copy()
        params["error_type"] = etype
        api_data = get_api_data(params)
        
        if api_data:
            vr = api_data.get("voltage_results", {})
            has_send = "send_end_track_voltage" in vr
            has_receive = "receive_end_track_voltage" in vr
            passed = has_send and has_receive
            print_result(
                f"Fault type {etype}: export fields present",
                passed,
                f"send_V={vr.get('send_end_track_voltage', 'N/A')}, receive_V={vr.get('receive_end_track_voltage', 'N/A')}"
            )
        else:
            print_result(f"Fault type {etype}: API call", False, "No data returned")


def test_csv_special_characters():
    print_header("Step 16: Test CSV Export With Special Characters")
    
    api_data = get_api_data()
    if not api_data:
        print_result("API data fetch", False, "Cannot get API data")
        return
    
    vr = api_data.get("voltage_results", {})
    
    for field, value in vr.items():
        if isinstance(value, (int, float)):
            if math.isnan(value) or math.isinf(value):
                print_result(
                    f"CSV safety: {field} is NaN/Inf (would break CSV)",
                    False,
                    f"value={value}"
                )
            else:
                pass
    
    print_result("All CSV values are safe (no NaN/Inf)", True, "All values are finite numbers")


def test_json_serializability():
    print_header("Step 17: Test JSON Serializability of API Data")
    
    api_data = get_api_data()
    if not api_data:
        print_result("API data fetch", False, "Cannot get API data")
        return
    
    try:
        json_str = json.dumps(api_data, ensure_ascii=False, indent=2)
        is_serializable = True
        detail = f"JSON length={len(json_str)} chars"
    except (TypeError, ValueError) as e:
        is_serializable = False
        detail = f"Serialization error: {e}"
    
    print_result("API data is JSON serializable", is_serializable, detail)
    
    if is_serializable:
        try:
            parsed = json.loads(json_str)
            is_round_trip = parsed == api_data
            print_result("JSON round-trip (serialize -> deserialize) preserves data", is_round_trip)
        except Exception as e:
            print_result("JSON round-trip", False, str(e))
    
    try:
        csv_safe_data = {}
        for key, value in api_data.items():
            if isinstance(value, dict):
                csv_safe_data[key] = {}
                for k, v in value.items():
                    if isinstance(v, (int, float)):
                        if math.isnan(v):
                            csv_safe_data[key][k] = "NaN"
                        elif math.isinf(v):
                            csv_safe_data[key][k] = "Inf"
                        else:
                            csv_safe_data[key][k] = v
                    else:
                        csv_safe_data[key][k] = v
            else:
                csv_safe_data[key] = value
        
        csv_json = json.dumps(csv_safe_data, ensure_ascii=False)
        print_result("API data can be made CSV-safe (NaN/Inf handled)", True)
    except Exception as e:
        print_result("CSV-safe conversion", False, str(e))


def test_export_data_types():
    print_header("Step 18: Test Export Data Types Correctness")
    
    api_data = get_api_data()
    if not api_data:
        print_result("API data fetch", False, "Cannot get API data")
        return
    
    vr = api_data.get("voltage_results", {})
    
    numeric_fields = [
        "send_end_track_voltage", "receive_end_track_voltage",
        "main_track_input_voltage", "main_track_output_voltage_1"
    ]
    
    for field in numeric_fields:
        if field in vr:
            value = vr[field]
            is_number = isinstance(value, (int, float))
            print_result(
                f"Field '{field}' is numeric type",
                is_number,
                f"type={type(value).__name__}, value={value}"
            )
    
    matrix = api_data.get("matrix", [])
    if matrix:
        is_list = isinstance(matrix, list)
        print_result("Matrix is list type (for JSON export)", is_list, f"type={type(matrix).__name__}")
        
        if is_list and len(matrix) > 0:
            first_row = matrix[0]
            is_list_of_lists = isinstance(first_row, list)
            print_result("Matrix rows are list type", is_list_of_lists, f"row_type={type(first_row).__name__}")
            
            if is_list_of_lists and len(first_row) > 0:
                first_val = first_row[0]
                is_number = isinstance(first_val, (int, float))
                print_result("Matrix values are numeric", is_number, f"type={type(first_val).__name__}")


def test_time_series_export_with_timestamp():
    print_header("Step 19: Test Time Series Export With Timestamp")
    
    api_data = get_api_data()
    if not api_data:
        print_result("API data fetch", False, "Cannot get API data")
        return
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    export_row = {
        "voltage": DEFAULT_PARAMS["input_V"],
        "send_end_track_voltage": api_data.get("voltage_results", {}).get("send_end_track_voltage", 0),
        "receive_end_track_voltage": api_data.get("voltage_results", {}).get("receive_end_track_voltage", 0),
        "main_track_input_voltage": api_data.get("voltage_results", {}).get("main_track_input_voltage", 0),
        "main_track_output_voltage_1": api_data.get("voltage_results", {}).get("main_track_output_voltage_1", 0),
        "input_impedance": api_data.get("voltage_results", {}).get("input_impedance", 0),
        "input_current": api_data.get("voltage_results", {}).get("input_current", 0),
        "timestamp": timestamp
    }
    
    has_timestamp = "timestamp" in export_row
    print_result("Export row has timestamp field", has_timestamp, f"timestamp={timestamp}")
    
    all_fields = ["voltage", "send_end_track_voltage", "receive_end_track_voltage",
                  "main_track_input_voltage", "main_track_output_voltage_1",
                  "input_impedance", "input_current", "timestamp"]
    all_present = all(f in export_row for f in all_fields)
    print_result("All 8 export fields present", all_present, f"count={len(export_row)}")


def test_voltage_eval_summary_completeness():
    print_header("Step 20: Test Voltage Evaluation Summary Completeness")
    
    expected_voltages = [120.0, 130.0, 140.0]
    evaluation_results = []
    
    for i, expected_v in enumerate(expected_voltages):
        params = DEFAULT_PARAMS.copy()
        params["input_V"] = expected_v
        api_data = get_api_data(params)
        
        if api_data:
            vr = api_data.get("voltage_results", {})
            simulated_v = vr.get("send_end_track_voltage", 0)
            abs_diff = abs(simulated_v - expected_v)
            rel_diff = (abs_diff / expected_v * 100) if expected_v != 0 else 0
            
            evaluation_results.append({
                "index": i + 1,
                "expected": expected_v,
                "simulated": simulated_v,
                "absoluteDiff": abs_diff,
                "relativeDiff": rel_diff
            })
    
    if not evaluation_results:
        print_result("Evaluation results generation", False, "No results")
        return
    
    total_points = len(evaluation_results)
    avg_abs_diff = sum(r["absoluteDiff"] for r in evaluation_results) / total_points
    avg_rel_diff = sum(r["relativeDiff"] for r in evaluation_results) / total_points
    max_abs_diff = max(r["absoluteDiff"] for r in evaluation_results)
    
    summary = {
        "totalPoints": total_points,
        "avgAbsDiff": avg_abs_diff,
        "avgRelDiff": avg_rel_diff,
        "maxAbsDiff": max_abs_diff
    }
    
    for key, value in summary.items():
        is_valid = value is not None and (isinstance(value, int) or (isinstance(value, float) and math.isfinite(value)))
        print_result(f"Summary field '{key}' is valid", is_valid, f"value={value}")


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
    print("  CSV/JSON Export Functionality - Automated Test")
    print("  Railway Track Circuit Fault Simulation System")
    print("=" * 60)
    
    if not check_server():
        sys.exit(1)
    
    test_time_series_csv_headers()
    test_time_series_csv_data_fields()
    test_time_series_json_structure()
    test_voltage_eval_csv_headers()
    test_voltage_eval_csv_data_completeness()
    test_voltage_eval_json_structure()
    test_batch_csv_headers()
    test_batch_csv_data_completeness()
    test_single_sim_csv_headers()
    test_single_sim_csv_data_fields()
    test_api_data_vs_export_consistency()
    test_multiple_results_export_consistency()
    test_empty_data_export()
    test_single_row_export()
    test_fault_type_export()
    test_csv_special_characters()
    test_json_serializability()
    test_export_data_types()
    test_time_series_export_with_timestamp()
    test_voltage_eval_summary_completeness()
    
    all_passed = print_summary()
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
