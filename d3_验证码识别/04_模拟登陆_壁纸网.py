import requests
import re
import os
from lxml import etree
from hashlib import md5

# 主方法
if __name__ == "__main__":
    url = 'https://wallhaven.cc/login'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Safari/537.36'
    }

    # post请求的发送-模拟登陆
    login_url = 'http://47.120.2.65:8989/user/login'

    # 用于用户的登陆的数据请求体
    data = {
        'userName': 'dong',
        'password': '1234'
    }

    login_page_text = requests.post(url=login_url, headers=headers, data=data).text
    print(login_page_text)

    with open('bizhi.html', 'w', encoding='utf-8') as fp:
        fp.write(login_page_text)
