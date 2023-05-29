import os

import requests
from lxml import etree
import re

# 页面为
page = 2
for page in range(2, 10):
    url = f'http://www.netbian.com/meinv/index_{page}.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Safari/537.36'
    }
    page_text = requests.get(url=url, headers=headers)
    # 设置编码为页面的编码
    page_text.encoding = page_text.apparent_encoding
    # 转换为文本形式
    page_text = page_text.text

    # 利用正则数据解析
    obj = re.compile('<a href="(?P<img_path>.*?)" title=".*?" target="_blank"><img src=".*?" alt="(?P<img_title>.*?)" '
                     '/><b>.*?</b></a>')
    result = obj.finditer(page_text)

    # 持久化存储
    if not os.path.exists('./z03_壁纸'):
        os.mkdir('./z03_壁纸')

    for item in result:
        dic = item.groupdict()
        # 壁纸的详情页面
        img_path = 'http://www.netbian.com' + dic['img_path']
        # 壁纸的主题
        img_title = dic['img_title']
        # 请求图片的详情页面
        img_page_text = requests.get(url=img_path, headers=headers)
        img_page_text.encoding = img_page_text.apparent_encoding
        img_page_text = img_page_text.text
        # xpath解析图片的地址
        tree = etree.HTML(img_page_text)
        # 获取图片的最终地址
        img_src = tree.xpath('//*[@id="main"]/div[3]/div/p/a/img/@src')[0]
        # 请求下载
        img_content = requests.get(url=img_src, headers=headers).content
        img_save_path = 'z03_壁纸/' + img_title + '.jpg'

        with open(img_save_path, 'wb') as fp:
            fp.write(img_content)
            print(img_title + "-->爬取成功!!!")





