#! /usr/bin/python3
# coding=utf-8

import json
import subprocess
from datetime import datetime
import socket
import requests

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open('/etc/hostname', 'r', encoding='utf-8') as f:
    hostname = f.readline().strip('\n')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(('8.8.8.8', 80))
    IP = s.getsockname()[0]
finally:
    s.close()

def dingding(title, text):
    """将告警信息推送到钉钉"""
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    api_url = 'https://oapi.dingtalk.com/robot/send?access_token=39d3986130b060b680b5e6c3747ba7a461c1ba8d80dab3880e0bc35c7405d2a9'
    json_text = {
        "msgtype": "markdown",
        "at": {
            "atMobiles": ["18279367850"],
            "isAtall": False
        },
        "markdown": {
            "title": title,
            "text": text
        }
    }
    res = requests.post(api_url, json.dumps(json_text), headers=headers)
    print(res.text)

def scan():
    res = subprocess.run(
            ["clamscan", "-ri", "/", "--max-dir-recursion=3", "--max-filesize=50M"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
    res_code = res.returncode
    stdout = res.stdout.decode()
    return res_code, stdout.replace('\n', ' \n\n')


if __name__ == '__main__':
    res_code,stderr_msg = scan()
    if res_code == 1:
        msg = "## <font face=KaiTi>服务器病毒文件通知 \n \
告警时间:</font>  <font face=KaiTi color=\"#008000\">%s</font>  \n\n  \
<font face=KaiTi>服务器名称:</font> \
<font face=KaiTi color=\"#008000\">%s</font> \
<font face=KaiTi>服务器IP:</font>  \
<font face=KaiTi color=\"#008000\">%s</font>  \n\n \
<font face=KaiTi>告警信息: </font> \n\n \
<font face=KaiTi color=\"#DC143C\">%s</font> \n\n \
<font face=KaiTi color=\"#1E90FF\">@18279367850</font> \n\n" \
% (now, hostname, IP, stderr_msg)
        dingding('运维助手告警', msg)
