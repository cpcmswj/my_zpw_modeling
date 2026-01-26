import shutil
import os

# 定义源文件和目标目录
source_files = [
    'test_api.py',
    'test_api_all_faults.py',
    'test_random_parameters.py'
]
target_dir = 'test/'

# 确保目标目录存在
os.makedirs(target_dir, exist_ok=True)

# 移动文件
for file in source_files:
    if os.path.exists(file):
        try:
            shutil.move(file, os.path.join(target_dir, file))
            print(f"✅ 已移动文件: {file} -> {target_dir}")
        except Exception as e:
            print(f"❌ 移动文件失败 {file}: {e}")
    else:
        print(f"⚠️ 文件不存在: {file}")

print("\n文件整理完成！")