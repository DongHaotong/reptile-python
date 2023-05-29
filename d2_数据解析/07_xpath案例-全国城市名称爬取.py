# 全国城市的名称
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

    url = 'http://www.aqistudy.cn/historydata/'
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)

    # 获取热门城市的名称
    li_list = tree.xpath("//div[@class='bottom']/ul/li")
    print("热门城市有：")
    for li in li_list:
        hot_city_name = li.xpath("./a/text()")[0]

    # 获取所有城市的城市名称
    li_list = tree.xpath("//div[@class='all']/div[@class='bottom']/ul/div[2]/li")
    for li in li_list:
        city_name = li.xpath("./a/text()")[0]
        print(city_name)
