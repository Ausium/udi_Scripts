#! /usr/bin/python3.8

import datetime as dt
from zhdate import ZhDate #*注：农历库记得引入
import requests

def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]

def time_parse(today):
    distance_year = (dt.datetime.strptime(str(today.year) + "-01-01", "%Y-%m-%d") - today).days
    if distance_year < 0 :
        distance_year = (dt.datetime.strptime(str(today.year + 1) + "-01-01", "%Y-%m-%d") - today).days

    distance_big_year = (ZhDate(today.year, 1, 1).to_datetime() - today).days
    if distance_big_year < 0 :
        distance_big_year = (ZhDate((today.year + 1), 1, 1).to_datetime() - today).days

    distance_4_5 = (dt.datetime.strptime(str(today.year) + "-04-05", "%Y-%m-%d") - today).days
    if distance_4_5 < 0 :
        distance_4_5 = (dt.datetime.strptime(str(today.year + 1) + "-04-05", "%Y-%m-%d") - today).days

    distance_5_1 = (dt.datetime.strptime(str(today.year) + "-05-01", "%Y-%m-%d") - today).days
    if distance_5_1 < 0 :
        distance_5_1 = (dt.datetime.strptime(str(today.year + 1) + "-05-01", "%Y-%m-%d") - today).days

    distance_5_5 = (ZhDate(today.year, 5, 5).to_datetime() - today).days
    if distance_5_5 < 0 :
        distance_5_5 = (ZhDate(today.year + 1, 5, 5).to_datetime() - today).days

    distance_8_15 = (ZhDate(today.year, 8, 15).to_datetime() - today).days
    if distance_8_15 < 0 :
        distance_8_15 = (ZhDate(today.year + 1, 8, 15).to_datetime() - today).days

    distance_10_1 = (dt.datetime.strptime(str(today.year) + "-10-01", "%Y-%m-%d") - today).days
    if distance_10_1 < 0 :
        distance_10_1 = (dt.datetime.strptime(str(today.year + 1) + "-10-01", "%Y-%m-%d") - today).days

    time_ = [
        {"v_": 5 - 1 - today.weekday(), "title": "周末"}, # 距离周末
        {"v_": distance_year, "title": "元旦"}, # 距离元旦
        {"v_": distance_big_year, "title": "过年"}, # 距离过年
        {"v_": distance_4_5, "title": "清明节"}, # 距离清明
        {"v_": distance_5_1, "title": "劳动节"}, # 距离劳动
        {"v_": distance_5_5, "title": "端午节"}, # 距离端午
        {"v_": distance_8_15, "title": "中秋节"}, # 距离中秋
        {"v_": distance_10_1, "title": "国庆节"}, # 距离国庆
    ]
    time_ = sorted(time_, key = lambda x: x['v_'], reverse = False)
    return time_

def get_weather():
    res = requests.get('http://wttr.in/深圳', params={'format': 4})
    if res.ok:
        return res.text
    else:
        print(res.text)

if __name__ == '__main__':
    holiday = ''
    today = dt.datetime.today()
    time_ = time_parse(today)
    for t_ in time_:
        if t_.get("v_") >= 0:
            holiday += '距离{}还有:{}天\n'.format(t_.get("title"), t_.get("v_"))
    date_new = '{}年{}月{}日 {}'.format(today.year, today.month, today.day, get_week_day(today))
    weather_data = get_weather()
    print(date_new)
    print(weather_data)
    print(holiday)

