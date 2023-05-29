import requests
import scrapy
from selenium import webdriver
from z06_wangyiPro.items import Z06WangyiproItem


# 该文件主要演示 下载中间件-响应拦截的功能

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
