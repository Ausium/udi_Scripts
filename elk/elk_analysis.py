#! /usr/bin/python
# coding=utf8
# 调用elk的接口获取nginx的相关数据

from elasticsearch import Elasticsearch
import datetime
import time
import threading
import requests
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Line
from pyecharts.charts import Map
from pyecharts.charts import Bar
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot

import pymongo
from qqwry import QQwry

pro_start = time.time()
max_connections = 1000
pool_sema = threading.Semaphore(max_connections)

es = Elasticsearch(["http://119.23.186.115:9200"], basic_auth=("elastic", "changeme"))
today = datetime.date.today()
#end_time= str(today) + 'T00:00:00.000+0800'
start_time = str(today - datetime.timedelta(days=1)) + 'T00:00:00.000+0800'
end_time = str(today - datetime.timedelta(days=1)) + 'T23:59:59.000+0800'
web_host = 'iov.unity-drive.net'
query = {"bool" : {
            "must": [],
            "filter": [
                    {
                        "bool": {
                            "should": [
                                {
                                    "match_phrase": {
                                        "http_host": web_host
                                        }
                                }
                                ],
                            "minimum_should_match": 1
                            }
                    },
            {
                "range":{
                    "@timestamp":{
                        "format": "strict_date_optional_time",
                        "gte": start_time,
                        "lte": end_time
                        }
                    }
            }
                ]
            }
    }
# pv和uv
def http_total():
    _query_res = es.search(index="nginx*", query=query, scroll='5m')
    _pv = _query_res['hits']['total']['value']
    _aggs = {
            "0": {
                "cardinality": {
                    "field": "remote_addr.keyword"
                    }
                }
            }
    _query_res = es.search(index="nginx*", query=query, aggs=_aggs, size=0)
    _uv =  _query_res['aggregations']['0']['value']
    return _pv, _uv

# 聚合查询,各字段统计
def http_log(_uv, _pv):
    _httpcode_sum = {}
    _http_req_method = {}
    _ip_sum = {}
    _http_agent = {}
    _http_url = {}
    _aggs = {
        "0": {
        "terms": {
            "field": "http_status.keyword",
            "order": {
                "_count": "desc"
                    },
            "size": 20
                }
            },
        "1": {
            "sum" : {
                    "field": "body_sent_bytes"
                    }
            },
        "2": {
            "terms": {
                    "field": "request_method.keyword",
                    "order": {
                        "_count": "desc"
                        }
                    }
            },
        "3": {
                "terms": {
                    "field": "remote_addr.keyword",
                    "order": {
                        "_count": "desc"
                        },
                    "size": _uv+10
                    }
            },
        "4": {
            "terms": {
                    "field": "http_user_agent.keyword",
                    "order" : {
                        "_count": "desc"
                        },
                    "size": _pv
                    }
            },
        "5": {
            "terms": {
                    "field": "uri.keyword",
                    "order": {
                        "_count": "desc"
                        },
                    "size": 10
                    }
            }
    }
    _query_res = es.search(index="nginx*", query=query, aggs=_aggs,  size=0)
    for i in _query_res['aggregations']['0']['buckets']:
        _httpcode_sum[i['key']] = i['doc_count']
    _net_out = _query_res['aggregations']['1']['value']
    _net_out = round(_net_out/1024/1024, 2)
    for i in _query_res['aggregations']['2']['buckets']:
        _http_req_method[i['key']] = i['doc_count']
    for i in _query_res['aggregations']['3']['buckets']:
        _ip_sum[i['key']] = i['doc_count']
    for i in _query_res['aggregations']['4']['buckets']:
        _http_agent[i['key']] =  i['doc_count']
    _sort_http_agent = dict(sorted(_http_agent.items(), key=lambda item: item[1], reverse=True))
    _http_agent.clear()
    for key, value in _sort_http_agent.items():
        if 'MicroMessenger' in key:
            _http_agent['WeChat'] = _http_agent.get('WeChat', 0) + value
        elif 'Edg' in key:
            _http_agent['Edge'] = _http_agent.get('Edge', 0) + value
        elif 'Chrome' in key:
            _http_agent['Chrome'] = _http_agent.get('Chrome', 0) + value
        elif 'Safari' in key:
            _http_agent['Safari'] = _http_agent.get('Safari', 0) + value
        elif 'Firefox' in key:
            _http_agent['Firefox'] = _http_agent.get('Firefox', 0) + value
        elif 'okhttp' in key:
            _http_agent['Android APP'] = _http_agent.get('Android APP', 0) + value
        elif 'python-requests' in key:
            _http_agent['Python'] = _http_agent.get('Python', 0) + value
        elif 'Android-' in key:
            _http_agent[key] = value
        elif 'Go-http-client' in key:
            _http_agent['Go-client'] = _http_agent.get('Go-cliet', 0) + value
        elif 'Apache-HttpClient' in key:
            _http_agent['Apache-Client'] = _http_agent.get('Apache-Client', 0) + value
        else:
            _http_agent['其他'] = _http_agent.get('其他', 0) + value
    for i in _query_res['aggregations']['5']['buckets']:
        _http_url[i['key']] = i['doc_count']
    return _httpcode_sum, _net_out, _http_req_method, _ip_sum, _http_agent, _http_url



