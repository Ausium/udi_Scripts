#! /bin/python3
# coding = utf-8
"""该脚本将统计的迭代需求数据发送到邮件中"""

import time
import jwt
import httpx
from datetime import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


def get_apptoken(_appid, _secret):
    """生成token"""
    now_time = int(time.time())
    expire_time = now_time + 3600
    token_dict = {'_appId': _appid, 'iat': now_time, 'exp': expire_time}
    headers = {'typ': 'jwt', 'alg': 'HS256'}
    encode = jwt.encode(payload=token_dict, key=_secret, headers=headers,
                        algorithm='HS256')
    return bytes.decode(encode)


# 获取企业成员
def get_orgmembers():
    params = {'orgId': '5b4ff29669269300014f47a3', 'pageSize': 150}
    res = client.get(url=host + '/api/org/member/list', params=params)
    org_members = {}
    for i in res.json()['result']:
        org_members[i['userId']] = i['name']
    return org_members


# 获取项目自定义字段
def get_customfield(projectId):
    res = client.get(
        url=host + '/api/v3/project/%s/customfield/search'
        % (projectId), headers=header)
    customfield_list = {}
    for i in res.json()['result']:
        customfield_list[i['id']] = i['name']
    return customfield_list


# 获取项目工作流状态
def get_taskflowstatus(projectId):
    res = client.get(
        url=host + '/api/v3/project/%s/taskflowstatus/search'
        % (projectId))
    taskflowstatus_list = {}
    for i in res.json()['result']:
        taskflowstatus_list[i['id']] = i['name']
    return taskflowstatus_list


# 获取项目标签
def get_tag(projectId):
    res = client.get(url=host + '/api/v3/project/%s/tag/search' % (projectId))
    tag_list = {}
    for i in res.json()['result']:
        tag_list[i['id']] = i['name']
    return tag_list


# 获取企业优先级
def get_priority():
    params = {'organizationId': '5b4ff29669269300014f47a3'}
    res = client.get(url=host + '/api/v3/project/priority/list', params=params)
    priority_list = {}
    for i in res.json()['result']:
        priority_list[i['priority']] = i['name']
    return priority_list


# 获取项目的任务类型
def get_tasktype(projectId):
    params = {"pageSize": 100}
    res = client.get(
        url=host +
        f'/api/v3/project/{projectId}/scenariofieldconfig/search',
        params=params)
    tasktype_list = {}
    for i in res.json()['result']:
        tasktype_list[i['id']] = i['name']
    return tasktype_list


