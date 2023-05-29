# READERME

## 爬虫

### 数据解析

#### 基础

聚焦爬虫：爬取页面中指定的页面内容。

编码流程:

1. 指定url
2. 发起请求
3. 获取响应数据
4. 数据解析
5. 持久化存储



数据解析分类：

- 正则
- bs4
- xpath(重点)



数据解析原理概述:解析的局部的文本内容都会在标签之间或者标签对应的属性中进行存储。

1. 进行指定标签的定位。
2. 标签或者标签对应的属性中存储的数据值进行提取(解析)



#### 正则表达式解析

```python
import re

s = """
    <div class='abc'>
        <div><a href="baidu.com">我是百度</a></div>
        <div><a href="qq.com">我是QQ</a></div>
        <div><a href="163.com">我是网易</a></div>
    </div>
"""

obj = re.compile(r'<div><a href="(?P<url>.*?)">(?P<txt>.*?)</a></div>')
result = obj.finditer(s)
for item in result:
    # url = item.group("url")
    # txt = item.group("txt")
    # print(url, txt)
    print(item.groupdict())
```

以上输出

```python
{'url': 'baidu.com', 'txt': '我是百度'}
{'url': 'qq.com', 'txt': '我是QQ'}
{'url': '163.com', 'txt': '我是网易'}
```



#### BS4解析

实例化一个BeautifulSoup对象，并且将页面源码数据加载到该对象中。通过调用BeautifulSoup对象中相关的属性或者方法进行标签定位和数据提取。

##### 对象的实例化

```python
from bs4 import BeautifulSoup

1 将本地的html文档中的数据加载到该对象中
		fp = open('./r02.html', 'r', encoding='utf-8')
    soup = BeautifulSoup(fp, 'lxml')
2 将互联网上获取的页面源码加载到该对象中
		page_text= response.text
		soup = BeautifulSoup(page_text, 'lxml')
```



##### 方法和属性

操作的样本数据

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>

<body>
    <div>第一个div标签</div>

    <a href="https://www.baidu.com">
        <span>this is span</span>
    </a>

    <div>第二个div标签</div>

</body>
</html>
```

1. soup.tagName 返回的是html中第一次出现的tagName标签

```python
from bs4 import BeautifulSoup
if __name__ == "__main__":
    fp = open('./r02.html', 'r', encoding='utf-8')
    soup = BeautifulSoup(fp, 'lxml')

    # soup.tagName 返回的是html中第一次出现的tagName标签
    print(soup.div)  # <div>第一个div标签</div>
```

2. soup.find

```python
第一种用法：find('tagName') : 等同于soup.div
  from bs4 import BeautifulSoup
  if __name__ == "__main__":
      fp = open('./r02.html', 'r', encoding='utf-8')
      soup = BeautifulSoup(fp, 'lxml')
      print(soup.find('div')) # <div>第一个div标签</div>
    
    
第二种用法：find('tagName', class_/id/attr='xxx') : 属性定位
	from bs4 import BeautifulSoup
  if __name__ == "__main__":
      fp = open('./r02.html', 'r', encoding='utf-8')
      soup = BeautifulSoup(fp, 'lxml')
      print(soup.find('div', class_='two')) # <div class="two">第二个div标签</div>
```

3. Soup.find_all() : 返回符合要求的所有标签（列表）

```python
from bs4 import BeautifulSoup
if __name__ == "__main__":
    fp = open('./r02.html', 'r', encoding='utf-8')
    soup = BeautifulSoup(fp, 'lxml')
    # [<div>第一个div标签</div>, <div class="two">第二个div标签</div>]
    print(soup.find_all('div'))