# IP归属地统计
def ip_search(ip, num, _city_sum: dict):
    pool_sema.acquire()
    url = "http://whois.pconline.com.cn/ip.jsp"
    params = {'ip': ip, 'level': 1}
    try:
        response = requests.get(url, params=params, timeout=15)
    except Exception as e:
        print(e)
    else:
        if response.ok:
            if not response.text.isspace():
                city = response.text.split()[0]
                _city_sum[city] = _city_sum.get(city, 0) + num
            else:
                params = {'ip': ip}
                try:
                    response = requests.get(url, params=params, timeout=10)
                except Exception as e:
                    print(e)
                else:
                    city = response.text.split()[0]
                    _city_sum[city] = _city_sum.get(city, 0) + num
        else:
            print('接口错误: ', response.reason)
    pool_sema.release()

# 本地数据库查询,运营商统计
def ip_search_ope(ip, num, _city_sum: dict):
    pool_sema.acquire()
    with os.popen('nali ' + ip) as f:
        ope = f.read().split('[')[1][:-3]
        _city_sum[ope] = _city_sum.get(ope, 0) + num
    pool_sema.release()

# 直接使用本地的纯真数据库
def ip_search_v2(ip, num, _city_sum: dict, _uv_city_sum:dict,  _ope_sum: dict, _uv_ope_sum:dict):
    pool_sema.acquire()
    city = q.lookup(ip)
    ope =  city[1]
    city = city[0][:3]
    if city == '中国':
        city = '其他'
    if '移动' in ope:
        ope = '移动'
    elif '联通' in ope:
        ope = '联通'
    elif '电信' in ope:
        ope = '电信'
    elif '阿里云' in ope:
        ope = '阿里云'
    _city_sum[city] = _city_sum.get(city, 0) + num
    _uv_city_sum[city] = _uv_city_sum.get(city, 0) + 1
    _ope_sum[ope] = _ope_sum.get(ope, 0) + num
    _uv_ope_sum[ope] = _uv_ope_sum.get(ope, 0) + 1
    pool_sema.release()

