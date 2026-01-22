"""
WSGI配置文件

用于将FastAPI应用部署到Apache mod_wsgi或其他WSGI服务器。

使用方法：
    将此文件配置到你的WSGI服务器中，例如Apache的httpd.conf或virtualhost配置。
"""

# 添加当前目录到Python路径
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 从main.py导入FastAPI应用
from main import app as application

# 确保日志配置正确
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("WSGI应用已加载")
