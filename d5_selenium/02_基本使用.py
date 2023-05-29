import time

from selenium import webdriver

# 启动Chrome浏览器，必须要指定浏览器对应版本的驱动程序
browser = webdriver.Chrome(executable_path='./chromedriver')

url = "https://www.baidu.com"

# 用你的浏览器对象访问页面
browser.get(url)
# 给浏览器一些加载资源的时间
time.sleep(2)

# 在百度首页查找'新闻',通过 链接文本 查询
button = browser.find_element_by_link_text("新闻")
button.click()

time.sleep(2)

# 都是关闭浏览器
browser.quit()