import scrapy

# 该文件主要演示 下载中间件-请求拦截的功能


class MiddleSpider(scrapy.Spider):
    name = "middle"
    start_urls = ["http://www.ip111.cn/"]

    def parse(self, response):
        page_text = response.text
        with open('ip.html', 'w', encoding='utf-8') as fp:
            fp.write(page_text)