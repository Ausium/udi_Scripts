#! /bin/python3
# coding = utf-8

import requests
import threading
import time
import ipaddress
import sys
import os
from datetime import datetime
import json

start_time = time.time()
max_connections = 1000
pool_sema = threading.Semaphore(max_connections)
log_path = "/var/log/nginx/access.log.1"

# 判断IP是否有效
def check_ip_valid(ip):
    try:
        ipaddress.ip_address(ip.strip())
        return True
    except Exception as e:
        return False

# 判断IP是否属于局域网
def is_lan(ip):
    try:
        return ipaddress.ip_address(ip.strip()).is_private
    except Exception as e:
        return False

# 获取日志开始和结束时间
def get_log_time():
    with open(log_path, 'r', encoding='utf-8') as f:
        r = f.readlines()
        _log_start_time = r[0].split()[3].strip('[')
        _log_start_time = datetime.strptime(_log_start_time, "%d/%b/%Y:%H:%M:%S")
        _log_end_time = r[-1].split()[3].strip('[')
        _log_end_time = datetime.strptime(_log_end_time, "%d/%b/%Y:%H:%M:%S")
    return _log_start_time, _log_end_time

# 获取分析后的字段
def analysis_log():
    _ip_sum = {}
    _pv = 0
    _httpcode_sum = {}
    _req_method_sum = {}
    method_list= ['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'CONNECT', 'TRACE']
    _url_sum = {}
    _host_sum = {}
    _user_agent_sum = {}
    net_out_sum = 0
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                ip = line.split()[0]
                httpcode = line.split()[8]
                req_method = line.split()[5].strip('"')
                url = line.split()[6]
                host = line.split()[10].strip('"')
                user_agent = line.split('"')[-2]
                net_out = int(line.split()[9])
            except IndexError as f:
                ...
            except ValueError as f:
                ...
            finally:
                if 'unity-drive' in host:
                    _host_sum[host] = _host_sum.get(host, 0) + 1
                # 这里只分析iov后台的数据
                if host == 'iov.unity-drive.net' or host == 'iov.unity-drive.com':
                    net_out_sum += net_out
                    if check_ip_valid(ip):
                        if not is_lan(ip):
                            _ip_sum[ip] = _ip_sum.get(ip, 0) + 1
                            _pv += 1
                    if httpcode.isdigit() and len(httpcode) == 3:
                        _httpcode_sum[httpcode] = _httpcode_sum.get(httpcode, 0) + 1
                    if req_method in method_list:
                        _req_method_sum[req_method] = _req_method_sum.get(req_method, 0) + 1
                    if url[0] == '/':
                        _url_sum[url] = _url_sum.get(url, 0) + 1
                    _user_agent_sum[user_agent] = _user_agent_sum.get(user_agent, 0) + 1

        _sort_httpcode_sum = dict(sorted(_httpcode_sum.items(), key=lambda item: item[1], reverse=True))
        _sort_req_method_sum = dict(sorted(_req_method_sum.items(), key=lambda item: item[1], reverse=True))
        _sort_url_sum = dict(sorted(_url_sum.items(), key=lambda item: item[1], reverse=True))
        _sort_host_sum = dict(sorted(_host_sum.items(), key=lambda item: item[1], reverse=True))
        _new_user_agent_sum = {}
        for key, value in _user_agent_sum.items():
            if 'MicroMessenger' in key:
                _new_user_agent_sum['WeChat'] = _new_user_agent_sum.get('WeChat', 0) + value
            elif 'Edg' in key:
                _new_user_agent_sum['Edg'] = _new_user_agent_sum.get('Edg', 0) + value
            elif 'Chrome' in key:
                _new_user_agent_sum['Chrome'] = _new_user_agent_sum.get('Chrome', 0) + value
            elif 'Safari' in key:
                _new_user_agent_sum['Safari'] = _new_user_agent_sum.get('Safari', 0) + value
            elif 'Firefox' in key:
                _new_user_agent_sum['Firefox'] = _new_user_agent_sum.get('Firefox', 0) + value
            elif 'okhttp' in key:
                _new_user_agent_sum['Android App'] = _new_user_agent_sum.get('Android App', 0) + value
            elif 'Android-' in key:
                _new_user_agent_sum[key] = value
            elif 'Go-http-client' in key:
                _new_user_agent_sum['Go-client'] = _new_user_agent_sum.get('Go-client', 0) + value
            elif 'Apache-HttpClient' in key:
                _new_user_agent_sum['Apache-Client'] = _new_user_agent_sum.get('Apache-Client', 0) +value
            else:
                _new_user_agent_sum['其他'] = _user_agent_sum.get('其他', 0) + value
        _sort_user_agent_sum = dict(sorted(_new_user_agent_sum.items(), key=lambda item: item[1], reverse=True))
    return _ip_sum, _pv, _sort_httpcode_sum, _sort_req_method_sum, _sort_url_sum, _sort_host_sum, _sort_user_agent_sum, net_out_sum


session = requests.Session()

# 该接口数据查询准确，推荐
def ip_search(ip, num, _city_sum:dict, _uv_city_sum:dict):
    pool_sema.acquire()
    # url = "http://whois.pconline.com.cn/ip.jsp"
    url = "https://api.vore.top/api/IPdata"
    params = {'ip': ip}
    try:
        response = session.get(url, params=params, timeout=5)
    except ConnectTimeout:
        print("request is timeout")
    if response.ok:
        city = response.text.split()[0]
        _city_sum[city] = _city_sum.get(city, 0) + num
        _uv_city_sum[city] = _uv_city_sum.get(city, 0) + 1
    else:
        print('接口错误: ', response.reason)
    pool_sema.release()


# 多线程调用
def th_ip_search(_ip_sum: dict):
    _city_sum = {}
    _uv_city_sum = {}
    for ip, num in _ip_sum.items():
        thread = threading.Thread(target=ip_search, args=(ip, num, _city_sum, _uv_city_sum))
        thread.start()
    thread.join()
    return _city_sum, _uv_city_sum


# 查询单个IP
def query_ip(ip):
    # url = "http://whois.pconline.com.cn/ip.jsp"
    url = "https://api.vore.top/api/IPdata"
    params = {'ip': ip}
    try:
        response = session.get(url, params=params, timeout=5)
    except ConnectTimeout:
        print("request is timeout")
    if response.ok:
        return response.json()['adcode']['n']
    else:
        print('接口错误: ', response.reason)


# 钉钉推送
def dingding(title, text):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    api_url = 'https://oapi.dingtalk.com/robot/send?access_token=39d3986130b060b680b5e6c3747ba7a461c1ba8d80dab3880e0bc35c7405d2a9'
    json_text = {
        "msgtype": "markdown",
        "at": {
            "atMobiles": ["all"],
            "isAtall": False
        },
        "markdown": {
            "title": title,
            "text": text
        }
    }
    res = requests.post(api_url,json.dumps(json_text),headers=headers)
    print(res.text)

if __name__ == '__main__':
    ip_sum, pv, sort_httpcode_sum, sort_req_method_sum, sort_url_sum, sort_host_sum, sort_user_agent_sum, net_out_sum = analysis_log()
    city_sum, uv_city_sum = th_ip_search(ip_sum)
    sort_city_sum = dict(sorted(city_sum.items(), key=lambda item: item[1], reverse=True))
    log_start_time, log_end_time = get_log_time()
    msg = '## <font face=KaiTi>网端调度后台日报</font> \n  日志开始时间: %s  \n  日志结束时间: %s  \n  ' % (log_start_time, log_end_time)
    msg += 'PV(Page View)数: <font color=\"#FF0000\">%d</font>  \n  UV(Unique Visitor)数: <font color=\"#008000\">%d</font>  \n  出口总流量: <font color=\"#FF0000\">%sMB</font>  \n  ' %(pv, len(ip_sum), round(net_out_sum/1024/1024, 2))
    msg += '## <font face=KaiTi>地区统计:</font>  \n  '
    max_len = max(len(x) for x in sort_city_sum.keys()) + 4
    for key,value in sort_city_sum.items():
        new_key = key + "  " * (max_len - len(key))
        msg += '%s\t<font color=\"#FF0000\">%d</font>\t<font color=\"#008000\">%d</font>  \n  ' %(new_key, value, uv_city_sum[key])
    sort_ip_sum = dict(sorted(ip_sum.items(), key=lambda item: item[1], reverse=True))
    msg += '## <font face=KaiTi>TOP10 IP统计:</font>  \n  '
    n = 0
    for key,value in sort_ip_sum.items():
        msg += '<font color=\"#0000FF\">%s</font>\t%s\t<font color=\"#FF0000\">%d</font>  \n  ' %(key,query_ip(key),value)
        n += 1
        if n == 10:
           break
    msg += '## <font face=KaiTi>客户端来源统计:</font>  \n  '
    for key,value in sort_user_agent_sum.items():
        msg += '%-20s\t<font color=\"#FF0000\">%d</font>  \n  ' %(key, value)
    msg += '## <font face=KaiTi>HTTP状态码统计:</font>  \n  '
    for key,value in sort_httpcode_sum.items():
        msg += '%s    <font color=\"#FF0000\">%d</font>  \n  ' %(key, value)
    msg += '## <font face=KaiTi>请求的URL统计:</font>  \n  '
    n = 0
    for key,value in sort_url_sum.items():
        msg += '%-100s    <font color=\"#FF0000\">%d</font>  \n  ' %(key, value)
        n += 1
        if n == 10:
            break
    msg += '## <font face=KaiTi>各网站PV统计:</font>  \n  '
    for key,value in sort_host_sum.items():
        msg += '%s\t<font color=\"#FF0000\">%d</font>  \n  ' %(key, value)
    dingding("nginx日志日报", msg)
    #print(msg)
    end_time = time.time()
    print(end_time - start_time)

