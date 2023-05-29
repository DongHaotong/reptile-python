import scrapy
from z01_biqugePro.items import Z01BiqugeproItem


class QubigeSpider(scrapy.Spider):
    name = "qubige"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://www.bbiquge.net/"]

    def parse(self, response):
        # 解析作者的名称和书名
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
