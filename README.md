# FastAPI 交互式 Web 应用

这是一个基于 FastAPI 框架构建的交互式 Web 应用，设计用于部署到 PythonAnywhere 等平台。

## 项目特点

- 🚀 **高性能**：基于 FastAPI 框架，提供异步支持
- 🎨 **交互式**：包含动态网页，可与后端 API 进行实时交互
- 📱 **响应式设计**：适配不同屏幕尺寸
- 📚 **完整的 API 文档**：自动生成 Swagger UI 和 ReDoc 文档
- 📦 **易于部署**：包含完整的依赖管理和部署指南

## 技术栈

- **后端框架**：FastAPI 0.128.0
- **编程语言**：Python 3.14
- **前端技术**：HTML5、CSS3、JavaScript（原生）
- **模板引擎**：Jinja2
- **Web 服务器**：Uvicorn

## 项目结构

```
.
├── main.py              # FastAPI 应用主文件
├── requirements.txt     # 项目依赖
├── templates/           # HTML 模板目录
│   └── index.html       # 主页面模板
├── static/              # 静态文件目录
└── README.md            # 项目说明文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动开发服务器

```bash
uvicorn main:app --reload
```

应用将在 `http://127.0.0.1:8000` 运行。

### 3. 访问应用

- **主页面**：`http://127.0.0.1:8000`
- **API 文档**：`http://127.0.0.1:8000/docs`（Swagger UI）
- **ReDoc 文档**：`http://127.0.0.1:8000/redoc`

## API 端点

### 1. 获取数据

```
GET /api/data
```

返回示例：
```json
{
  "message": "Hello from FastAPI!",
  "status": "success",
  "data": {
    "items": ["item1", "item2", "item3"],
    "count": 3
  }
}
```

### 2. 获取特定项目

```
GET /api/items/{item_id}?q={query}
```

参数：
- `item_id`：项目 ID（整数）
- `q`：可选查询参数（字符串）

返回示例：
```json
{
  "item_id": 1,
  "q": "测试参数",
  "description": "This is item 1"
}
```

## 部署到 PythonAnywhere

### 1. 准备工作

1. 在 PythonAnywhere 上创建一个账户
2. 创建一个新的 Web 应用（选择 "Manual Configuration"，Python 3.10+）

### 2. 上传代码

使用 PythonAnywhere 的文件管理器或 Git 上传项目文件到服务器。

### 3. 安装依赖

在 PythonAnywhere 的 Bash 控制台中运行：

```bash
cd /home/your_username/your_project_name
pip install -r requirements.txt
```

### 4. 配置 WSGI 文件

编辑 PythonAnywhere 提供的 WSGI 配置文件（通常位于 `/var/www/your_username_pythonanywhere_com_wsgi.py`）：

```python
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).resolve().parent))

from main import app

# 确保使用 asgi_application 而不是 application
application = app
```

### 5. 重启 Web 应用

在 PythonAnywhere 控制面板中重启 Web 应用。

### 6. 访问应用

应用将在 `https://your_username.pythonanywhere.com` 可用。

## 开发指南

### 添加新的 API 端点

在 `main.py` 文件中添加新的路由：

```python
@app.get("/api/new_endpoint")
async def new_endpoint():
    return {"message": "This is a new endpoint"}
```

### 修改前端页面

编辑 `templates/index.html` 文件，添加或修改 HTML、CSS 或 JavaScript 代码。

### 添加静态文件

将静态文件（如 CSS、JavaScript、图片）放在 `static` 目录中，然后在模板中引用：

```html
<link rel="stylesheet" href="{{ url_for('static', path='/styles.css') }}">
<script src="{{ url_for('static', path='/script.js') }}"></script>
```

## 测试

### 手动测试

使用浏览器访问应用，或使用工具如 Postman 测试 API 端点。

### 自动测试

可以使用 pytest 进行自动化测试：

```bash
pip install pytest httpx
pytest tests/
```

## 许可证

MIT License

## 贡献

欢迎提交问题和拉取请求！
