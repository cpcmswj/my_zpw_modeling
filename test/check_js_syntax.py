# 检查JavaScript代码的语法

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
    
    # 简单的语法检查
    # 检查是否有未闭合的括号、引号等
    print("\n语法检查结果：")
    
    # 检查括号
    brackets = [
        ("()", "圆括号"),
        ("{}", "花括号"),
        ("[]", "方括号")
    ]
    
    for bracket, name in brackets:
        count = js_code.count(bracket[0]) - js_code.count(bracket[1])
        if count > 0:
            print(f"警告：有 {count} 个未闭合的{name} ({bracket[0]})")
        elif count < 0:
            print(f"警告：有 {-count} 个多余的{name} ({bracket[1]})")
        else:
            print(f"✅ {name}匹配正常")
    
    # 检查引号
    double_quotes = js_code.count('"')
    single_quotes = js_code.count("'")
    print(f"双引号数量：{double_quotes}")
    print(f"单引号数量：{single_quotes}")
    
    # 检查是否有未闭合的字符串
    if double_quotes % 2 != 0:
        print("警告：可能有未闭合的双引号字符串")
    if single_quotes % 2 != 0:
        print("警告：可能有未闭合的单引号字符串")
    
    # 检查是否有未闭合的注释
    if js_code.count('/*') != js_code.count('*/'):
        print("警告：可能有未闭合的多行注释")
    
    # 检查是否有未闭合的模板字符串
    if js_code.count('`') % 2 != 0:
        print("警告：可能有未闭合的模板字符串")
    
    # 检查是否有未闭合的正则表达式
    # 这是一个简单的检查，可能不准确
    regex_count = js_code.count('/') - js_code.count('//') - js_code.count('/*') - js_code.count('*/')
    if regex_count % 2 != 0:
        print("警告：可能有未闭合的正则表达式")
    
    print("\n检查完成")
else:
    print("未找到JavaScript代码")