import time

from selenium import webdriver

# 无头浏览器 : 无界面的浏览器，只有源码
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# 启动Chrome浏览器，必须要指定浏览器对应版本的驱动程序
headless_browser = webdriver.Chrome(executable_path='./chromedriver', options=options)

url = "https://www.baidu.com"

# 用你的浏览器对象访问页面
headless_browser.get(url)
# 给浏览器一些加载资源的时间
time.sleep(2)

# 获取网页的源码
html_string = headless_browser.page_source
print(html_string)


# 获取输入框，输入'美女'
input_element = headless_browser.find_element_by_id('kw')
input_element.send_keys('美女')
time.sleep(2)

# 使用屏幕截图来监控整个访问流程
headless_browser.save_screenshot('./step1.png')

# 点击'百度一下'
button = headless_browser.find_element_by_xpath('//*[@id="su"]')
button.click()
time.sleep(2)

headless_browser.save_screenshot('./step2.png')


# 都是关闭浏览器
headless_browser.quit()
