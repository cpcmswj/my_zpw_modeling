import os
import shutil

# 定义路径
base_path = os.path.dirname(os.path.abspath(__file__))
others_dir = os.path.join(base_path, 'others')
test_dir = os.path.join(base_path, 'test')

# 创建others文件夹
if not os.path.exists(others_dir):
    os.makedirs(others_dir)
    print(f"创建文件夹: {others_dir}")
else:
    print(f"文件夹已存在: {others_dir}")

# 移动用于整理文件的程序到others文件夹
organize_files = [
    'move_test_files.py',
    'organize_test_files.py',
    'resist_counter.py',
    'setup_env.py',
    'start_server.py',
    'work.txt'
]

for file_name in organize_files:
    src_path = os.path.join(base_path, file_name)
    dst_path = os.path.join(others_dir, file_name)
    
    if os.path.exists(src_path):
        shutil.move(src_path, dst_path)
        print(f"移动文件: {file_name} -> others/")
    else:
        print(f"文件不存在: {file_name}")

# 移动测试用文件到test文件夹
test_files = [
    'test_circuit_tool.py',
    'test_safe_voltage_calc.py',
    'test_unit_conversion.py',
    'test_voltage_calculation.py'
]

for file_name in test_files:
    src_path = os.path.join(base_path, file_name)
    dst_path = os.path.join(test_dir, file_name)
    
    if os.path.exists(src_path):
        shutil.move(src_path, dst_path)
        print(f"移动文件: {file_name} -> test/")
    else:
        print(f"文件不存在: {file_name}")

print("\n文件整理完成！")
