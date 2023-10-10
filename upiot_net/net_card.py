#! /bin/python3
"""
物联网卡接口调用
"""

import hashlib
import json
import sqlite3
from datetime import datetime
import requests


API_KEY = 'fb525b41770ae34ae03be75c574362d5498253c5'
API_SECRET = "9cpiGPNy52"
HOST_URL = 'http://ec.upiot.net/api/v2'


def get(params=None):
    """生成get请求签名"""
    if params is None:
        params = {}
    if params:
        params = ''.join(sorted([f'{k}={v}' for k, v in params.items()]))
        sign_string = params + API_SECRET
    else:
        sign_string = API_SECRET
    _sign1 = hashlib.md5(sign_string.encode()).hexdigest()
    return _sign1

def post(request_body):
    """生成post请求签名"""
    params = request_body
    sign_string = params + API_SECRET
    _sign2 = hashlib.md5(sign_string.encode()).hexdigest()
    return _sign2

def billing_group():
    """获取计费组列表"""
    sign = get()
    get_params = {'_sign': sign}
    response = requests.get(f'{HOST_URL}/{API_KEY}/billing_group',\
            params=get_params, timeout=5)
    return response.json()

def card_list(bg_code=None, page=1, per_page=100):
    """获取卡号列表"""
    if bg_code:
        sign = get({'bg_code': bg_code, 'page': page, 'per_page': per_page})
        get_params = {'_sign': sign, 'bg_code': bg_code, 'page': page, 'per_page': per_page}
    else:
        sign = get({'page': page, 'per_page': per_page})
        get_params = {'_sign': sign, 'page': page, 'per_page': per_page}
    response = requests.get(f'{HOST_URL}/{API_KEY}/card_no_list',\
            params=get_params, timeout=5)
    return response.json()

def iccids(num=None):
    """将卡号列表中的iccid过滤出来"""
    iccid_list = []
    data = card_list(per_page=num)['data']['rows']
    for row in data:
        iccid = row['iccid']
        iccid_list.append(iccid)
    return iccid_list


# pool_info('202208')
def pool_info(month=''):
    """流量池计费组信息,不传month默认查本月"""
    if month:
        sign = get({'month': month})
        get_params = {'_sign': sign, 'month': month}
        response = requests.get(f'{HOST_URL}/{API_KEY}/billing_group/pool_info',\
                params=get_params, timeout=5)
    else:
        sign = get()
        get_params = {'_sign': sign}
        response = requests.get(f'{HOST_URL}/{API_KEY}/billing_group/pool_info',
                params=get_params, timeout=5)
    return response.json()

# card(8986112124008444299)
def card(iccid):
    """查询指定物联网卡的信息"""
    sign = get()
    get_params = {'_sign': sign}
    response = requests.get(f'{HOST_URL}/{API_KEY}/card/{iccid}',
            params=get_params, timeout=5)
    return response.json()

# batch_card([8986112124008444299, 8986112124008444298])
def batch_card(iccid_list: list):
    """批量查询物联网卡信息, 注销的卡返回的是空"""
    request_body = '{"iccids":' + json.dumps(iccid_list) + '}'
    sign = post(request_body)
    post_data = request_body
    response = requests.post(f'{HOST_URL}/{API_KEY}/batch/card/info/?_sign={sign}',\
        data=post_data, timeout=5)
    return response.json()

def usagelog_daily(_iccid, _month):
    """查询每日的物联网卡使用量"""
    sign = get()
    get_params = {'_sign': sign}
    response = requests.get(f'{HOST_URL}/{API_KEY}/card/{_iccid}/usagelog/{_month}/delta/',
            params=get_params, timeout=5)
    return response.json()

# usagelog(["8986112124008444299", "8986112124008444298"], '2022-08-01')
def usagelog(iccid_list: list, date):
    """批量查询当日用量信息"""
    request_body='{"iccids":' + json.dumps(iccid_list) + ', "query_date":' + '"' + date + '"' + '}'
    sign = post(request_body)
    # params = (('_sign', sign),)
    post_data = request_body
    response=requests.post(f'{HOST_URL}/{API_KEY}/card/daily/usagelog/\
        ?_sign={sign}', data=post_data, timeout=5)
    return response.json()

# month_use("8986112124008444299,8986112124008444298", '202301')
def month_use(iccid_list, month=""):
    """物联网卡月使用量信息"""
    request_body='{"msisdns":' + '[' + iccid_list +']'+ ', "month":' + '"' + month + '"' + '}'
    sign = post(request_body)
    response = requests.post(f'{HOST_URL}/{API_KEY}/card_usage_info/?_sign={sign}',
            data=request_body, timeout=5)
    return response.json()


def card_status(_iccid):
    """物联卡状态"""
    sign = get()
    get_params = {'_sign': sign}
    response = requests.get(f'{HOST_URL}/{API_KEY}/card/{_iccid}/status/', params=get_params,
            timeout=5)
    return response.json()


def expiry_date():
    """本月到期卡查询"""
    sign = get()
    get_params = {'_sign': sign}
    response = requests.get(f'{HOST_URL}/{API_KEY}/batch/card/expiry_date/', params=get_params,
            timeout = 5)
    return response.json()

