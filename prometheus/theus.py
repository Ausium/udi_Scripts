#! /usr/bin/python
# coding=utf-8

import requests
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

start_time = time.time()


# 调用prometheus接口查询
def prometheus_query(env, option):
    if option == 'api_time':
        param = 'query=increase(http_server_requests_duration_ms_sum{job="api"}[5m]) /increase(http_server_requests_duration_ms_count{job="api"}[5m])'
        arg = 'path'
    elif option == 'cpu_use':
        param = 'query=irate(process_cpu_seconds_total{env="%s"}[5m]) * 100' % (env)
        arg = 'app'
    elif option == 'mem_use':
        param = 'query=process_resident_memory_bytes{env="%s"} /1024/1024' % (env)
        arg = 'app'
    else:
        return 'option error'
    if env == 'test':
        url = 'http://192.168.19.97:9090/api/v1/query'
    elif env == 'pre':
        url = 'http://192.168.19.95:9090/api/v1/query'
    elif env == 'production':
        url = 'http://120.79.122.243:9090/api/v1/query'
    else:
        return 'env error'
    response = requests.get(url, params=param)
    _app_value = {}
    for i in response.json()['data']['result']:
        app = i['metric'][arg]
        value = i['value'][1]
        if value[-1].isdigit():
            _app_value[app] = round(float(value), 2)
    _sort_app_value = dict(sorted(_app_value.items(), key=lambda item: item[1], reverse=True))
    return _sort_app_value

def print_statistics(env, option, app_arg:dict):
    if env == 'test':
        env_text = '测试环境(ud3test)'
    elif env == 'pre':
        env_text = '预发布环境(ud3pre)'
    elif env == 'production':
        env_text = '生产环境(iov)'
    else:
        print('env error')
        return -1
    if option == 'api_time':
        title_text = '接口耗时统计'
        arg = ['接口', '耗时', 'ms']
    elif option == 'cpu_use':
        title_text = 'CPU利用率统计'
        arg = ['后台', 'CPU利用率', '%']
    elif option == 'mem_use':
        title_text = 'MEM使用值统计'
        arg = ['后台', 'MEM使用值', 'MB']
    else:
        print('option error')
        return -2
    print('\033[32m%s%s:\033[0m' %(env_text, title_text))
    max_len = max(len(x) for x in app_arg.keys())
    for key, value in app_arg.items():
        key += " " * (max_len - len(key))
        print('%s: %s\t%s: %s %s' %(arg[0], key, arg[1], value, arg[2]))

#发送邮件
def send_mail(subject, content, to_mail: list):
    message = MIMEMultipart()
    message.attach(MIMEText(content, 'html', 'utf-8'))
    message['Subject']= Header(subject, 'utf-8')
    smtp_server = 'smtp.exmail.qq.com'
    from_mail = 'noreply@unity-drive.com'
    mail_pass = 'vKaWcVGGJkwn3EXB'
    message['From'] = 'grafana<%s>' %from_mail
    message['To'] = ','.join(to_mail)
    try:
        s = smtplib.SMTP_SSL(smtp_server, '465')
        s.login(from_mail, mail_pass)
        s.sendmail(from_mail, to_mail, message.as_string())
        s.quit()
        print('successfully sent email')
    except smtplib.SMTPException as e:
        print("Error: unable to send email, %s" %e)


# 告警检测,并通过邮件通知
def alert_check(env, option, app_arg:dict):
    if option == 'api_time':
        thresholds = 2000
        arg = ['接口', '耗时', 'ms']
    elif option == 'cpu_use':
        thresholds = 50
        arg = ['后台', 'CPU利用率', '%']
    elif option == 'mem_use':
        arg = ['后台', '内存使用值', 'MB']
        thresholds = 1024
    else:
        print('option error')
        return -2
    if env == 'test':
        title = '测试环境(ud3test)'
        link = 'http://grafana.unity-drive.net/goto/LGUEo8K4z?orgId=1'
    elif env == 'pre':
        title = '预发布环境(ud3pre)'
        link = 'http://grafana.unity-drive.net/goto/gQvyoUFVk?orgId=1'
    elif env == 'production':
        title = '生产环境(iov)'
        link = 'http://grafana.unity-drive.net/goto/Db-oTFFVz?orgId=1'
    else:
        print('env error')
        return -1
    subject = '%s微服务后台告警通知' %(title)
    email_content = '<h3 style="color:red">%s %s告警通知</h3>' %(title, arg[0]+arg[1])
    email_content += '<table width="880"><tr><td bgcolor="#E0FFFF" style="font-weight:bold">%s</td><td bgcolor="#E0FFFF" style="font-weight:bold">%s</td></tr>' %(arg[0], arg[1])
    send = False
    for key, value in app_arg.items():
        if value > thresholds:
            email_content += '<tr><td>%s</td><td style="color:red">%s %s</td></tr>' %(key, value, arg[2])
            send = True
    email_content += '</table><br><a href=%s target="_blank" rel="noopener noreferrer">更多详情页面请点击此处</a>' %(link)
    if send:
        to_mail = ['caizhisheng@unity-drive.com', 'kuanghanqin@unity-drive.com', 'huanghanyi@unity-drive.com', 'zengming@unity-drive.com', 'wangweifeng@unity-drive.com']
        send_mail(subject, email_content, to_mail)

if __name__ == '__main__':
    test_path_avg = prometheus_query('test', 'api_time')
    pre_path_avg = prometheus_query('pre', 'api_time')
    production_path_avg = prometheus_query('production', 'api_time')
    #print_statistics('test', 'api_time', test_path_avg)
    #print_statistics('pre', 'api_time', pre_path_avg)
    #print_statistics('production', 'api_time', production_path_avg)
    alert_check('test', 'api_time', test_path_avg)
    alert_check('pre', 'api_time', pre_path_avg)
    alert_check('production', 'api_time', production_path_avg)

    test_cpu_use = prometheus_query('test', 'cpu_use')
    pre_cpu_use = prometheus_query('pre', 'cpu_use')
    production_cpu_use = prometheus_query('production', 'cpu_use')
    #print_statistics('test', 'cpu_use', test_cpu_use)
    #print_statistics('pre', 'cpu_use', pre_cpu_use)
    #print_statistics('production', 'cpu_use', production_cpu_use)
    alert_check('test', 'cpu_use', test_cpu_use)
    alert_check('pre', 'cpu_use', pre_cpu_use)
    alert_check('production', 'cpu_use', production_cpu_use)

    test_mem_use = prometheus_query('test', 'mem_use')
    pre_mem_use = prometheus_query('pre', 'mem_use')
    production_mem_use = prometheus_query('production', 'mem_use')
    alert_check('test', 'mem_use', test_mem_use)
    alert_check('pre', 'mem_use', pre_mem_use)
    alert_check('production', 'mem_use', production_mem_use)
    end_time=time.time()
#    print(end_time - start_time)