# 多线程调用
def th_ip_search(function, _ip_sum: dict):
    _city_sum = {}
    _uv_city_sum = {}
    _ope_sum = {}
    _uv_ope_sum = {}
    _sort_city_sum = {}
    _sort_ope_sum = {}
    for ip, num in _ip_sum.items():
        thread = threading.Thread(target=function, args=(ip, num, _city_sum, _uv_city_sum, _ope_sum, _uv_ope_sum))
        thread.start()
    thread.join()
    _sort_city_sum = dict(sorted(_city_sum.items(), key=lambda item: item[1], reverse=True))
    _sort_ope_sum = dict(sorted(_ope_sum.items(), key=lambda item: item[1], reverse=True))
    _sort_uv_city_sum = dict(sorted(_uv_city_sum.items(), key=lambda item: item[1], reverse=True))
    _sort_uv_ope_sum = dict(sorted(_uv_ope_sum.items(), key=lambda item: item[1], reverse=True))
    return _sort_city_sum, _sort_ope_sum, _sort_uv_city_sum, _sort_uv_ope_sum


# 每日pv，uv数据
def http_days(_query, day):
    _pv_days_sum = {}
    _uv_days_sum = {}
    new_start_time = str(today - datetime.timedelta(days=day)) + 'T00:00:00.000+0800'
    _query['bool']['filter'][1]['range']['@timestamp']['gte'] = new_start_time
    _aggs = {
            "0": {
                "date_histogram": {
                "field": "@timestamp",
                "calendar_interval": "1d",
                "time_zone": "Asia/Shanghai"
                },
                "aggs": {
                    "1": {
                        "cardinality": {
                            "field": "remote_addr.keyword"
                            }
                        }
                    }
                }
            }
    _query_res = es.search(index="nginx*", query=_query, aggs=_aggs,  size=0)
    for i in _query_res['aggregations']['0']['buckets']:
        key = i['key_as_string'].split('T')[0]
        _pv_days_sum[key] = i['doc_count']
        _uv_days_sum[key] = i['1']['value']
    return _pv_days_sum, _uv_days_sum

# 平台故障统计
def platform_failure(_httpcode_sum):
    client = "mongodb://admin:root123@10.10.10.13:27017/admin"
    mongo = pymongo.MongoClient(client)
    my_db = mongo['nginx_data']
    my_collection = my_db['failure_num']
    total_sum = 0
    code_sum = 0
    for code, value in _httpcode_sum.items():
        total_sum += value
        if code[0] == '5':
            code_sum += value
    per_code = code_sum / total_sum
    if per_code > 0.05:
        today_failure_num = 1
    else:
        today_failure_num = 0
    log_day = str(today - datetime.timedelta(days=1))
    document = { 'date': log_day, 'num': today_failure_num }
    lastdata = my_collection.find_one(sort=[('_id', -1)])
    if lastdata['date'] == log_day:
        my_collection.update_one({"date": log_day}, {"$set": {"num": today_failure_num}})
    else:
        my_collection.insert_one(document)
    new_year = int(today.year)
    new_month = int(today.month)
    month_failure_num = 0
    for doc in my_collection.find():
        year = int(doc['date'].split('-')[0])
        month = int(doc['date'].split('-')[1])
        if year == new_year and month == new_month:
            month_failure_num += doc['num']
    return today_failure_num, month_failure_num


