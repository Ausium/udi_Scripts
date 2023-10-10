#! /usr/bin/env python3
# coding=utf-8
# 获取外网地址和归属地信息

import requests
import sys


def get_ip(option):
    url1 = 'http://ip.useragentinfo.com/json'
    url2 = 'http://api.vore.top/api/IPdata'
    if option:
        if option == 'proxy':
            res = requests.get(url2)
            if res.ok:
                ip_data = {'IP': res.json()['ipinfo']['text'],
                           'o': res.json()['adcode']['o']}
                return ip_data
        param = {'ip': option}
        res = requests.get(url1, params=param)
        if res.ok:
            ip_data = {'IP': res.json()['ip'],
                       'o': res.json()['country']
                       + res.json()['province']
                       + res.json()['city']
                       + res.json()['area'] + '-'
                       + res.json()['isp']
                       + res.json()['net']}
            return ip_data
        else:
            res = requests.get(url2, params=param)
            if res.ok:
                ip_data = {'IP': res.json()['ipinfo']['text'],
                           'o': res.json()['adcode']['o']}
                return ip_data
            else:
                print('network exception')
    else:
        res = requests.get(url1)
        if res.ok:
            ip_data = {'IP': res.json()['ip'],
                       'o': res.json()['country']
                       + res.json()['province']
                       + res.json()['city']
                       + res.json()['area'] + '-'
                       + res.json()['isp']
                       + res.json()['net']}
            return ip_data
        else:
            res = requests.get(url2)
            if res.ok:
                ip_data = {'IP': res.json()['ipinfo']['text'],
                           'o': res.json()['adcode']['o']}
                return ip_data
            else:
                print('network exception')


if __name__ == '__main__':
    try:
        option = sys.argv[1]
    except Exception:
        option = ''
    if option == '-h':
        print("""\033[32m\tipme\033[0m -- return real IPdata
\033[32m\tipme proxy\033[0m -- return proxy ip_data
\033[32m\tipme 8.8.8.8\033[0m -- return this IPdata""")
        sys.exit(0)
    ip_data = get_ip(option)
    print(ip_data)
