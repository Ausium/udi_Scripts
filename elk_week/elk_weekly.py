#! /usr/bin/python3.8
# coding=utf-8

from elasticsearch import Elasticsearch
import pymongo
import datetime
import time
import threading
from qqwry import QQwry
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Map, Pie
# from pyecharts.globals import ThemeType
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

program_start_time = time.time()
max_connections = 1000
pool_sema = threading.Semaphore(max_connections)

es = Elasticsearch(["http://119.23.186.115:9200"],
                   basic_auth=("elastic", "changeme"))
today = datetime.date.today()
start_time = str(today - datetime.timedelta(days=7)) + 'T00:00:00.000+0800'
end_time = str(today - datetime.timedelta(days=1)) + 'T23:59:59.000+0800'
web_host = 'iov.unity-drive.net'

query = {
    "bool": {
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
                        "range": {
                            "@timestamp": {
                                "format": "strict_date_optional_time",
                                "gte": start_time,
                                "lte": end_time
                            }
                        }
                    }
                    ]
                }
        }


def http_log():
    """聚合查询nginx日志"""
    _aggs = {
        "all": {
            "date_histogram": {
                "field": "@timestamp",
                "calendar_interval": "1d",
                "time_zone": "Asia/Shanghai"
                },
            "aggs": {
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
                    "sum": {
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
                        "size": 10000
                        }
                    },
                "4": {
                    "terms": {
                        "field": "http_user_agent.keyword",
                        "order": {
                            "_count": "desc"
                            },
                        "size": 2000000
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
                    },
                "6": {
                    "cardinality": {
                        "field": "remote_addr.keyword"
                        }
                    }
                }
        }
    }
    daily_code_sum = {}
    daily_net_out = {}
    daily_req_method = {}
    daily_ip_sum = {}
    daily_user_agent = {}
    daily_url_sum = {}
    daily_pv_sum = {}
    daily_uv_sum = {}
    _query_res = es.search(index="nginx*", query=query, aggs=_aggs,  size=0)
    for buckets in _query_res['aggregations']['all']['buckets']:
        time_day = buckets['key_as_string'].split('T')[0]
        daily_code_sum[time_day] = {}
        daily_req_method[time_day] = {}
        daily_ip_sum[time_day] = {}
        daily_user_agent[time_day] = {}
        daily_url_sum[time_day] = {}
        daily_pv_sum[time_day] = buckets['doc_count']
        daily_uv_sum[time_day] = buckets['6']['value']
        for data in buckets['0']['buckets']:
            daily_code_sum[time_day][data['key']] = data['doc_count']
        daily_net_out[time_day] = round(buckets['1']['value']/1024/1024, 2)
        for data in buckets['2']['buckets']:
            daily_req_method[time_day][data['key']] = data['doc_count']
        for data in buckets['3']['buckets']:
            daily_ip_sum[time_day][data['key']] = data['doc_count']
        for data in buckets['4']['buckets']:
            daily_user_agent[time_day][data['key']] = data['doc_count']
        user_agent = {}
        for key, value in daily_user_agent[time_day].items():
            if 'MicroMessenger' in key:
                user_agent['WeChat'] = user_agent.get('WeChat', 0) + value
            elif 'Edg' in key:
                user_agent['Edge'] = user_agent.get('Edge', 0) + value
            elif 'Chrome' in key:
                user_agent['Chrome'] = user_agent.get('Chrome', 0) + value
            elif 'Safari' in key:
                user_agent['Safari'] = user_agent.get('Safari', 0) + value
            elif 'Firefox' in key:
                user_agent['Firefox'] = user_agent.get('Firefox', 0) + value
            elif 'okhttp' in key:
                user_agent['Android-Unknown'] = user_agent.get('Android-Unknown', 0)\
                    + value
            elif 'python-requests' in key:
                user_agent['Script-Tools'] = user_agent.get('Script-Tools', 0) + value
            elif 'Android-' in key:
                user_agent[key] = value
            elif 'Go-http-client' in key:
                user_agent['Script-Tools'] = user_agent.get('Script-Tools', 0) +\
                    value
            elif 'Apache-HttpClient' in key:
                user_agent['Script-Tools'] = user_agent.get('Script-Tools',
                                                             0) + value
            else:
                user_agent['Other'] = user_agent.get('Other', 0) + value
        daily_user_agent[time_day] = user_agent
        for data in buckets['5']['buckets']:
            daily_url_sum[time_day][data['key']] = data['doc_count']
    return daily_code_sum, daily_net_out, daily_req_method, daily_ip_sum,\
        daily_user_agent, daily_url_sum, daily_pv_sum, daily_uv_sum


