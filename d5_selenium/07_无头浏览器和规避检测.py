import time

from selenium import webdriver
# 实现无可视化界面
from selenium.webdriver.chrome.options import Options
# 实现规避检测
from selenium.webdriver import ChromeOptions

# 实现无可视化界面的操作
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 实现规避操作
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

bro = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options, options=options)

bro.get("https://www.baidu.com")
bro.save_screenshot('./step1_07.png')

time.sleep(2)
bro.quit()
