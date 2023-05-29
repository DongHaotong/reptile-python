from multiprocessing.dummy import Pool
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/111.0.0.0 Safari/537.36'
}

# 原则：线程池处理的是阻塞且耗时的操作
# 爬取梨视频中的视频
url = 'https://www.pearvideo.com/category_1'
page_text = requests.get(url=url, headers=headers).text

# 进行数据解析
tree = etree.HTML(page_text)
li_list = tree.xpath('//*[@id="listvideoListUl"]/li')
for li in li_list:
    # 获取了视频的存放页面地址
    video_path = 'https://www.pearvideo.com/' + li.xpath('./div/a/@href')[0]
    # 获取视频的主题名称
    video_name = li.xpath('./div/a/div[2]/text()')[0] + '.mp4'

    # 对详情页发起请求
    detail_page_text = requests.get(url=video_path, headers=headers).text

    # 这里详情页中已经获取不到视频的地址了，所以没法处理了
    # 这里模拟一下

# 这里模拟获得了视频的地址
urls = []
dic1 = {
    'name': '1.mp4',
    'url': 'https://video.pearvideo.com/mp4/short/20220427/cont-1749065-15869965-hd.mp4'
}
dic2 = {
    'name': '2.mp4',
    'url': 'https://video.pearvideo.com/mp4/short/20220601/cont-1749821-15889097-hd.mp4'
}
dic3 = {
    'name': '3.mp4',
    'url': 'https://video.pearvideo.com/mp4/short/20220616/cont-1749829-15896621-hd.mp4'
}
dic4 = {
    'name': '4.mp4',
    'url': 'https://video.pearvideo.com/mp4/short/20220415/cont-1749824-15862487-hd.mp4'
}
urls.append(dic1)
urls.append(dic2)
urls.append(dic3)
urls.append(dic4)


# 下载视频的函数
def get_video_data(dic):
    part_url = dic['url']
    print(dic['name'], '正在下载....')
    data = requests.get(url=part_url, headers=headers).content
    # 持久化操作
    with open(dic['name'], 'wb') as fp:
        fp.write(data)
        print(dic['name'], '下载成功!')


# 使用线程池对视频进行数据请求处理
pool = Pool(4)
pool.map(get_video_data, urls)

pool.close()  # 关闭线程池
pool.join()  # 主线程等待子线程结束后再结束
