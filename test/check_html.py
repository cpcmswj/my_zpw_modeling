# 检查HTML文件中的特殊字符

with open('templates/image_viewer.html', 'rb') as f:
    content = f.read()

# 检查是否有BOM（Byte Order Mark）
if content.startswith(b'\xef\xbb\xbf'):
    print("文件有BOM字符")
    # 移除BOM
    content = content[3:]
    with open('templates/image_viewer.html', 'wb') as f:
        f.write(content)
    print("已移除BOM字符")
else:
    print("文件没有BOM字符")

# 检查是否有其他特殊字符
print("\n检查特殊字符：")
for i, byte in enumerate(content[:100]):
    if byte < 32 and byte not in [9, 10, 13]:  # 排除制表符、换行符、回车符
        print(f"位置 {i}: 特殊字符 {byte}")

# 检查HTML标签是否正确闭合
print("\n检查HTML结构：")
from html.parser import HTMLParser

class TagCounter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []
        self.errors = []
    
    def handle_starttag(self, tag, attrs):
        # 忽略自闭合标签
        self_closing = tag in ['br', 'img', 'input', 'meta', 'link', 'hr']
        if not self_closing:
            self.tag_stack.append(tag)
    
    def handle_endtag(self, tag):
        if not self.tag_stack:
            self.errors.append(f"多余的结束标签：{tag}")
        else:
            last_tag = self.tag_stack.pop()
            if last_tag != tag:
                self.errors.append(f"标签不匹配：预期 {last_tag}，得到 {tag}")
    
    def check(self):
        if self.tag_stack:
            self.errors.extend([f"未闭合的标签：{tag}" for tag in self.tag_stack])
        return self.errors

parser = TagCounter()
parser.feed(content.decode('utf-8'))
errors = parser.check()

if errors:
    for error in errors:
        print(f"错误：{error}")
else:
    print("HTML标签结构正确")