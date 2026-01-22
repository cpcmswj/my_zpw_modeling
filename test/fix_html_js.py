# 修复HTML文件中的JavaScript代码

# 读取HTML文件内容
with open('templates/image_viewer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取JavaScript代码
import re
js_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if js_match:
    js_code = js_match.group(1)
    print("提取的JavaScript代码：")
    print(js_code[:200] + "...")
    
    # 检查JavaScript代码的语法
    # 这里我们简单地检查一下常见的语法错误
    lines = js_code.split('\n')
    for i, line in enumerate(lines):
        # 检查是否有未闭合的引号
        if line.count('"') % 2 != 0 or line.count("'") % 2 != 0:
            print(f"第 {i+1} 行可能有未闭合的引号：{line.strip()}")
        # 检查是否有未闭合的括号
        if line.count('(') != line.count(')') or line.count('{') != line.count('}'):
            print(f"第 {i+1} 行可能有未闭合的括号：{line.strip()}")
        # 检查是否有未闭合的方括号
        if line.count('[') != line.count(']'):
            print(f"第 {i+1} 行可能有未闭合的方括号：{line.strip()}")
    
    # 重新生成HTML文件
    # 我们将使用之前测试过的JavaScript代码来替换HTML文件中的JavaScript代码
    with open('test_js.js', 'r', encoding='utf-8') as f:
        fixed_js = f.read()
    
    # 替换HTML文件中的JavaScript代码
    fixed_content = re.sub(r'<script>(.*?)</script>', f'<script>{fixed_js}</script>', content, flags=re.DOTALL)
    
    # 保存修复后的HTML文件
    with open('templates/image_viewer_fixed.html', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("已生成修复后的HTML文件：templates/image_viewer_fixed.html")
else:
    print("未找到JavaScript代码")