def ip_search(ip, num, _city_sum: dict, _uv_city_sum: dict,
              _ope_sum: dict, _uv_ope_sum: dict):
    """IP归属地查询"""
    pool_sema.acquire()
    city = q.lookup(ip)
    ope = city[1]
    city = city[0]
    if '省' in city:
        city = city[:2] + '省'
    elif '市' in city:
        city = city[:2] + '市'
    else:
        city = '未知'
    if '移动' in ope:
        ope = '移动'
    elif '联通' in ope:
        ope = '联通'
    elif '电信' in ope:
        ope = '电信'
    elif '阿里云' in ope:
        ope = '阿里云'
    else:
        ope = '未知'
    _city_sum[city] = _city_sum.get(city, 0) + num
    _uv_city_sum[city] = _uv_city_sum.get(city, 0) + 1
    _ope_sum[ope] = _ope_sum.get(ope, 0) + num
    _uv_ope_sum[ope] = _uv_ope_sum.get(ope, 0) + 1
    pool_sema.release()


def th_ip_search(function, _ip_sum: dict):
    """多线程调用"""
    _city_sum = {}
    _uv_city_sum = {}
    _ope_sum = {}
    _uv_ope_sum = {}
    _sort_city_sum = {}
    _sort_ope_sum = {}
    for ip, num in _ip_sum.items():
        thread = threading.Thread(target=function,
                                  args=(ip, num, _city_sum,
                                        _uv_city_sum, _ope_sum, _uv_ope_sum))
        thread.start()
    thread.join()
    _sort_city_sum = dict(sorted(_city_sum.items(),
                                 key=lambda item: item[1], reverse=True))
    _sort_ope_sum = dict(sorted(_ope_sum.items(),
                                key=lambda item: item[1], reverse=True))
    _sort_uv_city_sum = dict(sorted(_uv_city_sum.items(),
                                    key=lambda item: item[1], reverse=True))
    _sort_uv_ope_sum = dict(sorted(_uv_ope_sum.items(),
                                   key=lambda item: item[1], reverse=True))
    return _sort_city_sum, _sort_ope_sum, _sort_uv_city_sum, _sort_uv_ope_sum


def html_table_2(title: str, table_header: list, table_content, width="880"):
    """绘制表格"""
    html_title = '<table border="0" width=%s cellpadding="5" cellspacing="0"\
    style=""微软雅黑",Helvetica,Arial,sans-serif;font-size:14px;"><tr>\
    <td colspan="8" style="text-align:center;border:none;font-size:20px;\
    color:#9e1423;padding-bottom:20px">%s</td></tr>' % (width, title)
    html_header = '<tr>'
    _table_header = table_header.copy()
    _table_header.insert(0, title.strip('统计'))
    _table_header.append('总计')
    for header in _table_header:
        html_header += '<td bgcolor="#E0FFFF" style="font-weight:bold">\
        %s</td>' % (header)
    html_header += '</tr>'
    html_content = ''
    sort_table_content = dict(sorted(
                                  table_content.items(),
                                  key=lambda item: sum(item[1]), reverse=True))
    for key, item in sort_table_content.items():
        html_content += '<tr><td>%s</td>' % (key)
        if len(item) < 7:
            for _ in range(len(item), 7):
                item.append(0)
        for value in item:
            if value > 100000:
                html_content += '<td style="color:red">%d</td>' % (value)
            elif value > 10000:
                html_content += '<td style="color:#DAA520">%d</td>' % (value)
            elif value > 1000:
                html_content += '<td style="color:blue">%d</td>' % (value)
            else:
                html_content += '<td>%d</td>' % (value)
        html_content += '<td style="color:green">%d</td>' % (sum(item))
        html_content += '</tr>'
    _html_table = html_title + html_header + html_content + '</table>'
    return _html_table


