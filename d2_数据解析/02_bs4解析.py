# 对象的的实例化
#   1 将本地的html文档中的数据加载到该对象中
#   2 将互联网上获取的页面源码加载到该对象中

from bs4 import BeautifulSoup
if __name__ == "__main__":
    # 将本地的html文档中的数据加载到该对象中
    fp = open('./r02.html', 'r', encoding='utf-8')
    soup = BeautifulSoup(fp, 'lxml')
    print(soup.select('.tang > ul > li')[0].text)
    print(soup.select('.tang > ul > li')[0].get_text())
    print(soup.select('.tang > ul > li')[0].string)