def carid2iccid(_carid:str, iccid=None):
    """将carID和iccid的对应关系存入数据库中"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('upoit.db')
    cursor = conn.cursor()
    cursor.execute("select name from sqlite_master where type='table' AND name='car2iccid';")
    res = cursor.fetchall()
    if res:
        sql = f"select iccid from car2iccid where carId='{_carid}';"
        cursor.execute(sql)
        res = cursor.fetchone()
        if res:
            #print(f'{_carid} 对应的iccid为: {res[0]}')
            if iccid:
                sql = f"update car2iccid set iccid='{iccid}', updatetime='{now}' where\
                        carId='{_carid}'"
                cursor.execute(sql)
                conn.commit()
                print('update data successed !')
            else:
                return res[0]
        elif not res and iccid:
            sql = f"insert into car2iccid(carId, createtime, iccid) values('{_carid}', '{now}',\
                '{iccid}')"
            cursor.execute(sql)
            conn.commit()
            print('insert data successed !')
        elif _carid and not res:
            return None
        else:
            sql = "select carId,iccid from car2iccid"
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
    else:
        sql = "create table car2iccid (id INTEGER PRIMARY KEY AUTOINCREMENT,\
                createtime NUMERIC, updatetime NUMERIC, carId TEXT, iccid TEXT)"
        cursor.execute(sql)
        conn.commit()
        print('create table successed !')
    return None

def mem_list():
    """菜单"""
    _mem = ['查询所有车辆ID与iccid的对应关系', '查询所有车辆的流量消耗情况', '查询指定车辆的流量消耗情况',
        '查询所有流量池计费组统计信息', '查询车辆对应的流量卡信息', '查询当月流量消耗情况',
        '查询物联卡状态', '查询本月到期卡', '修改或新建车辆ID与iccid记录']
    _card_stat = {'00': '正使用', '01': '测试期', '02': '停机', '03': '预销号', '04': '销号', '11':
    '沉默期', '12': '停机保号', '99': '未知'}
    _carrier = {0: '中国移动', 1: '中国联通', 2: '中国电信'}
    print(f"{'一清无人车流量查询服务':^30}\n")
    for num, value in enumerate(_mem):
        print(f"{num+1}. {value:^23}")
    option = input('请输入选项前的编号[1-9]: ')
    match option:
        case '1':
            iccid_list = carid2iccid(None)
            for item in iccid_list:
                print(f"车辆ID: {item[0]}, ICCID: {item[1]}")
        case '2':
            iccid_list = carid2iccid(None)
            for item in iccid_list:
                _msg = card(item[1])
                print('车辆ID: ', item[0])
                print('ICCID: ', _msg['data']['iccid'])
                print('IMSI: ', _msg['data']['imsi'])
                print('运营商: ', _msg['data']['carrier'])
                print('短信端口号: ', _msg['data']['sp_code'])
                print('套餐大小: ', _msg['data']['data_plan'], 'M')
                print('计费结束日期: ', _msg['data']['expiry_date'])
                print("当月使用流量: ", _msg['data']['data_usage'], 'M')
                print("卡状态: ", _card_stat[_msg['data']['account_status']])
                print("是否激活: ", _msg['data']['active'])
                print("测试期起始日期: ", _msg['data']['test_valid_date'])
                print("沉默期起始日期: ", _msg['data']['silent_valid_date'])
                print("出库日期: ", _msg['data']['outbound_date'])
                print("激活日期: ", _msg['data']['active_date'])
                print("是否支持短信: ", _msg['data']['support_sms'])
                print("剩余流量: ", _msg['data']['data_balance'], 'M')
                print("测试期已用流量: ", _msg['data']['test_used_data_usage'], 'M')
                print("sim卡类型: ", _msg['data']['sim_type'])
                print("是否是累计卡: ", _msg['data']['accumulated'])
                print("计费组ID: ", _msg['data']['code'])
                print("总流量: ", _msg['data']['data_traffic_amount'], 'M')
                print("计费起始日期: ", _msg['data']['valid_date'])
                print("超出用量: ", _msg['data']['out_data_usage'], 'M')
                print("标签: ", _msg['data']['customize_comment'], '\n')
        case '3':
            _date = datetime.now().strftime('%Y%m')
            _carid = input('please into carId: ')
            _iccid = carid2iccid(_carid)
            if  _iccid:
                _msg = usagelog_daily(_iccid, _date)
                print(f'{_carid}小车每日用量统计: ')
                for item in _msg['data']['rows']:
                    print(f'{item["date"]} 单日用量为: {item["data_usage"]}(M)')
            else:
                print(f'你输入的carid:{_carid}不存在')
        case '4':
            _msg = pool_info()
            for row in _msg['data']['rows']:
                print('运营商: ', row['carrier'])
                print('计费组代码: ', row['bg_code'])
                print('套餐名称: ', row['name'])
                print('套餐大小: ', row['data_plan'], 'M')
                print('流量卡总数: ', row['total_card_count'])
                print('激活的流量卡数: ', row['active_card_count'])
                print('流量池大小: ', row['pool_size'], 'M')
                print('激活卡已用流量: ', row['data_usage'], 'M')
                print('流量模式(0: 单卡, 1:共享(流量池)): ', row['billing_mode'], end='\n\n')
        case '5':
            _carid = input('please into carId: ')
            _iccid = carid2iccid(_carid)
            if _iccid:
                _msg = card(_iccid)
                print('车辆ID: ', _carid)
                print('ICCID: ', _msg['data']['iccid'])
                print('运营商: ', _msg['data']['carrier'])
                print('短信端口号: ', _msg['data']['sp_code'])
                print('套餐大小: ', _msg['data']['data_plan'], 'M')
                print('计费结束日期: ', _msg['data']['expiry_date'])
                print("当月使用流量: ", _msg['data']['data_usage'], 'M')
                print("卡状态: ", _card_stat[_msg['data']['account_status']])
                print("是否激活: ", _msg['data']['active'])
                print("测试期起始日期: ", _msg['data']['test_valid_date'])
                print("沉默期起始日期: ", _msg['data']['silent_valid_date'])
                print("出库日期: ", _msg['data']['outbound_date'])
                print("激活日期: ", _msg['data']['active_date'])
                print("是否支持短信: ", _msg['data']['support_sms'])
                print("剩余流量: ", _msg['data']['data_balance'], 'M')
                print("测试期已用流量: ", _msg['data']['test_used_data_usage'], 'M')
                print("sim卡类型: ", _msg['data']['sim_type'])
                print("是否是累计卡: ", _msg['data']['accumulated'])
                print("计费组ID: ", _msg['data']['code'])
                print("总流量: ", _msg['data']['data_traffic_amount'], 'M')
                print("计费起始日期: ", _msg['data']['valid_date'])
                print("超出用量: ", _msg['data']['out_data_usage'], 'M')
                print("标签: ", _msg['data']['customize_comment'], '\n')
            else:
                print(f'你输入的carid:{_carid}不存在')
        case '6':
            _carid = input('please into carId: ')
            _iccid = carid2iccid(_carid)
            if _iccid:
                _msg = month_use(_iccid)
                for row in _msg['data']['rows']:
                    print("msisdn号: ", row['msisdn'])
                    print("iccid号: ", row['iccid'])
                    print("imsi号: ", row['imsi'])
                    print("卡状态: ", _card_stat[row['account_status']])
                    print("运营商: ", _carrier[row['carrier']])
                    print("流量用量: ", row['data_usage'], 'M')
                    print("剩余流量: ", row['data_balance'], 'M')
                    print("流量套餐: ", row['data_plan'])
                    print("语音用量: ", row['voice_usage'])
                    print("剩余语音: ", row['voice_balance'])
                    print("语音套餐: ", row['voice_plan'])
                    print("上行短信数量: ", row['sms_mo'])
                    print("下行短信数量: ", row['sms_mt'])
                    print("计费起始日期: ", row['valid_date'])
                    print("计费结束日期: ", row['expiry_date'])
                    print("测试期起始日期: ", row['test_valid_date'])
                    print("沉默期起始日期: ", row['test_data_usage'])
                    print("激活日期: ", row["active_date"])
                    print("出库日期: ", row['outbound_date'])
                    print("是否支持短信: ", row['support_sms'])
                    print("是否支持语音: ", row['support_voice'])
                    print("查询日期: ", row['month'])
                    print("流量更新时间: ", row['updated_time'])
            else:
                print(f'你输入的carid:{_carid}不存在')
        case '7':
            _carid = input('please into carId: ')
            _iccid = carid2iccid(_carid)
            if _iccid:
                _msg = card_status(_iccid)
                print("开机状态: ", _msg['data']['power_status_msg'])
                print("工作状态: ", _msg['data']['gprs_status_msg'])
                print("IP: ", _msg['data'].get('IP', None))
                print("网络接入类型: ", _msg['data'].get('RAT', None))
                print("无线接入模式: ", _msg['data']['net_model'])
                print("最后下线时间: ", _msg['data']['stop_time'])
                print("最后上线时间: ", _msg['data']['start_time'])
            else:
                print(f'你输入的carid:{_carid}不存在')
        case '8':
            _msg = expiry_date()
            if _msg['code'] == 200:
                for row in _msg['data']['rows']:
                    print(row)
            else:
                print(_msg)
        case '9':
            _carid = input('please into carId: ')
            _iccid = input('please into iccid: ')
            if _carid and _iccid:
                _msg = carid2iccid(_carid, _iccid)
                if _msg:
                    print(_msg)
            else:
                print('carid and iccid cannot empty')
        case _:
            print('please into correct number')

if __name__ == '__main__':
    # iccid_list = iccids(50)
    # response2 = batch_card(iccid_list)
    #now_carId = input('please into carID: ')
    #now_iccid = input('please into iccid: ')
    mem_list()
    #res = month_use("8986112124008444299, 8986112124008444298")
    #print(res)
