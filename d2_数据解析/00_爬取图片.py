
# 如何爬取图片

import requests

if __name__ == "__main__":
    # 指定图片地址
    url = 'https://5b0988e595225.cdn.sohucs.com/images/20200102/59a5cc9a208249c6b4a58a8287f50485.jpeg'
    # content返回的是二进制形式的图片数据
    # text-字符串 content-二进制 json()-对象
    img_data = requests.get(url=url).content

    with open("./r0-qiutu.jpg", 'wb') as fp:
        fp.write(img_data)

    print("over!!!")
