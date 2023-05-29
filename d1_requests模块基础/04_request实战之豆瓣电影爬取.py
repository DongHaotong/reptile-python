import json

import requests

if __name__ == "__main__":
    url = ' https://movie.douban.com/j/chart/top_list'
    param = {
        'type': '24',
        'interval_id': '100:90',
        'action': '',
        'start': '0',  # 从库中的第几部电影取
        'limit': '20'  # 一次取多少部电影
    }

    # 进行UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    response = requests.get(url=url, params=param, headers=headers)

    list_data = response.json()
    fp = open('douban04.json', 'w', encoding='utf-8')
    json.dump(list_data, fp=fp, ensure_ascii=False)

    print('over!!!!')
