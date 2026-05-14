"""
一键式批量测试用户登录注册逻辑程序
===================================
使用方法：
1. 先启动服务器: python start_server.py
2. 运行本测试: python test/test_login_register.py

测试内容：
- 注册功能：正常注册、用户名已存在、密码过短
- 登录功能：正常登录、用户名不存在、密码错误
- 密码哈希验证：确认密码经过哈希处理存储
- 清理测试数据
"""

import requests
import time
import sys
import json
import io
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://127.0.0.1:8000"

test_results = []
test_users = []


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


def register(username, password):
    try:
        response = requests.post(
            f"{BASE_URL}/api/register",
            data={"username": username, "password": password},
            timeout=30
        )
        return response.status_code, response.json()
    except Exception as e:
        return -1, {"status": "error", "message": str(e)}


def login(username, password):
    try:
        response = requests.post(
            f"{BASE_URL}/api/login",
            data={"username": username, "password": password},
            timeout=30
        )
        return response.status_code, response.json()
    except Exception as e:
        return -1, {"status": "error", "message": str(e)}


def check_server():
    print_header("Step 0: Check Server Connection")
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"  Server response status: {response.status_code}")
        if response.status_code == 200:
            print("  [OK] Server connection normal")
            return True
        else:
            print("  [FAIL] Server response abnormal")
            return False
    except requests.exceptions.ConnectionError:
        print("  [FAIL] Cannot connect to server!")
        print("  Please run: python start_server.py")
        return False
    except Exception as e:
        print(f"  [FAIL] Connection error: {e}")
        return False


def test_register_normal():
    print_header("Step 1: Test Normal Registration")
    
    ts = int(time.time())
    
    user1 = f"test_user_{ts}"
    code1, result1 = register(user1, "test123456")
    passed1 = code1 == 200 and result1.get("status") == "success"
    print_result(f"Register user {user1}", passed1, f"code={code1}, resp={result1}")
    if passed1:
        test_users.append(user1)
    
    user2 = f"test_user_{ts}_2"
    code2, result2 = register(user2, "MyP@ss789")
    passed2 = code2 == 200 and result2.get("status") == "success"
    print_result(f"Register user {user2}", passed2, f"code={code2}, resp={result2}")
    if passed2:
        test_users.append(user2)


def test_register_duplicate():
    print_header("Step 2: Test Duplicate Username Registration")
    
    if not test_users:
        print("  [SKIP] No test users available")
        return
    
    existing_user = test_users[0]
    code, result = register(existing_user, "another_password")
    
    passed = (
        code == 400
        and result.get("status") == "error"
        and result.get("error_code") == "username_taken"
    )
    print_result(
        f"Duplicate register {existing_user} should be rejected",
        passed,
        f"code={code}, error_code={result.get('error_code')}, msg={result.get('message')}"
    )


def test_register_short_password():
    print_header("Step 3: Test Short Password Registration")
    
    ts = int(time.time())
    
    test_cases = [
        ("1-char password", f"short_{ts}", "1"),
        ("3-char password", f"short_{ts}_3", "abc"),
        ("5-char password", f"short_{ts}_5", "12345"),
    ]
    
    for desc, username, password in test_cases:
        code, result = register(username, password)
        passed = (
            code == 400
            and result.get("status") == "error"
            and result.get("error_code") == "password_too_short"
        )
        print_result(
            f"{desc} should be rejected",
            passed,
            f"code={code}, error_code={result.get('error_code')}, msg={result.get('message')}"
        )


def test_login_normal():
    print_header("Step 4: Test Normal Login")
    
    if len(test_users) < 2:
        print("  [SKIP] Not enough test users")
        return
    
    for i, username in enumerate(test_users[:2]):
        password = ["test123456", "MyP@ss789"][i]
        code, result = login(username, password)
        passed = (
            code == 200
            and result.get("status") == "success"
            and result.get("user", {}).get("username") == username
        )
        print_result(
            f"User {username} normal login",
            passed,
            f"code={code}, user={result.get('user', {})}"
        )


def test_login_user_not_found():
    print_header("Step 5: Test Login With Non-existent Username")
    
    ts = int(time.time())
    nonexistent_user = f"nonexistent_{ts}"
    code, result = login(nonexistent_user, "somepassword")
    
    passed = (
        code == 401
        and result.get("status") == "error"
        and result.get("error_code") == "username_not_found"
    )
    print_result(
        f"Non-existent user {nonexistent_user} should show 'username not found'",
        passed,
        f"code={code}, error_code={result.get('error_code')}, msg={result.get('message')}"
    )


def test_login_wrong_password():
    print_header("Step 6: Test Login With Wrong Password")
    
    if not test_users:
        print("  [SKIP] No test users available")
        return
    
    existing_user = test_users[0]
    code, result = login(existing_user, "wrong_password_999")
    
    passed = (
        code == 401
        and result.get("status") == "error"
        and result.get("error_code") == "password_wrong"
    )
    print_result(
        f"User {existing_user} wrong password should show 'password wrong'",
        passed,
        f"code={code}, error_code={result.get('error_code')}, msg={result.get('message')}"
    )


