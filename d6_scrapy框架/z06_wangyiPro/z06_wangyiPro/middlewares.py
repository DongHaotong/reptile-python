from scrapy import signals
from scrapy.http import HtmlResponse
from time import sleep


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
