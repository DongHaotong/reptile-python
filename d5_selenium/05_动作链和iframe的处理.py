import time

from selenium import webdriver
from selenium.webdriver import ActionChains

url = "https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable"
browser = webdriver.Chrome(executable_path='./chromedriver')
browser.get(url)

# 如果定位的标签在于iframe标签之中，则必须通过如下操作在进行标签定位
browser.switch_to_frame('iframeResult')  # 参数：iframe的id  作用：切换浏览器标签作用的作用域
div = browser.find_element_by_id("draggable")  # 获取需要拖动的标签

# 动作链
action = ActionChains(browser)
# 点击长按指定的标签
action.click_and_hold(div)

for i in range(5):
    # perform()立即执行动作链操作
    # move_by_offset(x,y):x水平方向，y竖直方向
    action.move_by_offset(17, 0).perform()
    time.sleep(0.3)

# 释放动作链
action.release().perform()

time.sleep(2)

browser.quit()
