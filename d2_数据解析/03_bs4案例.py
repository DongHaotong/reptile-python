# 爬取三国演义小说所有的章节标题和章节内容
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    # 进行UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Safari/537.36'
    }
    # 三国小说的地址
    url = 'https://sanguo.5000yan.com/'

    page_text = requests.get(url=url, headers=headers).content.decode()

    # 在首页中解析出章节的标题和详情页的url
    # 实例化BeautifulSoup对象，需要将页面源码数据加载到该对象中
    soup = BeautifulSoup(page_text, 'lxml')

    # 解析章节标题
    li_list = soup.select('.sidamingzhu-list-mulu > ul > li')

    # 写入的文件
    fp = open('./r03-sanguo.txt', 'w', encoding='utf-8')
    for li in li_list:
        # 每一回的标题
        title = li.a.string
        # 每一回的详细内容
        detail_url = li.a['href']
        # 对详情页发起请求，解析出章节内容
        detail_page_text = requests.get(url=detail_url, headers=headers).content.decode()

        detail_soup = BeautifulSoup(detail_page_text, 'lxml')
        # 这是获取包含内容的那个总div标签
        div_tag = detail_soup.find('div', class_='grap')
        # 获取该div里面所有的内容，包括子标签的。也就是章节的所有内容
        content = div_tag.text
        # 将文章标题和文章内容，写入对应的文件
        fp.write(title + ':' + content + '\n')

        print(title, '爬取成功！')

        