#! /bin/python3
# coding=utf-8
# 定期删除elk索引

import requests
from datetime import datetime

expire_days = 30


def clean_index():
    today = datetime.today()
    url = 'http://192.168.19.113:9200/'
    header = {'Authorization': 'Basic ZWxhc3RpYzpjaGFuZ2VtZQ=='}
    res = requests.get(url + '_cat/indices?v', headers=header)
    if res.ok:
        for line in res.text.split('\n')[1:-1]:
            index_name = line.split()[2]
            try:
                index_time = datetime.strptime(
                        index_name.split('-')[-1],
                        '%Y.%m.%d')
            except ValueError:
                index_time = ''
            if index_time:
                gap_day = (today - index_time).days
                if gap_day > expire_days:
                    print(index_name)
                    res = requests.delete(url + index_name,
                                          headers=header)
                    print(res.text)


if __name__ == "__main__":
    clean_index()