```

4. soup.select()

```python
from bs4 import BeautifulSoup
if __name__ == "__main__":
  # 将本地的html文档中的数据加载到该对象中
  fp = open('./r02.html', 'r', encoding='utf-8')
  soup = BeautifulSoup(fp, 'lxml')

  # 第一种用法：select('某种选择器(id, class, 标签...选择器)'),返回的是一个列表
  print(soup.select('.tang'))
  """
    输出：
    	[<div class="tang">
        <ul>
        <li title="teacher">老师</li>
        <li title="student">学生</li>
        </ul>
        </div>]
    """

  # 第二种用法: 层级选择器
  # > 表示一个层级
  print(soup.select('.tang > ul > li')) 
  # 输出：[<li title="teacher">老师</li>, <li title="student">学生</li>]
  
  # 空格 表示多个层级
  print(soup.select('.tang > ul li')) 
  # 输出：[<li title="teacher">老师</li>, <li title="student">学生</li>]
```

5. 获取标签之间的文本数据 

```python
soup.a.text/string/get_text()
	text/get_text() : 可以获取某一个标签中所有的文本内容
  string ：只可以获取该标签下面直系的文本内容

print(soup.select('.tang > ul > li')[0].text) # 输出：老师
print(soup.select('.tang > ul > li')[0].get_text()) # 输出：老师
print(soup.select('.tang > ul > li')[0].string) # 输出：老师
```

5. 获取标签中属性值

```python
soup.a['href']
```



#### XPath解析

解析原理：实例化etree的对象，且需要将被解析的页面源码数据加载到该对象中。调用etree对象中的xpath方法结合着xpath表达式实现标签的定位和内容的捕获。

```python
实例化etree对象：
	1.将本地的html文档中的源码数据加载到etree对象中
			etree.parse(filePath)
	2.可以将从互联网上获取的源码数据加载到该对象中
			etree.HTML('page_text')
```



##### xpath表达式

1. `/` 从根节点开始定位，表示的是一个层级。

2. `//` 表示多个层级,可以从任意位置开始定位

3. `属性定位`  tag[@attrName="attrValue"]

4. `索引定位` 从1开始

实例：

本地待操作的HTML

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8"/>
    <title>Document</title>
</head>

<body>
    <div>第一个div标签</div>

    <a href="https://www.baidu.com">
        <span>this is span</span>
    </a>

    <div class="two">第二个div标签</div>

    <div class="tang">
        <ul>
            <li title="teacher">老师</li>
            <li title="student">学生</li>
        </ul>
    </div
</body>
</html>
```

操作实例

```python
from lxml import etree

if __name__ == "__main__":
    # 实例化etree对象，并且将被解析的源码加载到该对象中
    tree = etree.parse('r02.html')
    title = tree.xpath('/html/head/title')
    print(title)  # 输出：[<Element title at 0x104b4a140>]

    body_div = tree.xpath('/html/body/div')
    print(body_div)  # 输出：[<Element div at 0x106d603c0>, <Element div at 0x106d60400>, <Element div at 0x106d60440>]
    # 上面的等价替换
    body_div = tree.xpath('/html//div')
    body_div = tree.xpath('//div')

    # 属性定位
    body_div = tree.xpath('//div[@class="tang"]')
    print(body_div)  # 输出：[<Element div at 0x1070fc300>]

    # 索引定位，从1开始
    body_li = tree.xpath('//div[@class="tang"]/ul/li')
    print(body_li)  # 输出：[<Element li at 0x104e1d600>, <Element li at 0x104e1d5c0>]
    body_li = tree.xpath('//div[@class="tang"]/ul/li[1]')
    print(body_li)  # 输出：[<Element li at 0x104e1d600>]
```

5. 取文本
6. 取属性

```python
from lxml import etree

if __name__ == "__main__":
    # 实例化etree对象，并且将被解析的源码加载到该对象中
    tree = etree.parse('r02.html')
    # 获取直系文本的内容-获取第三个div中第二个li的文本内容
    text = tree.xpath('//div[@class="tang"]//li[2]/text()')  # ['学生']
    print(text)
    text = tree.xpath('//div[@class="tang"]//li[2]/text()')[0]  # 学生
    print(text)

    # 获取非直系的文本内容
    text = tree.xpath('//div[@class="tang"]//text()')
    print(text)  # ['\n', '\n', '老师', '\n', '学生', '\n', '\n']

    # 取属性
    text = tree.xpath('//div[@class="two"]/@class')
    print(text)  # ['two']
