import time
import requests
from hashlib import md5

from PIL import Image
from lxml import etree
from selenium import webdriver

"""
    1. 使用selenium打开登陆页面
    2. 使用当前的selenium打开该页面的截图
    3. 对当前图片局部区域（验证码图片）进行裁剪
    4. 使用超级鹰识别验证码，登陆 
"""


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


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/111.0.0.0 Safari/537.36'
}

url = "https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
browser = webdriver.Chrome(executable_path='./chromedriver')
# browser.maximize_window()  # 最大化浏览器页面
browser.get(url)

# 重点
# 进行页面的截取 和 保存
browser.save_screenshot("./page.png")
# 确定验证码图片对应的左上角和右下角坐标
code_img_ele = browser.find_element_by_xpath('//*[@id="imgCode"]')  # 查找验证码标签
location = code_img_ele.location  # location返回验证码图片左上角的坐标(x,y)
size = code_img_ele.size  # size返回验证码的长和宽

print("location:", location)
print("size:", size)

# 左上角和右上角坐标
# 这里需要*2才能找到位置，不知道为啥 
code_img_range = (
    location['x'] * 2,
    location['y'] * 2,
    (location['x'] + size['width']) * 2,
    (location['y'] + size['height']) * 2
)

print("code_img_range:", code_img_range)

# 至此 验证码图片区域就确定下来了

i = Image.open("./page.png")
code_img_name = './code.png'
# crop根据指定区域进行图片裁剪
frame = i.crop(code_img_range)
frame.save(code_img_name)

time.sleep(3)

# 获取登陆框
loginName = browser.find_element_by_id("email")
loginName.send_keys("dht990924@163.com")

password = browser.find_element_by_id("pwd")
password.send_keys("959966pangDONG")

# 利用超级鹰，识别验证码
chaojiying = Chaojiying_Client('dong1111111', '959966pangDONG', '947109')
im = open('code.png', 'rb').read()
code_str = chaojiying.PostPic(im, 1902)

code = browser.find_element_by_id("code")
code.send_keys(code_str['pic_str'])

time.sleep(3)

denglu = browser.find_element_by_id("denglu")
denglu.click()

time.sleep(3)
browser.close()