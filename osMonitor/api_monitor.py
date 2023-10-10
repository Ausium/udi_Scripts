#! /bin/python3
# coding=utf-8

import json
import requests
import time

pro_start_time = time.time()
session = requests.Session()
now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def get_token():
    """获取token"""
    url = host + '/api/v1/pub/login/3rd'
    header = {'Content-Type': 'application/json'}
    payload = json.dumps(
            {"ID": "caizhisheng",
             "secret": "25d55ad283aa400af464c76d713c07ad",
             "type": "default"})
    res = session.post(url, headers=header, data=payload)
    return res.json()['data']['access_token']


def get_user(token):
    """获取当前用户信息"""
    url = host + '/api/v1/pub/current/user'
    header = {'Authorization': 'Bearer ' + token}
    res = session.get(url, headers=header)
    if res.ok:
        back_code = res.json()['status']
        if back_code != 1:
            return 'udi-admin service is error\n\nmessage: %s \n '\
                    % (res.json()['message'])
    else:
        return 'HTTP request error\n\nurl: %s\n\ncode: %s \n'\
                % (res.url, res.status_code)


def get_area(token):
    """查询园区列表"""
    url = host + '/api/v1/pub/current/base/area'
    header = {'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token}
    param = {'id': '61c940607a18f300017f51ee'}
    res = session.get(url, headers=header, params=param)
    if res.ok:
        back_code = res.json()['status']
        if back_code != 1:
            return 'area service is error\n\nmessage: %s \n'\
                    % (res.json()['message'])
    else:
        return 'HTTP request error\n\nurl: %s\n\ncode: %s \n'\
                % (res.url, res.status_code)


def get_carlist(token):
    """查询车辆列表"""
    url = host + '/api/v1/pub/current/base/cardevice/monitoring/list'
    header = {'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token}
    payload = json.dumps(
            {'page': 1, 'size': 10})
    res = session.post(url, headers=header, data=payload)
    if res.ok:
        back_code = res.json()['status']
        if back_code != 1:
            return 'cardevice service is error\n\nmessage: %s \n'\
                    % (res.json()['message'])
    else:
        return 'HTTP request error\n\nurl: %s\n\ncode: %s \n'\
                % (res.url, res.status_code)


def get_carstatus(token):
    """获取车辆状态"""
    url = host + '/api/m1/car/last/status'
    header = {'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token}
    payload = json.dumps(
            {'area_id': '61c940607a18f300017f51ee'}
            )
    res = session.post(url, headers=header, data=payload)
    if res.ok:
        back_code = res.json()['status']
        if back_code != 1:
            return 'car_manager service is error\n\nmessage: %s \n'\
                    % (res.json()['message'])
    else:
        return 'HTTP request error\n\nurl: %s\n\ncode: %s \n'\
                % (res.url, res.status_code)


def get_tasklist(token):
    """获取任务列表"""
    url = host + '/api/m1/task'
    header = {'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token}
    res = session.get(url, headers=header)
    if res.ok:
        back_code = res.json()['status']
        if back_code != 1:
            return 'task service is error\n\nmessage: %s \n'\
                    % (res.json()['message'])
    else:
        return 'HTTP request error\n\nurl: %s\n\ncode: %s \n'\
                % (res.url, res.status_code)


def get_company(token):
    """获取公司列表"""
    url = host + '/api/m1/usermanage/company/list'
    header = {'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token}
    res = session.get(url, headers=header)
    if res.ok:
        back_code = res.json()['status']
        if back_code != 1:
            return 'go-admin service is error\n\nmessage: %s \n'\
                    % (res.json()['message'])
    else:
        return 'HTTP request error\n\nurl: %s\n\ncode: %s \n'\
                % (res.url, res.status_code)


def get_notice(token):
    """获取通知详情"""
    url = host + '/api/m1/notice/detail/query'
    header = {'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token}
    res = session.get(url, headers=header)
    if res.ok:
        back_code = res.json()['status']
        if back_code != 1:
            return 'notice-center service is error\n\nmessage: %s \n'\
                    % (res.json()['message'])
    else:
        return 'HTTP request error\n\nurl: %s\n\ncode: %s \n'\
                % (res.url, res.status_code)


def get_expressdate(token):
    """获取可配送日期"""
    url = host + '/api/m1/expressbox/wechat/user/order/date'
    header = {'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token}
    param = {'area_id': '6333c9992efa840008a1ab12', 'station_id': 1}
    res = session.get(url, headers=header, params=param)
    if res.ok:
        back_code = res.json()['status']
        if back_code != 1:
            return 'expressbox service is error\n\nmessage: %s \n'\
                    % (res.json()['message'])
    else:
        return 'HTTP request error\n\nurl: %s\n\ncode: %s \n'\
                % (res.url, res.status_code)


def get_summary(token):
    """查询任务数据概览"""
    url = host + '/api/m1/data/task/summary'
    header = {'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token}
    payload = json.dumps(
            {"start_date": "2023-02-01",
             "end_date": "2023-03-01"}
            )
    res = session.post(url, headers=header, data=payload)
    if res.ok:
        back_code = res.json()['status']
        if back_code != 1:
            return 'platform-data service is error\n\nmessage: %s \n'\
                    % (res.json()['message'])
    else:
        return 'HTTP request error\n\nurl: %s\n\ncode: %s \n'\
                % (res.url, res.status_code)


def dingding(title, text):
    """发送钉钉通知"""
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    api_url = 'https://oapi.dingtalk.com/robot/send?access_token=\
39d3986130b060b680b5e6c3747ba7a461c1ba8d80dab3880e0bc35c7405d2a9'
    json_text = {
        "msgtype": "markdown",
        "at": {
            "atMobiles": ["18279367850"],
            "isAtAll": False
        },
        "markdown": {
            "title": title,
            "text": text
        }
    }
    res = requests.post(api_url, json.dumps(json_text), headers=headers)
    print(res.text)


def api_check(function_list: list, token):
    """整体调用,推送告警消息"""
    msg = ''
    for function in function_list:
        res = function(token)
        if res:
            msg += res
    if msg:
        return msg


if __name__ == '__main__':
    function_list = [get_user, get_area, get_carlist, get_carstatus,
                     get_tasklist, get_company, get_notice, get_expressdate,
                     get_summary]
    host_list = ['iov', 'ud3pre', 'ud3test', 'ud3dev']
    for name in host_list:
        if name == 'iov':
            host = f'https://{name}.unity-drive.com'
        else:
            host = f'https://{name}.unity-drive.net'
        token = get_token()
        msg = api_check(function_list, token)
        if msg:
            dingding_msg = "## <font face=KaiTi>后台告警通知 \n \
告警时间: </font> <font face=KaiTi color=\"#008000\">%s</font> \n\n \
<font face=KaiTi>后台环境: </font> \
<font face=KaiTi color=\"#008000\">%s</font> \n\n \
<font face=KaiTi>告警信息: </font> \
<font face=KaiTi color=\"#DC143C\">%s</font> \n\n \
<font face=KaiTi color=\"#1E90FF\">@18279367850 @15697789593</font> \n\n" \
% (now, host, msg)
            dingding('运维助手告警', dingding_msg)
    end_time = time.time()
    print(end_time - pro_start_time)