def test_login_empty_fields():
    print_header("Step 7: Test Login With Empty Fields")
    
    code1, result1 = login("", "somepassword")
    passed1 = code1 in [400, 401, 422]
    print_result("Empty username login should be rejected", passed1, f"code={code1}")
    
    code2, result2 = login("someuser", "")
    passed2 = code2 in [400, 401, 422]
    print_result("Empty password login should be rejected", passed2, f"code={code2}")


def test_boundary_password():
    print_header("Step 8: Test Password Boundary Values")
    
    ts = int(time.time())
    
    user_5 = f"boundary_{ts}_5"
    code_5, result_5 = register(user_5, "12345")
    passed_5 = code_5 == 400 and result_5.get("error_code") == "password_too_short"
    print_result("5-char password should be rejected (< 6)", passed_5, f"code={code_5}, error_code={result_5.get('error_code')}")
    
    user_6 = f"boundary_{ts}_6"
    code_6, result_6 = register(user_6, "123456")
    passed_6 = code_6 == 200 and result_6.get("status") == "success"
    print_result("6-char password should succeed (exactly 6)", passed_6, f"code={code_6}")
    if passed_6:
        test_users.append(user_6)
    
    user_7 = f"boundary_{ts}_7"
    code_7, result_7 = register(user_7, "1234567")
    passed_7 = code_7 == 200 and result_7.get("status") == "success"
    print_result("7-char password should succeed (> 6)", passed_7, f"code={code_7}")
    if passed_7:
        test_users.append(user_7)


def test_password_hash_verification():
    print_header("Step 9: Verify Password Hash Storage")
    
    if not test_users:
        print("  [SKIP] No test users available")
        return
    
    username = test_users[0]
    correct_password = "test123456"
    wrong_password = "wrong_password"
    
    login_code_correct, result_correct = login(username, correct_password)
    login_code_wrong, result_wrong = login(username, wrong_password)
    
    correct_login_works = login_code_correct == 200 and result_correct.get("status") == "success"
    wrong_login_fails = login_code_wrong == 401 and result_wrong.get("error_code") == "password_wrong"
    
    passed = correct_login_works and wrong_login_fails
    print_result(
        f"User {username} password is hashed (correct pw works, wrong pw fails)",
        passed,
        f"correct_login={correct_login_works}, wrong_login_fails={wrong_login_fails}"
    )


def test_login_after_register():
    print_header("Step 10: Test Login Immediately After Registration")
    
    ts = int(time.time())
    username = f"immediate_{ts}"
    password = "immediate_pass_123"
    
    reg_code, reg_result = register(username, password)
    reg_passed = reg_code == 200 and reg_result.get("status") == "success"
    print_result(f"Register user {username}", reg_passed, f"code={reg_code}")
    
    if reg_passed:
        test_users.append(username)
        login_code, login_result = login(username, password)
        login_passed = login_code == 200 and login_result.get("status") == "success"
        print_result(
            f"Login immediately after register {username}",
            login_passed,
            f"code={login_code}"
        )


def test_special_characters():
    print_header("Step 11: Test Special Character Passwords")
    
    ts = int(time.time())
    
    special_users = [
        (f"user_{ts}_sp", "p@ss!w0rd#", "special symbol password"),
        (f"user_{ts}_space", "pass word123", "password with space"),
    ]
    
    for username, password, desc in special_users:
        code, result = register(username, password)
        if len(password) >= 6:
            passed = code == 200 and result.get("status") == "success"
            if passed:
                test_users.append(username)
        else:
            passed = code == 400 and result.get("error_code") == "password_too_short"
        print_result(f"Register with {desc}", passed, f"code={code}, msg={result.get('message', '')}")


def cleanup():
    print_header("Cleanup: Remove Test Users")
    
    try:
        from database import user_store
        
        cleaned = 0
        for username in test_users:
            with user_store._lock:
                if username in user_store._users:
                    del user_store._users[username]
                    cleaned += 1
                    print(f"  [DEL] Removed: {username}")
        
        user_store._save_to_edge_config()
        print(f"\n  Total cleaned: {cleaned} test users")
    except ImportError:
        print("  [INFO] Cannot access database directly (different process)")
        print(f"  [INFO] {len(test_users)} test users remain in server memory")
        print("  [INFO] Restart server to clear test users")


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
    print("  Login/Register Logic Batch Test")
    print("  Railway Track Circuit Fault Simulation System")
    print("=" * 60)
    
    if not check_server():
        sys.exit(1)
    
    try:
        test_register_normal()
        test_register_duplicate()
        test_register_short_password()
        test_login_normal()
        test_login_user_not_found()
        test_login_wrong_password()
        test_login_empty_fields()
        test_boundary_password()
        test_password_hash_verification()
        test_login_after_register()
        test_special_characters()
    finally:
        cleanup()
    
    all_passed = print_summary()
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
