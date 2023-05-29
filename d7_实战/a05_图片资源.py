import os

import requests
from lxml import etree
import re

url = f'https://fulitu.me/group/senluocaituan-2.html'
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

# xpath解析图片的地址
tree = etree.HTML(page_text)
# 获取图片的最终地址
collections = tree.xpath('/html/body/div[2]/div[2]/div/ul/li')

# 创建总文件夹
if not os.path.exists('./z05_森萝'):
    os.mkdir('./z05_森萝')

# 遍历每一个合集，获取合集的详情页面和主题
for item in collections:
    # 详细地址
    item_href = 'https://fulitu.me' + item.xpath('./a/@href')[0]
    # 访问详细页面
    item_page_text = requests.get(url=item_href, headers=headers).text
    tree = etree.HTML(item_page_text)
    # 解析出文章的标题，用作文件夹的名称
    item_page_title = tree.xpath('/html/body/div[2]/div/div/div[1]/h1/text()')[0]

    # 创建子文件夹
    if not os.path.exists('./z05_森萝/' + item_page_title):
        os.mkdir('./z05_森萝/' + item_page_title)

    # 获取所有的a标签，也就是获得所有的页链接
    item_page_index = tree.xpath('/html/body/div[2]/div/div/div[4]/div/div/a')
    # 标记下载图片的序号
    index = 1
    for page_index_item in item_page_index:
        page_index_item_path = 'https://fulitu.me' + page_index_item.xpath('./@href')[0]
        # 获取当前页码的页面数据
        current_page_text = requests.get(url=page_index_item_path, headers=headers).text
        tree = etree.HTML(current_page_text)
        item_page = tree.xpath('//img[@alt="内部"]/@src')
        for current_img in item_page:
            # 图片的二进制数据
            current_img_content = requests.get(url=current_img, headers=headers).content

            # 对图片进行保存
            # 图片的保存路径
            img_save_path = 'z05_森萝/' + item_page_title + '/' + str(index) + '.jpg'

            with open(img_save_path, 'wb') as fp:
                fp.write(current_img_content)
                print(item_page_title, ":", index, "-->爬取成功!!!")

            index = index + 1
