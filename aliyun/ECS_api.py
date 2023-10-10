#! /usr/bin/python
# coding=utf8

import sys

from typing import List

from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
import requests
import time
#import dns.resolver
import socket

class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Ecs20140526Client:
        config = open_api_models.Config(
            # 您的 AccessKey ID,
            access_key_id='LTAI5tBSc5CVgWfbPzVWnrtN',
            # 您的 AccessKey Secret,
            access_key_secret='B4S0LNkjduwJIKh4kE8qeA7urlH6k5'
        )
        # 访问的域名
        config.endpoint = f'ecs.cn-shenzhen.aliyuncs.com'
        return Ecs20140526Client(config)

    # 新增入方向的安全组规则
    @staticmethod
    def authorize_security(
        args: List[str],
    ) -> None:
        client = Sample.create_client('accessKeyId', 'accessKeySecret')
        permissions_0 = ecs_20140526_models.AuthorizeSecurityGroupRequestPermissions(
            ip_protocol='TCP',
            source_cidr_ip=args[0],
            port_range=args[1],
            description=args[2]
        )
        authorize_security_group_request = ecs_20140526_models.AuthorizeSecurityGroupRequest(
            region_id='cn-shenzhen',
            security_group_id=args[3],
            permissions=[
                permissions_0
            ]
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.authorize_security_group_with_options(authorize_security_group_request, runtime)
            print("新增安全组",  authorize_security_group_request)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)
            print(error.message)

    # 删除入方向的安全组规则
    @staticmethod
    def revoke_security(
        args: List[str],
    ) -> None:
        client = Sample.create_client('accessKeyId', 'accessKeySecret')
        permissions_0 = ecs_20140526_models.RevokeSecurityGroupRequestPermissions(
            source_cidr_ip=args[0],
            ip_protocol='TCP',
            port_range=args[1],
            description=args[2]
        )
        revoke_security_group_request = ecs_20140526_models.RevokeSecurityGroupRequest(
            region_id='cn-shenzhen',
            security_group_id=args[3],
            permissions=[
                permissions_0
            ]
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.revoke_security_group_with_options(revoke_security_group_request, runtime)
            print("删除安全组", revoke_security_group_request)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)
            print(error.message)
def check_lan():
    #response = requests.get('https://iov.unity-drive.net/ip', timeout=5)
    #external_ip = response.text.strip()
    #external_ip1 = str(dns.resolver.resolve('ddns.unity-drive.net', 'A').rrset[0])
    #external_ip2 = str(dns.resolver.resolve('udi01.picp.vip', 'A').rrset[0])
    external_ip1 = socket.gethostbyname('ddns.unity-drive.net')
    external_ip2 = socket.gethostbyname('udi01.picp.vip')
    today = time.strftime('%Y-%m-%d %H:%M')
    with open('/home/udi/python/aliyun/history_ip_1.txt', 'r', encoding='utf-8') as f:
        old_ip1 = f.readlines()[-1].split()[-1]
    with open('/home/udi/python/aliyun/history_ip_2.txt', 'r', encoding='utf-8') as f:
        old_ip2 = f.readlines()[-1].split()[-1]
    old_lan1 = '.'.join(old_ip1.split('.')[:2])
    new_lan1 = '.'.join(external_ip1.split('.')[:2])
    if old_ip1 != external_ip1:
        with open('/home/udi/python/aliyun/history_ip_1.txt', 'a', encoding='utf-8') as f:
            f.write(today+'\t'+external_ip1+'\n')
        if old_lan1 != new_lan1:
            new_security_lan1 = new_lan1 + '.0.0/16'
            old_security_lan1 = old_lan1 + '.0.0/16'
            Sample.authorize_security([new_security_lan1, '9200/9200', 'elasticsearch对公司开放', 'sg-wz99cloitj9s2b0p3udv'])
            Sample.revoke_security([old_security_lan1,'9200/9200','elasticsearch对公司开放','sg-wz99cloitj9s2b0p3udv'])
            Sample.authorize_security([new_security_lan1, '9090/9090', 'prometheus对外端口', 'sg-wz9fqq342f0gjilnzyou'])
            Sample.revoke_security([old_security_lan1,'9090/9090','prometheus对外端口','sg-wz9fqq342f0gjilnzyou'])


    if old_ip2 == external_ip2:
        sys.exit(0)
    else:
        old_lan2 = '.'.join(old_ip2.split('.')[:2])
        new_lan2 = '.'.join(external_ip2.split('.')[:2])
        with open('/home/udi/python/aliyun/history_ip_2.txt', 'a', encoding='utf-8') as f:
             f.write(today+'\t'+external_ip2+'\n')
        res = requests.post('http://10.10.10.35:8888/?type=udi01', headers={"Content-Type":"application/json"}, json={"IP": external_ip2})
        if old_lan2 == new_lan2:
            sys.exit(0)
        else:
            new_security_lan2 = new_lan2 + '.0.0/16'
            Sample.authorize_security([new_security_lan2, '9090/9090', 'prometheus对外端口-udi01', 'sg-wz9fqq342f0gjilnzyou'])
            if old_lan2 != old_lan1 and old_lan2 != new_lan1:
                old_security_lan2 = old_lan2 + '.0.0/16'
                Sample.revoke_security([old_security_lan2,'9090/9090','prometheus对外端口-udi01','sg-wz9fqq342f0gjilnzyou'])

if __name__ == '__main__':
    #Sample.main(sys.argv[1:])
    check_lan()
