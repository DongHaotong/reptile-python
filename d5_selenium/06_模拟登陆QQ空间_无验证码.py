import time

from lxml import etree
from selenium import webdriver

url = "https://qzone.qq.com/"
browser = webdriver.Chrome(executable_path='./chromedriver')
browser.get(url)

# QQ空间进去是扫描二维码，需要点击"账号密码"登陆
# 切换到id=login_frame的iframe中
browser.switch_to_frame('login_frame')
plogin = browser.find_element_by_id("switcher_plogin")
plogin.click()

userName = browser.find_element_by_id("u")
userName.send_keys("1431430924")
time.sleep(2)
passWord = browser.find_element_by_id("p")
passWord.send_keys("959966PANGdong")
time.sleep(2)

submit = browser.find_element_by_id("login_button")
submit.click()

time.sleep(5)
browser.quit()
