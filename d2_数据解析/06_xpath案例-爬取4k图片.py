# 爬58同城二手房信息的主题
import requests
import os
from lxml import etree

if __name__ == "__main__":
    # 进行UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Safari/537.36'
    }

    url = 'https://pic.netbian.com/4kmeinv/'

    # 处理中文数据乱码问题
    response = requests.get(url=url, headers=headers)
    response.encoding = 'gbk'
    page_text = response.text

    # 数据解析：src属性值 alt属性
    tree = etree.HTML(page_text)
    li_list = tree.xpath("//div[@class='slist']/ul/li")

    # 创建一个文件夹
    if not os.path.exists('./r06-pic'):
        os.mkdir('./r06-pic')

    for li in li_list:
        img_path = 'https://pic.netbian.com' + li.xpath("./a/img/@src")[0]
        img_name = li.xpath('./a/img/@alt')[0] + '.jpg'
        # 数据持久化存储
        img_data = requests.get(url=img_path, headers=headers).content
        img_path = 'r06-pic/' + img_name
        with open(img_path, 'wb') as fp:
            fp.write(img_data)
            print(img_name + "-->爬取成功!!!")

