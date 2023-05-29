import scrapy


class BizhiSpider(scrapy.Spider):
    name = "bizhi"
    start_urls = ["https://www.ivsky.com/bizhi/tuzi_t662/"]

    def parse(self, response):
        print(response.text)
        li_list = response.xpath('//ul[@class="il"]/li')
        print(li_list)
        for li in li_list:
            img_name = li.xpath('./div/a/img/@alt')[0]
            print(img_name)
