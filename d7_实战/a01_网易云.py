import os

import requests
from lxml import etree
import re

url = 'https://music.163.com/discover/toplist?id=3778678'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/111.0.0.0 Safari/537.36'
}
page_text = requests.get(url=url, headers=headers).text


pattern = re.compile(r'\d+')  # 查找数字

# 数据解析
tree = etree.HTML(page_text)
li_list = tree.xpath('//ul[@class="f-hide"]/li')

# 持久化存储
if not os.path.exists('./z01_网易云音乐'):
    os.mkdir('./z01_网易云音乐')

for li in li_list:
    # 获取歌曲的名称
    song_name = li.xpath('./a/text()')[0]
    song_id = li.xpath('./a/@href')[0]
    song_id = pattern.findall(song_id)[0]
    music_url = f'http://music.163.com/song/media/outer/url?id={song_id}.mp3'
    music_content = requests.get(url=music_url, headers=headers).content

    music_path = 'z01_网易云音乐/' + song_name + '.mp3'

    with open(music_path, 'wb') as fp:
        fp.write(music_content)
        print(song_name + "-->爬取成功!!!")

href="/song?id="


