#! /bin/python3
# coding = utf-8
"""该脚本将统计的缺陷数据发送到邮件中"""

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
    return encode


# 获取企业成员
def get_orgmembers():
    params = {'orgId': '5b4ff29669269300014f47a3', 'pageSize': 150}
    res = client.get(url=host + '/api/org/member/list', params=params)
    org_members = {}
    for i in res.json()['result']:
        org_members[i['userId']] = i['name']
    return org_members


# 获取部门成员
def get_members():
    params = {
        'orgId': '5b4ff29669269300014f47a3',
        'deptId': '62859fd92c1198b62bfe7ac5',
        'pageSize': 30}
    res = client.get(url=host+'/api/org/department/members', params=params)
    mem_list = {}
    for i in res.json()['result']:
        mem_list[i['userId']] = i['name']
    print(mem_list)
    return mem_list


# 获取用户参与的项目
def get_usertask(userId):
    params = {'pageSize': 50}
    header2 = {'x-operator-id': userId}
    res = client.get(url=host+'/api/v3/project/user-joined', headers=header2,
                     params=params)
    return res.json()['result']


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


# 获取项目的任务类型
def get_tasktype(projectId):
    res = client.get(
        url=host + '/api/v3/project/%s/scenariofieldconfig/search'
        % (projectId))
    tasktype_list = {}
    for i in res.json()['result']:
        tasktype_list[i['name']] = i['id']
    return tasktype_list


# 获取项目标签
def get_tag(projectId):
    res = client.get(url=host + '/api/v3/project/%s/tag/search' % (projectId))
    tag_list = {}
    for i in res.json()['result']:
        tag_list[i['id']] = i['name']
    return tag_list


# 指定项目中每个人的任务
def get_task(client, TQL, projectId):
    customfield_list = get_customfield(projectId)
    taskflowstatus_list = get_taskflowstatus(projectId)
    org_members = get_orgmembers()
    tasktype_list = get_tasktype(projectId)
    sfcId = tasktype_list.get('网端缺陷')
    if not sfcId:
        sfcId = tasktype_list.get('缺陷')
    params = {'pageSize': 1000, 'q': 'TQL: sfcId=%s %s' % (sfcId, TQL)}
    res = client.get(
        url=host+'/api/v3/project/%s/task/query'
        % (projectId), params=params)
    if res.json()['count'] == 0:
        return 0
    else:
        count = res.json()['count']
    now_time = datetime.now()
    bug_delay_sum = {}
    time_sum = {}
    done_bug_sum = {}
    taskstatus_sum = {}
    user_sum = {}
    bugtype_sum = {}
    buglevel = None
    buglevel_sum = {}
    bugorigin_sum = {}
    bugenv_sum = {}
    bugback_sum = {}
    serious_bug = 0
    sprint_version = ''
    for i in res.json()['result']:
        bug_name = i['content']
        bug_status = i['isDone']
        username = org_members.get(i['executorId'])
        create_time = datetime.strptime(
            i['created'], "%Y-%m-%dT%H:%M:%S.%fZ")
        create_str = create_time.strftime('%Y/%m/%d')
        update_time = datetime.strptime(
            i['updated'], "%Y-%m-%dT%H:%M:%S.%fZ")
        update_str = update_time.strftime('%Y/%m/%d')
        time_sum[create_str] = time_sum.get(create_str, 0) + 1
        for field in i['customfields']:
            if customfield_list.get(field['cfId']) == '缺陷类型':
                bugtype = field['value'][0]['title']
                bugtype_sum[bugtype] = bugtype_sum.get(bugtype, 0) + 1
            elif customfield_list.get(field['cfId']) == '严重程度':
                buglevel = field['value'][0]['title']
                buglevel_sum[buglevel] = buglevel_sum.get(buglevel, 0) + 1
            elif customfield_list.get(field['cfId']) == '缺陷来源':
                bugorigin = field['value'][0]['title']
                bugorigin_sum[bugorigin] = bugorigin_sum.get(bugorigin, 0) + 1
            elif customfield_list.get(field['cfId']) == '环境信息':
                bugenv = field['value'][0]['title']
                bugenv_sum[bugenv] = bugenv_sum.get(bugenv, 0) + 1
            elif customfield_list.get(field['cfId']) == '前/后端':
                bugback = field['value'][0]['title']
                bugback_sum[bugback] = bugback_sum.get(bugback, 0) + 1
            elif customfield_list.get(field['cfId']) == '版本':
                if field['value']:
                    sprint_version = field['value'][0].get('title', '')
                else:
                    sprint_version = ''
        if bug_status:
            done_bug_sum[update_str] = done_bug_sum.get(update_str, 0) + 1
        else:
            gap_days = (now_time - create_time).days
            if int(gap_days) > 7:
                if projectId == '616ce28fccce3c69eca1b933' or\
                   projectId == '600173319b9da85382df80ed':
                    bug_delay_sum[bug_name] = [
                            create_str, update_str, gap_days, username,
                            buglevel, sprint_version]
                else:
                    bug_delay_sum[bug_name] = [
                        create_str, update_str, gap_days, username, buglevel
                    ]
            if buglevel == '严重' or buglevel == '致命':
                serious_bug += 1
        user_sum[username] = user_sum.get(username, 0) + 1

        taskstatus = taskflowstatus_list.get(i['tfsId'])
        taskstatus_sum[taskstatus] = taskstatus_sum.get(taskstatus, 0) + 1
        # tag = tag_list.get(i['tagIds'][0])
        # tag_sum[tag] = tag_sum.get(tag, 0) + 1
    return count, time_sum, done_bug_sum, taskstatus_sum,\
        user_sum, bugtype_sum, buglevel_sum, bugorigin_sum,\
        bugenv_sum, bugback_sum, bug_delay_sum, serious_bug


