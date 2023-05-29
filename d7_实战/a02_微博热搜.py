import os

import requests
from lxml import etree
import re

url = 'https://tophub.today/n/KqndgxeLl9'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/111.0.0.0 Safari/537.36'
}
page_text = requests.get(url=url, headers=headers).text

tree = etree.HTML(page_text)
tr_list = tree.xpath('//*[@id="page"]/div[2]/div[2]/div[1]/div[2]/div/div[1]/table/tbody/tr')
i = 1
for tr in tr_list:
    content = tr.xpath('./td[2]/a/text()')[0]  # 标题
    hot = tr.xpath('./td[3]/text()')[0]  # 热度
    print(i, ':', content, '-->', hot)
    i = i + 1

