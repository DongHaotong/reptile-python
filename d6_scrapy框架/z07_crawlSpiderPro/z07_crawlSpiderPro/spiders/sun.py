from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SunSpider(CrawlSpider):
    name = "sun"
    start_urls = ["http://wzzdg.sun0769.com/political/index/supervise?page=2"]

    # 使用链接提取器解析详情页的链接
    link_detail = LinkExtractor(allow=r"/political/politics/index?id=\d+")

    rules = (
        # Rule规则解析器
        # LinkExtractor链接提取器
        Rule(LinkExtractor(allow=r"page=\d+"), callback="parse_item", follow=True),
        Rule(link_detail, callback="parse_detail")
    )

    """
        - 链接提取器：根据指定规则（allow="正则"）进行指定链接的提取
        - 规则解析器：将链接提取器提取到的链接进行指定规则（callback）的解析操作
        - follow=True:可以将链接提取器继续作用到链接提取器提取到的链接所对应的页面中
    """

    # 解析新闻的标题和编号
    def parse_item(self, response):
        li_list = response.xpath('/html/body/div[2]/div[3]/ul/li')
        for li in li_list:
            new_num = li.xpath('./span[1]/text()').extract_first()
            new_title = li.xpath('./span[3]/a/text()').extract_first()
            new_href = 'http://wzzdg.sun0769.com' + li.xpath('./span[3]/a/@href').extract_first()

    # 解析新闻内容和新闻编号
    def parse_detail(self, response):
        print(response)
        new_num = response.xpath('/html/body/div[3]/div[2]/div[2]/div[1]/span[5]/test()').extract_first()
        new_content = response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/pre/text()').extract_first()
        print(new_num, new_content)