```



### 验证码识别

#### 超级鹰使用流程

在 `用户中心->软件ID`中创建一个软件，利用官网的帮助文档即可直接使用

```python
import requests
from hashlib import md5


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


# 只需要改这一部分即可
if __name__ == '__main__':
    chaojiying = Chaojiying_Client('dong1111111', '959966pangDONG', '947109')  # 用户中心>>软件ID 生成一个替换 96001
    im = open('a.jpg', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    print(chaojiying.PostPic(im, 1902))  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    # print chaojiying.PostPic(base64_str, 1902)  #此处为传入 base64代码
```



### 模拟登陆

教学视频的网站无效了，等待机会。。。。





### 代理

代理：破解封IP这种反爬机制

什么是代理：代理服务器

代理的作用：突破自身IP访问的限制 和 隐藏自身真实IP

代理相关的网站：快代理 https://www.kuaidaili.com/   熊猫代理 http://www.xiongmaodaili.com/

代理ip的类型：

- http：应用到http协议对应的url中
- https：应用到https协议对应的url中

代理IP的匿名度：

- 透明明：服务器知道该次请求使用了代理，也知道请求对应的真实ip
- 匿名：知道使用了代理，不知道真实IP
- 高匿：不知道使用了代理，更不知道真实的IP



### 异步爬虫

异步爬虫的方式：

多线程，多进程（不建议）：

​	好处：可以为相关阻塞的操作单独开启线程或者进程，阻塞操作就可以异步执行。

​	弊端：无法无限制的开启多线程或者多进程。

线程池、进程池 （适党的使用）

​	好处：我们可以降低系统对进程或者线程创建和销毀的一个频率，从而很好的降低系统的开销。

​	弊端：池中线程或进程的数量是有上限。

单线程＋异步协程（推荐）：

1. event_loop：事件循环，相当于一个无限循环，我们可以把一些西数注册到这个事件循环上，当满足某些条件的时候，函数就会被循环执行。
2. coroutine：协程对象，我们可以将协程对象注册到事件循环中，它会被事件循环调用。我们可以使用async 关键字来定义一个方法，这个方法在调用时不会立即被执行，而是返回一个协程对象。
3. task： 任务，它是对协程对象的进一步封装，包含了任务的各个状态。
4. future：代表将来执行或还没有执行的任务，实际上和 task 没有本质区别。
5. async： 定义一个协程。
6. await： 用来挂起阻塞方法的执行。





### Selenium

#### 使用步骤

1. python：`pip install selenium`

2. 配置浏览器驱动使用：http://chromedriver.storage.googleapis.com/index.html?path=111.0.5563.64/
3. 实例化一个浏览器对象
4. 编写基于浏览器自动化的操作代码

#### 自动化操作

- 发起请求：get (url)

- 标签定位：find系列的方法
- 标签交互：send_keys("xxx")
- 执行js程序：excute_script('jscode" )
- 前进，后退：backO，forward()
- 关闭浏览器：quit()



### Scrapy

爬虫的框架

#### 基本使用

创建工程: `scrapy startproject 工程名`

<img src="../../../../笔记/Python/基础/img/截屏2023-04-16 11.43.55.png" alt="截屏2023-04-16 11.43.55" style="zoom:50%;" />

在spiders子目录中创建一个爬虫文件：`scrapy genspider 文件名 url`(进入第一个firstBlood中，使用该命令,爬虫文件自动放在spiders中)

```python
% cd firstBlood 
% scrapy genspider test www.baidu.com
```

执行工程:`scrapy crawl 文件名    `

执行工程:`scrapy crawl 文件名 --nolog` 不现实其他杂乱的信息，只显示自己输出的

案列:test.py

```python
# scrapy.Spider类是爬虫文件的总类
class TestSpider(scrapy.Spider):
    # 爬虫文件的名称 : 爬虫源文件的唯一标识
    name = "test"
    # 允许的域名 : 用来限定start_urls中哪些URL可以进行请求发送
    allowed_domains = ["www.baidu.com"]
    # 起始的url列表 : 该列表存放的url会被scrapy自动进行请求的发送
    start_urls = ["http://www.baidu.com/", "http://www.sogou.com/"]

    # 用作数据解析：response参数表示的就是请求成功后对应的响应对象
    # 调用次数和start_urls中的路径个数有关，会自动的调用parse方法
    def parse(self, response):
        print(response)
```

```python
% scrapy crawl test        
<200 http://www.baidu.com/>
<200 https://www.sogou.com/>
```



#### 数据解析

extract()方法:在该框架中使用xpath返回的是Selector标签集合。extract作用于集合时，返回的是集合中所有属性为data的内容，作用于单个标签时，返回的是该标签的data内容。

```python
import scrapy

class QubigeSpider(scrapy.Spider):
    name = "qubige"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://www.bbiquge.net/"]

    def parse(self, response):
        # 解析作者的名称和书名
        div_list = response.xpath('//*[@id="container"]/div')
        for div in div_list:
            # xpath返回的是列表，但是列表元素一定是Selector类型的对象
            # <Selector xpath='./div[2]/dl/dt/a/text()' data='神印王座II皓月当空'>
            # extract()可以将Selector对象中data参数存储的字符串提取出来
            title = div.xpath('./div[2]/dl/dt/a/text()')[0].extract()
            category = div.xpath('./div[2]/dl/dd[1]/span[1]/text()')[0].extract()
            author = div.xpath('./div[2]/dl/dd[1]/span[2]/text()')[0].extract()
            # 列表调用extract之后，则表示将列表中每一个Selector对象中data对应的字符串提取出来
            print(title, category, author)
```

测试：终端输入指令`scrapy crawl qubige --nolog`

```
神印王座II皓月当空 都市 唐家三少
宇宙职业选手 玄幻 我吃西红柿
风起龙城 科幻 伪戒
斗罗大陆V重生唐三 玄幻 唐家三少
深空彼岸 都市 辰东
万相之王 玄幻 天蚕土豆
```



#### 持久化存储

##### 基于终端指令

只可以将parse方法的返回值存储到本地的文本文件中，并且持久化存储对应的文件的类型只可以为(json、jsonlines、jl、csv、xml、marshal、pickle)

```python
import scrapy
class QubigeSpider(scrapy.Spider):
    name = "qubige"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://www.bbiquge.net/"]

    def parse(self, response):
        div_list = response.xpath('//*[@id="container"]/div')

        # 存储所有解析到的数据
        all_data = []

        for div in div_list:
            title = div.xpath('./div[2]/dl/dt/a/text()')[0].extract()
            category = div.xpath('./div[2]/dl/dd[1]/span[1]/text()')[0].extract()
            author = div.xpath('./div[2]/dl/dd[1]/span[2]/text()')[0].extract()
            print(title, category, author)
            dic = {
                'title': title,
                'category': category,
                'author': author
            }
            all_data.append(dic)
				# 会将该数据进行保存
        return all_data
```

```python
语法：scrapy crawl 文件名 -o 文件存储路径
实例：scrapy crawl qubige -o ./biquge.json
```



##### 基于管道 

编码流程：

1. 数据解析
2. 在item类中定义相关的属性(也就是目录中items.py)
3. 将解析的数据封装存储到item类型的对象中
4. 将item类型的对象提交给管道进行持久化存储的操作
5. 在管道类的process_item中要将其接受到的item对象中存储的数据进行持久化存储操作(也就是目录中pipelines.py)
6. 在配置文件中开启管道

```python
# 第一步：文件items.py中
import scrapy
class Z01BiqugeproItem(scrapy.Item):
    # define the fields for your item here like:
    # 设置对应需要存储的属性
    title = scrapy.Field()
    category = scrapy.Field()
    author = scrapy.Field()
    
    
# 第二步：qubige.py
import scrapy
from z01_biqugePro.items import Z01BiqugeproItem # 导入第一步中的类
class QubigeSpider(scrapy.Spider):
    name = "qubige"
    start_urls = ["https://www.bbiquge.net/"]

    def parse(self, response):
        div_list = response.xpath('//*[@id="container"]/div')

        for div in div_list:
            title = div.xpath('./div[2]/dl/dt/a/text()')[0].extract()
            category = div.xpath('./div[2]/dl/dd[1]/span[1]/text()')[0].extract()
            author = div.xpath('./div[2]/dl/dd[1]/span[2]/text()')[0].extract()
            print(title, category, author)

            # 创建item类并且传递对应的参数
            item = Z01BiqugeproItem()
            item['title'] = title
            item['category'] = category
            item['author'] = author

            # 将item提交给管道
            yield item
            
            
# 第三步：pipelines.py
lass Z01BiqugeproPipeline(object):
    fp = None

    # 重写父类的一个方法：该方法只在开始爬虫的时候被调用一次
    def open_spider(self, spider):
        print("开始爬虫....")
        self.fp = open('./biquge.txt', 'w', encoding='utf-8')

    # 专门用来处理item类型对象
    # 该方法可以接收爬虫文件提交过来的item对象
    # 该方法每接收一个item就会调用一次
    def process_item(self, item, spider):
        title = item['title']
        category = item['category']
        author = item['author']
        # 将类型转换为字符串类型
        title = ''.join(title)
        category = ''.join(category)
        author = ''.join(author)
        self.fp.write(title + ':' + category + ':' + author + '\n')
        return item

    def close_spider(self, spider):
        print("结束爬虫...")
        self.fp.close()
        
        
# 第四步：在配置文件中settings.py打开这一段
# 请求头
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 " \
             "Safari/537.36"

# 显示指定类型的日志信息,这里指定显示异常的日志信息
LOG_LEVEL = 'ERROR'

ITEM_PIPELINES = {
    "z01_biqugePro.pipelines.Z01BiqugeproPipeline": 300,
    # 300表示优先级，数值越小优先级越高
}

# 终端执行：scrapy crawl qubige
# biquge.txt文件内容
神印王座II皓月当空:都市:唐家三少
宇宙职业选手:玄幻:我吃西红柿
风起龙城:科幻:伪戒
斗罗大陆V重生唐三:玄幻:唐家三少
深空彼岸:都市:辰东
万相之王:玄幻:天蚕土豆
```



#### 请求参数



#### 存储图片

 使用流程：

- 数据解析（图片的地址）
- 将存储图片地址的item提交到制定的管道类

- 在管道文件中自定制一个基于ImagesPipeLine的一个管道类
  - get_media_request
  - file_path 
  - item_completed
- 在配置文件中：
  - ﻿指定图片存储的目录：IMAGES_ STORE = "./imgs_ boba"
  - ﻿指定开启的管道：自定制的管道类

```python
# 第一步：获取图片的src，并且保存在item中，最后进行提交
import scrapy
from z03_imgPro.items import Z03ImgproItem

class ImgSpider(scrapy.Spider):
    name = "img"
    start_urls = ["https://sc.chinaz.com/tupian/renwutupian.html"]

    def parse(self, response):
        div_list = response.xpath('/html/body/div[3]/div[2]/div')
        for div in div_list:
            # 该网站的图片均为懒加载，只有查看到指定位置，才会加载指定位置的图片
            # 所以我们使用该属性获取图片地址
            src = 'https:' + div.xpath('./img/@data-original').extract_first()
            item = Z03ImgproItem()
            item['src'] = src
            yield item

            
# 第二步：在items.py中加入对应的属性
class Z03ImgproItem(scrapy.Item):
    src = scrapy.Field()
    
    
# 第三步：在pipelines.py中自定义自己的类
from scrapy.pipelines.images import ImagesPipeline
import scrapy
class imagesPipeLine(ImagesPipeline):
    # 重写父类的三个方法

    # 可以根据图片地址进行图片数据的请求
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['src'])

    # 指定图片持久化存储的路径
    def file_path(self, request, response=None, info=None, *, item=None):
        imgName = request.url.split('/')[-1]
        return imgName

    # 返回给下一个即将执行的管道类
    def item_completed(self, results, item, info):
        return item
      
      
