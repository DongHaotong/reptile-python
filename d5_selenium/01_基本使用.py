import time

from selenium import webdriver


# 启动Chrome浏览器，必须要指定浏览器对应版本的驱动程序
browser = webdriver.Chrome(executable_path='./chromedriver')

url = "https://www.baidu.com"

# 用你的浏览器对象访问页面
browser.get(url)
# 给浏览器一些加载资源的时间
time.sleep(2)


# selenium的主要功能就是交互：访问 点击 输入 滑动 关闭
# 不要理解成一种解析的软件
# eg:找到百度的首页的输入框， 使用根据id查找
input_element = browser.find_element_by_id('kw')
# 对输入框进行信息输入
input_element.send_keys('美女')

# 在查找"百度一下"的搜索按钮，演示功能使用其他的查找方式
button = browser.find_element_by_xpath('//*[@id="su"]')
# 点击按钮
button.click()

time.sleep(2)

# 滚动当前页面到最下方（一定要留出足够的时间去加载页面）
browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
# browser.execute_script('alert("hello world!!!")') 弹出提示框


time.sleep(5)

# 都是关闭浏览器
# browser.close()
browser.quit()
