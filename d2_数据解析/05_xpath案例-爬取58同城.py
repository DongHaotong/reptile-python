# 爬58同城二手房信息的主题
import requests
from lxml import etree

if __name__ == "__main__":
    # 进行UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Safari/537.36'
    }

    url = 'https://bj.58.com/ershoufang/'

    page_text = requests.get(url=url, headers=headers).text

    # 数据解析
    tree = etree.HTML(page_text)
    div_list = tree.xpath('//section[@class="list"]/div')

    for temp in div_list:
        # 局部解析，一定要加'./'
        title = temp.xpath("./a//h3[@class='property-content-title-name']/text()")[0]
        print(title)
