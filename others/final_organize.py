import os
import shutil
import sys

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"当前工作目录: {current_dir}")

# 定义目标文件夹路径
others_dir = os.path.join(current_dir, 'others')
test_dir = os.path.join(current_dir, 'test')

# 1. 创建others文件夹
if not os.path.exists(others_dir):
    try:
        os.makedirs(others_dir)
        print(f"✅ 成功创建文件夹: others")
    except Exception as e:
        print(f"❌ 创建others文件夹失败: {e}")
else:
    print(f"📁 others文件夹已存在")

# 2. 移动用于整理文件的程序到others文件夹
organize_files = [
    'move_test_files.py',
    'organize_test_files.py',
    'resist_counter.py',
    'setup_env.py',
    'start_server.py',
    'work.txt'
]

print("\n移动整理文件程序到others文件夹:")
for file_name in organize_files:
    src_path = os.path.join(current_dir, file_name)
    dst_path = os.path.join(others_dir, file_name)
    
    if os.path.exists(src_path):
        try:
            shutil.move(src_path, dst_path)
            print(f"✅ 移动: {file_name} -> others/")
        except Exception as e:
            print(f"❌ 移动 {file_name} 失败: {e}")
    else:
        print(f"⚠️  文件不存在: {file_name}")

# 3. 移动测试用文件到test文件夹
test_files = [
    'test_circuit_tool.py',
    'test_safe_voltage_calc.py',
    'test_unit_conversion.py',
    'test_voltage_calculation.py'
]

print("\n移动测试文件到test文件夹:")
for file_name in test_files:
    src_path = os.path.join(current_dir, file_name)
    dst_path = os.path.join(test_dir, file_name)
    
    if os.path.exists(src_path):
        try:
            shutil.move(src_path, dst_path)
            print(f"✅ 移动: {file_name} -> test/")
        except Exception as e:
            print(f"❌ 移动 {file_name} 失败: {e}")
    else:
        print(f"⚠️  文件不存在: {file_name}")

# 4. 移动organize_files.py和create_others_folder.py到others文件夹
print("\n移动整理脚本到others文件夹:")
script_files = ['organize_files.py', 'create_others_folder.py', 'final_organize.py']
for file_name in script_files:
    src_path = os.path.join(current_dir, file_name)
    dst_path = os.path.join(others_dir, file_name)
    
    if os.path.exists(src_path):
        try:
            shutil.move(src_path, dst_path)
            print(f"✅ 移动: {file_name} -> others/")
        except Exception as e:
            print(f"❌ 移动 {file_name} 失败: {e}")
    else:
        print(f"⚠️  文件不存在: {file_name}")

print("\n📋 文件整理操作完成!")
print("\n📁 整理结果:")
print(f"- others文件夹: 存放用于整理文件的程序")
print(f"- test文件夹: 存放测试用文件")
