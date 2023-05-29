import time
# 导入线程池模块的类
from multiprocessing.dummy import Pool

start_time = time.time()


def get_page(name):
    print("正在下载：" + name)
    time.sleep(2)
    print("下载成功：" + name)


name_list = ['dd', 'aa', 'bb', 'cc']

# 实例化线程池的类
pool = Pool(4)
# 将列表中每一个列表元素传递给get_page进行处理
pool.map(get_page, name_list)

end_time = time.time()
print("%d second" % (end_time - start_time))