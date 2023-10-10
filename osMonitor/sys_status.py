#! /bin/python3
# coding = utf-8
"""系统性能检测和告警脚本"""

import subprocess
import time
from datetime import datetime
import requests
import os
import json
import socket

start_time = time.time()
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open('/etc/hostname', 'r', encoding='utf-8') as f:
    hostname = f.readline().strip('\n')
# IP = requests.get('https://iov.unity-drive.com/ip').text
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(('8.8.8.8', 80))
    IP = s.getsockname()[0]
finally:
    s.close()


def disk():
    """获取磁盘空间"""
    out = subprocess.Popen(
        "df -t xfs -t ext4 -h|grep -v File",
        shell=True,
        stdout=subprocess.PIPE,
        encoding='utf-8'
    )
    outtext = out.communicate()[0]
    _msg = ''
    for line in outtext.strip().split('\n'):
        ratio = int(line.split()[-2].strip('%'))
        if ratio >= 90:
            _msg += '系统磁盘使用率过高，\
            <font color=\"#FF0000\">%s</font> \
            分区剩余空间<font color=\"#FF0000\">%s</font>  \n  '\
                % (line.split()[-1], line.split()[-3])
    return _msg


def memory():
    """获取内存使用率"""
    out = subprocess.Popen(
        "free -b|grep Mem",
        shell=True,
        stdout=subprocess.PIPE,
        encoding='utf-8'
    )
    mem_text = out.communicate()[0].strip('\n')
    free_mem = int(mem_text.split()[-1])
    total_mem = int(mem_text.split()[1])
    free_ratio = free_mem / total_mem
    _msg = ''
    if free_ratio < 0.1:
        _msg += '系统内存使用率过高，当前使用率: \
        <font color=\"#FF0000\">%s%%</font>, \
        剩余内存: <font color=\"#FF0000\">%sM</font>  \n  '\
              % (round(100-free_ratio*100, 2),
                 round(free_mem/1024/1024, 2))
    return _msg


def cpuLoad():
    """系统负载"""
    out = subprocess.Popen(
        "nproc",
        shell=True,
        stdout=subprocess.PIPE,
        encoding='utf-8'
    )
    nproc = int(out.communicate()[0])
    out = subprocess.Popen(
        "uptime",
        shell=True,
        stdout=subprocess.PIPE,
        encoding='utf-8'
    )
    _msg = ''
    text = out.communicate()[0].strip('\n')
    load15 = float(text.split()[-1])
    if load15 > nproc:
        _msg += '当前系统CPU负载过高，15分钟平均负载为: \
        <font color=\"#FF0000\">%s</font>  \n  ' % (load15)
    return _msg


def fileCheck():
    """判断重要文件是否改变"""
    if os.path.isfile("/tmp/md5.hash"):
        out = subprocess.Popen(
            "md5sum -c /tmp/md5.hash",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8'
        )
        status = out.communicate()[1]
        _msg = ''
        if status:
            text = out.communicate()[0].strip('\n')
            for line in text.split('\n'):
                if line.split(':')[1].strip() == 'FAILED':
                    _msg += '重要文件<font color=\"#FF0000\">%s</font>\
                    发送了改变，请上服务器上确认  \n  ' % (line.split(':')[0])
    else:
        out = subprocess.Popen(
            "md5sum /etc/passwd /etc/shadow /etc/sudoers > /tmp/md5.hash",
            shell=True
        )
    return _msg


def conn_check():
    """系统连接数检测"""
    out = subprocess.Popen(
        "netstat -anut4 |grep  -E '^tcp|^udp'|wc -l",
        shell=True,
        stdout=subprocess.PIPE,
        encoding='utf-8'
    )
    conn_num = out.communicate()[0].strip('\n')
    _msg = ''
    if int(conn_num) > 1024:
        _msg += '系统连接数过多，当前系统连接数为\
        <font color=\"#FF0000\">%s</font>  \n  ' % (conn_num)
    return _msg


def port_check():
    """端口检测"""
    port_list = [
        '22', '25', '53', '80', '2017', '8888', '20170', '20171',
        '20172', '45171', '46787', '32345']
    out = subprocess.Popen(
    # centos系统使用/sbin/ss,ubuntu系统直接使用ss就行
        "/sbin/ss -tnl | grep -v State | awk '{print $4}' \
        | awk -F ':' '{print $NF}' | sort -nu",
        shell=True,
        stdout=subprocess.PIPE,
        encoding='utf-8'
    )
    now_portlist = out.communicate()[0].split()
    _msg = ''
    for port in now_portlist:
        if port not in port_list:
            command = "ss -lntp|grep %s" % (port)
            out = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                encoding='utf-8'
            )
            text = out.communicate()[0].split('"')
            if len(text) > 1:
                process_name = text[1]
            else:
                process_name = 'unknow'
            _msg += '<font color=\"#FF0000\">%s</font>端口被打开了, \
            进程名为: <font color=\"#FF0000\">%s</font>  \n  ' \
                % (port, process_name)
    for port in port_list:
        if port not in now_portlist:
            _msg += '<font color=\"#FF0000\">%s</font>端口被关闭了  \n  ' % (port)
    return _msg


def dingding(title, text):
    """将告警信息推送到钉钉"""
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    api_url = 'https://oapi.dingtalk.com/robot/send?access_token\
=876448b37219c8c25860ededf2ca13529588b6348595499d8c526775edbe6500'
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
    res = requests.post(api_url, json.dumps(json_text), headers=headers)
    print(res.text)


if __name__ == '__main__':
    msg = disk()
    msg += memory()
    msg += cpuLoad()
    msg += fileCheck()
    msg += conn_check()
    msg += port_check()
    if msg:
        msg = "## <font face=KaiTi>服务器告警通知 \n \
告警时间:</font>  <font face=KaiTi color=\"#008000\">%s</font>  \n  \
<font face=KaiTi>服务器名称:</font> \
<font face=KaiTi color=\"#008000\">%s</font> \
<font face=KaiTi>服务器IP:</font>  \
<font face=KaiTi color=\"#008000\">%s</font>  \n  " % (now, hostname, IP) + msg
        # print(msg)
        dingding('光之使者告警', msg)
    end_time = time.time()
    print(
        '\033[32mProgram time consuming: %s\033[0m'
        % (end_time - start_time))
