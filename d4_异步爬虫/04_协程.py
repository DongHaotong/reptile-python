import asyncio


async def request(url):
    print("正在请求的url:" + url)
    print("请求成功！")


# 用async修饰的函数，调用之后返回一个协程对象
c = request("www.baidu.com")

# 第一部分
# 创建一个事件循环对象
# loop = asyncio.get_event_loop()
# 将协程对象注册到loop中，然后启动loop
# loop.run_until_complete(c)

# 第二部分
# task的使用
loop = asyncio.get_event_loop()
# 基于loop创建了一个task对象
task = loop.create_task(c)
print(task)
loop.run_until_complete(task)
print(task)
