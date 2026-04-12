import csv

with open('static/username_code.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    print('CSV文件内容:')
    for row in reader:
        print(f'  username: {repr(row.get("username"))}')
        print(f'  code: {repr(row.get("code"))}')
        print(f'  类型: username={type(row.get("username"))}, code={type(row.get("code"))}')
