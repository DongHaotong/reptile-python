# post请求（携带了参数）
# 响应数据是一组JSON数据
import json

import requests

if __name__ == "__main__":
    # 1. 指定url
    post_url = 'https://fanyi.baidu.com/sug'
    # 2. 进行UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    # 3. post请求参数处理（同get请求一致）
    data = {
        'kw': 'dog'
    }

    # 4. 请求发送
    response = requests.post(url=post_url, data=data, headers=headers)

    # 5. 获取响应数据 : .json()方法返回的是obj（如果确认响应数据是json类型的，
    #                       才可以使用json()方法）
    dic_obj = response.json()

    # 6. 持久化存储
    fp = open('dog03.json', 'w', encoding='utf-8')
    json.dump(dic_obj, fp=fp, ensure_ascii=False)

    print("over!!!")