def data_convert(data: dict):
    """将数据转换成适合表格的形式"""
    n = 1
    _new_value = {}
    for item in data.values():
        for key, value in item.items():
            if key in _new_value:
                _new_value[key].append(value)
                if len(_new_value[key]) != n:
                    for i in range(len(_new_value[key]) - 1, n - 1):
                        _new_value[key].insert(i, 0)
            else:
                _new_value[key] = [value]
                if n != 1:
                    for i in range(0, n-1):
                        _new_value[key].insert(i, 0)
        n += 1
    return _new_value


def bar_chart(data: dict, title_name) -> Bar:
    """绘制条形图"""
    x_data = list(data.keys())
    y_data = list(data.values())
    # 换一下顺序,显示的更好看
    x_data.reverse()
    y_data.reverse()
    c = (
        Bar(init_opts=opts.InitOpts(width='880px', height='440px',
                                    bg_color='white',
                                    js_host='/home/udi/.config/'))
        .add_xaxis(x_data)
        .add_yaxis("", y_data, color='#26d2f0', category_gap='40%')
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title_name),
            yaxis_opts=opts.AxisOpts(
                name='地区',
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#979ca8")),
            ),
            xaxis_opts=opts.AxisOpts(
                name='UV',
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#979ca8"))
            )
        )
    )
    return c.render('bar.html')


def line_chart(pv_data, uv_data, x_data, title):
    """绘制双折线图"""
    c = (
        Line(init_opts=opts.InitOpts(width='880px', height='440px',
                                     bg_color="white",
                                     js_host='/home/udi/.config/'))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title, subtitle='7日数据趋势'),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                # 修改坐标轴线和字体颜色
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#979ca8")),
                axislabel_opts=opts.LabelOpts(formatter="{value} PV")
            ),
            xaxis_opts=opts.AxisOpts(
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#979ca8"))
            ),
            legend_opts=opts.LegendOpts(legend_icon='circle')
        )
        .add_xaxis(x_data)
        .add_yaxis(
            series_name="PV",
            y_axis=pv_data,
            linestyle_opts=opts.LineStyleOpts(width=3),
            itemstyle_opts=opts.ItemStyleOpts(color='#6688ff'),
            is_smooth=True
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value} UV"),
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#979ca8"))
            )
        )
    )
    c2 = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            series_name="UV",
            y_axis=uv_data,
            linestyle_opts=opts.LineStyleOpts(width=3),
            itemstyle_opts=opts.ItemStyleOpts(color='#4cd9f8'),
            is_smooth=True,
            yaxis_index=1
        )
    )
    c.overlap(c2)
    return c.render('line.html')


def one_line_chart(y_data, x_data, title, unit):
    """绘制单折线图"""
    c = (
        Line(init_opts=opts.InitOpts(width='880px', height='440px',
                                     bg_color="white",
                                     js_host='/home/udi/.config/'
                                     ))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title, subtitle='7日数据趋势'),
            legend_opts=opts.LegendOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#979ca8")),
                axislabel_opts=opts.LabelOpts(formatter="{value} " + unit)
            ),
            xaxis_opts=opts.AxisOpts(
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#979ca8"))
            )
        )
        .add_xaxis(x_data)
        .add_yaxis(
            series_name='',
            y_axis=y_data,
            linestyle_opts=opts.LineStyleOpts(width=3),
            itemstyle_opts=opts.ItemStyleOpts(color='#6688ff'),
            is_smooth=True
        )
    )
    return c.render('one_line.html')


def map_chart(_city_uv: dict):
    """绘制地图"""
    city_name = [ i.strip('省市') for i in _city_uv.keys() ]
    c = (
        Map(init_opts=opts.InitOpts(width='880px', height='440px',
                                    bg_color="white",
                                    js_host='/home/udi/.config/'))
        .add(
             " ", [list(z) for z in zip(city_name, _city_uv.values())],
             zoom=1, center=[105, 34.5], is_map_symbol_show=False,
             itemstyle_opts={
                "normal": {"areaColor": "#e6f4ff", "borderColor": "#979ca8"},
                "emphasis": {
                    "areaColor": "rgba(255,255,255, 0.5)"
                 }
             }
            )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="用户分布区域", pos_left="center"),
            legend_opts=opts.LegendOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                dimension=0,
                pos_left="10",
                pos_top="center",
                min_=min(_city_uv.values()),
                max_=max(_city_uv.values()),
                range_text=["High", "Low"],
                is_calculable=True,
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                range_color=["#a5f1ff", "#4c74ff"]
            )
        )
    )
    return c.render('map.html')


