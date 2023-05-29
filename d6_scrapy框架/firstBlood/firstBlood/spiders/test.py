import scrapy


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
