"""
WSGI配置文件

用于将FastAPI应用部署到生产环境，支持Gunicorn等WSGI服务器。

使用方法：
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker wsgi:app

或者使用脚本启动：
    python wsgi.py
"""

from main import app as application

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1,
        loop="uvloop"
    )