# 获取项目中的需求
def get_need_task(client, projectId):
    taskflowstatus_list = get_taskflowstatus(projectId)
    org_members = get_orgmembers()
    priority_list = get_priority()
    params = {
        'pageSize': 1000,
        'q': 'TQL: sfcId=616ce2c6833e44b14b577071 \
            AND tfsId!=632bc554880e9700409f817c \
            AND tfsId!=6411858633068f00177e1e74 \
            AND tasklistId=6260c6a49bed45003f706c25'
    }
    res = client.get(
        url=host+'/api/v3/project/%s/task/query'
        % (projectId), params=params
    )
    need_count = res.json()['count']
    need_done_sum = 0
    need_status_sum = {}
    need_exceed_sum = {}
    need_emergency_sum = {}
    for i in res.json()['result']:
        taskstatus = taskflowstatus_list.get(i['tfsId'])
        task_priority = priority_list.get(i['priority'])
        if taskstatus == '待处理' or taskstatus == '待开发':
            need_status_sum['待开发'] = need_status_sum.get('待开发', 0) + 1
            if task_priority == '紧急' or task_priority == '非常紧急':
                need_emergency_sum['待开发'] = need_emergency_sum.get(
                    '待开发', 0
                ) + 1
        elif taskstatus == '进行中' or taskstatus == '待部署' or taskstatus == '开发中':
            need_status_sum['开发中'] = need_status_sum.get('开发中', 0) + 1
            if task_priority == '紧急' or task_priority == '非常紧急':
                need_emergency_sum['开发中'] = need_emergency_sum.get(
                    '开发中', 0
                ) + 1
        elif taskstatus == '待回归' or taskstatus == '待测试':
            need_status_sum['待测试'] = need_status_sum.get('待测试', 0) + 1
            if task_priority == '紧急' or task_priority == '非常紧急':
                need_emergency_sum['待测试'] = need_emergency_sum.get(
                    '待测试', 0
                ) + 1
        elif taskstatus == '已解决（回归通过）' or taskstatus == '待上线':
            need_status_sum['待上线'] = need_status_sum.get('待上线', 0) + 1
            if task_priority == '紧急' or task_priority == '非常紧急':
                need_emergency_sum['待上线'] = need_emergency_sum.get(
                    '待上线', 0
                ) + 1
        else:
            need_status_sum[taskstatus] = need_status_sum.get(
                taskstatus, 0) + 1
            if task_priority == '紧急' or task_priority == '非常紧急':
                need_emergency_sum[taskstatus] = need_emergency_sum.get(
                    taskstatus, 0) + 1
        now_time = datetime.now()
        create_time = datetime.strptime(
            i['created'], "%Y-%m-%dT%H:%M:%S.%fZ")
        create_str = create_time.strftime('%Y/%m/%d')
        update_time = datetime.strptime(
            i['updated'], "%Y-%m-%dT%H:%M:%S.%fZ")
        update_str = update_time.strftime('%Y/%m/%d')
        needDone = i['isDone']
        if needDone:
            need_done_sum += 1
        else:
            gap_days = (now_time - create_time).days
            if int(gap_days) > 14:
                need_name = i['content']
                username = org_members.get(i['executorId'])
                for item in i['customfields']:
                    if item['cfId'] == '636a19dd144f0291f96bba66':
                        if item['value']:
                            sprint_version = item['value'][0].get('title', "")
                            break
                        else:
                            sprint_version = ""
                    else:
                        sprint_version = ""
                need_exceed_sum[need_name] = [
                    task_priority, taskstatus, username, sprint_version,
                    gap_days, create_str, update_str]
    return need_count, need_done_sum, need_status_sum, need_emergency_sum,\
        need_exceed_sum


