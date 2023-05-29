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