def pie_chart(data, title, max_num) -> Pie:
    """绘制饼图"""
    chart_data = {}
    for name, num in data.items():
        if num > max_num:
            chart_data[name] = num
        else:
            chart_data['Other'] = chart_data.get('Other', 0) + num
    c = (
        Pie(init_opts=opts.InitOpts(width='880px', height='440px',
                                    bg_color="white",
                                    js_host='/home/udi/.config/'))
        .add("", [list(z) for z in chart_data.items()],
             radius=["50%", "75%"], center=["50%", "60%"])
        .set_colors(['#66C7FF', '#66E6FF', '#66FFE3', '#69F5AA', '#CBF54C',
                     '#F5EF56', '#FAD264', '#FFBA66', '#66A8FF', '#6687FF'])
        .set_global_opts(title_opts=opts.TitleOpts(title=title,
                                                   pos_left="center"),
                         legend_opts=opts.LegendOpts(orient="vertical",
                                                     pos_top="15%",
                                                     pos_left="2%"))
        .set_series_opts(label_opts=opts.LabelOpts(
                             formatter="{b}: {d}%"))
        # .render("pie.html")
            )
    return c.render('pie.html')


def html_table(title, table_header: list, table_content, width="880"):
    """绘制html表格"""
    html_title = '<table border="1" bordercolor="#c8c9cc" width=%s cellpadding="5" cellspacing="0"\
            "style=""微软雅黑",Helvetica,Arial,sans-serif;font-weight:bold;font-size:14px;">\
    <tr><td colspan="8" style="text-align:center;border:none;font-size:16px;\
    color:#0fb9d3;padding-bottom:16px">%s</td></tr>' % (width, title)
    html_header = '<tr>'
    for header in table_header:
        html_header += '<td bgcolor="#e1e4eb" style="font-weight:bold">%s\
        </td>' % (header)
    html_header += '</tr>'
    html_content = ''
    if type(table_content) == list:
        html_content += '<tr>'
        for value in table_content:
            html_content += '<td>%s</td>' % (value)
        html_content += '</tr>'
    elif type(table_content) == dict:
        sort_table_content = dict(
            sorted(table_content.items(),
                   key=lambda item: sum(item[1]), reverse=True))
        for key, item in sort_table_content.items():
            html_content += '<tr><td>%s</td>' % (key)
            if len(item) < 7:
                for _ in range(len(item), 7):
                    item.append(0)
            for value in item:
                #if value > 100000:
                #    html_content += '<td style="color:red">%d</td>' % (value)
                #elif value > 10000:
                #    html_content += '<td style="color:#DAA520">%d\
                #    </td>' % (value)
                #elif value > 1000:
                #    html_content += '<td style="color:blue">%d</td>' % (value)
                #else:
                html_content += '<td>%d</td>' % (value)
            html_content += '<td style="color:green">%d</td>' % (sum(item))
            html_content += '</tr>'
    _html_table = html_title + html_header + html_content + '</table>'
    return _html_table


def convert_sum(ip_sum):
    """将每天的IP数据统计出pv和uv"""
    new_ip_sum = {}
    for item in ip_sum.values():
        for ip, num in item.items():
            new_ip_sum[ip] = new_ip_sum.get(ip, 0) + num
    pv = sum(new_ip_sum.values())
    uv = len(new_ip_sum)
    return pv, uv