# 绘制饼图
def pie_chart(data, title) -> Pie:
    width = "1000px"
    height = "500px"
    c = (
        Pie(init_opts=opts.InitOpts(width=width, height=height, bg_color="white", page_title="Nginx日志分析",
                                    js_host="/home/udi/.config/"))
        .add("", [list(z) for z in data.items()], radius=[0, 100], center=["50%", "50%"])
        .set_global_opts(title_opts=opts.TitleOpts(title=title,pos_left="center"),legend_opts=opts.LegendOpts(orient="vertical",pos_top="15%", pos_left="2%"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        .render("pie.html")
        )
    return c


# 绘制折线图
def line_chart(_pv_days:dict,_uv_days:dict):
    c = (
         Line(init_opts=opts.InitOpts(width="880px", height="450px", bg_color="white", page_title="Nginx日志分析",
                                      js_host='/home/udi/.config/'))
         .set_global_opts(
             title_opts=opts.TitleOpts(title='7日数据趋势'),
             yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(formatter="{value} PV")
            ),
             legend_opts=opts.LegendOpts(legend_icon='circle')
         )
         .add_xaxis(xaxis_data=[ i for i in _pv_days.keys()])
         .add_yaxis(
             series_name="PV",
             y_axis=[ i for i in _pv_days.values()],
             linestyle_opts=opts.LineStyleOpts(width=5),
             itemstyle_opts=opts.ItemStyleOpts(color='#65f2d6'),
             is_smooth=True
         )
         .extend_axis(
             yaxis=opts.AxisOpts(
                 axislabel_opts=opts.LabelOpts(formatter="{value} UV"), interval=50
                 )
             )
     )
    c2 = (
         Line(init_opts=opts.InitOpts(width="880px", height="450px", js_host='/home/udi/.config/'))
         .add_xaxis(xaxis_data=[ i for i in _pv_days.keys() ])
         .add_yaxis(
             series_name = "UV",
             y_axis=[ i for i in _uv_days.values() ],
             linestyle_opts=opts.LineStyleOpts(width=5),
             itemstyle_opts=opts.ItemStyleOpts(color='#A0522D'),
             is_smooth=True,
             yaxis_index=1
         )
    )
    c.overlap(c2)
    return c.render('line.html')

# 绘制全国热点图
def map_chart(_city_sum:dict):
    city_name = [ i.strip('省市') for i in _city_sum.keys() ]
    c = (
            Map(init_opts=opts.InitOpts(bg_color="white", js_host='/home/udi/.config/'))
           .add("", [list(z) for z in zip(city_name, _city_sum.values())],
               is_map_symbol_show=False,
               itemstyle_opts={
                "normal": {"areaColor": "#8F999F", "borderColor": "#404A59"},
                "emphasis": {
                    "areaColor": "rgba(255,255,255, 0.5)",
                    },
                },
            )
           .set_global_opts(
               title_opts=opts.TitleOpts(title="用户分布区域", pos_left="center"),
               visualmap_opts=opts.VisualMapOpts(
                   dimension=0,
                   pos_left="10",
                   pos_top="center",
                   min_=min(_city_sum.values()),
                   max_=max(_city_sum.values()),
                   range_text = ["High", "Low"],
                   is_calculable=True,
                   textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                   range_color=["lightskyblue", "yellow", "orangered"],
                   )
               )
            )
    return c.render('map.html')

# 绘制条形图
def bar_chart(data, title_name, y_name) -> Bar:
    x_data = [ i for i in data.keys() ]
    x_data.reverse()
    y_data = [i for i in data.values()]
    y_data.reverse()
    c = (
        Bar(init_opts=opts.InitOpts(width="800px", height="400px", bg_color="white",
            js_host='/home/udi/.config/'))
        .add_xaxis(x_data)
        .add_yaxis("", y_data, color='#65f2d6')
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title_name),
            yaxis_opts=opts.AxisOpts(name=y_name,axislabel_opts=opts.LabelOpts(rotate=15)),
            xaxis_opts=opts.AxisOpts(name='次数')
            )
        .render("bar.html")
        )
    return c

# 多数据条形图
def mixed_bar_chart(data, uv_data, title_name, y_name) -> Bar:
     x_data = [ i for i in data.keys() ]
     x_data.reverse()
     y_data = [i for i in data.values()]
     y_data.reverse()
     y2_data = []
     for i in x_data:
         y2_data.append(uv_data[i])
     c = (
         Bar(init_opts=opts.InitOpts(width="800px", height="400px", bg_color="white",
             js_host='/home/udi/.config/'))
         .add_xaxis(x_data)
         .add_yaxis("PV", y_data, color='#A0522D')
         .add_yaxis("UV", y2_data, color='#65f2d6')
         .reversal_axis()
         .set_series_opts(label_opts=opts.LabelOpts(position="right"))
         .set_global_opts(
             title_opts=opts.TitleOpts(title=title_name),
             yaxis_opts=opts.AxisOpts(name=y_name),
             xaxis_opts=opts.AxisOpts(name='次数')
             )
         .render("bar.html")
         )
     return c