# 获取web项目的迭代版本信息
def get_task(client, projectId):
    taskflowstatus_list = get_taskflowstatus(projectId)
    org_members = get_orgmembers()
    priority_list = get_priority()
    tasktype_list = get_tasktype(projectId)
    # 将版本不为空的需求过滤出来
    params = {
        'pageSize': 1000,
        'q': 'TQL: cf:636a19dd144f0291f96bba66 != null'}
    res = client.get(
        url=host+'/api/v3/project/%s/task/query'
        % (projectId), params=params)
    sprint_count = {}
    now_time = datetime.now()
    sprint_task_delay_sum = {}
    sprint_done_task_sum = {}
    sprint_taskstatus_sum = {}
    sprint_task_priority_sum = {}
    sprint_emergency_needs = {}
    for i in res.json()['result']:
        taskstatus = taskflowstatus_list.get(i['tfsId'])
        if taskstatus == '待设计' or taskstatus == '事务性工作':
            # 符合以上条件，跳过本次循环
            continue
        for item in i['customfields']:
            if item['cfId'] == '636a19dd144f0291f96bba66':
                sprint_version = item['value'][0]['title']
        taskstatus_sum = sprint_taskstatus_sum.get(sprint_version, {})
        task_priority = priority_list.get(i['priority'])
        emergency_sum = sprint_emergency_needs.get(sprint_version, {})
        if taskstatus == '待处理' or taskstatus == '待开发':
            taskstatus_sum['待开发'] = taskstatus_sum.get('待开发', 0) + 1
            if task_priority == '紧急' or task_priority == '非常紧急':
                emergency_sum['待开发'] = emergency_sum.get('待开发', 0) + 1
        elif taskstatus == '进行中' or taskstatus == '待部署' or taskstatus == '开发中':
            taskstatus_sum['开发中'] = taskstatus_sum.get('开发中', 0) + 1
            if task_priority == '紧急' or task_priority == '非常紧急':
                emergency_sum['开发中'] = emergency_sum.get('开发中', 0) + 1
        elif taskstatus == '待回归' or taskstatus == '待测试':
            taskstatus_sum['待测试'] = taskstatus_sum.get('待测试', 0) + 1
            if task_priority == '紧急' or task_priority == '非常紧急':
                emergency_sum['待测试'] = emergency_sum.get('待测试', 0) + 1
        elif taskstatus == '已解决（回归通过）' or taskstatus == '待上线':
            taskstatus_sum['待上线'] = taskstatus_sum.get('待上线', 0) + 1
            if task_priority == '紧急' or task_priority == '非常紧急':
                emergency_sum['待上线'] = emergency_sum.get('待上线', 0) + 1
        else:
            taskstatus_sum[taskstatus] = taskstatus_sum.get(taskstatus, 0) + 1
            if task_priority == '紧急' or task_priority == '非常紧急':
                emergency_sum[taskstatus] = emergency_sum.get(
                    taskstatus, 0) + 1
        sprint_emergency_needs[sprint_version] = emergency_sum
        sprint_taskstatus_sum[sprint_version] = taskstatus_sum
        sprint_count[sprint_version] = sprint_count.get(sprint_version, 0) + 1
        task_name = i['content']
        task_status = i['isDone']
        username = org_members.get(i['executorId'])
        create_time = datetime.strptime(
            i['created'], "%Y-%m-%dT%H:%M:%S.%fZ")
        create_str = create_time.strftime('%Y/%m/%d')
        update_time = datetime.strptime(
            i['updated'], "%Y-%m-%dT%H:%M:%S.%fZ")
        update_str = update_time.strftime('%Y/%m/%d')
        task_priority_sum = sprint_task_priority_sum.get(sprint_version, {})
        task_priority_sum[task_priority] = task_priority_sum.get(
            task_priority, 0) + 1
        sprint_task_priority_sum[sprint_version] = task_priority_sum
        if task_status:
            done_task_sum = sprint_done_task_sum.get(sprint_version, {})
            done_task_sum[update_str] = done_task_sum.get(update_str, 0) + 1
            sprint_done_task_sum[sprint_version] = done_task_sum
        else:
            gap_days = (now_time - create_time).days
            tasktype = tasktype_list.get(i['sfcId'])
            task_delay_sum = sprint_task_delay_sum.get(sprint_version, {})
            task_delay_sum[task_name] = [
                tasktype, task_priority, taskstatus, username, gap_days,
                create_str, update_str]
            sprint_task_delay_sum[sprint_version] = task_delay_sum
    return sprint_count, sprint_done_task_sum, sprint_taskstatus_sum,\
        sprint_task_delay_sum, sprint_task_priority_sum,\
        sprint_emergency_needs


def table_transform(sprint_count, sprint_donetask_sum, sprint_taskstatus_sum):
    """将数据转换成表格形式"""
    project_table_data = {}
    if type(sprint_count) == dict:
        for version, value in sprint_count.items():
            total_done = sprint_donetask_sum.get(version, 0)
            if total_done != 0:
                total_done = sum(total_done.values())
            wait_devlop = sprint_taskstatus_sum[version].get('待开发', 0)
            developing = sprint_taskstatus_sum[version].get('开发中', 0)
            pending_task = sprint_status_sum[version].get('待测试', 0)
            wait_production = sprint_status_sum[version].get('待上线', 0)
            leave_task = wait_devlop + developing + pending_task +\
                wait_production
            if leave_task == 0:
                continue
            else:
                project_table_data[version] = [
                        leave_task, wait_devlop, developing,
                        pending_task, wait_production, value]
    else:
        wait_devlop = sprint_taskstatus_sum.get('待开发', 0)
        developing = sprint_taskstatus_sum.get('开发中', 0)
        pending_task = sprint_taskstatus_sum.get('待测试', 0)
        wait_production = sprint_taskstatus_sum.get('待上线', 0)
        leave_task = wait_devlop + developing + pending_task + wait_production
        project_table_data = [
            leave_task, wait_devlop, developing, pending_task,
            wait_production, sprint_count]
    return project_table_data