def platform_failfure(daily_code_sum: dict):
    client = "mongodb://admin:root123@10.10.10.13:27017/admin"
    mongo = pymongo.MongoClient(client)
    my_db = mongo['nginx_data']
    my_collection = my_db['failure_num']
    week_failure_num = 0
    for date, item in daily_code_sum.items():
        total_sum = sum(item.values())
        code_sum = item.get('500', 0)
        per_code = code_sum / total_sum
        if per_code > 0.05:
            today_failure_num = 1
            week_failure_num += 1
        else:
            today_failure_num = 0
        document = {'date': date, 'num': today_failure_num}
        lastdata = my_collection.find_one(sort=[('_id', -1)])
        if lastdata['date'] == date:
            my_collection.update_one({"date": date}, {"$set": {"num": today_failure_num}})
        else:
            my_collection.insert_one(document)
    month = today.strftime('%m')
    year = today.year
    month_res = my_collection.find({'date': {'$regex': f'{year}-{month}'}})
    month_failure_num = 0
    for doc in month_res:
        month_failure_num += doc['num']
    quarter1 = ['01', '02', '03']
    quarter2 = ['04', '05', '06']
    quarter3 = ['07', '08', '09']
    quarter4 = ['10', '11', '12']
    if month in quarter1:
        quarter = quarter1
        quarter_num = 1
    elif month in quarter2:
        quarter = quarter2
        quarter_num = 2
    elif month in quarter3:
        quarter = quarter3
        quarter_num = 3
    elif month in quarter4:
        quarter = quarter4
        quarter_num = 4
    else:
        print('error')
    quarter_res = my_collection.find({'date': {'$regex': f'{year}-{quarter}'}})
    quarter_failure_num = 0
    for doc in quarter_res:
        quarter_failure_num += doc['num']
    return quarter_num, week_failure_num, month_failure_num, quarter_failure_num


def send_mail(subject, content, images, to_mail: list):
    message = MIMEMultipart()
    message.attach(MIMEText(content, 'html', 'utf-8'))
    message['Subject'] = Header(subject, 'utf-8')
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
        print("Error: unable to send email, %s" % e)