# 第四步：在配置setting.py文件中，将ITEM_PIPELINES中类修改为第三步中自己创建的类名。并且添加对应的存储地址
ITEM_PIPELINES = {
   "z03_imgPro.pipelines.imagesPipeLine": 300,
}
# 指定图片存储的目录
IMAGES_STORE = './imgs'
```



#### 组件

![e1868b22bb82ef7f1eacb68dc2086499](../../../../笔记/Python/基础/img/e1868b22bb82ef7f1eacb68dc2086499.png)

1. 引擎(Scrapy)
       用来处理整个系统的数据流处理, 触发事务(框架核心)
2. 调度器(Scheduler)
       用来接受引擎发过来的请求, 压入队列中, 并在引擎再次请求的时候返回. 可以想像成一个URL（抓取网页的网址或者说是链接）的优先队列, 由它来决定下一个要抓取的网址是什么, 同时去除重复的网址
3. 下载器(Downloader)（scrapy的异步在这里）
       用于下载网页内容, 并将网页内容返回给蜘蛛(Scrapy下载器是建立在twisted这个高效的异步模型上的)
4. 爬虫(Spiders)
       爬虫是主要干活的, 用于从特定的网页中提取自己需要的信息, 即所谓的实体(Item)。用户也可以从中提取出链接,让Scrapy继续抓取下一个页面
5. 项目管道(Pipeline)
       负责处理爬虫从网页中抽取的实体，主要的功能是持久化实体、验证实体的有效性、清除不需要的信息。当页面被爬虫解析后，将被发送到项目管道，并经过几个特定的次序处理数据。
6. 下载器中间件
   可以拦截请求和响应对象，请求和响应交互的时候一定会经过下载中间件，可以处理请求和响应。
7. 爬虫中间件
     拦截请求和响应，对请求和响应进行处理。



#### 下载中间件

位置：引擎和下载器之间

作用：批量拦截到整个工程中所有的请求和响应

拦截请求：

- ﻿﻿UA伪装
- ﻿﻿代理IP

拦截响应：

​	篡改响应数据，响应对象



##### 拦截请求

UA池的封装

```python
user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
```



使用步骤

```python
# 第一步：写出测试页面，该url是查看请求ip地址的网站
class MiddleSpider(scrapy.Spider):
    name = "middle"
    start_urls = ["http://www.ip111.cn/"]

    def parse(self, response):
      	# 获取网页的源码
        page_text = response.text
        # 将获取到的页面源码进行保存
        with open('ip.html', 'w', encoding='utf-8') as fp:
            fp.write(page_text)
            
