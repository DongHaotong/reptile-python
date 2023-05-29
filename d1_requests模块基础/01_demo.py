# 爬去搜狗首页的页面数据

import requests

# 1. 指定url
url = "https://www.sogou.com/"

# 2. 发起请求
# get方法会返回一个响应对象
response = requests.get(url=url)

# 3. 获取响应数据
# .text返回的是字符串形式的响应数据
text = response.text
print(text)

# 4. 持久化存储
with open('sogou.html', 'w', encoding='utf-8') as fp:
    fp.write(text)

print('爬取数据结束!!!')

