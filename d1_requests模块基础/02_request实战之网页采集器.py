

# UA检测 ：门户网站的服务器会检测对应请求的载体身份标识，如果检测到请求的载体身份标识
#         为某一款浏览器。说明该请求是一个正常的请求，但是如果检测到请求的载体身份
#         标识不是基于某一款浏览器的，则标识该请求为不正常的请求(爬虫),则服务器端就
#         很可能拒绝该次请求。
# UA ：User-Agent(请求载体的身份标识)
# UA伪装：让爬虫对应的请求载体身份标识伪装成一款浏览器


import requests
# UA伪装：将对应的User-Agent封装到一个字典中
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

url = 'https://www.sogou.com/web'
# 处理url携带的参数：封装到数据字典中
kw = input('enter a word:')
param = {
    'query': kw
}

response = requests.get(url=url, params=param, headers=headers)
page_text = response.text

fileName = kw + '02.html'
with open(fileName, 'w', encoding='utf-8') as fp:
    fp.write(page_text)

print(fileName, '保存成功！！！')
