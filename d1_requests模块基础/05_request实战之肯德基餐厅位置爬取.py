import json

import requests

if __name__ == "__main__":
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    kw = input('enter a site to find kfc:')

    data = {
        'cname': '',
        'pid': '',
        'keyword': kw,
        'pageIndex': '1',
        'pageSize': '10'
    }

    response = requests.post(url=url, data=data, headers=headers)

    dic_obj = response.json()
    fp = open('kfc05.json', 'w', encoding='utf-8')
    json.dump(dic_obj, fp=fp, ensure_ascii=False)
    print('over')
