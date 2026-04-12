import subprocess
import os

# 直接运行uvicorn服务器
subprocess.run(["python", "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])