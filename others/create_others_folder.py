import os

# 创建others文件夹
others_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'others')
if not os.path.exists(others_dir):
    os.makedirs(others_dir)
    print(f"成功创建文件夹: {others_dir}")
else:
    print(f"文件夹已存在: {others_dir}")