# 绘制html表格
def html_table(
    title, table_header: list, table_content, emergency_needs={},
        width='1200'):
    html_title = '<table border="1" bordercolor="#c8c9cc" width=%s \
        cellpadding="5" cellspacing="0" "style=""微软雅黑",Helvetica,\
        Arial,sans-serif;font-weight:bold;font-size:14px;">\
        <tr><td colspan="8" style="text-align:center;border:none;\
        font-size:16px;color:#4476ff;padding-bottom:16px">%s</td>\
        </tr>' % (width, title)
    html_header = '<tr>'
    html_content = ''
    if type(table_content) == dict:
        for n, header in enumerate(table_header):
            if n == 0:
                html_header += '<td bgcolor="#e1e4eb" style="text-align:\
                center; font-weight:bold; width:50%%">%s</td>' % (header)
            elif n == 4:
                html_header += '<td bgcolor="#e1e4eb" style="text-align:\
                center; font-weight:bold; width:10%%">%s</td>' % (header)
            else:
                html_header += '<td bgcolor="#e1e4eb" style="text-align:\
                center; font-weight:bold">%s</td>' % (header)
        html_header += '</tr>'
        for key, item in table_content.items():
            if table_header[0] == '版本名称':
                html_content += '<tr><td style="text-align:center">%s</td>'\
                    % (key)
            else:
                html_content += '<tr><td>%s</td>' % (key)
            for n, value in enumerate(item):
                if value == '紧急' or value == '非常紧急':
                    html_content += '<td style="text-align:center; color:red">\
                        %s</td>' % (value)
                    continue
                elif n == 5:
                    emergency_num = sum(emergency_needs.get(
                        key, {}).values())
                elif n == 0:
                    key_in_sum = ['待开发', '开发中', '待测试', '待上线']
                    emergency_num = 0
                    for a in key_in_sum:
                        emergency_num += emergency_needs.get(key, {}).get(a, 0)
                elif n == 1:
                    emergency_num = emergency_needs.get(
                        key, {}).get('待开发', 0)
                elif n == 2:
                    emergency_num = emergency_needs.get(
                        key, {}).get('开发中', 0)
                elif n == 3:
                    emergency_num = emergency_needs.get(
                        key, {}).get('待测试', 0)
                elif n == 4:
                    emergency_num = emergency_needs.get(
                        key, {}).get('待上线', 0)
                else:
                    emergency_num = ''
                if emergency_num:
                    html_content += '<td style="text-align:center">%s\
                        (<span style="color: red" >%s</span>)</td>'\
                            % (value, emergency_num)
                else:
                    html_content += '<td style="text-align:center">%s</td>'\
                        % (value)
            html_content += '</tr>'
    elif type(table_content) == list:
        for header in table_header:
            html_header += '<td bgcolor="#e1e4eb" style="text-align:center;\
            font-weight:bold">%s</td>' % (header)
        html_header += '</tr>'
        for n, value in enumerate(table_content):
            if n == 5:
                emergency_num = sum(emergency_needs.values())
            elif n == 0:
                key_in_sum = ['待开发', '开发中', '待测试', '待上线']
                emergency_num = 0
                for a in key_in_sum:
                    emergency_num += emergency_needs.get(a, 0)
            elif n == 1:
                emergency_num = emergency_needs.get('待开发', 0)
            elif n == 2:
                emergency_num = emergency_needs.get('开发中', 0)
            elif n == 3:
                emergency_num = emergency_needs.get('待测试', 0)
            elif n == 4:
                emergency_num = emergency_needs.get('待上线', 0)
            else:
                emergency_num = ''
            if emergency_num:
                html_content += '<td style="text-align:center">%s \
                    (<span style="color: red;"\
                    >%s</span>)</td>' % (value, emergency_num)
            else:
                html_content += '<td style="text-align:center">%s</td>'\
                    % (value)
        html_content += '</tr>'
    else:
        print('table_content type is', type(table_content))
    _html_table = html_title + html_header + html_content + '</table>'
    return _html_table