# HTML表格
def html_table(title, table_header, table_content, width="880"):
    html_title='<table border="0" width=%s cellpadding="5" cellspacing="0"  style=""微软雅黑",Helvetica,Arial,sans-serif;font-size:14px;"><tr><td colspan="8" style="text-align:center;border:none;font-size:20px;color:#9e1423;padding-bottom:20px">%s</td></tr>' % (width, title)
    html_header = '<tr>'
    for header in table_header:
        html_header += '<td bgcolor="#E0FFFF" style="font-weight:bold">%s</td>' % (header)
    html_header += '</tr>'
    html_content = ''
    if type(table_content) == list:
        html_content += '<tr>'
        for value in table_content:
            html_content += '<td>%s</td>' % (value)
        html_content += '</tr>'
    elif type(table_content) == dict:
        for key, value in table_content.items():
            html_content += '<tr><td>%s</td><td>%s</td></tr>' % (key, value)
    _html_table = html_title + html_header + html_content + '</table>'
    return _html_table

# 发送邮件,包括文字和图片
def send_mail(subject, content, images, to_mail: list):
    message = MIMEMultipart()
    message.attach(MIMEText(content, 'html', 'utf-8'))
    message['Subject']= Header(subject, 'utf-8')
    smtp_server = 'smtp.exmail.qq.com'
    mail_user = 'noreply@unity-drive.com'
    from_mail = 'caizhisheng<noreply@unity-drive.com>'
    mail_pass = 'vKaWcVGGJkwn3EXB'
    message['From'] = from_mail
    message['To'] = ','.join(to_mail)
    for i, img_name in enumerate(images):
        with open(img_name, 'rb') as f:
            msg_image = MIMEImage(f.read())
            msg_image.add_header('Content-ID', '<image%d>' % (i+1))
            message.attach(msg_image)
    try:
        s = smtplib.SMTP_SSL(smtp_server, '465')
        s.login(mail_user, mail_pass)
        s.sendmail(from_mail, to_mail, message.as_string())
        s.quit()
        print('successfully sent email')
    except smtplib.SMTPException as e:
        print("Error: unable to send email, %s" %e)