if __name__ == '__main__':
    daily_code_sum, daily_net_out, daily_req_method, daily_ip_sum,\
        daily_user_agent, daily_url_sum,\
        daily_pv_sum, daily_uv_sum = http_log()
    day_list = list(daily_net_out.keys())
    new_user_agent = data_convert(daily_user_agent)
    new_code_sum = data_convert(daily_code_sum)
    new_net_out = list(daily_net_out.values())
    new_req_method = data_convert(daily_req_method)
    new_url_sum = data_convert(daily_url_sum)
    # new_ip_sum = data_convert(daily_ip_sum)
    q = QQwry()
    q.load_file('/home/udi/.local/share/nali/qqwry.dat')
    total_ip_sum = {}
    total_req_method = {}
    total_code = {}
    total_user_agent = {}
    for item in daily_ip_sum.values():
        for ip, num in item.items():
            total_ip_sum[ip] = total_ip_sum.get(ip, 0) + num
    for item in daily_req_method.values():
        for req, num in item.items():
            total_req_method[req] = total_req_method.get(req, 0) + num
    for item in daily_code_sum.values():
        for code, num in item.items():
            total_code[code] = total_code.get(code, 0) + num
    for item in daily_user_agent.values():
        for user, num in item.items():
            total_user_agent[user] = total_user_agent.get(user, 0) + num
    city_sum, ope_sum, uv_city_sum, uv_ope_sum = th_ip_search(ip_search,
                                                              total_ip_sum)
    email_content = '<h3>一、总体统计（%s - %s）</h3>'\
        % (start_time.split('T')[0], end_time.split('T')[0])
    quarter, week_num, month_num, quarter_num = platform_failfure(daily_code_sum)
    table_title = '网端调度平台稳定性故障统计'
    table_header = ['本周故障总数', f'{today.month}月故障总数', f'第{quarter}季度故障总数']
    table_content = [week_num, month_num, quarter_num]
    email_content += html_table(table_title, table_header, table_content)
    email_content += '<p style="color:#898a8c;font-size: 14px">稳定性指标定义:用户反馈故障次数或HTTP状态码5xx\
    (指程序或服务器请求异常)大于5%视为一次故障</p><br><br>'
    table_title = '调度平台用户(本周)活跃数统计'
    pv, uv = convert_sum(daily_ip_sum)
    table_header = ['PV(7日用户总点击量)', 'UV(7日总用户数)', '7日出口总流量(MB)']
    table_content = [pv, uv, round(sum(new_net_out), 2)]
    email_content += html_table(table_title, table_header, table_content)

    make_snapshot(snapshot, line_chart(list(daily_pv_sum.values()),
                                       list(daily_uv_sum.values()),
                                       day_list, "7日数据趋势"), "daily_line.jpeg")
    email_content += '<br><br><p><img src="cid:image1" width="880"></p>'
    make_snapshot(snapshot, one_line_chart(
                      list(daily_net_out.values()),
                      day_list, "出口流量", "MB"), "net_line.jpeg")
    email_content += '<p><img src="cid:image2" width="880"></p>'
    make_snapshot(snapshot, map_chart(uv_city_sum), "map.jpeg")
    email_content += '<p><img src="cid:image3" width="880"></p>'
    make_snapshot(snapshot, bar_chart(uv_city_sum, "用户分布区域数量统计(Top10)"),
                  "bar.jpeg")
    email_content += '<p><img src="cid:image4" width="880"></p>'
    make_snapshot(snapshot, pie_chart(uv_city_sum,
                                      "用户分布区域占比", 2), "uv_city.jpeg")
    email_content += '<p><img src="cid:image5" width="880"></p>'
    #make_snapshot(snapshot, pie_chart(city_sum,
    #                                  "用户分布区域QPS占比", 100), "pv_city.jpeg")
    #email_content += '<p><img src="cid:image6" width="880"></p>'
    make_snapshot(snapshot, pie_chart(uv_ope_sum,
                                      "用户运营商占比", 5), "uv_ope.jpeg")
    email_content += '<p><img src="cid:image6" width="880"></p>'
    #make_snapshot(snapshot, pie_chart(ope_sum,
    #                                  "运营商QPS统计", 100), "pv_ope.jpeg")
    #email_content += '<p><img src="cid:image8" width="880"></p>'
    email_content += '<h3>二、详细数据统计  (<a href="http://grafana.unity-drive.net\
/goto/7OWZeEd4k?orgId=1" target="_blank" rel="noopener noreferrer">\
更多详情页面请点击此处</a>)</h3>'
    #table_header = ['请求方法'] + day_list + ['总计']
    #email_content += html_table('请求方法7日数据统计', table_header, new_req_method)
    #make_snapshot(snapshot, pie_chart(total_req_method,
    #                                  "请求方法(7日总计)占比", 100), "req_method.jpeg")
    #email_content += '<p><img src="cid:image9" width="880"></p>'
    table_header = ['状态码'] + day_list + ['总计']
    email_content += html_table('状态码7日数据统计', table_header, new_code_sum)
    email_content += '<p style="color:#898a8c;font-size: 14px">HTTP状态码含义: 1xx表示信息(如:mqtt)，2xx表示\
    成功, 3xx表示重定向, <br>4xx表示客户端错误，5xx表示服务器或后台程序错误<br>\
    <a href="https://m.runoob.com/http/http-status-codes.html"\
    target="_blank" rel="noopener noreferrer">点击查看HTTP码详细定义</a></p>'
    make_snapshot(snapshot, pie_chart(total_code,
                                      "状态码(7日总计)占比", 1000),
                  "code.jpeg")
    email_content += '<p><img src="cid:image7" width="880"></p><br><br>'
    table_header = ['客户端'] + day_list + ['总计']
    email_content += html_table('客户端7日数据统计', table_header, new_user_agent)
    make_snapshot(snapshot, pie_chart(total_user_agent,
                                      "客户端来源(7日总计)占比", 1000),
                  "user_agent.jpeg")
    email_content += '<p><img src="cid:image8" width="880"></p>'
    # 发送邮件
    subject = "网端调度平台用户活跃度统计周报"
    img_name = [
        'daily_line.jpeg', 'net_line.jpeg', 'map.jpeg', 'bar.jpeg',
        'uv_city.jpeg', 'uv_ope.jpeg', 'code.jpeg', 'user_agent.jpeg']
    to_mail = ['wangduanjishubu@unity-drive.com',
               'yaozujie@unity-drive.com', 'liguojian@unity-drive.com',
               'linjinyan@unity-drive.com', 'liqingwei@unity-drive.com', 'xudongdong@unity-drive.com',
               'xubin@unity-drive.com', 'yangpan@unity-drive.com']
    #to_mail = ['caizhisheng@unity-drive.com']
    send_mail(subject, email_content, img_name, to_mail)
    program_end_time = time.time()
    print('\033[32mProgram time consuming: %.2fs\033[0m' % (
              program_end_time - program_start_time))