# 获取不同项目数据
def project_analysis(project_dict: dict):
    project_count = {}
    project_bug_delay_sum = {}
    project_time_sum = {}
    project_donebug_sum = {}
    project_status_sum = {}
    project_user_sum = {}
    project_bugtype_sum = {}
    project_buglevel_sum = {}
    project_bugorigin_sum = {}
    project_bugenv_sum = {}
    project_bugback_sum = {}
    project_serious_bug = {}
    for name, projectId in project_dict.items():
        if name == '任务流程规范化':
            TQL = 'AND (stageId=6392a4feccb00b0040efa25a OR \
            stageId=63e468e1a1053d001899eb44)'
        elif name == '开机自检':
            TQL = 'AND tasklistId=637f067025d55600403ca0e2'
        elif name == '无人车管理平台Web':
            TQL = 'AND (tasklistId=63c0c43648e35f0018f53cd7 OR \
                    tasklistId=639a8e4b7697d90041644251)'
        elif name == '运营APP':
            TQL = 'AND tasklistId=639a8f86a348fe0040ad39cc'
        else:
            TQL = ''
        count, time_sum, done_bug_sum, taskstatus_sum, user_sum,\
            bugtype_sum, buglevel_sum, bugorigin_sum, bugenv_sum,\
            bugback_sum, bug_delay_sum, serious_bug \
            = get_task(client, TQL, projectId)
        project_count[name] = count
        project_time_sum[name] = time_sum
        project_donebug_sum[name] = done_bug_sum
        project_status_sum[name] = taskstatus_sum
        project_user_sum[name] = user_sum
        project_bugtype_sum[name] = bugtype_sum
        project_buglevel_sum[name] = buglevel_sum
        project_bug_delay_sum[name] = bug_delay_sum
        project_serious_bug[name] = serious_bug
        if name != '监控中心' and name != '开机自检':
            project_bugorigin_sum[name] = bugorigin_sum
            project_bugenv_sum[name] = bugenv_sum
            project_bugback_sum[name] = bugback_sum
    return project_count, project_time_sum, project_donebug_sum,\
        project_status_sum, project_user_sum, project_bugtype_sum,\
        project_buglevel_sum, project_bugorigin_sum, project_bugenv_sum,\
        project_bugback_sum, project_bug_delay_sum, project_serious_bug


# 将每日数据转换成每月数据
def month_transform(project_day_sum: dict):
    project_month_sum = {}
    for item in project_day_sum.values():
        for key, num in item.items():
            new_key = key[:-3]
            project_month_sum[new_key] = \
                project_month_sum.get(new_key, 0) + num
    return project_month_sum


# def table_transform(project_count, project_donebug_sum, project_serious_bug):
#     """将数据转换成表格形式"""
#     project_table_data = {}
#     for project, value in project_count.items():
#         total_done = sum(project_donebug_sum[project].values())
#         leave_bug = value - total_done
#         project_table_data[project] = [
#                 value, total_done, leave_bug, project_serious_bug[project]]
#     return project_table_data


# def html_table(title, table_header: list, table_content, width='1200'):
#     """绘制html表格"""
#     html_title = '<table border="1" bordercolor="#c8c9cc" width=%s \
#         cellpadding="5" cellspacing="0" "style=""微软雅黑",Helvetica,\
#         Arial,sans-serif;font-weight:bold;font-size:14px;">\
#         <tr><td colspan="8" style="text-align:center;border:none;\
#         font-size:16px;color:#4476ff;padding-bottom:16px">%s</td>\
#         </tr>' % (width, title)
#     html_header = '<tr>'
#     for header in table_header:
#         if header == 'BUG名称':
#             html_header += '<td bgcolor="#e1e4eb" style="font-weight:bold;\
#                 text-align:center; width:50%%">%s</td>' % (header)
#         else:
#             html_header += '<td bgcolor="#e1e4eb" style="font-weight:bold;\
#             text-align:center">%s</td>' % (header)
#     html_header += '</tr>'
#     html_content = ''
#     for key, item in table_content.items():
#         html_content += '<tr><td>%s</td>' % (key)
#         for value in item:
#             if value == '严重' or value == '致命':
#                 html_content += '<td style="text-align:center; color:red"\
#                     >%s</td>' % (value)
#             else:
#                 html_content += '<td style="text-align:center">%s</td>'\
#                     % (value)
#         html_content += '</tr>'
#     _html_table = html_title + html_header + html_content + '</table><br><br>'
#     return _html_table


