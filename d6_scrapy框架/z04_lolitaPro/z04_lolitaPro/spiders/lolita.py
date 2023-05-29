import scrapy

# 实现深度爬取 和 图片存储
"""
-图片数据爬取之ImagesPipeline
    基于scrapy爬取宇符串类型的数据和爬取图片类型的数据区别？
        字符串：只需要基于xpath进行解析且提交管道进行持久化存储
        图片：xpath解析出图片src的属性值。单独的对图片地址发起请求获取图片二进制类型的数据
    ImagesPipeline:
        只需要将img的src的属性值进行解析，提交到管道，管道就会对图片的src进行请求发送获取
        图片的二进制的数据类型，并且还会帮我们进行持久化存储
"""


class LolitaSpider(scrapy.Spider):
    name = "lolita"
    start_urls = ["http://m.xiannvku.co/tags/loli-1.html"]

    # 解析详情页之后回滚的方法
    def parse_detail(self, response):
        # 回调函数接收参数
        detail_title = response.meta['detail_title']
        print(detail_title)
        # 获取图片的详细地址
        img_list = response.xpath('//img[@class="content_img"]')
        for img in img_list:
            img_href = img.xpath('./@src')[0].extract()
            print(img_href)

    def parse(self, response):
        # 获取所有的标签的链接
        li_list = response.xpath('/html/body/div[3]/ul/li')

        for li in li_list:
            # 获得图集的详细地址
            detail_href = li.xpath('./a/@href')[0].extract()
            # 获得图集的主题名称
            detail_title = li.xpath('./a/img/@alt')[0].extract()

            # 对详情页发送数据请求获取详情页的页面源码数据
            # 手动请求的发送
            # 请求传参：meta={},可以将meta字典传递给请求对应的回调函数
            yield scrapy.Request(detail_href, callback=self.parse_detail,
                                 meta={
                                     'detail_title': detail_title
                                 })

