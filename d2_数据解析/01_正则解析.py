# 需求：
#       1 爬取豆瓣的电影信息
#       2 进行分页处理，获取所有的页
#       3 对电影的图片进行保存

import requests
import re
import os

if __name__ == "__main__":

    # 将所有的图片信息进行保存到该新创建的文件夹下
    if not os.path.exists('./moive_img'):
        os.mkdir('./moive_img')

    # 进行UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Safari/537.36'
    }

    for i in range(1, 11): # 循环发送请求，解决分页问题
        page = (i - 1) * 25
        url = f"https://movie.douban.com/top250?start={page}"

        # 使用通用爬虫对url对应的一整张页面进行爬取
        page_text = requests.get(url=url, headers=headers).text

        # 利用正则表达式进行数据的提取
        obj = re.compile(r'<div class="item">.*?<img .*? src="(?P<moiveImage>.*?)" class="">.*?<span '
                         r'class="title">(?P<moiveName>.*?)</span>.*?<br>('
                         r'?P<moiveYear>.*?)&nbsp;.*?<span class="rating_num" property="v:average">('
                         r'?P<moiveScore>.*?)</span>.*?<span>(?P<moiveNum>.*?)人评价</span>', re.S)
        # re.S可以让re匹配到换行符

        result = obj.finditer(page_text)
        for item in result:
            dic = item.groupdict()
            dic['moiveYear'] = dic['moiveYear'].strip()  # 去掉年份左右两端的空白(空格，换行符，制表位)
            print(dic)

            # 对图片进行保存操作
            moiveImgSrc = dic['moiveImage']  # 获得图片的地址
            # 请求图片的二进制数据
            img_data = requests.get(url=moiveImgSrc, headers=headers).content
            # 将图片进行保存，并且以电影名进行保存
            img_name = dic['moiveName']
            img_path = './moive_img/' + img_name + '.jpg'  # 图片最终存储的路径
            with open(img_path, 'wb') as fp:
                fp.write(img_data)
                print(img_name, '-->下载成功！')