# @retrying.retry(stop_max_attempt_number=3, wait_fixed=60000)
# def send_mali(subject, content, to_mail: list):
#     """发送邮件"""
#     message = MIMEMultipart()
#     message.attach(MIMEText(content, 'html', 'utf-8'))
#     message['Subject'] = Header(subject, 'utf-8')
#     smtp_server = 'smtp.exmail.qq.com'
#     mail_user = 'noreply@unity-drive.com'
#     from_mail = 'caizhisheng<noreply@unity-drive.com>'
#     mail_pass = 'vKaWcVGGJkwn3EXB'
#     message['From'] = from_mail
#     message['To'] = ','.join(to_mail)
#     try:
#         s = smtplib.SMTP_SSL(smtp_server, '465')
#         s.login(mail_user, mail_pass)
#         s.sendmail(from_mail, to_mail, message.as_string())
#         s.quit()
#         print('successfully sent email')
#     except smtplib.SMTPException as e:
#         print("Error: unable to send email, %s" % e)


if __name__ == '__main__':
    start_time = time.time()
    token = get_apptoken('63ad342a6aa592f07643d034',
                         'BMeIMuNiCPtaelXcbfoznWjzABuXldeg')
    host = 'https://open.teambition.com'
    header = {
        'Authorization': 'Bearer '+token,
        'X-Tenant-Type': 'organization',
        'X-Tenant-Id': '5b4ff29669269300014f47a3'}
    projectId = '63218086700e621f7bd2748e'
    project_dict = {
        '任务流程规范化': '62dfab5fd51a977b23f51970',
        '开机自检': '63218086700e621f7bd2748e',
        '监控中心': '62a9afb92ed5566088cc0840',
        '无人车不同模式': '62df473b376ec29c45950b63',
        '无人车管理平台Web': '616ce28fccce3c69eca1b933',
        '运营APP': '600173319b9da85382df80ed',
        '大屏展示解决方案': '63218048a0263948c1901ffb'}
    with httpx.Client(headers=header) as client:
        project_count, project_time_sum, project_donebug_sum,\
            project_status_sum, project_user_sum, project_bugtype_sum,\
            project_buglevel_sum, project_bugorigin_sum, project_bugenv_sum,\
            project_bugback_sum, project_bug_delay_sum, project_serious_bug \
            = project_analysis(project_dict)
    # project_table_data = table_transform(
    #         project_count, project_donebug_sum, project_serious_bug)
    # html_msg = '<h3>一、总体数据(<a href="http://10.10.10.35" target="_blank" \
    #         rel="noopener noreferrer">点击查看详细图表数据</a>)</h3>'
    # table_header = ['项目名称', '总BUG数', '已解决BUG数', '剩余BUG数', '剩余严重BUG数']
    # html_msg += html_table('项目BUG数据预览', table_header, project_table_data)
    # html_msg += '<h3>二、逾期BUG提醒</h3>'
    # for name, content in project_bug_delay_sum.items():
    #     if name == '无人车管理平台Web' or name == '运营APP':
    #         table_header = [
    #             'BUG名称', 'BUG创建时间', 'BUG更新时间', 'BUG开放时间(天)',
    #             '执行人', '严重程度', '迭代版本']
    #     else:
    #         table_header = [
    #             'BUG名称', 'BUG创建时间', 'BUG更新时间', 'BUG开放时间(天)',
    #             '执行人', '严重程度']
    #     if content:
    #         html_msg += html_table(name, table_header, content)
    # subject = "网端缺陷统计周报"
    # # to_mail = [
    # #         'wangduanjishubu@unity-drive.com',
    # #         'linjinyan@unity-drive.com',
    # #         'liqingwei@unity-drive.com',
    # #         'xudongdong@unity-drive.com',
    # #         'yaozujie@unity-drive.com',
    # #         'liguojian@unity-drive.com']
    # to_mail = ['caizhisheng@unity-drive.com']
    # try:
    #     send_mali(subject, html_msg, to_mail)
    # except Exception as e:
    #     print(e)
    # end_time = time.time()
    # print(
    #     '\033[32mProgram time consuming: %s\033[0m'
    #     % (end_time - start_time))