def send_mali(subject, content, to_mail: list, Cc_list):
    """发送邮件"""
    message = MIMEMultipart()
    message.attach(MIMEText(content, 'html', 'utf-8'))
    message['Subject'] = Header(subject, 'utf-8')
    smtp_server = 'smtp.exmail.qq.com'
    mail_user = 'noreply@unity-drive.com'
    from_mail = 'caizhisheng<noreply@unity-drive.com>'
    mail_pass = 'vKaWcVGGJkwn3EXB'
    message['From'] = from_mail
    message['To'] = ','.join(to_mail)
    message['Cc'] = ','.join(Cc_list)
    try:
        s = smtplib.SMTP_SSL(smtp_server, '465')
        s.login(mail_user, mail_pass)
        s.sendmail(from_mail, to_mail + Cc_list, message.as_string())
        s.quit()
        print('successfully sent email')
    except smtplib.SMTPException as e:
        print("Error: unable to send email, %s" % e)


if __name__ == '__main__':
    start_time = time.time()
    token = get_apptoken('63ad342a6aa592f07643d034',
                         'BMeIMuNiCPtaelXcbfoznWjzABuXldeg')
    host = 'https://open.teambition.com'
    header = {
        'Authorization': 'Bearer '+token,
        'X-Tenant-Type': 'organization',
        'X-Tenant-Id': '5b4ff29669269300014f47a3'}
    projectId = '616ce28fccce3c69eca1b933'
    project_dict = {
        '无人车管理平台Web': '616ce28fccce3c69eca1b933'}
    with httpx.Client(headers=header) as client:
        sprint_count, sprint_donetask_sum, sprint_status_sum,\
            sprint_task_delay_sum, sprint_task_priority_sum,\
            sprint_emergency_needs = get_task(client, projectId)
        need_count, need_done_sum, need_status_sum, need_emergency_sum,\
            need_exceed_sum = get_need_task(client, projectId)
    # 将需求数据绘制成表格
    need_table_data = table_transform(
        need_count, need_done_sum,
        need_status_sum)
    html_msg = '<h3>一、需求数据统计(无人车管理Web)</h3>'
    table_header = [
        "剩余需求数", "待开发需求数", "开发中需求数",
        "待测试需求数", "待上线需求数", "总需求数"
    ]
    html_msg += html_table(
        "", table_header, need_table_data,
        need_emergency_sum)
    html_msg += '<p>注:<br>1.括号中的标红数值为紧急/非常紧急的需求数<br>\
        2.总需求数=剩余需求数+已发布需求数+待确认需求数</p><br>'
    # 对迭代版本的名字进行排序
    sorted_sprint_count = {k: sprint_count[k] for k in sorted(
        sprint_count.keys(), reverse=True)}
    project_table_data = table_transform(
        sorted_sprint_count, sprint_donetask_sum, sprint_status_sum)
    html_msg += '<h3>二、迭代版本数据</h3>'
    table_header = [
        '版本名称',  '未完成卡片数', '待开发卡片数', '开发中卡片数',
        '待测试卡片数', '待上线卡片数', '卡片总数']
    html_msg += html_table(
        '', table_header, project_table_data,
        sprint_emergency_needs)
    html_msg += '<p>注:<br>1.括号中的标红数值为紧急/非常紧急的卡片数<br>\
        2.卡片总数=未完成卡片数+已完成卡片数</p><br>'
    html_msg += '<br><h3>三、迭代卡片内容</h3>'
    table_header = [
        '卡片名称', '类型', '优先级', '状态', '执行人', '开放时间(天)',
        '创建时间', '更新时间']
    for version in sorted_sprint_count.keys():
        content = sprint_task_delay_sum.get(version, 0)
        if content:
            html_msg += html_table(
                version, table_header, content)
    html_msg += '<h3>四、积压需求提醒(无人车管理Web)</h3>'
    table_header = [
        '需求名称', '优先级', '状态', '执行人', '迭代版本', '开放时间(天)',
        '创建时间', '更新时间']
    html_msg += html_table('', table_header, need_exceed_sum)
    subject = "网端需求&迭代卡片统计周报"
    # to_mail = [
    #     'wangduanjishubu@unity-drive.com',
    #     'liguojian@unity-drive.com',
    #     'yaozujie@unity-drive.com']
    # Cc_list = ['chanpinbu@unity-drive.com']
    to_mail = ['caizhisheng@unity-drive.com']
    Cc_list = []
    send_mali(subject, html_msg, to_mail, Cc_list)
    # print(html_msg)
    end_time = time.time()
    print(
        '\033[32mProgram time consuming: %s\033[0m'
        % (end_time - start_time))
