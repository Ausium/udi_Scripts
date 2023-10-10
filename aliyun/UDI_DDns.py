#! /usr/bin/python
# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List

from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
import requests


class Sample:
    def __init__(self):
        pass

    @staticmethod
    # 声明为静态方法，不用实例化也能调用
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Alidns20150109Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的 AccessKey ID,
            access_key_id='LTAI5tBSc5CVgWfbPzVWnrtN',
            # 您的 AccessKey Secret,
            access_key_secret='B4S0LNkjduwJIKh4kE8qeA7urlH6k5'
        )
        # 访问的域名
        config.endpoint = f'alidns.cn-shenzhen.aliyuncs.com'
        return Alidns20150109Client(config)

    @staticmethod
    def main(args: List[str],) -> None:
        client = Sample.create_client('accessKeyId', 'accessKeySecret')
        update_domain_record_request = alidns_20150109_models.UpdateDomainRecordRequest(
            record_id=args[1],
            rr='ddns',
            type='A',
            value=args[0]
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.update_domain_record_with_options(update_domain_record_request, runtime)
            print(update_domain_record_request)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)
            print(error.message)

    @staticmethod
    def get_ip():
        client = Sample.create_client('accessKeyId', 'accessKeySecret')
        describe_domain_records_request = alidns_20150109_models.DescribeDomainRecordsRequest(
            domain_name='unity-drive.net',
            key_word='ddns'
        )
        runtime = util_models.RuntimeOptions()
        try:
            reponse = client.describe_domain_records_with_options(describe_domain_records_request, runtime)
            context = reponse.body.to_map()
            record_id = context['DomainRecords']['Record'][0]['RecordId']
            ip_value = context['DomainRecords']['Record'][0]['Value']
            return record_id, ip_value
        except Exception as error:
            UtilClient.assert_as_string(error.message)
            print(error.message)

    @staticmethod
    # async await python3新增概念,异步调用
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client('accessKeyId', 'accessKeySecret')
        update_domain_record_request = alidns_20150109_models.UpdateDomainRecordRequest(
            record_id='786566520979607552',
            rr='ddns',
            type='A',
            value=args[0]
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.update_domain_record_with_options_async(update_domain_record_request, runtime)
            print(update_domain_record_request)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)
            print(error.message)


def check_lan():
    recordId,old_ip = Sample.get_ip()
    response = requests.get('https://iov.unity-drive.com/ip', timeout=10)
    if response.ok:
        new_ip = response.text
        #old_lan = '.'.join(old_ip.split('.')[0:2])
        #new_lan = '.'.join(new_ip.split('.')[0:2])
        if new_ip == old_ip:
            sys.exit()
        else:
            external_ip = new_ip.split()[0]
            res = requests.post('http://10.10.10.35:8888/?type=udi02',
                                headers={"Content-Type":"application/json"},
                                json={"IP": external_ip})
            Sample.main([external_ip, recordId])
    else:
        print(response.text)


if __name__ == '__main__':
    # Sample.main(sys.argv[1:])
    # 这里传入外网IP
    check_lan()
