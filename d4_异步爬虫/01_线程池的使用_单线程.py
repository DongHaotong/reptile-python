import time


def get_page(name):
    print("正在下载：" + name)
    time.sleep(2)
    print("下载成功：" + name)


name_list = ['dd', 'aa', 'bb', 'cc']

start_time = time.time()

for i in range(len(name_list)):
    get_page(name_list[i])

end_time = time.time()

print("%d second" % (end_time - start_time))
