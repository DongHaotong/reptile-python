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

