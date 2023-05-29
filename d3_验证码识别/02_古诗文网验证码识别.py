# 识别流程：
#   1 将验证码下载到本地
#   2 调用平台提供的实例代码进行图片数据标识

import requests
import re
import os
from lxml import etree
from hashlib import md5


# 超级鹰的验证码识别类
class Chaojiying_Client(object):
    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def PostPic_base64(self, base64_str, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
            'file_base64': base64_str
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == "__main__":
    url = 'https://so.gushiwen.cn/user/login.aspx?from' \
          '=http://so.gushiwen.cn/user/collect.aspx'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Safari/537.36'
    }

    page_text = requests.get(url=url, headers=headers).text

    # 解析页面中的验证码图片
    tree = etree.HTML(page_text)
    imgCode_path = 'https://so.gushiwen.cn' + tree.xpath('//*[@id="imgCode"]/@src')[0]
    img_data = requests.get(url=imgCode_path, headers=headers).content

    # 将验证码保存到本地
    with open('./code.jpg', 'wb') as fp:
        fp.write(img_data)

    # 调用打码平台的验证码进行验证码识别
    chaojiying = Chaojiying_Client('dong1111111', '959966pangDONG', '947109')
    im = open('code.jpg', 'rb').read()
    imgCode_Value = chaojiying.PostPic(im, 1902)['pic_str']
    print(imgCode_Value)