if __name__ == '__main__':
    pv,uv = http_total()
    httpcode_sum, net_out, http_method_sum, ip_sum, http_agent_sum, http_url_sum = http_log(uv,pv)
    q = QQwry()
    q.load_file('/home/udi/.local/share/nali/qqwry.dat')
    city_sum, ope_sum, uv_city_sum, uv_ope_sum = th_ip_search(ip_search_v2, ip_sum)
    email_content = '<h3>一、总体统计（%s当日统计数据）</h3>' % (today - datetime.timedelta(days=1))
    today_fail_num, month_fail_num = platform_failure(httpcode_sum)
    table_title = '网端调度平台稳定性故障统计'
    table_header = ['当月故障总数', '当日故障次数']
    table_content = [month_fail_num, today_fail_num]
    email_content += html_table(table_title, table_header, table_content)
    email_content += '<p style="color:red">稳定性指标定义:用户反馈故障次数或HTTP状态码5xx(指程序或服务器请求异常)大于5%视为一次故障</p>'
    table_title = '调度平台用户(当日)活跃数统计'
    table_header = ['PV(用户点击量)', 'UV(访问用户数)', '出口总流量(MB)']
    table_content = [pv, uv, net_out]
    email_content += html_table(table_title, table_header, table_content)
    pv_days_sum, uv_days_sum = http_days(query, 7)
    make_snapshot(snapshot, line_chart(pv_days_sum,uv_days_sum), "days_line.jpeg")
    email_content += '<p><img src="cid:image1" width="880"></p>'
    make_snapshot(snapshot, map_chart(uv_city_sum), "city_map.jpeg")
    email_content += '<p><img src="cid:image2" width="880"></p>'
    table_title = "用户分布区域统计"
    email_content += '<table border="0"><tr><td valign="top">'
    make_snapshot(snapshot, mixed_bar_chart(city_sum, uv_city_sum, table_title, "地区"), "city_bar.jpeg")
    email_content += '<img src="cid:image3" width="600"></td>'
    make_snapshot(snapshot, pie_chart(uv_city_sum, table_title), "city_pie.jpeg")
    email_content += '<td><img src="cid:image4" width="600"></td></tr></table>'
    table_title = "用户的运营商统计"
    email_content += '<table border="0"><tr><td valign="top">'
    make_snapshot(snapshot, mixed_bar_chart(ope_sum, uv_ope_sum, table_title, "运营商"), "ope_bar.jpeg")
    email_content += '<img src="cid:image5" width="600">'
    make_snapshot(snapshot, pie_chart(uv_ope_sum, table_title), "ope_pie.jpeg")
    email_content += '<td><img src="cid:image6" width="600"></td></tr></table><h3>二、详细数据统计  (<a href="http://grafana.unity-drive.net/goto/7OWZeEd4k?orgId=1" target="_blank" rel="noopener noreferrer">更多详情页面请点击此处</a>)</h3>'
    table_title = "客户端来源统计"
    email_content += '<table border="0"><tr><td valign="top">'
    make_snapshot(snapshot, bar_chart(http_agent_sum, table_title, '客户端'), "user_agent_bar.jpeg")
    email_content += '<img src="cid:image7" width="600"></td>'
    make_snapshot(snapshot, pie_chart(http_agent_sum, table_title), "user_agent_pie.jpeg")
    email_content += '<td><img src="cid:image8" width="600"></td></tr></table>'
    table_title = "HTTP状态码统计"
    email_content += '<table border="0"><tr><td valign="top">'
    make_snapshot(snapshot, bar_chart(httpcode_sum, table_title, '状态码'), "httpcode_bar.jpeg")
    email_content += '<img src="cid:image9" width="600">'
    email_content += '<p style="color: red">HTTP状态码含义: 1xx表示信息(如:mqtt)，2xx表示成功，3xx表示重定向，<br>4xx表示客户端错误，5xx表示服务器或后台程序错误<br><a href="https://m.runoob.com/http/http-status-codes.html" target="_blank" rel="noopener noreferrer">点击查看HTTP码详细定义</a></p>'
    make_snapshot(snapshot, pie_chart(httpcode_sum, table_title), "httpcode_pie.jpeg")
    email_content += '</td><td><img src="cid:image10" width="600"></td></tr></table>'
    table_title = '请求路径统计'
    table_header = ['URL', '总数']
    email_content += html_table(table_title, table_header, http_url_sum)
    table_title = "请求方法统计"
    table_header = ['请求方法', '总数']
    email_content += html_table(table_title, table_header, http_method_sum)
    subject = "网端调度平台用户活跃数统计日报(初稿)"
    img_name = ['days_line.jpeg', 'city_map.jpeg', 'city_bar.jpeg', 'city_pie.jpeg', 'ope_bar.jpeg', 'ope_pie.jpeg', 'user_agent_bar.jpeg', 'user_agent_pie.jpeg', 'httpcode_bar.jpeg', 'httpcode_pie.jpeg']
    #to_mail = ['kuanghanqin@unity-drive.com']
    #to_mail = ['caizhisheng@unity-drive.com']
    to_mail = ['wangduanjishubu@unity-drive.com','yaozujie@unity-drive.com','langming@unity-drive.com','liguojian@unity-drive.com']
    send_mail(subject, email_content, img_name, to_mail)
    pro_end = time.time()
    print(pro_end - pro_start)