# 第二步：在中间件文件中middlewares.py，进行下载中间件的配置
# 下载中间件
class Z05MiddleproDownloaderMiddleware:
    # UA池
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

    # 拦截请求
    def process_request(self, request, spider):
        # UA伪装,从UA池中随机选择一个
        request.headers['User-Agent'] = random.choice(self.user_agent_list)
        # 为了验证代理的操作是否有效, 因为发生异常的请求执行不到，所有用该方法来模拟
        request.meta['proxy'] = 'http://121.22.53.166:9091'
        return None

    # 拦截所有的响应
    def process_response(self, request, response, spider):
        return response

    # 拦截发生异常的请求
    def process_exception(self, request, exception, spider):
        # ip被禁了之后，访问会不成功
        # 使用代理替换原来的ip即可
        pass

      
# 第三步：在设置中进行配置，主要是打开下载中间件的设置。配置文件中不同设置请求头了
ROBOTSTXT_OBEY = False
LOG_LEVEL = 'ERROR'
DOWNLOADER_MIDDLEWARES = {
    "z05_middlePro.middlewares.Z05MiddleproDownloaderMiddleware": 543,
}

# 注意：http和https要分别处理
```



##### 拦截响应

篡改响应数据，响应对象

需求：爬取网易新闻中的新闻数据（标题和内容）

1. 通过网易新闻的首页解析出五大板块对应的详情页的url（没有动态加载）
2. 每一个板块对应的新闻标题都是动态加载出来的（动态加载）
3. 通过解析出每一条新间详情页的url获取详情页的页面源码，解析出新闻内容



第一步：编写爬取网页的代码

```python
class WangyiSpider(scrapy.Spider):
    name = "wangyi"
    start_urls = ["https://news.163.com/"]

    # 存储四大板块的详情地址
    models_url = []

    # 实例化浏览器对象，用于解决动态数据问题
    def __init__(self):
        self.bro = webdriver.Chrome(
            '/Users/donghaotong/Public/project/python_project/pathon_learn/爬虫课程/d6_scrapy框架/z06_wangyiPro/chromedriver')

    # 解析五大板块的详细信息的url
    def parse(self, response):
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[3]/div[2]/div[2]/div[2]/div/ul/li')
        alist = [1, 2, 4, 5]
        for index in alist:
            li = li_list[index]
            model_detail_href = li.xpath('./a/@href').extract_first()
            self.models_url.append(model_detail_href)

        # 依次对每一个板块对应的页面进行请求
        for url in self.models_url:
            yield scrapy.Request(url, callback=self.parse_model)

    # 解析每一个板块页面中对应新闻的标题和新闻详情页的url
    # 每一个模块对应的新闻标题相关内容都是动态加载的
    def parse_model(self, response):
        div_list = response.xpath('/html/body/div/div[3]/div[3]/div[1]/div[1]/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            title_href = div.xpath('./div/div[1]/h3/a/@href').extract_first()

            # 持久化存储的item
            item = Z06WangyiproItem()
            item['title'] = title
            print(title_href)
            # 对新闻详情页进行解析
            yield scrapy.Request(url=title_href, callback=self.parse_detail, meta={'item': item})

    # 解析新闻的内容
    def parse_detail(self, response):
        content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
        content = ''.join(content)
        item = response.meta['item']
        item['content'] = content
        print(item['title'])
        print(item['content'])
        # 提交到管道中
        yield item

    # 关闭浏览器
    def closed(self, spider):
        self.bro.quit()
```

第二步：编写item所需要的属性

```python
class Z06WangyiproItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
```

第三步: 编写中间件的代码,主要编写响应的代码,selenium去处理动态获取资源

```python
class Z06WangyiproDownloaderMiddleware:
    def process_request(self, request, spider):
        return None

    # 通过该方法拦截四大板块的响应对象，进行篡改
    def process_response(self, request, response, spider):
        # 获取在爬虫文件中定义的浏览器对象
        bro = spider.bro
        """
          挑选出指定的响应对象进行篡改
          通过url指定request
          通过request指定response
          spider爬虫对象，就是wangyi.py里面的WangyiSpider类
        """
        if request.url in spider.models_url:
            # 使用selenium请求
            bro.get(request.url)
            sleep(2)
            page_text = bro.page_source  # 包含动态加载的数据
            """
              response四大板块里面的响应对象,针对定位到的这些response进行篡改
              实例化一个新的响应对象，(符合需求：包含动态加载的新闻数据),替代原来的数据
              如何获取动态加载的新闻数据?
                基于selenium便捷的获取动态加载的数据
            """
            new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
            return new_response
        else:
            # response其他请求的响应对象
            return response

    def process_exception(self, request, exception, spider):
        pass

```

第四步：在管道文件中，持久化存储，和配置文件的相关配置



#### CrawlSpider

Crawlspider类，Spider的一个子类

- ﻿全站数据爬取的方式
   - ﻿﻿基于Spider：手动请求
   - ﻿﻿基于Crawlspider
- ﻿CrawlSpider的使用：
   - ﻿﻿创建一个工程
   - ﻿﻿cd XXX
   - ﻿﻿创建爬虫文件 (CrawlSpider)
       - 创建指令有所不同`scrapy genspider -t crawl xxx www.xxx.com`
       - 链接提取器：根据指定规则（allow="正则"）进行指定链接的提取
       - 规则解析器：将链接提取器提取到的链接进行指定规则（callback）的解析操作
       - follow=True:可以将链接提取器继续作用到链接提取器提取到的链接所对应的页面中