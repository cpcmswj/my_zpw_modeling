import os
import shutil

# 定义要移动的文件列表
test_files = [
    'test_api.py',
    'test_api_all_faults.py',
    'test_random_parameters.py'
]

# 定义源目录和目标目录
source_dir = r'c:\Users\阳\Documents\trae_projects\py_bishe'
dest_dir = r'c:\Users\阳\Documents\trae_projects\py_bishe\test'

# 确保目标目录存在
os.makedirs(dest_dir, exist_ok=True)

# 移动文件
for file in test_files:
    source_path = os.path.join(source_dir, file)
    dest_path = os.path.join(dest_dir, file)
    
    if os.path.exists(source_path):
        shutil.move(source_path, dest_path)
        print(f'✓ 已移动: {file} -> test/{file}')
    else:
        print(f'✗ 文件不存在: {file}')

print('\n所有文件移动完成！')